---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-11-03"
unidad: Programación dinámica I
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Programación dinámica
  - Subproblemas superpuestos
  - Planificación ponderada de intervalos
  - Subestructura óptima
  - Memoización
  - Tabulación
  - Reconstrucción de soluciones
referencias:
  - "06DynamicProgrammingI.pdf, diapositivas 1–18 (Kevin Wayne; Kleinberg y Tardos)"
tags:
  - clase
  - algoritmos
  - programacion-dinamica
  - intervalos
---

# Clase 19 · Programación dinámica I: intervalos con pesos

> [!info] Alcance y procedencia
> Este apunte desarrolla **las diapositivas 1–18** de [[06DynamicProgrammingI.pdf|06DynamicProgrammingI.pdf]]. El apunte rápido de clase decía «llegamos a la página 22»; aquí se respeta el límite solicitado de la 18. Los intervalos, los pesos 1–999–1 y los valores de $p(j)$ indicados como «de las diapositivas» provienen del material. La tabla con ocho pesos numéricos es un **ejemplo didáctico añadido** para poder ejecutar la recurrencia completa.

## Pregunta central

Si cada trabajo ocupa un intervalo de tiempo y produce una ganancia, ¿cómo elegimos un conjunto compatible de **peso total máximo** cuando la regla voraz de terminar primero ya no basta?

> [!summary] Idea de la clase
> Ordenamos los trabajos por hora de fin. Para cada prefijo $1,\ldots,j$ hacemos una elección binaria: **excluir** $j$ o **incluirlo** y continuar en el último prefijo compatible $p(j)$. La ecuación $OPT(j)=\max\{OPT(j-1),w_j+OPT(p(j))\}$ expresa la estructura del problema. Una recursión directa repite subproblemas; una tabla guarda cada valor una sola vez. Al final, otra pasada permite recuperar los trabajos elegidos.

![[Screenshot 2026-11-03 at 11.43.56 a.m..png]]

## 1. ¿Por qué programación dinámica? (diapositivas 1–6)

### Del problema grande a los pequeños

En un **algoritmo voraz**, se inspeccionan los elementos en cierto orden y se toman decisiones irrevocables con información local. En **divide y vencerás**, se divide la entrada en subproblemas independientes, se resuelven y se combinan sus respuestas. En **programación dinámica (PD)** también se resuelven problemas pequeños y se combinan, pero **distintas ramas necesitan los mismos subproblemas**. Guardar cada respuesta evita recalcularla.

Un ejemplo intuitivo de superposición es la recurrencia de Fibonacci: calcular $F(5)$ pide $F(4)$ y $F(3)$; calcular $F(4)$ vuelve a pedir $F(3)$. Si guardamos $F(3)$ la primera vez, la segunda consulta cuesta tiempo constante. En un problema de optimización la tabla guarda, además, el mejor valor para un **estado** precisamente definido. «Recordar resultados» solo es útil si el estado contiene toda la información necesaria para decidir el futuro.

![[pd-paradigmas.svg]]

**Lectura del diagrama.** A la izquierda, los hijos de cada llamada son independientes. A la derecha, dos rutas llegan al mismo estado $OPT(3)$: allí aparece el trabajo repetido que la PD elimina. El diagrama es conceptual; la recurrencia concreta de intervalos se deduce más abajo.

Richard Bellman estudió sistemáticamente estos procesos de decisiones por etapas en la década de 1950. El nombre «dinámica» alude a planificar a lo largo de etapas; **no** significa que los datos cambien mientras corre el algoritmo. Las diapositivas también enumeran aplicaciones en IA, compiladores, gráficos, investigación de operaciones, teoría de la información, control y bioinformática. Ejemplos citados allí son *diff*, Viterbi, Bellman–Ford, alineamiento de secuencias y ajuste de texto. Las diapositivas 1 y 6 anuncian también mínimos cuadrados segmentados, mochila y estructura de RNA; **hasta la 18 solo se desarrolla planificación ponderada de intervalos**.

La diapositiva 5 muestra una selección de libros de PD y no introduce un algoritmo adicional. Su función aquí es contextual: el mismo patrón de estados, decisiones y reutilización aparece en problemas de áreas muy diferentes.

### Qué debe tener una formulación de PD

1. **Estado:** qué subproblema representa una entrada de la tabla.
2. **Opciones:** las decisiones exhaustivas que puede tomar una solución óptima.
3. **Recurrencia:** cómo se obtiene el valor del estado a partir de estados menores.
4. **Casos base:** respuestas para estados sin decisiones.
5. **Orden de evaluación:** que cada dependencia esté resuelta antes de usarla.
6. **Reconstrucción:** cómo pasar del valor óptimo a una solución concreta, si se necesita.

En este ejemplo, el estado será simplemente el índice $j$ del último trabajo permitido. Esa elección es la clave: resume todo el pasado relevante en un prefijo.

## 2. El problema de los intervalos con pesos (diapositiva 7)

Cada trabajo $j$ tiene inicio $s_j$, fin $f_j$ y peso o ganancia $w_j>0$. Modelamos el tiempo ocupado como $[s_j,f_j)$: si uno acaba justo cuando empieza otro, **sí son compatibles**. Buscamos un conjunto $S$ de trabajos sin traslapes que maximice

$$
\sum_{j\in S}w_j.
$$

La diapositiva 7 dibuja ocho trabajos $a,\ldots,h$ sobre una línea de tiempo. Por ejemplo, $a$ ocupa $[0,6)$, $b$ ocupa $[1,4)$, $c$ ocupa $[3,5)$ y $h$ ocupa $[8,11)$. Los trabajos $a$ y $h$ son compatibles porque $6\leq8$; $a$ y $b$ no lo son porque se traslapan. La figura **no da pesos numéricos** para esos ocho trabajos: el símbolo $w_j$ indica que cada uno aporta una ganancia.

> [!important] Dos objetivos distintos
> Si todos los pesos valen $1$, maximizar la suma equivale a escoger el **mayor número** de intervalos. Con pesos diferentes queremos la **mayor ganancia total**, incluso si elegimos menos trabajos. No se debe confundir «más intervalos» con «más peso».

## 3. Por qué falla terminar primero (diapositiva 8)

El algoritmo voraz conocido para intervalos **sin pesos** ordena por fin ascendente y acepta un trabajo si no se traslapa con lo ya elegido. Su argumento de intercambio permite tomar uno que termina temprano sin reducir cuántos trabajos caben después. Con pesos, reemplazar un intervalo por otro que termina antes puede perder una gran ganancia.

La diapositiva 8 contiene este contraejemplo exacto:

| Trabajo | Intervalo | Peso |
|:--|:--:|--:|
| $a$ | $[0,3)$ | $1$ |
| $b$ | $[0,10)$ | $999$ |
| $h$ | $[8,11)$ | $1$ |

Ordenar por fin escoge primero $a$. Después rechaza $b$ porque se traslapa con $a$ y acepta $h$, que empieza en $8$: obtiene $\{a,h\}$ con peso $2$. La mejor opción es $\{b\}$, con peso $999$, porque $b$ se traslapa tanto con $a$ como con $h$. La razón $999/2$ muestra que el error puede crecer arbitrariamente si aumentamos el peso de $b$.

**Por qué sí funcionaba sin pesos.** Si el objetivo fuera contar trabajos, toma una solución óptima cualquiera y compara su primer trabajo con el que termina más temprano de todos. Reemplazar el primero por el que termina más temprano no puede estorbar a ninguno de los trabajos posteriores, así que conserva el número de trabajos. Repitiendo este argumento después de cada elección se obtiene el algoritmo voraz. Con pesos distintos, ese reemplazo puede cambiar la ganancia: en la figura, sustituir $b$ por $a$ reduce el peso de $999$ a $1$.

**Explora el contraejemplo:** cambia el peso de $b$ y observa cuándo cambia la solución óptima. La explicación anterior contiene el caso original aunque el interactivo no cargue.

<iframe src="pd-voraz-intervalos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 4. Ordenar y calcular el predecesor $p(j)$ (diapositiva 9)

Ordenamos los trabajos por fin no decreciente y los renumeramos de modo que

$$
f_1\leq f_2\leq\cdots\leq f_n.
$$

Para cada $j$, definimos $p(j)$ como el **mayor índice $i<j$** compatible con $j$; si no existe, $p(j)=0$. Dado que los trabajos están ordenados por fin, compatibilidad con un trabajo anterior equivale a $f_i\leq s_j$. Por tanto,

$$
p(j)=\max\bigl(\{i<j:f_i\leq s_j\}\cup\{0\}\bigr).
$$

El «mayor índice» es importante: los trabajos $1,\ldots,p(j)$ son todos los candidatos anteriores que pueden acompañar a $j$, mientras que $p(j)+1,\ldots,j-1$ terminan demasiado tarde. **No** significa que debamos seleccionar obligatoriamente el trabajo $p(j)$; solo marca el final del prefijo permitido.

La diapositiva 9 usa los siguientes intervalos (sin pesos). Aquí se completa la columna $p(j)$ a partir de la figura:

| $j$ | $[s_j,f_j)$ | $p(j)$ | Motivo breve |
|--:|:--:|--:|:--|
| 1 | $[1,4)$ | 0 | Ninguno termina a tiempo. |
| 2 | $[3,5)$ | 0 | $f_1=4>3$. |
| 3 | $[0,6)$ | 0 | Empieza en $0$. |
| 4 | $[4,7)$ | 1 | $f_1=4\leq4$. |
| 5 | $[3,8)$ | 0 | No hay fin anterior $\leq3$. |
| 6 | $[5,9)$ | 2 | $f_2=5\leq5$. |
| 7 | $[6,10)$ | 3 | $f_3=6\leq6$. |
| 8 | $[4,11)$ | 1 | $f_1=4\leq4$. |

Así obtenemos exactamente los ejemplos de la lámina: $p(8)=1$, $p(7)=3$ y $p(2)=0$. Para hallar todos los $p(j)$, buscamos el último fin $\leq s_j$ **solo en las posiciones anteriores a $j$**. Como los fines ya están ordenados, cada búsqueda binaria tarda $O(\log n)$ y las $n$ búsquedas tardan $O(n\log n)$.

Por ejemplo, para $j=7$ buscamos $s_7=6$ entre los fines anteriores $4,5,6,7,8,9$: el último valor admisible es $f_3=6$, así que $p(7)=3$. Para $j=8$ buscamos $s_8=4$ entre $4,5,6,7,8,9,10$: solo $f_1=4$ es admisible y $p(8)=1$. Una implementación que evita errores de límites es:

~~~text
para j ← 1 hasta n:
    lo ← 1; hi ← j - 1; p[j] ← 0
    mientras lo ≤ hi:
        mid ← ⌊(lo + hi) / 2⌋
        si f[mid] ≤ s[j]:
            p[j] ← mid       # candidato válido; buscar uno posterior
            lo ← mid + 1
        si no:
            hi ← mid - 1     # termina demasiado tarde
~~~

**Explora $p(j)$:** selecciona un trabajo y mira qué trabajos quedan en su prefijo compatible. El valor $p(j)$ de la tabla de arriba permite estudiar esta parte sin el interactivo.

<iframe src="pd-predecesores-tabla.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 5. Estado, elección binaria y ecuación de Bellman (diapositiva 10)

Definimos $OPT(j)$ como el **peso máximo** que puede obtenerse usando exclusivamente trabajos con índices $1,\ldots,j$. No es el peso del trabajo $j$ ni exige incluirlo. La respuesta buscada es $OPT(n)$; para el conjunto vacío, $OPT(0)=0$.

Para encontrar la recurrencia, consideramos una solución óptima cualquiera para el prefijo $1,\ldots,j$. Hay **exactamente dos casos**:

- **No contiene $j$.** Entonces usa solo $1,\ldots,j-1$. Si su peso fuera menor que $OPT(j-1)$, podríamos reemplazarla por una mejor solución de ese prefijo. Por eso, el mejor valor de este caso es $OPT(j-1)$.
- **Sí contiene $j$.** Ganamos $w_j$. Los trabajos anteriores compatibles con $j$ están dentro de $1,\ldots,p(j)$. Si la parte restante no fuese óptima para ese prefijo, podríamos sustituirla por una mejor y aumentar el peso total. Por eso, el mejor valor de este caso es $w_j+OPT(p(j))$.

Como ambos casos cubren todas las soluciones posibles, tomamos el mayor:

$$
OPT(j)=\begin{cases}
0,&j=0,\\[2mm]
\max\bigl\{OPT(j-1),\;w_j+OPT(p(j))\bigr\},&j\geq1.
\end{cases}
$$

![[pd-decision-binaria.svg]]

**Lectura del diagrama.** Al excluir $j$ avanzamos al prefijo $j-1$ sin ganancia inmediata. Al incluirlo sumamos $w_j$ y saltamos a $p(j)$, porque los índices intermedios no son compatibles. Esta demostración es la **subestructura óptima** de la que habla la diapositiva: una solución óptima contiene soluciones óptimas de subproblemas apropiados.

### Ejemplo numérico completo, añadido para estudiar la recurrencia

La diapositiva 9 da los intervalos, pero **no asigna pesos**. Añadimos $w=(3,5,8,7,6,9,5,10)$ únicamente para ejecutar la tabla. El vector de predecesores, que sí se deduce de la figura, es $p=(0,0,0,1,0,2,3,1)$.

| $j$ | $w_j$ | $p(j)$ | Excluir: $M[j-1]$ | Incluir: $w_j+M[p(j)]$ | $M[j]$ | Decisión para este prefijo |
|--:|--:|--:|--:|--:|--:|:--|
| 0 | — | — | — | — | **0** | Caso base |
| 1 | 3 | 0 | 0 | 3 | **3** | Incluir 1 |
| 2 | 5 | 0 | 3 | 5 | **5** | Incluir 2 |
| 3 | 8 | 0 | 5 | 8 | **8** | Incluir 3 |
| 4 | 7 | 1 | 8 | $7+3=10$ | **10** | Incluir 4 |
| 5 | 6 | 0 | 10 | 6 | **10** | Excluir 5 |
| 6 | 9 | 2 | 10 | $9+5=14$ | **14** | Incluir 6 |
| 7 | 5 | 3 | 14 | $5+8=13$ | **14** | Excluir 7 |
| 8 | 10 | 1 | 14 | $10+3=13$ | **14** | Excluir 8 |

La mejor ganancia es **14**, alcanzada con los trabajos $\{2,6\}$: $[3,5)$ termina cuando comienza $[5,9)$, y $5+9=14$. Observa que elegir el trabajo 4 es óptimo para el **prefijo 1..4**, pero no permanece en la solución global: la tabla guarda mejores valores de prefijos, no una única elección irrevocable.

En el interactivo anterior, el control «Paso de la tabla» deja ver cómo cada fila usa únicamente resultados ya conocidos y luego reconstruye $\{2,6\}$.

## 6. Recursión directa: correcta pero lenta (diapositivas 11–13)

El pseudocódigo literal de la idea matemática es:

~~~text
COMPUTE-OPT(j):
    si j = 0: devolver 0
    sin_j ← COMPUTE-OPT(j - 1)
    con_j ← w[j] + COMPUTE-OPT(p[j])
    devolver max(sin_j, con_j)
~~~

Antes se ordenan los trabajos y se calculan los predecesores. El pseudocódigo es **correcto** por la ecuación de Bellman. Su problema es que una misma llamada $COMPUTE\text{-}OPT(k)$ se repite en distintas ramas.

En la familia «escalonada» de la diapositiva 13 se cumple $p(1)=0$ y $p(j)=j-2$ para $j\geq2$. Si $C(j)$ cuenta llamadas recursivas incluyendo la llamada actual, entonces $C(j)=1+C(j-1)+C(j-2)$ para $j\geq2$. Este crecimiento es del orden de $\varphi^j$, con $\varphi=(1+\sqrt5)/2\approx1.618$. El árbol de la lámina muestra varias apariciones de estados como $3$, $2$ y $1$: son **llamadas distintas al mismo subproblema**.

La pregunta de la diapositiva 12 pide el **peor caso** de $COMPUTE\text{-}OPT(n)$. La respuesta es $\Theta(2^n)$ (opción D), no $\Theta(1.618^n)$: esta última corresponde a la familia escalonada ilustrativa. Si todos los trabajos son consecutivos y compatibles, $p(j)=j-1$, y ambas ramas llaman a $j-1$; entonces $C(j)=1+2C(j-1)=\Theta(2^j)$. También $p(j)\leq j-1$, por lo que ninguna instancia puede generar más que un árbol binario de profundidad $n$ salvo constantes. Se trata del costo de **esa implementación recursiva**, no de una dificultad inevitable del problema.

**Explora el número de llamadas:** compara la familia escalonada con el peor caso, y observa cuántos estados diferentes existen frente a cuántas veces se invocan.

<iframe src="pd-superposicion-memo.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 7. Memoización: resolver cada estado una vez (diapositivas 14–15)

La versión **top-down** conserva la recursión, pero usa una tabla $M$ para recordar el valor calculado de cada estado. Inicializamos $M[0]=0$ y marcamos $M[1],\ldots,M[n]$ como no calculados. Es importante usar una marca separada o un valor especial: un resultado $0$ no debe confundirse con «sin inicializar».

~~~text
M-COMPUTE-OPT(j):
    si M[j] ya está calculado: devolver M[j]
    M[j] ← max(M-COMPUTE-OPT(j - 1),
               w[j] + M-COMPUTE-OPT(p[j]))
    devolver M[j]
~~~

La primera llamada a $j$ calcula $M[j]$ usando estados menores; las siguientes devuelven el valor almacenado. La recursión termina porque $j-1<j$ y $p(j)<j$. La tabla representa el mismo $OPT(j)$ que acabamos de demostrar; cambia **cómo** se evalúa, no la definición matemática.

**Costo de las llamadas.** Hay $n$ estados no base. Cada estado se inicializa a lo sumo una vez y, al hacerlo, emite a lo sumo dos llamadas. Contando la llamada inicial, hay $O(n)$ invocaciones, y cada una hace $O(1)$ trabajo propio. La diapositiva 15 expresa esto con el potencial $\Phi=$ número de entradas inicializadas: empieza en $0$, nunca supera $n$ y una llamada que expande subproblemas lo incrementa en $1$ al terminar. Una cota cómoda es $2n+1$ invocaciones para todo el cálculo, contando el inicio; la diapositiva resume el argumento como «a lo sumo $2n$ llamadas recursivas» emitidas por las expansiones.

**Costo completo.** Ordenar por fin cuesta $O(n\log n)$; calcular todos los $p(j)$ por búsqueda binaria cuesta $O(n\log n)$; llenar $M$ cuesta $O(n)$. Por tanto, el algoritmo completo tarda **$O(n\log n)$** y ocupa **$O(n)$ espacio** para $p$ y $M$, además de hasta $O(n)$ de pila recursiva. Esta cota supone operaciones aritméticas y comparaciones de pesos de costo constante.

La diapositiva 16 condensa la motivación en una frase sobre no repetir el pasado: en términos algorítmicos, significa **guardar el resultado de un estado ya resuelto** y reutilizarlo cuando otra rama lo solicite.

## 8. Recuperar los trabajos elegidos (diapositiva 17)

$M[n]$ solo dice cuánto vale la mejor solución. Para obtener los trabajos, repetimos la decisión que produjo cada máximo:

~~~text
FIND-SOLUTION(j):
    si j = 0: devolver ∅
    si w[j] + M[p[j]] > M[j - 1]:
        devolver {j} ∪ FIND-SOLUTION(p[j])
    si no:
        devolver FIND-SOLUTION(j - 1)
~~~

El signo **$>$** establece que, en un empate, se excluye $j$. También sería correcto usar $\geq$ si se quiere incluirlo al empatar, siempre que se mantenga una política coherente. Cuando se incluye $j$, se salta directamente a $p(j)$; cuando se excluye, se retrocede a $j-1$. En ambos casos el índice baja, así que hay a lo sumo $n$ pasos y costo **$O(n)$**, además del espacio necesario para devolver la solución.

En el ejemplo añadido: en $j=8$ excluimos (13<14), en $j=7$ excluimos (13<14), en $j=6$ incluimos (14>10) y saltamos a $p(6)=2$; en $j=2$ incluimos (5>3) y saltamos a $0$. Resultado: $\{2,6\}$.

> [!tip] Error frecuente
> Una fila que dice «incluir» no significa que ese trabajo esté en la solución final. Solo es la elección óptima **para ese prefijo**. La reconstrucción debe comenzar en $n$ y seguir los saltos; no basta con reunir todas las filas marcadas «incluir».

## 9. Tabulación: desenrollar la recursión (diapositiva 18)

La versión **bottom-up** llena la tabla de izquierda a derecha:

~~~text
ordenar trabajos por fin y renumerar 1..n
calcular p[1..n]
M[0] ← 0
para j ← 1 hasta n:
    M[j] ← max(M[j - 1], w[j] + M[p[j]])
devolver M[n]
~~~

Es válido este orden porque **ambas dependencias son anteriores a $j$**: $j-1<j$ y $p(j)<j$. Su invariante de ciclo es: al empezar la iteración $j$, $M[i]=OPT(i)$ para todo $0\leq i<j$. La base $M[0]=OPT(0)=0$ vale. Si el invariante vale al empezar, la recurrencia calcula $M[j]=OPT(j)$; por inducción vale al terminar. La tabulación llena $n$ filas en $O(n)$ después del preprocesamiento, así que el costo completo sigue siendo **$O(n\log n)$** y el espacio de tablas es **$O(n)$**. No utiliza pila recursiva. Se puede aplicar el mismo `FIND-SOLUTION` a su tabla.

| Aspecto | Recursión sin tabla | Memoización (*top-down*) | Tabulación (*bottom-up*) |
|:--|:--|:--|:--|
| Orden | Según el árbol de llamadas | Según las llamadas necesarias | $0,1,\ldots,n$ |
| ¿Repite un estado? | Sí, muchas veces | No se recalcula | No |
| Trabajo de la recurrencia | $\Theta(2^n)$ en el peor caso | $O(n)$ | $O(n)$ |
| Costo total con ordenación y $p$ | Exponencial en el peor caso | $O(n\log n)$ | $O(n\log n)$ |
| Memoria adicional | Pila $O(n)$ | Tablas y pila $O(n)$ | Tablas $O(n)$ |

## 10. Guía para resolver un ejercicio similar

1. **Escribe los intervalos y pesos.** Aclara si tocarse en un extremo cuenta como compatibilidad; aquí sí.
2. **Ordena por fin** y renumera. Nunca uses la numeración original para calcular $p$ después de ordenar.
3. **Calcula $p(j)$** buscando el último fin $\leq s_j$ entre índices menores que $j$. Comprueba algunos valores a mano.
4. **Define $OPT(j)$ en palabras.** «Mejor peso posible usando los primeros $j$ trabajos» evita confundir valor con conjunto.
5. **Separa incluir/excluir** y justifica por qué cada rama usa un subproblema óptimo.
6. **Llena $M[0..n]$** en orden; para cada fila anota ambos candidatos antes de tomar el máximo.
7. **Reconstruye desde $n$** y verifica dos cosas: que los trabajos recuperados son compatibles y que sus pesos suman $M[n]$.
8. **Analiza por fases:** ordenación $O(n\log n)$, predecesores $O(n\log n)$, tabla $O(n)$, recuperación $O(n)$.

**Autocomprobación.** En la figura de la diapositiva 9, ¿por qué $p(4)=1$ aunque $p(7)=3$? Porque $p$ depende del inicio de **cada** trabajo: el 4 empieza en 4 y solo el 1 termina a más tardar en 4; el 7 empieza en 6 y el último trabajo previo que termina a tiempo es el 3. ¿Por qué la respuesta del ejemplo numérico es $14$ y no $10+9$? Porque $M[4]=10$ representa una solución que puede solaparse con el trabajo 6; al incluir 6 solo se permite sumar $M[p(6)]=M[2]=5$.

## Referencia y continuación

- Fuente de esta nota: [[06DynamicProgrammingI.pdf|Kevin Wayne, *Dynamic Programming I*, diapositivas 1–18]].
- Conexión con la clase anterior: [[2026-10-27 ADA - divide_y_veceras_1|divide y vencerás]] resuelve subproblemas independientes; aquí las ramas se superponen y usamos una tabla.
- El resto del archivo presenta otras aplicaciones, pero quedan fuera del alcance de este apunte.
