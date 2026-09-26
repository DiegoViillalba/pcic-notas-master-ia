---
tipo: concepto
aliases:
  - Terminación
  - Algorithm termination
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, correccion]
---

# Terminación de un algoritmo

## Definición

Propiedad por la que un algoritmo finaliza después de un número finito de pasos para toda entrada permitida.

## Intuición

No basta con que el procedimiento produzca una respuesta si llega al final: también hay que descartar ejecuciones infinitas.

## Formulación

$$
\forall x\in I,\; \exists t<\infty \text{ tal que la ejecución de }A(x)\text{ se detiene en }t.
$$

## Ejemplo mínimo

La búsqueda lineal termina porque su ciclo examina como máximo las $n$ posiciones del arreglo.

## Contraejemplo o límites

Un ciclo cuyo progreso no está acotado ni se justifica con una medida decreciente puede no terminar.

## Relaciones

- Junto con: [[Validez de un algoritmo|Validez de un algoritmo]].
- Se utiliza en: demostraciones de corrección total.
- Contrasta con: [[Problema de la parada|Problema de la parada]], que limita la verificación automática de esta propiedad en general.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 11–13.
