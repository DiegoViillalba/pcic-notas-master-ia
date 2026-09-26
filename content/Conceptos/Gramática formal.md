---
tipo: concepto
aliases:
  - Formal grammar
area: programación avanzada
materias:
  - "[[Indice|Programación Avanzada]]"
estado: semilla
fuentes:
  - "[[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas]]"
tags: [concepto, programacion-avanzada, lenguajes-formales]
---

# Gramática formal

## Definición inicial

Sistema finito de símbolos y reglas que describe cómo generar las cadenas válidas de un lenguaje.

## Formulación inicial

$$
G=(V,T,S,P),
$$

donde $T$ contiene los terminales, $S$ es el símbolo inicial y $P$ contiene las producciones.

## Ejemplo mínimo

Con $S\to aS\mid b$, la gramática genera `b`, `ab`, `aab` y, en general, $a^nb$ para $n\geq0$.

## Relaciones

- Genera un: [[Lenguaje de programación|Lenguaje formal o de programación]].
- Se clasifica mediante la: [[Jerarquía de Chomsky|Jerarquía de Chomsky]].

## Procedencia

- Clase: [[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas y técnicas de programación]].
- Fuente: diapositivas 3–5.

## Para completar

- [ ] Explicar derivación, árbol sintáctico y ambigüedad.
- [ ] Construir una gramática pequeña para expresiones aritméticas.

