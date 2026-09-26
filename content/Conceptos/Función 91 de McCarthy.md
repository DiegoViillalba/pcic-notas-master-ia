---
tipo: concepto
aliases:
  - mc91
  - Función 91
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]]"
tags: [concepto, programacion, recursion, induccion, verificacion-formal]
---

# Función 91 de McCarthy

## Definición

Función propuesta por John McCarthy (1970) como ejemplo clásico de verificación de programas recursivos:

$$
f(x)=
\begin{cases}
x-10 & \text{si } x>100\\
f\big(f(x+11)\big) & \text{si } x\le 100
\end{cases}
$$

## Por qué es un ejemplo relevante

La rama recursiva llama a `f` **dos veces anidadas** (recursión doble) y el argumento interno puede crecer antes de que la recursión toque el caso base. No es evidente, solo con la definición, que la recursión termine ni que produzca siempre el mismo valor.

## Resultado principal

$$
f(x)=91\ \ \forall\ \text{entero } x\le100,
\qquad
f(x)=x-10\ \ \forall\ x>100.
$$

Se demuestra con el [[Principio de inducción matemática modificado|principio de inducción modificado]], bajando desde el techo \(k=100\): el paso inductivo separa dos casos según si \(x+11\) supera 100 o no, y en ambos usa que la propiedad ya vale para valores mayores que \(x\).

## Implementación (C#)

~~~csharp
public static int mc91( int n )
{
    if (n > 100) return n - 10;
    else         return mc91( mc91( n + 11 ) );
}
~~~

## Relaciones

- Se demuestra con: [[Principio de inducción matemática modificado|principio de inducción modificado]].
- Comparte estructura (recursión doble, inducción anidada) con: [[Función de Ackermann|función de Ackermann]].
- Contrasta con: [[Inducción matemática aplicada a ciclos|inducción aplicada a ciclos]] (esa sube desde 0; esta baja desde un techo fijo).

## Procedencia

- Clase: [[2026-09-03 ProgAv - Función 91 de McCarthy, inducción modificada y función de Ackermann|Función 91 de McCarthy, inducción modificada y función de Ackermann]].
- Fuentes: *Programación Avanzada Notas 7*, láminas 118–125; proyecto `Funcion91JohnMcCarthy` (Visual Studio).
