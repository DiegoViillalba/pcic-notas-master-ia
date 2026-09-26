---
tipo: concepto
aliases: [Función heurística, Heuristic function]
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-20 IA - Algoritmos de busqueda|Algoritmos de búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda, heuristicas]
---

# Heurística

## Definición

Función $h(n)$ que estima el costo mínimo restante desde el estado de un nodo $n$ hasta una meta. Incorpora conocimiento del dominio para orientar la búsqueda.

## No debe confundirse con

- $g(n)$: costo **real acumulado** desde el inicio.
- $h^*(n)$: costo restante **real óptimo**, normalmente desconocido.
- $f(n)=g(n)+h(n)$: estimación del costo total usada por [[Algoritmo A estrella|A*]].

## Admisibilidad

$h$ es admisible si nunca sobreestima:

$$0\le h(n)\le h^*(n).$$

## Consistencia

$h$ es consistente si, para toda transición $n\xrightarrow{a}n'$,

$$h(n)\le c(n,a,n')+h(n').$$

La consistencia es una desigualdad triangular y hace que los valores $f$ no disminuyan a lo largo de un camino. Toda heurística consistente es admisible si $h(G)=0$; la conversa no siempre vale.

## Calidad

Una heurística más informada puede reducir expansiones, pero debe ser barata de calcular. Una estimación agresiva que sobreestima puede acelerar la búsqueda y, a cambio, perder garantías de optimalidad.

## Relaciones

- Usada sola por la [[Búsqueda voraz primero el mejor|búsqueda voraz]].
- Combinada con $g(n)$ por [[Algoritmo A estrella|A*]].

