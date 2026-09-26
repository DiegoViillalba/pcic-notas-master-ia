---
tipo: concepto
aliases:
  - Búsqueda secuencial
  - Linear search
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, busqueda]
---

# Búsqueda lineal

## Definición

Algoritmo que examina secuencialmente los elementos de una colección hasta encontrar el valor buscado o agotar la colección.

## Formulación

```text
para c = 1 hasta n:
    si A[c] = x: devolver c
devolver NULL
```

## Ejemplo mínimo

Para $A=[4,7,2]$ y $x=7$, compara primero con $4$ y después con $7$; devuelve la posición 2.

## Análisis

- Terminación: a lo más $n$ iteraciones.
- Validez: revisa todas las posiciones hasta encontrar $x$.
- Tiempo en peor caso: $O(n)$.
- Espacio auxiliar: $O(1)$.

## Contraejemplo o límites

No aprovecha que la colección esté ordenada. Otras estructuras o algoritmos pueden permitir búsquedas más rápidas bajo supuestos adicionales.

## Relaciones

- Es un caso de: [[Algoritmo|Algoritmo]].
- Ilustra: [[Terminación de un algoritmo|terminación]], [[Validez de un algoritmo|validez]], [[Complejidad temporal|tiempo]] y [[Complejidad espacial|espacio]].

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 12–13.
