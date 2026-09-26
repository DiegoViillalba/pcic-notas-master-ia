---
tipo: concepto
aliases:
  - Complejidad de tiempo
  - Time complexity
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad]
---

# Complejidad temporal

## Definición

Medida del número de operaciones que ejecuta un algoritmo en función del tamaño de la entrada.

## Intuición

Permite comparar el crecimiento del trabajo requerido sin depender principalmente de una computadora o implementación concreta.

## Formulación

Para entradas de tamaño $n$, se representa mediante una función $T(n)$. Por ejemplo, si $T(n)\le dn+c$ para constantes $c,d$, entonces $T(n)=O(n)$.

## Ejemplo mínimo

En el peor caso, la búsqueda lineal compara $x$ con los $n$ elementos; su complejidad temporal es $O(n)$.

## Contraejemplo o límites

La notación asintótica no da por sí sola el tiempo exacto ni elimina la importancia de constantes, distribución de entradas o arquitectura para tamaños pequeños.

## Relaciones

- Es un criterio de: [[Eficiencia algorítmica|Eficiencia algorítmica]].
- Contrasta con: [[Complejidad espacial|Complejidad espacial]].
- Incluye como clase importante: [[Tiempo polinomial|Tiempo polinomial]].

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 11–13.
