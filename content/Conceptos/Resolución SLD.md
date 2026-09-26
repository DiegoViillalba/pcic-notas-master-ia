---
tipo: concepto
aliases:
  - SLD-resolution
  - Resolución lineal selectiva para cláusulas definidas
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-22 IA - logica de primer orden|Clase del 22 de septiembre]]"
  - "https://www.swi-prolog.org/pldoc/man?section=glossary"
  - "https://www.swi-prolog.org/pldoc/man?section=execquery"
tags:
  - concepto
  - inteligencia-artificial
  - prolog
  - resolucion-sld
  - clausulas-horn
---

# Resolución SLD

## Definición

La **resolución SLD** (*Selective Linear Definite-clause resolution*) es una estrategia de [[Resolución de primer orden|resolución de primer orden]] para programas formados por [[Cláusula de Horn|cláusulas definidas]]: cláusulas con exactamente un literal positivo. La consulta se representa como una cláusula objetivo (sin literal positivo).

En cada paso:

1. se selecciona una meta pendiente;
2. se elige un hecho o una regla cuya cabeza pueda [[Unificación|unificarse]] con la meta;
3. se aplica el unificador;
4. la meta se sustituye por las premisas de la regla;
5. el proceso termina con éxito cuando ya no quedan metas; si una rama falla, se pueden probar alternativas mediante retroceso.

```mermaid
flowchart TD
  Q["Meta: mortal(socrates)"] -->|unificar con cabeza| R["Regla: mortal(X) ← humano(X)"]
  R -->|θ = {X/socrates}| G["Nueva meta: humano(socrates)"]
  G -->|unificar| F["Hecho: humano(socrates)"]
  F --> E["Meta vacía: éxito"]
  G -. "si no hay cláusula aplicable" .-> B["Falla esta rama"]
  B -. "retroceso" .-> ALT["Probar alternativa"]
```

## Ejemplo en Prolog

```prolog
humano(socrates).
mortal(X) :- humano(X).

?- mortal(socrates).
```

La meta `mortal(socrates)` unifica con `mortal(X)` mediante `{X/socrates}` y se reemplaza por `humano(socrates)`. El hecho correspondiente cierra la prueba. Esta reducción dirigida por la consulta evita construir todas las consecuencias posibles del programa.

## Diferencia entre significado y ejecución

El significado declarativo de una regla indica qué relación es verdadera. La ejecución de [[Prolog|Prolog]] agrega una política convencional: selecciona metas de izquierda a derecha y explora cláusulas en orden, con búsqueda en profundidad y retroceso. Por eso el orden puede afectar rendimiento y terminación. La regla SLD abstracta permite distintas funciones de selección; la elección concreta de Prolog es una estrategia operacional.

## Límites

- Trabaja con cláusulas definidas, no con cláusulas arbitrarias de primer orden.
- La estrategia de búsqueda puede entrar en ciclos aunque exista otra rama con una solución.
- El uso operativo de negación en Prolog suele ser negación como fallo, que no debe confundirse sin más con la negación clásica.
- La terminación no está garantizada para todos los programas y consultas.

## Relaciones

- Es un caso importante de [[Lenguajes declarativos|programación declarativa]] y constituye el mecanismo de búsqueda central de [[Prolog|Prolog]].
- Opera sobre [[Cláusula de Horn|cláusulas definidas]], un subconjunto de las cláusulas de Horn.
- Depende de [[Unificación|unificación]] y retroceso.

## Procedencia y referencias

- Clase: [[2026-09-22 IA - logica de primer orden|Inferencia en lógica de primer orden]], diapositiva 16.
- SWI-Prolog, [glosario: SLD resolution](https://www.swi-prolog.org/pldoc/man?section=glossary) y [ejecución de consultas](https://www.swi-prolog.org/pldoc/man?section=execquery).
- Sterling, L. y Shapiro, E. *The Art of Prolog*, 2.ª ed., MIT Press, capítulo 3.
- [[Lenguajes declarativos|Lenguajes declarativos]].
