---
tipo: concepto
aliases:
  - P vs NP
  - P igual a NP
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad, p-np]
---

# P versus NP

## Definición

Pregunta abierta que busca determinar si todo problema de decisión cuya solución puede verificarse en tiempo polinomial también puede resolverse en tiempo polinomial.

## Formulación

$$
\mathrm{P}\stackrel{?}{=}\mathrm{NP}
$$

- $\mathrm{P}$: problemas de decisión resolubles en tiempo polinomial por un algoritmo determinista.
- $\mathrm{NP}$: problemas de decisión cuyas soluciones afirmativas poseen certificados verificables en tiempo polinomial.

## Ejemplo mínimo

En [[Satisfacibilidad de circuitos|satisfacibilidad de circuitos]], una asignación que hace verdadera la salida puede verificarse rápidamente, pero no se conoce un algoritmo polinomial que siempre encuentre tal asignación o determine que no existe.

## Contraejemplo o límites

$\mathrm{NP}$ no significa “no polinomial”. Se sabe que $\mathrm{P}\subseteq\mathrm{NP}$; lo desconocido es si la inclusión es estricta.

## Relaciones

- Requiere conocer: [[Tiempo polinomial|Tiempo polinomial]].
- Caso representativo: [[Satisfacibilidad de circuitos|Satisfacibilidad de circuitos]].
- Pertenece a: teoría de la complejidad computacional.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositiva 19.
- Estado: problema abierto; la presentación lo describe como la “pregunta del millón”.
