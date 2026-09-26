---
tipo: concepto
aliases:
  - Circuit SAT
  - Circuit satisfiability
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, complejidad, satisfacibilidad]
---

# Satisfacibilidad de circuitos

## Definición

Problema de decisión que pregunta si existe una asignación booleana a las entradas de un circuito que haga verdadera su salida.

## Formulación

Dado un circuito booleano $C:\{0,1\}^n\to\{0,1\}$, se pregunta:

$$
\exists e\in\{0,1\}^n\text{ tal que }C(e)=1\;?
$$

## Ejemplo mínimo

Para $C(x_1,x_2)=x_1\land x_2$, la entrada $(1,1)$ hace verdadera la salida; por tanto, el circuito es satisfacible.

## Algoritmo exhaustivo

Probar las $2^n$ asignaciones posibles es correcto, pero requiere tiempo exponencial en el peor caso.

## Contraejemplo o límites

Que el algoritmo exhaustivo sea exponencial no demuestra que ningún algoritmo polinomial exista. Precisamente se desconoce si este problema puede resolverse en tiempo polinomial.

## Relaciones

- Es central en: [[P versus NP|P versus NP]].
- Ilustra la diferencia entre: [[Validez de un algoritmo|validez]] y [[Eficiencia algorítmica|eficiencia]].
- Su solución propuesta usa: búsqueda exhaustiva.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 18–19.
