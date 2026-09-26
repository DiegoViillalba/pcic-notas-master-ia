---
tipo: concepto
aliases:
  - Analytical and numerical solution
  - Solución numérica
  - Solución analítica
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]]"
  - "[[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]]"
tags: [concepto, modelacion-matematica, metodos-numericos]
---

# Solución analítica y solución numérica

## Definición

Una **solución analítica** expresa la respuesta mediante una fórmula o relaciones matemáticas exactas. Una **solución numérica** calcula valores aproximados mediante un algoritmo.

No son enfoques rivales: una solución analítica ayuda a entender el modelo y puede servir para comprobar un método numérico; la numérica permite estudiar modelos cuya solución exacta no existe o no resulta práctica.

## Comparación

| Criterio | Analítica | Numérica |
|---|---|---|
| Resultado | Fórmula o relación exacta | Valores aproximados |
| Interpretación | Facilita estudiar parámetros y límites | Facilita explorar escenarios concretos |
| Alcance | Restringido a modelos tratables | Admite modelos más complejos |
| Error | Puede haber error algebraico o de parámetros | Añade discretización y redondeo |
| Costo | Se paga principalmente al derivarla | Depende del paso, tamaño y número de ejecuciones |

## Ejemplo mínimo

Para

$$
y'=y, \qquad y(0)=1,
$$

la solución analítica es $y(t)=e^t$. Con [[Método de Euler|Euler]] y paso $h=0.1$,

$$
y_1=y_0+h y_0=1.1,
$$

mientras que $y(0.1)=e^{0.1}\approx1.10517$. La diferencia es parte del error numérico.

## Criterios numéricos mínimos

- **Error:** diferencia entre la aproximación y una referencia.
- **Convergencia:** la aproximación se acerca a la solución al refinar el cálculo.
- **Estabilidad:** los errores no crecen de manera incontrolada durante el cálculo.
- **Costo computacional:** tiempo y memoria necesarios para obtener la precisión deseada.

## Límites

Una fórmula exacta sigue dependiendo de que el modelo y sus supuestos sean adecuados. Del mismo modo, una simulación con muchos decimales no es necesariamente precisa: debe revisarse su error, estabilidad y convergencia.

## Relaciones

- Son formas de resolver un [[Modelo matemático|modelo matemático]].
- Repetir una solución numérica para muchos escenarios puede formar un [[Experimento computacional|experimento computacional]].
- Ambas deben interpretarse dentro del [[Ciclo de modelación|ciclo de modelación]].

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
- Ejemplo numérico: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].
