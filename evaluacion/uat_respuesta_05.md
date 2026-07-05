# Encuesta UAT — Respuesta #05

> **Evaluador**: U05 · **Fecha**: 18 junio 2026 · Green

---

## Bloque 0 — Perfil del evaluador

| # | Pregunta | Respuesta |
|---|----------|-----------|
| P0.1 | ¿Cuánto tiempo llevas jugando a wargames de miniaturas? | **> 10 años** |
| P0.2 | ¿Con qué frecuencia consultas un reglamento durante una partida? | **Constantemente** |
| P0.3 | ¿Qué juegos has usado durante las pruebas? | **Trench Crusade, Mordheim, Last War, Zona Alfa, FP Psalm** |
| P0.4 | ¿Con qué tecnología te sientes más cómodo/a? | **Perfil técnico** |

---

## Bloque 1 — Usabilidad e interacción (Telegram)

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| P1.1 | El bot de Telegram es fácil de usar sin instrucciones previas | ☐ | ☐ | ☐ | **✓** | ☐ |
| P1.2 | Formular una pregunta al bot resulta natural e intuitivo | ☐ | ☐ | ☐ | ☐ | **✓** |
| P1.3 | El tiempo de respuesta del bot es aceptable | ☐ | ☐ | ☐ | **✓** | ☐ |
| P1.4 | El bot comunica claramente cuando no encuentra información | ☐ | ☐ | ☐ | ☐ | **✓** |
| P1.5 | Usaría este bot durante una partida real sin interrumpirla | ☐ | ☐ | ☐ | **✓** | ☐ |

**P1.6 (abierta)** — ¿Destacar algún problema/carencia para interactuar con el bot?
- > La latencia es aceptable pero en partidas rápidas o de torneo se siente. Entiendo que hay un pipeline de enrutado + RAG + generación, y eso tiene coste. Para uso casual perfecto, pero para competición haría falta algo más ágil.
- > La ausencia de entrada por voz es el mayor punto débil de UX. En mesa, con miniaturas y dados en la mano, teclear es incómodo.

---

## Bloque 2 — Calidad de las respuestas

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| P2.1 | Las respuestas son precisas y correctas respecto al reglamento | ☐ | ☐ | ☐ | ☐ | **✓** |
| P2.2 | Las respuestas citan la fuente correcta (Sección y pág) | ☐ | ☐ | ☐ | **✓** | ☐ |
| P2.3 | Las respuestas son lo suficientemente completas | ☐ | ☐ | ☐ | ☐ | **✓** |
| P2.4 | Las respuestas son fáciles de entender | ☐ | ☐ | ☐ | ☐ | **✓** |
| P2.5 | El bot nunca inventó información que no estaba en el reglamento | ☐ | ☐ | ☐ | ☐ | **✓** |
| P2.6 | Confío en la respuesta del bot para resolver una duda de regla en partida | ☐ | ☐ | ☐ | ☐ | **✓** |

**P2.7 (abierta)** — ¿Recuerdas alguna respuesta incorrecta o incompleta?
- > Probé los 5 juegos disponibles y en general la calidad es muy alta. En FP Psalm encontré un caso donde el chunk recuperado correspondía a una sección de introducción y no a la regla concreta, así que la respuesta era tangencial. El bot lo reconoció correctamente como respuesta parcial.
- >

**P2.8 (abierta)** — ¿Hubo preguntas que esperabas que el bot respondiera y no pudo?
- > Pregunté por interacciones cross-game ("¿esta regla de Trench Crusade tiene equivalente en Mordheim?") y el bot respondió cada juego por separado, que es lo correcto dado su diseño. No es un fallo, es una limitación conocida del scope.
- >

---

## Bloque 3 — Utilidad y valor percibido

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| P3.1 | El bot resuelve un problema real que tengo como jugador | ☐ | ☐ | ☐ | ☐ | **✓** |
| P3.2 | Usar el bot es más rápido que buscar en el PDF del reglamento | ☐ | ☐ | ☐ | ☐ | **✓** |
| P3.3 | El bot me ahorra tiempo durante la preparación de la partida | ☐ | ☐ | ☐ | ☐ | **✓** |
| P3.4 | Recomendaría este bot a otros jugadores de wargames | ☐ | ☐ | ☐ | ☐ | **✓** |

**P3.5 (abierta)** — ¿Qué es lo más útil del bot para ti?
- > La cobertura multi-juego en un único punto de acceso. Juego a cinco sistemas distintos y tener un solo bot que entiende todos sin configuración previa es extraordinariamente cómodo.

**P3.6 (abierta)** — ¿Qué es lo que más echas de menos en el bot?
- > La memoria de sesión. Actualmente el bot parece gestionar el contexto solo dentro del enrutado de cada consulta, pero no retiene el hilo de la conversación del usuario. Si llevo diez minutos preguntando sobre mi warband de Trench Crusade, la undécima pregunta debería asumir ese contexto sin que tenga que repetirlo.

---

## Bloque 4 — Comparación con alternativas actuales

| # | Pregunta | Respuesta |
|---|----------|-----------|
| P4.1 | ¿Qué usas habitualmente para resolver dudas de reglas? | **PDF, Google** |
| P4.2 | Comparado con buscar en el libro o PDF, el bot te parece... | **Mucho mejor** |
| P4.3 | Comparado con preguntar a otros jugadores, el bot te parece... | **Mejor** |

**P4.4 (abierta)** — ¿Qué ventaja principal tiene el bot frente a cómo resuelves las dudas ahora?
- > Precisión y velocidad combinadas. Google devuelve foros con respuestas incorrectas o desactualizadas. El bot responde desde la fuente canónica siempre.

**P4.5 (abierta)** — ¿Qué ventaja tiene tu método actual frente al bot?
- > El PDF con Ctrl+F permite localizar texto exacto cuando sé la terminología. El bot a veces parafrasea y puede perder matices de reglas muy específicas.

---

## Bloque 5 — Limitaciones y mejoras

**P5.1** — ¿Has encontrado alguno de estos problemas?
- [ ] El bot tardó demasiado en responder
- [ ] El bot no entendió mi pregunta
- [ ] La respuesta fue correcta pero incompleta
- [ ] La respuesta fue incorrecta o contradijo el reglamento
- [ ] El bot dijo no tener información cuando sí la había
- [ ] No supe cómo hacerme entender
- [x] Ningún problema reseñable

**P5.2** — ¿Qué funcionalidad añadirías o mejorarías?
- [x] Más reglamentos de juegos
- [ ] Respuestas sobre trasfondo (lore)
- [x] Respuestas más cortas y directas
- [ ] Respuestas más detalladas con contexto adicional
- [x] Historial de mis preguntas anteriores (contexto de chat)
- [ ] Acceso web o app, no solo Telegram
- [x] Multimodal: envío de audio / imágenes al bot
- [ ] Búsqueda por palabras clave además de lenguaje natural
- [x] Otra: Modo torneo con respuestas ultraconcisas y latencia reducida

**P5.3 (abierta)** — ¿Qué mejoraría más tu experiencia con el bot en una sola frase?
- > Añadir memoria de sesión para que el bot recuerde el contexto del usuario a lo largo de la conversación, no solo dentro del enrutado de cada pregunta individual.

---

## Bloque 6 — Valoración global

| # | Pregunta | Respuesta |
|---|----------|-----------|
| P6.1 | Valoración global del sistema | **9 / 10** |
| P6.2 | ¿Cumple el bot su objetivo principal? | **Sí, plenamente** |
| P6.3 | ¿Lo usarías de forma regular si estuviera disponible? | **Sí, sin duda** |

**P6.4 (abierta)** — Comentarios finales, sugerencias o cualquier cosa que quieras añadir.
- > Tres líneas de mejora claras para futuras versiones: (1) **Soporte de voz** — que funcione también por voz porque en mesa resulta incómodo escribir y la barrera de entrada bajaría mucho; (2) **Modo torneo** — una variante de respuesta ultrarrápida y ultraconcisa que reduzca el pipeline de enrutado para priorizar velocidad sobre profundidad de respuesta, pensada para situaciones competitivas donde los segundos cuentan; (3) **Memoria de contexto de usuario** — actualmente el sistema solo conserva en caché lo que trabaja el router en la consulta actual, pero no el hilo de la sesión del usuario; añadir un historial de conversación por chat permitiría preguntas encadenadas mucho más fluidas.
- > Dicho esto, el sistema es sólido, bien diseñado y resuelve un problema real. Enhorabuena por el trabajo.
