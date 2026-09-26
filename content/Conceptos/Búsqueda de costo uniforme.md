---
tipo: concepto
aliases: [Uniform-cost search, UCS]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, costos]
---

# Búsqueda de costo uniforme

## Definición

Estrategia no informada que extrae de una cola de prioridad el nodo con menor costo acumulado

$$g(n)=\sum_{a\in\operatorname{camino}(n)}c(a).$$

## Propiedades

Si $b$ es finito y cada acción cuesta al menos $\varepsilon>0$:

- es completa;
- es óptima;
- tiempo y espacio son $O\!\left(b^{1+\lfloor C^*/\varepsilon\rfloor}\right)$ en el peor caso.

## Prueba de meta

La meta se acepta cuando es **extraída** como nodo de costo mínimo, no cuando entra en la [[Frontera de búsqueda|frontera]]. Una meta cara puede generarse antes que otra ruta todavía incompleta pero más barata.

## Relación con otros algoritmos

- Generaliza [[Búsqueda en anchura|BFS]] a costos distintos.
- Es el caso de [[Algoritmo A estrella|A*]] con $h(n)=0$.
- Equivale conceptualmente al algoritmo de Dijkstra aplicado hasta extraer una meta.

## Límite

Conoce cuánto se ha gastado, pero no estima cuánto falta; puede explorar extensamente en direcciones que no acercan a la meta.

