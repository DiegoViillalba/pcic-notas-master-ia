---
tipo: concepto
aliases: [Depth-first search, DFS]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Búsqueda en profundidad

## Definición

Estrategia no informada que expande primero el nodo más profundo de la [[Frontera de búsqueda|frontera]]. Se implementa con una pila LIFO o mediante recursión.

## Regla

$$f(n)=-\operatorname{profundidad}(n),$$

entendida como una prioridad que favorece mayor profundidad. No compara costos ni cercanía a la meta.

## Propiedades

- Tiempo: $O(b^m)$.
- Espacio: $O(bm)$.
- No es óptima.
- No es completa en búsqueda en árbol con ciclos o profundidad infinita.
- En un grafo finito, con registro correcto de estados alcanzados, sí termina y es completa.

## Intuición

Explora una rama hasta agotarla y después retrocede. Su memoria es pequeña porque conserva principalmente el camino actual y los hermanos pendientes, pero puede invertir todo el tiempo en una rama sin solución.

## Relaciones

- Es una [[Búsqueda no informada|búsqueda no informada]].
- Su versión con límites crecientes es [[Búsqueda de profundidad iterativa|profundidad iterativa]].
- Se evalúa con los [[Criterios de evaluación de algoritmos de búsqueda|criterios de búsqueda]].

