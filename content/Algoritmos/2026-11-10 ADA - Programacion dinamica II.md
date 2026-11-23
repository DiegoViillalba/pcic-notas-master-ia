---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-11-10"
unidad: Programación dinámica I (continuación)
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Programación dinámica
  - Mínimos cuadrados
  - Mínimos cuadrados segmentados
  - Elección múltiple
  - Problema de la mochila
  - Programación dinámica en dos variables
  - Tiempo pseudopolinomial
  - Cambio de monedas
referencias:
  - "06DynamicProgrammingI.pdf, diapositivas 24–41 (Kevin Wayne; Kleinberg y Tardos, secciones 6.3 y 6.4)"
tags:
  - clase
  - algoritmos
  - programacion-dinamica
  - mochila
---

# Clase 20 · Programación dinámica II: mínimos cuadrados segmentados, mochila y cambio de monedas

![[06DynamicProgrammingI.pdf]]
> [!info] Alcance y procedencia
> Este apunte desarrolla **las diapositivas 24–41** de [[06DynamicProgrammingI.pdf|06DynamicProgrammingI.pdf]], hasta donde llegó la clase. Continúa [[2026-11-03 ADA - Programacion dinamica|Clase 19 · Programación dinámica I]] (diapositivas 1–23). Cada sección abre con sus diapositivas en un bloque plegable. La instancia de la mochila, su tabla y las denominaciones del cambio de monedas son de las diapositivas; la tabla de errores $e_{ij}$ de la sección 4, el ejemplo de monedas $\{1,4,6\}$ y los puntos del interactivo de rectas son **ejemplos didácticos añadidos**.

## Pregunta central

¿Qué cambia en la receta de PD cuando la decisión ya no es binaria (incluir o excluir), o cuando un solo índice no basta para describir el subproblema?

> [!summary] Idea de la clase
> Tres problemas, tres variaciones sobre la misma receta *estado → elección → ecuación de Bellman → orden de llenado*:
> - **Mínimos cuadrados segmentados:** elección **múltiple**. Para los primeros $j$ puntos probamos todos los inicios posibles $i$ del último segmento: $OPT(j)=\min_{i}\{e_{ij}+c+OPT(i-1)\}$. Tiempo $O(n^3)$, mejorable a $O(n^2)$.
> - **Mochila 0/1:** el estado necesita **dos variables**, objetos disponibles y capacidad restante: $OPT(i,w)$. Tabla de $\Theta(nW)$ casillas; ningún voraz funciona. El tiempo $\Theta(nW)$ es **pseudopolinomial**, no polinomial.
> - **Cambio de monedas:** una variable (el monto) y elección múltiple (la última moneda), porque las monedas se pueden repetir. $O(nV)$, y corrige el fallo del cajero voraz.

## 1. Mínimos cuadrados: una sola recta (diapositivas 24–25)

> [!example]+ Diapositivas 24–25
> ![[06DP-slide-24.jpg]]
>
> ![[06DP-slide-25.jpg]]

La diapositiva 24 abre la sección 6.3 del libro. El punto de partida es el problema clásico de estadística: dados $n$ puntos $(x_1,y_1),\ldots,(x_n,y_n)$, encontrar la recta $y=ax+b$ que minimiza la **suma de errores cuadráticos**

$$
SSE=\sum_{i=1}^{n}(y_i-ax_i-b)^2 .
$$

Cada término es el cuadrado de la distancia **vertical** entre el punto y la recta (el segmento rojo de la figura). Derivando respecto a $a$ y $b$ e igualando a cero se obtiene la solución cerrada

$$
a=\frac{n\sum_i x_iy_i-\left(\sum_i x_i\right)\left(\sum_i y_i\right)}{n\sum_i x_i^2-\left(\sum_i x_i\right)^2},
\qquad
b=\frac{\sum_i y_i-a\sum_i x_i}{n}.
$$

Para el algoritmo lo que importa es: **dado un conjunto de puntos, su mejor recta y su error se calculan con unas cuantas sumas**, en tiempo $O(\text{número de puntos})$. Aquí no hay PD todavía; es la subrutina que usaremos.

## 2. Varios segmentos: precisión contra parsimonia (diapositivas 26–27)

> [!example]+ Diapositivas 26–27
> ![[06DP-slide-26.jpg]]
>
> ![[06DP-slide-27.jpg]]

Si los puntos siguen aproximadamente **varios tramos rectos** (la figura tiene tres), una sola recta ajusta mal. Con $x_1<x_2<\cdots<x_n$ queremos partir la secuencia en bloques **consecutivos** y ajustar una recta a cada bloque.

¿Qué función $f$ minimizar? Si sólo minimizamos el error, la respuesta trivial es usar muchísimas rectas: con un segmento por cada uno o dos puntos el error es $0$ (sobreajuste). Hay que equilibrar:

- **precisión** (*goodness of fit*): error pequeño;
- **parsimonia**: pocas rectas.

La diapositiva 27 fija el objetivo

$$
f=E+c\,L,\qquad c>0,
$$

donde $E$ es la suma de los $SSE$ de cada segmento y $L$ el número de rectas. La constante $c$ es el «precio» de cada recta adicional: con $c$ grande preferimos pocas rectas; con $c$ pequeño, muchas. Una recta extra vale la pena sólo si reduce el error en más de $c$.

## 3. Elección múltiple y ecuación de Bellman (diapositiva 28)

> [!example]+ Diapositiva 28
> ![[06DP-slide-28.jpg]]

**Notación.**

- $OPT(j)$: costo mínimo $f$ para los puntos $p_1,\ldots,p_j$.
- $e_{ij}$: error $SSE$ de la mejor recta para los puntos $p_i,\ldots,p_j$.

**¿Qué decisión hacemos?** Miramos el **último segmento** de una solución óptima para $p_1..p_j$. Termina en $p_j$ y empieza en algún $p_i$ con $1\le i\le j$. Como no sabemos cuál, **probamos todos los $i$**. A diferencia de los intervalos con pesos (dos opciones), aquí hay $j$ opciones: es una **elección múltiple** (*multiway choice*).

Si el último segmento es $p_i..p_j$, el costo es:

$$
\underbrace{e_{ij}}_{\text{error del último tramo}}+\underbrace{c}_{\text{su recta}}+\underbrace{OPT(i-1)}_{\text{resto óptimo}} .
$$

**Subestructura óptima (argumento de intercambio).** Si la parte $p_1..p_{i-1}$ de una solución óptima no fuese óptima para esos puntos, la cambiaríamos por una mejor sin tocar el último segmento y el costo total bajaría: contradicción. Por eso aparece $OPT(i-1)$.

$$
OPT(j)=\begin{cases}
0, & j=0,\\[1mm]
\displaystyle\min_{1\le i\le j}\bigl\{\,e_{ij}+c+OPT(i-1)\,\bigr\}, & j>0.
\end{cases}
$$

| | Intervalos con pesos | Mínimos cuadrados segmentados |
|:--|:--|:--|
| Estado | prefijo de trabajos $1..j$ | prefijo de puntos $1..j$ |
| Pregunta | ¿está $j$ en la solución? | ¿dónde empieza el último segmento? |
| Opciones | 2 | $j$ |
| Costo de una casilla | $O(1)$ | $O(j)$ |

## 4. Algoritmo, análisis y ejemplo a mano (diapositivas 29–30)

> [!example]+ Diapositivas 29–30
> ![[06DP-slide-29.jpg]]
>
> ![[06DP-slide-30.jpg]]

~~~text
SEGMENTED-LEAST-SQUARES(n, p1..pn, c):
    para j ← 1 hasta n:
        para i ← 1 hasta j:
            calcular e[i][j]            # SSE de la mejor recta para p_i..p_j
    M[0] ← 0
    para j ← 1 hasta n:
        M[j] ← min_{1 ≤ i ≤ j} { e[i][j] + c + M[i − 1] }
        A[j] ← el i que alcanza el mínimo          # para reconstruir (añadido)
    devolver M[n]
~~~

El orden es válido porque $M[i-1]$ con $i\le j$ ya está calculado («*previously computed value*»).

**Reconstrucción** *(no aparece en la lámina, pero es igual que en intervalos)*: guardamos en $A[j]$ el índice $i$ ganador. Desde $j=n$, el último segmento es $p_{A[n]}..p_n$; luego saltamos a $j=A[n]-1$ y repetimos hasta $j=0$.

**Teorema (Bellman, 1961).** El algoritmo resuelve el problema en **$O(n^3)$ tiempo y $O(n^2)$ espacio**.

- Hay $O(n^2)$ pares $(i,j)$ y cada $e_{ij}$ cuesta $O(n)$ con las fórmulas de $a_{ij},b_{ij}$ (donde «$n$» en la fórmula es el número de puntos del tramo, $j-i+1$). Éste es el **cuello de botella**: $O(n^3)$.
- Llenar $M$ cuesta $\sum_j O(j)=O(n^2)$.
- Guardar todos los $e_{ij}$ ocupa $O(n^2)$.

**Mejora a $O(n^2)$.** Precalculando las sumas acumuladas $\sum_{k\le i}x_k$, $\sum_{k\le i}y_k$, $\sum_{k\le i}x_k^2$, $\sum_{k\le i}x_ky_k$, cada suma sobre $p_i..p_j$ es una resta de prefijos y $e_{ij}$ sale en $O(1)$. Es el mismo truco de sumas acumuladas del subarreglo máximo (diapositiva 20).

### Ejemplo didáctico con cuatro puntos

Suponemos ya calculados los errores (dos puntos siempre caben exactos en una recta, así que $e_{ii}=e_{i,i+1}=0$):

| $e_{ij}$ | $j=1$ | $j=2$ | $j=3$ | $j=4$ |
|:--|--:|--:|--:|--:|
| $i=1$ | 0 | 0 | 0.5 | 4.0 |
| $i=2$ | | 0 | 0 | 0.2 |
| $i=3$ | | | 0 | 0 |
| $i=4$ | | | | 0 |

Con $c=1$:

| $j$ | candidatos $e_{ij}+c+M[i-1]$ para $i=1,\ldots,j$ | $M[j]$ | $A[j]$ |
|--:|:--|--:|--:|
| 0 | — | 0 | — |
| 1 | $0+1+0=1$ | 1 | 1 |
| 2 | $0+1+0=\mathbf{1}$; $0+1+1=2$ | 1 | 1 |
| 3 | $0.5+1+0=\mathbf{1.5}$; $0+1+1=2$; $0+1+1=2$ | 1.5 | 1 |
| 4 | $4+1+0=5$; $0.2+1+1=2.2$; $0+1+1=\mathbf{2}$; $0+1+1.5=2.5$ | 2 | 3 |

Reconstrucción: $A[4]=3$ ⇒ último tramo $p_3..p_4$; saltamos a $j=2$, $A[2]=1$ ⇒ tramo $p_1..p_2$. Dos rectas, $E=0$, $f=0+1\cdot2=2$.

Con $c=5$ la misma tabla da $M[4]=\min\{9,\;10.2,\;10,\;10.5\}=9$: conviene **una sola recta** aunque su error sea $4$, porque una segunda recta cuesta $5$. Así se ve el papel de $c$.

**Explora la penalización $c$.** Mueve el control: con $c$ muy pequeño la PD parte los datos en muchos tramos; con $c$ grande usa una sola recta. Debajo aparece la tabla $M[j]$ con los índices $A[j]$ que siguen la reconstrucción.

<iframe src="pd-minimos-cuadrados-segmentados.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 5. El problema de la mochila (diapositivas 31–32)

> [!example]+ Diapositivas 31–32
> ![[06DP-slide-31.jpg]]
>
> ![[06DP-slide-32.jpg]]

Hay $n$ objetos; el objeto $i$ vale $v_i>0$ y pesa $w_i>0$. La mochila soporta a lo más $W$. Queremos un **subconjunto** de objetos (cada uno se toma **0 o 1 vez**) de peso total $\le W$ y valor total máximo. **Supuesto:** valores y pesos son enteros.

Instancia de la lámina, con $W=11$:

| $i$ | $v_i$ | $w_i$ | $v_i/w_i$ |
|--:|--:|--:|--:|
| 1 | \$1 | 1 kg | 1.00 |
| 2 | \$6 | 2 kg | 3.00 |
| 3 | \$18 | 5 kg | 3.60 |
| 4 | \$22 | 6 kg | 3.67 |
| 5 | \$28 | 7 kg | 4.00 |

- $\{1,2,5\}$: valor \$35, peso 10.
- $\{3,4\}$: valor **\$40**, peso 11. Es el óptimo.

## 6. Quiz 2: ¿algún voraz resuelve la mochila? (diapositiva 33)

> [!example]+ Diapositiva 33
> ![[06DP-slide-33.jpg]]

**Respuesta: D, ninguno.** En la propia instancia, agregando objetos en el orden indicado mientras quepan:

| Regla voraz | Orden de prueba | Toma | Valor |
|:--|:--|:--|--:|
| A. Mayor valor | 5, 4, 3, 2, 1 | 5 (7 kg), 4 y 3 no caben, 2 (9 kg), 1 (10 kg) | \$35 |
| B. Menor peso | 1, 2, 3, 4, 5 | 1, 2, 3 (8 kg), 4 y 5 no caben | \$25 |
| C. Mayor $v_i/w_i$ | 5, 4, 3, 2, 1 | igual que A | \$35 |
| Óptimo | — | 3 y 4 (11 kg) | **\$40** |

La razón $v_i/w_i$ sí es óptima para la mochila **fraccionaria** (cuando se puede tomar parte de un objeto), pero en la versión 0/1 el espacio que sobra no se puede «rellenar a medias»: tomar el objeto 5 deja 4 kg en los que sólo caben objetos baratos. Es el mismo fenómeno que el contraejemplo 1–999–1 de los intervalos con pesos.

## 7. Quiz 3: ¿qué subproblemas? (diapositiva 34)

> [!example]+ Diapositiva 34
> ![[06DP-slide-34.jpg]]

**Respuesta: C**, $OPT(i,w)$ con objetos $1..i$ y límite $w$.

- **B, $OPT(i)$ sólo con los objetos $1..i$:** si decidimos tomar el objeto $i$, necesitamos el mejor valor de $1..i-1$ **con la capacidad que queda**, $W-w_i$. $OPT(i-1)$ se calculó con capacidad $W$ y no sirve. Es la diferencia con los intervalos: allí, incluir $j$ sólo recortaba el **prefijo** ($p(j)$); aquí recorta también un **recurso**.
- **A, $OPT(w)$ sólo con la capacidad:** no recuerda qué objetos ya se usaron, así que la recurrencia podría tomar el mismo objeto varias veces. Eso resuelve otra variante (mochila **sin límite de copias**), y justo por eso el cambio de monedas de la sección 11 sí funciona con una variable.

> [!tip] Cómo descubrir el estado
> Escribe la elección («¿tomo el objeto $i$?») y pregunta: después de decidir, **¿qué necesito saber para resolver lo que queda?** Aquí: qué objetos siguen disponibles ($1..i-1$) y cuánto espacio queda ($w$ o $w-w_i$). Esas son las dos coordenadas.

## 8. Dos variables y ecuación de Bellman (diapositiva 35)

> [!example]+ Diapositiva 35
> ![[06DP-slide-35.jpg]]

**Definición.** $OPT(i,w)$ = valor óptimo usando sólo los objetos $1,\ldots,i$ con límite de peso $w$. **Objetivo:** $OPT(n,W)$.

- **Caso 1: la solución no toma $i$.** Entonces es la mejor de $\{1..i-1\}$ con límite $w$: $OPT(i-1,w)$. Este caso es **obligatorio** si $w_i>w$ (no cabe).
- **Caso 2: la solución toma $i$.** Gana $v_i$, el nuevo límite es $w-w_i$, y el resto debe ser óptimo para $\{1..i-1\}$ con ese límite (si no, lo cambiaríamos por algo mejor): $v_i+OPT(i-1,w-w_i)$.

$$
OPT(i,w)=\begin{cases}
0, & i=0,\\[1mm]
OPT(i-1,w), & w_i>w,\\[1mm]
\max\bigl\{\,OPT(i-1,w),\;v_i+OPT(i-1,w-w_i)\,\bigr\}, & \text{en otro caso.}
\end{cases}
$$

Es la misma elección binaria de los intervalos, pero el «salto» del caso 2 se mueve en **las dos coordenadas**: una fila arriba y $w_i$ columnas a la izquierda.

## 9. Tabla de abajo hacia arriba y demostración (diapositivas 36–37)

> [!example]+ Diapositivas 36–37
> ![[06DP-slide-36.jpg]]
>
> ![[06DP-slide-37.jpg]]

~~~text
KNAPSACK(n, W, w1..wn, v1..vn):
    para w ← 0 hasta W:  M[0, w] ← 0
    para i ← 1 hasta n:
        para w ← 0 hasta W:
            si w_i > w:  M[i, w] ← M[i − 1, w]
            si no:       M[i, w] ← max{ M[i − 1, w], v_i + M[i − 1, w − w_i] }
    devolver M[n, W]
~~~

Cada casilla de la fila $i$ sólo mira la **fila $i-1$**: justo arriba (no tomar) y arriba a la izquierda (tomar). Por eso llenar fila por fila es un orden válido.

Tabla completa de la diapositiva 37 (filas = objetos disponibles, columnas = límite $w$):

| objetos \ $w$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| $\{\}$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $\{1\}$ | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| $\{1,2\}$ | 0 | 1 | 6 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| $\{1,2,3\}$ | 0 | 1 | 6 | 7 | 7 | **18** | 19 | 24 | 25 | 25 | 25 | 25 |
| $\{1,..,4\}$ | 0 | 1 | 6 | 7 | 7 | 18 | 22 | 24 | 28 | 29 | 29 | **40** |
| $\{1,..,5\}$ | 0 | 1 | 6 | 7 | 7 | 18 | 22 | 28 | 29 | 34 | 35 | **40** |

Dos casillas calculadas a mano:

- $M[3,7]$: el objeto 3 pesa 5 ≤ 7. $\max\{M[2,7],\;18+M[2,2]\}=\max\{7,\;18+6\}=24$: conviene tomar 3 junto con el 2.
- $M[4,11]$: $\max\{M[3,11],\;22+M[3,5]\}=\max\{25,\;22+18\}=40$: tomar 4 y llenar los 5 kg restantes con lo mejor de $\{1,2,3\}$, que es el objeto 3.

**Explora la tabla.** Avanza casilla por casilla: verde es «no tomar» ($M[i-1,w]$), amarillo es «tomar» ($M[i-1,w-w_i]$). «Reconstruir solución» dibuja el camino de las flechas de la diapositiva 37. Abajo se comparan las tres reglas voraces del quiz 2.

<iframe src="pd-mochila-tabla.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 10. Tiempo de ejecución y reconstrucción (diapositiva 38)

> [!example]+ Diapositiva 38
> ![[06DP-slide-38.jpg]]

**Teorema.** El algoritmo resuelve la mochila con $n$ objetos y límite $W$ en **$\Theta(nW)$ tiempo y $\Theta(nW)$ espacio**.

- La tabla tiene $(n+1)(W+1)=\Theta(nW)$ casillas, cada una en $O(1)$.
- **Reconstrucción:** el objeto $i$ está en la solución de $OPT(i,w)$ **si y sólo si** $M[i,w]>M[i-1,w]$. Empezamos en $(n,W)$; si se toma $i$, bajamos a $(i-1,\,w-w_i)$; si no, a $(i-1,\,w)$. Son $n$ pasos, $O(n)$.

Siguiendo las flechas de la diapositiva 37:

| casilla | comparación | decisión | sigue en |
|:--|:--|:--|:--|
| $M[5,11]=40$ | $=M[4,11]=40$ | no tomar 5 | $(4,11)$ |
| $M[4,11]=40$ | $>M[3,11]=25$ | **tomar 4** | $(3,\,11-6=5)$ |
| $M[3,5]=18$ | $>M[2,5]=7$ | **tomar 3** | $(2,\,5-5=0)$ |
| $M[2,0]=0$, $M[1,0]=0$ | iguales | no tomar | fin |

Solución: $\{3,4\}$, valor \$40, peso 11 kg.

**Observaciones de la lámina.**

- El algoritmo **depende críticamente** de que los pesos sean enteros: son índices de columna.
- **No** se usó que los valores sean enteros: los $v_i$ sólo se suman y comparan.

> [!note] Complemento: memoria $O(W)$
> Como cada fila sólo usa la anterior, basta un arreglo de tamaño $W+1$ si se recorre $w$ **de $W$ hacia $0$** (para no reutilizar el objeto $i$ en la misma fila). El valor óptimo sale en $O(W)$ memoria, pero se pierde la tabla completa necesaria para la reconstrucción anterior.

## 11. Quiz 4: ¿hay algoritmo polinomial? Tiempo pseudopolinomial (diapositiva 39)

> [!example]+ Diapositiva 39
> ![[06DP-slide-39.jpg]]

**Respuesta: D, se desconoce.** La mochila es **NP-difícil**, así que un algoritmo polinomial existe si y sólo si $\mathbf{P}=\mathbf{NP}$, que es la conjetura abierta. Las otras opciones fallan así:

- **A** confunde $\Theta(nW)$ con tiempo polinomial. El tamaño de la entrada es el número de **bits** para escribirla: $W$ ocupa $\approx\log_2 W$ bits. Por eso $nW=n\cdot2^{\log_2 W}$ es **exponencial** en el tamaño de $W$. Si $W=2^{60}$, la entrada cabe en unas pocas líneas, pero la tabla tendría $\approx10^{18}$ columnas.
- **B** es cierto sobre **este** algoritmo, pero no prueba que no exista otro algoritmo polinomial.
- **C** sólo sería correcto suponiendo $\mathbf{P}\neq\mathbf{NP}$, que no está demostrado.

A un tiempo polinomial en $n$ y en el **valor numérico** de la entrada (no en su longitud en bits) se le llama **pseudopolinomial**. Es muy útil en la práctica cuando $W$ es pequeño. Conecta con [[P versus NP|P versus NP]] de la introducción del curso.

## 12. Cambio de monedas con PD (diapositivas 40–41)

> [!example]+ Diapositivas 40–41
> ![[06DP-slide-40.jpg]]
>
> ![[06DP-slide-41.jpg]]

**Problema.** Dadas $n$ denominaciones $\{d_1,\ldots,d_n\}$ (cada una con copias ilimitadas) y un valor $V$, encontrar el **menor número de monedas** que suman $V$, o reportar que es imposible.

**Recordatorio.** En la [[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas|clase del 22 de septiembre]] vimos que el cajero voraz (tomar siempre la moneda más grande que quepa) es óptimo para las monedas de EE. UU., pero no para denominaciones arbitrarias. Con los «timbres» $\{1,10,21,34,70,100,350,1295,1500\}$ y $V=140$:

- voraz: $100+34+1+1+1+1+1+1$, **8 monedas**;
- óptimo: $70+70$, **2 monedas**.

**Estado.** $OPT(v)$ = mínimo de monedas para formar exactamente $v$. **Objetivo:** $OPT(V)$.

**Elección múltiple.** Fijamos la **última moneda**: alguna denominación $d_i$. Lo que queda, $v-d_i$, debe formarse con el mínimo de monedas (si no, lo cambiaríamos: subestructura óptima por intercambio).

$$
OPT(v)=\begin{cases}
\infty, & v<0,\\[1mm]
0, & v=0,\\[1mm]
\displaystyle\min_{1\le i\le n}\bigl\{\,1+OPT(v-d_i)\,\bigr\}, & v>0.
\end{cases}
$$

$\infty$ codifica «imposible»: si una moneda se pasa del monto, esa opción nunca gana el mínimo; si todas las opciones dan $\infty$, $OPT(v)=\infty$. *(La lámina escribe $c_i$ en el texto y $d_i$ en la fórmula; son lo mismo.)*

**¿Por qué basta una variable aquí y en la mochila no?** Porque las monedas se pueden **repetir**: tras usar una de 70, sigue habiendo de 70. No hay que recordar qué denominaciones quedan, sólo cuánto falta. Es la variante «sin límite de copias» que mencionamos en el quiz 3.

~~~text
COIN-CHANGE(d1..dn, V):
    OPT[0] ← 0
    para v ← 1 hasta V:
        OPT[v] ← ∞;  ULT[v] ← nada
        para i ← 1 hasta n:
            si d_i ≤ v y 1 + OPT[v − d_i] < OPT[v]:
                OPT[v] ← 1 + OPT[v − d_i];  ULT[v] ← d_i
    devolver OPT[V]          # reconstruir: restar ULT[v] hasta llegar a 0
~~~

**Tiempo: $O(nV)$**, memoria $O(V)$. Igual que la mochila, es **pseudopolinomial**: depende del valor $V$, no de su número de bits.

### Ejemplo a mano: $\{1,4,6\}$ y $V=8$

El voraz toma $6+1+1$ (3 monedas). La tabla:

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| $1+OPT(v-1)$ | — | 1 | 2 | 3 | 4 | 2 | 3 | 2 | 3 |
| $1+OPT(v-4)$ | — | — | — | — | **1** | 2 | 3 | 4 | **2** |
| $1+OPT(v-6)$ | — | — | — | — | — | — | **1** | 2 | 3 |
| $OPT(v)$ | 0 | 1 | 2 | 3 | 1 | 2 | 1 | 2 | **2** |

$OPT(8)=2$ con última moneda 4, y $OPT(4)=1$: la solución es $4+4$.

**Explora el cambio de monedas.** Compara el cajero voraz con la PD para el ejemplo de la lámina o para tus propias denominaciones; haz clic en cualquier casilla $OPT(v)$ para ver su mínimo. El ejemplo $\{4,7\}$, $V=12$ muestra un caso donde el voraz ni siquiera encuentra cambio.

<iframe src="pd-cambio-monedas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 13. Comparativa y guía para ejercicios

| Problema | Estado | Elección | Ecuación | Tiempo |
|:--|:--|:--|:--|:--|
| Intervalos con pesos | $OPT(j)$, prefijo | binaria | $\max\{OPT(j-1),\,w_j+OPT(p(j))\}$ | $O(n\log n)$ |
| Kadane | $OPT(i)$, termina en $i$ | binaria | $\max\{x_i,\,x_i+OPT(i-1)\}$ | $O(n)$ |
| Mín. cuadrados segmentados | $OPT(j)$, prefijo | múltiple ($j$ inicios) | $\min_i\{e_{ij}+c+OPT(i-1)\}$ | $O(n^3)$ → $O(n^2)$ |
| Mochila 0/1 | $OPT(i,w)$ | binaria | $\max\{OPT(i-1,w),\,v_i+OPT(i-1,w-w_i)\}$ | $\Theta(nW)$, pseudopolinomial |
| Cambio de monedas | $OPT(v)$ | múltiple ($n$ monedas) | $\min_i\{1+OPT(v-d_i)\}$ | $O(nV)$, pseudopolinomial |

**Receta para un problema nuevo.**

1. **Mira la última decisión** de una solución óptima: ¿el último objeto entra?, ¿dónde empieza el último segmento?, ¿cuál es la última moneda?
2. **Pregunta qué hay que saber después** de esa decisión. Esas son las variables del estado: prefijo, capacidad, monto…
3. **Escribe la ecuación** con $\max$ o $\min$ sobre todas las opciones, y justifica la subestructura óptima con un argumento de intercambio.
4. **Casos base**, incluido «imposible» ($\infty$ o $-\infty$) cuando aplique.
5. **Orden de llenado** en que cada dependencia ya esté calculada.
6. **Costo** = número de estados × costo por estado (+ preprocesamiento). Si depende de un **valor numérico** ($W$, $V$), es pseudopolinomial.
7. **Reconstrucción**: guarda la opción ganadora o compárala de nuevo hacia atrás.

> [!question]- Autocomprobación
> 1. En la tabla de la mochila, ¿por qué $M[5,7]=28$ si $M[4,7]=24$? *El objeto 5 pesa 7 y vale 28; $28+M[4,0]=28>24$.*
> 2. ¿Por qué el voraz por razón $v_i/w_i$ falla en la mochila 0/1 pero no en la fraccionaria? *En la fraccionaria se rellenan los 4 kg sobrantes con parte del objeto 4; en la 0/1 sólo caben objetos de poco valor.*
> 3. En mínimos cuadrados segmentados, ¿qué pasa si $c=0$? *Cada tramo de 1 o 2 puntos tiene error 0, así que cualquier partición fina es óptima: el modelo sobreajusta.*
> 4. ¿Por qué el cambio de monedas sólo necesita $OPT(v)$ y la mochila necesita $OPT(i,w)$? *Las monedas se repiten; los objetos de la mochila no, así que hay que recordar cuáles siguen disponibles.*
> 5. Un algoritmo $O(nV)$ para monedas, ¿es polinomial? *No en el tamaño de la entrada: $V$ se escribe con $\log V$ bits. Es pseudopolinomial.*

## Referencia y continuación

- Fuente: [[06DynamicProgrammingI.pdf|Kevin Wayne, *Dynamic Programming I*, diapositivas 24–41]]; Kleinberg y Tardos, *Algorithm Design*, secciones 6.3 y 6.4. Diapositivas extraídas en `Recursos/slides-06-pd/`.
- Clase anterior: [[2026-11-03 ADA - Programacion dinamica|Programación dinámica I: intervalos con pesos y subarreglo máximo (diapositivas 1–23)]].
- Pendiente en el archivo: diapositivas 42–55 (estructura secundaria de RNA).
- Siguiente apunte: [[2026-11-12 ADA - Programacion dinamica III - Alineamiento y Hirschberg|12 de noviembre — alineamiento de secuencias y algoritmo de Hirschberg (presentación Dynamic Programming II)]].
