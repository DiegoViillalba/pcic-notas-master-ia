---
tipo: concepto
aliases:
  - Complejidad de espacio
  - Space complexity
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad]
---

# Complejidad espacial

## Definición

Medida de la memoria utilizada por un algoritmo en función del tamaño de la entrada; puede distinguirse la memoria total del espacio de trabajo adicional.

## Intuición

Dos algoritmos igualmente rápidos pueden diferir de manera decisiva en la memoria que necesitan.

## Formulación

Para entradas de tamaño $n$, el uso de espacio se describe mediante $S(n)$. Si solo se mantienen un número fijo de variables adicionales, $S(n)=O(1)$ de espacio auxiliar.

## Ejemplo mínimo

La búsqueda lineal conserva únicamente un contador además del arreglo de entrada; por ello usa espacio de trabajo constante.

## Contraejemplo o límites

Decir $O(1)$ no significa “cero memoria”; significa que la memoria adicional no crece con $n$.

## Relaciones

- Es un criterio de: [[Eficiencia algorítmica|Eficiencia algorítmica]].
- Contrasta con: [[Complejidad temporal|Complejidad temporal]].
- Puede intercambiarse con tiempo en algunos diseños algorítmicos.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 11–13.
