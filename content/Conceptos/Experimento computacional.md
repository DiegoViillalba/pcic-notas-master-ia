---
tipo: concepto
aliases:
  - Computational experiment
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-10 ModMat - Introducción al modelado|Introducción al modelado]]"
tags:
  - concepto
  - modelacion-matematica
  - computacion-cientifica
---

# Experimento computacional

## Definición

Estudio sistemático de un modelo mediante algoritmos y ejecuciones computacionales para explorar escenarios, parámetros, incertidumbre o comportamiento a distintas escalas.

## Intuición

Resolver un modelo una sola vez responde qué ocurre bajo una configuración. Ejecutarlo sobre miles de configuraciones permite estudiar sensibilidad, incertidumbre y robustez, pero introduce costos de tiempo, memoria y paralelismo.

## Ejemplo mínimo

Resolver una ecuación logística para una combinación de $r$, $K$ y $P_0$ es una simulación. Repetirla para miles de combinaciones y comparar sus resultados constituye un experimento computacional.

## Cuándo puede requerir HPC

- Miles o millones de escenarios.
- Muchos parámetros o muestras.
- Datos de gran volumen.
- Mallas espaciales o temporales finas.
- Ejecuciones independientes que pueden paralelizarse.

## Relaciones

- Evalúa un [[Modelo matemático|modelo matemático]].
- Explora [[Variable y parámetro de un modelo|parámetros]].
- Requiere distinguir modelo, algoritmo y ejecución.

## Procedencia

- Clase: [[2026-08-10 ModMat - Introducción al modelado|Introducción al modelado]]

