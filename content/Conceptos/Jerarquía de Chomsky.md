---
tipo: concepto
aliases:
  - Chomsky hierarchy
area: programación avanzada
materias:
  - "[[Indice|Programación Avanzada]]"
estado: semilla
fuentes:
  - "[[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas]]"
tags: [concepto, programacion-avanzada, lenguajes-formales]
---

# Jerarquía de Chomsky

## Definición inicial

Clasificación de gramáticas formales según las restricciones de sus reglas: tipo 0, sensibles al contexto, libres de contexto y regulares.

## Intuición

Al imponer más restricciones, disminuye la capacidad expresiva, pero suele facilitarse el reconocimiento del lenguaje.

## Relación de inclusión

$$
\text{regulares}\subseteq\text{libres de contexto}\subseteq
\text{sensibles al contexto}\subseteq\text{irrestrictas}.
$$

## Relaciones

- Clasifica una: [[Gramática formal|Gramática formal]].
- Las gramáticas tipo 2 describen gran parte de la sintaxis de los lenguajes de programación.

## Procedencia

- Clase: [[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas y técnicas de programación]].
- Fuente: diapositivas 4–5.

## Para completar

- [ ] Asociar cada tipo con su modelo de cómputo.
- [ ] Añadir un lenguaje representativo de cada nivel.

