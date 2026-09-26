---
tipo: concepto
aliases:
  - Branching factor
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, complejidad]
---

# Factor de ramificación

## Definición

Cantidad de hijos que genera un nodo de búsqueda; suele representarse con $b$, ya sea como valor uniforme, promedio o cota superior según el análisis.

## Intuición

Mide cuántas alternativas abre cada paso. Incluso con profundidad moderada, un valor grande de $b$ hace crecer rápidamente el árbol.

## Formulación

Con factor constante, el nivel $k$ contiene hasta $b^k$ nodos.

## Ejemplo mínimo

Si cada estado ofrece tres sucesores, entonces $b=3$ y en profundidad $4$ puede haber hasta $3^4=81$ nodos en ese nivel.

## Relaciones

- Determina el crecimiento de un: [[Árbol de búsqueda|Árbol de búsqueda]].
- Se combina con la: [[Profundidad máxima de un árbol de búsqueda|Profundidad máxima]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositiva 19.
