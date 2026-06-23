
# Plantilla de análisis y presentación de resultados UAT

---

## 1. Datos cuantitativos — Cómo calcularlos

### 1.1 Medias por bloque (escala Likert 1-5)

Para cada ítem Likert, calcular media aritmética y desviación estándar:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i \qquad \sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

Presentar en tabla resumen:

| Bloque | Dimensión | Media | σ | Interpretación |
|--------|-----------|-------|---|----------------|
| B1 | Usabilidad | — | — | ≥ 4,0 = satisfactorio |
| B2 | Calidad respuestas | — | — | ≥ 4,0 = satisfactorio |
| B3 | Utilidad percibida | — | — | ≥ 4,0 = satisfactorio |

**Umbral de referencia recomendado**: media ≥ 4,0 en escala 1-5 se considera resultado positivo; entre 3,0 y 3,9, mejorable; < 3,0, problemático.

### 1.2 Puntuación NPS implícita (P3.4 y P6.3)

- P3.4 ("Recomendaría el bot"): puntuaciones 5 → promotores, 3-4 → pasivos, 1-2 → detractores.
- P6.1 (valoración 1-10): calcular NPS = %promotores (9-10) − %detractores (1-6).

### 1.3 Distribución de respuestas cerradas

Para P4.1, P5.1, P5.2: representar con gráfico de barras horizontales mostrando % de usuarios que seleccionó cada opción.

---

## 2. Datos cualitativos — Cómo analizarlos

Para las respuestas abiertas (P1.6, P2.7, P2.8, P3.6, P4.4, P4.5, P5.3, P6.4):

1. **Agrupar por temas recurrentes** (codificación temática simple).
2. **Categorías sugeridas**: precisión de respuestas · velocidad · cobertura de juegos · facilidad de uso · confianza · mejoras solicitadas.
3. Citar 2-3 verbatims representativos por categoría en el texto del TFG.

---

## 3. Relación con los objetivos del sistema

| Objetivo del sistema | Ítem(s) UAT relacionados | Resultado esperado |
|----------------------|-------------------------|--------------------|
| Responder preguntas en lenguaje natural | P1.2, P2.1, P2.3 | Media ≥ 4,0 |
| Citar siempre la fuente | P2.2 | Media ≥ 4,0 |
| No inventar información | P2.5 | Media ≥ 4,5 (crítico) |
| Ser más rápido que buscar en PDF | P3.2 | Media ≥ 4,0 |
| Informar cuando no hay contexto | P1.4 | Media ≥ 3,5 |
| Cubrir múltiples juegos | P3.5, P0.3 | Uso de ≥ 3 juegos distintos |

---

## 4. Relación con el estado del arte

Comparar los resultados de P4.2 y P4.3 con la hipótesis inicial: *"un sistema RAG sobre dominio cerrado es más preciso y rápido para el usuario final que la búsqueda manual en documentos"*.

- Si P4.2 ≥ "Mejor" en ≥ 70% de respuestas → hipótesis confirmada.
- Contrastar con limitaciones conocidas de LLMs generales (alucinación, falta de dominio específico) frente al diseño RAG con restricción de fuente.

---

## 5. Tabla de fortalezas y debilidades (a rellenar con datos reales)

| Dimensión | Fortaleza identificada | Debilidad identificada | Mejora propuesta |
|-----------|------------------------|------------------------|------------------|
| Calidad de respuesta | Alta precisión en reglas básicas | Respuestas incompletas en reglas complejas | Ampliar chunks de contexto |
| Usabilidad | Interfaz Telegram familiar | Sin guía de inicio para nuevos usuarios | Añadir mensaje de bienvenida con ejemplos |
| Cobertura | 5 juegos indexados | Faltan algunos suplementos | Plan de expansión de manuales |
| Velocidad | Respuesta en < 10 s | Picos ocasionales de latencia | Optimizar tamaño de índice |
| Confianza | Siempre cita la fuente | Usuarios dudan sin imagen/tabla | Incluir referencia a sección exacta |

---

## 6. Gráficos recomendados para el TFG

1. **Radar/araña** con las 5 dimensiones (Usabilidad, Calidad, Utilidad, Cobertura, Confianza) — muestra el perfil global del sistema de un vistazo.
2. **Barras agrupadas** comparando medias por bloque vs. umbral de 4,0.
3. **Barras horizontales** para P5.1 (distribución de problemas encontrados).
4. **Pie/dona** para P6.2 (¿cumple su objetivo?) y P6.3 (intención de uso).
5. **Tabla de verbatims** con citas textuales agrupadas por categoría.

---

## 7. Conclusión interpretativa tipo (rellenar con datos reales)

> *"Los [N] evaluadores que participaron en las pruebas UAT otorgaron al sistema una valoración global media de [X]/10. La dimensión mejor valorada fue [___] (media [X]/5), lo que confirma que el sistema cumple el objetivo de [___]. La dimensión con mayor margen de mejora fue [___] (media [X]/5), principalmente por [motivo extraído de respuestas abiertas]. El [Y]% de los participantes prefiere el bot frente a buscar en el PDF del reglamento, lo que valida la hipótesis de partida. Las principales debilidades detectadas son [___] y [___], y se proponen como líneas de mejora futura [___]."*
