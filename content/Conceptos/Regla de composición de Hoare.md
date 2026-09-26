---
tipo: concepto
aliases:
  - Regla de concatenación de Hoare
  - Regla de secuencia de Hoare
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]]"
tags: [concepto, programacion, logica-de-hoare, verificacion-formal]
---

# Regla de composición de Hoare

## Definición

Regla que demuestra una secuencia \(C_1;C_2\) conectando la postcondición del primer fragmento con la precondición del segundo:

$$
\frac{\{P\}C_1\{R\}\qquad\{R\}C_2\{Q\}}
{\{P\}C_1;C_2\{Q\}}.
$$

\(R\) es la aserción intermedia.

## Intuición

El estado final de \(C_1\) es el estado inicial de \(C_2\). Si \(C_1\) garantiza \(R\) y \(C_2\) funciona siempre que \(R\) sea cierta, la secuencia completa transforma \(P\) en \(Q\).

## Ejemplo mínimo

$$
\{\top\}\ c:=a+b\ \{c=a+b\},
$$

$$
\{c=a+b\}\ c:=c/2\ \left\{c=\frac{a+b}{2}\right\}.
$$

Por composición:

$$
\{\top\}\ c:=a+b;c:=c/2\ \left\{c=\frac{a+b}{2}\right\}.
$$

## Contraejemplo o límites

No se pueden concatenar dos ternas si la postcondición de la primera no garantiza la precondición de la segunda. En ese caso se ajustan las aserciones mediante la regla de consecuencia o se busca otra condición intermedia.

## Ejercicio rápido

Para `x:=x+1; y:=2*x` y meta $y\ge10$, la condición intermedia antes de la última asignación es $x\ge5$ y la precondición inicial es $x\ge4$. El desarrollo completo está en [[Guía paso a paso - Lógica de Hoare#3. Secuencias una condición intermedia une dos pruebas|Secuencias paso a paso]].

## Relaciones

- Compone: [[Terna de Hoare|ternas de Hoare]].
- Las condiciones intermedias suelen obtenerse con: [[Precondición más débil|precondiciones más débiles]].
- Para asignaciones utiliza: [[Axioma de asignación de Hoare|axioma de asignación]].
- Ajusta condiciones con: [[Regla de consecuencia de Hoare|regla de consecuencia]].

## Procedencia

- Clase: [[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]].
- Fuente: *Programación Avanzada Notas 5*, diapositivas 3–8 (láminas 84–89).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 24–25.
