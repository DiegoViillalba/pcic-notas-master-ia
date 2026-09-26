---
tipo: concepto
aliases:
  - Relación de fortalecimiento
  - Aserción fuerte y débil
  - Logical strength
area: logica
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, logica, aserciones, logica-de-hoare]
---

# Fortaleza lógica de una aserción

## Definición

Una aserción $R$ es más fuerte que $S$ si todo estado que satisface $R$ también satisface $S$; equivalentemente, $R\Rightarrow S$ es válida.

## Intuición

Una condición más fuerte es más restrictiva y admite menos estados. Debilitar una condición permite más estados.

## Formulación

Si $\llbracket P\rrbracket$ es el conjunto de estados que satisfacen $P$:

$$
R\Rightarrow S
\iff
\llbracket R\rrbracket\subseteq\llbracket S\rrbracket.
$$

$\bot$ es la aserción más fuerte y $\top$ la más débil.

## Ejemplo mínimo

$$
i>5\Rightarrow i>0,
\qquad
i>0\not\Rightarrow i>5.
$$

```text
false  ->  i > 5  ->  i > 0  ->  true
más fuerte                         más débil
```

## Contraejemplo o límites

La implicación no suele ser reversible. $y=4\Rightarrow y\ne0$, pero $y\ne0$ permite muchos valores distintos de $4$.

## Aplicación práctica

Si una prueba hacia atrás calcula $wlp(C,Q)$, la precondición declarada $P$ basta exactamente cuando

$$
P\Rightarrow wlp(C,Q).
$$

Esa implicación es una [[Condición de verificación|condición de verificación]]. Practica la comparación de condiciones en [[Guía paso a paso - Lógica de Hoare#8. Ejercicios graduados|los ejercicios graduados]].

## Relaciones

- Compara: [[Aserción de programa|aserciones de programa]].
- Fundamenta: [[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]].
- Permite comparar una precondición declarada con la [[Precondición más débil|precondición más débil]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 11–15 (láminas 65–69).
