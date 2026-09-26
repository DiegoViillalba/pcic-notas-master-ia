---
tipo: concepto
aliases:
  - Model variable
  - Model parameter
  - Variable de modelo
  - Parámetro de modelo
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-10 ModMat - Introducción al modelado|Introducción al modelado]]"
tags:
  - concepto
  - modelacion-matematica
---

# Variable y parámetro de un modelo

## Definición

Una **variable** es una magnitud que cambia o se calcula dentro del modelo. Un **parámetro** caracteriza el sistema y normalmente se fija durante una ejecución o escenario.

## Intuición

La distinción depende de la pregunta y la escala. Una cantidad puede mantenerse fija en una simulación y convertirse en variable cuando se comparan muchos escenarios.

## Ejemplo mínimo

En

$$
\frac{dP}{dt}=rP,
$$

$P(t)$ es una variable dependiente y $r$ es un parámetro. Al estudiar sensibilidad respecto de $r$, este toma múltiples valores, aunque siga funcionando como parámetro en cada ejecución.

## Relaciones

- Forma parte de un [[Modelo matemático|modelo matemático]].
- La exploración de muchos parámetros puede producir un [[Experimento computacional|experimento computacional]].

## Procedencia

- Clase: [[2026-08-10 ModMat - Introducción al modelado|Introducción al modelado]]

