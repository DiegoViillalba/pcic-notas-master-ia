---
tipo: concepto
aliases:
  - Comprobación hacia adelante
  - Revisión hacia adelante
  - Forward checking
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html"
tags: [concepto, inteligencia-artificial, csp, backtracking, propagacion-de-restricciones]
---

# Forward checking

## Definición

El **filtrado** en un CSP consiste en reducir por anticipado los dominios de las variables no asignadas. Su objetivo es eliminar valores que, según la asignación parcial disponible, inevitablemente conducirían a un retroceso posterior.

*Forward checking* es un método básico de filtrado: después de asignar $X_i=x$, revisa cada variable no asignada que comparte una restricción con $X_i$ y elimina de su dominio los valores incompatibles con $x$. Si algún dominio queda vacío, la asignación actual no puede extenderse hasta una solución y se aplica [[Backtracking|backtracking]] sin explorar más esa rama.

## Procedimiento

1. Asignar un valor $x$ a una variable $X_i$.
2. Localizar sus vecinas no asignadas en el grafo de restricciones.
3. Eliminar de cada dominio vecino los valores que violarían su restricción con $X_i=x$.
4. Si aparece un dominio vacío, declarar fallida la rama actual y retroceder.
5. Si todos conservan al menos un valor, continuar con la siguiente variable.

## Regla básica

Para cada variable vecina $Y$ todavía no asignada:

$$
D(Y)\leftarrow\{y\in D(Y):C_{XY}(x,y)\text{ se cumple}\}.
$$

La operación no elige una solución por sí misma: solo conserva las opciones que siguen siendo posibles después de la última decisión.

## Ejemplo mínimo: N-reinas

Se usa una variable por fila y cada dominio contiene columnas. Si se coloca una reina en la fila $0$, columna $1$, se eliminan de las filas posteriores la columna $1$ y las posiciones situadas en sus diagonales. Si una fila futura pierde todas sus columnas, se retrocede inmediatamente.

En el ejemplo de coloreado de mapas de CS 188 sucede lo mismo: después de fijar colores para regiones como $WA$ o $Q$, se reducen los dominios de sus regiones vecinas. El dominio registra únicamente los colores que siguen siendo compatibles con las decisiones ya tomadas.

## Visualización

El tablero muestra los dominios que sobreviven; el árbol registra las decisiones probadas, las ramas podadas y el punto exacto donde un dominio se vacía.

<iframe src="csp-forward-checking-n-reinas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!tip] Lectura rápida
> Una casilla descartada representa trabajo evitado. Un dominio vacío no significa que el problema completo sea insoluble: significa que la **rama actual** no puede completarse.

## Alcance y límite

*Forward checking* solo propaga desde la variable recién asignada hacia variables no asignadas adyacentes. Puede dejar sin detectar una incompatibilidad entre dos variables futuras. La [[Consistencia de arcos|consistencia de arcos]], normalmente implementada mediante [[Algoritmo AC-3|AC-3]], revisa también relaciones entre variables todavía no asignadas y suele evitar más retrocesos, pero requiere más cómputo. Elegir entre ambos métodos implica balancear el costo de filtrar ahora contra el trabajo de búsqueda que podría evitarse después.

## Relaciones

- Especializa la [[Poda del espacio de búsqueda|poda]] dentro de un CSP.
- Se combina con [[Backtracking|backtracking]].
- Puede reducir los dominios antes de aplicar [[Heurística MRV|MRV]].
- Es una propagación más local que [[Algoritmo AC-3|AC-3]].
- El [[Problema de las ocho reinas|problema de las N-reinas]] permite verlo con claridad.

## Referencias

- UC Berkeley CS 188, [«Filtering»](https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html), sección 2.3 del libro en línea de introducción a IA.
- [[2026-08-27 IA - CSP-Backtracking|Apunte de clase: CSP y backtracking]], sección «Revisión hacia adelante».
- [[AI 5 Problemas de satisfacción de restricciones.pdf|Diapositivas: problemas de satisfacción de restricciones]].
- Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], capítulo sobre CSP.
