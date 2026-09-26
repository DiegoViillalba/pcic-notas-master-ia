---
tipo: concepto
aliases:
  - Model validation
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]]"
tags: [concepto, modelacion-matematica, validacion]
---

# Validación de un modelo

## Definición

Proceso de contrastar las predicciones y el comportamiento de un modelo con evidencia relevante para decidir si es útil para una pregunta y un contexto concretos.

Validar no significa demostrar que el modelo es verdadero. Significa reunir evidencia de que su error y sus límites son aceptables para el uso previsto.

## Evidencia útil

- Datos observados, de preferencia distintos de los usados para ajustar parámetros.
- Conocimiento físico, biológico o social previo.
- Unidades, signos, cotas y casos límite conocidos.
- Comparación con modelos o simulaciones de referencia.
- En métodos numéricos, resultados al reducir el paso o aumentar la resolución.

## Métricas mínimas

Si $y_i$ es el dato observado y $\widehat y_i$ la predicción:

$$
E_i=|y_i-\widehat y_i|,
\qquad
\operatorname{MAE}=\frac{1}{N}\sum_{i=1}^N|y_i-\widehat y_i|.
$$

El error absoluto conserva las unidades. Cuando interesa penalizar con mayor fuerza errores grandes puede usarse

$$
\operatorname{RMSE}
=\sqrt{\frac{1}{N}\sum_{i=1}^N(y_i-\widehat y_i)^2}.
$$

La métrica debe corresponder a la pregunta: en tráfico, el promedio puede ocultar retrasos extremos; en una población, también importa conservar la no negatividad.

## Ejemplo mínimo

Después de ajustar un modelo de tráfico con datos de lunes a jueves, se predicen los tiempos del viernes y se calcula el MAE. También se comprueba que el número de vehículos no sea negativo y que la simulación reproduzca el aumento de congestión en la hora pico.

## Mala validación y límites

Una curva visualmente parecida a los datos no basta: puede ocultar errores sistemáticos, usar los mismos datos con los que se ajustó o acertar por compensación entre parámetros incorrectos.

Una validación favorable tampoco autoriza extrapolar fuera de las condiciones estudiadas. Si cambian la escala, la intervención o los supuestos, el modelo debe evaluarse de nuevo.

## Relaciones

- Es una etapa del [[Ciclo de modelación|ciclo de modelación]].
- Puede obligar a revisar un [[Supuesto de modelación|supuesto de modelación]].
- Evalúa si el [[Modelo matemático|modelo matemático]] responde la pregunta prevista.
- En una [[Solución analítica y solución numérica|solución numérica]] también exige revisar error y convergencia.

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
