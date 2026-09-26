---
tipo: concepto
aliases:
  - State space
  - Espacio de búsqueda
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Espacio de estados

## Definición

Conjunto de configuraciones que una formulación considera posibles o relevantes para resolver un problema.

## Intuición

Cada estado resume lo necesario para decidir qué acciones pueden ejecutarse y si se alcanzó la meta.

## Ejemplos

- **Rumania:** cada ciudad es un estado.
- **Magic 8:** cada distribución alcanzable de las ocho fichas y el hueco es un estado.

## Representación

Puede representarse como un [[Grafo de espacio de estados|grafo]]: los vértices son estados y las aristas representan transiciones producidas por acciones.

## Límites

No debe confundirse un estado con un [[Nodo de búsqueda|nodo de búsqueda]]. El mismo estado puede aparecer en varios nodos cuando se alcanza mediante planes diferentes.

## Relaciones

- Forma parte de la: [[Formulación de un problema de búsqueda|Formulación de un problema de búsqueda]].
- Es recorrido mediante una: [[Función sucesor|Función sucesor]].
- Se despliega desde un inicio como un: [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 10 y 17–20.
