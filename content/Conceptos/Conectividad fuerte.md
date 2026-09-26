---
tipo: concepto
aliases:
  - Strong connectivity
  - Componente fuertemente conexa
  - SCC
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-09-08 ADA - biparticion-y-grafos-dirigidos|Clase: Bipartición y grafos dirigidos]]"
tags:
  - concepto
  - algoritmos
  - grafos
  - conectividad
---

# Conectividad fuerte

## Definición

En un [[Grafo dirigido|grafo dirigido]] $G = (V, E)$, dos nodos $u$ y $v$ son **mutuamente alcanzables** si existe un camino dirigido de $u$ a $v$ ($u \rightsquigarrow v$) y también existe un camino dirigido de $v$ a $u$ ($v \rightsquigarrow u$).

Un grafo dirigido $G$ es **fuertemente conexo** (*strongly connected*) si **todo par** de nodos $u, v \in V$ es mutuamente alcanzable.

Una **componente fuertemente conexa (SCC)** es un subconjunto maximal de vértices que son mutuamente alcanzables entre sí.

## Lema del nodo testigo

Determinar si todos los pares son mutuamente alcanzable requeriría evaluar $n(n-1)$ caminos dirigidos. El siguiente lema reduce drásticamente el problema a un solo nodo:

> [!important] Lema del Nodo Testigo
> Sea $s \in V$ cualquier nodo arbitrario. Un digrafo $G$ es fuertemente conexo **si y solo si**:
> 1. Todo nodo $v \in V$ es alcanzable desde $s$ en $G$ ($s \rightsquigarrow v$).
> 2. El nodo $s$ es alcanzable desde todo nodo $u \in V$ en $G$ ($u \rightsquigarrow s$).

### Demostración
- **$\implies$ (Necesidad):** Si todo par es mutuamente alcanzable, en particular lo es para el par $\{s, v\}$, por lo que se cumplen (1) y (2).
- **$\impliedby$ (Suficiencia):** Sean $u$ y $v$ dos nodos cualesquiera. Por la condición (2), existe un camino $u \rightsquigarrow s$. Por la condición (1), existe un camino $s \rightsquigarrow v$. Concatenando ambos caminos, obtenemos $u \rightsquigarrow s \rightsquigarrow v$, demostrando que $v$ es alcanzable desde $u$. De forma análoga se construye $v \rightsquigarrow s \rightsquigarrow u$.

## Algoritmo en tiempo lineal $O(m + n)$

El lema permite verificar conectividad fuerte mediante **dos búsquedas BFS (o DFS)** en tiempo $O(m + n)$:

```python
def es_fuertemente_conexo(G):
    s = elegir_un_nodo(G)
    
    # 1. BFS en G desde s
    alcanzados_desde_s = BFS(G, s)
    if len(alcanzados_desde_s) < n:
        return False
        
    # 2. BFS en G_rev desde s (equivale a buscar quienes alcanzan a s en G)
    G_rev = invertir_aristas(G)
    alcanzan_a_s = BFS(G_rev, s)
    if len(alcanzan_a_s) < n:
        return False
        
    return True
```

### Complejidad
- Invertir aristas para crear $G^{rev}$: $O(m + n)$.
- Cada recorrido BFS: $O(m + n)$.
- Tiempo total: $O(m + n)$. Espacio: $O(m + n)$.

## Teorema de Tarjan (1972)

Si $G$ no es fuertemente conexo, puede descomponerse en sus componentes fuertemente conexas disjuntas (SCCs).

> [!note] Teorema de Robert Tarjan (1972)
> Todas las componentes fuertemente conexas de un grafo dirigido pueden encontrarse en tiempo lineal $O(m + n)$ mediante un único recorrido DFS que gestiona números de descubrimiento y ancestros bajos (*low-link values*).

## Gráfica de componentes conexas ($G_{cc}$)

Al colapsar cada componente fuertemente conexa en un supernodo y trazar una arista entre componentes distintas siempre que exista al menos una arista dirigida entre sus nodos en $G$, se obtiene la [[Gráfica de componentes conexas|gráfica de componentes conexas ($G_{cc}$)]], la cual es **garantizadamente un DAG**.

## Relaciones

- Aplica sobre un: [[Grafo dirigido|Grafo dirigido]].
- Se verifica mediante: [[Búsqueda en anchura|Búsqueda en anchura (BFS)]] sobre $G$ y $G^{rev}$.
- Se descompone en: [[Gráfica de componentes conexas|Gráfica de componentes conexas ($G_{cc}$)]].
- Si un digrafo no tiene ciclos (y por ende no tiene componentes fuertes de más de 1 nodo), es un: [[Grafo dirigido acíclico|Grafo dirigido acíclico (DAG)]].

## Procedencia

- Clases: [[2026-09-08 ADA - biparticion-y-grafos-dirigidos|Clase del 8 de septiembre de 2026]] y [[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|Clase del 17 de septiembre de 2026]].
- Fuente: Kleinberg & Tardos, *Algorithm Design*, Sección 3.5; Tarjan, R. (1972), *Depth-First Search and Linear Graph Algorithms*, SIAM J. Comput.
