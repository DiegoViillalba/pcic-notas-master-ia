---
tipo: concepto
aliases:
  - Arc consistency
  - Consistencia de arco
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html"
  - "https://www.cs.ubc.ca/~mack/Publications/AI77.pdf"
tags: [concepto, inteligencia-artificial, csp, propagacion-de-restricciones]
---

# Consistencia de arcos

## Idea esencial

Un valor de una variable debe tener al menos un valor compatible en la variable situada al otro extremo de la restricción. Ese valor compatible se llama **soporte**.

> [!note] Prerrequisito mínimo
> En un CSP binario, los nodos representan variables, sus dominios contienen valores posibles y cada arista representa una restricción entre dos variables.

## De una arista a dos arcos

Una restricción binaria entre $X_i$ y $X_j$ se examina en dos direcciones:

$$
X_i\to X_j
\qquad\text{y}\qquad
X_j\to X_i.
$$

El arco dirigido $X_i\to X_j$ es consistente si cada $x\in D(X_i)$ tiene al menos un soporte $y\in D(X_j)$ que satisface la restricción:

$$
\forall x\in D(X_i),\ \exists y\in D(X_j)
\text{ tal que } C_{ij}(x,y).
$$

La cuantificación explica la asimetría: se revisan **todos** los valores del dominio situado en la cola del arco, buscando **algún** soporte en la cabeza. Por eso $X_i\to X_j$ puede ser consistente aunque $X_j\to X_i$ no lo sea.

## Ejemplo mínimo

Sean

$$
D(X)=\{1,2,3\},\qquad D(Y)=\{2\},\qquad X<Y.
$$

Al revisar $X\to Y$:

- $x=1$ tiene soporte $y=2$, pues $1<2$;
- $x=2$ no tiene soporte, porque $2<2$ es falso;
- $x=3$ tampoco tiene soporte.

Se eliminan $2$ y $3$ de $D(X)$, de modo que $D(X)=\{1\}$. Al revisar el arco inverso $Y\to X$, el valor $y=2$ sí tiene como soporte $x=1$ para la relación equivalente $X<Y$.

## Operación `REVISAR`

La consistencia de un arco se logra eliminando del dominio de su variable de origen —la cola del arco— los valores sin soporte:

```text
REVISAR(Xi, Xj):
    cambió ← falso
    para cada x en D(Xi):
        si no existe y en D(Xj) que satisfaga Cij(x, y):
            eliminar x de D(Xi)
            cambió ← verdadero
    devolver cambió
```

Esta operación no inventa asignaciones ni elimina soluciones: un valor sin soporte no puede aparecer en ninguna solución que respete esa restricción.

## Visualización: primero el soporte

Empieza con $X\to Y$ y pregunta para cada valor de $X$: «¿encuentro al menos un soporte en $Y$?». Después observa el arco inverso. Solo al final presta atención a la cola, que pertenece al [[Algoritmo AC-3|algoritmo AC-3]].

<iframe src="csp-consistencia-arcos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## Qué garantiza y qué no

- Si un dominio queda vacío, el CSP no tiene solución bajo la asignación parcial actual.
- Si todos los dominios quedan unitarios, se ha determinado una asignación completa; todavía debe verificarse que las restricciones representadas sean las correctas.
- Si todos los arcos son consistentes y quedan dominios con varios valores, normalmente todavía hace falta búsqueda.
- Consistencia local no implica consistencia global.

### Contraejemplo: triángulo con dos colores

Tres variables $A,B,C$ forman un triángulo, cada una con dominio $\{rojo,azul\}$, y cada arista exige colores diferentes. Cada valor tiene soporte en cada vecino, por lo que todos los arcos son consistentes. Sin embargo, el triángulo no puede colorearse con solo dos colores. La consistencia de arcos no detecta esta incompatibilidad global.

## De lo local a lo más fuerte

La consistencia de arcos corresponde a **2-consistencia**. La consistencia de caminos examina ternas de variables y equivale a una forma de 3-consistencia en redes binarias. Las nociones más fuertes pueden podar más, pero requieren más tiempo y memoria.

## Relaciones

- [[Forward checking|Forward checking]] establece consistencia únicamente desde la variable recién asignada hacia sus vecinas futuras.
- [[Algoritmo AC-3|AC-3]] aplica `REVISAR` repetidamente hasta que todos los arcos sean consistentes o aparezca un dominio vacío.
- La reducción de dominios alimenta a [[Heurística MRV|MRV]].
- Es una forma de [[Poda del espacio de búsqueda|poda segura]].

## Referencias

- Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], 4.ª ed., sección 5.2.2, pp. 170–171.
- UC Berkeley CS 188, [«Filtering»](https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html), sección 2.3.
- Alan K. Mackworth, [«Consistency in Networks of Relations»](https://www.cs.ubc.ca/~mack/Publications/AI77.pdf), *Artificial Intelligence*, 8(1), 1977, pp. 99–118.
- [[AI 5 Problemas de satisfacción de restricciones.pdf|Diapositivas: problemas de satisfacción de restricciones]].
