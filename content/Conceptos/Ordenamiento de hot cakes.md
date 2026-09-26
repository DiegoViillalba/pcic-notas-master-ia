---
tipo: concepto
aliases:
  - Algoritmo de los hot cakes
  - Pancake sorting
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]"
tags: [concepto, algoritmos, ordenamiento]
---

# Ordenamiento de hot cakes

## Definición

Problema de ordenar una pila de elementos de tamaños distintos usando únicamente volteos de la parte superior de la pila.

## Intuición

Como no se puede extraer un elemento intermedio, primero se lleva a la cima el mayor elemento pendiente y luego se voltea la región desordenada para colocarlo en su posición definitiva al fondo de esa región.

## Formulación

Dada una permutación $A=(a_1,\ldots,a_n)$, se busca transformarla en orden creciente mediante operaciones [[Volteo de prefijo|$F_k$]] que invierten los primeros $k$ elementos.

El esquema clásico fija los elementos desde el fondo:

```text
para m = n, n-1, ..., 2:
    lleva el máximo de A[1..m] a la cima
    voltea A[1..m] para colocarlo en la posición m
```

## Ejemplo mínimo

La pila $[2,3,1]$ se transforma en $[1,2,3]$ llevando primero el $3$ a la cima y después al fondo:

$$
[2,3,1]\xrightarrow{F_2}[3,2,1]\xrightarrow{F_3}[1,2,3].
$$

## Contraejemplo o límites

Si se permiten intercambios arbitrarios, ya no se trata de este problema. Además, que un hot cake coincida accidentalmente con su índice objetivo no significa que pertenezca al bloque fijado: el algoritmo necesita conservar un sufijo ordenado.

## Relaciones

- Utiliza: [[Volteo de prefijo|Volteo de prefijo]].
- Se demuestra con: [[Invariante de ciclo|Invariante de ciclo]].
- Se evalúa mediante: [[Análisis de mejor y peor caso|Análisis de mejor y peor caso]] y [[Complejidad temporal|Complejidad temporal]].
- Requiere justificar: [[Terminación de un algoritmo|Terminación]] y [[Validez de un algoritmo|validez]].

## Procedencia

- Clase: [[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]
- Fuente: *El Algoritmo de los Hot Cakes*.
- Página o sección: diapositivas 2–5.

## Preguntas abiertas

- ¿Qué entradas fuerzan el mayor número de volteos para esta variante concreta?
- ¿Cómo cambia el algoritmo si la pila debe ordenarse en sentido opuesto?
