---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-22"
unidad: Algoritmos voraces · estructuras de datos
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Estructura Union-Find (conjuntos disjuntos)
  - Quick-find
  - Quick-union
  - Unión por tamaño (weighted union)
  - Compresión de caminos
  - Función inversa de Ackermann
  - Algoritmo de Kruskal
  - Percolación y conectividad dinámica
referencias:
  - "[[2026-10-20 ADA - bienary heap y heap sort]]"
  - "[[15UnionFind.pdf]], diapositivas 4–42 (estructura) y 44–57 (percolación)"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 46–47 (Kruskal) y 64 (clustering)"
  - "Kleinberg y Tardos, Algorithm Design, secciones 4.5–4.6"
  - "Wayne, K., presentación Union-Find (Kleinberg–Tardos)"
tags:
  - clase
  - algoritmos
  - estructuras-de-datos
  - union-find
  - conjuntos-disjuntos
  - kruskal
  - analisis-amortizado
---

# Clase 17 · Estructura Union-Find (conjuntos disjuntos)

> [!info] Alcance de la sesión
> Siguiendo la presentación de Kleinberg–Tardos, se vieron cuatro implementaciones del tipo de datos **Union-Find**, todas con las operaciones `MAKE-SET`, `FIND-SET` y `UNION`: **quick-find** (*fast find*), **quick-union** (*fast union*), **unión ponderada** (*weighted*) y **compresión de caminos** (*path compression*). Es la estructura que hace eficiente al algoritmo de **Kruskal** para árboles generadores mínimos, así como el [[2026-10-20 ADA - bienary heap y heap sort|heap]] hace eficientes a Dijkstra y Prim.

> [!quote] Apuntes rápidos originales
> - Implementaciones vistas en clase, siguiendo la presentación de Tardos.
> - Fast find, fast union, weighted, compression; todas con crear (`MAKE-SET`), `FIND-SET` y `UNION`.

> [!warning] Nota reconstruida
> El desarrollo y los costos siguen Kleinberg–Tardos §4.6 y la presentación de Wayne. Las convenciones de desempate (qué raíz cuelga de cuál) son una elección; verifica la que usó el profesor.

> [!info] Diapositivas añadidas para estudiar
> La presentación de Sedgewick y Wayne **1.5 Union-Find** muestra paso a paso las mismas representaciones y después las aplica a percolación. El bloque de percolación de esta nota es un **complemento de estudio**, no un registro de lo visto en el pizarrón.

![[15UnionFind.pdf]]

## Pregunta central

Kruskal necesita preguntar una y otra vez “¿$u$ y $v$ ya están en la misma componente?” mientras las componentes se van fusionando. ¿Cómo representar una partición que solo **crece por uniones** para responder esa pregunta casi en tiempo constante?

> [!summary] Idea de la clase
> Cada conjunto se representa con un **elemento representante**. *Quick-find* guarda el representante de cada elemento en un arreglo: `FIND` es $O(1)$ pero `UNION` reetiqueta $O(n)$ elementos. *Quick-union* guarda un **bosque** de apuntadores al padre: `UNION` solo enlaza dos raíces, pero los árboles pueden degenerar en cadenas de altura $n-1$. La **unión ponderada** cuelga el árbol pequeño del grande y garantiza altura $\le\log_2 n$. Con **compresión de caminos**, cada `FIND` aplana el camino recorrido y $m$ operaciones cuestan $O(m\,\alpha(n))$, donde $\alpha$ —la inversa de Ackermann— no pasa de $4$ en la práctica.

---

## 1. Motivación: componentes que se fusionan

En [[2026-09-03 ADA - grafos|grafos]] calculamos componentes conexas con BFS o DFS en $O(m+n)$. Pero en Kruskal el grafo **cambia**: se agregan aristas una por una y, antes de cada una, hay que saber si sus extremos ya están conectados.

- Buscar un camino con BFS/DFS en el **bosque de aristas ya aceptadas**: $O(n)$ por consulta y $O(mn)$ para $m$ aristas examinadas.
- Con Union-Find ponderado y compresión: la secuencia completa tiene costo **casi lineal**; el costo casi constante es **amortizado**, no una garantía para cada consulta aislada.

La observación clave es que **nunca se quitan aristas**: las componentes solo se unen. Esa restricción es lo que permite una estructura tan eficiente.

**Antes de pensar en arreglos:** si empezamos con $\{1\},\{2\},\{3\},\{4\}$ y añadimos las conexiones $(1,2)$ y $(2,3)$, el resultado es $\{1,2,3\},\{4\}$. Entonces `connected(1,3)` es verdadero aunque no se haya añadido directamente $(1,3)$; existe el camino $1\to2\to3$. En cambio, `connected(1,4)` sigue siendo falso. La estructura guarda **componentes**, no una lista de todos los caminos.

---

## 2. El tipo de datos

Union-Find mantiene una **partición** de un conjunto de $n$ elementos en conjuntos disjuntos:

| Operación | Efecto |
|---|---|
| `MAKE-SET(x)` | Crea el conjunto unitario $\{x\}$. |
| `FIND-SET(x)` | Devuelve el **representante** del conjunto que contiene a $x$. |
| `UNION(x, y)` | Reemplaza los conjuntos de $x$ y $y$ por su unión. |

La conectividad es una **relación de equivalencia**: cada elemento está conectado consigo mismo (reflexividad), el sentido del camino no importa en este modelo no dirigido (simetría) y dos caminos que comparten un punto se concatenan (transitividad). Por eso los elementos conectados forman conjuntos disjuntos o **componentes**.

La única propiedad que se exige al representante es que sea **canónico**:

$$
\texttt{FIND-SET}(x)=\texttt{FIND-SET}(y)\iff x\text{ y }y\text{ están en el mismo conjunto}.
$$

Medimos el costo de una **secuencia** de $n$ `MAKE-SET` y $m$ operaciones `FIND`/`UNION` en total; a lo más hay $n-1$ uniones efectivas.

---

## 3. Quick-find (*fast find*)

**Representación:** un arreglo `id[1..n]`, donde `id[x]` es el representante del conjunto de $x$.

```python
def make_set(x):
    id[x] = x

def find(x):
    return id[x]                    # O(1)

def union(x, y):
    a, b = id[x], id[y]
    if a == b:
        return
    for z in range(1, n + 1):       # O(n): reetiquetar todo el conjunto de x
        if id[z] == a:
            id[z] = b
```

**Ejemplo** con $n=8$ y la secuencia $U(1,2)$, $U(3,4)$, $U(5,6)$, $U(7,8)$, $U(1,3)$, $U(5,7)$, $U(1,5)$ (el conjunto de $x$ toma la etiqueta del de $y$):

| Operación | `id[1..8]` |
|---|---|
| inicio | $1,2,3,4,5,6,7,8$ |
| $U(1,2)$ | $\mathbf2,2,3,4,5,6,7,8$ |
| $U(3,4)$ | $2,2,\mathbf4,4,5,6,7,8$ |
| $U(5,6)$ | $2,2,4,4,\mathbf6,6,7,8$ |
| $U(7,8)$ | $2,2,4,4,6,6,\mathbf8,8$ |
| $U(1,3)$ | $\mathbf4,\mathbf4,4,4,6,6,8,8$ |
| $U(5,7)$ | $4,4,4,4,\mathbf8,\mathbf8,8,8$ |
| $U(1,5)$ | $\mathbf8,\mathbf8,\mathbf8,\mathbf8,8,8,8,8$ |

**Costo:** `FIND` $O(1)$; `UNION` $O(n)$. Una secuencia de $n-1$ uniones cuesta $\Theta(n^2)$: demasiado para Kruskal en grafos grandes.

> [!tip] Mejora de Kleinberg–Tardos: reetiquetar el conjunto **pequeño**
> Si cada conjunto guarda la lista de sus elementos y su tamaño, `UNION` puede reetiquetar solo el conjunto **menor**. Cada vez que un elemento cambia de etiqueta, el tamaño de su conjunto al menos se **duplica**; como no puede pasar de $n$, cada elemento se reetiqueta a lo más $\log_2 n$ veces. Así, $k$ uniones cuestan $O(k\log k)$ en total —$O(\log n)$ **amortizado** por unión— aunque una unión aislada siga pudiendo costar $\Theta(n)$.

---

## 4. Quick-union (*fast union*)

**Representación:** un **bosque**. Cada elemento apunta a su padre con `parent[x]`; las raíces se apuntan a sí mismas y son los representantes.

```python
def make_set(x):
    parent[x] = x

def find(x):
    while parent[x] != x:           # subir hasta la raíz
        x = parent[x]
    return x

def union(x, y):
    r, s = find(x), find(y)
    if r != s:
        parent[r] = s               # enlazar raíces: O(1)
```

**Costo:** el enlace es $O(1)$, pero `FIND` cuesta la **profundidad** del nodo, y nada impide que los árboles sean altos.

**Peor caso:** $U(1,2)$, $U(2,3)$, …, $U(n-1,n)$ produce la cadena

$$
1\to2\to3\to\cdots\to n,
$$

de altura $n-1$, y `FIND(1)` recorre $n$ nodos. Ahora el cuello de botella se movió de `UNION` a `FIND`: $\Theta(n)$ en el peor caso.

---

## 5. Unión ponderada (*weighted quick-union*)

**Idea:** al unir, colgar la raíz del árbol con **menos nodos** de la raíz del árbol con más. Se guarda `size[r]` en cada raíz.

```python
def make_set(x):
    parent[x] = x
    size[x] = 1

def union(x, y):
    r, s = find(x), find(y)
    if r == s:
        return
    if size[r] > size[s]:           # que r sea la raíz del árbol menor
        r, s = s, r
    parent[r] = s
    size[s] += size[r]
```

**Ejemplo** con la misma secuencia de §3 (en empate, la raíz de $x$ cuelga de la de $y$):

| Operación | Enlace | Árboles resultantes |
|---|---|---|
| $U(1,2)$, $U(3,4)$, $U(5,6)$, $U(7,8)$ | $1\to2$, $3\to4$, $5\to6$, $7\to8$ | cuatro árboles de tamaño $2$ |
| $U(1,3)$ | raíces $2,4$ empatadas: $2\to4$ | $\{1,2,3,4\}$ con raíz $4$ |
| $U(5,7)$ | $6\to8$ | $\{5,6,7,8\}$ con raíz $8$ |
| $U(1,5)$ | raíces $4,8$ empatadas: $4\to8$ | un árbol de tamaño $8$ y raíz $8$ |

```text
                8
             /  |  \
            4   6   7
           / \  |
          2   3 5
          |
          1            profundidad(1) = 3 = log₂ 8
```

> [!important] Lema de la altura
> Con unión ponderada, todo nodo tiene profundidad a lo más $\log_2 n$.

**Demostración.** La profundidad de un nodo $x$ aumenta en $1$ solo cuando la raíz de su árbol $T_1$ se cuelga de la raíz de otro árbol $T_2$, y eso pasa solo si $|T_2|\ge|T_1|$. Entonces el árbol que contiene a $x$ pasa de tamaño $|T_1|$ a $|T_1|+|T_2|\ge2|T_1|$: **al menos se duplica**. Como empieza en $1$ y no puede superar $n$, eso ocurre a lo más $\log_2 n$ veces. $\square$

**Costo:** `FIND` y `UNION` en $O(\log n)$ en el peor caso.

> [!note] Unión por rango
> En vez del tamaño puede guardarse un **rango**, una cota superior de la altura: al unir se cuelga la raíz de menor rango y, en empate, el rango de la nueva raíz aumenta en $1$. Un árbol de rango $k$ tiene al menos $2^k$ nodos, así que la cota $\log_2 n$ es la misma. Es la versión que se combina habitualmente con compresión.

---

## 6. Compresión de caminos

**Idea:** cuando `FIND(x)` encuentra la raíz $r$, conviene que **todos** los nodos del camino de $x$ a $r$ apunten directamente a $r$. El trabajo extra es proporcional al que ya se hizo, y las siguientes búsquedas desde esos nodos serán de un solo paso.

```python
def find(x):
    r = x
    while parent[r] != r:           # 1.ª pasada: encontrar la raíz
        r = parent[r]
    while parent[x] != r:           # 2.ª pasada: apuntar todo el camino a r
        siguiente = parent[x]
        parent[x] = r
        x = siguiente
    return r
```

Versión recursiva compacta: `if parent[x] != x: parent[x] = find(parent[x])`.

**Ejemplo:** en el árbol de §5, `FIND(1)` recorre $1\to2\to4\to8$. Después de comprimir:

```text
antes:            8                después:          8
               /  |  \                       /  /  |  \  \
              4   6   7                     1  2   4   6  7
             / \  |                                |   |
            2   3 5                                3   5
            |
            1
```

Ahora $1$ y $2$ cuelgan directamente de $8$: la próxima `FIND(1)` es de un paso. La compresión **no** cambia qué elementos pertenecen a cada árbol, así que `size` sigue siendo el **tamaño exacto** en cada raíz; `rank` sigue siendo una **cota superior** válida, aunque ya no sea la altura real.

> [!example] Variante de una sola pasada
> **Partición a la mitad** (*path halving*): mientras se sube, cada nodo apunta a su abuelo (`parent[x] = parent[parent[x]]`). Tiene la misma cota asintótica y evita la segunda pasada.

### 6.1 El teorema de Tarjan

> [!important] Teorema (Tarjan, 1975)
> Con unión ponderada (por tamaño o rango) **y** compresión de caminos, cualquier secuencia de $m\ge n$ operaciones `MAKE-SET`, `FIND` y `UNION` sobre $n$ elementos cuesta
> $$
> O(m\,\alpha(m,n)),
>
> $$
> donde $\alpha$ es la **inversa de la función de Ackermann**.

- $\alpha(n)$ crece tan lento que $\alpha(n)\le4$ para cualquier $n$ menor que el número de átomos del universo: en la práctica, cada operación cuesta **constante amortizado**.
- Una cota más sencilla de demostrar (Hopcroft–Ullman, 1973) es $O(m\log^* n)$, con el logaritmo iterado de la diapositiva **41 de `15UnionFind.pdf`**:
$$
\lg^* n=\begin{cases}0 & n\le1\\ 1+\lg^*(\lg n) & n>1\end{cases}
\qquad \lg^*(2^{65536})=5 .
$$
- **No se garantiza $O(m)$ para todas las secuencias:** Fredman y Saks (1989) demostraron una cota inferior $\Omega(m\,\alpha(m,n))$ en el modelo de sondeo de celdas. La estructura alcanza esa cota asintótica.

---

## 7. Comparación de las cuatro implementaciones

Peor caso por operación ($n$ elementos):

| Implementación | `MAKE-SET` | `FIND` | `UNION` | Altura máxima |
|---|---:|---:|---:|---:|
| Quick-find (*fast find*) | $O(1)$ | $O(1)$ | $O(n)$ | $1$ |
| Quick-find reetiquetando el menor | $O(1)$ | $O(1)$ | $O(\log n)$ amortizado | $1$ |
| Quick-union (*fast union*) | $O(1)$ | $O(n)$ | $O(n)$ | $n-1$ |
| Unión ponderada | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $\lfloor\log_2 n\rfloor$ |
| Ponderada + compresión | $O(1)$ | $O(\alpha(n))$ amortizado | $O(\alpha(n))$ amortizado | — |

> [!tip] Lectura de la tabla
> Quick-find y quick-union son extremos opuestos: uno paga en `UNION` lo que el otro paga en `FIND`. La unión ponderada equilibra ambos al controlar la **forma** del árbol —igual que el heap controla su forma casi completa—, y la compresión aprovecha el trabajo de cada búsqueda para mejorar las futuras.

---

## 8. Aplicación: algoritmo de Kruskal

> [!info] Contexto mínimo
> La teoría completa de árboles generadores mínimos —ciclos, cortes, reglas roja y azul, Prim, Borůvka— está en *Greedy Algorithms II*, diapositivas 21–57. Aquí solo se usa lo necesario para entender por qué Kruskal necesita Union-Find.

Sea $G=(V,E)$ no dirigido y conexo, con costos $c_e$. Un **árbol generador** $T\subseteq E$ es acíclico y conexo (equivalentemente, conexo con $n-1$ aristas). Un **árbol generador mínimo** (MST) minimiza $\sum_{e\in T}c_e$. Por el teorema de Cayley, $K_n$ tiene $n^{n-2}$ árboles generadores: la fuerza bruta es inviable.

### 8.1 Algoritmo

Considerar las aristas en orden **creciente de costo** y agregar cada una **a menos que forme un ciclo**. Una arista $(u,v)$ forma un ciclo exactamente cuando $u$ y $v$ ya están en la misma componente del bosque construido: la pregunta de Union-Find.

```python
def kruskal(V, E, c):
    E.sort(key=c)                       # O(m log m)
    T = []
    for v in V:
        make_set(v)
    for (u, v) in E:
        if find(u) != find(v):          # ¿u y v en componentes distintas?
            T.append((u, v))
            union(u, v)                 # fusionar componentes
    return T
```

### 8.2 Corrección (idea)

Kruskal es un caso particular del algoritmo voraz de colorear aristas (diapositiva 46). Para la arista $e=(u,v)$ que se examina:

- **Mismo componente:** todas las demás aristas del ciclo que formaría ya están en $T$ y son más baratas (se examinaron antes); $e$ es la más cara del ciclo y puede descartarse (**regla roja**).
- **Componentes distintas:** tomemos el corte definido por la componente de $u$. Ninguna arista de ese corte es más barata que $e$ —si lo fuera, se habría examinado antes y habría unido ambos lados—, así que $e$ es la mínima del corte y está en algún MST (**regla azul**). $\square$

### 8.3 Costo

- Ordenar: $O(m\log m)=O(m\log n)$ para un **grafo simple**, donde $m\le n(n-1)/2$. Si se permiten aristas paralelas sin límite, se conserva la expresión $O(m\log m)$.
- $n$ `MAKE-SET`, $2m$ `FIND` y $n-1$ `UNION`: $O(m\log n)$ con unión ponderada, u $O(m\,\alpha(n))$ con compresión.

Total: $O(m\log m)$, dominado por el ordenamiento. Si las aristas ya vienen ordenadas, Kruskal con Union-Find óptimo es casi lineal.

### 8.4 Traza

Grafo de la diapositiva 52, con aristas ordenadas por costo:

| Arista  | Costo | `FIND(u)` vs `FIND(v)` | Decisión            | Componentes           |
| ------- | ----: | ---------------------- | ------------------- | --------------------- |
| $4$–$6$ |     1 | distintas              | ✔ agregar           | $\{4,6\}$             |
| $3$–$6$ |     2 | distintas              | ✔ agregar           | $\{3,4,6\}$           |
| $1$–$4$ |     3 | distintas              | ✔ agregar           | $\{1,3,4,6\}$         |
| $2$–$5$ |     4 | distintas              | ✔ agregar           | $\{1,3,4,6\},\{2,5\}$ |
| $1$–$5$ |     5 | distintas              | ✔ agregar           | $\{1,2,3,4,5,6\}$     |
| $1$–$2$ |     6 | iguales                | ✘ ciclo $1$–$2$–$5$ | —                     |
| $4$–$5$ |     7 | iguales                | ✘                   | —                     |
| $2$–$3$ |     8 | iguales                | ✘                   | —                     |
| $5$–$6$ |     9 | iguales                | ✘                   | —                     |

MST con $n-1=5$ aristas y costo $1+2+3+4+5=15$. Puede detenerse en cuanto $T$ tiene $n-1$ aristas.

> [!example] Clustering de un solo enlace (diapositiva 64)
> Para agrupar $n$ objetos en $k$ grupos maximizando la separación mínima entre grupos, se ejecuta **Kruskal y se detiene cuando quedan $k$ componentes** (equivalentemente, se calcula el MST y se quitan sus $k-1$ aristas más caras). Union-Find lleva la cuenta de las componentes: cada `UNION` efectiva reduce su número en $1$.

---

## 9. Laboratorio interactivo

<iframe src="union-find-interactivo.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Quick-find:** `id[x]` es el representante; unir reetiqueta todo un conjunto.
> - **Quick-union:** se sube por `parent[]` hasta la raíz; unir enlaza raíces y puede crear cadenas.
> - **Ponderada:** la raíz del árbol menor cuelga de la del mayor; altura $\le\log_2 n$.
> - **Compresión:** tras `FIND(x)`, todo el camino apunta a la raíz.
> - **Kruskal:** recorre aristas por costo; acepta si `FIND(u) ≠ FIND(v)` y entonces hace `UNION(u, v)`.

---

## 10. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| `UNION(x, y)` enlaza $x$ con $y$ directamente. | Enlaza las **raíces** de sus árboles; enlazar nodos internos rompería la estructura. |
| La unión ponderada compara alturas exactas. | Compara tamaños (o rangos); con compresión, las alturas exactas ya no se conocen y no hace falta. |
| La compresión de caminos debe actualizar `size`. | El tamaño solo importa en las raíces y no cambia al comprimir. |
| $O(m\,\alpha(n))$ significa que **cada** operación cuesta $O(\alpha(n))$. | Es una cota **amortizada**: una operación aislada puede costar $O(\log n)$. |
| Union-Find permite separar conjuntos. | Solo une; borrar aristas (conectividad totalmente dinámica) es un problema mucho más difícil. |
| Kruskal sin Union-Find sigue siendo $O(m\log m)$. | Detectar ciclos con BFS/DFS en cada paso lo lleva a $O(m\,n)$. |

---

## 11. Preguntas de autoevaluación

1. ¿Por qué quick-find tiene altura $1$ si lo dibujamos como bosque?
2. Da una secuencia de uniones que fuerce altura $n-1$ en quick-union.
3. En el lema de la altura, ¿dónde se usa que se cuelga el árbol **menor**?
4. Con unión ponderada y $n=1000$, ¿cuál es la mayor profundidad posible?
5. ¿Por qué la compresión de caminos no afecta la corrección de la unión por tamaño?
6. Si las aristas ya vienen ordenadas, ¿cuánto cuesta Kruskal con unión ponderada y compresión?
7. ¿Cómo usarías Union-Find para contar las componentes conexas de un grafo leyendo sus aristas una sola vez?

<details>
<summary>Respuestas breves</summary>

1. Cada elemento apunta directamente a su representante.
2. $U(1,2), U(2,3),\dots,U(n-1,n)$ con la regla “raíz de $x$ cuelga de raíz de $y$”.
3. Para garantizar que cuando $x$ baja un nivel, su árbol al menos duplica su tamaño.
4. $\lfloor\log_2 1000\rfloor=9$.
5. El tamaño de un árbol depende de **qué** nodos contiene, no de su forma; comprimir no cambia los conjuntos.
6. $O(m\,\alpha(n))$, prácticamente lineal.
7. Empezar con $n$ componentes, hacer `UNION` por cada arista y restar $1$ cada vez que las raíces sean distintas: $O(m\,\alpha(n))$.

</details>

---

## Aplicación adicional de las diapositivas: percolación (44–57)

**Pregunta:** en una cuadrícula $L\times L$, ¿existe un camino de casillas **abiertas** desde la fila superior hasta la inferior? Solo se permite caminar en las cuatro direcciones; una casilla diagonal no cuenta como vecina. Este es otro problema de conectividad que cambia por **inserciones**: al abrir una casilla pueden fusionarse componentes, pero ninguna se separa.

### Modelar la cuadrícula con Union-Find

1. Numera la casilla $(r,c)$ como $rL+c$, con $0\le r,c<L$. Reserva los índices $L^2$ y $L^2+1$ para dos nodos virtuales: **arriba** y **abajo**.
2. Al abrir $(r,c)$, márcala como abierta. Únela solo con sus vecinos ortogonales que **ya estén abiertos**. Si está en la primera fila, únela con **arriba**; si está en la última, con **abajo**.
3. Después de cada apertura, la cuadrícula percola exactamente cuando `find(arriba) == find(abajo)`.

**Ejemplo $3\times3$.** Abre $(0,1)$, luego $(1,1)$ y por último $(2,1)$. Tras la primera apertura, arriba está conectado con la casilla $1$, pero no con abajo. La segunda une $1$ con $4$. La tercera une $4$ con $7$ y $7$ con el nodo virtual de abajo. Ahora existe el camino vertical $1\leftrightarrow4\leftrightarrow7$ y la consulta devuelve **sí**. Si $(1,1)$ permaneciera bloqueada, las otras dos casillas no bastarían.

> [!important] ¿Por qué sirven los nodos virtuales?
> Sin ellos habría que buscar si **alguna** casilla abierta de arriba está conectada con **alguna** de abajo. Los dos nodos convierten esa condición en **una sola consulta** `connected(arriba, abajo)`. No deben conectarse por adelantado a casillas bloqueadas: eso produciría caminos falsos.

Con $L^2$ aperturas como máximo y a lo sumo cuatro uniones por apertura, una prueba completa cuesta $O(L^2\alpha(L^2))$ con unión ponderada y compresión, más el costo de elegir las casillas. Para estimar el **umbral de percolación** de las diapositivas, se abren casillas en orden aleatorio hasta que aparece el primer camino, se registra la fracción abierta y se promedian muchas pruebas. Para la red cuadrada grande, las diapositivas sitúan el umbral cerca de $0.593$; en una cuadrícula pequeña la fracción observada cambia de una prueba a otra.

> [!note] Dos consultas distintas
> `connected(arriba, abajo)` responde si **el sistema percola**. Si además se pregunta si una casilla individual está conectada con arriba (*fullness*), el nodo virtual de abajo puede causar **backwash** tras la primera percolación: casillas inferiores abiertas parecen conectadas con arriba por la vía del nodo de abajo. Para esa consulta adicional se usa un segundo Union-Find **sin** el nodo virtual inferior. La consulta de percolación anterior sigue siendo correcta.

<iframe src="percolacion-union-find.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

En el laboratorio, abre casillas y observa cuándo aparece un camino azul entre los extremos. Las casillas cerradas no participan en `UNION`.

---

## Cierre de las dos presentaciones: la estructura detrás de Kruskal

La secuencia de estudio queda cerrada aquí: [[2026-09-29 ADA - Contunuacion-scheduling|Dijkstra]] → [[2026-10-06 ADA - codigos-de-prefijos|cortes, ciclos y MST]] → [[2026-10-08 ADA - arboles-binarios-y-codigos-optimos|Prim y Kruskal]] → [[2026-10-13 ADA - algoritmo-de-huffman|Borůvka]] → [[2026-10-20 ADA - bienary heap y heap sort|clustering y arborescencias]] → **Union-Find**. Las arborescencias son dirigidas y requieren la contracción de ciclos de Edmonds; Union-Find resuelve otra necesidad: saber si los extremos de una arista **no dirigida** ya están conectados mientras Kruskal construye su bosque.

![[union-find-kruskal.svg]]

En la figura, las raíces de dos árboles codifican dos componentes. `find(u)≠find(v)` significa que añadir $(u,v)$ no forma ciclo; después de aceptarla, `union(u,v)` fusiona las componentes. La ruta interna de cada árbol puede cambiar por compresión de caminos sin cambiar la partición que representa.

> [!example] Ejercicio final tipo examen (10 puntos)
> Considera $V=\{1,2,3,4,5\}$ y aristas ya ordenadas $12:1,23:2,13:3,34:4,45:5,25:6$. Usa unión por tamaño, desempata a favor de la raíz numéricamente menor y compresión completa. **(a)** Traza Kruskal indicando para cada arista las raíces consultadas, si se acepta y el arreglo `parent` después de la operación. **(b)** Da el MST y su costo. **(c)** Explica por qué la arista $13$ se rechaza por una propiedad de ciclos y por qué $34$ se acepta por una propiedad de cortes. **(d)** Da el costo asintótico con y sin ordenar las aristas.
>
> <details><summary>Comprobación</summary>
>
> Se aceptan $12,23,34,45$ y se rechazan $13,25$; costo $12$. Con la convención indicada, después de las cuatro uniones efectivas todos los padres pueden apuntar a $1$ (en esta secuencia lo hacen tras consultar/comprimir). $13$ cierra el ciclo $1-2-3-1$ y es una arista máxima de él. $34$ es la menor arista del corte de la componente $\{1,2,3\}$ en ese momento. Si ya están ordenadas, $O(m\alpha(n)+n)$; si no, $O(m\log m+m\alpha(n)+n)$.
>
> </details>

---

## Conexiones

- **Clase anterior:** [[2026-10-20 ADA - bienary heap y heap sort|heap binario y heapsort]], la otra estructura de la unidad.
- **Componentes conexas estáticas:** [[2026-09-03 ADA - grafos|BFS/DFS en grafos]].
- **Gemelo voraz con heap:** [[2026-09-29 ADA - Contunuacion-scheduling|Dijkstra (§8)]]; Prim tiene casi el mismo código.
- **Contracción de componentes:** idea relacionada con la [[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas|condensación de SCC]] y con Borůvka (diapositivas 50–54).
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].
- **Recurso interactivo:** [[union-find-interactivo.htm|Union-Find interactivo]].
- **Otra aplicación:** [[percolacion-union-find.htm|percolación interactiva]].

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, secciones 4.5 (MST, Kruskal) y 4.6 (estructura Union-Find).
2. Wayne, K. (2020). *Greedy Algorithms II* (`04GreedyAlgorithmsII.pdf`), diapositivas 46–47, 57 y 64.
3. Galler, B. A. y Fischer, M. J. (1964). “An Improved Equivalence Algorithm”. *Communications of the ACM*, 7(5), 301–303.
4. Hopcroft, J. E. y Ullman, J. D. (1973). “Set Merging Algorithms”. *SIAM Journal on Computing*, 2(4), 294–303.
5. Tarjan, R. E. (1975). “Efficiency of a Good but Not Linear Set Union Algorithm”. *Journal of the ACM*, 22(2), 215–225.
6. Fredman, M. L. y Saks, M. E. (1989). “The Cell Probe Complexity of Dynamic Data Structures”. *Proceedings of STOC ’89*, 345–354.
7. Kruskal, J. B. (1956). “On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem”. *Proceedings of the AMS*, 7(1), 48–50.
8. Sedgewick, R. y Wayne, K. *Algorithms, 4th Edition*, presentación **1.5 Union-Find** (`15UnionFind.pdf`), diapositivas 4–57.

## Resumen después de clase

Union-Find mantiene una partición que solo crece por uniones y responde si dos elementos están en el mismo conjunto. Quick-find hace `FIND` en $O(1)$ a costa de uniones de $O(n)$; quick-union hace uniones baratas pero puede degenerar en cadenas. La unión ponderada cuelga el árbol menor del mayor y acota la altura por $\log_2 n$, porque cada vez que un nodo baja, su árbol se duplica. Con compresión de caminos, $m$ operaciones cuestan $O(m\,\alpha(n))$, prácticamente lineal y asintóticamente óptimo. Su aplicación central en el curso es Kruskal: ordenar aristas y aceptar cada una si `FIND(u) ≠ FIND(v)`, en $O(m\log m)$.

## Acciones adicionales

- [ ] Confirmar la regla de desempate y si el profesor usó tamaño o rango.
- [ ] Demostrar que un árbol de rango $k$ tiene al menos $2^k$ nodos.
- [ ] Ejecutar Kruskal a mano en el grafo de la diapositiva 32 (MST de costo 50) usando unión ponderada.
- [ ] Implementar Union-Find con compresión y resolver “contar componentes” sobre un grafo de prueba.
