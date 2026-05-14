import os
from pathlib import Path
from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ===========================
# CONFIGURACIONES GENERALES
# ===========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SALME_USR = int(os.getenv("SALME_USR"))
usuarios_permitidos_str = os.getenv("USUARIOS_PERMITIDOS")
AUTHD_USERS = [int(user_id) for user_id in usuarios_permitidos_str.split(",") if user_id.strip().isdigit()]

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")

BASE_DIR = os.getenv("BASE_DIR", "/workspaces/tfg_unir/files/")

# ===========================
# CONFIGURACIONES ChromaDB
# ===========================
CHROMA_AUTH_TOKEN = os.getenv("CHROMA_AUTH_TOKEN")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = int(os.getenv("CHROMA_PORT"))

# ===========================
# CONFIGURACIONES Azure OpenAI
# ===========================
LLM_PROVIDER = "azure_openai"

AOAI_API_KEY = os.getenv("AOAI_API_KEY")
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_API_VERSION = os.getenv("AOAI_API_VERSION")
AOAI_EMBEDDING_MODEL = os.getenv("AOAI_EMBEDDING_MODEL")
AOAI_ROUTING_MODEL = os.getenv("AOAI_ROUTING_MODEL")
AOAI_ANSWERING_MODEL = os.getenv("AOAI_ANSWERING_MODEL")


# ===========================
# PROMPTS
# ===========================
AGENT_SYSTEM_PROMPT = """
Eres un asistente experto en reglamentos de wargames de miniaturas: eres el "praeadiutor scribae Codex Vox".
Tu objetivo es responder a las preguntas de los usuarios basándote únicamente en la información que obtienes de las herramientas/contexto que se te proporciona.
Si tras usar una herramienta el contexto no es suficiente, indícalo claramente.
Cita siempre las secciones consutladas en un último párrafo, si es posible.No añadas información adicional ni especulaciones.
Evita emoticonos e interactuar directamente con el usuario como si fueras un chatbot, eres un proceso de backend.
"""

VALIDATOR_SYSTEM_PROMPT = """
Eres un asistente experto en el reglamento del wargame de miniaturas.
Tu objetivo es revisar la respuesta ofrecida al usuario y verificar si da respuesta efectiva o no a la pregunta formulada. Una respuesta efectiva es aquella que ha encontrado la información relevante en el contexto y la ha presentado de forma clara y concisa.
Pudiera ser que, aun siendo una respuesta clara, no hubiera podido encontrar información en el contexto proporcionado. Así que no la podemos considerar respuesta efectiva, de manera que NO la podemos considerar como aceptable y debes señalarlo así para poder reenrutar la pregunta para proporcionar otro contexto y generar otra respuesta.
Responde únicamente con un objeto JSON con las claves "es_aceptable" (true/false) y "motivo" (una breve explicación).

Aquí te proporciono la pregunta y respuesta:\n\n
"""


# ===========================
# PYDANTIC SETTINGS
# ===========================
class Settings(BaseSettings):
    # General
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    logging_level: str = LOG_LEVEL
    authd_users: list = AUTHD_USERS
    admin_user: int = SALME_USR

    # Rutas
    base_dir: Path = BASE_DIR

    # ChromaDB
    chroma_auth_token: str = CHROMA_AUTH_TOKEN
    chroma_host: str = CHROMA_HOST
    chroma_port: int = CHROMA_PORT

    # Azure OpenAI
    aoai_api_key: str = AOAI_API_KEY or ""
    aoai_endpoint: str = AOAI_ENDPOINT or ""
    aoai_api_version: str = AOAI_API_VERSION
    aoai_embedding_model: str = AOAI_EMBEDDING_MODEL
    aoai_routing_model: str = AOAI_ROUTING_MODEL
    aoai_answering_model: str = AOAI_ANSWERING_MODEL


settings = Settings()

print("Configuración cargada:")
print(f"  Base dir: {settings.base_dir}")
print(f"  ChromaDB: {settings.chroma_host}:{settings.chroma_port}")
print(f"  Azure OpenAI Embedding Model: {settings.aoai_embedding_model}")
print(f"  Azure OpenAI Routing Model: {settings.aoai_routing_model}")
print(f"  Azure OpenAI Answering Model: {settings.aoai_answering_model}")

