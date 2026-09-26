---
tipo: concepto
aliases: [Cuadrado mágico, Constante mágica]
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Clase del 20 de agosto]]"
tags: [concepto, algoritmos, combinatoria]
---

# Cuadro mágico

## Definición

Matriz $n\times n$ que usa una vez cada entero de $1$ a $n^2$ y tiene la misma suma en todas las filas, columnas y las dos diagonales principales.

## Constante mágica

La suma común está determinada por el orden:

$$
M_n=\frac{n(n^2+1)}2.
$$

Por ejemplo, $M_3=15$, $M_4=34$ y $M_9=369$.

## Métodos

- [[Backtracking|Backtracking]] permite enumerar cuadros, pero escala con rapidez.
- La [[Construcción por patrones|construcción por patrones]] genera una solución directamente para familias de órdenes.

## Límite

Los métodos dependen del tipo de orden: impar, doblemente par o simplemente par. Una regla válida para una familia no se transfiere automáticamente a otra.

## Procedencia

[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Ocho reinas y cuadros mágicos]].
