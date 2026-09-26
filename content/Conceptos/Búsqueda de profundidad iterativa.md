---
tipo: concepto
aliases: [Iterative deepening search, IDS, IDDFS]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Búsqueda de profundidad iterativa

## Definición

Estrategia que repite una [[Búsqueda en profundidad|búsqueda en profundidad]] limitada con cotas $0,1,2,\ldots$ hasta encontrar una meta.

## Propósito

Combina dos ventajas:

- la completitud y optimalidad por profundidad de [[Búsqueda en anchura|BFS]];
- el bajo consumo de memoria de DFS.

## Propiedades

- Completa si $b$ es finito.
- Óptima cuando los costos de paso son iguales.
- Tiempo: $O(b^d)$.
- Espacio: $O(bd)$.

## Por qué repetir no es tan costoso

Aunque regenera los niveles superiores, en un árbol con $b>1$ la mayor parte de los nodos está en el nivel más profundo. Por ello, las repeticiones no cambian el orden asintótico $O(b^d)$.

## Límite

Si los costos de acción varían, hallar la meta menos profunda no implica hallar la ruta de menor costo.

