---
tipo: concepto
aliases: [Breadth-first search, BFS]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Búsqueda en anchura

## Definición

Estrategia no informada que expande primero los nodos de menor profundidad. Recorre el árbol por capas mediante una cola FIFO.

## Propiedades

- Completa si el [[Factor de ramificación|factor de ramificación]] $b$ es finito.
- Óptima cuando todos los costos de paso son iguales.
- Tiempo y espacio: $O(b^d)$; algunas convenciones cuentan la capa siguiente y escriben $O(b^{d+1})$.

## Distinción clave

BFS minimiza el **número de acciones**, no el costo total. Si las aristas tienen costos distintos, una ruta más profunda puede ser más barata; en ese caso se usa [[Búsqueda de costo uniforme|costo uniforme]].

## Prueba de meta

Con costos unitarios, la primera vez que se genera una meta se ha encontrado una ruta de profundidad mínima. También es correcta una implementación general que compruebe la meta al extraer el nodo.

## Relaciones

- Es una [[Búsqueda no informada|búsqueda no informada]].
- [[Búsqueda de profundidad iterativa|IDS]] conserva su completitud usando menos memoria.

