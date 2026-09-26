---
tipo: concepto
aliases:
  - Algoritmo greedy
  - Greedy algorithm
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: semilla
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, diseno]
---

# Algoritmo voraz

## Definición

Paradigma que construye una solución mediante una secuencia de elecciones localmente preferibles, sin reconsiderar decisiones anteriores.

## Intuición

Busca convertir buenas decisiones inmediatas en una solución global; para que sea correcto, el problema debe poseer una estructura que lo justifique.

## Ejemplo mínimo

Seleccionar repetidamente la actividad compatible que termina primero es la idea voraz del problema clásico de selección de actividades.

## Contraejemplo o límites

Elegir lo mejor en cada paso no siempre produce el óptimo global. La propiedad voraz debe demostrarse para cada problema.

## Relaciones

- Es un: [[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]].
- Contrasta con: [[Programación dinámica|Programación dinámica]], que compara subsoluciones y reutiliza sus valores.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositiva 14. El paradigma solo se menciona; definición y ejemplos deberán revisarse al estudiarlo.

