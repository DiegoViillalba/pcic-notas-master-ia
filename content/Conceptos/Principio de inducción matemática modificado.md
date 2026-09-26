---
tipo: concepto
aliases:
  - Inducción modificada
  - Inducción hacia abajo desde un techo k
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]]"
tags: [concepto, programacion, induccion, recursion, verificacion-formal]
---

# Principio de inducción matemática modificado

## Definición

Sea \(k\) un entero fijo (positivo, negativo o cero). Para demostrar que una proposición \(P(n)\) es verdadera para toda \(n\le k\), basta demostrar:

1. **Paso básico:** \(P(k)\) es verdadera.
2. **Paso inductivo:** para toda \(n<k\), si \(P(m)\) es verdadera para **todo** \(m\) con \(n<m\le k\) (hipótesis de inducción), entonces \(P(n)\) es verdadera.

Entonces \(P(n)\) es verdadera para toda \(n\le k\).

## Diferencia con la inducción "hacia adelante"

| | Inducción sobre iteraciones | Inducción modificada |
|---|---|---|
| Dirección | Sube desde un caso base pequeño | Baja desde un techo fijo \(k\) |
| Alcance de la hipótesis | Un valor anterior específico | Todo el rango \((n,k]\) |
| Uso típico | Invariantes de ciclos | Funciones recursivas cuyo argumento crece antes de resolverse |

## Ejemplo mínimo

Para la [[Función 91 de McCarthy|función 91 de McCarthy]], con \(k=100\):

- Base: \(f(100)=91\), calculado directamente.
- Hipótesis: \(f(m)=91\) para todo \(m\) con \(x<m\le100\).
- Paso: al expandir \(f(x)=f(f(x+11))\), ambos argumentos intermedios (\(x+11\) y, en un caso, \(91\)) caen dentro del rango \((x,100]\), así que la hipótesis se aplica dos veces.

## Por qué hace falta la versión "fuerte" (rango completo) y no solo el vecino

Algunas demostraciones (como el caso `x+11 ≤ 100` de `mc91`) necesitan el valor de la propiedad en **más de un punto** mayor que \(x\), no solo en el sucesor inmediato. Una hipótesis que solo cubriera "el siguiente valor" no bastaría.

## Relaciones

- Generaliza/adapta: [[Inducción matemática aplicada a ciclos|inducción matemática aplicada a ciclos]].
- Se usa para demostrar: [[Función 91 de McCarthy|función 91 de McCarthy]], [[Función de Ackermann|función de Ackermann]].

## Procedencia

- Clase: [[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]].
- Fuente: *Programación Avanzada Notas 7*, lámina 121.
