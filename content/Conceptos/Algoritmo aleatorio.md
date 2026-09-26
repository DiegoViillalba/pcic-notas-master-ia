---
tipo: concepto
aliases:
  - Algoritmo probabilístico
  - Randomized algorithm
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: semilla
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, diseno, probabilidad]
---

# Algoritmo aleatorio

## Definición

Algoritmo que utiliza elecciones aleatorias durante su ejecución, por lo que su tiempo, trayectoria o salida puede depender del azar.

## Intuición

La aleatoriedad puede evitar casos adversos, simplificar un diseño o permitir una respuesta útil cuando una solución determinista exacta es demasiado costosa.

## Ejemplo mínimo

Elegir un pivote al azar en quicksort hace que el tiempo de ejecución sea una variable aleatoria.

## Contraejemplo o límites

“Aleatorio” no significa “sin garantías”: deben especificarse la probabilidad de error, el tiempo esperado o la certeza de la salida, según el tipo de algoritmo.

## Relaciones

- Es un: [[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]].
- Se evalúa mediante: probabilidad de éxito, error y [[Complejidad temporal|tiempo esperado]].

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 14 y 20. El paradigma solo se menciona; su clasificación queda pendiente.

