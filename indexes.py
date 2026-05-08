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
                "tags": ["reglas", "banda", "combate", "magia", "mercenarios", "equipo", "armamento"],
                "data_subdir": "rules",
                "page_offset": 2
            },
            "hostiles": {
                "description": "Listado y reglas de los enemigos ('hostiles') en The Last War. Incluye su activación, comportamiento, perfiles (HP, Moral, Armadura, Ataques, Especiales), moral, y generación aleatoria. Cada hostil tiene reglas especiales únicas, desde efectos de gas, regeneración, inmunidades, hasta ataques devastadores y habilidades de saqueo. Se incluyen tanto criaturas sobrenaturales como humanos y máquinas, con perfiles resumidos para referencia rápida durante la partida.",
                "data_subdir": "hostiles",
                "tags": ["hostiles", "enemigos", "perfiles", "comportamiento"],
                "page_offset": 44
            },
            "campaign": {
                "description": "Reglas y gestión de la campaña y el postpartida. La campaña se gestiona tras cada escenario: se resuelven muertes y lesiones, se ganan recursos y experiencia, se pueden contratar nuevos miembros, comprar mejoras de búnker, reasignar equipo y calcular puntuación final. Incluye reglas para lesiones permanentes, artefactos únicos, y formas de progresión o recuperación de la banda.",
                "data_subdir": "campanya",
                "tags": ["campaña", "mejoras", "progresión"],
                "page_offset": 92
            },
            "tank_bunker": {
                "description": "Reglas y gestión de Tanque, Búnker y Campaña en The Last War. El tanque es esencial para escapar y está compuesto por varios componentes (motor, orugas, cañón principal, armadura, armas secundarias, munición), cada uno con funciones y reglas específicas. El tanque requiere tripulación con roles definidos (conductor, artillero, ingeniero) y puede ser reparado o mejorado entre escenarios. El búnker de la banda actúa como base: permite almacenar equipo, obtener mejoras (a cambio de recursos), reclutar miembros y animales de servicio, y acceder a beneficios como curación y equipo extra entre partidas.",
                "tags": ["tanque", "búnker"],
                "data_subdir": "tanque_bunker",
                "page_offset": 96
            },
            "scenarios": {
                "description": "Lista de escenarios jugables en The Last War, cada uno con objetivos, recompensas y condiciones únicas. Incluye reglas para despliegue, botín, amenazas, modos solitario y cooperativo, y condiciones especiales de terreno y clima. Los escenarios forman parte de una campaña narrativa donde la banda busca piezas para un tanque y la supervivencia en un mundo devastado. Se detalla también el modo 'Guerra sin Fin' para partidas aleatorias y de mayor escala.",
                "tags": ["escenarios", "objetivos", "partidas"],
                "data_subdir": "escenarios",
                "page_offset": 60
            },
        }
    },

    ###
    # FORBIDDEN PSALM
    ###
    "forbidden_psalm": {
        "collection": "fpsalm",
        "base_subdir": "fpsalm_files",
        "sections": {
            "core_rules": {
                "description": "Reglas principales de Forbidden Psalm, incluyendo la preparación de partida, turnos, activación, acciones, movimiento, combate, moral, estados (Downed, Dead), pruebas (tests), uso de dados, modificadores, y gestión de tesoros. Explica cómo crear y gestionar una warband (banda): asignación de estadísticas, compra de equipo, armas, armaduras, objetos y mascotas, reglas de mercenarios y mejora de banda. Incluye el sistema de Feats y Flaws, reglas de experiencia, heridas, compra/venta de objetos y equipo especial, y el uso de hechizos mediante scrolls. Incluye también reglas de terreno, clima y condiciones especiales.",
                "tags": [ "reglas", "warband", "equipo", "armas", "objetos" ],
                "data_subdir": "rules",
                "page_offset": 2
            },
            "monsters": {
                "description": "Lista y reglas de monstruos en Forbidden Psalm. Incluye perfiles con HP, Moral, ataque, armadura y reglas especiales. Explica activación, moral, interacción con modelos caídos, keywords y cómo afectan los monstruos a la partida. Contiene monstruos únicos como Afanc, Cath Palug, Rat King, Siren, Skeleton, Faecal Ghoul, Spider Queen, Sock Stealing Goblin, Tapeworm Terror, The Silent, y más.",
                "tags": ["hostiles", "enemigos", "perfiles", "comportamiento"],
                "data_subdir": "monsters",
                "page_offset": 79
            },
            "scenarios": {
                "description": "Escenarios para Forbidden Psalm, cada uno con su objetivo principal, recompensas, despliegue, amenazas y reglas especiales. Los escenarios incluyen misiones de exploración, combate, rescate, caza de monstruos, obtención de artefactos y enfrentamientos contra rivales, con despliegue para juego competitivo, cooperativo o solitario. Muchos escenarios presentan reglas de terreno, eventos aleatorios, aparición de monstruos y condiciones de victoria específicas. Cada uno ofrece una narrativa única y desafíos variados en la campaña.",
                "tags": [ "escenarios", "misiones", "tesoros", "campaña" ],
                "data_subdir": "scenarios",
                "page_offset": 84
            },
        }
    },

    ###
    # FORBIDDEN PSALM
    ###
    "zona_alfa": {
        "collection": "zona_alfa",
        "base_subdir": "zona_alfa_files",
        "sections": {
            "core_rules": {
                "description": "Reglamento básico de Zona Alfa. Incluye componentes necesarios y definiciones clave (WYSIWYG, LOS/LOF, unidad, tipos de dados y tiradas críticas). Explica los dos tipos de estadísticas (modelo y arma), y la mecánica central: iniciativa, activación alterna, experiencia de combate (Rookie, Hardened, Veteran) y número de acciones por activación. Detalla las acciones disponibles, el sistema de chequeos de habilidad y tareas complejas, movimiento, terreno, coberturas y cómo afectan el combate. Cubre el combate a distancia y cuerpo a cuerpo, resolución de impactos, heridas, estados (Pinned, Out of Action), uso de Med-Kits, y el sistema de heridas múltiples. Incluye reglas de área de misión: niveles de amenaza (Threat Level), objetivos de misión, límites de turno, Hot Spots y cómo se activan, aparición y control de Hostiles de la Zona (IA, despliegue, acciones), tablas de Salvamento y Anomalías, y efectos ambientales opcionales. Presenta ejemplos de juego y perfiles de muestra.",
                "tags": [ "reglas básicas","acciones","activación","combate","heridas","pinned","med-kit","cobertura","terreno","objetivos","hot spots","hostiles","anomalías","salvamento" ],
                "data_subdir": "rules",
                "page_offset": 5
            },
            "partyrun": { #***
                "description": "Lista y reglas de monstruos en Forbidden Psalm. Incluye perfiles con HP, Moral, ataque, armadura y reglas especiales. Explica activación, moral, interacción con modelos caídos, keywords y cómo afectan los monstruos a la partida. Contiene monstruos únicos como Afanc, Cath Palug, Rat King, Siren, Skeleton, Faecal Ghoul, Spider Queen, Sock Stealing Goblin, Tapeworm Terror, The Silent, y más.",
                "tags": ["hostiles", "enemigos", "perfiles", "comportamiento"],
                "data_subdir": "monsters",
                "page_offset": 79
            },
            "warbands": {
                "description": "Resumen de la gestión y creación de bandas (crews) en Zona Alfa. Incluye la composición y reclutamiento de la tripulación, el sistema de experiencia (Rookie, Hardened, Veteran), la asignación de habilidades (Skills), equipo inicial según experiencia, y el sistema de puntos Khrabrost’ para equilibrar la banda. Explica la selección de Facciones y sus beneficios, así como el sistema de alianzas y enemistades entre ellas. Cubre la progresión post-misión: cómo se obtienen y gastan Avances (mejoras de stats, slots de equipo, nuevas habilidades, promociones) y el sistema de Battle Scars para modelos que quedan fuera de combate. También incluye la economía de Zona Alfa: contratación de nuevos miembros, recompra de armas/equipo y uso de The Stalls para mejorar la banda.",
                "tags": ["bandas","facciones","habilidades","reclutamiento","avances","alianzas","economía"],
                "data_subdir": "warbands",
                "page_offset": 33 # many
            },
            "armory_equip": {
                "description": "Este índice cubre el Armamento, la Armadura y el Equipo disponibles en Zona Alfa. Detalla los diferentes tipos de armas (cuerpo a cuerpo, a distancia, de apoyo, granadas y explosivos), incluyendo sus estadísticas (Alcance, Potencia de Fuego, Daño) y Reglas Especiales (como Fuego Indirecto, Recarga, Munición Limitada, Armas de Apoyo, Servidas por Dotación, y el uso de Plantillas de Área/Llama). Explica cómo las armas de efecto de área interactúan con el terreno. Describe los tipos de Armadura Corporal, desde equipo básico hasta armaduras avanzadas, indicando su Valor de Armadura, penalizaciones de movimiento y efectos especiales (como Objetivo Oscurecido o dados extra en Tiradas de Salvación de Armadura). También menciona la armadura natural de criaturas y las clasificaciones de armadura para vehículos ligeros y robots. Adicionalmente, cubre el sistema de Equipo, explicando el concepto de Slots de Equipo asignados según el nivel de experiencia de los miembros de la tripulación (Novato, Experimentado, Veterano). Lista y describe el Equipo Básico, Avanzado y Especial, detallando sus efectos en el juego y cómo utilizan (o conceden) Slots de Equipo.",
                "tags": ["armamento","equipo","armas","armadura","granadas","explosivos","fuego indirecto","recarga","slots de equipo","valor", "efecto de área"],
                "data_subdir": "armory_equip",
                "page_offset": 24 # many
            },
        }
    },

    ###
    # MORDHEIM DOCUMENTS
    ###
    "mordheim": {
        "collection": "mordheim",
        "base_subdir": "mordheim_files",
        "sections": {
            "core_rules": {
                "description": "Reglas básicas y opcionales de Mordheim, incluyendo la creación y gestión de bandas, secuencia de turnos, movimiento (correr, cargar, escalar, saltar, caer), combate a distancia y cuerpo a cuerpo, heridas, armaduras y salvaciones, psicología (miedo, frenesí, odio, estupidez), experiencia, pruebas de liderazgo, y reglas opcionales como golpes críticos por tipo de arma, monturas, y fallos de armas de pólvora negra. Incluye tablas de referencia para impactos, heridas, críticos y salvaciones, así como reglas para terreno, cobertura, y condiciones de victoria.",
                "tags": ["reglas","movimiento","combate","psicología"],
                "data_subdir": "rules",
                "page_offset": 19 #many
            },
            "armory": {
                "description": "Lista y descripción de todas las armas, armaduras y equipo especial disponibles en Mordheim. Incluye armas cuerpo a cuerpo (mazas, dagas, espadas, hachas, flails, alabardas, lanzas, armas a dos manos, armas élficas y gromril), armas a distancia (arcos, ballestas, hondas, cuchillos arrojadizos, pistolas, mosquetes, blunderbuss, rifle Hochland, etc.), armaduras (ligera, pesada, gromril, ithilmar), escudos, hebillas, y cascos, con sus reglas especiales. También cubre equipo especial y misceláneo (cuerdas, venenos, drogas, amuletos, mapas, animales, tomos, etc).",
                "tags": ["armas","armaduras","equipo"],
                "data_subdir": "armory",
                "page_offset": 40 #many
            },
            "magic": {
                "description": "Lista y descripción de todos los hechizos y habilidades mágicas disponibles en Mordheim. Incluye detalles sobre los diferentes tipos de magia, como la Magia de la Rata Cornuda, Necromancia, y los Rituales del Caos, así como sus efectos, dificultades de lanzamiento y requisitos.",
                "tags": ["magia", "hechizos", "rituales"],
                "data_subdir": "magic",
                "page_offset": 57
            },
            "scenarios": {
                "description": "Escenarios clásicos de Mordheim, incluyendo reglas para la secuencia previa a la batalla, despliegue, condiciones de victoria, experiencia y objetivos especiales. Cada escenario presenta un tipo de enfrentamiento diferente entre bandas rivales, con reglas específicas para el terreno, despliegue, inicio y finalización del juego, y recompensas como fragmentos de wyrdstone y experiencia. Incluye escenarios como Defend the Find, Skirmish, Wyrdstone Hunt, Breakthrough, Street Fight, Chance Encounter, Hidden Treasure, Occupy y Surprise Attack.",
                "tags": ["escenarios","despliegue","wyrdstone","victoria"],
                "data_subdir": "scenarios",
                "page_offset": 110 #many
            },
            "campanya": {
                "description": "Reglas y procedimientos de campaña y postpartida de Mordheim, esenciales para campañas. Incluye la secuencia completa tras cada batalla: resolución de heridas graves (con tablas para Héroes y Secuaces), asignación de experiencia y avances, exploración y búsqueda de wyrdstone (con tabla de exploración y localizaciones especiales), cálculo de ingresos y venta de wyrdstone, contratación de nuevos miembros (incluyendo Hired Swords), búsqueda de objetos raros y comercio (con reglas de rareza y precios), redistribución de equipo, y actualización del rating de la banda. Contempla también el reemplazo de líderes, disolución de bandas, y reglas para adquirir y vender equipo, objetos mágicos y animales. Incluye las tablas de progresión de experiencia y de habilidades por tipo (combate, disparo, académico, fuerza, velocidad).",
                "tags": ["campaña","exploración","heridas","experiencia","comercio", "postpartida"],
                "data_subdir": "campanya",
                "page_offset": 100 #many
            },
            "warbands": {
                "description": "Sección dedicada a la creación, gestión y tipos de bandas de guerra (warbands) en Mordheim. Incluye reglas de reclutamiento, organización en Héroes y Secuaces, listas de equipo, experiencia inicial, reglas especiales y habilidades por banda. Contiene perfiles y reglas para bandas principales (Mercenarios de Reikland, Middenheim, Marienburg; Culto de los Poseídos; Cazadores de Brujas; Hermanas de Sigmar; No Muertos; Skaven; etc), así como reglas para Mutaciones. Cada banda tiene reglas únicas, acceso a equipo y habilidades particulares, límites de reclutamiento y reglas de experiencia.",
                "tags": ["bandas","reclutamiento","heroes","secuaces"],
                "data_subdir": "warbands",
                "page_offset": 64 #many
            },
            "dramatis_personae": {
                "description": "Este índice detalla los personajes especiales ('Dramatis Personae') y mercenarios ('Hired Swords') disponibles en Mordheim y la expansión Empire in Flames. Incluye perfiles de personajes como el Beast Hunter, Balewolf, Highwayman, Roadwarden, Pit Fighter, Ogre Bodyguard, Halfling Scout, Warlock, Freelancer, Elf Ranger, Dwarf Troll Slayer, Aenur (the Sword of Twilight), Johann the Knife, Bertha Bestraufrung (High Matriarch), y Veskit (High Executioner of Clan Eshin). Para cada personaje, se especifica su coste de contratación y mantenimiento (Hire Fee, Upkeep), las warbands que pueden contratarlo (May be Hired), cómo afecta la calificación de la warband (Rating), su perfil de atributos (Profile), equipo (Equipment), habilidades (Skills) y reglas especiales (SPECIAL RULES). También se mencionan reglas generales para reclutar, gestionar y tratar las heridas de los Hired Swords en una campaña.",
                "tags": [ "personajes especiales", "mercenarios", "hired swords", "perfiles", "habilidades" ],
                "data_subdir": "dramatispersonae",
                "page_offset": 131 #many
            },
            "mounts_vehicles": {
                "description": "Este índice cubre las reglas para Monturas (animales de caballería) y Vehículos (carros y barcos) en Mordheim: Empire in Flames. Detalla cómo incluir y manejar animales montados y no montados en una banda, las habilidades de Manejo de Animales, las reglas para montar/desmontar, movimiento (incluyendo restricciones de terreno y bolting), combate montado (incluyendo habilidades especiales de caballería y la tabla 'Whoa Boy!' para heridas del jinete), y perfiles de diferentes animales. También cubre las reglas para Vehículos como Carros y Barcos, incluyendo su movimiento (velocidad según carga, giros, aplicar el látigo), interacción con el terreno, colisiones, capacidad de transporte, embarque/desembarque (incluso en movimiento), disparo desde/hacia vehículos, pérdida de control (animales de tiro) y daño (ubicaciones, efectos).",
                "tags": [ "monturas", "vehiculos", "caballeria", "combate montado" ],
                "data_subdir": "vehicles",
                "page_offset": 24
            },
            "wilderness": {
                "description": "Reglas para partidas ambientadas en la zona salvaje (wilderness) del Imperio. Cubre la idoneidad de las bandas de guerra, el uso de 'Treasures' (tesoros) en lugar de Wyrdstone, y la regla de 'Lost!' para heridas. Detalla varios tipos de terreno (bosques, pantanos, ríos) y sus efectos en el movimiento y combate. Incluye reglas para interactuar con edificios (puertas cerradas, habitantes, combate interior).",
                "tags": [ "wilderness", "terreno", "tesoros", "edificios" ],
                "data_subdir": "wilderness",
                "page_offset": 12
            },
        }
    },


}

GAMES = list(INDEX_CONFIG.keys())