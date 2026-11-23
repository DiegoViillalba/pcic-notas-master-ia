---
tipo: concepto
aliases: [Probability factor, Factor de probabilidad]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-13 IA - Inferencia en redes bayesianas]]"
  - "[[AI 15 Inferencia en redes bayesianas.pdf]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf]]"
tags: [concepto, inteligencia-artificial, redes-bayesianas]
---

# Factor probabilístico

## Pregunta

¿Qué representación nos permite multiplicar información local y resumir variables durante la inferencia?

## Definición e intuición

Un factor es una función no negativa sobre asignaciones de un conjunto de variables. Ese conjunto es su **alcance** o *scope*. Para variables discretas, podemos representarlo como una tabla con una entrada por asignación del alcance.

Las CPT son factores iniciales. Los productos, las restricciones por evidencia y las sumas producen otros factores; no todos representan distribuciones normalizadas.

## Operaciones

Para $f(X,Y)$ y $g(Y,Z)$:

$$
h(X,Y,Z)=f(X,Y)g(Y,Z).
$$

El alcance del producto es la unión de los alcances; se multiplican entradas con el mismo valor compartido de $Y$. Es un producto punto a punto sobre asignaciones compatibles, no multiplicación de matrices.

Eliminar $Y$ significa $k(X,Z)=\sum_Y h(X,Y,Z)$. Restringir $Y=y$ significa sustituir ese valor; el alcance del factor restringido ya no incluye $Y$.

## Ejemplo mínimo

Supongamos $P(R=+)=0.1$, $P(T=+\mid R=+)=0.8$ y $P(T=+\mid R=-)=0.1$.

1. El producto $P(R)P(T\mid R)$ tiene alcance $\{R,T\}$.
2. Sus entradas para $T=+$ son $0.1(0.8)=0.08$ y $0.9(0.1)=0.09$.
3. Al sumar $R$, el factor sobre $T$ tiene entrada $P(T=+)=0.17$.

## Límites y confusiones

Una CPT booleana $P(T\mid R)$ suma uno sobre $T$ para cada valor de $R$; sumar todas sus entradas da dos. Un factor general no está obligado a sumar uno. Para eliminar una variable en un producto, debemos reunir todos los factores que la mencionan antes de sumarla.

Un factor de alcance $S$ necesita $\prod_{X\in S}|\operatorname{Dom}(X)|$ entradas en una representación tabular densa. El tamaño puede crecer mucho al multiplicar factores pequeños.

## Relaciones

- Es la representación utilizada por [[Eliminación de variables]].
- Permite calcular los productos de [[Inferencia por enumeración]].

## Procedencia

- Clase: [[2026-10-13 IA - Inferencia en redes bayesianas|13 de octubre de 2026]], §§7–10.
- Presentación AI 15, diapositivas 17–21.
- AIMA, 4.ª edición global, §13.3.2, pp. 448–450.
