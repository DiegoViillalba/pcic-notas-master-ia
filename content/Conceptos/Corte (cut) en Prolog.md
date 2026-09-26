---
tipo: concepto
aliases:
  - Cut en Prolog
  - "!/0"
área: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]]"
tags: [concepto, programacion, prolog, backtracking, programacion-logica]
---

# Corte (cut, `!`) en Prolog

## Definición

El corte `!` es un predicado especial de Prolog que siempre tiene éxito la primera vez, pero que **elimina los puntos de elección** creados desde que se entró en la cláusula donde aparece: descarta tanto las cláusulas alternativas del mismo predicado que aún no se habían probado como los puntos de elección de las metas anteriores dentro de esa misma cláusula.

## Efecto operacional

~~~prolog
factorial( 0, 1 ) :- !.
factorial( N, F ) :- N > 0, N1 is N - 1, factorial( N1, F1 ), F is N * F1.
~~~

Al resolver `factorial(0, F)`:

- **Sin** `!`: Prolog encuentra `F = 1`; si más adelante el programa retrocede hasta aquí, todavía intentaría la segunda cláusula (que fallaría por `0 > 0`).
- **Con** `!`: en cuanto se cruza el corte, la segunda cláusula queda descartada para esa llamada, sin importar qué pase después. Prolog nunca vuelve a intentarla.

## Corte verde vs. corte rojo

- **Corte verde:** solo mejora la eficiencia (evita explorar una rama que de todos modos fallaría), sin cambiar el conjunto de soluciones. El ejemplo de `factorial` de arriba es un corte verde.
- **Corte rojo:** si se quita el corte, el programa produce soluciones **distintas** (más de las que se querían). Cambia el significado lógico del predicado, no solo su eficiencia.

## Relaciones

- Modifica el comportamiento de: [[Unificación|unificación]] y enumeración de soluciones alternativas.
- Se usa junto con: [[Prolog|Prolog]], cláusulas con [[Cláusula de Horn|cláusulas de Horn]].

## Procedencia

- Clase: [[2026-09-10 ProgAv - Hechos, unificación, backtracking y corte en Prolog|Hechos, unificación, backtracking y corte en Prolog]].
- Fuente: proyecto `EjemplosProlog.pl` (predicados `mayor`, `max`, `factorial`, `fib`, `potencia`).
