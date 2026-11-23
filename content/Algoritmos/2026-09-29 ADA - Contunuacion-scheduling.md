---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-09-29"
unidad: Algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[Algoritmo voraz|Algoritmo voraz]]"
  - Selección de intervalos
  - Partición de intervalos
  - Tardanza máxima
  - Argumento de intercambio
  - Caché óptima fuera de línea
  - Caminos más cortos desde una fuente
  - Algoritmo de Dijkstra
  - Cola de prioridad
referencias:
  - "[[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas]]"
  - "[[04GreedyAlgorithmsI.pdf]], diapositivas 9–52"
  - "[[04GreedyAlgorithmsII.pdf]], diapositivas 2–20 (Dijkstra, incorporado después)"
  - "Kleinberg y Tardos, Algorithm Design, secciones 4.1–4.4"
tags:
  - clase
  - algoritmos
  - greedy
  - interval-scheduling
  - interval-partitioning
  - earliest-deadline-first
  - exchange-argument
  - caching
  - belady
  - dijkstra
  - shortest-paths
---

# Clase 12 · Algoritmos voraces: intervalos, tardanza y caché

![[04GreedyAlgorithmsI.pdf]]

> [!info] Alcance de la sesión
> Esta clase continuó exactamente donde terminó la del [[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas|22 de septiembre]]. Se completaron las diapositivas 9–52 de *Greedy Algorithms I*: **selección de intervalos**, **partición de intervalos**, **calendarización para minimizar la tardanza máxima** y **caché óptima fuera de línea**. El hilo común no es solo “tomar una decisión local”, sino demostrar que dicha decisión puede incorporarse a una solución óptima.
>
> **Añadido posterior (§8):** el **algoritmo de Dijkstra** para caminos más cortos, tomado de *Greedy Algorithms II* (diapositivas 2–20). Se integra aquí porque en Kleinberg–Tardos es la sección 4.4, justo después de la caché óptima, y porque su prueba es el ejemplo más limpio de “greedy se mantiene por delante”.

## Pregunta central

¿Cómo reconocemos la regla voraz correcta para cada problema y cómo demostramos que sus decisiones locales producen un óptimo global?

> [!summary] Idea de la clase
> Problemas que parecen casi iguales pueden requerir órdenes opuestos: para **elegir el mayor número de intervalos** se ordena por finalización; para **asignar todos los intervalos al menor número de aulas** se ordena por inicio; y para **minimizar la tardanza máxima** se ordena por fecha límite. En caché, si conocemos todo el futuro, expulsamos el elemento cuya próxima solicitud está más lejana. Las pruebas usan tres patrones: intercambio, una cota estructural y el principio de que greedy “se mantiene por delante”.

---

## 1. Qué debe contener una solución voraz correcta

Un [[Algoritmo voraz|algoritmo voraz]] construye una solución irreversible mediante una secuencia de elecciones localmente convenientes. Para que sea una solución algorítmica completa necesitamos separar tres afirmaciones:

1. **Factibilidad:** la salida respeta todas las restricciones.
2. **Terminación y complejidad:** el procedimiento concluye y puede implementarse eficientemente.
3. **Optimalidad:** ninguna solución factible tiene un valor objetivo mejor.

La intuición local no implica optimalidad. La regla “más natural” cambia con el objetivo, aun cuando las instancias sean los mismos intervalos.

### 1.1 Estrategias de prueba de la presentación

| Estrategia | Idea | Uso en esta clase |
|---|---|---|
| **Greedy stays ahead** | Después de cada elección, greedy deja una situación al menos tan favorable como cualquier competidor. | Otra lectura de selección de intervalos; invariante de Dijkstra (§8). |
| **Cota estructural** | Toda solución necesita al menos cierto costo; greedy alcanza esa cota. | Partición de intervalos: número de aulas $\ge$ profundidad. |
| **Argumento de intercambio** | Se transforma una solución óptima para que coincida con greedy sin empeorarla. | Selección de intervalos, tardanza y caché de Bélády. |

> [!important] Plantilla mental
> No hay que preguntar “¿cuál regla parece buena?”, sino “¿qué propiedad permitiría reemplazar la primera decisión de un óptimo por mi decisión greedy sin perder calidad?”.

---

## 2. Selección de intervalos (*interval scheduling*)

### 2.1 Modelo

Cada trabajo $j$ ocupa un intervalo semiabierto

$$
[s_j,f_j),
$$

donde $s_j$ es su inicio y $f_j$ su final. Dos trabajos $i$ y $j$ son compatibles si no se traslapan; por ejemplo, si

$$
f_i\le s_j.
$$

Los intervalos se consideran semiabiertos para que un trabajo que termina exactamente cuando otro comienza sea compatible con él.

**Objetivo:** encontrar un subconjunto de cardinalidad máxima cuyos intervalos sean mutuamente compatibles.

### 2.2 Reglas tentadoras que fallan

- **Inicio más temprano:** puede elegir un trabajo muy largo que bloquea muchos trabajos posteriores.
- **Duración más corta:** puede elegir un intervalo corto colocado en el centro y bloquear dos intervalos compatibles entre sí.
- **Menor número aparente de conflictos:** requiere conocer una estructura global y tampoco da, por sí sola, la prueba presentada.

La regla correcta es **finalización más temprana**: escoger primero el trabajo que libera el recurso antes.

### 2.3 Algoritmo *earliest-finish-time-first*

```python
def seleccion_intervalos(trabajos):
    # cada trabajo es (inicio, fin, nombre)
    trabajos.sort(key=lambda j: j.fin)
    seleccion = []
    ultimo_fin = float("-inf")

    for j in trabajos:
        if j.inicio >= ultimo_fin:
            seleccion.append(j)
            ultimo_fin = j.fin

    return seleccion
```

Ordenar cuesta $O(n\log n)$ y el barrido cuesta $O(n)$, así que

$$
T(n)=O(n\log n).
$$

Si los intervalos ya vienen ordenados por finalización, el algoritmo es lineal.

### 2.4 Ejemplo

| Trabajo | Intervalo | Orden por $f_j$ | Decisión |
|---|---:|---:|---|
| $B$ | $[1,2)$ | 1 | Aceptar |
| $A$ | $[0,3)$ | 2 | Rechazar: se traslapa con $B$ |
| $C$ | $[3,5)$ | 3 | Aceptar |
| $D$ | $[4,7)$ | 4 | Rechazar: se traslapa con $C$ |
| $E$ | $[5,9)$ | 5 | Aceptar |
| $F$ | $[8,10)$ | 6 | Rechazar: se traslapa con $E$ |

La salida es $\{B,C,E\}$, con tres trabajos.

### 2.5 Prueba de optimalidad por intercambio

Sea

$$
G=(i_1,i_2,\ldots,i_k)
$$

la solución greedy y sea

$$
O=(j_1,j_2,\ldots,j_m)
$$

una solución óptima ordenada cronológicamente. Escogemos, entre todos los óptimos, uno que coincida con greedy en el prefijo más largo posible:

$$
i_1=j_1,\ldots,i_r=j_r.
$$

Si todavía difieren, greedy escogió $i_{r+1}$ como el trabajo compatible que termina primero. Por tanto,

$$
f_{i_{r+1}}\le f_{j_{r+1}}.
$$

Reemplazar $j_{r+1}$ por $i_{r+1}$ no rompe la compatibilidad con el prefijo, porque greedy verificó esa compatibilidad. Tampoco rompe la compatibilidad con los trabajos posteriores de $O$: $i_{r+1}$ termina a más tardar cuando terminaba $j_{r+1}$, de modo que deja al menos el mismo espacio libre.

Así obtenemos otra solución óptima con una coincidencia más larga con greedy, contradiciendo la elección de $O$. En consecuencia, existe un óptimo que contiene todas las decisiones greedy y $k=m$. $\square$

### 2.6 La versión ponderada es otro problema

Si cada trabajo tiene un peso $w_j$ y queremos maximizar el peso total, terminar primero deja de ser correcto. Basta un intervalo de peso $1$ que termine temprano y se traslape con otro de peso $100$: greedy podría elegir el primero y perder el segundo.

> [!warning] No confundir objetivos
> Maximizar el **número** de intervalos compatibles admite esta solución voraz. Maximizar la **suma de pesos** es el problema de selección de intervalos ponderados y normalmente se resuelve con programación dinámica.

---

## 3. Partición de intervalos (*interval partitioning*)

### 3.1 Mismo tipo de datos, objetivo distinto

Ahora debemos programar **todos** los intervalos. Cada aula puede alojar trabajos compatibles y buscamos minimizar el número de aulas.

| Problema | ¿Se permiten descartar intervalos? | Objetivo | Orden greedy |
|---|---:|---|---|
| Selección | Sí | Elegir el máximo número compatible | Fin creciente |
| Partición | No | Usar el mínimo número de recursos | Inicio creciente |

### 3.2 Profundidad: la cota inferior estructural

La **profundidad** del conjunto de intervalos es

$$
d=\max_t\left|\{j:t\in[s_j,f_j)\}\right|.
$$

Es decir, $d$ es el máximo número de intervalos simultáneamente activos. Si en algún instante hay $d$ clases, cualquier solución necesita al menos $d$ aulas:

$$
\operatorname{OPT}\ge d.
$$

La pregunta decisiva es si puede construirse siempre una calendarización con exactamente $d$ aulas. La respuesta es sí.

### 3.3 Algoritmo *earliest-start-time-first*

1. Ordenar las clases por tiempo de inicio creciente.
2. Mantener las aulas en una cola de prioridad cuya llave sea el final de la última clase asignada.
3. Para la clase $j$, consultar el aula que se libera antes.
4. Si ese final es $\le s_j$, reutilizar el aula; de lo contrario, abrir una nueva.

```python
def particion_intervalos(clases):
    clases.sort(key=lambda c: c.inicio)
    aulas = MinHeap()  # pares (fin_actual, id_aula)

    for c in clases:
        if aulas and aulas.min().fin <= c.inicio:
            _, aula = aulas.extract_min()
        else:
            aula = nueva_aula()

        asignar(c, aula)
        aulas.insert((c.fin, aula))

    return calendario
```

El ordenamiento cuesta $O(n\log n)$ y hay $O(n)$ operaciones de heap, cada una de $O(\log n)$:

$$
T(n)=O(n\log n).
$$

### 3.4 Ejemplo con tres aulas

Procesamos en orden de inicio:

$$
a=[9,10.5),\ b=[9.5,11),\ c=[10,12),\ d=[11,12.5),\ e=[11.5,13),\ f=[12,13).
$$

| Clase | Decisión |
|---|---|
| $a$ | Abrir aula 1 |
| $b$ | Abrir aula 2 |
| $c$ | Abrir aula 3 |
| $d$ | Reutilizar aula 1, libre desde 10.5 |
| $e$ | Reutilizar aula 2, libre desde 11 |
| $f$ | Reutilizar aula 3, libre desde 12 |

Entre las 10:00 y las 10:30 coinciden $a,b,c$, así que la profundidad es $3$. El algoritmo usa tres aulas: alcanza la cota inferior y, por tanto, es óptimo.

### 3.5 Prueba de optimalidad

Supongamos que el algoritmo abre el aula número $D$ para colocar una clase $j$. En ese momento:

- cada una de las $D-1$ aulas anteriores contiene una clase que termina después de $s_j$;
- como procesamos por inicio creciente, esas clases comenzaron a más tardar en $s_j$;
- junto con $j$, hay $D$ intervalos que se traslapan inmediatamente después de $s_j$.

Por la cota de profundidad, cualquier solución necesita al menos $D$ aulas. El algoritmo usa exactamente $D$, luego

$$
D=\operatorname{OPT}=d.
$$

Esta es una prueba estructural: en vez de comparar directamente con un óptimo desconocido, encontramos un testigo que obliga a cualquier solución a pagar el mismo costo que greedy.

---

## 4. Calendarización para minimizar la tardanza máxima

Esta parte corresponde a la anotación original de la clase: **earliest deadline first** y “emplearemos método de intercambio”.

### 4.1 Modelo

Hay un solo recurso que procesa un trabajo a la vez. Para cada trabajo $j$ conocemos:

- tiempo de procesamiento $t_j$;
- fecha límite $d_j$;
- inicio $s_j$;
- finalización $f_j=s_j+t_j$.

Siguiendo la convención de las diapositivas, la tardanza no negativa es

$$
\ell_j=\max\{0,f_j-d_j\}.
$$

El objetivo es minimizar

$$
L=\max_j\ell_j.
$$

> [!note] Terminología
> En algunos textos, *lateness* se define como $f_j-d_j$ y puede ser negativa, mientras que $\max\{0,f_j-d_j\}$ se llama *tardiness*. Las diapositivas usan “lateness” para la cantidad no negativa; aquí conservamos esa convención.

### 4.2 Por qué no conviene dejar tiempo ocioso

Existe un calendario óptimo sin huecos. Si un calendario tiene tiempo ocioso antes de terminar todos los trabajos, podemos desplazar hacia la izquierda los trabajos posteriores. Ninguna finalización aumenta, así que ninguna $\ell_j$ aumenta.

Por ello basta estudiar permutaciones de los trabajos colocadas consecutivamente desde el tiempo $0$.

### 4.3 Regla *earliest-deadline-first* (EDF)

Ordenamos por fecha límite creciente:

$$
d_1\le d_2\le\cdots\le d_n,
$$

y ejecutamos los trabajos en ese orden, sin tiempo ocioso.

```python
def earliest_deadline_first(trabajos):
    trabajos.sort(key=lambda j: j.deadline)
    tiempo = 0
    calendario = []

    for j in trabajos:
        inicio = tiempo
        fin = inicio + j.procesamiento
        calendario.append((j, inicio, fin))
        tiempo = fin

    return calendario
```

La complejidad está dominada por ordenar:

$$
T(n)=O(n\log n).
$$

### 4.4 Ejemplo de las diapositivas

| Trabajo $j$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| Procesamiento $t_j$ | 3 | 2 | 1 | 4 | 3 | 2 |
| Fecha límite $d_j$ | 6 | 8 | 9 | 9 | 14 | 15 |

El orden EDF es $1,2,3,4,5,6$.

| $j$ | Intervalo de ejecución | $f_j$ | $\ell_j$ |
|---:|---:|---:|---:|
| 1 | $[0,3)$ | 3 | 0 |
| 2 | $[3,5)$ | 5 | 0 |
| 3 | $[5,6)$ | 6 | 0 |
| 4 | $[6,10)$ | 10 | 1 |
| 5 | $[10,13)$ | 13 | 0 |
| 6 | $[13,15)$ | 15 | 0 |

Por tanto,

$$
L_{EDF}=1.
$$

En cambio, el orden $3,2,6,1,5,4$ termina el trabajo 4 en $15$ aunque su límite es $9$, y tiene $L=6$.

### 4.5 Inversiones

Numeremos los trabajos de modo que $d_1\le d_2\le\cdots\le d_n$. Una **inversión** es una pareja $i<j$ donde $j$ aparece antes que $i$ en el calendario. En otras palabras, un trabajo con fecha límite posterior se ejecuta antes que uno con fecha límite anterior.

Con un desempate fijo para fechas iguales, EDF es el calendario sin huecos y sin inversiones.

Además, si un calendario sin huecos tiene alguna inversión, tiene una **inversión adyacente**. Es el mismo hecho estructural que permite ordenar una permutación mediante intercambios vecinos.

### 4.6 Lema de intercambio

Consideremos dos trabajos adyacentes en orden invertido:

$$
j\;\to\;i,
\qquad d_i\le d_j.
$$

Los cambiamos a

$$
i\;\to\;j.
$$

Sea $C_i$ la finalización del segundo trabajo antes del intercambio. Después de intercambiar:

- $i$ termina antes que antes, así que $\ell_i'\le\ell_i$;
- $j$ termina exactamente en el antiguo $C_i$;
- como $d_i\le d_j$,

$$
\ell_j'
=\max\{0,C_i-d_j\}
\le\max\{0,C_i-d_i\}
=\ell_i.
$$

Los demás trabajos conservan su tiempo de finalización, porque el bloque intercambiado tiene la misma duración total. Por tanto, el intercambio:

1. elimina exactamente esa inversión adyacente; y
2. no aumenta la tardanza máxima.

### 4.7 Teorema de optimalidad de EDF

Tomemos un calendario óptimo $S^*$ que, entre todos los óptimos, tenga el menor número de inversiones. Podemos suponer que no tiene tiempo ocioso.

- Si $S^*$ no tiene inversiones, coincide con EDF, salvo empates equivalentes.
- Si tiene una inversión, también tiene una inversión adyacente.
- Por el lema anterior, podemos intercambiar esa pareja sin aumentar $L$ y reducir en uno el número de inversiones.

El resultado seguiría siendo óptimo pero tendría menos inversiones que $S^*$, una contradicción. Luego EDF es óptimo. $\square$

### 4.8 Registro del pizarrón

![[IMG_9075.heic]]

La fotografía resume la comparación entre varias calendarizaciones posibles mediante su `max lat.`. La cantidad encerrada representa la meta: demostrar que el calendario producido por EDF pertenece al conjunto de calendarizaciones con tardanza máxima mínima. El argumento de intercambio anterior formaliza exactamente esa intuición.

---

## 5. Pausa conceptual: las tres reglas no son intercambiables

| Problema | Decisión local correcta | Razón que preserva |
|---|---|---|
| Elegir muchos intervalos | Menor $f_j$ | Deja el mayor sufijo temporal disponible. |
| Colocar todos en pocas aulas | Menor $s_j$; reutilizar el aula que acaba antes | Cuando abre un aula nueva, exhibe un traslape inevitable. |
| Minimizar $L_{\max}$ | Menor $d_j$ | Quitar una inversión no aumenta la tardanza máxima. |
| Caché óptima fuera de línea | Próximo uso más lejano | Conservar lo que se necesitará antes nunca es peor. |
| Caminos más cortos desde $s$ (§8) | Nodo no explorado con menor $\pi(v)$ | Con $\ell_e\ge 0$, ningún desvío fuera de $S$ puede abaratar el camino. |

> [!tip] Pregunta de examen
> Antes de aplicar una regla aprendida, identifica con precisión el objetivo. Cambiar “elegir algunos” por “colocar todos”, agregar pesos o perder el conocimiento del futuro puede invalidar por completo la solución voraz.

---

## 6. Interludio de las diapositivas: Google Foo.bar

La presentación menciona el reto de transformar un entero positivo $n$ en $1$ con las operaciones:

- sumar $1$;
- restar $1$;
- dividir entre $2$ cuando $n$ es par.

Ejemplo mostrado:

$$
29\to28\to14\to7\to8\to4\to2\to1.
$$

Una regla útil es dividir cuando $n$ es par. Cuando $n>1$ es impar, se elige entre $n-1$ y $n+1$ buscando producir más factores de $2$; la excepción $n=3$ conviene resolverla como $3\to2\to1$. Esta observación conecta greedy con la representación binaria, aunque la prueba completa requiere justificar que la elección local minimiza el número total de operaciones.

---

## 7. Caché óptima fuera de línea

### 7.1 Modelo

Tenemos:

- una caché con capacidad para $k$ elementos;
- una secuencia de solicitudes $d_1,d_2,\ldots,d_m$;
- un **acierto** si el elemento solicitado ya está en caché;
- un **fallo** si no está: debe cargarse y, si la caché está llena, expulsar otro elemento.

El objetivo es minimizar el número de expulsiones.

Las diapositivas contrastan varias reglas:

- **FIFO:** expulsar lo que entró primero;
- **LIFO:** expulsar lo que entró más recientemente;
- **LRU:** expulsar lo que se usó menos recientemente;
- **LFU:** expulsar lo solicitado con menor frecuencia.

Estas reglas miran el pasado. El óptimo fuera de línea conoce toda la secuencia futura.

### 7.2 Algoritmo de Bélády o *farthest in future* (FF)

Ante un fallo con caché llena, para cada elemento almacenado buscamos su siguiente solicitud. FF expulsa el elemento cuyo próximo uso está **más lejos**, considerando “nunca vuelve a usarse” como distancia infinita.

```python
def farthest_in_future(cache, solicitudes, i):
    # solicitudes[i] produjo un fallo
    def proximo_uso(x):
        for j in range(i + 1, len(solicitudes)):
            if solicitudes[j] == x:
                return j
        return float("inf")

    return max(cache, key=proximo_uso)
```

Se llama “clarividente” porque no es implementable en línea sin conocer el futuro. Su valor es teórico: fija el costo óptimo contra el cual se comparan las políticas reales.

### 7.3 Ejemplo de las diapositivas

Capacidad $k=2$, caché inicial $\{a,b\}$ y solicitudes

$$
a,b,c,b,c,a,b.
$$

| Paso | Solicitud | Caché antes | Acción FF | Caché después |
|---:|---:|---|---|---|
| 1 | $a$ | $\{a,b\}$ | Acierto | $\{a,b\}$ |
| 2 | $b$ | $\{a,b\}$ | Acierto | $\{a,b\}$ |
| 3 | $c$ | $\{a,b\}$ | Expulsar $a$: $b$ se usa antes | $\{b,c\}$ |
| 4 | $b$ | $\{b,c\}$ | Acierto | $\{b,c\}$ |
| 5 | $c$ | $\{b,c\}$ | Acierto | $\{b,c\}$ |
| 6 | $a$ | $\{b,c\}$ | Expulsar $c$: ya no reaparece | $\{b,a\}$ |
| 7 | $b$ | $\{b,a\}$ | Acierto | $\{b,a\}$ |

Total: **dos expulsiones**, que es óptimo.

### 7.4 Calendarizaciones reducidas

Una calendarización de caché es **reducida** si introduce un elemento $d$ en el paso $j$ solamente cuando:

1. en ese paso se solicita $d$; y
2. $d$ no estaba ya en la caché.

Toda calendarización no reducida puede transformarse en una reducida sin aumentar las expulsiones:

- si introduce $d$ sin que se solicite, conviene conservar temporalmente el elemento expulsado hasta la primera solicitud relevante de $d$;
- si introduce una copia de $d$ cuando $d$ ya estaba, esa carga es innecesaria y también puede diferirse o eliminarse.

Esta normalización evita que una supuesta solución óptima haga movimientos anticipados que compliquen la comparación con FF.

### 7.5 Prueba de optimalidad por intercambio

El invariante de las diapositivas es:

> Existe una calendarización óptima y reducida $S$ que coincide con FF en sus expulsiones durante los primeros $j$ pasos.

**Base:** para $j=0$, cualquier óptimo reducido sirve.

**Paso inductivo:** antes de la solicitud $j+1$, $S$ y FF tienen el mismo contenido porque han tomado las mismas decisiones.

1. Si la solicitud es un acierto, ambos pueden continuar sin cambios.
2. Si es un fallo y expulsan el mismo elemento, el invariante se conserva.
3. Si es un fallo y FF expulsa $e$ mientras $S$ expulsa $f\ne e$, modificamos $S$ para que expulse $e$ y conserve $f$.

Por definición de FF, $f$ se solicita antes que $e$, o $e$ nunca vuelve a solicitarse. Hasta el primer paso donde la diferencia entre conservar $f$ o $e$ importe, la nueva calendarización imita a $S$. En ese punto se intercambian los papeles de $e$ y $f$ o se sincronizan de nuevo las cachés, sin añadir una expulsión. Si la modificación introdujo un movimiento no reducido, se aplica el lema de reducción.

Así obtenemos otro óptimo reducido que coincide con FF un paso más. Por inducción, existe un óptimo que coincide con FF en toda la secuencia; por tanto, FF es óptimo. $\square$

### 7.6 Fuera de línea frente a en línea

- **Fuera de línea:** toda la secuencia se conoce de antemano; FF es óptimo.
- **En línea:** cada solicitud se revela al llegar; es el escenario real de CPU, memoria, disco, web y navegador.

La presentación cierra con comparación competitiva. Para una secuencia $\sigma$ y caché de tamaño $k$:

$$
LRU(\sigma)\le k\,FF(\sigma)+k.
$$

Por eso se dice que LRU es $k$-competitivo. LIFO puede ser arbitrariamente malo y algoritmos aleatorios de marcado alcanzan una razón esperada $O(\log k)$.

---

## 8. Caminos más cortos: algoritmo de Dijkstra

> [!info] Origen de esta sección
> Material de *Greedy Algorithms II* (`04GreedyAlgorithmsII.pdf`, diapositivas 2–20) y Kleinberg–Tardos §4.4, incorporado a esta nota como continuación natural de la unidad voraz. La cola de prioridad que necesita se desarrolla en [[2026-10-20 ADA - bienary heap y heap sort|heap binario y heapsort]].

![[04GreedyAlgorithmsII.pdf#page=3]]

### 8.1 Problemas

Sea $G=(V,E)$ un **digrafo** con longitudes $\ell_e\ge 0$ en sus aristas. La longitud de un camino dirigido $P$ es

$$
\ell(P)=\sum_{e\in P}\ell_e,
$$

y la **distancia** $d(s,v)$ es la mínima longitud de un camino $s\rightsquigarrow v$ ($\infty$ si no existe).

- **Un par (*single-pair*):** dados $s,t\in V$, encontrar un camino dirigido más corto $s\rightsquigarrow t$.
- **Una fuente (*single-source*):** dado $s$, encontrar un camino más corto de $s$ a **todo** nodo. La unión de esos caminos puede elegirse como un **árbol de caminos más cortos** enraizado en $s$.

En el ejemplo de las diapositivas, con fuente $0$ y destino $6$,

$$
0\to4\to5\to2\to6:\qquad 9+4+1+11=25.
$$

| Variante | Qué se pide | Cómo se resuelve con Dijkstra |
|---|---|---|
| Una fuente | $s$ a todos | Directamente. |
| Un sumidero | Todos a $t$ | Dijkstra desde $t$ en el transpuesto $G^T$ (misma idea que en [[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas\|conectividad fuerte]]). |
| Fuente–sumidero | $s$ a $t$ | Dijkstra desde $s$, deteniéndose cuando se extrae $t$. Es la variante de un **GPS** (quiz 2). |
| Todos los pares | Entre todo par | $n$ ejecuciones de Dijkstra si $\ell_e\ge0$ (o Floyd–Warshall, más adelante). |

**Aplicaciones mencionadas:** PERT/CPM, ruteo en mapas, *seam carving*, navegación de robots, tipografía de $\LaTeX$ (cortes de línea), planeación de tráfico y protocolos de ruteo de redes (OSPF, BGP, RIP).

### 8.2 Calentamiento: ¿qué transformaciones preservan los caminos más cortos?

*Quiz 1 de las diapositivas.* Si cambiamos todas las longitudes:

- **Multiplicar por $17$:** $\ell'(P)=17\,\ell(P)$ para todo camino, así que el orden entre caminos no cambia. ✔
- **Sumar $17$:** $\ell'(P)=\ell(P)+17\,|P|$, donde $|P|$ es el número de aristas. Se penaliza a los caminos con más aristas. ✘

Contraejemplo de la suma: $s\to t$ con longitud $10$ y $s\to a\to t$ con $4+4=8$. El óptimo original pasa por $a$; tras sumar $17$, el directo cuesta $27$ y el otro $21+21=42$. **Respuesta: B.**

> [!tip] Idea útil para examen
> Escalar por una constante positiva preserva cualquier óptimo que sea suma de costos; sumar una constante solo es inocuo cuando **todas** las soluciones tienen el mismo número de elementos. Esta misma pregunta reaparece con árboles generadores mínimos, donde todo árbol tiene exactamente $n-1$ aristas.

### 8.3 La idea voraz

Dijkstra mantiene un conjunto $S$ de nodos **explorados**, para los cuales ya conoce

$$
d[u]=\text{longitud de un camino más corto } s\rightsquigarrow u .
$$

1. Inicializar $S\leftarrow\{s\}$ y $d[s]\leftarrow 0$.
2. Repetir mientras haya nodos alcanzables fuera de $S$: elegir el nodo $v\notin S$ que minimiza
$$
\pi(v)=\min_{e=(u,v):\,u\in S}\; d[u]+\ell_e ,
$$
   agregarlo a $S$ y fijar $d[v]\leftarrow\pi(v)$.
3. Para reconstruir caminos, guardar $\mathrm{pred}[v]\leftarrow e$, la arista que logra el mínimo.

$\pi(v)$ es la longitud del mejor camino que **se queda dentro de $S$** hasta el último paso y luego usa una sola arista para salir hacia $v$. La regla voraz es: *de todos los nodos en la frontera, fija primero el más cercano*.

> [!note] Dijkstra generaliza BFS
> Si todas las aristas miden $1$, $\pi$ coincide con la capa de BFS y la cola de prioridad se comporta como una cola FIFO: Dijkstra explora por capas, igual que [[Búsqueda en anchura|BFS]]. Con longitudes arbitrarias no negativas explora en orden **creciente de distancia**, como una onda que se expande desde $s$.

### 8.4 Prueba de corrección

> [!important] Invariante
> Para todo $u\in S$, $d[u]$ es la longitud de un camino más corto $s\rightsquigarrow u$.

**Demostración por inducción sobre $|S|$.**

**Base.** $|S|=1$: $S=\{s\}$ y $d[s]=0$, que es correcto porque las longitudes son no negativas.

**Paso inductivo.** Supongamos el invariante para $|S|=k\ge1$. Sea $v$ el siguiente nodo agregado y $(u,v)$ la arista que logra $\pi(v)$.

- Un camino más corto $s\rightsquigarrow u$ seguido de $(u,v)$ es un camino $s\rightsquigarrow v$ de longitud $\pi(v)$; por tanto, $d(s,v)\le\pi(v)$.
- Sea $P$ **cualquier otro** camino $s\rightsquigarrow v$. Como empieza en $S$ y termina fuera, tiene una **primera arista** $e=(x,y)$ que sale de $S$; llamemos $P'$ al subcamino de $s$ a $x$.

Entonces, ya al llegar a $y$, $P$ es al menos tan largo como $\pi(v)$:

$$
\ell(P)\;\ge\;\ell(P')+\ell_e\;\ge\;d[x]+\ell_e\;\ge\;\pi(y)\;\ge\;\pi(v).
$$

| Desigualdad | Justificación |
|---|---|
| $\ell(P)\ge\ell(P')+\ell_e$ | El resto del camino, de $y$ a $v$, tiene longitud $\ge0$ (**longitudes no negativas**). |
| $\ell(P')+\ell_e\ge d[x]+\ell_e$ | Hipótesis inductiva: $x\in S$ y $d[x]$ es su distancia. |
| $d[x]+\ell_e\ge\pi(y)$ | Definición de $\pi(y)$ como mínimo sobre aristas que salen de $S$. |
| $\pi(y)\ge\pi(v)$ | Dijkstra eligió $v$ y no $y$. |

Luego $d[v]=\pi(v)=d(s,v)$ y el invariante se conserva. $\square$

> [!warning] Dónde se usa $\ell_e\ge0$
> Solo en la primera desigualdad, pero es indispensable. Con $s\to a$ ($2$), $s\to b$ ($3$) y $b\to a$ ($-2$), Dijkstra fija $d[a]=2$ antes de explorar $b$, aunque $s\to b\to a$ cuesta $1$. El camino “se abarata” **después** de salir de $S$, justo lo que la prueba descarta. Para longitudes negativas se usan otros algoritmos (Bellman–Ford, programación dinámica).

Esta prueba es un argumento **greedy stays ahead**: en cada paso, la decisión de Dijkstra es al menos tan buena como la de cualquier otro camino, porque cualquier competidor ya “se quedó atrás” en el momento de cruzar la frontera de $S$.

### 8.5 Implementación eficiente

Calcular $\pi(v)$ directamente desde la definición en cada iteración sería caro. Las diapositivas proponen dos optimizaciones críticas:

1. **Mantener $\pi[v]$ explícitamente** para cada $v\notin S$. Como $S$ solo crece, $\pi(v)$ solo puede **disminuir**. Cuando $u$ entra a $S$, basta revisar sus aristas salientes $e=(u,v)$:
$$
\pi[v]\leftarrow\min\{\pi[v],\;\pi[u]+\ell_e\}.
$$
   A esta operación se le llama **relajar** la arista $(u,v)$. Para $u\in S$, $\pi[u]=d[u]$.
2. **Usar una cola de prioridad de mínimos** con llaves $\pi[\cdot]$ para elegir el nodo no explorado con menor $\pi$. Una vez que $u$ sale de la cola, $\pi[u]$ es definitiva.

```python
def dijkstra(G, s):
    pi = {v: float("inf") for v in G.V}
    pred = {v: None for v in G.V}
    pi[s] = 0

    pq = MinPQ()
    for v in G.V:
        pq.insert(v, pi[v])

    while not pq.is_empty():
        u = pq.del_min()                 # pi[u] ya es definitiva
        for v, largo in G.adj[u]:        # aristas que salen de u
            if pi[v] > pi[u] + largo:    # relajación
                pi[v] = pi[u] + largo
                pred[v] = u
                pq.decrease_key(v, pi[v])

    return pi, pred
```

> [!tip] Versión “perezosa” con `heapq`
> El `heapq` de Python no tiene DECREASE-KEY. La práctica común es **insertar de nuevo** $(\pi[v],v)$ y descartar al extraer las entradas obsoletas (`if d > pi[u]: continue`). La cola llega a tener $O(m)$ entradas, así que el costo es $O(m\log m)=O(m\log n)$, igual asintóticamente.

### 8.6 Traza del ejemplo de las diapositivas

Aristas: $0\to1\,(5)$, $0\to7\,(8)$, $0\to4\,(9)$, $1\to3\,(15)$, $1\to7\,(4)$, $1\to2\,(12)$, $7\to2\,(7)$, $7\to5\,(6)$, $4\to7\,(5)$, $4\to5\,(4)$, $4\to6\,(20)$, $5\to2\,(1)$, $5\to6\,(13)$, $2\to3\,(3)$, $2\to6\,(11)$, $3\to6\,(9)$. Fuente $s=0$.

| Paso | DEL-MIN | $\pi[u]$ | Relajaciones que mejoran | Cola después del paso |
|---:|:---:|---:|---|---|
| 1 | $0$ | $0$ | $\pi[1]=5,\ \pi[7]=8,\ \pi[4]=9$ | $1{:}5,\ 7{:}8,\ 4{:}9$ |
| 2 | $1$ | $5$ | $\pi[3]=20,\ \pi[2]=17$ ($1\to7$ da $9>8$) | $7{:}8,\ 4{:}9,\ 2{:}17,\ 3{:}20$ |
| 3 | $7$ | $8$ | $\pi[2]=15,\ \pi[5]=14$ | $4{:}9,\ 5{:}14,\ 2{:}15,\ 3{:}20$ |
| 4 | $4$ | $9$ | $\pi[5]=13,\ \pi[6]=29$ ($7$ ya en $S$) | $5{:}13,\ 2{:}15,\ 3{:}20,\ 6{:}29$ |
| 5 | $5$ | $13$ | $\pi[2]=14,\ \pi[6]=26$ | $2{:}14,\ 3{:}20,\ 6{:}26$ |
| 6 | $2$ | $14$ | $\pi[3]=17,\ \pi[6]=25$ | $3{:}17,\ 6{:}25$ |
| 7 | $3$ | $17$ | ninguna ($17+9=26>25$) | $6{:}25$ |
| 8 | $6$ | $25$ | — | vacía |

Árbol de caminos más cortos ($\mathrm{pred}$): $1\leftarrow0$, $7\leftarrow0$, $4\leftarrow0$, $5\leftarrow4$, $2\leftarrow5$, $3\leftarrow2$, $6\leftarrow2$. Observa que el nodo $2$ cambió de padre **tres veces** ($1$, luego $7$, luego $5$): cada DECREASE-KEY corrige una estimación provisional, pero nunca una distancia ya fijada.

### 8.7 ¿Qué cola de prioridad conviene?

El costo depende de la cola: Dijkstra hace $n$ INSERT, $n$ DELETE-MIN y a lo más $m$ DECREASE-KEY (una por arista).

| Cola de prioridad | INSERT | DELETE-MIN | DECREASE-KEY | Total |
|---|---:|---:|---:|---:|
| Arreglo indexado por nodo | $O(1)$ | $O(n)$ | $O(1)$ | $O(n^2)$ |
| [[2026-10-20 ADA - bienary heap y heap sort\|Heap binario]] | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(m\log n)$ |
| Heap $d$-ario (Johnson 1975) | $O(d\log_d n)$ | $O(d\log_d n)$ | $O(\log_d n)$ | $O(m\log_{m/n}n)$ |
| Heap de Fibonacci (Fredman–Tarjan 1984) | $O(1)$ | $O(\log n)^\dagger$ | $O(1)^\dagger$ | $O(m+n\log n)$ |
| Cola entera (Thorup 2004) | $O(1)$ | $O(\log\log n)$ | $O(1)$ | $O(m+n\log\log n)$ |

$^\dagger$ amortizado; se supone $m\ge n$.

- **Grafos densos** ($m=\Theta(n^2)$): el arreglo simple es óptimo, $O(n^2)$; el heap binario daría $O(n^2\log n)$.
- **Grafos dispersos** ($m=\Theta(n)$): el heap binario es mucho mejor, $O(n\log n)$ frente a $O(n^2)$.
- El heap de 4 vías vale la pena en situaciones críticas de desempeño.

### 8.8 Grafos no dirigidos

*Quiz 3.* Con aristas no dirigidas y longitudes positivas funcionan ambas ideas: **(A)** reemplazar cada arista por dos antiparalelas de la misma longitud y correr Dijkstra, o **(B)** al procesar $u$, relajar todas las aristas incidentes a $u$. **Respuesta: C.**

> [!note] Más allá de Dijkstra
> **Thorup (1999):** caminos más cortos desde una fuente en grafos **no dirigidos** con longitudes enteras positivas en $O(m)$. Evita el “cuello de botella de ordenar”: todo algoritmo tipo Dijkstra visita los nodos en orden de distancia y, en efecto, los ordena; el de Thorup **no** explora en orden creciente de distancia.

### 8.9 Extensiones: la misma prueba en otros “álgebras”

El algoritmo y su prueba se trasladan a problemas donde extender un camino nunca lo mejora:

| Problema | Valor de un camino | Actualización |
|---|---|---|
| Caminos más cortos | suma de longitudes (mínima) | $\pi[v]\le\pi[u]+\ell(u,v)$ |
| Capacidad máxima (*bottleneck*) | capacidad de la arista más estrecha (máxima) | $\pi[v]\ge\min\{\pi[u],c(u,v)\}$ |
| Confiabilidad máxima | producto de probabilidades $\gamma\in[0,1]$ (máximo) | $\pi[v]\ge\pi[u]\times\gamma(u,v)$ |

La estructura algebraica común es un **semianillo cerrado** (min-plus, cuello de botella, Viterbi, …). El análogo de $\ell_e\ge0$ es que “agregar una arista no mejora el valor”: sumar algo no negativo, tomar mínimo con una capacidad o multiplicar por $\gamma\le1$.

### 8.10 Reto: Google Foo.bar (quitar una pared)

Mapa $w\times h$ de ceros (pasillo) y unos (pared); se va de $(0,0)$ a $(w-1,h-1)$ y se permite **quitar una pared**. ¿Longitud del camino más corto?

**Idea:** construir un grafo de **estados** $(x,y,k)$, donde $k\in\{0,1\}$ indica si ya se usó la demolición. Desde $(x,y,k)$ se puede ir a una celda vecina libre conservando $k$, o a una celda vecina con pared solo si $k=0$, pasando a $k=1$. Todas las aristas miden $1$, así que basta **BFS** —Dijkstra con longitudes unitarias— sobre $2wh$ estados: tiempo $O(wh)$.

> [!tip] Patrón reutilizable
> “Camino más corto con $k$ excepciones” se resuelve duplicando el grafo en $k+1$ capas. El recurso a elegir (paredes, cupones, transbordos) se vuelve parte del estado.

### 8.11 Nota histórica

Edsger W. Dijkstra diseñó el algoritmo en 1956, según contaba, en unos veinte minutos sentado en la terraza de un café de Ámsterdam pensando en la ruta más corta de Rotterdam a Groningen; lo publicó en 1959. Las diapositivas cierran con una caricatura del *trolley problem* sobre un grafo: elegir un camino “más corto” también es una decisión con consecuencias.

### 8.12 Laboratorio: Dijkstra paso a paso

<iframe src="dijkstra-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - Cada **DEL-MIN** fija la distancia del nodo extraído (verde); cada **relajación** compara $\pi[v]$ con $\pi[u]+\ell_e$ y, si mejora, actualiza $\pi[v]$ y $\mathrm{pred}[v]$.
> - En la instancia de las diapositivas, el orden de extracción es $0,1,7,4,5,2,3,6$ con distancias $0,5,8,9,13,14,17,25$.
> - El preset con arista negativa muestra el momento exacto en que una arista mejoraría un nodo ya explorado: Dijkstra no puede corregirlo.

> [!example] Gemelo: algoritmo de Prim
> En *Greedy Algorithms II* (diapositiva 45), Prim para árboles generadores mínimos tiene **casi el mismo código**: solo cambia la llave. Dijkstra usa $\pi[v]=\min_{(u,v):u\in S}(d[u]+\ell_e)$ —distancia **desde $s$**—, mientras que Prim usa $\pi[v]=\min_{(u,v):u\in S}c_e$ —costo de la arista más barata **hacia $S$**—. Ambos corren en $O(m\log n)$ con heap binario.

---

## 9. Laboratorio interactivo

El recurso siguiente permite ejecutar las cuatro ideas principales paso a paso: aceptar o rechazar intervalos por finalización, abrir y reutilizar aulas por inicio, eliminar inversiones mediante intercambios y simular la caché de Bélády.

<iframe src="greedy-intervalos-tardanza-cache.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Selección:** ordenar por $f_j$ y aceptar si $s_j$ no precede al último final elegido.
> - **Partición:** ordenar por $s_j$ y reutilizar el aula con menor final; abrir una nueva solo si todas están ocupadas.
> - **Tardanza:** intercambiar una inversión adyacente $j,i$ con $d_i\le d_j$ no aumenta $L$.
> - **Caché:** ante un fallo, expulsar el elemento con siguiente uso más lejano.

---

## 10. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| “Greedy” significa escoger siempre el valor numéricamente menor o mayor. | La elección depende de una propiedad específica que debe demostrarse segura. |
| Selección y partición de intervalos usan el mismo orden. | Selección ordena por **fin**; partición ordena por **inicio**. |
| La profundidad es solo el número de intervalos. | Es el máximo número de intervalos simultáneamente activos. |
| EDF minimiza la suma de tardanzas o el tiempo promedio. | La prueba vista garantiza la **tardanza máxima** $L_{\max}$. |
| El trabajo más corto siempre debe ir primero. | Para $L_{\max}$, la regla correcta es fecha límite más temprana. |
| Bélády sirve como política real de caché. | Requiere conocer el futuro; es un óptimo fuera de línea y un punto de comparación. |
| La misma prueba vale al agregar pesos a intervalos. | El problema ponderado cambia y earliest-finish deja de ser óptimo. |
| Dijkstra funciona con cualquier longitud. | Requiere $\ell_e\ge0$; una arista negativa puede abaratar un camino después de fijar una distancia. |
| Sumar una constante a todas las aristas no cambia los caminos más cortos. | Penaliza caminos con más aristas; solo escalar por $c>0$ es seguro. |
| Cuando Dijkstra actualiza $\pi[v]$, esa ya es la distancia final. | Es provisional hasta que $v$ sale de la cola; puede bajar varias veces. |
| El heap binario siempre es la mejor cola para Dijkstra. | En grafos densos el arreglo simple da $O(n^2)$, mejor que $O(n^2\log n)$. |

---

## 11. Preguntas de autoevaluación

1. ¿Por qué terminar primero es seguro para selección de intervalos, pero empezar primero es la regla de partición?
2. ¿Qué testigo demuestra que una calendarización necesita al menos $d$ aulas?
3. ¿Por qué podemos eliminar tiempo ocioso al minimizar $L_{\max}$?
4. En el intercambio $j,i\to i,j$ con $d_i\le d_j$, ¿por qué la tardanza del nuevo $j$ queda acotada por la antigua tardanza de $i$?
5. ¿Qué significa que una calendarización de caché sea reducida?
6. Con caché $\{x,y,z\}$ y próximos usos de $x,y,z$ en $2,7,4$ pasos, respectivamente, ¿qué expulsa FF?
7. ¿Qué cambia si selección de intervalos maximiza peso total y no cardinalidad?
8. En la prueba de Dijkstra, ¿por qué se toma la **primera** arista de $P$ que sale de $S$ y no la última?
9. ¿Cuántas veces puede ejecutarse DECREASE-KEY sobre un mismo nodo y cuántas en total?
10. Para un grafo con $n=10^4$ nodos y $m=5\cdot10^7$ aristas, ¿usarías arreglo o heap binario?
11. Da un grafo de tres nodos donde Dijkstra falle por una arista negativa.

<details>
<summary>Respuestas breves</summary>

1. En selección queremos dejar el mayor espacio futuro y basta escoger algunos trabajos; en partición debemos colocar todos y necesitamos procesarlos antes de que su inicio pase.
2. Un instante contenido en $d$ intervalos; esos $d$ trabajos requieren recursos distintos simultáneamente.
3. Desplazar trabajos a la izquierda no aumenta ninguna finalización ni tardanza.
4. El nuevo $j$ termina donde antes terminaba $i$, y $d_i\le d_j$ implica $C_i-d_j\le C_i-d_i$.
5. Solo carga un elemento cuando se solicita y no estaba en caché.
6. Expulsa $y$, cuyo siguiente uso está más lejos.
7. Earliest-finish puede descartar un intervalo muy valioso; se requiere otra técnica, típicamente programación dinámica.
8. Porque solo para el prefijo $P'$, que vive dentro de $S$, podemos usar la hipótesis inductiva ($\ell(P')\ge d[x]$) y la definición de $\pi(y)$.
9. Un nodo $v$ puede bajar su llave una vez por cada arista que entra a él; en total, a lo más $m$ veces.
10. Es denso ($m\approx n^2/2$): el arreglo da $O(n^2)=10^8$, mientras que el heap da $O(m\log n)\approx 7\cdot10^8$.
11. $s\to a\,(2)$, $s\to b\,(3)$, $b\to a\,(-2)$: Dijkstra fija $d[a]=2$, pero $d(s,a)=1$.

</details>

---

## Puente visual y práctica de examen: Dijkstra (*Greedy II*, diapositivas 3–20)

![Frontera de Dijkstra: distancias definitivas y tentativas](dijkstra-frontera.svg)

La frontera separa vértices con distancia **definitiva** ($S$) de vértices con distancia **tentativa**. Al extraer el mínimo de la cola, toda ruta alternativa que aún no se exploró debe cruzar la frontera; con longitudes no negativas, ese desvío no puede mejorar la llave elegida. La ilustración deja visible qué afirma el invariante y qué papel cumple la hipótesis $\ell_e\ge 0$.

> [!example] Ejercicio de examen — traza, prueba y contraejemplo (8 puntos)
> Digrafo con aristas $s\to a:2$, $s\to b:5$, $a\to b:1$, $a\to c:4$, $b\to c:1$. **(a)** Traza `extract-min`, $\pi$ y predecesores desde $s$. **(b)** Enuncia el invariante y explica por qué un camino que sale de $S$ no mejora al vértice extraído. **(c)** Sustituye $a\to c:4$ por $a\to c:-4$ y explica qué paso de la prueba deja de ser válido; da un contraejemplo pequeño donde Dijkstra falle con una arista negativa. **(d)** Compara sumar $5$ a todas las aristas con multiplicarlas por $5$: ¿cuál transformación conserva todos los caminos mínimos?
>
> <details><summary>Comprobación</summary>
>
> (a) Orden $s,a,b,c$; distancias $0,2,3,4$; predecesores de $a,b,c$: $s,a,b$. (b) Para el primer cruce $(x,y)$ de cualquier ruta, el prefijo hasta $x$ ya tiene costo mínimo y el resto no puede reducir costo. (c) La desigualdad que descarta el sufijo falla. Contraejemplo: $s\to a:2$, $s\to b:1$, $a\to b:-2$: si $b$ se fija primero con $1$, el verdadero costo es $0$. (d) Multiplicar por una constante positiva conserva el orden de costos; sumar una constante por arista puede cambiarlo si las rutas tienen distinto número de aristas.
>
> </details>

---

## Conexiones

- **Clase anterior:** [[2026-09-22 ADA - cierre-de-grafos-y-greedy-monedas|cierre de grafos y cambio de monedas voraz]].
- **Concepto transversal:** [[Algoritmo voraz|algoritmo voraz]].
- **Recurso interactivo:** [[greedy-intervalos-tardanza-cache.htm|intervalos, tardanza y caché paso a paso]].
- **Técnica futura relacionada:** [[Programación dinámica|programación dinámica]], necesaria para selección de intervalos ponderados.
- **Dijkstra como BFS ponderado:** [[2026-09-03 ADA - grafos|grafos y recorridos]].
- **Cola de prioridad de Dijkstra:** [[2026-10-20 ADA - bienary heap y heap sort|heap binario y heapsort]].
- **Búsqueda informada (IA):** [[Algoritmo A estrella|A*]] es Dijkstra con la llave $\pi[v]+h(v)$, guiada por una heurística.
- **Recurso interactivo:** [[dijkstra-paso-a-paso.htm|Dijkstra paso a paso]].

## Bibliografía

1. Wayne, K. (2020). *Greedy Algorithms I* (`04GreedyAlgorithmsI.pdf`), diapositivas 9–52.
2. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley, secciones 4.1–4.3.
3. Bélády, L. A. (1966). “A Study of Replacement Algorithms for a Virtual-Storage Computer”. *IBM Systems Journal*, 5(2), 78–101.
4. Wayne, K. (2020). *Greedy Algorithms II* (`04GreedyAlgorithmsII.pdf`), diapositivas 2–20: algoritmo de Dijkstra.
5. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*, sección 4.4: caminos más cortos en un grafo.
6. Dijkstra, E. W. (1959). “A Note on Two Problems in Connexion with Graphs”. *Numerische Mathematik*, 1, 269–271.
7. Fredman, M. L. y Tarjan, R. E. (1987). “Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms”. *Journal of the ACM*, 34(3), 596–615.
8. Thorup, M. (1999). “Undirected Single-Source Shortest Paths with Positive Integer Weights in Linear Time”. *Journal of the ACM*, 46(3), 362–394.

## Resumen después de clase

La presentación se cerró con cuatro aplicaciones voraces y tres técnicas de prueba. La selección de intervalos elige el final más temprano y se justifica por intercambio; la partición procesa por inicio y alcanza la cota inferior dada por la profundidad; EDF elimina inversiones sin aumentar la tardanza máxima; y Bélády expulsa el elemento cuyo uso está más lejano, transformando mediante intercambios un óptimo para que coincida con greedy. La principal lección es que reglas locales muy parecidas pueden ser correctas o falsas según el objetivo exacto y la información disponible.

**Añadido (Dijkstra):** para caminos más cortos con longitudes no negativas, la regla voraz es fijar el nodo de la frontera con menor $\pi(v)$; el invariante “$d[u]$ es exacta para todo $u\in S$” se demuestra mostrando que cualquier otro camino ya es igual de largo al cruzar la frontera de $S$. Con una cola de prioridad corre en $O(m\log n)$ (heap binario) u $O(n^2)$ (arreglo).

## Acciones adicionales

- [ ] Rehacer sin consultar la prueba de intercambio de EDF.
- [ ] Construir un contraejemplo para “inicio más temprano” en selección de intervalos.
- [ ] Ejecutar manualmente la cola de prioridad de partición sobre una instancia nueva.
- [ ] Comparar LRU y FF sobre una secuencia que provoque decisiones distintas.
- [ ] Reescribir sin ver la nota la cadena de desigualdades de la prueba de Dijkstra y justificar cada paso.
- [ ] Ejecutar Dijkstra a mano desde el nodo $4$ del ejemplo de las diapositivas y verificar con el laboratorio.
- [ ] Implementar la versión perezosa con `heapq` y resolver el reto Foo.bar con BFS en capas.
