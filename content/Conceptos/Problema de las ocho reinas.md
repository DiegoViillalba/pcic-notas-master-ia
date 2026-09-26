---
tipo: concepto
aliases: [Ocho reinas, N reinas]
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Clase del 20 de agosto]]"
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
tags: [concepto, algoritmos, backtracking]
---

# Problema de las ocho reinas

## Definición

Problema de colocar ocho reinas en un tablero de $8\times8$ sin que dos compartan fila, columna o diagonal. Su generalización usa $n$ reinas en un tablero $n\times n$.

## Representación

Si se coloca una reina por fila, una configuración parcial es un vector donde `sol[k]` indica la columna de la reina de la fila `k`. Una casilla $(k,j)$ es segura si no se han usado $j$, $j-k$ ni $j+k$.

## Propiedades

- Tiene 92 soluciones para $n=8$.
- Al identificar rotaciones y reflexiones, quedan 12 soluciones fundamentales.
- Es un problema clásico de satisfacción de restricciones y [[Backtracking|backtracking]].

## Relaciones

- Usa [[Poda del espacio de búsqueda|poda]] para eliminar columnas y diagonales ocupadas.
- [[Forward checking|Forward checking]] conserva explícitamente las columnas todavía posibles en cada fila futura.
- El árbol tiene un nivel por fila y una rama potencial por columna.

## Procedencia

[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Ocho reinas y cuadros mágicos]].
