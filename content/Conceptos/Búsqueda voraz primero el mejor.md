---
tipo: concepto
aliases: [Greedy best-first search, Búsqueda voraz]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, heuristicas]
---

# Búsqueda voraz primero el mejor

## Definición

Búsqueda informada que extrae el nodo con menor valor de [[Heurística|heurística]]:

$$f(n)=h(n).$$

## Intuición

Elige el estado que parece más cercano a una meta. Ignora el costo $g(n)$ ya pagado, por lo que puede preferir un atajo aparente cuyo camino total resulte caro.

## Propiedades

- No es óptima.
- No es completa en espacios infinitos ni sin control de repetidos.
- En búsqueda en grafo sobre un espacio finito sí termina.
- Su peor caso puede requerir $O(b^m)$ tiempo y espacio.

## Dependencia de la heurística

Con una buena heurística puede encontrar rápidamente una solución. Con una mala, puede comportarse como una exploración en profundidad mal dirigida. La heurística cambia el orden de exploración, no demuestra por sí misma que una solución sea óptima.

## Relación

[[Algoritmo A estrella|A*]] corrige su miopía al sumar el costo acumulado: $f(n)=g(n)+h(n)$.

