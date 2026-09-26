---
tipo: concepto
aliases:
  - AC-3
  - AC3
  - Arc Consistency Algorithm 3
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html"
  - "https://www.cs.ubc.ca/~mack/Publications/AI77.pdf"
tags: [concepto, inteligencia-artificial, csp, ac3, propagacion-de-restricciones]
---

# Algoritmo AC-3

## Idea esencial

AC-3 mantiene una cola de arcos pendientes. Revisa cada arco, elimina valores sin soporte y vuelve a revisar únicamente los arcos que podrían haberse vuelto inconsistentes a causa de esa eliminación.

> [!note] Antes de continuar
> Conviene dominar primero [[Consistencia de arcos|soporte, dirección y consistencia de un solo arco]]. AC-3 no introduce una definición nueva de soporte: organiza cuándo repetir esa revisión en toda la red.

## ¿Por qué no basta una sola pasada?

Supongamos que ya se revisó $X_k\to X_i$. Más tarde, otro arco elimina valores de $D(X_i)$. Algún valor de $X_k$ podría haber perdido precisamente su único soporte, así que el arco anterior debe reconsiderarse. La propagación continúa hasta alcanzar un punto fijo: una pasada completa ya no produciría cambios.

## Estructuras que utiliza

- **Dominios actuales:** se reducen de manera monótona; los valores eliminados no regresan durante una ejecución.
- **Cola $Q$:** contiene arcos cuya consistencia debe comprobarse.
- **`REVISAR(X_i,X_j)`:** elimina de $D(X_i)$ los valores que no tienen soporte en $D(X_j)$.

Una restricción binaria no dirigida produce dos arcos dirigidos. Inicialmente se insertan ambos en la cola.

## Algoritmo paso a paso

1. Introducir en $Q$ todos los arcos dirigidos del CSP.
2. Extraer un arco $(X_i,X_j)$.
3. Ejecutar `REVISAR(X_i,X_j)`.
4. Si $D(X_i)$ quedó vacío, devolver fallo.
5. Si $D(X_i)$ cambió, reinsertar cada arco $(X_k,X_i)$ de los otros vecinos de $X_i$.
6. Repetir hasta vaciar la cola.

```text
AC-3(csp):
    Q ← todos los arcos dirigidos del csp
    mientras Q no esté vacía:
        (Xi, Xj) ← extraer(Q)
        si REVISAR(Xi, Xj):
            si D(Xi) = ∅:
                devolver fallo
            para cada Xk vecino de Xi, Xk ≠ Xj:
                añadir (Xk, Xi) a Q
    devolver dominios consistentes por arcos
```

## Por qué se reinsertan arcos hacia $X_i$

`REVISAR(X_i,X_j)` solo puede reducir $D(X_i)$. Ese cambio no perjudica a $X_j$: los valores eliminados de $X_i$ eran precisamente los que no encontraban apoyo en $X_j$. En cambio, sí puede perjudicar a otro vecino $X_k$, porque alguno de sus valores quizá dependía de un valor de $X_i$ recién eliminado. Por eso se reinsertan los arcos $(X_k,X_i)$ y no todos los arcos de la red.

## Ejemplo mínimo

Con $D(X)=\{1,2,3\}$, $D(Y)=\{2\}$ y $X<Y$:

1. La cola comienza con $[X\to Y, Y\to X]$.
2. Revisar $X\to Y$ conserva $1$ y elimina $2,3$ de $D(X)$.
3. Revisar $Y\to X$ confirma que $2$ tiene soporte en $1$.
4. La cola queda vacía con $D(X)=\{1\}$ y $D(Y)=\{2\}$.

## Visualización: después, la propagación

Después del ejemplo de dos variables, la visualización añade una tercera: $X<Y<Z$ y $D(Z)=\{3\}$. Sigue cómo una reducción en $D(Y)$ obliga a reinsertar $X\to Y$ y cómo la información se propaga de derecha a izquierda hasta alcanzar dominios unitarios.

<iframe src="csp-ac3-propagacion.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!tip] Qué observar
> No memorices primero el orden exacto de la cola. Identifica la causa: si cambia el dominio situado en la **cabeza** de un arco ya revisado, algunos valores de su cola pueden haber perdido soporte y ese arco debe comprobarse otra vez.

## Visualización aplicada: coloreo de un mapa

Una vez entendido el mecanismo con la cadena de tres variables, este segundo recorrido lo aplica a un subproblema de coloreo. Cada región es una variable, los colores son su dominio y cada arista impone que las dos regiones tengan colores distintos. El ejemplo comienza con **SA = azul**; al avanzar, AC-3 examina un arco dirigido, elimina colores sin soporte y actualiza la cola cuando una reducción puede afectar a otros vecinos.

<iframe src="csp-ac3-mapa-australia.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!tip] Cómo leerla
> 1. Usa **Siguiente paso** y localiza la flecha naranja: indica el arco $X_i\to X_j$ que se está revisando.
> 2. Mira primero el dominio de $X_j$ y pregunta qué valores de $X_i$ todavía tienen algún color compatible allí.
> 3. Si desaparece un color de $X_i$, comprueba qué arcos dirigidos hacia $X_i$ regresan a la cola.
>
> El grafo contiene solo cuatro regiones y un conjunto reducido de adyacencias para aislar la mecánica de AC-3; no pretende reproducir todo el mapa australiano clásico.

## Resultados posibles

| Resultado | Interpretación |
|---|---|
| Algún dominio queda vacío | La rama actual es inconsistente; debe fallar o retroceder. |
| Todos los dominios quedan unitarios | La propagación determinó una asignación completa. |
| La cola se vacía y quedan dominios múltiples | El CSP es consistente por arcos, pero todavía puede requerir búsqueda. |

AC-3 conserva el conjunto de soluciones: solo elimina valores que no podrían satisfacer alguna restricción binaria con el dominio actual.

## Complejidad

Si $e$ es el número de arcos dirigidos y $d$ el tamaño máximo de un dominio, una cota clásica es

$$
O(ed^3).
$$

Cada revisión puede comparar hasta $d^2$ pares de valores y un arco puede volver a la cola un número acotado por las eliminaciones de dominio. Esta es una cota de peor caso; el ahorro real depende de cuánta búsqueda evite la propagación.

## Cuándo se ejecuta

- **Como preprocesamiento:** antes de buscar, para comenzar con dominios reducidos.
- **Durante la búsqueda:** después de una asignación. En *Maintaining Arc Consistency* (MAC), se inicia la cola con los arcos que llegan a la variable recién asignada y se propaga desde ahí.

AC-3 suele podar más que [[Forward checking|forward checking]], pero también realiza más trabajo por decisión.

## Errores comunes

- Tratar una arista como un solo arco y olvidar revisar la dirección inversa.
- Eliminar un valor porque no coincide con **todos** los valores vecinos; basta con que tenga **un** soporte.
- No reinsertar arcos después de reducir un dominio.
- Concluir que «cola vacía» significa «solución encontrada».
- Confundir AC-3, que es un algoritmo, con [[Consistencia de arcos|la propiedad que intenta imponer]].

## Referencias

- Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], 4.ª ed., sección 5.2.2, pp. 170–171.
- UC Berkeley CS 188, [«Filtering»](https://inst.eecs.berkeley.edu/~cs188/textbook/csp/filtering.html), sección 2.3.
- Alan K. Mackworth, [«Consistency in Networks of Relations»](https://www.cs.ubc.ca/~mack/Publications/AI77.pdf), *Artificial Intelligence*, 8(1), 1977, pp. 99–118. El artículo introduce AC-3 como la tercera variante de sus algoritmos de consistencia de arcos.
- [[AI 5 Problemas de satisfacción de restricciones.pdf|Diapositivas: problemas de satisfacción de restricciones]].
