---
tipo: concepto
aliases:
  - Algorithm
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, fundamentos]
---

# Algoritmo

## Definición

Secuencia finita y bien definida de instrucciones que transforma una entrada en una salida para solucionar un problema.

## Intuición

Se parece a una receta, pero cada paso, entrada y condición de finalización debe estar especificado sin ambigüedad.

## Formulación

Puede verse como una transformación $A:I\to O$, acompañada por un procedimiento efectivo que termina para las entradas de su dominio.

## Ejemplo mínimo

Recorrer un arreglo desde la primera posición y devolver el índice del primer elemento igual a $x$; si ninguno coincide, devolver `NULL`.

## Contraejemplo o límites

“Buscar hasta que parezca suficiente” no define un algoritmo: no precisa el criterio de terminación ni todos los pasos.

## Relaciones

- Se analiza mediante: [[Terminación de un algoritmo|terminación]], [[Validez de un algoritmo|validez]], [[Complejidad temporal|tiempo]] y [[Complejidad espacial|espacio]].
- Se formaliza mediante modelos como la [[Máquina de Turing|máquina de Turing]].
- Se construye con un [[Paradigma de diseño de algoritmos|paradigma de diseño de algoritmos]].

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 2–4.
