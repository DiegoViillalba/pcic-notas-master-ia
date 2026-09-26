---
tipo: concepto
aliases:
  - Exponential growth
  - Crecimiento malthusiano
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]]"
  - "[[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]]"
tags:
  - concepto
  - modelacion-matematica
  - ecuaciones-diferenciales
---

# Crecimiento exponencial

## Definición

El crecimiento exponencial describe una cantidad cuya tasa de cambio instantánea es proporcional a su valor actual. Su tasa relativa de crecimiento permanece constante.

## Intuición

Una cantidad mayor produce un incremento absoluto mayor durante el mismo intervalo: el crecimiento se retroalimenta. En una población, más individuos implican más nacimientos si cada individuo mantiene la misma contribución promedio.

## Formulación continua

$$
\frac{dP}{dt}=rP,
\qquad P(0)=P_0.
$$

$P(t)$ es la cantidad, $P_0$ su valor inicial y $r$ la tasa per cápita, con unidades de tiempo$^{-1}$. Separando variables,

$$
\frac{dP}{P}=r\,dt
\quad\Longrightarrow\quad
\ln P=rt+C,
$$

de donde

$$
P(t)=P_0e^{rt}.
$$

Si $r>0$ hay crecimiento; si $r<0$ hay decaimiento; si $r=0$, la cantidad permanece constante.

## Formulación discreta

Si la cantidad aumenta una fracción $q$ en cada paso,

$$
P_{n+1}=(1+q)P_n,
\qquad
P_n=P_0(1+q)^n.
$$

La tasa discreta $q$ no es idéntica a la tasa continua $r$. Para que ambos modelos coincidan después de una unidad de tiempo debe cumplirse $1+q=e^r$.

## Tiempo de duplicación

Para $r>0$, al resolver $P(t_d)=2P_0$ se obtiene

$$
t_d=\frac{\ln 2}{r}.
$$

## Ejemplo mínimo

Una colonia con $P_0=200$ que aumenta $15\%$ por generación sigue

$$
P_n=200(1.15)^n.
$$

Después de tres generaciones, $P_3\approx304.18$; según el contexto, el resultado puede redondearse a individuos enteros.

## Contraejemplo o límites

El modelo supone una tasa relativa constante y no incorpora recursos limitados, competencia ni cambios ambientales. Por ello suele describir solo una etapa de un proceso real y no un crecimiento indefinido.

## Relaciones

- Se formula mediante: [[Balance de tasas|Balance de tasas]].
- Contrasta con: [[Crecimiento logístico|Crecimiento logístico]].
- Comparte estructura con: [[Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]].
- Es un ejemplo de: [[Clasificación de modelos matemáticos|modelo continuo y determinista]].

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
- Clase: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].

