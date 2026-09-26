---
tipo: concepto
aliases:
  - Retroceso en Prolog
  - Enumeración de soluciones
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]]"
tags: [concepto, programacion, prolog, backtracking, programacion-logica]
---

# Backtracking en Prolog

## Definición

Cuando una consulta unifica con la cabeza de más de una cláusula, o con un hecho que deja variables libres, Prolog guarda un **punto de elección**. Al pedir más soluciones (`;` en la consola), Prolog retrocede hasta el último punto de elección no agotado y prueba la siguiente alternativa.

## Ejemplo mínimo

~~~prolog
gusta( maria, helado ).
gusta( maria, leer ).
gusta( maria, cine ).
~~~

~~~text
?- gusta( maria, X ).
X = helado ;
X = leer ;
X = cine.
~~~

Cada `;` fuerza a Prolog a deshacer la sustitución anterior y unificar `X` con el siguiente hecho que coincide con el patrón de la consulta.

## Relación con la unificación

El backtracking no es un mecanismo aparte de la [[Unificación|unificación]]: en cada alternativa se vuelve a intentar unificar la meta con la siguiente cláusula del programa. La diferencia con una sola llamada a unificación es que Prolog **recuerda dónde había otras opciones** y puede regresar a ellas.

## Por qué importa para el corte

El [[Corte (cut) en Prolog|corte]] existe precisamente para **desactivar** puntos de elección concretos cuando el programador sabe que las alternativas restantes son innecesarias o incorrectas.

## Relaciones

- Se apoya en: [[Unificación|unificación]].
- Se controla con: [[Corte (cut) en Prolog|corte (cut)]].
- Es la base operacional de: [[Resolución SLD|resolución SLD]] con múltiples cláusulas candidatas.

## Procedencia

- Clase: [[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]].
- Fuente: sesión de consola de `MariaGusta.pl` (documento *Unificación y Sustitución*).
