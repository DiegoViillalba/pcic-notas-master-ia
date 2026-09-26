---
tipo: concepto
aliases:
  - Search algorithm evaluation criteria
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Búsqueda I]]"
tags: [concepto, inteligencia-artificial, busqueda, complejidad]
---

# Criterios de evaluación de algoritmos de búsqueda

## Criterios

| Criterio | Definición | Pregunta práctica |
|---|---|---|
| Completitud | Garantiza encontrar una solución si existe | ¿Puede fallar o perderse aunque haya una meta alcanzable? |
| Optimalidad | Garantiza devolver una solución de costo mínimo | ¿La primera solución encontrada es la mejor? |
| Complejidad temporal | Número de nodos generados o expandidos | ¿Cuánto trabajo crece con el problema? |
| Complejidad espacial | Máximo de nodos almacenados simultáneamente | ¿Cuánta memoria necesita? |

## Parámetros de análisis

- $b$: [[Factor de ramificación|factor de ramificación]] máximo.
- $d$: profundidad de la solución menos profunda.
- $m$: [[Profundidad máxima de un árbol de búsqueda|profundidad máxima]] del árbol.
- $C^*$: costo de una solución óptima.
- $\varepsilon$: cota positiva mínima del costo de cada acción.

## Comparación de algoritmos

| Algoritmo | Completo | Óptimo | Tiempo | Espacio |
|---|---|---|---|---|
| BFS | Sí, si $b$ es finito | Sí, con costos de paso iguales | $O(b^d)$ | $O(b^d)$ |
| DFS | No en espacios de profundidad infinita o con ciclos no controlados | No | $O(b^m)$ | $O(bm)$ |
| IDS | Sí, si $b$ es finito | Sí, con costos de paso iguales | $O(b^d)$ | $O(bd)$ |
| UCS | Sí, si $b$ es finito y cada costo es $\geq\varepsilon>0$ | Sí, bajo la misma condición | $O\!\left(b^{1+\lfloor C^*/\varepsilon\rfloor}\right)$ | Igual que tiempo |

Estas son cotas estándar del peor caso para la versión en árbol. La búsqueda en grafo añade memoria para registrar estados y puede cambiar el análisis según el tamaño del grafo.

## Cómo leer la tabla

- BFS minimiza cantidad de pasos, no necesariamente costo.
- DFS ahorra memoria, pero su resultado depende mucho del orden de sucesores.
- UCS generaliza BFS: cuando todos los pasos cuestan lo mismo, ambos extraen nodos por capas de costo.
- IDS recupera la completitud de BFS usando el espacio lineal de DFS.
- La condición $\varepsilon>0$ evita explorar infinitos pasos de costo nulo o cada vez menor antes de alcanzar una solución.

## Relaciones

- Compara estrategias de [[Búsqueda no informada|Búsqueda no informada]].
- Sus cotas dependen del [[Factor de ramificación|factor de ramificación]] y la profundidad.

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 19–20, para $b$, $m$ y el crecimiento del árbol. Las propiedades de BFS, DFS y UCS corresponden al análisis estándar de búsqueda no informada preparado para la sesión siguiente.
