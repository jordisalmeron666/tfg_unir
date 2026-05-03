import os
from pathlib import Path
from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ===========================
# CONFIGURACIONES
# ===========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
usuarios_permitidos_str = os.getenv("USUARIOS_PERMITIDOS", "91385100")
AUTHD_USERS = [int(user_id) for user_id in usuarios_permitidos_str.split(",") if user_id.strip().isdigit()]

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
#MAX_ROUNDS = int(os.getenv("MAX_ROUNDS", 3))

BASE_DIR = os.getenv("BASE_DIR", "/workspaces/tfg_unir/files/")

CHROMA_AUTH_TOKEN = os.getenv("CHROMA_AUTH_TOKEN", "1234567890")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 801))

# ===========================
# CONFIGURACIONES OpenAi
# ===========================

AOAI_API_KEY = os.getenv("AOAI_API_KEY")
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_API_VERSION = os.getenv("AOAI_API_VERSION", "2024-02-15-preview")
AOAI_EMBEDDING_MODEL = os.getenv("AOAI_EMBEDDING_MODEL", "text-embedding-3-large")
AOAI_ROUTING_MODEL = os.getenv("AOAI_ROUTING_MODEL", "gpt-4.1")
AOAI_ANSWERING_MODEL = os.getenv("AOAI_ANSWERING_MODEL", "gpt-4.1")


# ===========================

"""Pydantic model for settings management."""
class Settings(BaseSettings):
    # General config
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    logging_level: str = LOG_LEVEL
    authd_users: list = AUTHD_USERS

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

    # Configuración de índices por juego
    # Cada juego tiene su colección ChromaDB y sus secciones
    index_config: dict = {
        ###
        # TRENCH CRUSADE
        ###
        "trench_crusade": {
            "collection": "trench_crusade",
            "base_subdir": "trench_crusade_files",
            "sections": {
                "rules": {
                    "description": "Reglas generales del juego, turnos y activaciones, mecánicas de combate, movimiento, chequeos de habilidad y estructura del turno.",
                    "data_subdir": "rules"
                },
                "armamento": {
                    "description": "Armamento, armadura y equipamiento disponibles. Perfiles de armas, armaduras y reglas de equipo. PERO LOS COSTES ESTAN EN SUS FACCIONES RESPECTIVAS.",
                    "data_subdir": "battlekit"
                },
                "scenarios": {
                    "description": "Escenarios de juego. Tamaño de la mesa, terreno, objetivos de misión, reglas de despliegue, condiciones de victoria y duración.",
                    "data_subdir": "scenarios"
                },
                "campaigns": {
                    "description": "Reglas para campañas. Santos/Demonios patrones, exploración, heridas y bajas, refuerzos, habilidades y experiencia.",
                    "data_subdir": "campaign"
                },
                "faction_heretics": {
                    "description": "Facción <Legión Herética>/<Heréticos>/<HL>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/heretics"
                },
                "faction_blackgrial": {
                    "description": "Facción <Culto de el Grial Negro>/<Grial Negro>/<BG>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/grial"
                },
                "faction_court": {
                    "description": "Facción <Corte de la serpiente de siete cabezas>/<Corte>/<Serpiente>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/court"
                },
                "faction_sultanate": {
                    "description": "Facción <Sultanato de Hierro>/<Sultanato>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/sultanate"
                },
                "faction_pilgrims": {
                    "description": "Facción <Peregrinos de las Trincheras>/<Peregrinos>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/pilgrims"
                },
                "faction_antioch": {
                    "description": "Facción <Principado de Nueva Antioquía>/<Nueva Antioquía>/<NA>: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/antioch"
                },
                "faction_mercenaries": {
                    "description": "<Mercenarios> contratables por facciones: unidades, lore, habilidades, armas especiales y costes.",
                    "data_subdir": "factions/mercenaries"
                },
            }
        },
        ###
        # LAST WAR
        ###
        "lastwar": {
            "collection": "lastwar",
            "base_subdir": "lastwar_files",
            "sections": {
                "core_rules": {
                    "description": "Reglas básicas de Forbidden Psalm: The Last War. Juego de escaramuzas con miniaturas en un mundo devastado por la guerra y la niebla. Incluye creación de banda (estadísticas, defectos, hazañas, equipo), uso de dados y pruebas DR, reglas de movimiento, combate cuerpo a cuerpo y a distancia, moral, bajas y recuperación, estados y condiciones, uso de manuscritos (magia), animales de servicio, reglas de despliegue, iniciativa y activación, ejemplo de juego, y conversión desde Forbidden Psalm/MÖRK BORG. Se detallan armas, armaduras, equipo, mercenarios, armas secretas y efectos especiales. Explica cómo jugar escenarios, gestionar recursos, y resolver situaciones de campaña y postpartida.",
                    "tags": ["reglas", "banda", "combate", "magia", "mercenarios", "equipo", "armamento"],
                    "data_subdir": "rules"
                },
                "hostiles": {
                    "description": "Listado y reglas de los enemigos ('hostiles') en The Last War. Incluye su activación, comportamiento, perfiles (HP, Moral, Armadura, Ataques, Especiales), moral, y generación aleatoria. Cada hostil tiene reglas especiales únicas, desde efectos de gas, regeneración, inmunidades, hasta ataques devastadores y habilidades de saqueo. Se incluyen tanto criaturas sobrenaturales como humanos y máquinas, con perfiles resumidos para referencia rápida durante la partida.",
                    "tags": ["hostiles", "enemigos", "perfiles", "comportamiento"],
                    "data_subdir": "hostiles"
                },
                "campaign": {
                    "description": "Reglas y gestión de la campaña y el postpartida. La campaña se gestiona tras cada escenario: se resuelven muertes y lesiones, se ganan recursos y experiencia, se pueden contratar nuevos miembros, comprar mejoras de búnker, reasignar equipo y calcular puntuación final. Incluye reglas para lesiones permanentes, artefactos únicos, y formas de progresión o recuperación de la banda.",
                    "tags": ["campaña", "mejoras", "progresión"],
                    "data_subdir": "campanya"
                },
                "tank_bunker": {
                    "description": "Reglas y gestión de Tanque, Búnker y Campaña en The Last War. El tanque es esencial para escapar y está compuesto por varios componentes (motor, orugas, cañón principal, armadura, armas secundarias, munición), cada uno con funciones y reglas específicas. El tanque requiere tripulación con roles definidos (conductor, artillero, ingeniero) y puede ser reparado o mejorado entre escenarios. El búnker de la banda actúa como base: permite almacenar equipo, obtener mejoras (a cambio de recursos), reclutar miembros y animales de servicio, y acceder a beneficios como curación y equipo extra entre partidas.",
                    "tags": ["tanque", "búnker"],
                    "data_subdir": "tanque_bunker"
                },

                "scenarios": {
                    "description": "Lista de escenarios jugables en The Last War, cada uno con objetivos, recompensas y condiciones únicas. Incluye reglas para despliegue, botín, amenazas, modos solitario y cooperativo, y condiciones especiales de terreno y clima. Los escenarios forman parte de una campaña narrativa donde la banda busca piezas para un tanque y la supervivencia en un mundo devastado. Se detalla también el modo 'Guerra sin Fin' para partidas aleatorias y de mayor escala.",
                    "tags": ["escenarios", "objetivos", "partidas"],
                    "data_subdir": "escenarios"
                },
            }
        },

    }

settings = Settings()

print("Configuración cargada:")
print(f"  Base dir: {settings.base_dir}")
print(f"  ChromaDB: {settings.chroma_host}:{settings.chroma_port}")
print(f"  Azure OpenAI Embedding Model: {settings.aoai_embedding_model}")

