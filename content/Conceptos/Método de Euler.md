---
tipo: concepto
aliases:
  - Euler method
  - Euler explícito
  - Método de Euler hacia adelante
area: métodos numéricos
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]]"
tags:
  - concepto
  - modelacion-matematica
  - metodos-numericos
  - ecuaciones-diferenciales
---

# Método de Euler

## Definición

El método de Euler explícito aproxima la solución de un problema de valor inicial avanzando en pasos y usando en cada paso la pendiente evaluada en el punto actual.

## Intuición

Una solución de $y'=f(t,y)$ sigue localmente su recta tangente. Euler reemplaza un tramo corto de la curva por esa recta y repite el procedimiento desde el nuevo punto aproximado.

## Formulación

Para

$$
y'=f(t,y), \qquad y(t_0)=y_0,
$$

y un tamaño de paso $h>0$,

$$
t_{n+1}=t_n+h,
\qquad
y_{n+1}=y_n+h f(t_n,y_n).
$$

La fórmula procede de truncar la expansión de Taylor:

$$
y(t_n+h)=y(t_n)+h y'(t_n)+O(h^2).
$$

Si la solución es suficientemente regular, el error local de truncamiento es $O(h^2)$ y el error global acumulado en un intervalo fijo es $O(h)$; por eso Euler es un método de primer orden.

## Ejemplo mínimo

Para

$$
y'=y, \qquad y(0)=1,
$$

con $h=0.1$,

$$
y_1=1+0.1(1)=1.1,
$$

mientras que la solución exacta da $y(0.1)=e^{0.1}\approx1.10517$.

## Contraejemplo o límites

Un paso menor suele mejorar la aproximación, pero exige más iteraciones. Un paso demasiado grande puede causar errores importantes o inestabilidad; en problemas rígidos, Euler explícito puede requerir pasos imprácticamente pequeños.

## Relaciones

- Es una: [[Solución analítica y solución numérica|solución numérica]].
- Se deriva mediante: expansión de Taylor.
- Puede aplicarse a: [[Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]].
- Puede aplicarse a: [[Crecimiento logístico|Crecimiento logístico]].

## Procedencia

- Clase: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].
