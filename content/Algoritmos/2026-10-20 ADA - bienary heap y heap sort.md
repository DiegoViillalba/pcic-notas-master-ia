---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-20"
unidad: Algoritmos voraces · estructuras de datos
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Cola de prioridad
  - Heap binario
  - Heapify-up y heapify-down
  - Construcción de un heap en tiempo lineal
  - Heapsort
referencias:
  - "[[2026-10-13 ADA - algoritmo-de-huffman]]"
  - "[[2026-09-29 ADA - Contunuacion-scheduling]], §8 (Dijkstra)"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 11–13 y 45, 58–83 (complemento de estudio)"
  - "Kleinberg y Tardos, Algorithm Design, sección 2.5"
  - "Cormen et al., Introduction to Algorithms, cap. 6"
tags:
  - clase
  - algoritmos
  - estructuras-de-datos
  - cola-de-prioridad
  - heap
  - heapsort
  - ordenamiento
---

# Clase 16 · Heap binario y heapsort

> [!info] Alcance de la sesión
> La clase introdujo el **heap binario** como implementación de una **cola de prioridad** y después lo transformó en un algoritmo de ordenamiento, **heapsort**. Es la estructura que ya usamos sin detallar en la [[2026-09-29 ADA - Contunuacion-scheduling|partición de intervalos]] y en [[2026-10-13 ADA - algoritmo-de-huffman|Huffman]], y la que fija el costo $O(m\log n)$ de [[2026-09-29 ADA - Contunuacion-scheduling|Dijkstra (§8 de la clase 12)]] y Prim.

> [!quote] Apuntes rápidos originales
> - En la clase comenzamos a hablar de un heap binario.
> - Posteriormente transformamos el heap binario a heap sort.

> [!warning] Nota reconstruida
> Los apuntes de clase eran breves; el desarrollo sigue Kleinberg–Tardos §2.5 (heap de **mínimos**, índices desde $1$) y CLRS cap. 6 (heapsort con heap de **máximos**). Conviene verificar contra el pizarrón qué convención usó el profesor; los argumentos son idénticos cambiando $\le$ por $\ge$.

> [!tip] Cobertura complementaria de *Greedy Algorithms II*
> Más abajo se desarrolla **clustering y arborescencias (diapositivas 58–83)**, con prueba intuitiva, SVG, laboratorio cuando aporta una exploración útil y ejercicios tipo examen. Este bloque amplía la cobertura del material sin alterar el registro original de la sesión.

## Pregunta central

¿Cómo mantenemos un conjunto que cambia —con inserciones y eliminaciones— de modo que siempre podamos obtener su mínimo rápidamente, y cómo convertimos esa estructura en un ordenamiento $O(n\log n)$ que no usa memoria adicional?

> [!summary] Idea de la clase
> Un heap es un árbol binario **casi completo** con **orden de heap**: cada padre es menor o igual que sus hijos. La forma casi completa garantiza altura $\lfloor\log_2 n\rfloor$ y permite guardarlo en un arreglo sin apuntadores; el orden de heap pone el mínimo en la raíz. Cada operación repara una sola violación subiendo (*heapify-up*) o bajando (*heapify-down*) por un camino raíz–hoja, en $O(\log n)$. Construir el heap de abajo hacia arriba cuesta solo $O(n)$, y extraer $n$ veces el máximo de un heap de máximos, dejando cada uno al final del arreglo, es **heapsort**: $O(n\log n)$ en el peor caso y en el lugar.

---

## 1. Motivación: la cola de prioridad

Una **cola de prioridad** mantiene un conjunto $S$ de elementos, cada uno con una **llave** numérica, y ofrece:

| Operación | Efecto |
|---|---|
| `insert(v, k)` | Agrega $v$ con llave $k$. |
| `find_min()` | Devuelve el elemento de menor llave sin quitarlo. |
| `extract_min()` | Quita y devuelve el elemento de menor llave. |
| `delete(v)` | Quita el elemento $v$. |
| `decrease_key(v, k)` | Baja la llave de $v$ a $k$. |

Ya la necesitamos varias veces en la unidad voraz:

- **Partición de intervalos:** aula que se libera antes (llave = fin de su última clase).
- **Huffman:** los dos símbolos de menor frecuencia.
- **Dijkstra / Prim:** nodo no explorado con menor $\pi[v]$; aquí además se usa `decrease_key`.

### 1.1 Implementaciones ingenuas

| Estructura | `insert` | `extract_min` |
|---|---:|---:|
| Lista no ordenada | $O(1)$ | $O(n)$ |
| Lista ordenada | $O(n)$ | $O(1)$ |
| **Heap binario** | $O(\log n)$ | $O(\log n)$ |

> [!important] No se puede tener todo en $O(1)$
> Con una cola de prioridad podemos ordenar: insertar $n$ números y extraer el mínimo $n$ veces. Si ambas operaciones costaran $O(1)$ usando solo comparaciones, ordenaríamos en $O(n)$, contradiciendo la cota inferior $\Omega(n\log n)$ para ordenamientos por comparación. El heap equilibra: ambas en $O(\log n)$. Esa misma observación es la semilla de **heapsort**.

---

## 2. Definición de heap binario

Un **heap (de mínimos)** es un árbol binario que cumple dos propiedades:

1. **Forma:** es **casi completo**: todos los niveles están llenos salvo quizá el último, que se llena de izquierda a derecha.
2. **Orden de heap:** para todo nodo $i$ distinto de la raíz,
$$
\mathrm{llave}(\mathrm{padre}(i))\le\mathrm{llave}(i).
$$

**Consecuencias inmediatas.**

- Por transitividad, cada nodo es menor o igual que todo su subárbol; en particular, el **mínimo está en la raíz**.
- **Altura.** Un árbol casi completo de altura $h$ tiene entre $2^h$ y $2^{h+1}-1$ nodos, así que
$$
2^h\le n\;\Longrightarrow\;h=\lfloor\log_2 n\rfloor .
$$
- El orden de heap **no** ordena hermanos ni niveles: un heap no es un arreglo ordenado ni un árbol binario de búsqueda.

> [!note] Heap de máximos
> Invirtiendo la desigualdad ($\mathrm{llave}(\mathrm{padre})\ge\mathrm{llave}(\text{hijo})$) se obtiene un **heap de máximos**, con el máximo en la raíz. Heapsort en el lugar usa este.

---

## 3. Representación en arreglo

La forma casi completa permite guardar el árbol nivel por nivel en un arreglo $H[1..n]$, sin apuntadores:

$$
\mathrm{padre}(i)=\left\lfloor \tfrac{i}{2}\right\rfloor,\qquad
\mathrm{izq}(i)=2i,\qquad
\mathrm{der}(i)=2i+1 .
$$

Ejemplo: $H=[2,5,3,9,6,4,8]$.

```text
índice:   1  2  3  4  5  6  7
H:      [ 2, 5, 3, 9, 6, 4, 8 ]

               2            ← H[1]
            /     \
           5       3        ← H[2], H[3]
          / \     / \
         9   6   4   8      ← H[4..7]
```

Se verifica el orden: $2\le5,3$; $5\le9,6$; $3\le4,8$.

> [!tip] Con índices desde $0$
> En Python o C: $\mathrm{padre}(i)=\lfloor(i-1)/2\rfloor$, $\mathrm{izq}(i)=2i+1$, $\mathrm{der}(i)=2i+2$. El módulo `heapq` de Python usa esta convención.

---

## 4. Reparar el orden: *heapify-up* y *heapify-down*

Todas las operaciones modifican **una sola posición** y luego reparan el orden por un camino del árbol. Kleinberg–Tardos lo formalizan con la noción de “casi heap”.

### 4.1 *Heapify-up* (subir)

**Situación:** $H$ es un heap salvo que la llave de la posición $i$ es **demasiado pequeña** (puede ser menor que la de su padre).

```python
def heapify_up(H, i):
    while i > 1 and H[i // 2] > H[i]:
        H[i], H[i // 2] = H[i // 2], H[i]   # intercambiar con el padre
        i //= 2
```

**Corrección.** Invariante: el único par posiblemente violado es $(\mathrm{padre}(i), i)$. Al intercambiar, el antiguo padre baja a $i$ y es $\le$ que los hijos de $i$ (ya lo era antes); el valor pequeño sube y la única violación posible pasa a ser con su nuevo padre. El ciclo termina en la raíz o cuando el padre es menor.

**Costo:** a lo más un intercambio por nivel, $O(\log n)$.

### 4.2 *Heapify-down* (bajar)

**Situación:** $H$ es un heap salvo que la llave de la posición $i$ es **demasiado grande**.

```python
def heapify_down(H, i, n):
    while 2 * i <= n:
        j = 2 * i                               # hijo izquierdo
        if j + 1 <= n and H[j + 1] < H[j]:
            j += 1                              # el hijo menor
        if H[i] <= H[j]:
            break
        H[i], H[j] = H[j], H[i]
        i = j
```

Hay que intercambiar con el **menor** de los hijos: así el que sube es menor o igual que su hermano y el orden se conserva en ese lado. **Costo:** $O(\log n)$, con dos comparaciones por nivel.

### 4.3 Las operaciones

| Operación | Implementación | Costo |
|---|---|---:|
| `find_min` | Devolver $H[1]$ | $O(1)$ |
| `insert(k)` | Poner $k$ en $H[n+1]$; `heapify_up(n+1)` | $O(\log n)$ |
| `extract_min` | Guardar $H[1]$; mover $H[n]$ a la raíz; `heapify_down(1)` | $O(\log n)$ |
| `delete(i)` | Mover $H[n]$ a la posición $i$; subir **o** bajar según convenga | $O(\log n)$ |
| `decrease_key(v, k)` | Cambiar la llave en `pos[v]`; `heapify_up` | $O(\log n)$ |

> [!important] `decrease_key` necesita un arreglo de posiciones
> Para bajar la llave del **nodo $v$** (Dijkstra, Prim), hay que saber dónde está $v$ dentro del heap. Se mantiene un arreglo auxiliar `pos[v]` que se actualiza en cada intercambio. Sin él, encontrar $v$ costaría $O(n)$.

### 4.4 Ejemplo

**Insertar 1** en $[2,5,3,9,6,4,8]$: se coloca en la posición $8$ y sube.

| Paso | Comparación | Arreglo |
|---|---|---|
| Colocar | — | $[2,5,3,9,6,4,8,\mathbf{1}]$ |
| $8\to4$ | $9>1$, intercambiar | $[2,5,3,\mathbf{1},6,4,8,9]$ |
| $4\to2$ | $5>1$, intercambiar | $[2,\mathbf{1},3,5,6,4,8,9]$ |
| $2\to1$ | $2>1$, intercambiar | $[\mathbf{1},2,3,5,6,4,8,9]$ |

**Extraer el mínimo** del resultado: se devuelve $1$, el último ($9$) pasa a la raíz y baja.

| Paso | Hijo menor | Arreglo |
|---|---|---|
| Mover $9$ a la raíz | — | $[\mathbf{9},2,3,5,6,4,8]$ |
| Posición $1$ | $\min(2,3)=2$ | $[2,\mathbf{9},3,5,6,4,8]$ |
| Posición $2$ | $\min(5,6)=5$ | $[2,5,3,\mathbf{9},6,4,8]$ |
| Posición $4$ | sin hijos | fin |

Regresamos al heap original.

---

## 5. Construir un heap en tiempo lineal

Dado un arreglo arbitrario, ¿cómo lo convertimos en heap?

- **Ingenuo:** $n$ inserciones, $O(n\log n)$.
- **De abajo hacia arriba:** las hojas (posiciones $\lfloor n/2\rfloor+1,\dots,n$) ya son heaps de un elemento. Recorremos los nodos internos **de derecha a izquierda** aplicando `heapify_down`.

```python
def build_heap(H, n):
    for i in range(n // 2, 0, -1):
        heapify_down(H, i, n)
```

**Corrección.** Invariante: al iniciar la iteración $i$, cada posición $i+1,\dots,n$ es raíz de un heap. Cuando procesamos $i$, sus dos subárboles ya son heaps y solo la raíz $i$ puede ser demasiado grande: exactamente la situación de `heapify_down`.

**Costo $O(n)$.** Un nodo a altura $h$ cuesta $O(h)$ y hay a lo más $\lceil n/2^{h+1}\rceil$ nodos de altura $h$:

$$
\sum_{h=0}^{\lfloor\log_2 n\rfloor}\left\lceil\frac{n}{2^{h+1}}\right\rceil O(h)
=O\!\left(n\sum_{h\ge0}\frac{h}{2^{h}}\right)=O(2n)=O(n).
$$

> [!tip] Intuición
> La mitad de los nodos son hojas y no cuestan nada; un cuarto baja a lo más un nivel; un octavo, dos… Casi todos los nodos están cerca del fondo, donde `heapify_down` es barato. Con `heapify_up` sería al revés: los muchos nodos del fondo tendrían que subir mucho.

---

## 6. Heapsort

### 6.1 Del heap al ordenamiento

Con un heap de mínimos y un arreglo auxiliar bastaría extraer el mínimo $n$ veces. Para ordenar **en el lugar** de forma ascendente se usa un **heap de máximos**: el máximo extraído se coloca en la posición que el heap acaba de liberar, al final.

```python
def heapsort(A):                      # A[1..n]
    n = len(A) - 1
    build_max_heap(A, n)              # O(n)
    for fin in range(n, 1, -1):
        A[1], A[fin] = A[fin], A[1]   # el máximo va a su lugar definitivo
        max_heapify_down(A, 1, fin - 1)   # el heap se encoge en uno
```

**Invariante del ciclo:** $A[1..\mathit{fin}]$ es un heap de máximos con los $\mathit{fin}$ elementos más pequeños, y $A[\mathit{fin}+1..n]$ contiene los mayores **ya ordenados**.

> [!note] Heapsort es selección con una buena estructura
> Es el ordenamiento por **selección** —poner el máximo al final y repetir— donde encontrar el máximo cuesta $O(\log n)$ en vez de $O(n)$ gracias al heap.

### 6.2 Traza: $A=[5,2,9,1,7,3]$

**Construcción del heap de máximos** ($i=3,2,1$):

| $i$ | Acción | Arreglo |
|---:|---|---|
| 3 | $9\ge3$, sin cambio | $[5,2,9,1,7,3]$ |
| 2 | hijos $1,7$; intercambiar $2\leftrightarrow7$ | $[5,7,9,1,2,3]$ |
| 1 | hijos $7,9$; intercambiar $5\leftrightarrow9$; luego $5\ge3$ | $[9,7,5,1,2,3]$ |

**Extracciones** (la barra separa heap │ parte ordenada):

| Iteración | Intercambio raíz–final | Después de `heapify_down` |
|---:|---|---|
| 1 | $[3,7,5,1,2\mid 9]$ | $[7,3,5,1,2\mid 9]$ |
| 2 | $[2,3,5,1\mid 7,9]$ | $[5,3,2,1\mid 7,9]$ |
| 3 | $[1,3,2\mid 5,7,9]$ | $[3,1,2\mid 5,7,9]$ |
| 4 | $[2,1\mid 3,5,7,9]$ | $[2,1\mid 3,5,7,9]$ |
| 5 | $[1\mid 2,3,5,7,9]$ | — |

Resultado: $[1,2,3,5,7,9]$.

### 6.3 Análisis

$$
T(n)=\underbrace{O(n)}_{\text{construir}}+\underbrace{(n-1)\cdot O(\log n)}_{\text{extracciones}}=O(n\log n)
$$

en el **peor caso**, con $O(1)$ memoria extra. Como todo ordenamiento por comparaciones requiere $\Omega(n\log n)$ comparaciones, heapsort es **asintóticamente óptimo**.

| Algoritmo | Peor caso | Memoria extra | Estable |
|---|---:|---:|:---:|
| Inserción | $O(n^2)$ | $O(1)$ | Sí |
| Mergesort | $O(n\log n)$ | $O(n)$ | Sí |
| Quicksort | $O(n^2)$ (esperado $O(n\log n)$) | $O(\log n)$ pila | No |
| **Heapsort** | $O(n\log n)$ | $O(1)$ | No |

> [!warning] No es estable
> Los intercambios a larga distancia —raíz con el final— pueden invertir el orden relativo de llaves iguales. En la práctica suele ser más lento que quicksort por su mal uso de caché (saltos $i\to2i$), pero su garantía de peor caso lo hace útil, por ejemplo, como respaldo en *introsort*.

---

## 7. Variantes y conexión con la unidad voraz

- **Heap $d$-ario:** cada nodo tiene $d$ hijos; la altura baja a $\log_d n$. Subir cuesta $O(\log_d n)$, pero bajar cuesta $O(d\log_d n)$ porque hay que hallar el menor de $d$ hijos. Dijkstra hace hasta $m$ `decrease_key` (subidas) y solo $n$ `extract_min` (bajadas); con $d\approx m/n$ se obtiene $O(m\log_{m/n} n)$ (diapositiva 13).
- **Heap de Fibonacci:** `decrease_key` en $O(1)$ amortizado; Dijkstra y Prim en $O(m+n\log n)$.
- **Algoritmos voraces con heap:** partición de intervalos $O(n\log n)$, Huffman $O(k\log k)$, Dijkstra y Prim $O(m\log n)$. En todos, la regla voraz es “tomar el de menor llave”, y el heap la hace barata.

---

## 8. Laboratorio interactivo

<iframe src="heap-binario-y-heapsort.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Heap:** `insert` coloca el valor al final y lo sube mientras sea menor que su padre; `extract_min` mueve el último a la raíz y lo baja por el hijo menor.
> - **Construcción lineal:** `heapify_down` desde $\lfloor n/2\rfloor$ hasta $1$.
> - **Heapsort:** construir heap de máximos, intercambiar raíz y final, encoger el heap y bajar la nueva raíz.

---

## 9. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| Un heap está ordenado. | Solo cada camino raíz–hoja está ordenado; hermanos y niveles no. |
| Buscar un elemento en un heap cuesta $O(\log n)$. | Buscar un valor arbitrario cuesta $O(n)$; por eso `decrease_key` usa `pos[v]`. |
| Construir un heap requiere $O(n\log n)$. | La construcción de abajo hacia arriba es $O(n)$. |
| En `heapify_down` da igual con qué hijo intercambiar. | Debe ser con el **menor** (heap de mínimos); si no, se viola el orden con el hermano. |
| Heapsort es estable. | No lo es. |
| El mínimo de un heap de máximos está en el último nivel en una posición fija. | Está en alguna hoja, pero no se sabe cuál. |

---

## 10. Preguntas de autoevaluación

1. ¿Cuál es la altura de un heap con $n=100$ elementos?
2. En un heap con índices desde $1$, ¿quién es el padre de la posición $13$ y quiénes son los hijos de la $6$?
3. ¿Por qué `build_heap` recorre de $\lfloor n/2\rfloor$ hacia $1$ y no de $1$ hacia $\lfloor n/2\rfloor$?
4. ¿Es $[1,3,2,7,4,2,5]$ un heap de mínimos? ¿Y $[1,3,2,2,4,5,7]$?
5. ¿Por qué Dijkstra con heap binario cuesta $O(m\log n)$ y no $O(n\log n)$?
6. ¿Dónde puede estar el segundo menor elemento de un heap de mínimos?

<details>
<summary>Respuestas breves</summary>

1. $\lfloor\log_2 100\rfloor=6$.
2. Padre de $13$: $6$. Hijos de $6$: $12$ y $13$.
3. Porque `heapify_down(i)` exige que los subárboles de $i$ ya sean heaps; al ir de derecha a izquierda, los hijos se procesan antes que el padre.
4. El primero sí: cada padre es menor o igual que sus hijos ($3\le7,4$; $2\le2,5$). El segundo no: $3>2$ en la posición $4$.
5. Puede haber hasta $m$ `decrease_key`, cada una de $O(\log n)$, además de $n$ `extract_min`.
6. En la posición $2$ o $3$: es hijo de la raíz, porque todo elemento fuera de la raíz tiene un ancestro hijo de la raíz que es menor o igual que él.

</details>

---

## Puente de *Greedy Algorithms II*: clustering de enlace simple (diapositivas 58–64)

Queremos dividir $n$ objetos en exactamente $k$ grupos no vacíos. La presentación usa una distancia no negativa y simétrica con $d(p_i,p_j)=0$ solo si $i=j$; el argumento de Kruskal no necesita desigualdad triangular. La **separación** (*spacing*) de una partición es la menor distancia entre dos objetos ubicados en grupos distintos. Buscamos maximizar esa separación; el objetivo es diferente de minimizar el diámetro dentro de cada grupo.

El algoritmo de **enlace simple** es Kruskal detenido al quedar $k$ componentes: se unen repetidamente los dos grupos conectados por el par de objetos más cercano. Equivale a calcular un MST y quitarle sus $k-1$ aristas más caras. La siguiente arista que Kruskal **habría** aceptado al continuar determina la separación de los $k$ grupos. Los empates pueden producir particiones distintas con el mismo valor óptimo. El **dendrograma** registra las fusiones a distintos umbrales de distancia; las diapositivas muestran un ejemplo aplicado a perfiles de expresión genética de tumores.

![[clustering-mst.svg]]

**Prueba de optimalidad.** Sea $d^*$ la separación de la partición obtenida por Kruskal. Cualquier partición alternativa en $k$ grupos debe separar al menos dos vértices que nuestra solución dejó conectados por aristas de costo $\le d^*$; si no, todos nuestros $k$ grupos quedarían íntegros y la partición alternativa sería la misma. En el camino del MST entre esos dos vértices hay una arista que cruza grupos alternativos, de costo $\le d^*$. La separación alternativa no supera $d^*$.

### Laboratorio: variar $k$ y observar la separación

<iframe src="clustering-enlace-simple.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Mueve $k$: el bosque conserva las $n-k$ aristas más baratas que no cierran ciclos. El laboratorio resalta la siguiente conexión entre grupos, cuyo peso es la separación máxima lograda.

> [!example] Práctica tipo examen (6 puntos)
> Para puntos en una recta en posiciones $0,1,4,5,11$, encuentra por Kruskal la partición óptima para $k=2$ y $k=3$, su separación y las aristas que se quitan del MST. Justifica por qué el intervalo más largo no siempre coincide con “diámetro mínimo dentro de cada grupo”.
>
> <details><summary>Comprobación</summary>
>
> MST con aristas de longitudes $1,3,1,6$. Para $k=2$, quita la de longitud $6$: $\{0,1,4,5\}$ y $\{11\}$; separación $6$. Para $k=3$, quita además la de longitud $3$: $\{0,1\}$, $\{4,5\}$, $\{11\}$; separación $3$. La función objetivo compara pares **entre** grupos, no el diámetro máximo de un grupo.
>
> </details>

## Puente de *Greedy Algorithms II*: arborescencias de costo mínimo (diapositivas 65–83)

Una **arborescencia** con raíz $r$ es el análogo dirigido de un árbol generador: hay un camino dirigido único desde $r$ a cada vértice. Equivale a elegir exactamente una arista **entrante** para cada $v\ne r$ y ninguna para $r$, sin ciclos dirigidos. Su costo es la suma de las aristas elegidas. Antes de optimizar, verifica que todos los vértices sean alcanzables desde $r$; de lo contrario no existe arborescencia generadora. Si todos son alcanzables, un árbol de BFS o DFS dirigido desde $r$ da una arborescencia factible, aunque no necesariamente de costo mínimo. Tampoco tiene por qué ser un árbol de caminos mínimos: se minimiza la **suma de las aristas elegidas**, no la distancia individual a cada vértice.

Elegir la arista entrante más barata de cada vértice parece óptimo porque cada arborescencia necesita una por vértice. Si las elegidas **no** forman un ciclo, ya son óptimas: alcanzan simultáneamente todas las cotas inferiores. Si forman un ciclo, la decisión local es incompatible con tener caminos desde $r$ y hay que corregirla.

![[arborescencia-ciclo.svg]]

### Costos reducidos y contracción de Edmonds

Para cada $v\ne r$, sea $y(v)$ el costo mínimo de una arista entrante. Sustituimos cada costo entrante por $c'(u,v)=c(u,v)-y(v)\ge0$. Toda arborescencia contiene **una** arista entrante por cada $v\ne r$, así que su costo baja exactamente $\sum_{v\ne r}y(v)$: las soluciones óptimas no cambian. Las aristas inicialmente elegidas tienen costo reducido cero.

Si estas aristas cero forman un ciclo $C$, se contrae $C$ a un supervértice y se resuelve recursivamente el grafo menor, preservando el costo reducido de **cada arista entrante individual**. Es importante no reemplazar todas las entradas a $C$ por su costo original: la reducción de $y(v)$ depende del vértice de entrada. Al expandir, si la solución contraída entra a $C$ por $(a,b)$, se conservan todas las aristas cero del ciclo salvo la que entraba a $b$. Así queda exactamente una entrada a cada vértice del ciclo y se rompe el ciclo.

**Lema que justifica la contracción.** Existe un óptimo que entra a un ciclo de costo reducido cero exactamente una vez. Si un óptimo entra varias veces, conserva la primera entrada que aparece en una ruta desde $r$ hasta el ciclo, elimina las demás entradas y añade las aristas cero del ciclo salvo la que llega al vértice de esa primera entrada. El costo no aumenta y todos los vértices siguen alcanzables. Por inducción sobre el número de vértices, la solución contraída óptima se expande a una solución óptima original. Una implementación directa con hasta $n$ contracciones y trabajo $O(m)$ por etapa cuesta $O(mn)$; la diapositiva final registra una implementación más avanzada $O(m+n\log n)$.

**Ejemplo guiado.** Con $r\to A:5$, $r\to B:4$, $r\to C:8$, $A\to B:1$, $B\to C:1$, $C\to A:1$, las entradas más baratas forman el ciclo $A\to B\to C\to A$. Se resta $1$ a las entradas de cada vértice; al contraer, la mejor entrada desde $r$ es $r\to B$ de costo reducido $3$. Al expandir se quita $A\to B$ y queda $\{r\to B:4,B\to C:1,C\to A:1\}$, costo original $6$.

### Laboratorio: romper el ciclo sin perder optimalidad

<iframe src="arborescencias-edmonds.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Avanza desde las elecciones locales hasta la contracción y expansión. Cada etapa muestra qué arista entra al ciclo y cuál se retira; el costo reducido separa el precio inevitable de entrar a cada vértice del precio extra por conectarlo con la raíz.

### Práctica tipo examen (10 puntos)

Usa el ejemplo guiado. **(a)** Calcula $y(A),y(B),y(C)$ y los costos reducidos de las tres aristas desde $r$. **(b)** Explica por qué las tres aristas de costo $1$ no son una arborescencia. **(c)** Contrae el ciclo y elige la entrada óptima. **(d)** Expande y calcula costo. **(e)** Refuta la afirmación “un MST no dirigido del grafo subyacente siempre da una arborescencia mínima orientando sus aristas desde $r$”.

<details><summary>Comprobación</summary>

(a) $y(A)=y(B)=y(C)=1$; costos reducidos $4,3,7$. (b) Forman ciclo dirigido y no hay camino desde $r$. (c) Entra por $r\to B$. (d) Se retira $A\to B$, quedan $r\to B$, $B\to C$, $C\to A$; costo $6$. (e) Orientar un MST puede requerir aristas que no existen en ese sentido en el digrafo; además el criterio de corte para MST no controla la restricción de una entrada por vértice.

</details>

---

## Conexiones

- **Clase anterior:** [[2026-10-13 ADA - algoritmo-de-huffman|algoritmo de Huffman]], donde el heap da $O(k\log k)$.
- **Uso con `decrease_key`:** [[2026-09-29 ADA - Contunuacion-scheduling|Dijkstra (§8 de la clase 12)]], tabla de colas de prioridad (§8.7).
- **Siguiente clase:** [[2026-10-22 ADA - Uniond-Find Datatype|estructura Union-Find]], la otra estructura de datos que necesitan los algoritmos de árboles generadores mínimos.
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].
- **Recurso interactivo:** [[heap-binario-y-heapsort.htm|heap binario y heapsort]].

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, sección 2.5: colas de prioridad y heaps.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2009). *Introduction to Algorithms*, 3.ª ed. MIT Press, cap. 6: heapsort.
3. Wayne, K. (2020). *Greedy Algorithms II* (`04GreedyAlgorithmsII.pdf`), diapositivas 11–13 (colas de prioridad en Dijkstra) y 45 (Prim).
4. Williams, J. W. J. (1964). “Algorithm 232: Heapsort”. *Communications of the ACM*, 7(6), 347–348.
5. Floyd, R. W. (1964). “Algorithm 245: Treesort 3”. *Communications of the ACM*, 7(12), 701. Construcción del heap en tiempo lineal.

## Resumen después de clase

Un heap binario es un árbol casi completo con orden de heap: su forma da altura logarítmica y una representación compacta en arreglo, y su orden pone el mínimo en la raíz. Insertar, extraer el mínimo y bajar una llave reparan una única violación con `heapify_up` o `heapify_down` en $O(\log n)$, y construir el heap desde un arreglo cuesta $O(n)$. Heapsort combina ambas ideas: construye un heap de máximos y lo vacía hacia el final del propio arreglo, ordenando en $O(n\log n)$ en el peor caso sin memoria extra. Es la pieza que hace eficientes a los algoritmos voraces que siempre toman “el de menor llave”: partición de intervalos, Huffman, Dijkstra y Prim.

## Acciones adicionales

- [ ] Verificar en las fotos o el pizarrón si el profesor usó heap de mínimos o de máximos, e índices desde $0$ o $1$.
- [ ] Ejecutar a mano `build_heap` sobre $[9,4,7,1,8,2,6,3]$ y comprobar con el laboratorio.
- [ ] Demostrar que hay a lo más $\lceil n/2^{h+1}\rceil$ nodos de altura $h$.
- [ ] Implementar un heap con `pos[v]` y usarlo en la implementación de Dijkstra.
