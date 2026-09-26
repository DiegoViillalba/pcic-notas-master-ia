---
tipo: concepto
aliases:
  - Logistic growth
  - Ecuación logística
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

# Crecimiento logístico

## Definición

El crecimiento logístico modela una población cuya tasa per cápita disminuye linealmente conforme aumenta la población y se aproxima a una capacidad de carga.

## Intuición

Cuando la población es pequeña respecto de los recursos disponibles, su crecimiento se parece al exponencial. Al aumentar la población, la competencia reduce el crecimiento; cerca de la capacidad de carga, los aumentos y las pérdidas se equilibran.

## Supuestos

- La capacidad de carga $K$ es constante.
- La población puede representarse como una variable continua.
- La tasa per cápita disminuye linealmente con $P/K$.
- No hay retrasos, estructura por edades ni variaciones aleatorias explícitas.

## Formulación

$$
\frac{dP}{dt}=rP\left(1-\frac{P}{K}\right),
\qquad P(0)=P_0.
$$

$P(t)$ es la población, $r>0$ la tasa de crecimiento intrínseca con unidades de tiempo$^{-1}$ y $K>0$ la capacidad de carga con las mismas unidades que $P$.

Los factores tienen papeles distintos:

- $rP$ produce el crecimiento exponencial que ocurriría sin restricciones;
- $1-P/K$ representa la fracción de capacidad todavía disponible.

## Solución analítica

Para $P_0>0$,

$$
P(t)=\frac{K}{1+\left(\frac{K-P_0}{P_0}\right)e^{-rt}}.
$$

## Equilibrios y comportamiento

Los equilibrios se obtienen de

$$
rP\left(1-\frac{P}{K}\right)=0,
$$

por lo que son $P^*=0$ y $P^*=K$. Para $r>0$, $P=0$ es inestable y $P=K$ es estable:

- si $0<P_0<K$, $P(t)$ crece hacia $K$;
- si $P_0>K$, $P(t)$ decrece hacia $K$;
- si $P_0=K$, permanece constante.

Cuando $0<P_0<K$, la tasa de crecimiento absoluta es máxima en $P=K/2$, punto de inflexión de la curva sigmoide.

## Ejemplo mínimo

Si $P_0=100$, $r=0.2$ año$^{-1}$ y $K=1000$,

$$
P(t)=\frac{1000}{1+9e^{-0.2t}}.
$$

Al principio la población crece casi exponencialmente, pero a largo plazo se aproxima a $1000$.

## Contraejemplo o límites

No es adecuado cuando la capacidad de carga cambia rápidamente, existen retrasos importantes, la población tiene estructura interna relevante o la variabilidad aleatoria domina. La capacidad de carga es un parámetro del modelo, no necesariamente un límite físico fijo y conocido.

## Relaciones

- Se formula mediante: [[Balance de tasas|Balance de tasas]].
- Extiende: [[Crecimiento exponencial|Crecimiento exponencial]].
- Puede aproximarse con: [[Método de Euler|Método de Euler]].
- Puede estudiarse mediante: [[Experimento computacional|Experimento computacional]].

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
- Clase: [[2026-08-17 ModMat - Modelos de cambio y método de Euler|Modelos de cambio y método de Euler]].

