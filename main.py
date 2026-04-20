import os, logging, subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ===========================
# CONFIGURACIONES
# ===========================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token del bot de Telegram
USER_AUTORIZADO = int(os.getenv("SALME_USR"))  # ID del usuario o chat de Telegram

# Enable logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
logging.basicConfig(level=LOG_LEVEL, 
                    format='%(asctime)s - %(funcName)s - - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('exec.log'),
                            logging.StreamHandler()
                        ])
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Diccionario para almacenar flujos de autenticación en ejecución
auth_flows = {}


# ===========================
# FUNCIONES
# ===========================
# Add error handler
async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Exception while handling an update: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, there was a network error. Please try again later."
        )


# Comando /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user = update.effective_user
    await update.message.reply_html(rf"Bienvenida {user.mention_html()}!")



###
# /help
###
async def help_command(update: Update, context: CallbackContext) -> None:
    
    botid = await context.bot.get_me()

    await update.message.reply_text(
                                    "User id: " + str(update.effective_user.id)
                                    +"\nUsername: " + str(update.effective_user.username)
                                    +"\nHostname: " + str(os.uname()[1]) + " - " + subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
                                    +"\n------------------"
                                    +"\nChat id: " + str(update.message.chat_id)
                                    +"\nBot id: " + str(botid.id)
                                    +"\nBotname: " + str(botid.username)
                                    +"\nAutorizados: " + str(USER_AUTORIZADO)
                                    +"\n------------------"
                                    , parse_mode="HTML"
                                )
    
###
#   echo chat
###
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


# ===========================
# INICIO DEL PROGRAMA
# ===========================

###
#  main del bot con el pooling a la espera de comandos
###
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler( "start", start_command, filters=filters.User(USER_AUTORIZADO) ))
    app.add_handler(CommandHandler( "help", help_command, filters=filters.User(USER_AUTORIZADO) ))
    app.add_handler(MessageHandler( filters.TEXT & ~filters.COMMAND & filters.User(USER_AUTORIZADO), echo ))

    # Add error handler
    app.add_error_handler(error_handler)

    try:
        # Run the bot until the user presses Ctrl-C
        print("TFG Bot started. HELLO!")
        app.run_polling(allowed_updates=Update.ALL_TYPES , drop_pending_updates=True)
        logger.info("TFG Bot stopped by user. BYE!")

    except KeyboardInterrupt:
        logger.info("TFG Bot stopped by user. BYE!")

    except Exception as e:
        logger.critical(f"Critical error in main loop: {e}", exc_info=True)


if __name__ == "__main__":
    main()