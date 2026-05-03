# ===========================
# CONFIGURACIÓN DE ÍNDICES POR JUEGO
# Cada juego tiene su colección ChromaDB y sus secciones
# ===========================

INDEX_CONFIG = {
    ###
    # TRENCH CRUSADE
    ###
    "trench_crusade": {
        "collection": "trench_crusade",
        "base_subdir": "trench_crusade_files",
        "sections": {
            "rules": {
                "description": "Reglas generales del juego, turnos y activaciones, mecánicas de combate, movimiento, chequeos de habilidad y estructura del turno.",
                "data_subdir": "rules",
                "page_offset": 22 #many
            },
            "armamento": {
                "description": "Armamento, armadura y equipamiento disponibles. Perfiles de armas, armaduras y reglas de equipo. PERO LOS COSTES ESTAN EN SUS FACCIONES RESPECTIVAS.",
                "data_subdir": "battlekit",
                "page_offset": 67 #many
            },
            "scenarios": {
                "description": "Escenarios de juego. Tamaño de la mesa, terreno, objetivos de misión, reglas de despliegue, condiciones de victoria y duración.",
                "data_subdir": "scenarios",
                "page_offset": 143
            },
            "campaigns": {
                "description": "Reglas para campañas. Santos/Demonios patrones, exploración, heridas y bajas, refuerzos, habilidades y experiencia.",
                "data_subdir": "campaign",
                "page_offset": 86 #many
            },
            "glossary": {
                "description": "Glosario de términos y keywords de armas y personajes utilizados en el juego.",
                "data_subdir": "glossary",
                "page_offset": 53 #many
            },
            "faction_heretics": {
                "description": "Facción <Legión Herética>/<Heréticos>/<HL>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/heretics",
                "page_offset": 104
            },
            "faction_blackgrial": {
                "description": "Facción <Culto de el Grial Negro>/<Grial Negro>/<BG>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/grial",
                "page_offset": 126
            },
            "faction_court": {
                "description": "Facción <Corte de la serpiente de siete cabezas>/<Corte>/<Serpiente>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/court",
                "page_offset": 145
            },
            "faction_sultanate": {
                "description": "Facción <Sultanato de Hierro>/<Sultanato>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/sultanate",
                "page_offset": 72
            },
            "faction_pilgrims": {
                "description": "Facción <Peregrinos de las Trincheras>/<Peregrinos>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/pilgrims",
                "page_offset": 48
            },
            "faction_antioch": {
                "description": "Facción <Principado de Nueva Antioquía>/<Nueva Antioquía>/<NA>: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/antioch",
                "page_offset": 22
            },
            "faction_mercenaries": {
                "description": "<Mercenarios> contratables por facciones: unidades, lore, habilidades, armas especiales y costes.",
                "data_subdir": "factions/mercenaries",
                "page_offset": 171
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
                "data_subdir": "rules",
                "page_offset": 2
            },
            "hostiles": {
                "description": "Listado y reglas de los enemigos ('hostiles') en The Last War. Incluye su activación, comportamiento, perfiles (HP, Moral, Armadura, Ataques, Especiales), moral, y generación aleatoria. Cada hostil tiene reglas especiales únicas, desde efectos de gas, regeneración, inmunidades, hasta ataques devastadores y habilidades de saqueo. Se incluyen tanto criaturas sobrenaturales como humanos y máquinas, con perfiles resumidos para referencia rápida durante la partida.",
                "data_subdir": "hostiles",
                "page_offset": 44
            },
            "campaign": {
                "description": "Reglas y gestión de la campaña y el postpartida. La campaña se gestiona tras cada escenario: se resuelven muertes y lesiones, se ganan recursos y experiencia, se pueden contratar nuevos miembros, comprar mejoras de búnker, reasignar equipo y calcular puntuación final. Incluye reglas para lesiones permanentes, artefactos únicos, y formas de progresión o recuperación de la banda.",
                "data_subdir": "campanya",
                "page_offset": 92
            },
            "tank_bunker": {
                "description": "Reglas y gestión de Tanque, Búnker y Campaña en The Last War. El tanque es esencial para escapar y está compuesto por varios componentes (motor, orugas, cañón principal, armadura, armas secundarias, munición), cada uno con funciones y reglas específicas. El tanque requiere tripulación con roles definidos (conductor, artillero, ingeniero) y puede ser reparado o mejorado entre escenarios. El búnker de la banda actúa como base: permite almacenar equipo, obtener mejoras (a cambio de recursos), reclutar miembros y animales de servicio, y acceder a beneficios como curación y equipo extra entre partidas.",
                "data_subdir": "tanque_bunker",
                "page_offset": 96
            },
            "scenarios": {
                "description": "Lista de escenarios jugables en The Last War, cada uno con objetivos, recompensas y condiciones únicas. Incluye reglas para despliegue, botín, amenazas, modos solitario y cooperativo, y condiciones especiales de terreno y clima. Los escenarios forman parte de una campaña narrativa donde la banda busca piezas para un tanque y la supervivencia en un mundo devastado. Se detalla también el modo 'Guerra sin Fin' para partidas aleatorias y de mayor escala.",
                "data_subdir": "escenarios",
                "page_offset": 60
            },
        }
    },
}

GAMES = list(INDEX_CONFIG.keys())