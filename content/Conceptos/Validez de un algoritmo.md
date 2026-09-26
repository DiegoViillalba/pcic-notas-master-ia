---
tipo: concepto
aliases:
  - Corrección de un algoritmo
  - Algorithm correctness
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 ADA - Introducción al curso|Introducción al curso]]"
tags: [concepto, algoritmos, correccion]
---

# Validez de un algoritmo

## Definición

Propiedad por la que el algoritmo calcula una salida correcta para cada entrada permitida por la especificación del problema.

## Intuición

La validez conecta los pasos ejecutados con lo que el problema exige, no solo con lo que el programa devuelve en algunos ejemplos.

## Formulación

Si $R(x,y)$ expresa que $y$ es una solución válida para $x$, entonces:

$$
\forall x\in I,\quad R(x,A(x)).
$$

## Ejemplo mínimo

La búsqueda lineal es válida porque revisa todas las posiciones: si devuelve $c$, entonces $A[c]=x$; si devuelve `NULL`, $x$ no aparece en el arreglo.

## Contraejemplo o límites

Probar unos cuantos casos no demuestra validez para todas las entradas. Además, un algoritmo puede ser válido pero imprácticamente lento.

## Relaciones

- Junto con: [[Terminación de un algoritmo|Terminación de un algoritmo]].
- Contrasta con: [[Eficiencia algorítmica|Eficiencia algorítmica]].
- Se demuestra mediante: invariantes, inducción u otros argumentos de corrección.

## Procedencia

- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción al curso]]
- Fuente: presentación introductoria, diapositivas 11–13.
