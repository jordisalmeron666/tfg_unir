import logging, os, subprocess
from telegram import Update, constants
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup #set_game_command
from telegram.ext import CallbackQueryHandler #set_game_command
import chromadb

from config import settings
from indexes import GAMES, INDEX_CONFIG
from llm_handler import orchestrate_answer_with_tools, load_game_answerer_model

# Configuración básica de logging
logging.basicConfig(level=settings.logging_level, 
                    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING) # Silenciar logs muy verbosos de httpx

GAME_SELECTED = "trench_crusade" # Valor por defecto


# ===========================
# HANDLER DEL BOT
# ===========================

###
# Envía un mensaje de bienvenida cuando se ejecuta el comando /start.
###
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    await update.message.reply_html(rf"Bienvenida {user.mention_html()}!")


###
# /help
###
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    botid = await context.bot.get_me()
    # Construir la lista de juegos disponibles a partir de INDEX_CONFIG
    games_list = "\n".join(
        f"    - «{game_key}»: <i>{', '.join(game_config['sections'].keys())}</i>"
        for game_key, game_config in INDEX_CONFIG.items()
    )
   
    await update.message.reply_text(
                                    "User id: " + str(update.effective_user.id)
                                    +"\nUsername: " + str(update.effective_user.username)
                                    +"\nHostname: " + str(os.uname()[1]) + " - " + subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
                                    +"\n<i>Salme 2026</i>"
                                    +"\n------------------"
                                    +"\nChat id: " + str(update.message.chat_id)
                                    +"\nBot id: " + str(botid.id)
                                    +"\nBotname: " + str(botid.username)
                                    +"\nAutorizados: " + str(settings.authd_users)
                                    +"\n------------------"
                                    +f"\n<b>Juego actual:</b> {GAME_SELECTED}"
                                    +f"\n\n<b>Juegos disponibles:</b>\n{games_list}"
                                    +"\n------------------"
                                    +"\nComandos:"
                                    +"\n/help - Esta ayuda"
                                    +"\n/game - Cambiar juego"
                                    , parse_mode="HTML"
                                )

#===========================

###
#   Enviar response en varios chunks / mensajes de Telegram
###
async def send_in_chunks(update, message_provisional, content, chunk_size=4090, parse_mode=False):

    search_offset = 100  # Rango hacia atrás para buscar un punto de división natural
    punctuation = '.,!?;:' # Caracteres de puntuación para buscar división
    current_pos = 0
    is_first_chunk = True # Para saber si editar o responder

    try:
        while current_pos < len(content):
            potential_end = current_pos + chunk_size

            # Si el resto del texto cabe en un chunk, este es el último
            if potential_end >= len(content):
                split_pos = len(content)
            else:
                # Buscar un punto de división más elegante hacia atrás desde potential_end
                actual_end = potential_end
                found_split = False
                # Definir el rango de búsqueda (sin ir antes de current_pos)
                search_start = max(current_pos, potential_end - search_offset)

                # 1. Buscar el último salto de línea ('\n') en el rango
                newline_pos = content.rfind('\n', search_start, actual_end)
                if newline_pos != -1:
                    split_pos = newline_pos + 1 # Dividir *después* del salto de línea
                    found_split = True
                else:
                    # 2. Buscar la última puntuación en el rango
                    best_punc_pos = -1
                    for punc in punctuation:
                        punc_pos = content.rfind(punc, search_start, actual_end)
                        if punc_pos > best_punc_pos:
                            best_punc_pos = punc_pos
                    
                    if best_punc_pos != -1:
                        split_pos = best_punc_pos + 1 # Dividir *después* de la puntuación
                        found_split = True
                    else:
                        # 3. Buscar el último espacio en blanco (' ') en el rango
                        space_pos = content.rfind(' ', search_start, actual_end)
                        if space_pos != -1:
                            split_pos = space_pos + 1 # Dividir *después* del espacio
                            found_split = True

               
            # Extraer el chunk basado en la posición de división encontrada
            if split_pos <= current_pos:
                 # Forzar avance mínimo si la búsqueda inteligente falla y devuelve una posición anterior
                 split_pos = min(current_pos + chunk_size, len(content))


            chunk = content[current_pos:split_pos]

            # Evitar enviar chunks vacíos si la lógica de división resulta en split_pos == current_pos
            if not chunk:
                logging.warning(f"Se generó un chunk vacío en la posición {current_pos}. Saltando.")
                # Forzar avance para evitar bucle infinito si algo va mal
                current_pos = min(current_pos + chunk_size, len(content))
                if current_pos == split_pos: # Si sigue sin avanzar
                    current_pos = len(content) # Forzar salida
                continue

            logging.debug(f"Chunk (len: {len(chunk)}): {chunk[:100]}...") # Log inicio del chunk

            # Si es la primera iteración, edita el mensaje provisional
            if is_first_chunk:
                if not parse_mode:
                    await message_provisional.edit_text(chunk)
                else:
                    await message_provisional.edit_text(chunk, parse_mode=parse_mode)
                is_first_chunk = False # Ya no es el primer chunk
            else:
                # Envía los chunks siguientes como respuesta al mensaje original del usuario
                if not parse_mode:
                    await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(chunk, parse_mode=parse_mode)

            # Actualizar la posición para el siguiente chunk
            current_pos = split_pos

    except Exception as e:
        logging.error(f"Error al enviar el contenido en chunks: {str(e)}", exc_info=True) # Añadir traceback al log
        try:
            # Intentar notificar el error en Telegram
            error_message = f"Hubo un error al procesar y enviar el contenido completo: {str(e)}"
            if is_first_chunk:
                # Si el error ocurrió antes de enviar el primer chunk, editar el provisional
                await message_provisional.edit_text(error_message[:4090]) # Limitar longitud del mensaje de error
            else:
                # Si ya se enviaron chunks, enviar el error como una nueva respuesta
                await update.message.reply_text(error_message[:4090])
                
        except Exception as report_e:
            # Si incluso el reporte de error falla, solo queda loggearlo
            logging.error(f"No se pudo ni siquiera reportar el error en Telegram: {str(report_e)}")


# ===========================
# HANDLER DE JUEGO
# ===========================

###
# Seteo del juego, comando inicial que muestra las opciones
###
async def set_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [[InlineKeyboardButton(game.strip(), callback_data=f"game_{game.strip()}")] for game in GAMES]
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_game_select")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    logging.info(f"User {update.effective_user.id} is selecting game")
    await update.message.reply_text(
        f'🎲 Juego actual: <b>{GAME_SELECTED}</b>\n\nSelecciona el juego:', 
        reply_markup=reply_markup, 
        parse_mode="HTML"
    )


###
# Función para manejar la elección del juego
###
async def set_game_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id

    # Confirma la recepción del callback
    await query.answer()
    option_selected = query.data

    # Si es un callback de cancelación de juego
    if option_selected == "cancel_game_select":
        await query.edit_message_text(text="🚫 Selección de juego cancelada.")
        logging.info(f"User {user_id} cancelled game selection")
        return

    # Si es un callback de juego, procesarlo aquí
    if option_selected.startswith("game_"):
        game_name = option_selected.replace("game_", "")
        global GAME_SELECTED
        GAME_SELECTED = game_name

        load_game_answerer_model(game_name)

        logging.info(f"User {user_id} selected game: {game_name}")
        await query.edit_message_text(text=f"🎲 Juego seleccionado: <b>{game_name}</b>", parse_mode="HTML")


# ===========================

###
#   Manejo de mensajes de texto
###
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    chat_id = update.effective_chat.id

    logging.info(f"Received message from chat_id {chat_id}: {user_text}")
    message_provisional = await update.message.reply_text("Procesando...")
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    answer = await orchestrate_answer_with_tools(user_text, message_provisional)

    await send_in_chunks(update, message_provisional, answer, parse_mode="HTML")



###
# Manejo de errores
###
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:

    print(f"Update {update} caused error {context.error}")
    logging.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    
    # Opcionalmente, informa al usuario que algo salió mal
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(f"¡Ups! Update {update}\n caused error\n {context.error}")




# ===========================
# INICIO DEL PROGRAMA
# ===========================


###
# Verificación de colecciones ChromaDB al arrancar y notificación al usuario
###
NOTIFY_USER_ID = settings.admin_user
async def startup_check(application: Application) -> None:
    """Verifica colecciones ChromaDB al arrancar y notifica al usuario."""
    try:
        client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            headers={"Authorization": f"Bearer {settings.chroma_auth_token}"}
        )
        existing = {c.name for c in client.list_collections()}
    except Exception as e:
        await application.bot.send_message(NOTIFY_USER_ID, f"⚠️ Error conectando a ChromaDB al arrancar: {e}")
        return

    ready = []
    missing = []
    for game_key, game_config in INDEX_CONFIG.items():
        col = game_config["collection"]
        if col in existing:
            sections = list(game_config["sections"].keys())
            ready.append(f"\n    <b>«{game_key}»</b> ({len(sections)} secciones): <i>{', '.join(sections)}</i>")
        else:
            missing.append(game_key)

    if not missing:
        msg = "🤖 <b>Hallo.</b> Colecciones disponibles en ChromaDB:\n" + "\n".join(ready)
        await application.bot.send_message(NOTIFY_USER_ID, msg, parse_mode="HTML")
    else:
        missing_str = ", ".join(missing)
        await application.bot.send_message(
            NOTIFY_USER_ID,
            f"⚠️ Colecciones faltantes: <b>{missing_str}</b>\nDebes lanzar una reindexación...",
            parse_mode="HTML"
        )


###
#  main del bot con el pooling a la espera de comandos
###
def main():
    app = Application.builder().token(settings.telegram_bot_token).post_init(startup_check).build()
    
    app.add_handler( CommandHandler("start", start_command, filters=filters.User(settings.authd_users)) )
    app.add_handler( CommandHandler("help", help_command, filters=filters.User(settings.authd_users)) )
    app.add_handler( CommandHandler("game", set_game_command, filters=filters.User(settings.authd_users)) )
    app.add_handler( CallbackQueryHandler(set_game_button) )

    app.add_handler( MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(settings.authd_users), handle_message) )

    app.add_error_handler(error_handler)

    try:
        # Run the bot until the user presses Ctrl-C
        print("TFG Bot started. HELLO!")
        app.run_polling(allowed_updates=Update.ALL_TYPES , drop_pending_updates=True)
        logging.info("TFG Bot stopped by user. BYE!")

    except KeyboardInterrupt:
        logging.info("TFG Bot stopped by user. BYE!")

    except Exception as e:
        print(f"Critical error in main loop: {e}")
        logging.critical(f"Critical error in main loop: {e}", exc_info=True)





if __name__ == '__main__':
    if not settings.telegram_bot_token:
        logging.error("Error: TELEGRAM_BOT_TOKEN no está configurado.")
        exit()

    main()

