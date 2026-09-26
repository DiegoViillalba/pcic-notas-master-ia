---
tipo: concepto
aliases: [A*, A-star search]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, heuristicas]
---

# Algoritmo A estrella

## Definición

Búsqueda informada que prioriza el menor costo total estimado:

$$f(n)=g(n)+h(n),$$

donde $g(n)$ es el costo real desde el inicio y $h(n)$ una [[Heurística|estimación]] del costo restante.

## Lectura

- $g(n)$ evita ignorar lo ya pagado, como hace la búsqueda voraz.
- $h(n)$ evita explorar sin dirección, como puede hacer [[Búsqueda de costo uniforme|UCS]].
- Si $h(n)=0$ para todo nodo, A* se reduce a UCS.

## Condiciones de optimalidad

- En búsqueda en árbol, A* es óptimo con una heurística admisible.
- En búsqueda en grafo que no reabre nodos, se requiere consistencia.
- Con heurística admisible pero inconsistente puede conservarse la optimalidad si se permite reabrir un estado cuando aparece un camino mejor.

## Prueba de meta

La meta se devuelve cuando es **extraída** con prioridad mínima, no cuando se genera. Como $h(G)=0$, en una meta se cumple $f(G)=g(G)$.

## Costo práctico

A* puede ser exponencial y suele consumir mucha memoria porque conserva numerosos nodos en la [[Frontera de búsqueda|frontera]]. Una buena heurística reduce expansiones, pero no elimina el peor caso.

## Límite conceptual

“A* es óptimo” es una afirmación incompleta: siempre deben especificarse las propiedades de $h$, la búsqueda en árbol o grafo y la política para caminos mejores.
