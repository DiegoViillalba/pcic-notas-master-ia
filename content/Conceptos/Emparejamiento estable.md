---
tipo: concepto
area: algoritmos
estado: desarrollado
tags: [concepto, algoritmos]
---
# Emparejamiento estable

## Definición

Un emparejamiento perfecto entre dos conjuntos con preferencias es estable si no contiene ningún [[Par inestable]].

## Formulación

Para todo $(h,s)\notin M$, no deben cumplirse simultáneamente $s\succ_h M(h)$ y $h\succ_s M(s)$.

## Intuición

Resiste acuerdos bilaterales: ninguna pareja preferiría abandonar sus asignaciones actuales para estar junta.

## Relaciones

- Requiere: [[Emparejamiento perfecto]], [[Par inestable]].
- Se obtiene con: [[Algoritmo de Gale-Shapley]].
