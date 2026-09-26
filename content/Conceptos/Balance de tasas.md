---
tipo: concepto
aliases:
  - Rate balance
  - Ecuación de balance
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

# Balance de tasas

## Definición

Un balance de tasas describe cómo cambia una cantidad almacenada al contabilizar los procesos que la aumentan y los que la disminuyen:

$$
\text{tasa de acumulación}
=\text{tasas de entrada}-\text{tasas de salida}
+\text{tasas de generación}-\text{tasas de consumo}.
$$

## Intuición

El balance funciona como una contabilidad: una cantidad solo puede cambiar si algo entra, sale, se genera o se consume. Separar esos mecanismos ayuda a asignar signos correctos y a detectar términos ausentes.

## Formulación

Si $x(t)$ es la cantidad almacenada,

$$
\frac{dx}{dt}=\sum_i E_i(t,x)-\sum_j S_j(t,x)+G(t,x)-C(t,x).
$$

Todos los términos deben tener las mismas unidades que $dx/dt$.

En tiempo discreto, el balance equivalente es

$$
x_{n+1}=x_n+\text{entradas del paso}-\text{salidas del paso}
+\text{generación}-\text{consumo}.
$$

## Ejemplo mínimo

Si entran $8$ L/min a un tanque y sale un volumen por unidad de tiempo igual a $0.3V$, entonces

$$
\frac{dV}{dt}=8-0.3V.
$$

La entrada es positiva y la fuga negativa. Como $[0.3]=\text{min}^{-1}$, ambos términos se miden en L/min.

## Contraejemplo o límites

El balance no determina por sí solo las expresiones de cada tasa; estas dependen de supuestos físicos o empíricos. Tampoco basta escribir “entrada menos salida” si se omiten fuentes internas, reacciones, retrasos o cambios de volumen relevantes.

## Relaciones

- Se utiliza en: [[Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]].
- Se utiliza en: [[Crecimiento exponencial|Crecimiento exponencial]].
- Se utiliza en: [[Crecimiento logístico|Crecimiento logístico]].
- Requiere definir: [[Variable y parámetro de un modelo|variables y parámetros del modelo]].

## Procedencia

- Clase: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].

