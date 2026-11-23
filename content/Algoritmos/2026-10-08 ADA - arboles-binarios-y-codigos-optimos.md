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
> $$
> \operatorname{PBS}(T)=\sum_{x\in\Sigma}f_x\operatorname{depth}(x).
> $$
> En un árbol óptimo: **(1)** todo nodo interno tiene dos hijos; **(2)** más profundo implica menos frecuente; **(3)** existe un óptimo en el que los **dos símbolos menos frecuentes son hermanos**. Esta última propiedad es la elección voraz de Huffman.

---

## 1. De árboles binarios a códigos

Sea $T$ un árbol binario enraizado con $|\Sigma|$ hojas, cada una etiquetada con un símbolo distinto de $\Sigma$. Etiquetamos cada arista que va a un hijo izquierdo con `0` y cada arista a un hijo derecho con `1`. El código de $x$ es la secuencia de bits del camino de la raíz a la hoja de $x$.

### 1.1 Ejemplo de la clase

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20600%20350%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20stroke%3D%22currentColor%22%20stroke-width%3D%222.5%22%20fill%3D%22none%22%20stroke-linecap%3D%22round%22%3E%3Cpath%20d%3D%22M300%2045%20L170%20125%20M300%2045%20L430%20125%20M170%20125%20L100%20220%20M170%20125%20L240%20220%20M430%20125%20L365%20220%20M430%20125%20L510%20220%20M510%20220%20L460%20310%20M510%20220%20L560%20310%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22%230f766e%22%3E%3Ccircle%20cx%3D%22300%22%20cy%3D%2245%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22430%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22510%22%20cy%3D%22220%22%20r%3D%229%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2219%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22220%22%20y%3D%2277%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22380%22%20y%3D%2277%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22115%22%20y%3D%22163%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22222%22%20y%3D%22163%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22375%22%20y%3D%22163%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22488%22%20y%3D%22163%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22458%22%20y%3D%22262%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22552%22%20y%3D%22262%22%3E1%3C%2Ftext%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2223%22%20font-weight%3D%22600%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22100%22%20y%3D%22242%22%3Ea%3C%2Ftext%3E%3Ctext%20x%3D%22240%22%20y%3D%22242%22%3Ec%3C%2Ftext%3E%3Ctext%20x%3D%22365%22%20y%3D%22242%22%3Eb%3C%2Ftext%3E%3Ctext%20x%3D%22460%22%20y%3D%22337%22%3Ee%3C%2Ftext%3E%3Ctext%20x%3D%22560%22%20y%3D%22337%22%3Ed%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma'''$ | `00` | `10` | `01` | `111` | `110` |

### 1.2 Por qué el resultado es un código de prefijos

- **Unicidad:** los caminos a hojas distintas son distintos, así que cada símbolo recibe una palabra distinta.
- **Propiedad de prefijos:** ningún camino a una hoja está contenido en otro. Si $\gamma(x)$ fuera prefijo de $\gamma(y)$, el camino a $y$ pasaría por la hoja de $x$, pero una hoja no tiene descendientes.

### 1.3 Un árbol que desperdicia bits

El segundo árbol de las notas es

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20600%20350%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20stroke%3D%22currentColor%22%20stroke-width%3D%222.5%22%20fill%3D%22none%22%20stroke-linecap%3D%22round%22%3E%3Cpath%20d%3D%22M300%2040%20L170%20125%20M300%2040%20L430%20125%20M170%20125%20L95%20220%20M430%20125%20L350%20220%20M430%20125%20L515%20220%20M350%20220%20L290%20310%20M350%20220%20L400%20310%20M515%20220%20L475%20310%20M515%20220%20L565%20310%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22%230f766e%22%3E%3Ccircle%20cx%3D%22300%22%20cy%3D%2240%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22430%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22350%22%20cy%3D%22220%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22515%22%20cy%3D%22220%22%20r%3D%229%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2219%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22218%22%20y%3D%2275%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22385%22%20y%3D%2275%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22116%22%20y%3D%22165%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22375%22%20y%3D%22165%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22490%22%20y%3D%22165%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22298%22%20y%3D%22264%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22393%22%20y%3D%22264%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22468%22%20y%3D%22264%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22558%22%20y%3D%22264%22%3E1%3C%2Ftext%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2224%22%20font-weight%3D%22600%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%2295%22%20y%3D%22244%22%3Ed%3C%2Ftext%3E%3Ctext%20x%3D%22290%22%20y%3D%22337%22%3Ec%3C%2Ftext%3E%3Ctext%20x%3D%22400%22%20y%3D%22337%22%3Eb%3C%2Ftext%3E%3Ctext%20x%3D%22475%22%20y%3D%22337%22%3Ea%3C%2Ftext%3E%3Ctext%20x%3D%22565%22%20y%3D%22337%22%3Ee%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

| $\Sigma$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\gamma^{iv}$ | `110` | `101` | `100` | `00` | `111` |

También es un código de prefijos válido, pero el hijo izquierdo de la raíz tiene **un solo hijo**. El bit que lleva a $d$ después del primer `0` no distingue nada: $d$ podría codificarse con `0`. Esta observación es el primer lema (§4).

---

## 2. De códigos a árboles binarios

En sentido inverso, se construye $T$ **inductivamente leyendo los bits uno a uno**: `0` → bajar a la izquierda, `1` → bajar a la derecha (creando nodos cuando no existan). Al terminar la palabra de $x$, el nodo alcanzado es la hoja de $x$.

Para $\gamma$ ($a=11$, $b=01$, $c=001$, $d=10$, $e=000$), en la raíz se separan $\{b,c,e\}$ (empiezan con `0`) de $\{a,d\}$ (empiezan con `1`). Del lado `0`: $\{c,e\}$ siguen con `0` y $b$ con `1`. Y así:

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20600%20360%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20stroke%3D%22currentColor%22%20stroke-width%3D%222.5%22%20fill%3D%22none%22%20stroke-linecap%3D%22round%22%3E%3Cpath%20d%3D%22M300%2040%20L175%20125%20M300%2040%20L435%20125%20M175%20125%20L100%20225%20M175%20125%20L255%20225%20M435%20125%20L375%20225%20M435%20125%20L515%20225%20M100%20225%20L55%20320%20M100%20225%20L145%20320%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22%230f766e%22%3E%3Ccircle%20cx%3D%22300%22%20cy%3D%2240%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22175%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22435%22%20cy%3D%22125%22%20r%3D%229%22%2F%3E%3Ccircle%20cx%3D%22100%22%20cy%3D%22225%22%20r%3D%229%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2219%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22217%22%20y%3D%2277%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22385%22%20y%3D%2277%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22115%22%20y%3D%22163%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22230%22%20y%3D%22163%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22382%22%20y%3D%22163%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22490%22%20y%3D%22163%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%2261%22%20y%3D%22267%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22141%22%20y%3D%22267%22%3E1%3C%2Ftext%3E%3C%2Fg%3E%3Cg%20fill%3D%22currentColor%22%20font-size%3D%2224%22%20font-weight%3D%22600%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22255%22%20y%3D%22247%22%3Eb%3C%2Ftext%3E%3Ctext%20x%3D%22375%22%20y%3D%22247%22%3Ed%3C%2Ftext%3E%3Ctext%20x%3D%22515%22%20y%3D%22247%22%3Ea%3C%2Ftext%3E%3Ctext%20x%3D%2255%22%20y%3D%22344%22%3Ee%3C%2Ftext%3E%3Ctext%20x%3D%22145%22%20y%3D%22344%22%3Ec%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

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

**Lema.** El árbol binario de un código de prefijos óptimo puede elegirse **completo**, es decir, cada nodo interno tiene exactamente dos hijos.

En inglés se denomina _full binary tree_. No debe confundirse con un árbol completo en el sentido de los _heaps_, donde todos los niveles están llenos excepto, posiblemente, el último.

### Intuición: ¿por qué un nodo con un solo hijo es ineficiente?

Recordemos que cada camino desde la raíz hasta una hoja representa una palabra código: recorrer una arista añade un bit (`0` o `1`). Por tanto, **la profundidad de una hoja determina la cantidad de bits necesarios para codificar su símbolo**.

Si un nodo interno tiene un único hijo, estamos utilizando un bit adicional sin que exista una bifurcación que permita distinguir entre dos posibilidades. Podemos eliminar ese nodo y conectar directamente su hijo con el padre, acortando las palabras código de todas las hojas que descienden de él.

**Ejemplo.** Consideremos el siguiente fragmento de un árbol:

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20480%20420%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20stroke%3D%22%23ffffff%22%20stroke-width%3D%223%22%20stroke-linecap%3D%22round%22%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M240%2052%20L150%20142%20M240%2052%20L335%20142%20M150%20142%20L150%20245%20M150%20245%20L150%20345%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22%23ffffff%22%20font-size%3D%2224%22%20text-anchor%3D%22middle%22%3E%3Ccircle%20cx%3D%22240%22%20cy%3D%2252%22%20r%3D%227%22%2F%3E%3Ctext%20x%3D%22187%22%20y%3D%2290%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22300%22%20y%3D%2290%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22150%22%20y%3D%22164%22%3Eu%3C%2Ftext%3E%3Ctext%20x%3D%22335%22%20y%3D%22164%22%3Eb%3C%2Ftext%3E%3Ctext%20x%3D%22130%22%20y%3D%22203%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22150%22%20y%3D%22266%22%3Ev%3C%2Ftext%3E%3Ctext%20x%3D%22130%22%20y%3D%22310%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22150%22%20y%3D%22372%22%3Ed%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

El símbolo $d$ tiene código `000`, mientras que $b$ tiene código `1`. Observemos que $u$ y $v$ tienen un único hijo, por lo que podemos eliminarlos sin introducir ambigüedades:

![700](data:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20style%3D%22color%3Argb\(237%2C%20237%2C%20237\)%22%20viewBox%3D%220%200%20320%20210%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20stroke%3D%22%23ffffff%22%20stroke-width%3D%223%22%20stroke-linecap%3D%22round%22%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M160%2038%20L80%20142%20M160%2038%20L240%20142%22%2F%3E%3C%2Fg%3E%3Ccircle%20cx%3D%22160%22%20cy%3D%2238%22%20r%3D%227%22%20fill%3D%22%23ffffff%22%2F%3E%3Cg%20fill%3D%22%23ffffff%22%20font-size%3D%2223%22%20text-anchor%3D%22middle%22%3E%3Ctext%20x%3D%22105%22%20y%3D%2284%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22215%22%20y%3D%2284%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%2280%22%20y%3D%22173%22%3Ed%3C%2Ftext%3E%3Ctext%20x%3D%22240%22%20y%3D%22173%22%3Eb%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

Ahora $d$ tiene código `0` y $b$ conserva `1`. Ambos códigos siguen siendo de prefijos, pero hemos reducido la longitud de $d$ de 3 a 1 bit.

Si $f_d=0.18$, la contribución de $d$ al promedio de bits por símbolo cambia de:

$$  
0.18(3)=0.54  
\quad\longrightarrow\quad  
0.18(1)=0.18  
$$

Por tanto, el promedio disminuye en $0.36$ bits por símbolo. **El código original no podía ser óptimo**, porque encontramos otro código válido que utiliza menos bits en promedio.

### Demostración por contradicción

Supongamos que $T$ es un árbol óptimo y que contiene un nodo interno $u$ con un único hijo $v$.

Construimos un nuevo árbol $T'$ eliminando $u$ y conectando directamente $v$ con el padre de $u$. Si $u$ es la raíz, entonces $v$ se convierte en la nueva raíz.

Sea $D(u)$ el conjunto de hojas descendientes de $u$. Al realizar esta transformación:

- Las hojas de $D(u)$ disminuyen su profundidad en una unidad.
    
- Las demás hojas conservan su profundidad.
    
- El nuevo árbol sigue representando un código de prefijos válido.
    

Como la longitud de cada palabra código corresponde a la profundidad de su hoja, tenemos:

$$  
\begin{aligned}  
\operatorname{PBS}(T')  
&=\sum_{x\in\Sigma}f_x|\gamma_T(x)|  
-\sum_{x\in D(u)}f_x\  
&=\operatorname{PBS}(T)-\sum_{x\in D(u)}f_x.  
\end{aligned}  
$$

Si todas las frecuencias son positivas, entonces:

$$  
\sum_{x\in D(u)}f_x>0  
$$

y, en consecuencia:

$$  
\boxed{\operatorname{PBS}(T')<\operatorname{PBS}(T)}  
$$

Esto contradice nuestra hipótesis de que $T$ era óptimo. Por tanto, un árbol óptimo no puede contener nodos internos con un único hijo. $\square$

### Aplicación al ejemplo de $\gamma^{iv}$

En el árbol de $\gamma^{iv}$, el símbolo $d$ tiene código `00`, pero su padre posee un único hijo. Podemos contraer ese nodo y cambiar la codificación de $d$ a `0`, manteniendo las demás palabras código.

Como $f_d=0.18$, el promedio disminuye en:

$$  
\Delta\operatorname{PBS}  
=f_d(2-1)=0.18.  
$$

Por tanto, $\gamma^{iv}$ no es óptimo.

**Conclusión:** En un código de prefijos óptimo no deben existir nodos internos con un solo hijo, porque representan bits innecesarios. Eliminar esos nodos conserva la propiedad de prefijos y reduce el promedio de bits por símbolo siempre que haya frecuencias positivas en el subárbol afectado.

_Nota:_ Si se permiten símbolos con frecuencia cero, puede existir un código óptimo con nodos de un solo hijo cuya eliminación no mejore estrictamente el PBS. En ese caso, el lema garantiza que existe al menos un árbol óptimo completo, aunque no necesariamente que todos los árboles óptimos lo sean.

---

## 5. Lema 2: más profundo implica menos frecuente

**Lema.** Sea $T$ el árbol de un código óptimo y sean $x,y\in\Sigma$ dos símbolos tales que:

$$  
\operatorname{depth}(x)<\operatorname{depth}(y).  
$$

Entonces necesariamente:

$$  
\boxed{f_x\geq f_y}  
$$

Es decir, **un símbolo situado a menor profundidad no puede ser menos frecuente que otro situado a mayor profundidad**.

### Intuición: ¿por qué los símbolos frecuentes deben estar más cerca de la raíz?

Recordemos que la profundidad de una hoja determina la longitud de su palabra código. Por tanto, cada bit adicional que asignamos a un símbolo se paga tantas veces como este aparece en el texto.

Si un símbolo es muy frecuente, conviene asignarle una palabra código corta, pues reducir su longitud produce un ahorro mayor que reducir la de un símbolo poco frecuente.

**Ejemplo.** Consideremos dos símbolos:

- $c$, con frecuencia $f_c=0.20$, situado a profundidad 3.
    
- $d$, con frecuencia $f_d=0.18$, situado a profundidad 2.
    

Como $c$ es más frecuente que $d$, resulta ineficiente que su codificación sea más larga. Podemos **intercambiar sus posiciones en el árbol** sin modificar su estructura ni las codificaciones de los demás símbolos.

Antes del intercambio, las contribuciones de ambos símbolos al promedio de bits son:

$$  
0.20(3)+0.18(2)=0.96.  
$$

Después de intercambiarlos:

$$  
0.20(2)+0.18(3)=0.94.  
$$

Por tanto, conseguimos un ahorro de:

$$  
\boxed{0.96-0.94=0.02\text{ bits/símbolo}}  
$$

El código original no podía ser óptimo, porque encontramos otro código de prefijos válido que utiliza menos bits en promedio.

### Demostración por contradicción (intercambio)

Supongamos que $T$ es un árbol óptimo y que existen dos símbolos $x,y$ tales que:

$$  
\operatorname{depth}(x)<\operatorname{depth}(y),  
\qquad f_x<f_y.  
$$

Es decir, el símbolo $x$ está más cerca de la raíz, pero es menos frecuente que $y$.

Construimos un nuevo árbol $T'$ **intercambiando únicamente las etiquetas de las hojas $x$ y $y$**, sin modificar la estructura del árbol. Como las hojas conservan sus posiciones, el nuevo código sigue siendo de prefijos.

Definimos la contribución de todos los demás símbolos al promedio de bits como:

$$  
\omega=\sum_{z\neq x,y}f_z\operatorname{depth}(z).  
$$

Así, el promedio del árbol original es:

$$  
\operatorname{PBS}(T)=\omega+f_x\operatorname{depth}(x)+f_y\operatorname{depth}(y).  
$$

Mientras que, después del intercambio:

$$  
\operatorname{PBS}(T')=\omega+f_x\operatorname{depth}(y)+f_y\operatorname{depth}(x).  
$$

Restando ambas expresiones, los términos $\omega$ se cancelan:

$$  
\begin{aligned}  
\operatorname{PBS}(T)-\operatorname{PBS}(T')  
&=f_x\operatorname{depth}(x)+f_y\operatorname{depth}(y)\  
&\quad-f_x\operatorname{depth}(y)-f_y\operatorname{depth}(x)\  
&=(f_x-f_y)\big(\operatorname{depth}(x)-\operatorname{depth}(y)\big).  
\end{aligned}  
$$

Por nuestra hipótesis:

$$  
\underbrace{(f_x-f_y)}_{<0}  
\underbrace{\big(\operatorname{depth}(x)-\operatorname{depth}(y)\big)}_{<0}>0.  
$$

Por tanto:

$$  
\boxed{\operatorname{PBS}(T)-\operatorname{PBS}(T')>0}  
$$

Esto implica que:

$$  
\operatorname{PBS}(T')<\operatorname{PBS}(T).  
$$

Hemos construido un código válido con menor promedio de bits, lo cual **contradice la hipótesis de que $T$ era óptimo**. En consecuencia:

$$  
\boxed{\operatorname{depth}(x)<\operatorname{depth}(y)\implies f_x\geq f_y}  
$$

$\square$

### Aplicación: el intercambio que mejoró $\gamma$

En el árbol de $\gamma$, el símbolo $c$ está a profundidad 3 con frecuencia $f_c=0.20$, mientras que $d$ está a profundidad 2 con frecuencia $f_d=0.18$.

Esto viola el lema, pues el símbolo más frecuente tiene una palabra código más larga.

Al intercambiar sus etiquetas, el ahorro es:

$$  
\begin{aligned}  
\Delta\operatorname{PBS}  
&=(3-2)(0.20-0.18)\  
&=\boxed{0.02\text{ bits/símbolo}}.  
\end{aligned}  
$$

De esta manera, obtenemos el código $\gamma'$ con:

$$  
\boxed{\operatorname{PBS}(\gamma')=2.23}  
$$

**Conclusión:** En un árbol óptimo, los símbolos más frecuentes no pueden estar a mayor profundidad que símbolos estrictamente menos frecuentes. Si esto ocurre, podemos intercambiar sus etiquetas y disminuir el promedio de bits sin modificar la estructura del árbol.

Este lema justifica una de las ideas fundamentales de Huffman: **reservar las palabras código más largas para los símbolos menos frecuentes**.

**Observación:** El lema establece una condición necesaria de optimalidad, pero no suficiente. Un árbol que respeta el orden entre frecuencias y profundidades no es necesariamente óptimo; todavía debemos determinar cómo organizar sus ramas.
### 5.1 Consecuencia: si nos dieran la forma del árbol

Kleinberg–Tardos destacan una lectura útil: si alguien nos diera la **forma** de un árbol óptimo $T^*$ sin etiquetas, sabríamos etiquetarlo: las hojas menos profundas reciben los símbolos más frecuentes, nivel por nivel. Dentro de un mismo nivel el orden **no importa**, porque todas esas hojas tienen el mismo multiplicador $\operatorname{depth}$.

El problema es que no conocemos la forma, y hay exponencialmente muchas. La clave es mirar el **fondo** del árbol.

---

## 6. Lema 3: los dos símbolos menos frecuentes pueden ser hermanos

**Lema.** Sean $x,y\in\Sigma$ los dos símbolos de menor frecuencia. Entonces existe un árbol de codificación óptimo en el que $x$ y $y$ son **hojas hermanas situadas a máxima profundidad**, es decir, comparten el mismo padre.

### Intuición: ¿por qué los símbolos menos frecuentes pueden ser hermanos?

Recordemos los dos resultados anteriores:

1. **Lema 1:** En un árbol óptimo, cada nodo interno tiene exactamente dos hijos.
    
2. **Lema 2:** Los símbolos menos frecuentes pueden colocarse a mayor profundidad sin aumentar el promedio de bits por símbolo.
    

Consideremos una hoja de máxima profundidad. Como el árbol es completo, su hermano también debe ser una hoja: si fuera un nodo interno, tendría descendientes todavía más profundos, contradiciendo que estamos en la profundidad máxima.

Por tanto, **existe un par de hojas hermanas a máxima profundidad**. Podemos colocar allí los dos símbolos menos frecuentes, intercambiando sus etiquetas con las de las hojas originales. Por el Lema 2, estos intercambios no aumentan el costo, por lo que el árbol resultante sigue siendo óptimo.

### Ejemplo: fusionar los símbolos menos frecuentes

Supongamos un alfabeto $\Sigma={a,b,c,d,e}$ con las siguientes frecuencias:

|Símbolo|Frecuencia|
|---|---|
|$a$|0.35|
|$b$|0.25|
|$c$|0.20|
|$d$|0.12|
|$e$|0.08|

Los dos símbolos menos frecuentes son $d$ y $e$. El lema garantiza que podemos construir un árbol óptimo donde ambos sean hermanos.

**La idea fundamental de Huffman consiste en fusionarlos temporalmente en un único símbolo artificial $z$:**

$$  
z=(d,e),\qquad f_z=f_d+f_e=0.12+0.08=0.20.  
$$

Así, reducimos el problema original de cinco símbolos a uno de cuatro:

$$  
{a,b,c,d,e}\longrightarrow{a,b,c,z}.  
$$

Una vez encontrado un árbol óptimo para el problema reducido, sustituimos la hoja $z$ por un nodo interno con dos hijos: $d$ y $e$.

### ¿Por qué podemos resolver el problema reducido?

Sea $T'$ el árbol del problema reducido y $T$ el árbol que obtenemos al expandir $z$ en sus dos hijos.

Al realizar esta expansión, las profundidades de $d$ y $e$ son exactamente una unidad mayores que la profundidad original de $z$:

$$  
\operatorname{depth}_T(d)=\operatorname{depth}_{T'}(z)+1  
$$

$$  
\operatorname{depth}_T(e)=\operatorname{depth}_{T'}(z)+1.  
$$

Las profundidades de los demás símbolos permanecen iguales. Por tanto, la contribución de $d$ y $e$ al promedio es:

$$  
\begin{aligned}  
&f_d(\operatorname{depth}_{T'}(z)+1)  
+f_e(\operatorname{depth}_{T'}(z)+1)\  
&=(f_d+f_e)\operatorname{depth}_{T'}(z)+f_d+f_e\  
&=f_z\operatorname{depth}_{T'}(z)+f_d+f_e.  
\end{aligned}  
$$

El primer término corresponde exactamente a la contribución de $z$ en el problema reducido. En consecuencia:

$$  
\boxed{\operatorname{PBS}(T)=\operatorname{PBS}(T')+f_d+f_e}  
$$

En nuestro ejemplo:

$$  
\operatorname{PBS}(T)=\operatorname{PBS}(T')+0.20.  
$$

Esto significa que **expandir el símbolo artificial incrementa el costo en una cantidad fija**, independiente de cómo se haya construido el resto del árbol.

Por tanto, minimizar el costo del problema reducido también minimiza el costo del problema original entre los árboles donde $d$ y $e$ son hermanos. Como el lema garantiza que existe un árbol óptimo con esa propiedad, resolver óptimamente el problema reducido permite recuperar una solución óptima del problema original.

### Conexión con el algoritmo greedy de Huffman

Los tres lemas justifican la estrategia de Huffman:

1. **Árbol completo:** Un código óptimo no necesita nodos internos con un único hijo.
    
2. **Frecuencia y profundidad:** Los símbolos menos frecuentes pueden situarse en las hojas más profundas.
    
3. **Propiedad de hermanos:** Los dos símbolos menos frecuentes pueden compartir un padre en algún árbol óptimo.
    

En consecuencia, podemos **fusionar los dos símbolos de menor frecuencia y resolver recursivamente un problema más pequeño**.

Este procedimiento constituye la elección _greedy_ de Huffman: en cada iteración se seleccionan los dos símbolos de menor frecuencia y se reemplazan por un nodo cuya frecuencia es la suma de ambas.

**Conclusión:** La elección greedy es segura porque existe una solución óptima que contiene a los dos símbolos menos frecuentes como hermanos. La fusión conserva la posibilidad de alcanzar el óptimo y reduce el tamaño del problema en una unidad. Esta es la propiedad que permite construir recursivamente un código de Huffman óptimo.

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
