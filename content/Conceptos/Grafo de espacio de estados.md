---
tipo: concepto
aliases:
  - State-space graph
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, grafos]
---

# Grafo de espacio de estados

## Definición

Representación en la que cada vértice es un estado y cada arista dirigida es una transición permitida por una acción.

## Intuición

El grafo describe la estructura del problema independientemente del recorrido concreto que emprenda un algoritmo.

## Ejemplo mínimo

En el mapa de Rumania, las ciudades son vértices, los caminos son aristas y sus distancias son costos.

## Grafo frente a árbol

Un estado aparece una vez como vértice del grafo, pero puede aparecer muchas veces como [[Nodo de búsqueda|nodo]] en un [[Árbol de búsqueda|árbol de búsqueda]] al ser alcanzado por planes distintos. Un ciclo pequeño en el grafo puede desplegar ramas arbitrariamente largas en el árbol.

## Relaciones

- Representa un: [[Espacio de estados|Espacio de estados]].
- Sus aristas están definidas por la: [[Función sucesor|Función sucesor]].
- Se despliega desde un estado inicial como un: [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 17 y 20.
