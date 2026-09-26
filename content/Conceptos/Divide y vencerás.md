---
tipo: concepto
aliases:
  - Divide and conquer
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
  - "[[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Clase del 18 de agosto]]"
tags: [concepto, algoritmos, diseno]
---

# Divide y vencerás

## Definición

Paradigma que divide un problema en subproblemas más pequeños, los resuelve —normalmente de forma recursiva— y combina sus soluciones.

## Intuición

La técnica funciona cuando resolver varias versiones menores del mismo problema y ensamblar sus resultados es más sencillo que atacar directamente la instancia completa. Debe existir un caso base y cada llamada debe reducir el tamaño del problema.

## Formulación

Un esquema frecuente es:

$$
T(n)=aT(n/b)+f(n),
$$

donde $a$ es el número de subproblemas, $n/b$ su tamaño y $f(n)$ el costo de dividir y combinar.

## Ejemplo mínimo

Ordenamiento por mezcla divide el arreglo en dos mitades, ordena cada mitad y después las mezcla.

QuickSort particiona alrededor de un pivote, ordena las regiones obtenidas y aprovecha que la partición ya establece la relación entre ambos lados.

## Contraejemplo o límites

Si los subproblemas se traslapan mucho y se recalculan, puede convenir [[Programación dinámica|programación dinámica]].

## Relaciones

- Es un: [[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]].
- Se utiliza en: [[QuickSort|QuickSort]] y búsqueda binaria.
- Contrasta con: [[Backtracking|backtracking]].
- Requiere analizar: recursión, casos base y costo de combinación.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositiva 14. El paradigma solo se menciona; definición y ejemplos deberán revisarse al estudiarlo.
- Clase: [[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Divide y vencerás, QuickSort y backtracking]].
- Fuente: *Programación Avanzada Notas 2*, diapositivas 22-32.
