---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-09-22"
unidad: Grafos y algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[Búsqueda en anchura|Búsqueda en anchura (BFS)]]"
  - "[[Búsqueda en profundidad|Búsqueda en profundidad (DFS)]]"
  - "[[Conectividad fuerte|Conectividad fuerte]]"
  - "[[Gráfica de componentes conexas|Gráfica de componentes fuertemente conexas]]"
  - "[[Algoritmo voraz|Algoritmo voraz]]"
  - Cambio de monedas
referencias:
  - "[[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas]]"
  - "[[03Graphs.pdf]], diapositivas 40–43"
  - "[[04GreedyAlgorithmsI.pdf]], diapositivas 1–8"
  - "Kleinberg y Tardos, Algorithm Design, caps. 3–4"
tags:
  - clase
  - algoritmos
  - grafos
  - bfs
  - dfs
  - conectividad-fuerte
  - componentes-fuertemente-conexas
  - kosaraju
  - greedy
  - cambio-de-monedas
---

# Clase 11 · Cierre de grafos y comienzo de algoritmos voraces

![[03Graphs.pdf]]

![[04GreedyAlgorithmsI.pdf]]

> [!info] Alcance de la sesión
> La clase cerró la unidad de grafos con dos problemas relacionados pero distintos: **decidir si todo un digrafo es fuertemente conexo** mediante dos BFS y **encontrar todas sus componentes fuertemente conexas** mediante dos DFS (algoritmo de Kosaraju–Sharir). Después comenzó la unidad de algoritmos voraces con el problema de **cambio de monedas**.

## Pregunta central

¿Cómo aprovechamos recorridos lineales para revelar la estructura de un grafo dirigido y qué hace falta demostrar para que una elección local —como tomar siempre la moneda más grande posible— produzca una solución globalmente óptima?

> [!summary] Idea de la clase
> Un solo recorrido desde $s$ únicamente comprueba qué vértices alcanza $s$. Para certificar **conectividad fuerte** se ejecuta también el recorrido en el grafo transpuesto, con lo que se comprueba quiénes pueden llegar a $s$. Para obtener **todas** las componentes fuertes, Kosaraju ordena los vértices por tiempos de finalización de un DFS en $G$ y recorre $G^T$ en ese orden. En ambos casos el costo es $O(|V|+|E|)$. El cambio de monedas introduce el paradigma voraz: tomar la mayor moneda factible funciona para las denominaciones estadounidenses, pero no para cualquier sistema de monedas.

---

## 1. Recordatorio: alcanzabilidad y conectividad fuerte

En un digrafo $G=(V,E)$ escribimos $u\rightsquigarrow v$ cuando existe un camino dirigido de $u$ a $v$.

Dos vértices $u$ y $v$ son **mutuamente alcanzables** si

$$
u\rightsquigarrow v \quad\text{y}\quad v\rightsquigarrow u.
$$

El grafo es **fuertemente conexo** si esto se cumple para todo par de vértices.

### 1.1 Lema del vértice testigo

Sea $s$ cualquier vértice de $G$. Entonces $G$ es fuertemente conexo si y solo si:

1. todos los vértices son alcanzables desde $s$; y
2. $s$ es alcanzable desde todos los vértices.

**Demostración.** La implicación directa viene de la definición. Para la recíproca, sean $u,v\in V$. Por la segunda condición existe $u\rightsquigarrow s$ y por la primera existe $s\rightsquigarrow v$; al concatenarlos obtenemos $u\rightsquigarrow v$. Intercambiando $u$ y $v$ obtenemos $v\rightsquigarrow u$. $\square$

---

## 2. Prueba completa de conectividad fuerte con dos BFS

El **grafo transpuesto** de $G$ es

$$
G^T=(V,E^T),\qquad E^T=\{(v,u):(u,v)\in E\}.
$$

Invertir las aristas convierte la pregunta “¿quién puede llegar a $s$ en $G$?” en “¿a quién alcanza $s$ en $G^T$?”.

```python
def es_fuertemente_conexo(G):
    s = un_vertice_cualquiera(G)

    alcanzados_ida = BFS(G, s)
    if len(alcanzados_ida) != len(G.V):
        return False

    GT = transponer(G)
    alcanzados_vuelta = BFS(GT, s)
    return len(alcanzados_vuelta) == len(G.V)
```

### 2.1 Corrección

- Si el primer BFS no visita todo $V$, existe algún $v$ tal que $s\not\rightsquigarrow v$; por tanto, $G$ no es fuertemente conexo.
- Si el segundo BFS no visita todo $V$, existe algún $u$ tal que $s\not\rightsquigarrow u$ en $G^T$, equivalente a $u\not\rightsquigarrow s$ en $G$; tampoco hay conectividad fuerte.
- Si ambos recorridos visitan todo $V$, se satisfacen las dos condiciones del lema del vértice testigo; por tanto, $G$ sí es fuertemente conexo.

### 2.2 Complejidad

Con listas de adyacencia:

| Operación | Tiempo |
|---|---:|
| BFS en $G$ | $O(|V|+|E|)$ |
| Construcción de $G^T$ | $O(|V|+|E|)$ |
| BFS en $G^T$ | $O(|V|+|E|)$ |
| **Total** | **$O(|V|+|E|)$** |

Cada vértice y cada arista se procesa un número constante de veces.

> [!note] Qué resuelve y qué no
> Los dos BFS responden una pregunta de decisión: **“¿todo $G$ es fuertemente conexo?”**. Si la respuesta es no, todavía no indican por sí solos cuál es la partición completa de $V$ en componentes fuertes. Para eso se usa el algoritmo de la siguiente sección.

---

## 3. Componentes fuertemente conexas y condensación

Una **componente fuertemente conexa** (*strongly connected component*, SCC) es un subconjunto maximal $C\subseteq V$ cuyos vértices son mutuamente alcanzables.

La maximalidad importa: si se puede agregar otro vértice y conservar la alcanzabilidad mutua, el conjunto todavía no era una componente completa.

Las SCC forman una partición

$$
V=C_1\;\dot\cup\;C_2\;\dot\cup\;\cdots\;\dot\cup\;C_k.
$$

Al contraer cada $C_i$ a un solo supervértice se obtiene el **grafo de condensación** $G_{cc}$. Existe una arista $C_i\to C_j$ si alguna arista de $G$ sale de un vértice de $C_i$ y entra a uno de $C_j$.

> [!important] Propiedad estructural
> $G_{cc}$ siempre es un DAG. Si hubiera un ciclo entre varias componentes, todas serían mutuamente alcanzables y su unión sería una componente fuerte mayor, contradiciendo su maximalidad.

Esta propiedad es la razón profunda por la que los tiempos de finalización de DFS permiten recuperar las componentes en un orden seguro.

---

## 4. Algoritmo de Kosaraju–Sharir: todas las SCC con dos DFS

Las fotografías del pizarrón registran el siguiente procedimiento bajo el nombre `Comp.Fuertes(G)`.

### 4.1 Algoritmo

1. Crear una lista vacía $L$.
2. Ejecutar `DFS(G)`. Cuando termine `DFS-Visit(u)` y se fije $u.f$, insertar $u$ al **frente** de $L$.
3. Construir el grafo transpuesto $G^T$.
4. Ejecutar `DFS(G^T)`, eligiendo los vértices en el orden de $L$, es decir, en orden decreciente de tiempo de finalización en el primer DFS.
5. Los vértices descubiertos dentro de un mismo árbol del segundo bosque DFS forman una componente fuertemente conexa.

```python
def componentes_fuertes(G):
    L = []

    def al_finalizar(u):
        L.insert(0, u)          # orden decreciente de u.f

    DFS(G, al_finalizar=al_finalizar)
    GT = transponer(G)

    componentes = []
    visitado = set()
    for u in L:
        if u not in visitado:
            C = DFS_desde(GT, u, visitado)
            componentes.append(C)

    return componentes
```

> [!tip] Implementación eficiente de $L$
> En vez de insertar al frente de un arreglo —lo cual costaría $O(|V|)$ por inserción— se puede apilar cada vértice al finalizar y después recorrer la pila al revés, o usar una lista enlazada con inserción al frente en $O(1)$.

### 4.2 Por qué funciona

Para una componente $C$, definamos

$$
f(C)=\max\{u.f:u\in C\}.
$$

Si en el grafo de condensación existe una arista $C\to D$, entonces el primer DFS satisface $f(C)>f(D)$:

- si DFS descubre primero $C$, puede alcanzar $D$; la exploración de $D$ termina antes de que termine la de $C$;
- si descubre primero $D$, como $G_{cc}$ es un DAG no hay camino de regreso de $D$ a $C$; $D$ termina antes de que $C$ sea descubierto.

Por ello, la componente con mayor tiempo de finalización es una **fuente** de $G_{cc}$. Al transponer el grafo se convierte en un **sumidero** de $G_{cc}^T$. Un DFS iniciado allí:

1. puede alcanzar todos los vértices de su propia SCC, porque dentro de ella existen caminos en ambos sentidos; y
2. no puede escapar hacia otra SCC todavía no procesada, porque la componente es sumidero en la condensación transpuesta.

Así, el primer árbol del segundo DFS recupera exactamente una SCC. Al marcarla como visitada y repetir el argumento, se obtienen todas las demás. $\square$

### 4.3 Complejidad

$$
O(|V|+|E|)+O(|V|+|E|)+O(|V|+|E|)=O(|V|+|E|).
$$

El primer término corresponde al primer DFS, el segundo a construir $G^T$ y el tercero al segundo DFS. La memoria adicional también es $O(|V|+|E|)$ si se almacena explícitamente el transpuesto.

### 4.4 BFS frente a Kosaraju

| Pregunta | Herramienta | Resultado |
|---|---|---|
| ¿Todo $G$ es fuertemente conexo? | BFS en $G$ y BFS en $G^T$ | Sí/no |
| ¿Cuáles son todas las SCC de $G$? | DFS en $G$ y DFS en $G^T$ en orden decreciente de $f$ | Partición $C_1,\dots,C_k$ |
| ¿Cómo se relacionan las SCC? | Condensación $G_{cc}$ | Un DAG de componentes |

---

## 5. Lema del pizarrón: agregar una arista a un árbol crea un ciclo

Sea $T$ un árbol y sea $e=\{u,v\}$ una arista que no pertenece a $T$. Como en un árbol existe un único camino simple $P_{uv}$ entre $u$ y $v$, al agregar $e$ aparece el ciclo

$$
P_{uv}\cup\{e\}.
$$

Además, es el único ciclo nuevo: cualquier ciclo que use $e$ tendría que completar la conexión entre $u$ y $v$ con un camino en $T$, y ese camino es único.

Este lema explica por qué una gráfica conexa con más de $|V|-1$ aristas no puede ser un árbol y aparece como herramienta natural al comparar árboles producidos por BFS y DFS con la gráfica original.

> [!question] Ejercicio visto en pantalla
> Sea $G$ una gráfica no dirigida y conexa. Un BFS desde $s$ produce un árbol $T$ y un DFS produce un bosque $R$. Tras omitir la orientación de sus aristas, demostrar que si $\widehat T=\widehat R$, entonces $G=\widehat T=\widehat R$.

---

## 6. Laboratorio interactivo

El laboratorio permite comparar la prueba de conectividad fuerte con dos BFS, seguir las fases de Kosaraju y experimentar con sistemas de monedas donde la regla voraz acierta o falla.

<iframe src="bfs-kosaraju-y-cambio-monedas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Dos BFS:** el recorrido en $G$ verifica $s\rightsquigarrow v$ para todo $v$; el recorrido en $G^T$ verifica $v\rightsquigarrow s$.
> - **Kosaraju:** el primer DFS ordena por tiempos de finalización; el segundo DFS, sobre $G^T$, separa un árbol por cada SCC.
> - **Monedas:** el algoritmo toma la mayor denominación que no rebasa el resto; debe compararse con un óptimo para saber si el sistema es canónico.

---

## 7. Inicio de algoritmos voraces

Un [[Algoritmo voraz|algoritmo voraz]] construye una solución mediante una secuencia de elecciones **localmente mejores** y no reconsidera decisiones anteriores.

El esquema general es:

1. identificar las elecciones factibles;
2. aplicar una regla local para elegir una de ellas;
3. reducir el problema a una instancia más pequeña;
4. repetir hasta terminar.

La rapidez o naturalidad de la regla no basta para demostrar corrección. Cada problema necesita un argumento —por ejemplo, intercambio, inducción o *greedy stays ahead*— que conecte las elecciones locales con un óptimo global.

---

## 8. Problema de cambio de monedas

Dadas denominaciones positivas

$$
0<c_1<c_2<\cdots<c_n
$$

y una cantidad $x$, buscamos multiplicidades enteras $a_i\ge 0$ tales que

$$
\sum_{i=1}^{n}a_i c_i=x
$$

y que minimicen el número total de monedas

$$
\sum_{i=1}^{n}a_i.
$$

### 8.1 Algoritmo del cajero

En cada iteración se toma la moneda de mayor valor que no rebase la cantidad restante.

```python
def cambio_voraz(x, monedas):
    monedas = sorted(monedas)
    S = []

    while x > 0:
        candidatas = [c for c in monedas if c <= x]
        if not candidatas:
            return None          # no encontró una solución

        c = max(candidatas)
        S.append(c)
        x -= c

    return S
```

Si las denominaciones ya están ordenadas, puede implementarse avanzando de la moneda mayor a la menor. El tiempo depende del número de monedas devueltas; una implementación que toma cocientes usa $a_i=\lfloor x/c_i\rfloor$ y procesa cada denominación una sola vez.


### 8.2. Ejemplos con monedas estadounidenses

Consideremos el sistema de denominaciones

$$
C=\{1,5,10,25,100\},
$$

donde todos los valores están expresados en centavos.

El **algoritmo del cajero (*Cashier's Algorithm*)** es una estrategia voraz (*greedy*) que consiste en seleccionar repetidamente la moneda de mayor denominación que no exceda la cantidad restante.

**Ejemplo 1. Cambio de 34 centavos**

Comenzamos con $x=34$:

1. La mayor moneda que no supera 34 es 25. Quedan $34-25=9$.
2. La mayor moneda que no supera 9 es 5. Quedan $9-5=4$.
3. Solamente podemos utilizar monedas de 1, así que tomamos cuatro.

Obtenemos

$$
34=25+5+1+1+1+1.
$$

El algoritmo devuelve **6 monedas**.

**Ejemplo 2. Cambio de 2.89 dólares**

Expresamos primero la cantidad en centavos:

$$
x=289.
$$

El algoritmo selecciona:

- Dos monedas de 100 centavos.
- Tres monedas de 25 centavos.
- Una moneda de 10 centavos.
- Cuatro monedas de 1 centavo.

Por tanto,

$$
289=100+100+25+25+25+10+1+1+1+1.
$$

El algoritmo devuelve **10 monedas**.

Sin embargo, que las monedas seleccionadas sumen correctamente la cantidad solicitada no demuestra que la solución sea óptima.

**¿Qué significa que el algoritmo sea óptimo?**

Definamos

$$
\operatorname{OPT}(x)=
\text{mínimo número de monedas necesario para formar }x.
$$

Un algoritmo es óptimo para una cantidad $x$ cuando devuelve exactamente $\operatorname{OPT}(x)$ monedas.

Por tanto, debemos demostrar que **no existe otra combinación que utilice menos monedas para representar la misma cantidad**.

---

## 9. La regla voraz no es universal

El algoritmo del cajero utiliza una decisión local:

> Elegir siempre la moneda más grande que no supere la cantidad restante.

La pregunta fundamental es si esta decisión local garantiza obtener una solución globalmente óptima.

La respuesta general es **no**.

### 9.1. Puede devolver demasiadas monedas

Consideremos las denominaciones postales

$$
C=\{1,10,21,34,70,100,350,1225,1500\}
$$

y la cantidad

$$
x=140.
$$

El algoritmo del cajero selecciona primero la moneda de 100, porque es la mayor denominación que no supera 140.

Quedan 40 unidades, por lo que selecciona una moneda de 34.

Finalmente, quedan 6 unidades, que se representan utilizando seis monedas de 1.

Así,

$$
140=100+34+1+1+1+1+1+1.
$$

El algoritmo voraz utiliza **8 monedas**.

Sin embargo, existe otra combinación:

$$
140=70+70.
$$

Esta solución utiliza solamente **2 monedas**, por lo que es óptima: ninguna solución puede utilizar una sola moneda, ya que no existe una denominación de 140.

En consecuencia,

$$
\operatorname{Greedy}(140)=8
>
2=\operatorname{OPT}(140).
$$

Este ejemplo demuestra que **tomar la moneda más grande no necesariamente conduce a utilizar el menor número de monedas**.

### 9.2. Incluso puede quedarse atascado

Consideremos

$$
C=\{7,8,9\}
$$

y

$$
x=15.
$$

El algoritmo voraz selecciona primero la moneda de 9:

$$
15-9=6.
$$

Sin embargo, ninguna denominación disponible puede representar las 6 unidades restantes.

El algoritmo fracasa, aunque existe una solución factible:

$$
15=7+8.
$$

Esto significa que Greedy puede tomar una decisión local que impida completar la solución.

**Lección importante**

Si nuestro sistema contiene una moneda de valor 1, el algoritmo voraz siempre podrá representar cualquier cantidad entera no negativa.

Sin embargo, tener una moneda de valor 1 **no garantiza la optimalidad**.

Por otra parte, si no existe una moneda de valor 1, el algoritmo puede fracasar incluso cuando la cantidad sí puede representarse.

### 9.3. Un contraejemplo más sencillo

Consideremos ahora

$$
C=\{1,3,4\}
$$

y queremos representar

$$
x=6.
$$

**Solución voraz:**

El algoritmo toma primero 4, porque es la moneda más grande que no supera 6.

Quedan 2 unidades, que representa mediante dos monedas de 1:

$$
6=4+1+1.
$$

Utiliza 3 monedas.

**Solución óptima:**

$$
6=3+3.
$$

Utiliza 2 monedas.

Así,

$$
\operatorname{Greedy}(6)=3
>
2=\operatorname{OPT}(6).
$$

Este ejemplo muestra que elegir la moneda más grande puede impedir aprovechar una combinación más eficiente de monedas pequeñas.

**Conclusión:** la estrategia voraz no es universalmente óptima. Su correctitud depende de las relaciones aritméticas entre las denominaciones disponibles.

---

## 10. ¿Por qué sí funciona para las monedas estadounidenses?

Consideremos nuevamente

$$
C=\{1,5,10,25,100\}.
$$

Queremos demostrar el siguiente resultado:

**Teorema (optimalidad del algoritmo del cajero).**

Para cualquier cantidad entera no negativa $x$, el algoritmo del cajero devuelve una combinación de monedas que representa $x$ utilizando el menor número posible de monedas, si las denominaciones disponibles son $\{1,5,10,25,100\}$.

La demostración utiliza dos ideas:

1. **Argumentos de intercambio:** demostrar que ciertas combinaciones de monedas no pueden aparecer en una solución óptima, porque pueden sustituirse por otras que utilicen menos monedas.
2. **Inducción fuerte:** demostrar que, una vez elegida la primera moneda, el problema restante también se resuelve óptimamente.

### 10.1. Notación para las cantidades de monedas

Para evitar confundir los nombres de las monedas, utilizaremos la siguiente notación:

| Variable | Significado |
|---|---|
| $n_1$ | Número de monedas de 1 centavo |
| $n_5$ | Número de monedas de 5 centavos |
| $n_{10}$ | Número de monedas de 10 centavos |
| $n_{25}$ | Número de monedas de 25 centavos |
| $n_{100}$ | Número de monedas de 100 centavos |

De esta forma, cualquier combinación que represente una cantidad $x$ satisface

$$
x=n_1+5n_5+10n_{10}+25n_{25}+100n_{100},
$$

donde cada $n_i$ es un entero no negativo.

El número total de monedas utilizadas es

$$
N=n_1+n_5+n_{10}+n_{25}+n_{100}.
$$

Nuestro objetivo es minimizar $N$ sujeto a la restricción de que las monedas sumen $x$.

### 10.2. Restricciones que debe satisfacer cualquier solución óptima

Supongamos que tenemos una solución óptima, es decir, una combinación que utiliza el menor número posible de monedas.

Demostraremos que esta solución necesariamente satisface ciertas restricciones.

#### Restricción 1: como máximo cuatro monedas de 1

Supongamos que una solución óptima contiene cinco monedas de 1:

$$
1+1+1+1+1=5.
$$

Podemos sustituirlas por una sola moneda de 5.

Esta sustitución conserva el valor total, pero reduce el número de monedas de cinco a una.

Esto contradice que la solución original fuera óptima.

Por tanto,

$$
\boxed{n_1\leq4}.
$$

La misma conclusión aplica si tenemos más de cinco monedas, porque podríamos reemplazar cinco de ellas.

#### Restricción 2: como máximo una moneda de 5

Observemos que

$$
5+5=10.
$$

Si una solución contiene dos monedas de 5, podemos reemplazarlas por una moneda de 10.

Así, cualquier solución que contenga dos o más monedas de 5 no puede ser óptima.

Por tanto,

$$
\boxed{n_5\leq1}.
$$

#### Restricción 3: como máximo dos monedas entre las de 5 y 10

Esta restricción requiere un poco más de cuidado.

Queremos demostrar que

$$
\boxed{n_5+n_{10}\leq2}.
$$

Supongamos que una solución óptima contiene al menos tres monedas entre las denominaciones de 5 y 10.

Como ya demostramos que $n_5\leq1$, solamente existen dos posibilidades relevantes:

**Caso A. Al menos tres monedas de 10.**

Podemos reemplazar

$$
10+10+10=30
$$

por

$$
25+5=30.
$$

De esta manera sustituimos tres monedas por dos, contradiciendo la optimalidad.

**Caso B. Al menos dos monedas de 10 y una moneda de 5.**

En este caso,

$$
10+10+5=25.
$$

Podemos reemplazar tres monedas por una sola moneda de 25.

Nuevamente obtenemos una contradicción.

Por lo tanto, ninguna solución óptima puede contener tres o más monedas entre las denominaciones de 5 y 10:

$$
\boxed{n_5+n_{10}\leq2}.
$$

Esta restricción es especialmente importante porque permite demostrar que las monedas de 1, 5 y 10 no pueden acumular una cantidad de 25 centavos en una solución óptima.

#### Restricción 4: como máximo tres monedas de 25

Observemos que

$$
25+25+25+25=100.
$$

Podemos reemplazar cuatro monedas de 25 por una sola moneda de 100.

Por tanto,

$$
\boxed{n_{25}\leq3}.
$$

#### Resumen de restricciones

Toda solución óptima debe satisfacer:

| Restricción | Justificación |
|---|---|
| $n_1\leq4$ | Cinco monedas de 1 pueden sustituirse por una de 5. |
| $n_5\leq1$ | Dos monedas de 5 pueden sustituirse por una de 10. |
| $n_5+n_{10}\leq2$ | Tres monedas de 10 pueden sustituirse por 25+5; dos de 10 y una de 5 pueden sustituirse por 25. |
| $n_{25}\leq3$ | Cuatro monedas de 25 pueden sustituirse por una de 100. |
| $n_{100}$ sin cota global | No existe una denominación superior en este sistema que permita una sustitución directa. |

Observemos que estas restricciones son **necesarias para que una solución sea óptima**, pero satisfacerlas no es, por sí solo, una demostración de optimalidad.

Su importancia es que nos permitirán justificar la elección voraz.

### 10.3. Consecuencia: máximo valor alcanzable con monedas menores

Este es el paso fundamental de la demostración.

Supongamos que queremos representar una cantidad $x$ y que el algoritmo voraz selecciona una moneda de valor $c_k$.

Nos preguntamos:

> ¿Podría existir una solución óptima que no utilice ninguna moneda de valor $c_k$ y forme la cantidad usando solamente denominaciones menores?

Vamos a utilizar las restricciones anteriores para responder.

**Caso 1. La siguiente moneda es de 5 centavos.**

Si solamente utilizamos monedas de 1, cualquier solución óptima puede contener como máximo cuatro de ellas.

Por tanto,

$$
x_{\max}=4(1)=4.
$$

Esto significa que ninguna solución óptima puede representar una cantidad de al menos 5 centavos usando solamente monedas de 1.

Si $5\leq x<10$, toda solución óptima debe contener una moneda de 5.

**Caso 2. La siguiente moneda es de 10 centavos.**

Si solamente utilizamos monedas de 1 y 5, las restricciones son

$$
n_1\leq4,\qquad n_5\leq1.
$$

El máximo valor posible es

$$
x_{\max}=4(1)+1(5)=9.
$$

Entonces,

$$
\boxed{x_{\max}=9<10}.
$$

Por tanto, si $10\leq x<25$, cualquier solución óptima debe contener al menos una moneda de 10.

**Caso 3. La siguiente moneda es de 25 centavos.**

Ahora podemos utilizar monedas de 1, 5 y 10.

Sabemos que

$$
n_1\leq4
$$

y

$$
n_5+n_{10}\leq2.
$$

Para maximizar el valor total, conviene tomar las dos monedas de mayor valor permitido, es decir, dos monedas de 10.

Por tanto,

$$
x_{\max}=4(1)+2(10)=24.
$$

De modo que

$$
\boxed{x_{\max}=24<25}.
$$

¡Este resultado es fundamental!

Significa que ninguna solución óptima puede representar 25 centavos o más utilizando exclusivamente monedas de 1, 5 y 10.

En consecuencia, si

$$
25\leq x<100,
$$

toda solución óptima debe incluir al menos una moneda de 25.

**Caso 4. La siguiente moneda es de 100 centavos.**

Finalmente, consideremos las monedas de 1, 5, 10 y 25.

Sabemos que

$$
n_{25}\leq3.
$$

Además, el máximo valor que podemos obtener utilizando monedas menores que 25 es 24, como acabamos de demostrar.

Por tanto,

$$
x_{\max}=3(25)+24=99.
$$

Así,

$$
\boxed{x_{\max}=99<100}.
$$

Esto significa que ninguna solución óptima puede representar una cantidad de al menos 100 centavos utilizando exclusivamente monedas menores que 100.

Por tanto, para $x\geq100$, cualquier solución óptima debe contener al menos una moneda de 100.

#### Tabla resumen

| Moneda más grande disponible para $x$ | Máximo valor con monedas menores en una solución óptima | Consecuencia |
|---|---|---|
| 1 | No hay monedas menores | Se utiliza una moneda de 1 cuando $x=1,2,3,4$. |
| 5 | $4$ | Para $5\leq x<10$, toda solución óptima contiene una moneda de 5. |
| 10 | $4+5=9$ | Para $10\leq x<25$, toda solución óptima contiene una moneda de 10. |
| 25 | $20+4=24$ | Para $25\leq x<100$, toda solución óptima contiene una moneda de 25. |
| 100 | $75+20+4=99$ | Para $x\geq100$, toda solución óptima contiene una moneda de 100. |

La conclusión general es que, para las denominaciones estadounidenses, **la moneda más grande que no supera la cantidad $x$ debe aparecer en cualquier solución óptima**.

Esto demuestra que la primera decisión de Greedy es compatible con la optimalidad.

### 10.4. Demostración formal mediante inducción fuerte

Ahora podemos demostrar el teorema completo.

**Teorema.**

El algoritmo del cajero es óptimo para

$$
C=\{1,5,10,25,100\}.
$$

**Demostración.**

Procedemos mediante inducción fuerte sobre la cantidad entera no negativa $x$ que queremos representar.

**Caso base: $x=0$.**

Para representar una cantidad de cero centavos, no necesitamos seleccionar ninguna moneda.

Por tanto,

$$
\operatorname{Greedy}(0)=0=\operatorname{OPT}(0).
$$

El algoritmo es óptimo para $x=0$.

**Hipótesis inductiva.**

Supongamos que, para toda cantidad entera $y$ tal que

$$
0\leq y<x,
$$

el algoritmo del cajero produce una solución óptima:

$$
\operatorname{Greedy}(y)=\operatorname{OPT}(y).
$$

**Paso inductivo.**

Queremos demostrar que también es óptimo para la cantidad $x>0$.

Ordenemos las denominaciones:

$$
c_1=1,\quad c_2=5,\quad c_3=10,\quad c_4=25,\quad c_5=100.
$$

Sea $c_k$ la mayor denominación que satisface

$$
c_k\leq x.
$$

Por definición, Greedy selecciona primero una moneda de valor $c_k$.

Gracias a las restricciones demostradas en las secciones anteriores, sabemos que **toda solución óptima para $x$ contiene al menos una moneda de valor $c_k$**.

En particular, podemos tomar una solución óptima para $x$ y separar una de sus monedas de valor $c_k$.

El resto de las monedas representa la cantidad

$$
x'=x-c_k.
$$

Además, ese resto debe ser una solución óptima para $x'$.

¿Por qué?

Supongamos que no lo fuera. Entonces existiría otra combinación que representara $x'$ utilizando menos monedas. Podríamos sustituir el resto original por esa combinación más eficiente y conservar la moneda $c_k$. Así obtendríamos una solución para $x$ que utiliza menos monedas que la supuestamente óptima, lo cual es una contradicción.

Por tanto,
$$
\operatorname{OPT}(x)=1+\operatorname{OPT}(x-c_k).
$$
Pero, como

$$
0\leq x-c_k<x,
$$

podemos aplicar la hipótesis inductiva:

$$
\operatorname{OPT}(x-c_k)=\operatorname{Greedy}(x-c_k).
$$

Sustituyendo,

$$
\operatorname{OPT}(x)
=
1+\operatorname{Greedy}(x-c_k).
$$

Y precisamente esto es lo que hace el algoritmo del cajero: selecciona primero $c_k$ y después aplica la misma estrategia al resto.

Por tanto,

$$
\operatorname{Greedy}(x)
=
1+\operatorname{Greedy}(x-c_k).
$$

En consecuencia,

$$
\boxed{\operatorname{Greedy}(x)=\operatorname{OPT}(x)}.
$$

Así, por el principio de inducción fuerte, el algoritmo del cajero es óptimo para toda cantidad entera no negativa $x$.

$\square$

### 10.5. ¿Qué propiedades justificaron la demostración?

La prueba anterior utiliza dos propiedades fundamentales de los algoritmos voraces.

**1. Propiedad de elección voraz (*Greedy-choice property*)**

Es posible seleccionar la moneda de mayor denominación sin descartar todas las soluciones óptimas.

Para las monedas estadounidenses demostramos una afirmación todavía más fuerte:

> Toda solución óptima contiene una moneda de la mayor denominación que no supera la cantidad restante.

Por tanto, Greedy puede tomar esa moneda sin perder optimalidad.

**2. Subestructura óptima (*Optimal substructure*)**

Una vez que fijamos una moneda $c_k$ perteneciente a una solución óptima, las monedas restantes deben representar óptimamente la cantidad $x-c_k$.

Formalmente,

$$
\operatorname{OPT}(x)
=
1+\operatorname{OPT}(x-c_k).
$$

La primera propiedad justifica la elección local; la segunda permite resolver recursivamente el problema restante.

Es importante distinguirlas: un problema puede tener subestructura óptima y, sin embargo, no admitir una estrategia voraz óptima.

**Alcance de la demostración**

La demostración depende de relaciones aritméticas específicas entre las denominaciones $1,5,10,25,100$.

No prueba que Greedy funcione para cualquier sistema de monedas.

---

## 11. Generalización a otros sistemas de monedas

Hasta ahora demostramos la optimalidad para un sistema específico.

La pregunta natural es:

> ¿Qué condiciones deben cumplir las denominaciones para garantizar que Greedy sea óptimo?

Consideremos un sistema general de monedas

$$
C=\{c_1,c_2,\ldots,c_m\},
$$

ordenadas de manera creciente:

$$
1=c_1<c_2<\cdots<c_m.
$$

La presencia de una moneda de valor 1 garantiza que cualquier cantidad entera no negativa pueda representarse.

Sin embargo, para garantizar la optimalidad necesitamos propiedades adicionales.

### 11.1. Una condición suficiente: divisibilidad entre denominaciones consecutivas

Supongamos que cada denominación es un múltiplo entero de la anterior:

$$
\boxed{c_{i+1}=r_ic_i},
$$

donde

$$
r_i\in\mathbb{N},\qquad r_i\geq2.
$$

Por ejemplo, consideremos

$$
C=\{1,2,4,8,16,32\}.
$$

Cada denominación es el doble de la anterior.

Otro ejemplo es

$$
C=\{1,3,9,27,81\},
$$

donde cada denominación es el triple de la anterior.

Demostraremos que **el algoritmo del cajero es óptimo para cualquier sistema de monedas que satisfaga esta condición de divisibilidad**.

### 11.2. Demostración de la condición suficiente

Supongamos que

$$
c_{i+1}=r_ic_i
$$

para todas las denominaciones consecutivas.

En una solución óptima no podemos tener $r_i$ o más monedas de valor $c_i$, siempre que exista la denominación siguiente $c_{i+1}$.

Esto se debe a que

$$
\underbrace{c_i+c_i+\cdots+c_i}_{r_i\text{ veces}}
=
r_ic_i=c_{i+1}.
$$

Podríamos sustituir esas $r_i$ monedas por una sola moneda de valor $c_{i+1}$.

Por tanto, cualquier solución óptima satisface

$$
\boxed{n_i\leq r_i-1}
$$

para cada $i<m$, donde $n_i$ es el número de monedas de valor $c_i$.

Ahora consideremos una denominación $c_k$.

Queremos encontrar el máximo valor posible que pueden sumar las monedas menores que $c_k$ dentro de una solución óptima.

Utilizando las restricciones anteriores, tenemos

$$
S_{\max}
=
\sum_{i=1}^{k-1}(r_i-1)c_i.
$$

Como

$$
r_ic_i=c_{i+1},
$$

podemos escribir

$$
(r_i-1)c_i=c_{i+1}-c_i.
$$

Por tanto,

$$
S_{\max}
=
\sum_{i=1}^{k-1}(c_{i+1}-c_i).
$$

Al desarrollar la suma obtenemos

$$
S_{\max}
=
(c_2-c_1)+(c_3-c_2)+\cdots+(c_k-c_{k-1}).
$$

Observemos que los términos intermedios se cancelan.

Se trata de una **suma telescópica**, por lo que

$$
S_{\max}=c_k-c_1.
$$

Como $c_1=1$, concluimos que

$$
\boxed{S_{\max}=c_k-1<c_k}.
$$

Esto demuestra que, en una solución óptima, las monedas menores que $c_k$ no pueden sumar una cantidad igual o superior a $c_k$.

En consecuencia, si $c_k$ es la moneda más grande que no supera $x$, cualquier solución óptima para $x$ debe contener al menos una moneda de valor $c_k$.

Hemos demostrado exactamente la propiedad de elección voraz que necesitamos.

El resto de la demostración procede por inducción fuerte, de la misma manera que en el sistema estadounidense.

Por tanto,

$$
\boxed{\operatorname{Greedy}(x)=\operatorname{OPT}(x)}
$$

para toda cantidad entera no negativa $x$.

$\square$

### 11.3. ¿Esta condición es necesaria?

No.

La divisibilidad entre denominaciones consecutivas es una **condición suficiente, pero no necesaria**.

El sistema estadounidense

$$
C=\{1,5,10,25,100\}
$$

es un contraejemplo a su necesidad, porque

$$
25\neq r(10)
$$

para cualquier entero $r$.

Aun así, Greedy es óptimo para dicho sistema, como demostramos anteriormente.

En general, los sistemas de monedas para los que el algoritmo voraz siempre es óptimo se conocen como **sistemas canónicos de monedas** (*canonical coin systems*).

La condición de divisibilidad proporciona una familia de sistemas canónicos, pero no describe a todos ellos.

### 11.4. Caracterización mediante la elección voraz

Podemos establecer una caracterización más general.

Sea $C$ un sistema de denominaciones que contiene una moneda de valor 1.

Para una cantidad positiva $x$, definamos

$$
c_k=\max\{c\in C:c\leq x\}.
$$

Es decir, $c_k$ es la moneda que elegiría Greedy en su primera iteración.

Entonces, el algoritmo voraz es óptimo para todas las cantidades enteras no negativas **si y solo si**, para cada $x>0$, existe al menos una solución óptima que contiene una moneda de valor $c_k$.

La palabra *existe* es importante.

No necesitamos demostrar que todas las soluciones óptimas contienen esa moneda; basta con encontrar una solución óptima compatible con la decisión voraz.

**¿Por qué esta condición es suficiente?**

Si existe una solución óptima que contiene $c_k$, podemos fijar esa moneda.

Por subestructura óptima, el problema restante debe resolverse óptimamente.

Aplicando inducción fuerte, concluimos que Greedy también resuelve óptimamente ese resto y, por tanto, la cantidad completa.

**¿Por qué es necesaria?**

Si Greedy es óptimo para todas las cantidades, su solución para $x$ es una solución óptima.

Pero, por definición, Greedy selecciona primero la moneda $c_k$.

Por tanto, existe al menos una solución óptima que contiene esa moneda: la propia solución producida por Greedy.

Así, la condición es necesaria y suficiente.

Esta caracterización expresa la propiedad esencial detrás de la optimalidad, aunque no siempre es fácil verificarla directamente para un conjunto arbitrario de denominaciones.

---

## 12. ¿Cómo resolver el problema para denominaciones arbitrarias?

Si no podemos garantizar que Greedy sea óptimo, podemos utilizar **programación dinámica (*Dynamic Programming*)**.

Esta técnica aprovecha la subestructura óptima del problema sin asumir que la mejor elección local sea necesariamente la moneda más grande.

### 12.1. Definición del subproblema

Definamos

$$
\operatorname{OPT}(x)
=
\text{mínimo número de monedas para representar }x.
$$

Nuestro caso base es

$$
\operatorname{OPT}(0)=0.
$$

Para representar una cantidad $x>0$, podemos elegir como primera moneda cualquiera de las denominaciones $c\in C$ que satisfagan $c\leq x$.

Si elegimos la moneda $c$, entonces necesitamos representar la cantidad restante $x-c$.

El número mínimo de monedas utilizando esa primera elección es

$$
1+\operatorname{OPT}(x-c).
$$

Pero, a diferencia de Greedy, no elegimos necesariamente la moneda más grande.

Consideramos todas las monedas posibles y seleccionamos aquella que produzca el menor resultado.

Obtenemos la recurrencia

$$
\boxed{
\operatorname{OPT}(x)
=
1+
\min_{\substack{c\in C\\c\leq x}}
\operatorname{OPT}(x-c)
}.
$$

Si una cantidad no puede representarse, definimos

$$
\operatorname{OPT}(x)=+\infty.
$$

De esta forma, las elecciones que conducen a cantidades imposibles no se consideran soluciones factibles.

### 12.2. Ejemplo con un sistema donde Greedy falla

Consideremos

$$
C=\{1,3,4\}
$$

y la cantidad

$$
x=6.
$$

La recurrencia nos da

$$
\operatorname{OPT}(6)
=
1+\min\{
\operatorname{OPT}(5),
\operatorname{OPT}(3),
\operatorname{OPT}(2)
\}.
$$

Calculemos primero los valores necesarios:

$$
\begin{aligned}
\operatorname{OPT}(0)&=0,\\
\operatorname{OPT}(1)&=1,\\
\operatorname{OPT}(2)&=2,\\
\operatorname{OPT}(3)&=1,\\
\operatorname{OPT}(4)&=1,\\
\operatorname{OPT}(5)&=2.
\end{aligned}
$$

Por tanto,

$$
\operatorname{OPT}(6)
=
1+\min\{2,1,2\}.
$$

Concluimos que

$$
\boxed{\operatorname{OPT}(6)=2}.
$$

La elección óptima es tomar primero una moneda de 3 y después otra moneda de 3:

$$
6=3+3.
$$

En cambio, Greedy seleccionaría primero 4 y terminaría utilizando tres monedas.

### 12.3. Comparación entre Greedy y programación dinámica

| Propiedad | Greedy | Programación dinámica |
|---|---|---|
| Estrategia | Seleccionar la moneda más grande posible. | Evaluar todas las denominaciones posibles para cada subproblema. |
| Elección local | Fija inmediatamente una moneda. | Compara las alternativas mediante sus soluciones óptimas. |
| Optimalidad | Depende de las denominaciones. | Garantiza el mínimo número de monedas cuando existe una representación. |
| Memoria auxiliar | $O(1)$, sin contar la salida. | $O(x)$. |
| Tiempo | $O(m)$ al calcular cantidades por denominación mediante división entera. | $O(mx)$. |

Aquí $m$ es el número de denominaciones y $x$ la cantidad entera que queremos representar.

Si Greedy emite una moneda por iteración, su tiempo también depende del número de monedas producidas. La cota $O(m)$ corresponde a una implementación que agrupa las monedas de cada denominación.

La programación dinámica permite reconstruir la combinación óptima si almacenamos también qué moneda produjo la mejor decisión para cada cantidad.

---

## 13. Conclusiones generales

El problema del cambio de monedas permite comprender una distinción fundamental en el diseño de algoritmos.

**1. La factibilidad no implica optimalidad.**

Que un algoritmo produzca una combinación de monedas cuya suma sea la cantidad deseada no garantiza que utilice el menor número posible.

**2. Una decisión local aparentemente razonable puede ser incorrecta.**

Elegir siempre la moneda más grande funciona en algunos sistemas, pero puede producir soluciones subóptimas en otros.

**3. La correctitud de Greedy requiere una demostración.**

Para las monedas estadounidenses, la prueba utiliza argumentos de intercambio para demostrar que la moneda más grande disponible debe aparecer en cualquier solución óptima.

**4. La subestructura óptima no es suficiente para justificar Greedy.**

El problema del cambio de monedas siempre presenta subestructura óptima, pero no todos los sistemas permiten una elección voraz óptima.

**5. La divisibilidad proporciona una condición suficiente de optimalidad.**

Si cada denominación es un múltiplo entero de la anterior y existe una moneda de valor 1, el algoritmo voraz siempre es óptimo.

**6. La programación dinámica resuelve el problema general.**

Cuando no tenemos garantías sobre la estrategia voraz, podemos considerar todas las primeras elecciones posibles y utilizar una recurrencia para encontrar la solución óptima.

La idea matemática central puede resumirse en una pregunta:

> ¿Podemos demostrar que la primera decisión del algoritmo voraz pertenece a alguna solución óptima?

Si la respuesta es afirmativa para todas las subinstancias, y los problemas restantes conservan la subestructura óptima, podemos justificar formalmente la estrategia Greedy mediante inducción.

---

## 11. Errores conceptuales frecuentes

| Error | Corrección |
|---|---|
| Un BFS desde $s$ basta para comprobar conectividad fuerte. | Solo prueba que $s$ alcanza a todos; falta verificar que todos alcanzan a $s$. |
| Invertir aristas cambia las SCC. | No: dentro de una SCC siguen existiendo caminos en ambos sentidos. Lo que se invierte es el DAG de condensación. |
| Cada ejecución de DFS en $G^T$ produce una SCC sin importar el orden. | El orden decreciente de finalización del primer DFS es esencial. |
| Todo algoritmo voraz es óptimo. | Una regla voraz solo es una heurística hasta que se demuestra su propiedad de elección segura. |
| Si existe una moneda de $1$, greedy es óptimo. | La moneda de $1$ garantiza factibilidad, no optimalidad. |

---

## 12. Preguntas de autoevaluación

1. ¿Por qué un recorrido en $G^T$ desde $s$ representa a los vértices que pueden alcanzar $s$ en $G$?
2. ¿Qué diferencia de salida hay entre la prueba con dos BFS y Kosaraju–Sharir?
3. ¿Por qué el segundo DFS de Kosaraju debe procesar vértices en orden decreciente de $u.f$?
4. Para $C=\{1,3,4\}$ y $x=6$, ¿qué devuelve greedy y cuál es el óptimo?
5. ¿Qué parte de la prueba para monedas estadounidenses deja de ser válida al cambiar las denominaciones?

<details>
<summary>Respuestas breves</summary>

1. Cada camino $v\rightsquigarrow s$ en $G$ se convierte, al invertir sus aristas, en un camino $s\rightsquigarrow v$ en $G^T$.
2. Dos BFS devuelven una decisión global; Kosaraju devuelve la partición completa en SCC.
3. Ese orden hace que cada nuevo DFS comience en una componente que no puede escapar hacia otra componente no procesada en $G^T$.
4. Greedy: $4+1+1$ (3 monedas). Óptimo: $3+3$ (2 monedas).
5. Las cotas de reemplazo entre monedas menores y la siguiente denominación dependen de los valores concretos del sistema estadounidense.

</details>

---

## Conexiones

- **Clase anterior:** [[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|TopoSort con DFS, SCC y condensación]].
- **Antecedente de BFS:** [[2026-09-08 ADA - biparticion-y-grafos-dirigidos|Bipartición y conectividad en grafos dirigidos]].
- **Recurso interactivo:** [[bfs-kosaraju-y-cambio-monedas.htm|Dos BFS, Kosaraju y cambio de monedas]].
- **Siguiente bloque de la presentación:** selección de intervalos por tiempo de finalización más temprano.

## Bibliografía

1. Kleinberg, J. y Tardos, É. (2006). *Algorithm Design*. Pearson/Addison-Wesley. Cap. 3, conectividad en grafos dirigidos; cap. 4, algoritmos voraces.
2. Wayne, K. *Graphs* (`03Graphs.pdf`), diapositivas 40–43: alcanzabilidad dirigida, conectividad fuerte y componentes fuertes.
3. Wayne, K. (2020). *Greedy Algorithms I* (`04GreedyAlgorithmsI.pdf`), diapositivas 1–8: cambio de monedas, contraejemplos y optimalidad para denominaciones estadounidenses.
4. Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2009). *Introduction to Algorithms*, 3.ª ed. MIT Press. Secciones 22.2 y 22.5.
5. Sharir, M. (1981). “A strong-connectivity algorithm and its applications in data flow analysis”. *Computers & Mathematics with Applications*, 7(1), 67–72.
6. Tarjan, R. E. (1972). “Depth-First Search and Linear Graph Algorithms”. *SIAM Journal on Computing*, 1(2), 146–160.

## Resumen después de clase

La conectividad fuerte puede certificarse en tiempo lineal con un recorrido en $G$ y otro en $G^T$. Para descomponer un digrafo arbitrario, Kosaraju combina los tiempos de finalización de un primer DFS con un segundo DFS sobre el transpuesto, obteniendo una SCC por árbol. La condensación de esas componentes siempre es un DAG. El cambio de monedas mostró la idea y el riesgo central de greedy: una elección local debe justificarse con propiedades específicas del problema; no basta con que parezca natural.

## Acciones adicionales

- [ ] Resolver formalmente el ejercicio de la Tarea 3 sobre la coincidencia entre los árboles de BFS y DFS.
- [ ] Practicar una traza manual de Kosaraju indicando $d[u]$, $f[u]$, $L$ y los árboles del segundo DFS.
- [ ] Buscar otro sistema de monedas no canónico y construir un contraejemplo mínimo para greedy.
