---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-06"
unidad: Algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Código de longitud fija
  - Código de longitud variable
  - Código de prefijos
  - Promedio de bits por símbolo (PBS)
  - Código óptimo
referencias:
  - "[[2026-09-29 ADA - Contunuacion-scheduling]]"
  - "[[05CodigosHuffman.pdf]], páginas 1–10"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 21–41 (complemento de estudio)"
  - "Kleinberg y Tardos, Algorithm Design, sección 4.8 (pp. 161–166)"
tags:
  - clase
  - algoritmos
  - greedy
  - huffman
  - codigos-de-prefijos
  - compresion
---

# Clase 13 · Códigos de prefijos: el problema detrás de Huffman

![[05CodigosHuffman.pdf]]

> [!info] Alcance de la sesión
> Después de cerrar *Greedy Algorithms I* (intervalos, tardanza y caché) en la [[2026-09-29 ADA - Contunuacion-scheduling|clase del 29 de septiembre]], se abrió otro ejemplo voraz de la unidad: **códigos de Huffman** (sección 4.8 de Kleinberg–Tardos). Esta sesión **no** presenta todavía el algoritmo; plantea con cuidado el problema que resuelve: cómo representar texto con bits, por qué conviene usar longitudes variables, qué propiedad evita ambigüedades al decodificar y cómo se mide la calidad de un código.

> [!note] Cómo se repartió el material
> Las notas manuscritas de Huffman cubren las clases del 6, 8 y 13 de octubre. En estas notas se dividen así: **6 oct** → problema y códigos de prefijos (pp. 1–10); **8 oct** → árboles binarios y lemas estructurales (pp. 11–20); **13 oct** → algoritmo, implementación y optimalidad (pp. 21–25).

> [!tip] Cobertura complementaria de *Greedy Algorithms II*
> Más abajo se desarrolla **cortes, ciclos, MST y reglas roja/azul (diapositivas 21–41)**, con prueba intuitiva, SVG, laboratorio cuando aporta una exploración útil y ejercicios tipo examen. Este bloque amplía la cobertura del material sin alterar el registro original de la sesión.

## Pregunta central

Si cada símbolo de un texto se traduce a una cadena de bits, ¿cómo elegimos esas cadenas para que el texto codificado sea **lo más corto posible** y, al mismo tiempo, **pueda decodificarse sin ambigüedad**?

> [!summary] Idea de la clase
> Un código de longitud fija gasta los mismos bits en símbolos frecuentes y raros. Uno de longitud variable puede ahorrar bits dando cadenas cortas a lo frecuente, pero corre el riesgo de ser ambiguo. La **propiedad de prefijos** —ninguna palabra del código es prefijo de otra— garantiza una decodificación única y voraz, leyendo bit por bit. La calidad se mide con el **promedio de bits por símbolo** $\operatorname{PBS}(\gamma)=\sum_x f_x|\gamma(x)|$, y el problema del curso es minimizarlo.

---

## 1. Puente con lo anterior

Hasta ahora, cada problema voraz tenía una regla de orden (por fin, por inicio, por fecha límite, por uso más lejano) y una prueba de intercambio. Huffman sigue la misma lógica, pero con dos diferencias:

1. La solución no es un subconjunto ni un orden, sino una **estructura**: un árbol binario.
2. La decisión voraz no fija un elemento de la respuesta final; **reduce el problema** a uno más pequeño que se resuelve recursivamente.

Para llegar ahí primero hay que entender qué es un código y cómo se compara con otro.

---

## 2. Códigos de longitud fija

Sea $\Sigma$ un alfabeto. Un **código binario** es una función

$$
\gamma:\Sigma\to\{0,1\}^{*}
$$

que asigna a cada símbolo una secuencia de bits que lo representa. Un texto $x_1x_2\cdots x_n$ se codifica concatenando:

$$
\gamma(x_1)\,\gamma(x_2)\cdots\gamma(x_n).
$$

En un **código de longitud fija** todas las secuencias tienen la misma longitud $\ell$.

### 2.1 Ejemplo de la clase

| Símbolo | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| Código | `000` | `001` | `111` | `010` | `101` |

El texto `aabced` se codifica como

$$
\underbrace{000}_{a}\;\underbrace{000}_{a}\;\underbrace{001}_{b}\;\underbrace{111}_{c}\;\underbrace{101}_{e}\;\underbrace{010}_{d}.
$$

### 2.2 Costo

Si el texto tiene $n$ símbolos,

$$
\text{longitud del texto codificado}=n\cdot\ell .
$$

Con $|\Sigma|$ símbolos se necesitan al menos

$$
\ell=\lceil\log_2|\Sigma|\rceil
$$

bits, porque con $\ell$ bits solo hay $2^{\ell}$ cadenas distintas. Para cinco símbolos, $\ell=3$ (con dos bits solo hay cuatro cadenas).

> [!example] ASCII
> La tabla ASCII que se mostró en clase es un código de longitud fija: cada carácter ocupa 7 bits ($2^7=128$ símbolos, del 0 al 127). Decodificar es trivial: se corta el texto cada 7 bits.

**Ventaja:** decodificar es inmediato. **Desventaja:** ignora que unos símbolos aparecen mucho más que otros.

---

## 3. Códigos de longitud variable

En un **código de longitud variable** las secuencias pueden tener longitudes distintas. La intuición es la de Morse: dar cadenas cortas a lo frecuente y largas a lo raro.

El problema aparece al decodificar. Considera

$$
\gamma(a)=0,\qquad \gamma(b)=1,\qquad \gamma(c)=01.
$$

La cadena `01` puede leerse como $ab$ o como $c$. El código asigna cadenas distintas a símbolos distintos y aun así es **ambiguo**: no basta con que $\gamma$ sea inyectiva símbolo por símbolo.

### 3.1 Código de prefijos

Partamos de la siguiente definición:
> [!important] Definicion
> Una secuencia \(u\) es prefijo de otra secuencia \(v\) si \(v\) comienza exactamente con \(u\).
Por ejemplo:

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20320%2082%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20x%3D%2240%22%20y%3D%228%22%20width%3D%2248%22%20height%3D%2242%22%20rx%3D%227%22%20fill%3D%22%230F766E%22%20fill-opacity%3D%220.23%22%20stroke%3D%22%2314B8A6%22%20stroke-width%3D%221.5%22%2F%3E%3Ctext%20x%3D%2264%22%20y%3D%2235%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20fill%3D%22currentColor%22%3E0%3C%2Ftext%3E%3Crect%20x%3D%22100%22%20y%3D%228%22%20width%3D%2248%22%20height%3D%2242%22%20rx%3D%227%22%20fill%3D%22%2364748b%22%20fill-opacity%3D%220.13%22%20stroke%3D%22%2394A3B8%22%20stroke-width%3D%221.5%22%2F%3E%3Ctext%20x%3D%22124%22%20y%3D%2235%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20fill%3D%22currentColor%22%3E1%3C%2Ftext%3E%3Crect%20x%3D%22160%22%20y%3D%228%22%20width%3D%2248%22%20height%3D%2242%22%20rx%3D%227%22%20fill%3D%22%2364748b%22%20fill-opacity%3D%220.13%22%20stroke%3D%22%2394A3B8%22%20stroke-width%3D%221.5%22%2F%3E%3Ctext%20x%3D%22184%22%20y%3D%2235%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20fill%3D%22currentColor%22%3E1%3C%2Ftext%3E%3Crect%20x%3D%22220%22%20y%3D%228%22%20width%3D%2248%22%20height%3D%2242%22%20rx%3D%227%22%20fill%3D%22%2364748b%22%20fill-opacity%3D%220.13%22%20stroke%3D%22%2394A3B8%22%20stroke-width%3D%221.5%22%2F%3E%3Ctext%20x%3D%22244%22%20y%3D%2235%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20fill%3D%22currentColor%22%3E0%3C%2Ftext%3E%3Cpath%20d%3D%22M64%2052%20V64%20H119%22%20stroke%3D%22%2314B8A6%22%20stroke-width%3D%221.5%22%20fill%3D%22none%22%2F%3E%3Ctext%20x%3D%22125%22%20y%3D%2269%22%20font-size%3D%2212%22%20fill%3D%22%2314B8A6%22%3EPrefijo%3A%200%3C%2Ftext%3E%3C%2Fsvg%3E)
De lo anterior podemos afirmar que:

> [!important] Definición
> Un código $\gamma$ es **de prefijos** si para todo par de símbolos distintos $x\neq y$, la secuencia $\gamma(x)$ **no es prefijo** de $\gamma(y)$.

En el ejemplo ambiguo, $\gamma(a)=0$ es prefijo de $\gamma(c)=01$; por eso falla.

$$
\text{Propiedad de prefijos}\;\Longrightarrow\;\text{no hay ambigüedades al decodificar.}
$$

> [!note] Terminología
> En la literatura también se les llama *códigos libres de prefijos* o *códigos instantáneos*: cada símbolo se reconoce en el instante en que termina su última cifra, sin mirar bits futuros.

### 3.2 Código de prefijos de la clase

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma$ | `11` | `01` | `001` | `10` | `000` |

Ninguna cadena es prefijo de otra: las dos de longitud 2 que empiezan con `0` (`01`) no coinciden con el inicio `00` de `001` y `000`, y así sucesivamente.

El mismo texto `aabced` queda

$$
\underbrace{11}_{a}\;\underbrace{11}_{a}\;\underbrace{01}_{b}\;\underbrace{001}_{c}\;\underbrace{000}_{e}\;\underbrace{10}_{d}
$$

con 14 bits en lugar de 18.

---

## 4. Decodificación voraz

### 4.1 Algoritmo de la clase

**Notación:**

- $\alpha$: cadena de bits pendientes por decodificar.
- $\beta$: cadena temporal donde se acumulan los bits leídos.
- $\mathrm{dec}$: secuencia de símbolos ya decodificados.
- $\varepsilon$: cadena vacía (sin símbolos ni bits).
- $v$: siguiente bit leído de $\alpha$.
- $x$: símbolo del alfabeto original.
- $\gamma(x)$: palabra binaria asignada al símbolo $x$.
- $\cdot$: operación de concatenación (unir secuencias). 

```
Alg. Decodificar(α)
  β = ε, dec = ε

  while α ≠ ε
      quitar de α el primer bit v
      β = β · v

      if existe un símbolo x con γ(x) = β then
          dec = dec · x
          β = ε
  end while

  return dec
```

**Funcionamiento:** Se leen los bits de $\alpha$ uno por uno y se acumulan en $\beta$. Cuando $\beta$ coincide con una palabra código $\gamma(x)$, se agrega el símbolo $x$ a $\mathrm{dec}$ y se reinicia $\beta=\varepsilon$. El proceso termina cuando $\alpha=\varepsilon$.

**Importante:** El algoritmo supone un código de prefijos y una entrada válida, lo que garantiza que cada símbolo se identifica sin ambigüedad.

![[Pasted image 20261115190502.png]]



### 4.2 Traza

Decodificamos `11110100100010` con $\gamma$:

| Bits leídos en $\beta$ | ¿Es palabra? | Salida acumulada |
|---|---|---|
| `1` | no | — |
| `11` | sí, $a$ | $a$ |
| `1`, `11` | sí, $a$ | $aa$ |
| `0`, `01` | sí, $b$ | $aab$ |
| `0`, `00`, `001` | sí, $c$ | $aabc$ |
| `0`, `00`, `000` | sí, $e$ | $aabce$ |
| `1`, `10` | sí, $d$ | $aabced$ |

### 4.3 Corrección

La justificación de la clase fue: **por la propiedad de prefijos**. Escrito con más detalle:

> **Invariante.** Al inicio de cada iteración, `dec` es la decodificación de los bits ya consumidos que forman palabras completas, y $\beta$ es un prefijo (posiblemente vacío) de la palabra del siguiente símbolo.

Cuando $\beta=\gamma(x)$ para algún $x$, el siguiente símbolo **tiene que ser** $x$: si fuera otro $y$, entonces $\beta=\gamma(x)$ sería prefijo de $\gamma(y)$, lo cual la propiedad de prefijos prohíbe. Por ello cortar en ese punto es la única opción posible, y la decisión local —emitir en cuanto hay coincidencia— nunca se equivoca. Al agotar $\alpha$, el invariante asegura que `dec` es el texto original.

> [!tip] Conexión con greedy
> El decodificador es un algoritmo voraz en miniatura: toma una decisión irreversible (emitir $x$) en cuanto ve una coincidencia. La propiedad de prefijos es exactamente lo que vuelve **segura** esa elección.

### 4.4 Complejidad

Cada bit se procesa una vez. Si la consulta “¿existe $x$ con $\gamma(x)=\beta$?” se implementa recorriendo el árbol del código (tema de la siguiente clase), cada bit cuesta $O(1)$ y la decodificación es lineal en la longitud de $\alpha$.

---

## 5. Morse no es un código de prefijos

En Morse, `E` es `·` y `A` es `·−`; `T` es `−` y `M` es `−−`, `N` es `−·`, `K` es `−·−`… El código de `T` es prefijo de los de `B`, `C`, `D`, `G`, `K`, `M`, entre otros.

> [!warning] ¿Entonces cómo funciona Morse?
> Morse **no es** un código binario de prefijos. Se puede decodificar porque usa un tercer símbolo: la **pausa** entre letras (y otra más larga entre palabras). Sin pausas, `·−` sería ambiguo entre `A` y `ET`.

---

## 6. Medir un código: promedio de bits por símbolo

Supongamos un texto de $n$ símbolos, donde cada símbolo $x\in\Sigma$ aparece con frecuencia relativa $f_x$, cumpliendo:

$$  
0\leq f_x\leq 1,\qquad \sum_{x\in\Sigma}f_x=1.  
$$

El símbolo $x$ aparece $nf_x$ veces y cada aparición requiere $|\gamma(x)|$ bits, donde $\gamma(x)$ es su codificación binaria y $|\gamma(x)|$ su longitud. Por tanto, la **longitud total del texto codificado** es:

$$  
L(\gamma)=\sum_{x\in\Sigma}nf_x|\gamma(x)|=n\sum_{x\in\Sigma}f_x|\gamma(x)|.  
$$

Como $n$ es una constante positiva que no depende del código elegido, **minimizar la longitud total equivale a minimizar el promedio de bits por símbolo (PBS)**:

$$  
\boxed{\operatorname{PBS}(\gamma)=\sum_{x\in\Sigma}f_x|\gamma(x)|}  
$$

En Kleinberg–Tardos se denomina _average number of bits per letter_ ($\operatorname{ABL}$). También puede interpretarse como el valor esperado de $|\gamma(X)|$, donde $X$ es un símbolo seleccionado aleatoriamente según las frecuencias $f_x$.

### Ejemplo: comparación de dos códigos

Consideremos un texto de $n=100$ símbolos con alfabeto $\Sigma={a,b,c}$ y las siguientes frecuencias y códigos de prefijos:

|Símbolo|$f_x$|Apariciones|$\gamma_1$|$\gamma_2$|
|---|---|---|---|---|
|$a$|0.5|50|`0` (1 bit)|`00` (2 bits)|
|$b$|0.3|30|`10` (2 bits)|`01` (2 bits)|
|$c$|0.2|20|`11` (2 bits)|`1` (1 bit)|

La longitud total del texto utilizando cada código es:

$$  
L(\gamma_1)=50(1)+30(2)+20(2)=150\text{ bits}  
$$

$$  
L(\gamma_2)=50(2)+30(2)+20(1)=180\text{ bits}  
$$

Sin embargo, podemos comparar su eficiencia directamente mediante el promedio de bits por símbolo:

$$  
\operatorname{PBS}(\gamma_1)=0.5(1)+0.3(2)+0.2(2)=1.5  
$$

$$  
\operatorname{PBS}(\gamma_2)=0.5(2)+0.3(2)+0.2(1)=1.8  
$$

Observamos que $\operatorname{PBS}(\gamma_1)<\operatorname{PBS}(\gamma_2)$, por lo que $\gamma_1$ es más eficiente. Además, como $L(\gamma)=n\operatorname{PBS}(\gamma)$ y $n>0$ es constante:

$$  
\boxed{\underset{\gamma}{\arg\min}\ L(\gamma)=\underset{\gamma}{\arg\min}\ \operatorname{PBS}(\gamma)}  
$$

**Conclusión:** Para comparar códigos sobre un mismo texto, no necesitamos considerar explícitamente $n$, pues únicamente escala la longitud total sin modificar cuál código es mejor. En cambio, si queremos conocer el número total de bits necesarios para almacenar el texto, sí debemos multiplicar el promedio por $n$. Esta equivalencia permite formular el problema de compresión como la minimización de $\operatorname{PBS}(\gamma)$, objetivo del **algoritmo de Huffman**.

### 6.1 Ejemplo de la clase

| $x$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---:|---:|---:|---:|---:|
| $f_x$ | .32 | .25 | .20 | .18 | .05 |
| $\gamma(x)$ | `11` | `01` | `001` | `10` | `000` |
| $\lvert\gamma(x)\rvert$ | 2 | 2 | 3 | 2 | 3 |

$$
\operatorname{PBS}(\gamma)=.32(2)+.25(2)+.20(3)+.18(2)+.05(3)=2.25 .
$$

Es **mejor que el código de longitud fija**, que siempre usa $3$ bits por símbolo. En un texto de $1000$ símbolos: $3000$ bits frente a $2250$.

---

## 7. El problema del código óptimo

> [!important] Problema
> Dado un alfabeto $\Sigma$ y sus frecuencias $f$, obtener un **código de prefijos** $\gamma$ tal que
> $$
> \operatorname{PBS}(\gamma)=\sum_{x\in\Sigma}f_x|\gamma(x)|
> $$
> sea el mínimo posible.

El código $\gamma$ no es óptimo. Basta con otro código de prefijos:

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma'$ | `11` | `10` | `01` | `001` | `000` |

$$
\operatorname{PBS}(\gamma')=.32(2)+.25(2)+.20(2)+.18(3)+.05(3)=2.23 .
$$

La mejora viene de intercambiar los papeles de $c$ y $d$: en $\gamma$, el símbolo $c$ (frecuencia .20) tenía 3 bits y $d$ (frecuencia .18) solo 2. Darle la cadena corta al más frecuente ahorra $(3-2)(.20-.18)=.02$ bits por símbolo. Esa cuenta será, en la clase siguiente, un **argumento de intercambio**.

> [!question] Pregunta que quedó abierta
> **¿Es posible mejorar $\gamma'$?** Hay una cantidad exponencial de códigos de prefijos posibles; no podemos probarlos todos. Hace falta entender la estructura de los códigos óptimos.

---

## 8. Contexto histórico

Las notas muestran a tres personajes:

- **Claude Shannon**, fundador de la teoría de la información (1948).
- **Robert Fano**, profesor en el MIT. Junto con Shannon propuso un método *de arriba hacia abajo* para construir códigos de prefijos: partir el alfabeto en dos mitades de frecuencia lo más parecida posible y repetir en cada mitad. Funciona bien en la práctica, pero **no siempre es óptimo**.
- **David Huffman**, estudiante de Fano. En 1951 el curso le dio a elegir entre un examen final y un trabajo sobre encontrar el código binario más eficiente. Huffman encontró un método *de abajo hacia arriba* y demostró que es óptimo (publicado en 1952).

Kleinberg–Tardos usan esta historia para mostrar que la idea “natural” (dividir arriba) falla y la correcta (fusionar abajo) es voraz.

---

## 9. Laboratorio interactivo

El recurso permite codificar y decodificar con cada uno de los códigos de la clase —longitud fija, $\gamma$, $\gamma'$ y uno ambiguo—, seguir el buffer $\beta$ bit por bit y comparar el PBS al cambiar las frecuencias. Sus otras pestañas se usan en la [[2026-10-08 ADA - arboles-binarios-y-codigos-optimos|siguiente clase]].

<iframe src="codigos-prefijos-y-arboles.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Longitud fija:** cortar cada $\ell$ bits; costo $n\ell$.
> - **Prefijos:** acumular bits en $\beta$ hasta que coincidan con una palabra; emitir y reiniciar.
> - **Ambiguo:** con $a=0$, $b=1$, $c=01$, la cadena `01` admite dos lecturas.
> - **PBS:** multiplicar cada frecuencia por la longitud de su palabra y sumar.

---

## 10. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| Si cada símbolo recibe una cadena distinta, el código se decodifica sin ambigüedad. | Con longitudes variables no basta: `0`, `1`, `01` es ambiguo. |
| Morse es un código de prefijos. | No; depende de las pausas como tercer símbolo. |
| El PBS depende de la longitud del texto. | La longitud total es $n\cdot\operatorname{PBS}$; el PBS solo depende de $f$ y $\gamma$. |
| Un código de longitud variable siempre gana al de longitud fija. | Solo si las frecuencias están desbalanceadas; con frecuencias uniformes y $|\Sigma|=2^k$ el fijo ya es óptimo. |
| Lo óptimo es minimizar la palabra más larga. | El objetivo es el **promedio ponderado** por las frecuencias. |

---

## 11. Preguntas de autoevaluación

1. ¿Cuántos bits por símbolo necesita un código de longitud fija para un alfabeto de 27 símbolos?
2. Da un código de longitud variable con tres símbolos que sea ambiguo y explica la ambigüedad.
3. ¿Por qué la propiedad de prefijos hace segura la decisión de emitir un símbolo en cuanto $\beta$ coincide con una palabra?
4. Decodifica `0010111000` con $\gamma$ ($a=11$, $b=01$, $c=001$, $d=10$, $e=000$).
5. Con frecuencias $f_a=f_b=f_c=f_d=.25$, ¿qué PBS tiene el código de longitud fija de 2 bits? ¿Puede mejorarse?

<details>
<summary>Respuestas breves</summary>

1. $\lceil\log_2 27\rceil=5$ bits.
2. $a=0$, $b=1$, $c=01$: la cadena `01` puede ser $ab$ o $c$.
3. Si $\beta=\gamma(x)$ y el siguiente símbolo fuera $y\ne x$, entonces $\gamma(x)$ sería prefijo de $\gamma(y)$, lo cual está prohibido.
4. `001` → $c$, `01` → $b$, `11` → $a$, `000` → $e$: el texto es $cbae$.
5. PBS $=2$. No puede mejorarse: con cuatro símbolos equiprobables cualquier código de prefijos tiene PBS $\ge 2$.

</details>

---

## Puente de *Greedy Algorithms II*: cortes, ciclos y árboles generadores (diapositivas 21–41)

Este bloque complementa los códigos de prefijos con la teoría de árboles generadores mínimos (MST). Se conserva el tema original de la clase; la sección sirve para estudiar de forma continua el segundo conjunto de diapositivas antes de llegar a Union-Find.

### De un ciclo a un corte

Un **corte** es una partición $S,V\setminus S$ de todos los vértices; $S$ no necesita ser conexo. Su **cutset** son las aristas con un extremo en cada lado. En un ciclo cerrado, cada entrada a $S$ exige una salida: por eso un ciclo y un cutset se intersectan en un **número par** de aristas. En particular, no pueden compartir exactamente una.

Los cortes y ciclos modelan redes de comunicación, carreteras, cableado y conexiones entre objetos; también aparecen al construir agrupamientos e imágenes a partir de semejanza.

Un **árbol generador** de un grafo no dirigido y conexo toca todos los vértices, es conexo y no tiene ciclos. Son equivalentes: tener $n-1$ aristas y ser conexo; tener $n-1$ aristas y ser acíclico; perder conectividad al quitar cualquier arista; crear un ciclo al agregar cualquier arista ajena. Un MST minimiza la **suma** de costos de sus $n-1$ aristas.

![[mst-corte-ciclo.svg]]

**Dos intercambios fundamentales.** Agregar a un árbol una arista $e$ crea un único ciclo; quitar otra arista $f$ de ese ciclo vuelve a dar un árbol. Quitar $f$ de un árbol crea dos componentes; agregar cualquier arista $e$ que cruce ese corte vuelve a dar un árbol. En ambos casos, si $c(e)<c(f)$, el árbol original no era mínimo. La figura muestra ambos movimientos sobre el mismo grafo.

### Reglas roja y azul

- **Azul (corte):** en un cutset sin aristas ya azules, se puede elegir una arista de costo mínimo y declararla segura para algún MST.
- **Roja (ciclo):** en un ciclo sin aristas ya rojas, se puede descartar una arista de costo máximo sin perder todos los MST posibles.

Con empates, “segura” significa que **existe** un MST compatible con la elección; una arista empatada no tiene por qué aparecer en **todos** los MST. El invariante común es: *existe un MST que contiene todas las aristas azules y ninguna roja*. Para añadir una azul que no está en ese MST, se incorpora, aparece un ciclo y se quita una arista del mismo ciclo que cruza el corte; su costo no es menor. Para marcar una roja que sí está en el MST, se quita, aparece un corte y se sustituye por otra arista del ciclo de costo no mayor. Así se conserva el invariante.

**Por qué termina.** Mientras haya una arista sin colorear, o sus extremos ya pertenecen al mismo bosque azul —forma un ciclo donde aplica la regla roja—, o pertenecen a árboles azules diferentes —el corte de uno permite la regla azul—. Al terminar, las azules son un MST.

> [!note] Transformar costos
> Sumar una constante $a$ a todas las aristas suma exactamente $(n-1)a$ al costo de **todo** árbol generador; multiplicar por $a>0$ también conserva el orden. Incluso aplicar $\log$ a cada costo positivo conserva **todos los MST**: es una transformación estrictamente creciente, deja igual el orden de las aristas y, por tanto, todas las decisiones posibles de Kruskal, incluidos los empates. Aunque $\sum\log c_e$ compare productos en lugar de sumas para árboles arbitrarios, la propiedad de corte garantiza que los mínimos globales coinciden. Esto contrasta con caminos mínimos: allí las rutas pueden tener distinto número de aristas y una transformación creciente no lineal puede cambiar la ruta óptima.

### Práctica tipo examen (8 puntos)

Sea $V=\{a,b,c,d\}$ y $E=\{ab:1,ac:4,bc:2,bd:5,cd:3\}$. **(a)** Para el corte $S=\{a,b\}$, escribe el cutset y su arista mínima. **(b)** En el ciclo $a-b-c-a$, marca una arista que la regla roja permite descartar. **(c)** Obtén el MST por intercambios y su costo. **(d)** Prueba en dos frases por qué ciclo y corte se intersectan un número par de veces. **(e)** Demuestra que aplicar $\log$ a todos los costos positivos sí preserva todos los MST, aunque la transformación no conserve el orden de las sumas de dos listas arbitrarias como $\{1,9\}$ y $\{4,4\}$.

<details><summary>Comprobación</summary>

(a) $\{ac:4,bc:2,bd:5\}$; mínima $bc:2$. (b) $ac:4$. (c) $\{ab:1,bc:2,cd:3\}$, costo $6$. (d) Cada cruce cambia de lado y un recorrido cerrado debe volver al lado inicial. (e) Kruskal procesa las aristas en el mismo orden porque $\log$ es estrictamente creciente; conserva también los empates, así que el conjunto de MST posibles no cambia. Las listas dadas muestran por qué no basta comparar sumas de dos árboles elegidos arbitrariamente: suman $10$ y $8$, mientras sus productos son $9$ y $16$. En un mismo grafo, ambas listas no pueden ser la prueba de que un MST deja de serlo bajo logaritmos.

</details>

---

## Conexiones

- **Clase anterior:** [[2026-09-29 ADA - Contunuacion-scheduling|Greedy: intervalos, tardanza y caché]].
- **Clase siguiente:** [[2026-10-08 ADA - arboles-binarios-y-codigos-optimos|árboles binarios y estructura de los códigos óptimos]].
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].
- **Recurso interactivo:** [[codigos-prefijos-y-arboles.htm|códigos de prefijos y árboles]].

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, sección 4.8, “Huffman Codes and Data Compression”, pp. 161–166.
2. Castañeda Rojano, A. *Códigos de Huffman* (notas manuscritas, `05CodigosHuffman.pdf`), pp. 1–10.
3. Huffman, D. A. (1952). “A Method for the Construction of Minimum-Redundancy Codes”. *Proceedings of the IRE*, 40(9), 1098–1101.

## Resumen después de clase

Un código asigna cadenas de bits a símbolos. El de longitud fija es simple pero desperdicia bits; el de longitud variable puede ahorrar, siempre que tenga la propiedad de prefijos, que permite decodificar de izquierda a derecha emitiendo un símbolo en cuanto su palabra aparece. La calidad de un código se mide con $\operatorname{PBS}(\gamma)=\sum f_x|\gamma(x)|$. En el ejemplo, el fijo cuesta 3, $\gamma$ cuesta 2.25 y $\gamma'$ cuesta 2.23; la pregunta abierta es cómo encontrar el mínimo sin probar todos los códigos.

## Acciones adicionales

- [ ] Escribir la invariante del decodificador sin consultar la nota.
- [ ] Construir un código de cuatro símbolos que sea de prefijos y otro que no lo sea.
- [ ] Calcular el PBS de $\gamma$ y $\gamma'$ con frecuencias uniformes y comparar.
