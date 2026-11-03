---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-08"
unidad: Algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Código de prefijos
  - Árbol binario de un código
  - Árbol binario completo (full)
  - Profundidad de una hoja
  - Argumento de intercambio
referencias:
  - "[[2026-10-06 ADA - codigos-de-prefijos]]"
  - "[[05CodigosHuffman.pdf]], páginas 11–20"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 42–48 (complemento de estudio)"
  - "Kleinberg y Tardos, Algorithm Design, sección 4.8 (pp. 166–171), enunciados (4.28)–(4.31)"
tags:
  - clase
  - algoritmos
  - greedy
  - huffman
  - arboles-binarios
  - exchange-argument
---

# Clase 14 · Árboles binarios y estructura de los códigos óptimos

![[05CodigosHuffman.pdf]]

> [!info] Alcance de la sesión
> En la [[2026-10-06 ADA - codigos-de-prefijos|clase anterior]] quedó planteado el problema: encontrar un código de prefijos con $\operatorname{PBS}$ mínimo. Esta sesión traduce **códigos de prefijos a árboles binarios** y viceversa, y con esa traducción demuestra tres lemas sobre cómo luce un árbol óptimo. Los tres se prueban con **argumentos de intercambio**, igual que EDF y Bélády. Al terminar sabemos exactamente qué decisión voraz es segura; el algoritmo queda para la [[2026-10-13 ADA - algoritmo-de-huffman|siguiente clase]].

> [!tip] Cobertura complementaria de *Greedy Algorithms II*
> Más abajo se desarrolla **Prim, Kruskal y borrado inverso (diapositivas 42–48)**, con prueba intuitiva, SVG, laboratorio cuando aporta una exploración útil y ejercicios tipo examen. Este bloque amplía la cobertura del material sin alterar el registro original de la sesión.

## Pregunta central

Sin conocer el código óptimo, ¿qué podemos afirmar con certeza sobre su forma? En particular, ¿dónde tienen que ir los símbolos menos frecuentes?

> [!summary] Idea de la clase
> Todo código de prefijos es un árbol binario cuyas hojas son los símbolos: el camino de la raíz a una hoja, leyendo $0$ a la izquierda y $1$ a la derecha, es su palabra. Entonces $|\gamma(x)|=\operatorname{depth}(x)$ y
> $$\operatorname{PBS}(T)=\sum_{x\in\Sigma}f_x\operatorname{depth}(x).$$
> En un árbol óptimo: **(1)** todo nodo interno tiene dos hijos; **(2)** más profundo implica menos frecuente; **(3)** existe un óptimo en el que los **dos símbolos menos frecuentes son hermanos**. Esta última propiedad es la elección voraz de Huffman.

---

## 1. De árboles binarios a códigos

Sea $T$ un árbol binario enraizado con $|\Sigma|$ hojas, cada una etiquetada con un símbolo distinto de $\Sigma$. Etiquetamos cada arista que va a un hijo izquierdo con `0` y cada arista a un hijo derecho con `1`. El código de $x$ es la secuencia de bits del camino de la raíz a la hoja de $x$.

### 1.1 Ejemplo de la clase

```text
              •
          0 /   \ 1
           •     •
         0/ \1  0/ \1
         a   c  b   •
                  0/ \1
                   e   d
```

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma'''$ | `00` | `10` | `01` | `111` | `110` |

### 1.2 Por qué el resultado es un código de prefijos

- **Unicidad:** los caminos a hojas distintas son distintos, así que cada símbolo recibe una palabra distinta.
- **Propiedad de prefijos:** ningún camino a una hoja está contenido en otro. Si $\gamma(x)$ fuera prefijo de $\gamma(y)$, el camino a $y$ pasaría por la hoja de $x$, pero una hoja no tiene descendientes.

### 1.3 Un árbol que desperdicia bits

El segundo árbol de las notas es

```text
              •
          0 /   \ 1
           •     •
         0/    0/ \1
         d     •    •
             0/ \1 0/ \1
             c   b a   e
```

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma^{iv}$ | `110` | `101` | `100` | `00` | `111` |

También es un código de prefijos válido, pero el hijo izquierdo de la raíz tiene **un solo hijo**. El bit que lleva a $d$ después del primer `0` no distingue nada: $d$ podría codificarse con `0`. Esta observación es el primer lema (§4).

---

## 2. De códigos a árboles binarios

En sentido inverso, se construye $T$ **inductivamente leyendo los bits uno a uno**: `0` → bajar a la izquierda, `1` → bajar a la derecha (creando nodos cuando no existan). Al terminar la palabra de $x$, el nodo alcanzado es la hoja de $x$.

Para $\gamma$ ($a=11$, $b=01$, $c=001$, $d=10$, $e=000$), en la raíz se separan $\{b,c,e\}$ (empiezan con `0`) de $\{a,d\}$ (empiezan con `1`). Del lado `0`: $\{c,e\}$ siguen con `0` y $b$ con `1`. Y así:

```text
                •
           0 /     \ 1
            •        •
          0/ \1    0/ \1
          •   b    d   a
        0/ \1
        e   c
```

La propiedad de prefijos garantiza que ningún símbolo quede en un nodo interno: cada palabra termina en una hoja.

> [!important] Equivalencia
> **Árbol** ↔ unicidad y propiedad de prefijos. **Binario** ↔ código binario. Por tanto, buscar el mejor código de prefijos es lo mismo que buscar el mejor árbol binario con hojas etiquetadas.

---

## 3. El PBS en lenguaje de árboles

La longitud de una palabra es el número de aristas del camino: $|\gamma(x)|=\operatorname{depth}(x)$, la distancia de la raíz a la hoja con símbolo $x$. Entonces

$$
\boxed{\operatorname{PBS}(T)=\sum_{x\in\Sigma}f_x\cdot\operatorname{depth}(x)}
$$

Para el árbol de $\gamma$ con $f=(.32,.25,.20,.18,.05)$:

$$
\operatorname{PBS}=.32(2)+.25(2)+.20(3)+.18(2)+.05(3)=2.25,
$$

el mismo valor de la clase anterior, ahora leído como “frecuencia por profundidad”.

> [!quote] Interludio: *La llegada* (*Arrival*)
> Las notas incluyen una imagen de los logogramas circulares de los heptápodos. Es un recordatorio de que **codificar** es elegir una representación: la misma información puede escribirse de formas muy distintas, y algunas son más compactas que otras.

---

## 4. Lema 1: el árbol de un código óptimo es completo

> [!important] Lema
> El árbol binario correspondiente a un código óptimo es necesariamente **completo**: cada vértice interno tiene exactamente 2 hijos.

En inglés se dice *full binary tree*. No confundir con “árbol completo” en el sentido de heaps (todos los niveles llenos salvo el último).

**Prueba (intercambio).** Supongamos que $T$ es óptimo y tiene un nodo $u$ con un único hijo $v$. Construimos $T'$ quitando $u$ y colgando $v$ en su lugar:

- si $u$ era la raíz, $v$ pasa a ser la raíz;
- si no, $v$ se vuelve hijo del padre de $u$.

Cada hoja en el subárbol de $u$ sube un nivel y las demás no cambian. Como hay al menos una hoja bajo $u$ con frecuencia positiva,

$$
\operatorname{PBS}(T')<\operatorname{PBS}(T),
$$

lo cual contradice que $T$ sea óptimo. $\square$

En el ejemplo de $\gamma^{iv}$: contraer el nodo de un solo hijo cambia $d$ de `00` a `0` y baja el PBS en $f_d=.18$.

---

## 5. Lema 2: más profundo implica menos frecuente

> [!important] Lema
> Sea $T$ el árbol de un código óptimo y sean $x,y\in\Sigma$ tales que $\operatorname{depth}(x)<\operatorname{depth}(y)$. Entonces $f_x\ge f_y$.

**Prueba (intercambio… de nuevo).** Por contradicción, supongamos $f_x<f_y$. Sea $T'$ el árbol que resulta de **intercambiar las etiquetas** $x$ y $y$. Separamos la parte que no cambia:

$$
\omega=\sum_{z\ne x,y}f_z\operatorname{depth}(z).
$$

$$
\operatorname{PBS}(T)=\omega+f_x\operatorname{depth}(x)+f_y\operatorname{depth}(y),
$$

$$
\operatorname{PBS}(T')=\omega+f_x\operatorname{depth}(y)+f_y\operatorname{depth}(x).
$$

Restando:

$$
\begin{aligned}
\operatorname{PBS}(T)-\operatorname{PBS}(T')
&=\operatorname{depth}(x)(f_x-f_y)-\operatorname{depth}(y)(f_x-f_y)\\
&=\underbrace{\big(\operatorname{depth}(x)-\operatorname{depth}(y)\big)}_{<0}\;\underbrace{\big(f_x-f_y\big)}_{<0}\;>\;0 .
\end{aligned}
$$

Así $\operatorname{PBS}(T')<\operatorname{PBS}(T)$, contradicción con la optimalidad de $T$. $\square$

> [!example] El intercambio que mejoró $\gamma$
> En el árbol de $\gamma$, $c$ está a profundidad 3 con $f_c=.20$ y $d$ a profundidad 2 con $f_d=.18$: viola el lema. Intercambiarlos ahorra $(3-2)(.20-.18)=.02$, y se obtiene exactamente $\operatorname{PBS}=2.23$, el valor de $\gamma'$.

### 5.1 Consecuencia: si nos dieran la forma del árbol

Kleinberg–Tardos destacan una lectura útil: si alguien nos diera la **forma** de un árbol óptimo $T^*$ sin etiquetas, sabríamos etiquetarlo: las hojas menos profundas reciben los símbolos más frecuentes, nivel por nivel. Dentro de un mismo nivel el orden **no importa**, porque todas esas hojas tienen el mismo multiplicador $\operatorname{depth}$.

El problema es que no conocemos la forma, y hay exponencialmente muchas. La clave es mirar el **fondo** del árbol.

---

## 6. Lema 3: los dos menos frecuentes pueden ser hermanos

> [!important] Lema
> Existe un árbol $T^*$ de un código óptimo tal que los dos símbolos con frecuencias más pequeñas son **hermanos** en $T^*$.

**Prueba.** Sea $T$ un árbol óptimo y sean $x,y$ los dos símbolos de menor frecuencia.

1. Toma una hoja $v$ de **profundidad máxima**. Por el Lema 1, su padre tiene otro hijo $w$.
2. $w$ también es hoja: si no lo fuera, tendría una hoja debajo con profundidad mayor que la de $v$, contradiciendo la elección de $v$.
3. Por el Lema 2, las hojas de mayor profundidad llevan las frecuencias menores. Entonces $x$ y $y$ están en el nivel más profundo (o tienen la misma frecuencia que quienes ocupan esas hojas).
4. Intercambia las etiquetas para que $x$ y $y$ ocupen $v$ y $w$. Los intercambios ocurren entre hojas del **mismo nivel** (o entre símbolos de igual frecuencia), así que el PBS no cambia.

El árbol resultante $T^*$ cumple $\operatorname{PBS}(T^*)=\operatorname{PBS}(T)$, es óptimo y tiene a $x,y$ como hermanos. $\square$

En las notas: en $T$, $x$ y $y$ estaban en el último nivel pero separados ($x$ junto a $w$); intercambiar $y$ con $w$ los vuelve hermanos sin cambiar el PBS.

---

## 7. Corolario

> [!summary] Corolario
> Sea $T^*$ el árbol de un código óptimo. Entonces:
> 1. $T^*$ es completo.
> 2. Los símbolos con frecuencias mínimas aparecen en las hojas de mayor profundidad.
> 3. Podemos suponer que los dos símbolos con menor frecuencia tienen el **mismo padre** en $T^*$.

El punto 3 es la **propiedad de elección voraz**: es seguro “amarrar” a los dos símbolos menos frecuentes como hermanos antes de saber nada más del árbol.

---

## 8. Complemento del libro: por qué dividir arriba no funciona

La estrategia de Shannon–Fano trabaja **de arriba hacia abajo**: dividir $\Sigma$ en dos grupos de frecuencia total lo más parecida posible a $\tfrac12$, asignar `0` a uno y `1` al otro, y repetir.

Con $f=(.32,.25,.20,.18,.05)$, la única división exacta es $\{a,d\}$ (.50) contra $\{b,c,e\}$ (.50). Luego $\{b\}$ (.25) contra $\{c,e\}$ (.25). El resultado es precisamente el árbol de $\gamma$, con $\operatorname{PBS}=2.25$, que no es óptimo: viola el Lema 2.

> [!warning] Lección
> Preocuparse primero por la división de la raíz parece natural, pero no es una elección segura. Los lemas sugieren lo contrario: **empezar por el fondo**, con los dos símbolos menos frecuentes.

---

## 9. Laboratorio interactivo

En la pestaña **Árbol del código** puedes ver cómo cada código de la clase se convierte en árbol y seguir el camino de cada bit. En **Intercambio** puedes hacer clic en dos hojas para intercambiar sus etiquetas y ver la fórmula $(\operatorname{depth}(x)-\operatorname{depth}(y))(f_x-f_y)$ en acción.

<iframe src="codigos-prefijos-y-arboles.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Árbol ↔ código:** `0` izquierda, `1` derecha; los símbolos solo en hojas.
> - **PBS:** $\sum f_x\operatorname{depth}(x)$.
> - **Intercambio:** mover un símbolo más frecuente a una hoja menos profunda nunca empeora el PBS.
> - **Hermanos:** las dos hojas más profundas son hermanas en un árbol completo.

---

## 10. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| “Completo” significa todos los niveles llenos. | Aquí significa que **ningún nodo interno tiene un solo hijo** (*full*). |
| El Lema 3 dice que **todo** óptimo tiene a los dos menores como hermanos. | Dice que **existe** uno así; con empates puede haber óptimos donde no lo sean. |
| Intercambiar hojas del mismo nivel cambia el PBS. | No: las profundidades, y por tanto los multiplicadores, son iguales. |
| Los símbolos pueden ir en nodos internos. | Entonces su palabra sería prefijo de las palabras de sus descendientes. |
| Shannon–Fano es óptimo porque divide de forma balanceada. | En el ejemplo de clase produce PBS 2.25, mientras que existe 2.23. |

---

## 11. Preguntas de autoevaluación

1. Dibuja el árbol del código $\gamma'$ ($a=11$, $b=10$, $c=01$, $d=001$, $e=000$) y verifica que es completo.
2. ¿Por qué ningún símbolo puede quedar en un nodo interno del árbol de un código de prefijos?
3. En la prueba del Lema 1, ¿qué pasa si $u$ es la raíz?
4. En el Lema 2, ¿por qué el término $\omega$ desaparece al restar?
5. En la prueba del Lema 3, ¿qué falla si el árbol no fuera completo?
6. Para $f_a=.4$, $f_b=.3$, $f_c=.2$, $f_d=.1$, ¿qué dos símbolos podemos suponer hermanos en un árbol óptimo?

<details>
<summary>Respuestas breves</summary>

1. Raíz: `0` → nodo con $c$ (`01`) y nodo con $e,d$ (`000`, `001`); `1` → $b$ (`10`) y $a$ (`11`). Todo nodo interno tiene dos hijos.
2. Su palabra sería prefijo de la palabra de cualquier hoja debajo de él.
3. Se elimina la raíz y su único hijo se vuelve la nueva raíz; todas las hojas suben un nivel.
4. Porque los demás símbolos conservan su profundidad en $T$ y en $T'$.
5. La hoja más profunda podría no tener hermano, o su hermano podría ser interno; el argumento de que existe una pareja de hojas hermanas en el último nivel se rompe.
6. $c$ y $d$, las dos frecuencias más pequeñas.

</details>

---

## Puente de *Greedy Algorithms II*: Prim, Kruskal y borrado inverso (diapositivas 42–48)

Las tres rutinas son formas concretas de aplicar las reglas de corte y ciclo de la [[2026-10-06 ADA - codigos-de-prefijos|sección anterior]]. Todas producen un MST en un grafo no dirigido y conexo, pero recorren las aristas de manera distinta.

![[mst-tres-recorridos.svg]]

| Método | Decisión | Invariante visible | Estructura |
|---|---|---|---|
| **Prim** | Desde el árbol actual $S$, toma la arista más barata que cruza $(S,V\setminus S)$. | Un árbol conectado crece desde la raíz. | Min-heap de $\pi[v]$: mejor arista conocida de $S$ a $v$. |
| **Kruskal** | Recorre aristas por costo creciente; acepta si une dos componentes. | Un bosque sin ciclos se fusiona. | Ordenamiento y Union-Find. |
| **Borrado inverso** | Recorre aristas por costo decreciente; borra si el resto sigue conexo. | La conectividad permanece mientras desaparecen ciclos. | Pruebas de conectividad; útil sobre todo como regla conceptual. |

**Prim paso a paso.** Partimos de $S=\{s\}$; para cada $v\notin S$, $\pi[v]$ es el costo de la arista más barata de $S$ a $v$. Se extrae el $v$ de menor $\pi$, se añade su arista predecesora y se actualizan las llaves de vecinos externos. Si se usa un heap con `decrease-key`, cuesta $O(m\log n)$; con una cola de inserciones duplicadas, $O(m\log m)$. La prueba es la **regla azul** para el corte de $S$.

**La diferencia con Dijkstra es la llave.** En Prim, $\pi[v]=\min\{c(u,v):u\in S\}$ mide **solo la arista que cruza**. En Dijkstra, $\pi[v]=\min\{d[u]+\ell(u,v):u\in S\}$ mide el **camino completo** desde $s$. Cambiar una fórmula por la otra resuelve otro problema.

**Kruskal paso a paso.** Ordenamos aristas, mantenemos una componente por cada árbol y aceptamos $(u,v)$ si `find(u)≠find(v)`. La arista aceptada es mínima para el corte de una componente actual; la rechazada cierra un ciclo donde es de costo máximo entre las aristas procesadas (con empates, una de las máximas). El costo total es $O(m\log m+m\alpha(n))=O(m\log m)$ con Union-Find optimizado. La implementación completa y sus operaciones se estudian en [[2026-10-22 ADA - Uniond-Find Datatype|Union-Find]].

**Borrado inverso.** Al procesar una arista cara, si existe otro camino entre sus extremos, esa arista pertenece a un ciclo y la regla roja permite eliminarla. Si no existe tal camino, es un puente en el grafo restante y hay que conservarla. Una implementación ingenua puede costar $O(m(m+n))$ al repetir DFS; la presentación la usa para mostrar la simetría de las reglas.

### Laboratorio: tres formas de construir el mismo MST

<iframe src="mst-reglas-y-algoritmos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Elige Prim, Kruskal o Borůvka y avanza decisión por decisión. El selector de corte muestra qué aristas lo cruzan y cuál es la más barata; si hay empate, varias elecciones pueden ser seguras. El bosque verde representa aristas ya aceptadas.

### Práctica tipo examen (9 puntos)

Con aristas $ab:4,ac:3,bc:1,bd:2,cd:4,ce:2,de:3,df:2,ef:3$, **(a)** traza Prim desde $a$ con desempate alfabético; anota $S$, $\pi$ y arista agregada en cada paso. **(b)** Traza Kruskal e indica por qué rechaza $ab$. **(c)** Da costo final y explica la prueba mediante un corte. **(d)** Si la arista $ce$ cambia a costo $-5$, ¿siguen siendo válidos Prim y Kruskal? Contrasta con Dijkstra.

<details><summary>Comprobación</summary>

(a) Una traza válida agrega $ac:3$, $bc:1$, $bd:2$, $ce:2$, $df:2$. (b) Tras $bc,bd,ce,df,ac$, $a$ y $b$ ya están conectados; $ab$ cerraría un ciclo. (c) Costo $10$; en cada paso de Prim se elige la mínima arista del corte actual. (d) Sí: MST admite costos negativos; sus intercambios solo comparan costos. Dijkstra necesita longitudes no negativas.

</details>

---

## Conexiones

- **Clase anterior:** [[2026-10-06 ADA - codigos-de-prefijos|códigos de prefijos y PBS]].
- **Clase siguiente:** [[2026-10-13 ADA - algoritmo-de-huffman|algoritmo de Huffman]].
- **Mismo patrón de prueba:** el intercambio de inversiones en EDF y de expulsiones en Bélády ([[2026-09-29 ADA - Contunuacion-scheduling|clase del 29 de septiembre]]).
- **Árboles:** [[2026-09-03 ADA - grafos|grafos y árboles]].
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, sección 4.8, pp. 166–171: enunciados (4.28) a (4.31).
2. Castañeda Rojano, A. *Códigos de Huffman* (notas manuscritas, `05CodigosHuffman.pdf`), pp. 11–20.
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2009). *Introduction to Algorithms*, 3.ª ed. MIT Press, sección 16.3, lemas 16.2 y 16.3.

## Resumen después de clase

Los códigos de prefijos son árboles binarios con símbolos en las hojas, y el PBS es la suma de frecuencia por profundidad. Con tres argumentos de intercambio se obtiene la forma de un árbol óptimo: es completo, los símbolos menos frecuentes están al fondo, y podemos suponer que los dos menos frecuentes son hermanos. Esa última propiedad dice qué decisión voraz es segura y prepara el algoritmo de Huffman, que construye el árbol de abajo hacia arriba.

## Acciones adicionales

- [ ] Reescribir de memoria la cuenta $\operatorname{PBS}(T)-\operatorname{PBS}(T')=(\operatorname{depth}(x)-\operatorname{depth}(y))(f_x-f_y)$.
- [ ] Construir el árbol de un código de prefijos de 6 símbolos y comprobar si es completo.
- [ ] Encontrar un ejemplo con empates donde exista un óptimo en que los dos menos frecuentes **no** sean hermanos.
