---
tipo: concepto
aliases:
  - Quicksort
  - Ordenamiento rápido
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Clase del 18 de agosto]]"
tags: [concepto, algoritmos, ordenamiento, divide-y-venceras]
---

# QuickSort

## Definición

Algoritmo de ordenamiento por [[Divide y vencerás|divide y vencerás]] que elige un pivote, particiona los elementos según su relación con él y ordena recursivamente las particiones.

## Intuición

Después de particionar, ningún elemento del lado izquierdo necesita cruzar con uno del lado derecho para respetar el orden relativo al pivote. Por ello, ambas regiones pueden ordenarse de forma independiente.

## Formulación

Para particiones de tamaños $k$ y $n-k-1$:

$$
T(n)=T(k)+T(n-k-1)+\Theta(n).
$$

Su tiempo típico o esperado es $\Theta(n\log n)$ y su peor caso es $\Theta(n^2)$. Una implementación in-place usa memoria adicional asociada principalmente con la pila recursiva.

## Ejemplo mínimo

En `[4, 2, 5, 1, 3]`, elegir `3` permite formar regiones con valores menores y mayores: `[2, 1]`, `[3]`, `[4, 5]`. Al ordenar recursivamente las regiones se obtiene `[1, 2, 3, 4, 5]`.

## Contraejemplo o límites

Elegir siempre un valor extremo como pivote produce particiones de tamaños $0$ y $n-1$ y conduce al peor caso. QuickSort tampoco es estable en sus implementaciones in-place habituales.

## Relaciones

- Es un caso de: [[Divide y vencerás|Divide y vencerás]].
- Contrasta con: ordenamiento por mezcla, que realiza la mayor parte del trabajo al combinar.
- Requiere conocer: recursión, partición e [[Invariante de ciclo|invariante de ciclo]].

## Procedencia

- Clase: [[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Divide y vencerás, QuickSort y backtracking]].
- Fuente: *Programación Avanzada Notas 2*, diapositivas 24-25; `Qsort.PAS`.
