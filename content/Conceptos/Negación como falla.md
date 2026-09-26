---
tipo: concepto
aliases:
  - "\\+ en Prolog"
  - Negation as failure
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]]"
tags: [concepto, programacion, prolog, logica, programacion-logica]
---

# Negación como falla (`\+`)

## Definición

En Prolog, `\+ G` tiene éxito si Prolog **no logra demostrar** `G` con el programa actual (falla finita de `G`), y falla si `G` sí se puede demostrar. No es la negación lógica clásica: solo refleja lo que el programa puede o no derivar, no una verdad absoluta.

$$
\text{\texttt{\textbackslash+ G}}\ \text{tiene éxito}\iff G\ \text{no es demostrable a partir del programa.}
$$

## Ejemplo

~~~prolog
a. b. c. d.
e :- fail.

y :- b, \+ e, a.
~~~

`e` nunca se puede demostrar (su única regla siempre falla). Por eso `\+ e` tiene éxito, y la regla `y` se cumple porque también se cumplen `b` y `a`.

## Riesgo: variables libres

Si `G` contiene variables sin instanciar, `\+ G` puede no significar lo que se espera, porque solo se comprueba si *existe* alguna manera de demostrar `G`; no enumera valores para la variable como sí lo hace una meta positiva.

## Relaciones

- Se combina con hechos y reglas descritas en [[Prolog|Prolog]].
- Contrasta con la enumeración de soluciones vía [[Backtracking en Prolog|backtracking]]: `\+ G` nunca liga variables, solo indica si G falla por completo.

## Procedencia

- Clase: [[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]].
- Fuente: `Proposiciones.pl`.
