---
tipo: concepto
aliases:
  - Newton's law of cooling
  - Ley de calentamiento y enfriamiento de Newton
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]]"
tags:
  - concepto
  - modelacion-matematica
  - ecuaciones-diferenciales
---

# Ley de enfriamiento de Newton

## Definición

La ley de enfriamiento de Newton modela la temperatura de un cuerpo suponiendo que su rapidez de cambio es proporcional a la diferencia entre su temperatura y la del ambiente.

## Intuición

Cuanto mayor es la diferencia térmica, más rápido cambia la temperatura. A medida que el cuerpo se acerca a la temperatura ambiente, esa diferencia disminuye y el cambio se vuelve más lento.

## Formulación

Si $T(t)$ es la temperatura del cuerpo, $T_a$ es una temperatura ambiente constante y $\kappa>0$ es el coeficiente de transferencia,

$$
\frac{dT}{dt}=-\kappa(T-T_a),
\qquad T(0)=T_0.
$$

Su solución es

$$
T(t)=T_a+(T_0-T_a)e^{-\kappa t}.
$$

Por tanto,

$$
\lim_{t\to\infty}T(t)=T_a.
$$

La misma ecuación describe calentamiento cuando $T_0<T_a$: el signo de $T-T_a$ hace que $dT/dt>0$.

## Ejemplo mínimo

Para un café con $T_0=90\,{}^\circ\mathrm C$ en una habitación a $T_a=20\,{}^\circ\mathrm C$,

$$
T(t)=20+70e^{-\kappa t}.
$$

Hace falta al menos una medición adicional $(t_1,T_1)$ para estimar $\kappa$:

$$
\kappa=-\frac{1}{t_1}\ln\left(\frac{T_1-20}{70}\right).
$$

## Contraejemplo o límites

El modelo pierde precisión si la temperatura ambiente varía, si existen cambios de fase, si la radiación domina o si el cuerpo no puede representarse mediante una sola temperatura uniforme.

## Relaciones

- Es una aplicación de: [[Balance de tasas|Balance de tasas]].
- Tiene la misma estructura matemática que: [[Crecimiento exponencial|decaimiento exponencial]].
- Puede aproximarse con: [[Método de Euler|Método de Euler]].
- Es un modelo continuo y determinista según: [[Clasificación de modelos matemáticos|Clasificación de modelos matemáticos]].

## Procedencia

- Clase: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].

