---
tipo: concepto
aliases:
  - Regla de fortalecimiento y debilitamiento
  - Hoare consequence rule
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica-de-hoare, inferencia]
---

# Regla de consecuencia de Hoare

## Definición

Regla que permite reemplazar la precondición de una terna por una condición más fuerte y su postcondición por una más débil.

## Intuición

Si un programa funciona para un conjunto de entradas, funciona para cualquier subconjunto. Si garantiza una salida precisa, también garantiza cualquier consecuencia menos exigente.

## Formulación

$$
\frac{P'\Rightarrow P\qquad\{P\}C\{Q\}\qquad Q\Rightarrow Q'}
{\{P'\}C\{Q'\}}.
$$

## Ejemplo mínimo

```text
y = 4 implica y != 0
{y != 0} x := 1/y {x = 1/y}
--------------------------------
{y = 4}  x := 1/y {x = 1/y}
```

También, de $max=b\Rightarrow max\ge b$, se pasa de la postcondición exacta a la más débil.

## Contraejemplo o límites

Las direcciones importan: debilitar la precondición o fortalecer la postcondición exige una demostración adicional y no se obtiene con esta regla.

## Regla mnemotécnica

- **Antes:** se permite pedir **más** al estado inicial: $P'\Rightarrow P$.
- **Después:** se permite prometer **menos**: $Q\Rightarrow Q'$.

En una prueba completa, estas implicaciones se convierten en [[Condición de verificación|condiciones de verificación]]. Véase [[Guía paso a paso - Lógica de Hoare#6. De programa anotado a condiciones de verificación|el procedimiento paso a paso]].

## Relaciones

- Se aplica a: [[Terna de Hoare|Terna de Hoare]].
- Usa: [[Fortaleza lógica de una aserción|Fortaleza lógica de una aserción]].
- Simplifica resultados de: [[Axioma de asignación de Hoare|Axioma de asignación de Hoare]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 16–19 (láminas 70–73).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 21–23.
