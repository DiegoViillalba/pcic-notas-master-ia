---
tipo: concepto
aliases:
  - Polynomial time
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad]
---

# Tiempo polinomial

## Definición

Tiempo de ejecución acotado superiormente por un polinomio en el tamaño de la entrada.

## Formulación

Un algoritmo corre en tiempo polinomial si existen constantes $c>0$ y $k\ge 0$ tales que, para entradas suficientemente grandes,

$$
T(n)\le c n^k.
$$

## Ejemplo mínimo

La búsqueda lineal tiene $T(n)=O(n)$, así que es polinomial con $k=1$.

## Contraejemplo o límites

$2^n$ y $n!$ no son cotas polinomiales. Que un algoritmo sea polinomial tampoco garantiza por sí solo que sea rápido para todos los tamaños prácticos.

## Relaciones

- Es una clase de: [[Complejidad temporal|Complejidad temporal]].
- Se usa como aproximación de: [[Eficiencia algorítmica|Eficiencia algorítmica]].
- Es central en: [[P versus NP|P versus NP]].

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 13 y 15.
