---
tipo: concepto
aliases:
  - Skolemization
  - Función de Skolem
  - Constante de Skolem
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-22 IA - logica de primer orden|Clase del 22 de septiembre]]"
  - Russell y Norvig, Artificial Intelligence: A Modern Approach, 4.ª ed., capítulo 9
tags:
  - concepto
  - inteligencia-artificial
  - logica-primer-orden
  - skolemizacion
---

# Skolemización

## Definición

La **skolemización** elimina cuantificadores existenciales de una fórmula de [[Lógica de primer orden|primer orden]] introduciendo símbolos nuevos que representan testigos de existencia.

- Si el existencial no depende de ningún universal en alcance, se usa una **constante de Skolem**.
- Si depende de variables universales $x_1,\dots,x_n$, se usa una **función de Skolem** $F(x_1,\dots,x_n)$.

## Ejemplos

Sin dependencia universal:

$$\exists y\,Gato(y)\quad\leadsto\quad Gato(c).$$

Con dependencia de $x$:

$$\forall x\,\exists y\,Ama(y,x)\quad\leadsto\quad\forall x\,Ama(F(x),x).$$

$F(x)$ expresa «algún objeto que ama a $x$». No es necesario conocer cuál objeto es, pero puede variar con $x$.

```mermaid
flowchart LR
    X[∀x: x] --> W[∃y: el testigo puede depender de x]
    W --> FX[F(x)]
    FX --> R[R(x,F(x))]
    C[∃y: no hay universales en alcance] --> K[constante c]
    K --> S[S(c)]
```

La aridad de la función de Skolem refleja las variables universales que están en alcance cuando aparece el existencial. Los universales no relacionados no se añaden como argumentos.

## Propiedad clave

La fórmula original y su forma skolemizada son **equisatisfactibles**: una tiene modelo si y solo si la otra tiene un modelo apropiado para el vocabulario ampliado. No son, en general, fórmulas lógicamente equivalentes porque la versión skolemizada contiene símbolos nuevos.

Esta propiedad es suficiente para preparar una [[Forma normal conjuntiva en lógica de primer orden|FNC de primer orden]] y buscar una contradicción mediante [[Resolución de primer orden|resolución]].

## Error frecuente

En $\forall x\,\exists y\,R(x,y)$, sustituir $y$ por una sola constante $c$ afirmaría que el mismo objeto sirve para todos los $x$. La fórmula original solo exige que cada $x$ tenga algún testigo, por lo que corresponde $R(x,F(x))$.

## Procedencia y referencias

- Clase: [[2026-09-22 IA - logica de primer orden|Inferencia en lógica de primer orden]], diapositivas 4–7.
- Russell, S. J. y Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4.ª ed.), §9.5; [sitio oficial](https://aima.cs.berkeley.edu/).
- Enderton, H. B. (2001). *A Mathematical Introduction to Logic* (2.ª ed.), capítulo 2. Academic Press. Presenta formas prenexas, testigos y transformación a formas normales.
