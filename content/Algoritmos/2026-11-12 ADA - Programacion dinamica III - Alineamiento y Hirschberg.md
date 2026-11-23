---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-11-12"
unidad: Programación dinámica II — alineamiento de secuencias y Hirschberg
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Alineamiento de secuencias
  - Distancia de edición
  - Subestructura óptima
  - Reconstrucción de soluciones
  - Grafo de edición
  - Programación dinámica en espacio lineal
  - Algoritmo de Hirschberg
referencias:
  - "06DynamicProgrammingII.pdf, diapositivas 1–27; aplicación opcional 28–30 (Kevin Wayne; Kleinberg y Tardos, secciones 6.6 y 6.7)"
tags:
  - clase
  - algoritmos
  - programacion-dinamica
  - alineamiento
  - hirschberg
---

# Clase 21 · Programación dinámica III: alineamiento de secuencias y algoritmo de Hirschberg

**12 de noviembre de 2026** · Continúa [[2026-11-10 ADA - Programacion dinamica II|la clase del 10 de noviembre: mínimos cuadrados segmentados, mochila y cambio de monedas]].

> [!info] Fuente y alcance
> El desarrollo principal sigue **las diapositivas 1–27** de *Dynamic Programming II*, de Kevin Wayne, hasta el análisis de Hirschberg. Al final se incluye, como **aplicación opcional**, la subsecuencia común más larga de las diapositivas 28–30; no se presupone que se haya visto en clase. El PDF completo contiene también temas posteriores. Los diagramas y simulaciones son elaboraciones didácticas; el ejemplo `PALETTE`/`PALATE`, su tabla y las penalizaciones $\delta=2$, $\alpha=1$ proceden de las diapositivas 6 y 10. La tabla numérica del corte de Hirschberg y los ejercicios se calculan aquí a partir de ese ejemplo.

![[06DynamicProgrammingII.pdf]]

## Ruta de la clase

La clase anterior usaba dos coordenadas en la mochila: **objetos disponibles y capacidad**. Ahora las dos coordenadas serán **cuántas letras de cada cadena hemos procesado**. El recorrido conceptual es:

1. Decidir qué significa que dos cadenas sean parecidas.
2. Describir las tres maneras de terminar un alineamiento.
3. Obtener una tabla de costos y recuperar una solución con retroceso.
4. Conservar sólo dos columnas para ahorrar memoria, perdiendo el historial.
5. Interpretar la tabla como un grafo y recuperar puntos de paso óptimos.
6. Usar esos puntos para reconstruir con divide y vencerás: **Hirschberg**.

> [!summary] Idea central
> **La tabla completa recuerda todo el pasado. Hirschberg recuerda dónde partir y vuelve a calcular lo necesario dentro de cada mitad.** Así conserva el tiempo $O(mn)$ y reduce el espacio de $\Theta(mn)$ a $O(m+n)$, incluyendo la solución.

## 1. Comparar cadenas: ¿qué estamos midiendo? · diapositivas 3–6

### Intuición

Si comparas dos palabras letra por letra y falta una letra al principio, todas las posiciones posteriores quedan desplazadas. Eso produce muchas diferencias aparentes aunque el error real sea pequeño. La diapositiva 3 compara `ocurrance` con `occurrence`: introducir **huecos** permite volver a poner frente a frente las letras que corresponden.

Un alineamiento escribe las dos cadenas en renglones de igual longitud, conserva el orden de sus letras y permite insertar el símbolo `−` como hueco. Para evaluar el resultado cobramos:

- **Coincidencia:** normalmente $0$.
- **Sustitución:** emparejar letras diferentes cuesta $\alpha_{pq}$.
- **Hueco:** dejar una letra sin pareja cuesta $\delta$.

No basta contar coincidencias: hay que comparar el costo de las sustituciones con el de introducir huecos. Un alineamiento con cero sustituciones puede tener demasiados huecos.

### Formalización

Sean $x=x_1\cdots x_m$ y $y=y_1\cdots y_n$. Usaremos $\delta>0$, $\alpha_{pq}\ge 0$ y $\alpha_{pp}=0$. Las diapositivas permiten que $\alpha_{pq}$ dependa de **qué letras** se emparejan; para los ejemplos numéricos tomaremos una penalización uniforme $\alpha$ si $p\ne q$.

El objetivo es encontrar un **alineamiento global de costo mínimo**: se consideran las dos cadenas completas, incluidos sus extremos. Con sustitución, inserción y eliminación de costo $1$ se obtiene la distancia de Levenshtein usual. En las slides se usa el modelo de costos más general.

**Quiz de la diapositiva 6.** Para `PALETTE` y `PALATE`, con hueco $2$ y sustitución $1$, un alineamiento es:

~~~text
x: P A L E T T E
y: P A L − A T E
         ↑ ↑
       hueco y sustitución T/A
~~~

Cuesta $2+1=\mathbf{3}$: respuesta **C**. Éste es un candidato; la programación dinámica demostrará que ningún alineamiento cuesta menos.

> [!note] La matriz BLOSUM de la diapositiva 5
> Ilustra que en proteínas no todas las sustituciones tienen el mismo significado. BLOSUM suele expresarse como una **puntuación de similitud que se maximiza**. Aquí seguimos la formulación de las diapositivas posteriores: **penalizaciones que se minimizan**. No se deben copiar sus puntuaciones como si fueran directamente los costos $\alpha_{pq}$ de este ejemplo.

## 2. Qué es un alineamiento válido · diapositiva 7

### Intuición

Podemos dejar letras sin pareja, pero no cambiar su orden ni reutilizarlas. Si emparejamos una letra temprana de $x$ con una tardía de $y$, una letra posterior de $x$ ya no puede retroceder a una posición anterior de $y$.

Por ejemplo, la lámina muestra:

~~~text
x: C T A C C − G
y: − T A C A T G
~~~

Las coincidencias y sustituciones son parejas; las letras frente a `−` quedan sin pareja. Una columna `−/−` no aporta ninguna letra y se excluye de la representación.

### Formalización

Un alineamiento es un conjunto $M$ de parejas de **posiciones** $(i,j)$ tal que:

1. Cada posición de $x$ o de $y$ pertenece a lo más a una pareja.
2. No hay cruces: si $(i,j),(i',j')\in M$ e $i<i'$, entonces $j<j'$.

Se distinguen posiciones aunque dos letras sean iguales. Su costo es:

$$
\operatorname{cost}(M)=
\sum_{(i,j)\in M}\alpha_{x_i y_j}
+\delta\,(m-|M|)+\delta\,(n-|M|).
$$

Los dos últimos términos cuentan las letras sin pareja de **ambas** cadenas. Para el ejemplo `CTACCG`/`TACATG`, las parejas son

$$
M=\{(2,1),(3,2),(4,3),(5,4),(6,6)\}.
$$

Con $\delta=2$ y sustitución $1$, **ese alineamiento** cuesta $2+1+2=5$. No se afirma todavía que sea el óptimo para cualquier sistema de penalizaciones.

## 3. Descubrir el estado y las tres decisiones · diapositiva 8

### Intuición

Imagina que el alineamiento ya está terminado y observa su última columna. Sólo puede contener:

1. La última letra de $x$ frente a la última de $y$.
2. La última letra de $x$ frente a un hueco.
3. Un hueco frente a la última letra de $y$.

Al quitar esa columna queda **el mismo problema sobre prefijos más pequeños**. Necesitamos dos índices porque una decisión puede consumir una letra de una cadena, de la otra o de ambas.

![Tres decisiones de la última columna](pd2-tres-decisiones.svg)

**Lectura del diagrama:** emparejar consume dos letras; un hueco consume sólo una. El resto de cada opción es un subproblema que la tabla ya sabe resolver.

### Formalización

Definimos

$$
OPT(i,j)=\text{costo mínimo de alinear }x_1\cdots x_i\text{ con }y_1\cdots y_j.
$$

La respuesta es $OPT(m,n)$. Los casos base alinean un prefijo con la cadena vacía $\varepsilon$:

$$
OPT(0,0)=0,\qquad OPT(i,0)=i\delta,\qquad OPT(0,j)=j\delta.
$$

Para $i,j>0$:

$$
\boxed{
OPT(i,j)=\min\left\{
\begin{array}{ll}
OPT(i-1,j-1)+\alpha_{x_i y_j} & \text{emparejar},\\
OPT(i-1,j)+\delta & \text{hueco en }y,\\
OPT(i,j-1)+\delta & \text{hueco en }x.
\end{array}\right.
}
$$

**Por qué el resto debe ser óptimo.** Fijada la última columna, si su prefijo pudiera alinearse más barato, lo sustituiríamos por ese mejor alineamiento sin cambiar la última columna. El total bajaría: contradicción. Éste es el argumento de intercambio de **subestructura óptima**.

Las tres opciones son exhaustivas para la representación por columnas. Si las dos últimas letras quedan sin pareja, aparecerán en dos columnas distintas, y una de ellas será la última: también queda cubierto por la recurrencia.

## 4. Llenar la tabla paso a paso · diapositivas 9–10

### Intuición

Cada casilla mira tres vecinas: diagonal superior izquierda, arriba e izquierda. Si llenamos de arriba hacia abajo y de izquierda a derecha, esas tres ya existen. La tabla evita resolver una y otra vez el mismo par de prefijos.

### Formalización y algoritmo

~~~text
ALINEAMIENTO(x[1..m], y[1..n], δ, α):
    para i = 0..m: M[i,0] = i·δ
    para j = 0..n: M[0,j] = j·δ
    para i = 1..m:
        para j = 1..n:
            M[i,j] = mín{
                M[i−1,j−1] + α(x[i],y[j]),
                M[i−1,j] + δ,
                M[i,j−1] + δ
            }
    devolver M
~~~

**Invariante:** antes de calcular $M[i,j]$, las tres casillas que consulta contienen el óptimo de sus prefijos. Por la recurrencia, el nuevo valor también es correcto. Los bordes inician la inducción.

Tabla completa de la diapositiva 10, con $x=\texttt{PALETTE}$, $y=\texttt{PALATE}$, $\delta=2$ y sustitución $1$:

| $x\backslash y$ | $\varepsilon$ | P | A | L | A | T | E |
|:--|--:|--:|--:|--:|--:|--:|--:|
| $\varepsilon$ | 0 | 2 | 4 | 6 | 8 | 10 | 12 |
| P | 2 | 0 | 2 | 4 | 6 | 8 | 10 |
| A | 4 | 2 | 0 | 2 | 4 | 6 | 8 |
| L | 6 | 4 | 2 | 0 | 2 | 4 | 6 |
| E | 8 | 6 | 4 | 2 | **1** | 3 | 4 |
| T | 10 | 8 | 6 | 4 | 3 | **1** | 3 |
| T | 12 | 10 | 8 | 6 | 5 | 3 | **2** |
| E | 14 | 12 | 10 | 8 | 7 | 5 | **3** |

Dos casillas para practicar el significado de las coordenadas:

$$
\begin{aligned}
M[4,4]&=\min\{M[3,3]+1,\;M[3,4]+2,\;M[4,3]+2\}\\
&=\min\{0+1,\;2+2,\;2+2\}=1,
\end{aligned}
$$

porque `PALE` y `PALA` sólo necesitan sustituir `E` por `A`. Después,

$$
M[6,5]=\min\{M[5,4]+0,\;M[5,5]+2,\;M[6,4]+2\}
=\min\{3,3,7\}=3.
$$

Aquí **empatan dos predecesores**. La tabla determina un valor óptimo, pero puede haber varias maneras de alcanzarlo.

**Simulación 1.** Usa «Siguiente» para ver las tres dependencias de cada casilla. «Completar» termina el llenado; «Reconstruir» inicia el retroceso y «Siguiente» lo recorre. Se puede cambiar el ejemplo y las penalizaciones.

<iframe src="pd2-alineamiento-tabla.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Si el interactivo no carga: el mínimo de cada casilla se calcula con la diagonal, arriba e izquierda; la respuesta está en la esquina inferior derecha y vale $3$.

## 5. Recuperar el alineamiento, no sólo su costo · diapositivas 10–11

### Intuición

El número $3$ no dice dónde colocar el hueco. Para descubrirlo, partimos de la última casilla y preguntamos **qué decisión pudo producir su valor**. Un predecesor sirve si su costo más el de la última columna es exactamente el valor actual.

### Formalización del retroceso

En $(i,j)$ probamos, respetando los bordes:

| Igualdad que se cumple | Columna que añadimos | Siguiente estado |
|:--|:--|:--|
| $M[i,j]=M[i-1,j-1]+\alpha_{x_i y_j}$ | $x_i/y_j$ | $(i-1,j-1)$ |
| $M[i,j]=M[i-1,j]+\delta$ | $x_i/\texttt{−}$ | $(i-1,j)$ |
| $M[i,j]=M[i,j-1]+\delta$ | $\texttt{−}/y_j$ | $(i,j-1)$ |

Recogemos columnas **de derecha a izquierda**, así que al final invertimos su orden. Ante un empate basta elegir cualquiera de las igualdades válidas.

Una ruta válida para la tabla es:

$$
(7,6)\to(6,5)\to(5,4)\to(4,3)\to(3,3)\to(2,2)\to(1,1)\to(0,0).
$$

Produce `PALETTE` frente a `PAL−ATE`, como la diapositiva. Otro desempate puede producir `PALA−TE`: también cuesta $3$.

**Costo del algoritmo completo.** Hay $(m+1)(n+1)$ casillas y trabajo constante por casilla. Para cadenas no vacías:

- Llenado: $\Theta(mn)$ tiempo y $\Theta(mn)$ espacio.
- Retroceso: $O(m+n)$ tiempo, porque cada paso consume al menos una letra.
- Salida: a lo más $m+n$ columnas, por lo que ocupa $O(m+n)$ espacio.

> [!note] Contexto de la diapositiva 11
> La lámina menciona una barrera condicional basada en SETH para obtener tiempo fuertemente subcuadrático en el caso general. No es una demostración de que cualquier algoritmo deba tardar $\Omega(n^2)$ sin hipótesis adicionales. Hirschberg mejora **espacio**, conservando la cota de tiempo de la PD.

## 6. Dos columnas: ahorrar memoria para calcular el valor · diapositiva 12

### Intuición

Una vez calculada una columna, ninguna columna futura necesita volver a consultar la que está dos posiciones atrás. Podemos reciclar el espacio: conservamos la columna anterior y la que estamos construyendo.

El problema aparece al intentar retroceder: ya borramos las casillas por las que tendríamos que pasar. **Saber el costo final no equivale a recordar las decisiones.**

### Formalización

Fijaremos la misma orientación que Hirschberg en las slides: **columnas indexadas por $j$, cada una con $m+1$ posiciones $i$**.

~~~text
ULTIMA-COLUMNA(x[1..m], y[1..n], δ, α):
    prev[i] = i·δ para i = 0..m
    para j = 1..n:
        cur[0] = j·δ
        para i = 1..m:
            cur[i] = mín{
                prev[i−1] + α(x[i],y[j]),
                cur[i−1] + δ,
                prev[i] + δ
            }
        intercambiar(prev, cur)       # reutilizar dos arreglos
    devolver prev
~~~

La diagonal y la izquierda están en `prev`; la vecina superior está en `cur`. Por eso el recorrido interno tiene que ser **de $i=1$ hacia $m$**.

El arreglo devuelto contiene **todos** los valores $OPT(i,n)$, no sólo $OPT(m,n)$. Eso será lo que necesite Hirschberg.

- Tiempo: $O(mn)$.
- Memoria de los costos: $O(m)$; podemos usar $O(\min\{m,n\})$ si elegimos la orientación más corta para los arreglos.
- Aún no tenemos un procedimiento de retroceso con esa memoria.

**Quiz de la diapositiva 12: A.** Es fácil modificar el algoritmo para calcular **la distancia** en espacio lineal. Recuperar un alineamiento con esa memoria exige una idea adicional, que se desarrolla a continuación; no basta borrar columnas.

**Simulación 2.** Observa qué valores permanecen en `prev`, cómo crece `cur` y cómo se reciclan al terminar la columna. Para `PALETTE`/`PALATE` son dos arreglos de $8$ posiciones, frente a las $8\times7=56$ casillas de la tabla completa.

<iframe src="pd2-dos-columnas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Si el interactivo no carga: cada costo nuevo depende únicamente de `prev[i−1]`, `prev[i]` y `cur[i−1]`. Las columnas más antiguas se pueden descartar, pero con ellas se pierde el historial del retroceso.

## 7. Ver la tabla como un grafo de edición · diapositivas 15–17

### Intuición

Cada casilla representa cuántas letras de ambas cadenas ya consumimos. Una decisión del alineamiento es un movimiento: derecha, abajo o diagonal. Así, construir un alineamiento es recorrer una cuadrícula desde la esquina inicial hasta la final.

![La tabla es un grafo de edición](pd2-grafo-de-edicion.svg)

**Lectura del diagrama:** avanzar a la derecha consume una letra de $y$; bajar consume una de $x$; la diagonal consume ambas. El costo del camino es la suma de las columnas del alineamiento.

### Formalización

El grafo tiene nodos $(i,j)$ para $0\le i\le m$, $0\le j\le n$, y aristas:

$$
\begin{array}{lll}
(i-1,j)\to(i,j) & \text{costo }\delta & \text{hueco en }y,\\
(i,j-1)\to(i,j) & \text{costo }\delta & \text{hueco en }x,\\
(i-1,j-1)\to(i,j) & \text{costo }\alpha_{x_i y_j} & \text{emparejamiento}.
\end{array}
$$

Es un **DAG**: cada arista aumenta $i+j$, de modo que no se puede regresar a un nodo anterior. Definimos

$$
f(i,j)=\text{distancia mínima de }(0,0)\text{ a }(i,j).
$$

Entonces $\boxed{f(i,j)=OPT(i,j)}$.

**Demostración por inducción fuerte en $i+j$ — diapositiva 16.**

1. En $(0,0)$ ambas cantidades valen $0$; en los bordes sólo se pueden usar huecos.
2. La última arista hacia $(i,j)$ viene de uno de sus tres predecesores.
3. Por hipótesis inductiva, sus distancias son los valores $OPT$ correspondientes.
4. Tomar el mínimo del costo del predecesor más la arista reproduce exactamente la ecuación de Bellman.

Ahora el problema es recuperar un **camino mínimo** usando poca memoria, sin almacenar toda la cuadrícula.

## 8. Mirar desde ambos extremos: $f$ y $g$ · diapositivas 17–21

### Intuición

Si queremos saber si conviene pasar por cierto nodo, necesitamos dos precios: cuánto cuesta **llegar** a él y cuánto cuesta **seguir desde él hasta el destino**. El primer cálculo mira prefijos; el segundo mira sufijos.

Hirschberg no prueba todos los caminos. Calcula esos dos precios para los nodos de **una sola columna**.

### Formalización

Además de $f$, definimos

$$
g(i,j)=\text{distancia mínima de }(i,j)\text{ a }(m,n).
$$

Sus condiciones de borde son

$$
g(m,n)=0,\qquad g(i,n)=(m-i)\delta,\qquad g(m,j)=(n-j)\delta.
$$

Para $i<m$, $j<n$:

$$
g(i,j)=\min\left\{
\alpha_{x_{i+1}y_{j+1}}+g(i+1,j+1),\;
\delta+g(i+1,j),\;
\delta+g(i,j+1)
\right\}.
$$

Se calcula desde abajo a la derecha, o aplicando la misma rutina a **los dos sufijos invertidos**. No se intercambian los papeles de $x$ y $y$, ni los argumentos de $\alpha$; sólo se invierte el orden de las posiciones.

Para una columna fija $j^*$:

- $F[i]=f(i,j^*)$ se obtiene alineando $x$ con $y_1\cdots y_{j^*}$, mediante dos columnas.
- Sea $R$ la última columna al alinear $\operatorname{rev}(x)$ con $\operatorname{rev}(y_{j^*+1}\cdots y_n)$. Entonces $G[i]=g(i,j^*)=R[m-i]$.

El índice $m-i$ es esencial: el sufijo $x_{i+1}\cdots x_m$ tiene **$m-i$ letras**. Los arreglos $F$ y $G$ deben referirse a la misma fila original antes de sumarlos.

**Observación 1, diapositiva 21.** El mejor camino que está obligado a pasar por $(i,j)$ cuesta

$$
\boxed{f(i,j)+g(i,j)}.
$$

La suma es alcanzable concatenando los dos caminos mínimos y ningún camino que pase por ese nodo puede mejorar alguna de sus partes. La concatenación es válida porque las coordenadas nunca retroceden.

## 9. Elegir un punto óptimo en la columna media · diapositiva 22

### Intuición

Dibuja una línea vertical en medio de la cuadrícula. Todo camino del inicio al final tiene que tocar esa columna. Si encontramos **un punto por el que pasa algún camino óptimo**, podemos resolver por separado lo que ocurre antes y después de él.

No elegimos la fila media por geometría. Elegimos la fila que hace menor el costo de **llegar más continuar**.

![Corte óptimo de PALETTE y PALATE](pd2-corte-hirschberg.svg)

**Lectura del diagrama:** la columna media es $j^*=3$. Se puede pasar por $(3,3)$ con costo total $3$. Sólo conservamos el rectángulo anterior y el posterior a ese punto para las llamadas recursivas.

### Formalización y justificación

Tomamos

$$
j^*=\lfloor n/2\rfloor,\qquad
q\in\operatorname*{arg\,min}_{0\le i\le m}\{f(i,j^*)+g(i,j^*)\}.
$$

Entonces existe un camino óptimo que pasa por $(q,j^*)$, porque:

1. Para cualquier $i$, concatenar los mejores caminos a través de $(i,j^*)$ da un camino completo. Por tanto $f(i,j^*)+g(i,j^*)\ge OPT(m,n)$.
2. Algún camino óptimo toca la columna $j^*$ en algún nodo $(i_0,j^*)$. Sus dos tramos deben ser óptimos; por tanto $f(i_0,j^*)+g(i_0,j^*)=OPT(m,n)$.
3. El mínimo entre todos los candidatos es exactamente $OPT(m,n)$, y cualquier minimizador sirve.

Un camino puede recorrer **varios nodos de la columna media mediante pasos verticales**. No hace falta que la cruce en un único nodo.

### Ejemplo completo del primer corte

Para `PALETTE` ($m=7$) y `PALATE` ($n=6$), usamos $j^*=3$ y obtenemos:

| $i$ | prefijo de $x$ | $F[i]=f(i,3)$ | $G[i]=g(i,3)$ | $F[i]+G[i]$ |
|--:|:--|--:|--:|--:|
| 0 | $\varepsilon$ | 6 | 8 | 14 |
| 1 | P | 4 | 6 | 10 |
| 2 | PA | 2 | 5 | 7 |
| **3** | **PAL** | **0** | **3** | **3** |
| **4** | **PALE** | **2** | **1** | **3** |
| 5 | PALET | 4 | 2 | 6 |
| 6 | PALETT | 6 | 4 | 10 |
| 7 | PALETTE | 8 | 6 | 14 |

Hay dos mínimos: **$q=3$ y $q=4$**. Fijamos el menor para hacer el recorrido reproducible. Con $q=3$:

~~~text
problema original: PALETTE / PALATE
                       ↓ corte (q,j*) = (3,3)
izquierda:         PAL / PAL      costo 0
derecha:          ETTE / ATE      costo 3
~~~

No se añade un costo de «unión»: el nodo del corte representa prefijos ya consumidos; cada letra queda en exactamente uno de los dos subproblemas.

## 10. Algoritmo de Hirschberg: dividir, resolver y concatenar · diapositivas 14 y 23

### Intuición

La PD con dos columnas nos entrega el mejor punto de paso. Divide y vencerás usa ese punto como frontera. Repetimos el procedimiento dentro de cada rectángulo hasta que una cadena sea tan pequeña que podamos resolverla directamente.

La combinación de paradigmas es la clave: **la PD decide dónde cortar; la recursión reconstruye la solución**.

### Formalización y pseudocódigo

En este pseudocódigo los fragmentos de cadenas son **vistas mediante índices**, no copias; `reverse` también puede recorrerse con índices decrecientes. Los casos pequeños se resuelven con la tabla y el retroceso de las secciones 4–5.

~~~text
HIRSCHBERG(x[1..m], y[1..n]):
    si m = 0:
        emitir n columnas hueco / y[j]
        regresar
    si n = 0:
        emitir m columnas x[i] / hueco
        regresar
    si m = 1 o n = 1:
        resolver con tabla pequeña y emitir su alineamiento
        regresar

    j* = piso(n/2)
    F = ULTIMA-COLUMNA(x, y[1..j*])
    R = ULTIMA-COLUMNA(reverse(x), reverse(y[j*+1..n]))
    G[i] = R[m−i] para i = 0..m
    q = menor índice que minimiza F[i] + G[i]

    liberar F, R y G                   # antes de las llamadas recursivas
    HIRSCHBERG(x[1..q],   y[1..j*])
    HIRSCHBERG(x[q+1..m], y[j*+1..n])
~~~

Las llamadas emiten las columnas sobre una misma lista de salida, primero la izquierda y después la derecha. Al final se forma una vez cada renglón. Así evitamos construir repetidamente cadenas grandes al concatenar.

**Casos que no deben omitirse.** $q$ puede ser $0$ o $m$: una de las piezas de $x$ será vacía. Si $n$ es impar, las dos partes de $y$ tienen longitudes $\lfloor n/2\rfloor$ y $\lceil n/2\rceil$.

**Corrección.** Los casos base producen alineamientos óptimos. Para una llamada mayor, la sección 9 garantiza un camino óptimo por $(q,j^*)$. Por inducción, cada llamada devuelve un alineamiento óptimo de su rectángulo; concatenarlos produce un camino por ese nodo con costo $f(q,j^*)+g(q,j^*)=OPT(m,n)$.

**Simulación 3.** Avanza por el cálculo del corte, la división, los casos base y las uniones. En la tabla de candidatos pulsa otra fila: el camino dibujado muestra el costo de obligar a pasar por ese punto. Prueba $i=3$, $i=4$ e $i=2$ en el primer corte. Los dos primeros cuestan $3$; el tercero cuesta $7$.

<iframe src="pd2-hirschberg.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Si el interactivo no carga: se escoge el mínimo de $F[i]+G[i]$, se divide en ese nodo y se concatenan dos soluciones óptimas. Para el ejemplo, el resultado tiene un hueco, una sustitución y costo $3$.

> [!note] Memoria del algoritmo y memoria del simulador
> El simulador conserva eventos didácticos para permitir volver a pasos anteriores. La cota de memoria que se demuestra a continuación corresponde al algoritmo con reutilización de arreglos, no al historial de la interfaz.

## 11. Por qué el espacio es lineal · diapositiva 24

### Intuición

Lo caro son las columnas de costos. Una vez elegida la fila $q$, **ya no necesitamos esas columnas para resolver las piezas**. Sólo debemos recordar los límites del rectángulo y el corte. Liberamos los arreglos antes de descender en la recursión y resolvemos una pieza a la vez.

### Formalización

Con la orientación de las slides:

- Los arreglos de una llamada usan $O(m')\le O(m)$ posiciones, donde $m'$ es la longitud local de $x$.
- Al recursar no quedan vivos los arreglos de los ancestros; sólo metadatos de tamaño constante por marco.
- Cada división parte por la mitad la longitud local de $y$: profundidad $O(\log n)$ para $n\ge2$.
- La salida ocupa $O(m+n)$: cada columna consume al menos una letra original.
- Un caso base con una longitud igual a $1$ usa una tabla de tamaño $O(m'+n')$, que también es lineal.

En conjunto:

$$
\boxed{\text{Espacio total}=O(m+n).}
$$

Es la cota lineal de la diapositiva 24, expresada allí como $\Theta(m+n)$ contando el almacenamiento lineal de cadenas y solución. El espacio auxiliar puede afinarse según la orientación y la representación, pero para esta clase basta la cota total.

> [!warning] Detalle de implementación que sostiene la prueba
> Si conservas $F$ y $G$ en cada ancestro durante la recursión, o copias todas las subcadenas, el argumento anterior deja de aplicar: pueden coexistir varios arreglos de longitud grande. Guardar índices, liberar los arreglos antes de recursar y construir una salida compartida hace concreta la cota lineal.

## 12. Por qué el tiempo sigue siendo $O(mn)$ · diapositivas 25–27

### Intuición

Podría parecer que repetir PD en varios niveles cuesta un factor $\log n$ adicional. Pero cada nivel trabaja sobre **menos área total**: no reconstruimos dos cuadrículas de altura $m$. Las alturas de las dos piezas suman $m$ y cada pieza tiene aproximadamente la mitad del ancho.

El trabajo se distribuye como

$$
mn+\frac{mn}{2}+\frac{mn}{4}+\cdots < 2mn.
$$

### Formalización: cota floja y cota ajustada

Calcular $F$, $G$ y escoger $q$ cuesta $O(mn)$ por llamada no trivial. Si simplificamos reemplazando ambas alturas por $m$, obtenemos la cota válida pero floja de la diapositiva 26:

$$
T(m,n)\le 2T(m,n/2)+O(mn)=O(mn\log n).
$$

Se pierde información: las alturas reales son $q$ y $m-q$. Para anchos pares, la recurrencia precisa es

$$
\boxed{T(m,n)\le T(q,n/2)+T(m-q,n/2)+c\,mn.}
$$

La suma de las áreas hijas es

$$
q\frac n2+(m-q)\frac n2=\frac{mn}{2}.
$$

**Inducción fuerte de la diapositiva 27.** En esta cuenta de áreas, asignamos costo de cuadrícula $0$ a las piezas vacías y contabilizamos por separado sus emisiones y la gestión de esas llamadas. Ajustamos una constante $c$ para cubrir el trabajo local y los casos base no vacíos; suponemos para llamadas menores que $T(a,b)\le2cab$. Entonces:

$$
\begin{aligned}
T(m,n)
&\le cmn+2cq\frac n2+2c(m-q)\frac n2\\
&=cmn+cqn+cmn-cqn\\
&=2cmn.
\end{aligned}
$$

Las llamadas con cadena vacía emiten huecos; los casos de una dimensión constante se resuelven directamente. La escritura total de la salida es $O(m+n)$. La gestión de las llamadas también cabe en la cota: hay $O(n)$ nodos en el árbol, pues cada división reparte un intervalo de $y$ en dos intervalos no vacíos y disjuntos.

**¿Y si $n$ es impar?** Se usan piso y techo en la recurrencia. Para ver que el orden no cambia, podemos acotar el ancho inicial por la siguiente potencia de dos, $N<2n$, y en el nivel $\ell$ acotar cada ancho por $N/2^\ell$. Los intervalos activos de $x$ son disjuntos y sus longitudes suman a lo más $m$. El trabajo de ese nivel queda acotado por $O(mN/2^\ell)$; la suma geométrica sigue siendo $O(mn)$. Los casos base y las salidas vacías aportan a lo más un término lineal.

Por tanto, para $m,n\ge1$:

$$
\boxed{\text{Hirschberg: }O(mn)\text{ tiempo y }O(m+n)\text{ espacio}.}
$$

Si permitimos cadenas vacías, una expresión que también cuenta la escritura de la salida es $O(mn+m+n)$.

**Quiz de la diapositiva 25: A, $O(mn)$.** La opción con $\log n$ corresponde al análisis flojo, no a la mejor cota demostrada.

## 13. Comparación y receta para recordar

### Intuición

Las tres versiones resuelven el mismo problema. Lo que cambia es **qué información conservan** para poder reconstruir una solución.

### Comparación formal

| Método | Información conservada | Tiempo, $m,n\ge1$ | Espacio | ¿Devuelve un alineamiento? |
|:--|:--|:--|:--|:--|
| PD con tabla completa | Todos los costos | $\Theta(mn)$ | $\Theta(mn)$ | Sí, con retroceso |
| PD con dos columnas | Costos de la frontera actual | $O(mn)$ | $O(m)$ para los costos | El cálculo por sí solo devuelve el costo |
| Hirschberg | Fronteras temporales y puntos de corte | $O(mn)$ | $O(m+n)$ total | Sí, por divide y vencerás |

**Para reconstruir la idea sin memorizar pseudocódigo:**

1. Define el estado con dos prefijos.
2. Mira la última columna: emparejar, hueco en $x$ o hueco en $y$.
3. Escribe la recurrencia y los bordes con $\varepsilon$.
4. Reconoce que dos columnas bastan para calcular valores.
5. Cambia de perspectiva: alineamiento = camino en un DAG.
6. Calcula costos desde el origen y desde el destino en la columna media.
7. Minimiza **$f+g$**, guarda el corte y libera los arreglos.
8. Resuelve las dos piezas y emite sus columnas en orden.
9. Analiza el tiempo sumando **áreas reales**, no copiando la altura completa a ambos hijos.

## 14. Aplicación opcional de las slides: LCS · diapositivas 28–30

> [!info] Complemento de estudio
> Esta aplicación aparece después del análisis de Hirschberg y antes del siguiente bloque de la presentación. Se incluye para conectar las ideas; el alcance confirmado de la clase llega a Hirschberg.

### Intuición

En lugar de permitir sustituciones, podemos pedir una cadena que aparezca en las dos originales después de borrar algunas letras. No tienen que ser posiciones consecutivas: deben conservar el orden. Eso es una **subsecuencia**, no necesariamente una subcadena.

Por ejemplo, `AC` es subsecuencia de `ABC`, aunque no sea un bloque contiguo. Buscar la subsecuencia común más larga, *Longest Common Subsequence* o LCS, equivale a conservar tantas letras compartidas como sea posible.

### Formalización

Sea $L(i,j)$ la longitud de una LCS de los prefijos de longitudes $i,j$. Entonces:

$$
L(i,j)=
\begin{cases}
0, & i=0\text{ o }j=0,\\
1+L(i-1,j-1), & x_i=y_j,\\
\max\{L(i-1,j),L(i,j-1)\}, & x_i\ne y_j.
\end{cases}
$$

La diapositiva 30 lo reduce al alineamiento con

$$
\delta=1,\qquad
\alpha_{pq}=\begin{cases}0,&p=q,\\+\infty,&p\ne q.\end{cases}
$$

Sólo se emparejan letras iguales. Si conservamos $k$ parejas, quedan $m-k$ letras sin pareja en $x$ y $n-k$ en $y$, por lo que

$$
D=m+n-2k,\qquad
\boxed{|LCS(x,y)|=\frac{m+n-D}{2}}.
$$

La fórmula corresponde a **esta distancia con sustituciones prohibidas**, no a cualquier distancia de edición. Ejemplo: `ABC` y `AC` conservan `AC`, de longitud $2$; hay un hueco, $D=1$ y $(3+2-1)/2=2$.

Aplicando Hirschberg al problema reducido se recupera una LCS en $O(mn)$ tiempo y $O(m+n)$ espacio. El artículo original mostrado en la diapositiva 14 se presenta precisamente en el contexto de subsecuencias comunes.

## 15. Ejercicios de autocomprobación

Intenta justificar primero la decisión en palabras y después escribir la ecuación o el cálculo.

1. ¿Cuánto cuesta alinear `ABC` con $\varepsilon$ si $\delta=2$? ¿Dónde aparece ese valor en la tabla?
2. Para `A` y `G`, con hueco $1$ y sustitución $3$, ¿conviene sustituir? Escribe el alineamiento.
3. Calcula $M[5,5]$ para la tabla `PALETTE`/`PALATE` y explica qué letras se consumen.
4. ¿Por qué no basta escoger el menor $F[i]$ para decidir el corte de Hirschberg?
5. En el primer corte del ejemplo, ¿puede elegirse $q=4$? Escribe los dos subproblemas.
6. ¿Por qué guardar una flecha por casilla no resuelve el requisito de espacio lineal?
7. Si $q=0$, ¿se pierde alguna letra? ¿Cuáles son las dos llamadas?
8. ¿Qué error produce sumar $F[i]+R[i]$ sin reindexar el cálculo inverso?
9. ¿Por qué $2T(m,n/2)$ da una cota floja?
10. ¿Se puede aplicar $(m+n-D)/2$ usando la distancia de Levenshtein usual sin cambiar las penalizaciones?

> [!success]- Respuestas razonadas
> 1. $6$: tres letras sin pareja; es $M[3,0]=3\delta$.
> 2. No. `A−` frente a `−G` cuesta $2<3$; puede evitarse la sustitución mediante dos huecos.
> 3. $\min\{M[4,4]+0,M[4,5]+2,M[5,4]+2\}=\min\{1,5,5\}=1$. Se emparejan las dos T finales de `PALET`/`PALAT`.
> 4. Porque un punto barato para llegar puede ser muy caro para continuar. Se necesita el costo total $F[i]+G[i]$.
> 5. Sí: `PALE`/`PAL` y `TTE`/`ATE`, con costos $2$ y $1$; suman $3$.
> 6. Hay $\Theta(mn)$ casillas; una flecha de tamaño constante por casilla sigue ocupando $\Theta(mn)$.
> 7. No. Se resuelven $\varepsilon/y_1\cdots y_{j^*}$ y $x_1\cdots x_m/y_{j^*+1}\cdots y_n$. La primera llamada emite huecos en $x$.
> 8. $R[i]$ corresponde a un sufijo de $x$ de longitud $i$, mientras que $F[i]$ usa un prefijo de longitud $i$. Para continuar desde esa fila se necesita el sufijo de longitud $m-i$: $G[i]=R[m-i]$.
> 9. Trata ambos hijos como si conservaran las $m$ filas. Sus alturas reales suman $m$, así que el área total se reduce aproximadamente a la mitad en cada nivel.
> 10. No. Para `A`/`B`, Levenshtein da $D=1$ y la fórmula daría $1/2$, que no es una longitud de LCS. La reducción de las slides prohíbe sustituciones y usa hueco $1$.

## Referencias y navegación

- Fuente principal: [[06DynamicProgrammingII.pdf|Kevin Wayne, Dynamic Programming II]], diapositivas **3–12** (alineamiento) y **14–27** (Hirschberg); aplicación opcional **28–30** (LCS). Kleinberg y Tardos, *Algorithm Design*, secciones 6.6 y 6.7, indicadas en las portadas de bloque.
- Anterior: [[2026-11-10 ADA - Programacion dinamica II|10 de noviembre — mínimos cuadrados segmentados, mochila y monedas]].
- Índice: [[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]].
- El siguiente bloque del PDF empieza en la diapositiva 31; queda para una continuación.
