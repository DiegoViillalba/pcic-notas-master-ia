---
tipo: concepto
aliases:
  - Successor function
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Función sucesor

## Definición

Regla que, dado un estado, devuelve las acciones aplicables, los estados que producen y el costo correspondiente.

## Formulación

Puede representarse como

$$
\operatorname{Suc}(s)=\{(a,s',c): a\text{ es aplicable en }s,\;a(s)=s',\;c\text{ es su costo}\}.
$$

## Ejemplo mínimo

En el mapa de Rumania, desde Arad cada camino hacia una ciudad adyacente define una acción; el sucesor es la ciudad de llegada y el costo es la distancia indicada.

## Límites

No decide cuál sucesor conviene explorar primero. Solo define las transiciones disponibles dentro de la formulación.

## Relaciones

- Forma parte de la: [[Formulación de un problema de búsqueda|Formulación de un problema de búsqueda]].
- Define las aristas de un: [[Grafo de espacio de estados|Grafo de espacio de estados]].
- Genera los hijos de un: [[Nodo de búsqueda|Nodo de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 10 y 17.
