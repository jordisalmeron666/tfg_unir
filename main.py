"""
main.py — Punto de entrada del bot de Telegram para consultas de reglamentos de wargames.

Arquitectura general:
  - El bot recibe mensajes de usuarios autorizados a través de la API de Telegram (long-polling).
  - Las preguntas de texto libre se pasan al orquestador LLM (`llm_handler`), que utiliza
    herramientas RAG (Retrieval-Augmented Generation) sobre ChromaDB para buscar fragmentos
    relevantes de los reglamentos y construir la respuesta.
  - El usuario puede cambiar el juego activo en cualquier momento con /game; cada juego tiene
    su propia colección en ChromaDB (ver `indexes.py` e `INDEX_CONFIG`).
  - Las respuestas largas se envían en varios mensajes para respetar el límite de 4096 caracteres
    de la API de Telegram.

Flujo principal:
    Telegram → handle_message → orchestrate_answer_with_tools → send_in_chunks → Telegram
"""

import logging
import os
import subprocess

from telegram import Update, constants
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup   # para el menú inline de /game
from telegram.ext import CallbackQueryHandler                       # para recibir la pulsación del botón inline
import chromadb

from config import settings           # Pydantic-settings: variables de entorno tipadas
from indexes import GAMES, INDEX_CONFIG  # GAMES: lista de claves; INDEX_CONFIG: configuración por juego
from llm_handler import orchestrate_answer_with_tools, load_game_answerer_model


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
# El nivel se toma de la variable de entorno LOG_LEVEL (default WARNING).
# El formato incluye timestamp, nivel, nombre de función y mensaje para
# facilitar la depuración en producción.
logging.basicConfig(
    level=settings.logging_level,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
)
# httpx es la librería HTTP que usa python-telegram-bot internamente.
# Genera un log por cada petición a la API de Telegram, lo que resulta
# muy ruidoso en modo DEBUG; lo silenciamos a WARNING.
logging.getLogger("httpx").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# ESTADO GLOBAL DE SESIÓN
# ---------------------------------------------------------------------------
# Juego activo por defecto al arrancar el bot.
# Se actualiza mediante el comando /game → set_game_button.
# NOTA: al ser una variable de módulo es compartida por todos los usuarios;
#       si en el futuro se necesita estado por usuario habría que usar
#       context.user_data o una estructura de datos indexada por user_id.
GAME_SELECTED = "trench_crusade"


# ===========================================================================
# HANDLERS DEL BOT
# ===========================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start con un saludo personalizado.

    Se registra con un filtro de usuario autorizado, por lo que sólo
    llegará aquí si el remitente está en settings.authd_users.

    Args:
        update:  Objeto Telegram con toda la información del evento.
        context: Contexto de la aplicación (bot, user_data, etc.).
    """
    user = update.effective_user
    # reply_html permite usar HTML y la mención del usuario es un enlace
    # con el nombre de Telegram del destinatario.
    await update.message.reply_html(rf"Bienvenida {user.mention_html()}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /help con información de diagnóstico y uso del bot.

    Muestra:
      - Datos del usuario que ejecuta el comando (id, username).
      - Información del host donde corre el bot (útil para depuración en contenedor).
      - Estado del bot (id, username, usuarios autorizados).
      - Juego activo actualmente y lista de todos los juegos con sus secciones
        indexadas en ChromaDB.
      - Lista de comandos disponibles.

    Args:
        update:  Objeto Telegram con toda la información del evento.
        context: Contexto de la aplicación (bot, user_data, etc.).
    """
    # Consulta la información del propio bot a la API de Telegram
    botid = await context.bot.get_me()

    # Construye dinámicamente la lista de juegos a partir de INDEX_CONFIG
    # (fuente de verdad en indexes.py) para que se actualice automáticamente
    # al añadir nuevos juegos sin tocar este handler.
    games_list = "\n".join(
        f"    - «{game_key}»: <i>{', '.join(game_config['sections'].keys())}</i>"
        for game_key, game_config in INDEX_CONFIG.items()
    )

    # subprocess.check_output(["hostname", "-I"]) devuelve todas las IPs del host;
    # tomamos sólo la primera (.split()[0]) para mostrarla de forma limpia.
    await update.message.reply_text(
        "User id: " + str(update.effective_user.id)
        + "\nUsername: " + str(update.effective_user.username)
        + "\nHostname: " + str(os.uname()[1])
        + " - " + subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        + "\n<i>Salme 2026</i>"
        + "\n------------------"
        + "\nChat id: " + str(update.message.chat_id)
        + "\nBot id: " + str(botid.id)
        + "\nBotname: " + str(botid.username)
        + "\nAutorizados: " + str(settings.authd_users)
        + "\n------------------"
        + f"\n<b>Juego actual:</b> {GAME_SELECTED}"
        + f"\n\n<b>Juegos disponibles:</b>\n{games_list}"
        + "\n------------------"
        + "\nComandos:"
        + "\n/help - Esta ayuda"
        + "\n/game - Cambiar juego",
        parse_mode="HTML"
    )

# ===========================================================================
# ENVÍO DE RESPUESTAS EN CHUNKS
# ===========================================================================

async def send_in_chunks(
    update,
    message_provisional,
    content,
    chunk_size: int = 4090,
    parse_mode=False
):
    """Envía un texto largo dividido en múltiples mensajes de Telegram.

    La API de Telegram impone un límite de 4096 caracteres por mensaje.
    Esta función divide el contenido en «chunks» intentando respetar
    límites naturales del texto (saltos de línea → puntuación → espacios)
    para no cortar palabras ni frases a mitad.

    Estrategia de división (por orden de prioridad):
      1. Último salto de línea '\\n' dentro de los últimos `search_offset` caracteres.
      2. Último signo de puntuación ('.', ',', '!', '?', ';', ':') en el mismo rango.
      3. Último espacio en blanco ' ' en el mismo rango.
      4. Si ninguno de los anteriores funciona, corte forzado en `chunk_size`.

    El primer chunk edita el mensaje «Procesando...» que ya existe en el chat
    (evita un flash de mensajes). Los chunks siguientes se envían como nuevas
    respuestas al mensaje original del usuario.

    Args:
        update:              Objeto Telegram del evento original (necesario para reply_text).
        message_provisional: Mensaje de «Procesando...» ya enviado; será editado con el primer chunk.
        content:             Texto completo a enviar.
        chunk_size:          Tamaño máximo de cada chunk en caracteres (default 4090, algo menor
                             que el límite de 4096 para dejar margen a parse_mode).
        parse_mode:          Modo de parseo de Telegram ('HTML', 'MarkdownV2', etc.) o False
                             para texto plano.
    """
    # Rango hacia atrás (en caracteres) desde el límite ideal en el que
    # buscar un punto de corte más natural.
    search_offset = 100
    punctuation = '.,!?;:'   # Caracteres considerados «buena» frontera de frase
    current_pos = 0
    is_first_chunk = True    # Controla si editar el provisional o enviar nuevo mensaje

    try:
        while current_pos < len(content):
            potential_end = current_pos + chunk_size

            # --- Calcular dónde cortar este chunk ---
            if potential_end >= len(content):
                # El texto restante cabe entero: no hace falta buscar corte
                split_pos = len(content)
            else:
                actual_end = potential_end
                found_split = False  # noqa: F841 — señalizador para legibilidad
                # Ventana de búsqueda hacia atrás: nunca retroceder antes de current_pos
                search_start = max(current_pos, potential_end - search_offset)

                # 1. Buscar el último '\n' en la ventana
                newline_pos = content.rfind('\n', search_start, actual_end)
                if newline_pos != -1:
                    split_pos = newline_pos + 1   # corte *después* del '\n'
                    found_split = True
                else:
                    # 2. Buscar la última puntuación en la ventana
                    best_punc_pos = -1
                    for punc in punctuation:
                        punc_pos = content.rfind(punc, search_start, actual_end)
                        if punc_pos > best_punc_pos:
                            best_punc_pos = punc_pos

                    if best_punc_pos != -1:
                        split_pos = best_punc_pos + 1   # corte *después* del signo
                        found_split = True
                    else:
                        # 3. Buscar el último espacio en la ventana
                        space_pos = content.rfind(' ', search_start, actual_end)
                        if space_pos != -1:
                            split_pos = space_pos + 1   # corte *después* del espacio
                            found_split = True
                        else:
                            # 4. Corte forzado: ningún límite natural encontrado
                            split_pos = actual_end

            # Salvaguarda: si la lógica de división devuelve una posición que no avanza
            # (p. ej. split_pos <= current_pos), forzamos avance mínimo para evitar
            # un bucle infinito.
            if split_pos <= current_pos:
                split_pos = min(current_pos + chunk_size, len(content))

            chunk = content[current_pos:split_pos]

            # Guardia contra chunks vacíos (no debería ocurrir, pero por robustez)
            if not chunk:
                logging.warning(f"Se generó un chunk vacío en la posición {current_pos}. Saltando.")
                current_pos = min(current_pos + chunk_size, len(content))
                if current_pos == split_pos:
                    current_pos = len(content)   # Forzar salida del bucle
                continue

            logging.debug(f"Chunk (len: {len(chunk)}): {chunk[:100]}...")

            # --- Enviar el chunk ---
            if is_first_chunk:
                # Primer chunk: edita el mensaje provisional «Procesando...»
                # en lugar de enviar un mensaje nuevo (mejor UX).
                if not parse_mode:
                    await message_provisional.edit_text(chunk)
                else:
                    await message_provisional.edit_text(chunk, parse_mode=parse_mode)
                is_first_chunk = False
            else:
                # Chunks adicionales: nuevas respuestas al mensaje original del usuario
                if not parse_mode:
                    await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(chunk, parse_mode=parse_mode)

            current_pos = split_pos   # Avanzar el cursor al siguiente chunk

    except Exception as e:
        # Registramos el traceback completo para facilitar la depuración
        logging.error(f"Error al enviar el contenido en chunks: {str(e)}", exc_info=True)
        try:
            # Intentar notificar al usuario en Telegram que algo falló
            error_message = f"Hubo un error al procesar y enviar el contenido completo: {str(e)}"
            if is_first_chunk:
                # El error ocurrió antes de enviar el primer chunk: editar el provisional
                await message_provisional.edit_text(error_message[:4090])
            else:
                # Ya se enviaron chunks previos: nuevo mensaje de error
                await update.message.reply_text(error_message[:4090])
        except Exception as report_e:
            # Si incluso el reporte de error falla, sólo queda loggearlo
            logging.error(f"No se pudo ni siquiera reportar el error en Telegram: {str(report_e)}") 



# ===========================================================================
# HANDLER DE SELECCIÓN DE JUEGO
# ===========================================================================

async def set_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /game mostrando un teclado inline con los juegos disponibles.

    Genera un botón por cada entrada de la lista GAMES (importada de indexes.py)
    y añade un botón de cancelación al final. La pulsación de cualquier botón
    lanza el callback `set_game_button`.

    El callback_data de cada botón sigue el esquema «game_<nombre_juego>» para
    que `set_game_button` pueda identificarlo de forma fiable.

    Args:
        update:  Objeto Telegram con toda la información del evento.
        context: Contexto de la aplicación.
    """
    # Construir la matriz de botones: una fila por juego + fila de cancelación
    keyboard = [
        [InlineKeyboardButton(game.strip(), callback_data=f"game_{game.strip()}")]
        for game in GAMES
    ]
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_game_select")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    logging.info(f"User {update.effective_user.id} is selecting game")
    await update.message.reply_text(
        f'🎲 Juego actual: <b>{GAME_SELECTED}</b>\n\nSelecciona el juego:',
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


async def set_game_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la pulsación de un botón del teclado inline de /game.

    Identifica la acción por el campo `callback_data` del botón pulsado:
      - «cancel_game_select»: cancela la selección sin cambiar el juego activo.
      - «game_<nombre>»: cambia el juego activo a <nombre> y recarga el modelo
        de respuesta correspondiente (llama a `load_game_answerer_model`).

    Modifica la variable global `GAME_SELECTED` para reflejar el cambio en
    todos los handlers posteriores.

    Args:
        update:  Objeto Telegram con toda la información del evento.
        context: Contexto de la aplicación.
    """
    query = update.callback_query
    user_id = update.effective_user.id

    # Siempre hay que confirmar la recepción del callback para que Telegram
    # quite el indicador de «cargando» del botón pulsado.
    await query.answer()
    option_selected = query.data

    if option_selected == "cancel_game_select":
        await query.edit_message_text(text="🚫 Selección de juego cancelada.")
        logging.info(f"User {user_id} cancelled game selection")
        return

    if option_selected.startswith("game_"):
        game_name = option_selected.replace("game_", "")

        # «global» necesario para reasignar la variable de módulo desde dentro
        # de una función; sin él Python crearía una variable local.
        global GAME_SELECTED
        GAME_SELECTED = game_name

        # Precarga el modelo/prompt específico del juego seleccionado para que
        # la primera consulta no sufra la latencia de inicialización.
        load_game_answerer_model(game_name)

        logging.info(f"User {user_id} selected game: {game_name}")
        await query.edit_message_text(
            text=f"🎲 Juego seleccionado: <b>{game_name}</b>",
            parse_mode="HTML"
        )



# ===========================================================================
# HANDLER DE MENSAJES DE TEXTO
# ===========================================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa los mensajes de texto libre recibidos por el bot.

    Flujo:
      1. Envía inmediatamente un mensaje provisional «Procesando...» para dar
         feedback visual al usuario mientras se genera la respuesta (puede tardar
         varios segundos si el LLM hace múltiples llamadas a herramientas RAG).
      2. Activa el indicador de «escribiendo...» en el chat (ChatAction.TYPING).
      3. Invoca al orquestador LLM, que usa el juego activo (GAME_SELECTED) para
         elegir la colección ChromaDB correcta y construir la respuesta.
      4. Envía la respuesta al chat, dividida en chunks si supera el límite de
         caracteres de Telegram.

    Args:
        update:  Objeto Telegram con toda la información del evento.
        context: Contexto de la aplicación.
    """
    user_text = update.message.text
    chat_id = update.effective_chat.id

    logging.info(f"Received message from chat_id {chat_id}: {user_text}")

    # Mensaje provisional: aparece de inmediato para que el usuario no piense
    # que el bot está caído mientras el LLM procesa la pregunta.
    message_provisional = await update.message.reply_text("Procesando...")

    # El indicador de «escribiendo» en Telegram expira a los ~5 s;
    # para respuestas largas sería necesario renovarlo, pero para el uso
    # habitual es suficiente con enviarlo una vez.
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    # El orquestador recibe el texto del usuario y el mensaje provisional
    # (por si quiere actualizarlo con mensajes de estado intermedios).
    answer = await orchestrate_answer_with_tools(user_text, message_provisional)

    # Envío de la respuesta, posiblemente en varios mensajes si es larga.
    # parse_mode="HTML" porque el LLM genera etiquetas <b>, <i>, etc.
    await send_in_chunks(update, message_provisional, answer, parse_mode="HTML")


# ===========================================================================
# HANDLER DE ERRORES GLOBALES
# ===========================================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador de errores global de python-telegram-bot.

    Telegram PTB captura cualquier excepción no controlada que ocurra en un
    handler y la pasa aquí. Esto evita que el bot muera silenciosamente.

    Acciones:
      - Registra el error en el log con traceback completo.
      - Si el error está asociado a un mensaje de usuario (Update válido),
        notifica al usuario para que sepa que algo falló.

    NOTA: en producción conviene no enviar `context.error` al usuario
    (podría filtrar información sensible); aquí se mantiene por ser un TFG
    en entorno controlado con usuarios de confianza.

    Args:
        update:  Puede ser un objeto Update o cualquier otro objeto; por eso
                 el tipo es `object` y no `Update`.
        context: Contexto de la aplicación; `context.error` contiene la excepción.
    """
    print(f"Update {update} caused error {context.error}")
    logging.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

    # Notificamos al usuario sólo si hay un mensaje al que responder
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            f"¡Ups! Update {update}\n caused error\n {context.error}"
        )


# ===========================================================================
# ARRANQUE Y VERIFICACIÓN INICIAL
# ===========================================================================

# ID del usuario administrador al que se envían las notificaciones de arranque.
# Se toma de settings para no hardcodear valores en el código.
NOTIFY_USER_ID = settings.admin_user


async def startup_check(application: Application) -> None:
    """Hook de post-inicialización: verifica ChromaDB y notifica al administrador.

    Se ejecuta una sola vez justo después de que la aplicación Telegram esté
    lista pero antes de empezar a recibir mensajes. Permite detectar de inmediato
    si alguna colección no ha sido indexada, sin esperar a que un usuario haga
    una consulta.

    Comprueba cada juego definido en INDEX_CONFIG:
      - Si su colección existe en ChromaDB: la añade a la lista «ready».
      - Si no existe: la añade a la lista «missing».

    Envía al administrador (NOTIFY_USER_ID) un resumen con el estado de todas
    las colecciones. Si hay colecciones faltantes, el mensaje incluye un aviso
    para lanzar la reindexación.

    Args:
        application: La instancia de Application de python-telegram-bot,
                     necesaria para acceder al bot y poder enviar mensajes.
    """
    try:
        # Conectar al servidor ChromaDB usando las credenciales de configuración.
        # La autenticación se realiza mediante Bearer token en la cabecera HTTP.
        client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            headers={"Authorization": f"Bearer {settings.chroma_auth_token}"}
        )
        # Obtener el conjunto de nombres de colecciones existentes de una vez
        # para no hacer N llamadas (una por juego) al servidor.
        existing = {c.name for c in client.list_collections()}
    except Exception as e:
        # Si ChromaDB no está disponible al arrancar, notificamos y salimos del check.
        # El bot arrancará igualmente, pero las consultas fallarán hasta que ChromaDB esté activo.
        await application.bot.send_message(
            NOTIFY_USER_ID,
            f"⚠️ Error conectando a ChromaDB al arrancar: {e}"
        )
        return

    ready = []
    missing = []
    for game_key, game_config in INDEX_CONFIG.items():
        col = game_config["collection"]
        if col in existing:
            sections = list(game_config["sections"].keys())
            ready.append(
                f"\n    <b>«{game_key}»</b> ({len(sections)} secciones): "
                f"<i>{', '.join(sections)}</i>"
            )
        else:
            missing.append(game_key)

    if not missing:
        # Todas las colecciones están listas: mensaje informativo normal
        msg = "🤖 <b>Hallo.</b> Colecciones disponibles en ChromaDB:\n" + "\n".join(ready)
        await application.bot.send_message(NOTIFY_USER_ID, msg, parse_mode="HTML")
    else:
        # Alguna colección falta: aviso de acción requerida
        missing_str = ", ".join(missing)
        await application.bot.send_message(
            NOTIFY_USER_ID,
            f"⚠️ Colecciones faltantes: <b>{missing_str}</b>\nDebes lanzar una reindexación...",
            parse_mode="HTML"
        )


# ===========================================================================
# FUNCIÓN PRINCIPAL
# ===========================================================================

def main():
    """Configura y arranca el bot de Telegram en modo long-polling.

    Registra todos los handlers en el siguiente orden (el orden importa en PTB:
    el primer handler que coincide es el que se ejecuta):
      - /start  → start_command    (sólo usuarios autorizados)
      - /help   → help_command     (sólo usuarios autorizados)
      - /game   → set_game_command (sólo usuarios autorizados)
      - Callbacks inline → set_game_button (sin filtro de usuario; cualquiera
        que haya recibido el teclado puede pulsarlo, pero en la práctica sólo
        los autorizados pueden obtenerlo)
      - Mensajes de texto (no comandos) → handle_message (sólo autorizados)
      - Handler de errores global → error_handler

    `post_init=startup_check` hace que `startup_check` se ejecute una vez
    al arrancar, antes del primer poll.

    `drop_pending_updates=True` descarta mensajes acumulados mientras el bot
    estuvo offline, evitando responder a preguntas obsoletas al arrancar.
    """
    app = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .post_init(startup_check)   # Hook de verificación de ChromaDB al arrancar
        .build()
    )

    # Comandos — sólo accesibles para los user_id en settings.authd_users
    app.add_handler(CommandHandler("start", start_command, filters=filters.User(settings.authd_users)))
    app.add_handler(CommandHandler("help",  help_command,  filters=filters.User(settings.authd_users)))
    app.add_handler(CommandHandler("game",  set_game_command, filters=filters.User(settings.authd_users)))

    # Callbacks de botones inline del menú /game (no filtramos por usuario aquí
    # porque el filtro ya está implícito: sólo quien recibió el menú puede pulsar)
    app.add_handler(CallbackQueryHandler(set_game_button))

    # Mensajes de texto que no sean comandos (/...) — sólo usuarios autorizados
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.User(settings.authd_users),
            handle_message
        )
    )

    # Handler de errores no controlados: captura excepciones de cualquier handler
    app.add_error_handler(error_handler)

    try:
        print("TFG Bot started. HELLO!")
        # run_polling bloquea hasta recibir SIGINT (Ctrl-C) o SIGTERM.
        # allowed_updates=Update.ALL_TYPES asegura recibir todos los tipos
        # de actualización, incluidos los callbacks inline.
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        logging.info("TFG Bot stopped by user. BYE!")

    except KeyboardInterrupt:
        logging.info("TFG Bot stopped by user. BYE!")

    except Exception as e:
        print(f"Critical error in main loop: {e}")
        logging.critical(f"Critical error in main loop: {e}", exc_info=True)


# ===========================================================================
# PUNTO DE ENTRADA
# ===========================================================================

if __name__ == '__main__':
    # Guardia mínima antes de arrancar: si no hay token no tiene sentido continuar.
    # El token lo lee settings desde la variable de entorno TELEGRAM_BOT_TOKEN.
    if not settings.telegram_bot_token:
        logging.error("Error: TELEGRAM_BOT_TOKEN no está configurado.")
        exit()

    main()

