---
tipo: concepto
aliases:
  - Goal test
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Prueba de meta

## Definición

Predicado que determina si un estado satisface el objetivo de un problema de búsqueda.

## Formulación

$$
\operatorname{Meta}(s)\in\{\mathrm{verdadero},\mathrm{falso}\}.
$$

## Ejemplo mínimo

En el problema de viajar por Rumania, la prueba pregunta: “¿el estado actual es Bucarest?”.

## Límites

Reconocer una meta no indica cómo alcanzarla ni garantiza que el plan encontrado sea el de menor costo.

## Relaciones

- Forma parte de la: [[Formulación de un problema de búsqueda|Formulación de un problema de búsqueda]].
- Identifica soluciones dentro de un: [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 10 y 17–18.
