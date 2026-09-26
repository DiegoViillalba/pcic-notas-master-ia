---
tipo: concepto
aliases:
  - LPO
  - FOL
  - First-order logic
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-22 IA - logica de primer orden|Clase del 22 de septiembre]]"
  - Russell y Norvig, Artificial Intelligence: A Modern Approach, 4.ª ed., capítulos 8–9
tags:
  - concepto
  - inteligencia-artificial
  - logica-primer-orden
  - representacion-conocimiento
---

# Lógica de primer orden

## Definición

La **lógica de primer orden** extiende la [[Lógica proposicional|lógica proposicional]] para representar objetos, propiedades y relaciones. Su lenguaje incluye:

- **constantes**, como $Sócrates$;
- **variables**, como $x$;
- **funciones**, como $MadreDe(x)$;
- **predicados**, como $Humano(x)$ o $Ama(x,y)$;
- **cuantificadores** universal $\forall$ y existencial $\exists$.

Una interpretación fija un dominio de objetos y asigna significado a constantes, funciones y predicados. Una sentencia es consecuencia de una base $KB$ cuando es verdadera en todos los modelos de $KB$.

## Ejemplo mínimo

$$
\forall x\,[Humano(x)\to Mortal(x)],\qquad Humano(Sócrates).
$$

La primera sentencia expresa una regularidad sobre cualquier objeto del dominio; la segunda identifica un caso. Mediante [[Resolución de primer orden|resolución]] puede demostrarse $Mortal(Sócrates)$.

## Diferencia respecto de la lógica proposicional

Una proposición como $SocratesEsMortal$ es indivisible. En primer orden, $Mortal(Sócrates)$ conserva la estructura predicado–argumento, lo que permite expresar una sola regla para todos los humanos y aplicarla a objetos distintos mediante [[Unificación|unificación]].

## Límites

- La consecuencia lógica general de primer orden es **semidecidible**: si una sentencia es consecuencia puede existir una prueba finita, pero una búsqueda ingenua puede no terminar cuando no lo es.
- Los cuantificadores y el alcance de variables vuelven esencial renombrar variables y evitar capturas.
- Mayor expresividad suele implicar inferencia más costosa que en lógica proposicional.

## Relaciones

- Sus fórmulas se preparan para resolución mediante [[Forma normal conjuntiva en lógica de primer orden|FNC de primer orden]].
- Los existenciales se eliminan mediante [[Skolemización|skolemización]].
- Los términos se hacen coincidir mediante [[Unificación|unificación]].
- [[Resolución SLD|Prolog]] usa un fragmento restringido de este lenguaje.

## Procedencia y referencias

- Clase: [[2026-09-22 IA - logica de primer orden|Inferencia en lógica de primer orden]].
- Russell, S. J. y Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4.ª ed.), capítulos 8 y 9; [sitio oficial](https://aima.cs.berkeley.edu/).

