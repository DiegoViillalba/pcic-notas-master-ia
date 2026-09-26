---
tipo: concepto
aliases:
  - Search tree
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, arboles]
---

# Árbol de búsqueda

## Definición

Despliegue de los planes que pueden generarse al aplicar sucesivamente acciones desde un estado inicial.

## Estructura

- La raíz corresponde al estado inicial.
- Los hijos de un nodo corresponden a sus sucesores.
- Un nodo muestra un estado, pero representa también el plan que lo alcanza.
- Las soluciones pueden encontrarse en lugares distintos del árbol.

## Tamaño

Si cada nodo tiene a lo sumo [[Factor de ramificación|$b$ hijos]] y la [[Profundidad máxima de un árbol de búsqueda|profundidad máxima]] es $m$, el número de nodos puede crecer como

$$
1+b+b^2+\cdots+b^m.
$$

Por ello rara vez se construye el árbol completo.

## Límites

No es lo mismo que el [[Grafo de espacio de estados|grafo de espacio de estados]]: un mismo estado puede repetirse en ramas diferentes y los ciclos del grafo pueden producir un árbol infinito.

## Relaciones

- Contiene: [[Nodo de búsqueda|Nodos de búsqueda]].
- Despliega un: [[Espacio de estados|Espacio de estados]].
- Sus hijos se generan con la: [[Función sucesor|Función sucesor]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 19–20.
