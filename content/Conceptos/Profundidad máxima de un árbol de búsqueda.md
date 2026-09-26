---
tipo: concepto
aliases:
  - Maximum search depth
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, complejidad]
---

# Profundidad máxima de un árbol de búsqueda

## Definición

Mayor número de acciones que puede contener una rama del árbol de búsqueda; se representa con $m$.

## Intuición

Indica hasta dónde puede prolongarse la generación de planes. Si el espacio permite ciclos y no se evitan repeticiones, $m$ puede ser infinito aun cuando el grafo tenga pocos estados.

## Ejemplo mínimo

En un grafo con transiciones $a\to b$ y $b\to a$, el árbol puede generar los planes $a,b,a,b,\ldots$ sin una profundidad máxima finita.

## Límites

No debe confundirse $m$ con la profundidad de una solución concreta. Las soluciones pueden aparecer a profundidades menores y en diferentes ramas.

## Relaciones

- Limita, junto con el [[Factor de ramificación|Factor de ramificación]], el tamaño de un [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 19–20.
