---
tipo: concepto
aliases:
  - Renombrado de variables
  - Estandarización de variables aparte
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-22 IA - logica de primer orden|Clase del 22 de septiembre]]"
  - Russell y Norvig, Artificial Intelligence: A Modern Approach, 4.ª ed., §9.5
tags:
  - concepto
  - inteligencia-artificial
  - logica-primer-orden
  - variables
  - resolucion
---

# Estandarización aparte de variables

## Definición

La **estandarización aparte** (standardizing apart) consiste en cambiar los nombres de las variables de una cláusula para que no coincidan con los de otra cláusula que se combinará con ella. Es una renominación de variables, no una sustitución de sus valores: las variables de cada cláusula conservan su cuantificación universal implícita.

Las variables ligadas dentro de una fórmula también pueden renombrarse si se evita capturar variables libres. Por ejemplo, $\forall x\,P(x)$ y $\forall z\,P(z)$ son variantes equivalentes.

## Por qué se necesita al resolver

Supónganse las cláusulas $P(x)$ y $\neg P(x)\vee Q(x)$. Aunque ambas usan el glifo $x$, inicialmente son variables independientes. Se renombran como $P(x)$ y $\neg P(y)\vee Q(y)$; al unificarse $P(x)$ con $P(y)$, la sustitución apropiada es $\{y/x\}$ y el resolvente es $Q(x)$.

```mermaid
flowchart LR
    A[Cláusula 1: P(x)] --> R[Renombrar aparte]
    B[Cláusula 2: ¬P(x) ∨ Q(x)] --> R
    R --> A2[P(x)]
    R --> B2[¬P(y) ∨ Q(y)]
    A2 --> U[Unificar P(x) con P(y)]
    B2 --> U
    U --> O[Resolvente: Q(x)]
```

El renombrado evita una unión accidental de variables solo porque comparten un nombre. La unificación posterior sí determina las igualdades necesarias entre los términos.

## Alcance y captura

El alcance de un cuantificador determina qué apariciones liga. Al renombrar, solo se cambian las apariciones ligadas por ese cuantificador; hay que elegir un nombre fresco que no cambie el alcance ni capture otra variable. Esta limpieza se hace antes de skolemizar y también cada vez que se seleccionan cláusulas para una resolución.

## Errores frecuentes

- Tratar el mismo nombre de variable en dos cláusulas como una identidad compartida.
- Cambiar una sola aparición ligada y alterar accidentalmente el alcance.
- Usar una variable fresca que ya aparece en la otra cláusula.
- Confundir renombrado aparte con unificación: el primero evita colisiones; la segunda identifica términos para inferir.

## Procedencia y referencias

- Clase: [[2026-09-22 IA - logica de primer orden|Inferencia en lógica de primer orden]], conversión a FNC y resolución, diapositivas 4–8. Se cita como material docente de referencia.
- Russell, S. J. y Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4.ª ed.), §9.5, «The resolution algorithm»; [sitio oficial del libro](https://aima.cs.berkeley.edu/).
- Enderton, H. B. (2001). *A Mathematical Introduction to Logic* (2.ª ed.), capítulos 2–3. Academic Press. Tratamiento formal de variables ligadas, sustitución y normalización lógica.
