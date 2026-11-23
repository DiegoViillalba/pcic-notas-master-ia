---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-13"
unidad: Algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Algoritmo de Huffman
  - Código de Huffman
  - Cola de prioridad
  - Reducción a un subproblema
  - Argumento de intercambio
referencias:
  - "[[2026-10-08 ADA - arboles-binarios-y-codigos-optimos]]"
  - "[[05CodigosHuffman.pdf]], páginas 21–25"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 49–57 (complemento de estudio)"
  - "Kleinberg y Tardos, Algorithm Design, sección 4.8 (pp. 171–177), enunciados (4.32)–(4.33)"
tags:
  - clase
  - algoritmos
  - greedy
  - huffman
  - cola-de-prioridad
  - compresion
  - strandbeest
---

# Clase 15 · El algoritmo de Huffman

![[05CodigosHuffman.pdf]]

> [!info] Alcance de la sesión
> Con el corolario de la [[2026-10-08 ADA - arboles-binarios-y-codigos-optimos|clase anterior]] —existe un árbol óptimo en el que los dos símbolos menos frecuentes son hermanos— se construyó el **algoritmo de Huffman**: primero como recursión que reduce el alfabeto en un símbolo, después como ciclo con **cola de prioridad** en $O(|\Sigma|\log|\Sigma|)$. Se resolvió el ejemplo de la clase y se obtuvo $\operatorname{PBS}=2.23$. Al final, el profesor mencionó los **strandbeests** de Theo Jansen (§9).

> [!tip] Cobertura complementaria de *Greedy Algorithms II*
> Más abajo se desarrolla **Borůvka, contracción y cuello de botella (diapositivas 49–57)**, con prueba intuitiva, SVG, laboratorio cuando aporta una exploración útil y ejercicios tipo examen. Este bloque amplía la cobertura del material sin alterar el registro original de la sesión.

## Pregunta central

Sabemos que es seguro poner a los dos símbolos menos frecuentes como hermanos. ¿Cómo convertimos esa única decisión segura en un algoritmo completo, y cómo demostramos que el árbol que produce es óptimo?

> [!summary] Idea de la clase
> Se fusionan los dos símbolos menos frecuentes $x,y$ en un **nuevo símbolo** $\omega$ con $f_\omega=f_x+f_y$, se resuelve el problema para el alfabeto reducido y luego se “abre” $\omega$ en dos hojas: $x$ con `0` y $y$ con `1`. La identidad $\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_\omega$ hace que la optimalidad pase del problema pequeño al grande por inducción. Con un min-heap, cada fusión cuesta $O(\log|\Sigma|)$.

---

## 1. Idea principal: reducir el alfabeto

Sea $T^*$ un árbol óptimo para $\Sigma$ en el que $x,y$ —los de menor frecuencia— son hermanos. Si **borramos** las hojas $x,y$, su padre se vuelve hoja. Si a esa hoja le ponemos un nuevo símbolo $\omega$, obtenemos un árbol $U^*$ para

$$
\Sigma'=\Sigma-\{x,y\}\cup\{\omega\},\qquad f_\omega=f_x+f_y .
$$

```text
       T*  (para Σ)                    U*  (para Σ')
          ...                              ...
           •           ⟺                   ω
         0/ \1
         x   y
```

Observaciones de las notas:

- $\Sigma'$ tiene un símbolo menos que $\Sigma$.
- El nuevo símbolo tiene frecuencia $f_\omega=f_x+f_y$.
- **Tal vez $\omega$ no es de menor frecuencia** en $\Sigma'$: en el siguiente paso pueden fusionarse otros dos símbolos.

La flecha va en ambos sentidos: un árbol para $\Sigma'$ se convierte en uno para $\Sigma$ colgando $x,y$ debajo de $\omega$. La prueba de §5 muestra que esta traducción preserva la optimalidad.

> [!tip] Un tipo distinto de voracidad
> En intervalos o EDF la decisión voraz fijaba un elemento de la respuesta. Aquí la decisión **no dice dónde** quedarán $x$ y $y$ en el árbol final; solo los compromete a ser hermanos. Eso basta para transformar el problema en uno equivalente más pequeño. Kleinberg–Tardos lo describen como usar la regla voraz para **encoger** la instancia.

---

## 2. Algoritmo recursivo

```text
Alg. Huffman(Σ, f)
  if |Σ| = 2 then
      devolver un código γ en el que un símbolo tiene 0 y el otro 1
  else
      x, y = los dos símbolos de Σ con menor frecuencia
      Σ' = Σ − {x, y} ∪ {ω}
      ∀ z ≠ x, y:  f'_z = f_z ;   f'_ω = f_x + f_y
      γ' = Huffman(Σ', f')
      ∀ z ≠ x, y:  γ(z) = γ'(z)
      γ(x) = γ'(ω) · 0
      γ(y) = γ'(ω) · 1
      devolver γ
```

**Terminación:** cada llamada recursiva trabaja con un alfabeto de un símbolo menos, así que hay $|\Sigma|-2$ llamadas antes del caso base.

> [!note] Caso $|\Sigma|=1$
> El pseudocódigo supone $|\Sigma|\ge2$. Si solo hay un símbolo, cualquier palabra de un bit (por ejemplo `0`) sirve; en implementaciones reales conviene tratarlo aparte.

---

## 3. Ejemplo de la clase

Frecuencias: $f_a=.32$, $f_b=.25$, $f_c=.20$, $f_d=.18$, $f_e=.05$.

| Paso | Alfabeto actual (ordenado) | Se fusionan | Nuevo símbolo |
|---:|---|---|---|
| 1 | $e{:}.05,\ d{:}.18,\ c{:}.20,\ b{:}.25,\ a{:}.32$ | $e,d$ | $de{:}.23$ |
| 2 | $c{:}.20,\ de{:}.23,\ b{:}.25,\ a{:}.32$ | $c,de$ | $cde{:}.43$ |
| 3 | $b{:}.25,\ a{:}.32,\ cde{:}.43$ | $b,a$ | $ab{:}.57$ |
| 4 | $cde{:}.43,\ ab{:}.57$ | caso base | raíz |

Observa el paso 2: el símbolo fusionado $de$ (.23) **no** es el más pequeño, pero vuelve a entrar en la competencia y se fusiona con $c$.

Al “abrir” las fusiones se obtiene el árbol de las notas:

```text
                    •
              0  /     \  1
           ab:.57         cde:.43
          0/   \1        0/    \1
       a:.32  b:.25   c:.20    de:.23
                               0/   \1
                            d:.18   e:.05
```

| $x$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma_H(x)$ | `00` | `01` | `10` | `110` | `111` |
| $\operatorname{depth}(x)$ | 2 | 2 | 2 | 3 | 3 |

$$
\operatorname{PBS}=.32(2)+.25(2)+.20(2)+.18(3)+.05(3)=2.23 .
$$

Es el mismo valor que $\gamma'$ de la [[2026-10-06 ADA - codigos-de-prefijos|primera clase de Huffman]]: la respuesta a “¿es posible mejorarlo?” es **no**.

> [!note] Etiquetas 0/1
> Qué hijo recibe `0` y cuál `1` es arbitrario: intercambiar los dos hijos de cualquier nodo no cambia ninguna profundidad. Por eso puede haber varios códigos de Huffman distintos, todos con el mismo PBS.

---

## 4. Implementación con cola de prioridad

La versión recursiva repite una operación: **sacar los dos de menor frecuencia y meter su suma**. Esa es exactamente la interfaz de una cola de prioridad de mínimos.

```text
Alg. Huffman(Σ, f)
  Q = cola de prioridad vacía
  for each x ∈ Σ do
      x.freq = f_x
      x.left = x.right = NULL
      Q.insert(x, x.freq)
  while Q.size() > 1 do
      z = nuevo símbolo
      x = Q.extractMin()
      y = Q.extractMin()
      z.left = x
      z.right = y
      z.freq = x.freq + y.freq
      Q.insert(z, z.freq)
  endwhile
  return Q.extractMin()       // la raíz del árbol
```

- Cada símbolo es un **nodo** con tres propiedades: `freq`, `left`, `right`.
- **El código se obtiene del árbol creado:** un recorrido desde la raíz que agrega `0` al bajar por `left` y `1` al bajar por `right`.

```python
import heapq
from itertools import count

def huffman(frecuencias):
    # frecuencias: dict símbolo -> f_x
    contador = count()          # desempate estable en el heap
    Q = [(f, next(contador), (s, None, None)) for s, f in frecuencias.items()]
    heapq.heapify(Q)

    while len(Q) > 1:
        fx, _, x = heapq.heappop(Q)
        fy, _, y = heapq.heappop(Q)
        heapq.heappush(Q, (fx + fy, next(contador), (None, x, y)))

    raiz = Q[0][2]
    codigo = {}

    def recorrer(nodo, prefijo):
        simbolo, izq, der = nodo
        if simbolo is not None:
            codigo[simbolo] = prefijo or "0"
            return
        recorrer(izq, prefijo + "0")
        recorrer(der, prefijo + "1")

    recorrer(raiz, "")
    return codigo
```

### 4.1 Tiempo

Sea $k=|\Sigma|$.

| Parte | Costo |
|---|---:|
| Insertar los $k$ símbolos | $O(k\log k)$ (o $O(k)$ con *heapify*) |
| Iteraciones del `while` | $k-1=O(k)$ |
| Cada iteración: 2 `extractMin` + 1 `insert` | $O(\log k)$ |
| Recorrido para leer el código | $O(k)$ |
| **Total** | $\mathbf{O(k\log k)}$ |

$$
T(|\Sigma|)=O(|\Sigma|\log|\Sigma|).
$$

Sin cola de prioridad, buscar los dos mínimos con un barrido cuesta $O(k)$ por iteración y $O(k^2)$ en total.

> [!tip] Si las frecuencias ya vienen ordenadas
> Se puede bajar a $O(k)$ con **dos colas FIFO**: una con las hojas en orden creciente y otra con los nodos fusionados, que se generan en orden creciente. Los dos mínimos siempre están al frente de alguna de las dos colas.

---

## 5. Prueba de optimalidad

Esta parte sigue a Kleinberg–Tardos, enunciados (4.32) y (4.33). Completa el razonamiento de la idea principal (§1) con el corolario de la clase anterior.

### 5.1 Lema: relación entre $T$ y $T'$

Sea $T'$ el árbol para $\Sigma'$ y $T$ el árbol para $\Sigma$ que resulta de colgar $x,y$ bajo la hoja $\omega$. Entonces

$$
\boxed{\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_\omega}
$$

**Prueba.** Los símbolos $z\ne x,y$ tienen la misma profundidad en ambos árboles, y $\operatorname{depth}_T(x)=\operatorname{depth}_T(y)=1+\operatorname{depth}_{T'}(\omega)$:

$$
\begin{aligned}
\operatorname{PBS}(T)
&=f_x\operatorname{depth}_T(x)+f_y\operatorname{depth}_T(y)+\sum_{z\ne x,y}f_z\operatorname{depth}_T(z)\\
&=(f_x+f_y)\big(1+\operatorname{depth}_{T'}(\omega)\big)+\sum_{z\ne x,y}f_z\operatorname{depth}_{T'}(z)\\
&=f_\omega+\Big(f_\omega\operatorname{depth}_{T'}(\omega)+\sum_{z\ne x,y}f_z\operatorname{depth}_{T'}(z)\Big)\\
&=f_\omega+\operatorname{PBS}(T').\qquad\square
\end{aligned}
$$

En el ejemplo: el último árbol reducido con $\{a,b,c,de\}$ tiene $\operatorname{PBS}=2(.32+.25+.20+.23)=2.00$, y $2.00+f_{de}=2.00+.23=2.23$.

### 5.2 Teorema: Huffman es óptimo

> [!important] Teorema
> Para todo alfabeto $\Sigma$ con $|\Sigma|\ge2$, el código de Huffman tiene el mínimo $\operatorname{PBS}$ entre todos los códigos de prefijos.

**Prueba por inducción en $k=|\Sigma|$.**

**Base, $k=2$:** el algoritmo usa un bit por símbolo, $\operatorname{PBS}=1$, y ningún código de prefijos puede usar menos de un bit por símbolo.

**Paso inductivo.** Supongamos que Huffman es óptimo para alfabetos de tamaño $k-1$ y sea $|\Sigma|=k$. Sean $x,y$ los dos de menor frecuencia, $T'$ el árbol que Huffman produce para $\Sigma'$ (óptimo por hipótesis) y $T$ el árbol final.

Por contradicción, supongamos que existe $Z$ con $\operatorname{PBS}(Z)<\operatorname{PBS}(T)$. Por el corolario de la clase anterior, podemos tomar $Z$ con $x,y$ **hermanos**. Borramos $x,y$ de $Z$ y etiquetamos a su padre con $\omega$: obtenemos $Z'$ para $\Sigma'$. Por el lema anterior aplicado a $Z$ y $Z'$,

$$
\operatorname{PBS}(Z')=\operatorname{PBS}(Z)-f_\omega<\operatorname{PBS}(T)-f_\omega=\operatorname{PBS}(T').
$$

Eso contradice la optimalidad de $T'$ para $\Sigma'$. Por lo tanto $T$ es óptimo. $\square$

> [!summary] Estructura de la prueba
> 1. **Elección voraz segura:** existe un óptimo con $x,y$ hermanos (intercambio, clase anterior).
> 2. **Subestructura óptima:** con $x,y$ amarrados, el problema equivale a uno con un símbolo menos, y los costos difieren en la constante $f_\omega$.
> 3. **Inducción:** resolver bien el problema pequeño implica resolver bien el grande.
>
> Es la misma receta que verás en programación dinámica, pero aquí solo hay **un** subproblema y no hay que comparar alternativas.

---

## 6. Abajo hacia arriba vs. arriba hacia abajo

| | Shannon–Fano | Huffman |
|---|---|---|
| Dirección | De la raíz a las hojas | De las hojas a la raíz |
| Primera decisión | Dividir $\Sigma$ en dos mitades de frecuencia parecida | Fusionar los dos menos frecuentes |
| ¿Elección segura demostrada? | No | Sí (Lema 3 + identidad del PBS) |
| Ejemplo de clase | PBS 2.25 | PBS 2.23 |

---

## 7. Complemento: ¿qué tan bueno es 2.23?

En teoría de la información, la **entropía** de las frecuencias es

$$
H(f)=\sum_{x}f_x\log_2\frac1{f_x}.
$$

Para el ejemplo, $H\approx2.15$. Shannon demostró que **ningún** código de prefijos baja de $H$, y se sabe que Huffman cumple

$$
H(f)\le\operatorname{PBS}(\text{Huffman})<H(f)+1 .
$$

El hueco entre 2.15 y 2.23 existe porque las palabras deben tener un número **entero** de bits.

### 7.1 Límites del modelo (extensiones del libro)

- **Fracciones de bit:** si un símbolo tiene frecuencia altísima (una imagen casi toda blanca), un código de prefijos sigue gastando al menos un bit por símbolo. La *codificación aritmética* supera esa barrera.
- **Frecuencias que cambian:** si la primera mitad del texto solo usa $a,b$ y la segunda solo $c,d$, conviene **cambiar de código a mitad** del texto. Son los esquemas *adaptativos*.
- **En la práctica:** Huffman se usa como etapa final en formatos como DEFLATE (ZIP, gzip, PNG) y JPEG.

---

## 8. Laboratorio interactivo

El recurso ejecuta Huffman **paso a paso**: muestra la cola de prioridad, resalta los dos mínimos que se extraen, dibuja el bosque mientras se fusiona y al final compara el PBS con el código de longitud fija, Shannon–Fano y la entropía. Las frecuencias son editables.

<iframe src="huffman-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> 1. Meter todos los símbolos en un min-heap por frecuencia.
> 2. Mientras haya más de un nodo: sacar los dos mínimos, crear un padre con la suma y volverlo a meter.
> 3. Leer el código desde la raíz: `0` a la izquierda, `1` a la derecha.
> 4. En el ejemplo: $a=00$, $b=01$, $c=10$, $d=110$, $e=111$, con $\operatorname{PBS}=2.23$.

---

## 9. Comentario final de la clase: los strandbeests

Al cierre, el profesor habló de los **strandbeests** (“bestias de playa” en neerlandés), los robots no electrónicos que mencionó en clase:

- Son esculturas cinéticas enormes, creadas desde 1990 por el artista y físico neerlandés **Theo Jansen**.
- Se mueven **solo con energía del viento**, presión de aire y sistemas de articulaciones mecánicas.
- Están hechas de materiales cotidianos: tubos de PVC, cinchos, madera, velas de tela y cinta.
- Jansen usó **algoritmos evolutivos** para calcular las proporciones exactas de las longitudes de los tubos —los “números sagrados”— que convierten la rotación de un eje en una caminata suave y casi orgánica.
- A lo largo de décadas de “evolución” desarrollaron pies anchos para no hundirse en la arena, botellas con aire presurizado que funcionan como “músculos” en días sin viento y “sensores de agua” que detectan el mar para dar la vuelta.

> [!question] Para reflexionar
> Huffman y los strandbeests son dos formas muy distintas de diseñar con algoritmos. Huffman toma una decisión local con una **prueba** de que lleva al óptimo. Un algoritmo evolutivo explora muchas soluciones, conserva las mejores y las combina: no garantiza el óptimo, pero sirve cuando el espacio de diseño (aquí, las longitudes de las barras de un mecanismo) es demasiado complejo para un argumento de intercambio.

---

## 10. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| Huffman fusiona siempre el símbolo nuevo con el siguiente. | Fusiona los dos **mínimos actuales**; el nodo nuevo puede tardar en volver a elegirse. |
| El código de Huffman es único. | Los empates y la elección de `0`/`1` dan códigos distintos con el mismo PBS. |
| La complejidad es $O(n\log n)$ con $n$ = longitud del texto. | Es $O(k\log k)$ con $k=|\Sigma|$; contar frecuencias en el texto cuesta $O(n)$ aparte. |
| La prueba de optimalidad solo necesita el lema de los hermanos. | También necesita $\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_\omega$ y la inducción. |
| Huffman es la mejor compresión posible. | Es el mejor **código de prefijos símbolo a símbolo con frecuencias fijas**. |

---

## 11. Preguntas de autoevaluación

1. Ejecuta Huffman con $f_a=.4$, $f_b=.3$, $f_c=.2$, $f_d=.1$. ¿Qué PBS obtienes?
2. ¿Por qué la identidad $\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_\omega$ no depende de dónde esté $\omega$ en $T'$?
3. En la prueba del teorema, ¿dónde se usa que $x,y$ sean los de **menor** frecuencia?
4. ¿Cuántas operaciones de heap hace el algoritmo para $|\Sigma|=k$?
5. Con frecuencias uniformes y $|\Sigma|=8$, ¿qué árbol produce Huffman?
6. ¿Por qué un código de prefijos no puede alcanzar PBS menor a 1?

<details>
<summary>Respuestas breves</summary>

1. Fusiones: $c+d=.3$; luego $b$ (.3) con $cd$ (.3) $=.6$; luego $a$ con $bcd$. Profundidades: $a=1$, $b=2$, $c=d=3$. $\operatorname{PBS}=.4+.6+.6+.3=1.9$.
2. Porque $x,y$ quedan exactamente un nivel debajo de $\omega$, y el bit extra se paga con peso $f_x+f_y=f_\omega$, sin importar la profundidad de $\omega$.
3. Para aplicar el corolario: solo para los dos de menor frecuencia sabemos que existe un óptimo $Z$ donde son hermanos.
4. $k$ inserciones iniciales y $k-1$ iteraciones con $3$ operaciones: $O(k)$ operaciones de $O(\log k)$ cada una.
5. Un árbol binario perfecto de altura 3: todos los símbolos con 3 bits, PBS $=3$.
6. Cada palabra tiene al menos un bit (con $|\Sigma|\ge2$, la palabra vacía no sirve), así que $\sum f_x|\gamma(x)|\ge\sum f_x=1$.

</details>

---

## Puente de *Greedy Algorithms II*: Borůvka, contracción y cuello de botella (diapositivas 49–57)

Borůvka parte de $n$ componentes unitarias. En **cada fase**, cada componente elige su arista saliente de costo mínimo. Las aristas elegidas se agregan al bosque y se contraen las componentes resultantes. Cada una de estas elecciones aplica la regla azul; las elecciones duplicadas se añaden una sola vez. Para que la explicación simultánea sea sencilla, la presentación supone costos distintos. Con empates puede fijarse un orden total consistente sobre las aristas.

![Una fase de Borůvka contrae pares de componentes](boruvka-contraccion.svg)

**Por qué son pocas fases.** Cada componente elige una arista hacia otra, así que después de la fase toda componente nueva contiene al menos dos anteriores. Si había $q$ componentes, quedan a lo sumo $q/2$. Por tanto hay a lo sumo $\lceil\log_2 n\rceil$ fases. Se pueden encontrar las componentes y escanear todas las aristas en $O(m+n)$ por fase; el costo total es $O(m\log n)$ en un grafo conexo.

**Contracción en detalle.** Tras elegir un conjunto $F$ de aristas, calculamos las componentes de $(V,F)$ y asignamos a cada vértice un `id`. Recorremos cada arista $(u,v)$ del grafo original: si `id[u]=id[v]`, es un lazo y se descarta; en otro caso se convierte en arista entre supervértices. Si aparecen aristas paralelas, para MST basta conservar la más barata. Las diapositivas proponen ordenarlas por pares de IDs mediante radix sort para obtener contracción en $O(m+n)$ bajo el modelo de enteros acotados; con ordenamiento por comparación, la eliminación de paralelas puede costar $O(m\log m)$.

**Casos especializados de las diapositivas.** En grafos planares simples, $m=O(n)$ y la contracción conserva planaridad. Como cada fase reduce el número de supervértices al menos a la mitad, $n+n/2+n/4+\cdots=O(n)$. El híbrido Borůvka–Prim ejecuta aproximadamente $\log_2\log_2 n$ fases y luego Prim sobre el grafo contraído; la cota $O(m\log\log n)$ indicada en la presentación usa **heap de Fibonacci**, no el heap binario habitual. La diapositiva histórica recorre algoritmos MST más rápidos y plantea la pregunta de una cota lineal basada solo en comparaciones; esos hitos no se necesitan para probar la corrección de Borůvka.

**Árbol de cuello de botella mínimo.** Si el objetivo es minimizar $\max_{e\in T} c_e$ en vez de la suma, cualquier MST también es óptimo: si existiera un árbol cuyas aristas fueran todas menores que la mayor arista $b$ del MST, las aristas de costo $<b$ conectarían todo el grafo y Kruskal habría terminado sin tomar una arista de costo $b$. El recíproco falla: un árbol de cuello de botella mínimo puede tener suma mayor.

### Práctica tipo examen (8 puntos)

Con $V=\{a,b,c,d\}$ y aristas $ab:1,ac:4,bc:3,bd:5,cd:2$, **(a)** ejecuta una fase de Borůvka con desempate alfabético; muestra aristas elegidas y componentes tras contraer. **(b)** Justifica formalmente la reducción a la mitad de componentes. **(c)** Demuestra que todo MST es árbol de cuello de botella mínimo. **(d)** Da un ejemplo donde un árbol de cuello de botella mínimo no minimice la suma.

<details><summary>Comprobación</summary>

(a) $a$ y $b$ eligen $ab:1$; $c$ y $d$ eligen $cd:2$. Quedan $\{a,b\}$ y $\{c,d\}$. (b) Cada componente nueva contiene al menos dos componentes anteriores, porque toda componente eligió una arista saliente. (c) Usa el argumento del umbral $b$ del párrafo anterior. (d) En un triángulo de costos $2,2,3$, ambos árboles con aristas $\{2,2\}$ y $\{2,3\}$ tienen cuello de botella mínimo $2$ y $3$ respectivamente, así que **no** sirve como contraejemplo. Uno correcto: grafo de cuatro vértices con dos árboles generadores de costos $\{1,2,2\}$ y $\{2,2,2\}$ y sin árbol con cuello de botella menor que $2$; por ejemplo, ciclo $a-b:1,b-c:2,c-d:2,d-a:2$. El primer árbol suma $5$; el segundo suma $6$, y ambos tienen cuello $2$.

</details>

---

## Conexiones

- **Clase anterior:** [[2026-10-08 ADA - arboles-binarios-y-codigos-optimos|árboles binarios y estructura de los códigos óptimos]].
- **Planteamiento del problema:** [[2026-10-06 ADA - codigos-de-prefijos|códigos de prefijos y PBS]].
- **Misma estructura de cola de prioridad:** partición de intervalos en la [[2026-09-29 ADA - Contunuacion-scheduling|clase del 29 de septiembre]].
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].
- **Técnica futura relacionada:** [[Programación dinámica|programación dinámica]] (elección + subestructura óptima con varios subproblemas).
- **Recurso interactivo:** [[huffman-paso-a-paso.htm|Huffman paso a paso]].

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, sección 4.8, pp. 171–177: algoritmo, enunciados (4.32)–(4.33), implementación y extensiones.
2. Castañeda Rojano, A. *Códigos de Huffman* (notas manuscritas, `05CodigosHuffman.pdf`), pp. 21–25.
3. Huffman, D. A. (1952). “A Method for the Construction of Minimum-Redundancy Codes”. *Proceedings of the IRE*, 40(9), 1098–1101.
4. Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2009). *Introduction to Algorithms*, 3.ª ed. MIT Press, sección 16.3.
5. Jansen, T. (2007). *The Great Pretender*. 010 Publishers. Sobre los strandbeests.

## Resumen después de clase

El algoritmo de Huffman fusiona repetidamente los dos símbolos de menor frecuencia en uno nuevo cuya frecuencia es la suma, hasta que queda un solo árbol; el código se lee de la raíz a las hojas. Con un min-heap corre en $O(|\Sigma|\log|\Sigma|)$. Su optimalidad combina la elección voraz segura (existe un óptimo con los dos menores como hermanos) con la identidad $\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_\omega$, que permite inducir sobre el tamaño del alfabeto. En el ejemplo de clase obtiene $2.23$ bits por símbolo, el mínimo posible, frente a $3$ del código fijo y $2.25$ de Shannon–Fano.

## Acciones adicionales

- [ ] Ejecutar Huffman a mano sobre las frecuencias de las letras de una frase corta.
- [ ] Reescribir sin ver la nota la prueba por inducción del teorema.
- [ ] Implementar el decodificador recorriendo el árbol que produce `huffman()`.
- [ ] Ver un video de los strandbeests y pensar qué se optimiza al elegir las longitudes de las barras.
