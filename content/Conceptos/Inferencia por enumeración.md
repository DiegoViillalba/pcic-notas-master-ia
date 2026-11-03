---
tipo: concepto
aliases: [Inference by enumeration]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-13 IA - Inferencia en redes bayesianas]]"
  - "[[AI 15 Inferencia en redes bayesianas.pdf]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf]]"
tags: [concepto, inteligencia-artificial, inferencia-probabilistica]
---

# Inferencia por enumeración

## Pregunta

¿Cómo obtenemos una posterior sumando las posibilidades que siguen abiertas después de observar evidencia?

## Definición e intuición

La inferencia por enumeración calcula el peso de cada valor consultado sumando las probabilidades de todos los mundos completos compatibles con ese valor y con la evidencia. Después divide cada peso entre la suma de los pesos.

Una variable oculta no se considera falsa ni se fija arbitrariamente: sus distintos valores describen posibilidades que contribuyen a la respuesta.

## Formulación

Para consulta $Q$, evidencia $\mathbf e$ y ocultas $\mathcal H$:

$$w(q)=\sum_{\mathbf h}P(q,\mathbf e,\mathbf h),\qquad P(q\mid\mathbf e)=\frac{w(q)}{\sum_{q'}w(q')}.$$

En una red bayesiana, la probabilidad de cada mundo es el producto de sus probabilidades locales. La posterior está definida por esta fórmula cuando la evidencia tiene probabilidad positiva.

## Ejemplo mínimo

Supongamos $P(+x,+y)=0.2$, $P(+x,-y)=0.3$, $P(-x,+y)=0.4$ y $P(-x,-y)=0.1$. Para consultar $P(X\mid-y)$:

1. Seleccionamos las dos filas con $Y=-y$.
2. Sus pesos son $0.3$ y $0.1$; no quedan ocultas que sumar.
3. Dividimos por $0.4$ y obtenemos $\langle0.75,0.25\rangle$ en el orden $(+x,-x)$.

## Límites y confusiones

- Si hay muchas ocultas, el número de asignaciones puede crecer exponencialmente.
- Enumerar no exige almacenar toda la conjunta: una implementación recursiva puede acumular pesos con espacio lineal.
- La normalización no permite resolver evidencia con probabilidad cero mediante división entre cero.

## Relaciones

- Contrasta con [[Eliminación de variables]], que reorganiza la misma suma para reutilizar cálculos.
- Utiliza [[Factor probabilístico|factores probabilísticos]] para evaluar los mundos en una red.

## Procedencia

- Clase: [[2026-10-13 IA - Inferencia en redes bayesianas|13 de octubre de 2026]], §§3–6.
- Presentación AI 15, diapositivas 9–14.
- AIMA, 4.ª edición global, §13.3.1, pp. 445–447: enumeración recursiva y repetición de subcálculos.
