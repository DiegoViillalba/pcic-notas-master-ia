---
tipo: concepto
aliases:
  - Mejor caso y peor caso
  - Best-case and worst-case analysis
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]"
tags: [concepto, algoritmos, complejidad]
---

# Análisis de mejor y peor caso

## Definición

Estudio del costo mínimo y máximo que un algoritmo puede tener entre todas las entradas de un mismo tamaño.

## Intuición

Dos entradas con $n$ elementos pueden exigir cantidades muy distintas de trabajo. El mejor caso describe la configuración más favorable; el peor caso proporciona una garantía que vale incluso para la más desfavorable.

## Formulación

Si $T(x)$ es el costo sobre la entrada $x$ y $|x|=n$, entonces:

$$
T_{\min}(n)=\min_{|x|=n}T(x),
\qquad
T_{\max}(n)=\max_{|x|=n}T(x).
$$

También debe especificarse qué operación se cuenta; para los hot cakes puede ser el número de usos de la pala o el número total de movimientos elementales.

## Ejemplo mínimo

En búsqueda lineal, el mejor caso necesita una comparación cuando el elemento está al principio; el peor necesita $n$ comparaciones cuando está al final o no aparece.

## Contraejemplo o límites

El peor caso no describe necesariamente una entrada típica, y contar volteos como operaciones unitarias puede ocultar el costo de implementarlos en memoria.

## Relaciones

- Es parte de: [[Complejidad temporal|Complejidad temporal]].
- Se aplica a: [[Ordenamiento de hot cakes|Ordenamiento de hot cakes]].
- Depende del modelo de costo de: [[Volteo de prefijo|Volteo de prefijo]].
- Contrasta con: análisis de caso promedio y análisis amortizado.

## Procedencia

- Clase: [[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]
- Fuente: *El Algoritmo de los Hot Cakes*.
- Página o sección: diapositiva 10.

## Preguntas abiertas

- ¿Qué permutaciones alcanzan los extremos para la variante presentada del algoritmo de los hot cakes?
