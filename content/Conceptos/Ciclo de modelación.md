---
tipo: concepto
aliases:
  - Modeling cycle
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]]"
tags: [concepto, modelacion-matematica]
---

# Ciclo de modelación

## Definición

Proceso iterativo que transforma una pregunta sobre un fenómeno en un [[Modelo matemático|modelo matemático]], estudia sus resultados y los contrasta con el sistema real.

## Intuición

Modelar no termina al resolver una ecuación. Si el resultado contradice los datos, las unidades o el comportamiento esperado, hay que regresar y revisar la pregunta, los supuestos o la formulación.

## Etapas

| Etapa | Pregunta que responde | Producto |
|---|---|---|
| Problema | ¿Qué queremos explicar, predecir o comparar? | Pregunta modelable |
| Supuestos | ¿Qué simplificamos y bajo qué condiciones? | Alcance explícito |
| Formulación | ¿Qué variables, parámetros y relaciones usamos? | Modelo matemático |
| Resolución | ¿Cómo obtenemos una respuesta? | Solución analítica o numérica |
| Análisis | ¿Qué significan los resultados y cómo cambian? | Interpretación y sensibilidad |
| Validación | ¿El resultado es consistente con la evidencia? | Medidas de ajuste y límites |

## Ejemplo mínimo

Para estudiar el tráfico se pregunta cómo cambia el tiempo medio de recorrido si una luz verde pasa de 45 a 60 segundos. Se supone una tasa de llegada fija, se formula una cola de vehículos, se simulan ambos escenarios, se comparan sus tiempos y se validan contra mediciones. Si el modelo subestima las horas pico, se revisa el supuesto de llegadas constantes.

## Límites

El ciclo no garantiza un modelo único ni verdadero. Produce una representación útil para una pregunta y un contexto; cambiar la escala, los datos o el objetivo puede exigir otro modelo.

## Relaciones

- Comienza con una [[Pregunta modelable|pregunta modelable]].
- Hace explícito cada [[Supuesto de modelación|supuesto de modelación]].
- Incluye la [[Validación de un modelo|validación de un modelo]].
- Puede usar una [[Solución analítica y solución numérica|solución analítica o numérica]].

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
