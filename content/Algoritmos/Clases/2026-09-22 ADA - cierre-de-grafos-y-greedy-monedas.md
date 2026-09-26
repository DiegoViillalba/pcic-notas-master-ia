---
tipo: clase
materia: "[[01_Materias/Algoritmos/Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-09-22"
unidad: Grafos y algoritmos voraces
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[03_Conceptos/Búsqueda en anchura|Búsqueda en anchura (BFS)]]"
  - "[[03_Conceptos/Búsqueda en profundidad|Búsqueda en profundidad (DFS)]]"
  - "[[03_Conceptos/Conectividad fuerte|Conectividad fuerte]]"
  - "[[03_Conceptos/Gráfica de componentes conexas|Gráfica de componentes fuertemente conexas]]"
  - "[[03_Conceptos/Algoritmo voraz|Algoritmo voraz]]"
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

<iframe src="../../algoritmos/recursos/bfs-kosaraju-y-cambio-monedas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

> [!note] Si el recurso no carga
> - **Dos BFS:** el recorrido en $G$ verifica $s\rightsquigarrow v$ para todo $v$; el recorrido en $G^T$ verifica $v\rightsquigarrow s$.
> - **Kosaraju:** el primer DFS ordena por tiempos de finalización; el segundo DFS, sobre $G^T$, separa un árbol por cada SCC.
> - **Monedas:** el algoritmo toma la mayor denominación que no rebasa el resto; debe compararse con un óptimo para saber si el sistema es canónico.

---

## 7. Inicio de algoritmos voraces

Un [[03_Conceptos/Algoritmo voraz|algoritmo voraz]] construye una solución mediante una secuencia de elecciones **localmente mejores** y no reconsidera decisiones anteriores.

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

### 8.2 Ejemplos con monedas estadounidenses

Para $C=\{1,5,10,25,100\}$ centavos:

$$
34=25+5+1+1+1+1
$$

El algoritmo devuelve $6$ monedas.

Para $\$2.89$:

$$
289=100+100+25+25+25+10+1+1+1+1,
$$

por lo que devuelve $10$ monedas.

---

## 9. La regla voraz no es universal

### 9.1 Puede devolver demasiadas monedas

Con las denominaciones postales

$$
C=\{1,10,21,34,70,100,350,1225,1500\}
$$

y $x=140$, el algoritmo del cajero produce

$$
140=100+34+1+1+1+1+1+1
$$

con $8$ monedas. Sin embargo, la solución óptima es

$$
140=70+70,
$$

con solo $2$ monedas.

### 9.2 Incluso puede quedarse atascada

Con $C=\{7,8,9\}$ y $x=15$, la regla elige primero $9$ y deja un residuo de $6$, que no puede pagarse. No obstante,

$$
15=7+8
$$

sí es una solución factible.

> [!important] Lección
> Tener una moneda de valor $1$ garantiza que la estrategia siempre termina con una representación, pero **no** garantiza que use el menor número de monedas. Sin moneda de valor $1$, la estrategia puede fracasar aun cuando exista una solución.

---

## 10. Por qué sí funciona para las monedas estadounidenses

Consideremos $C=\{1,5,10,25,100\}$. Toda solución óptima satisface estas restricciones:

| Restricción | Justificación por mejora local |
|---|---|
| $P\le 4$ | Cinco monedas de $1$ se reemplazan por una de $5$. |
| $N\le 1$ | Dos monedas de $5$ se reemplazan por una de $10$. |
| $Q\le 3$ | Cuatro monedas de $25$ se reemplazan por una de $100$. |
| $N+D\le 2$ | Tres monedas de $10$ se reemplazan por $25+5$; dos de $10$ y una de $5$ se reemplazan por $25$. |

Aquí $P,N,D,Q$ denotan el número de monedas de $1,5,10,25$ centavos, respectivamente.

### 10.1 Consecuencia de las restricciones

En una solución óptima que todavía no usa la siguiente denominación, el máximo valor posible es:

| Moneda que elige greedy | Máximo con monedas menores en un óptimo | Conclusión |
|---:|---:|---|
| $5$ | $4$ | Si $x\ge5$, algún $5$ es obligatorio. |
| $10$ | $4+5=9$ | Si $x\ge10$, algún $10$ es obligatorio. |
| $25$ | $20+4=24$ | Si $x\ge25$, algún $25$ es obligatorio. |
| $100$ | $75+20+4=99$ | Si $x\ge100$, algún $100$ es obligatorio. |

### 10.2 Prueba inductiva de optimalidad

Sea $c_k$ la mayor denominación tal que $c_k\le x$. El algoritmo voraz elige $c_k$.

Las cotas anteriores demuestran que cualquier solución óptima para $x$ también debe contener al menos una moneda $c_k$: usando solo denominaciones menores no podría alcanzarse $x$ sin violar una de las restricciones de optimalidad.

Después de fijar esa moneda, queda la subinstancia $x-c_k$. Por hipótesis inductiva, el algoritmo resuelve óptimamente ese resto. Por tanto, la solución completa también es óptima. $\square$

> [!warning] Alcance de la prueba
> La demostración depende de relaciones aritméticas específicas entre $1,5,10,25$ y $100$. No prueba que la estrategia funcione para cualquier conjunto de denominaciones.

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
- **Recurso interactivo:** [[01_Materias/Algoritmos/Recursos/bfs-kosaraju-y-cambio-monedas.html|Dos BFS, Kosaraju y cambio de monedas]].
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
