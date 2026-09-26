---
tipo: concepto
aliases:
  - Search node
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Nodo de búsqueda

## Definición

Elemento de un árbol de búsqueda que muestra un estado y representa el plan concreto seguido para alcanzarlo desde la raíz.

## Estado frente a nodo

| Estado | Nodo de búsqueda |
|---|---|
| Configuración del problema | Ocurrencia de esa configuración dentro de un plan |
| Puede aparecer una sola vez en el grafo | Puede repetirse en distintas ramas del árbol |
| Determina acciones aplicables | Conserva el contexto del camino que lo alcanzó |

## Ejemplo mínimo

En el mapa de Rumania, “Sibiu” es un estado. El árbol puede contener un nodo para llegar a Sibiu desde Arad y otro para llegar a la misma ciudad mediante una ruta distinta.

## Relaciones

- Contiene un estado de: [[Espacio de estados|Espacio de estados]].
- Forma parte de un: [[Árbol de búsqueda|Árbol de búsqueda]].
- Sus hijos se obtienen mediante la: [[Función sucesor|Función sucesor]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositiva 19.
