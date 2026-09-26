---
tipo: concepto
aliases:
  - Aseveración de programa
  - Assertion
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica, verificacion-formal]
---

# Aserción de programa

## Definición

Predicado lógico sobre las variables de un programa que puede ser verdadero o falso en un estado determinado.

## Intuición

Una aserción selecciona estados: $x>0$ admite exactamente aquellos donde `x` es positivo. Antes de un código funciona como precondición; después, como postcondición.

## Formulación

Si $\Sigma$ es el conjunto de estados, una aserción puede verse como:

$$
P:\Sigma\to\{\text{verdadero},\text{falso}\}.
$$

La aserción $\top$ —escrita `{ }` en las diapositivas— es verdadera para todo estado; $\bot$ no es satisfecha por ninguno.

## Ejemplo mínimo

```python
P = lambda estado: estado["x"] >= 0
Q = lambda estado: estado["r"] >= 0 and estado["r"]**2 == estado["x"]
```

## Contraejemplo o límites

`{ }` no representa una condición falsa ni un conjunto de estados sin elementos: en la notación de las diapositivas representa $\top$, ausencia de restricciones.

## Relaciones

- Es satisfecha por: [[Estado de programa|Estado de programa]].
- Aparece en: [[Terna de Hoare|Terna de Hoare]].
- Se compara mediante: [[Fortaleza lógica de una aserción|Fortaleza lógica de una aserción]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 3–4 y 8–9 (láminas 57–58 y 62–63).

