---
tipo: concepto
aliases:
  - Dynamic programming
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: semilla
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, diseno]
---

# Programación dinámica

## Definición

Paradigma que resuelve subproblemas relacionados una sola vez y almacena sus resultados para construir la solución del problema completo.

## Intuición

Evita repetir trabajo cuando una descomposición genera los mismos subproblemas muchas veces.

## Ejemplo mínimo

Los números de Fibonacci pueden calcularse guardando los valores anteriores, en vez de recomputar recursivamente cada subárbol.

## Contraejemplo o límites

No toda recursión requiere programación dinámica: debe existir solapamiento de subproblemas y una relación que permita componer soluciones.

## Relaciones

- Es un: [[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]].
- Contrasta con: [[Divide y vencerás|Divide y vencerás]] cuando los subproblemas son independientes.
- Contrasta con: [[Algoritmo voraz|Algoritmo voraz]] al considerar varias subsoluciones antes de decidir.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositiva 14. El paradigma solo se menciona; definición y ejemplos deberán revisarse al estudiarlo.

