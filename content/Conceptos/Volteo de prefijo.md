---
tipo: concepto
aliases:
  - Pancake flip
  - Inversión de prefijo
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]"
tags: [concepto, algoritmos, operaciones]
---

# Volteo de prefijo

## Definición

Operación que invierte el orden de los primeros $k$ elementos de una secuencia y deja intactos los restantes.

## Intuición

Equivale a introducir una pala debajo del elemento en la posición $k$ y voltear de una sola vez toda la parte que está encima.

## Formulación

$$
F_k(a_1,\ldots,a_k,a_{k+1},\ldots,a_n)
=(a_k,\ldots,a_1,a_{k+1},\ldots,a_n),
\qquad 1\le k\le n.
$$

La operación es su propia inversa:

$$
F_k(F_k(A))=A.
$$

## Ejemplo mínimo

$$
F_3([2,4,1,3])=[1,4,2,3].
$$

## Contraejemplo o límites

Intercambiar dos elementos cualesquiera no es un volteo de prefijo. Tampoco lo es invertir un segmento que comienza después de la primera posición.

## Relaciones

- Se utiliza en: [[Ordenamiento de hot cakes|Ordenamiento de hot cakes]].
- Su número de aplicaciones se estudia con: [[Análisis de mejor y peor caso|Análisis de mejor y peor caso]].
- Contrasta con: intercambio arbitrario y rotación de una secuencia.

## Procedencia

- Clase: [[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]
- Fuente: *El Algoritmo de los Hot Cakes*.
- Página o sección: diapositiva 3.

## Preguntas abiertas

- ¿Qué costo debe asignarse al volteo: una operación física o $\Theta(k)$ movimientos en una representación de arreglo?
