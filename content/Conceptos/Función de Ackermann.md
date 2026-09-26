---
tipo: concepto
aliases:
  - Ackermann
  - A(m,n)
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]]"
tags: [concepto, programacion, recursion, induccion, verificacion-formal]
---

# Función de Ackermann

## Definición

Función doblemente recursiva de dos variables, propuesta por Wilhelm Ackermann (1928):

$$
A(m,n)=
\begin{cases}
n+1 & \text{si } m=0\\
A(m-1,1) & \text{si } m>0 \text{ y } n=0\\
A\big(m-1,A(m,n-1)\big) & \text{si } m>0 \text{ y } n>0
\end{cases}
$$

## Resultados cerrados (demostrados por inducción en cascada)

| \(m\) | \(A(m,z)\) |
|---:|---|
| 0 | \(z+1\) |
| 1 | \(z+2\) |
| 2 | \(2z+3\) |
| 3 | \(2^{z+3}-3\) |
| 4 | torre de potencias de 2, \(z+2\) veces, menos 3 |

Cada fila se demuestra por inducción sobre \(z\) **usando el resultado ya probado de la fila anterior** como hipótesis auxiliar dentro del paso inductivo.

## Por qué crece tan rápido

A partir de \(m=3\)–\(4\) el crecimiento deja de ser exponencial simple y se vuelve una torre de exponenciales. Por ejemplo, \(A(4,1)=65533\) y \(A(4,2)=2^{65536}-3\) (19 729 dígitos). Se usa históricamente como ejemplo de función **no primitiva-recursiva**.

## Propiedad con inducción sobre dos variables

$$
\forall\,x,y\in\mathbb{N}_0:\quad y+1\le A(x,y).
$$

Se demuestra con una inducción sobre \(x\) que contiene, dentro de su paso inductivo, una segunda inducción sobre \(y\).

## Uso en ternas de Hoare

Una vez demostrado \(A(1,z)=z+2\), se puede usar como lema dentro de una verificación de programas:

$$
\{x=1\}\ w:=A(x,y)\ \{w=y+2\}
$$

combinando el axioma de asignación con la [[Regla de consecuencia de Hoare|regla de consecuencia]].

## Relaciones

- Se demuestra con: [[Principio de inducción matemática modificado|principio de inducción modificado]] (inducción anidada, sobre dos variables).
- Comparte estructura con: [[Función 91 de McCarthy|función 91 de McCarthy]] (recursión doble).
- Se combina con: [[Terna de Hoare|terna de Hoare]] y [[Regla de consecuencia de Hoare|regla de consecuencia]].

## Procedencia

- Clase: [[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]].
- Fuente: *Programación Avanzada Notas 7*, láminas 126–138.
