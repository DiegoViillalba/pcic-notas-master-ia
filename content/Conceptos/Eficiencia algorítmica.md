---
tipo: concepto
aliases:
  - Algorithmic efficiency
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad]
---

# Eficiencia algorítmica

## Definición

Uso suficientemente moderado de recursos —principalmente tiempo y memoria— conforme crece el tamaño de la entrada. En la presentación, “eficiente” se aproxima a tiempo polinomial.

## Intuición

Un algoritmo correcto puede no servir en la práctica si requiere explorar una cantidad factorial o exponencial de posibilidades.

## Formulación

Como criterio grueso del curso:

$$
T(n)=O(n^k)\text{ para alguna constante }k \quad\Longrightarrow\quad \text{tiempo polinomial}.
$$

## Ejemplo mínimo

La búsqueda lineal es eficiente porque usa tiempo $O(n)$ y espacio auxiliar $O(1)$.

## Contraejemplo o límites

Enumerar más de $n!$ rutas puede producir la ruta mínima y aun así ser inservible. Tiempo polinomial es una aproximación teórica: un grado o constantes grandes también pueden dificultar el uso práctico.

## Relaciones

- Depende de: [[Complejidad temporal|Complejidad temporal]] y [[Complejidad espacial|Complejidad espacial]].
- Se asocia con: [[Tiempo polinomial|Tiempo polinomial]].
- Contrasta con: [[Validez de un algoritmo|Validez de un algoritmo]], que no mide recursos.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 15–20.
