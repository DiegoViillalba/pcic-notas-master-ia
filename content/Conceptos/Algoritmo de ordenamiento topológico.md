---
tipo: concepto
aliases:
  - Topological sorting algorithm
  - Algoritmo de Kahn
  - TopoSort DFS
  - Topo-Sort
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-09-10 ADA - DAGs-y-ordenamiento-topologico|Clase: DAGs y ordenamiento topológico]]"
  - "[[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|Clase: TopoSort con DFS y Componentes Fuertes]]"
tags:
  - concepto
  - algoritmos
  - grafos
  - dag
  - complejidad
---

# Algoritmo de ordenamiento topológico

## Definición

Procedimiento algorítmico para computar un [[Ordenamiento topológico|ordenamiento topológico]] en un [[Grafo dirigido acíclico|DAG]] o determinar que la gráfica contiene un ciclo dirigido (NO-DAG).

En el curso de Análisis y Diseño de Algoritmos se estudian y contrastan cuatro formulaciones formales: la versión recursiva, la versión iterativa ingenua, la versión iterativa mejorada (algoritmo de Kahn) y la versión basada en búsqueda en profundidad (`TopoSort-DFS`).

---

## 1. Versión Recursiva (`Topo-Recursivo`)

Basada directamente en la demostración constructiva por inducción:

```python
def Topo_Recursivo(G):
    if |V| == 1:
        return [v]
    else:
        v = buscar_vertice_sin_aristas_de_entrada(G)
        if v is None:
            return "NO-DAG"   # Existe al menos un ciclo
        G_prima = G.eliminar_vertice_y_aristas_salientes(v)
        return [v] + Topo_Recursivo(G_prima)
```

---

## 2. Versión Iterativa Ingenua (`Topo-Iterativo`)

Elimina la recursión pero realiza una búsqueda exhaustiva del vértice fuente en cada paso:

```python
def Topo_Iterativo(G):
    L = []                                                # O(1)
    while G.tiene_vertices():                             # Se repite n veces
        v = buscar_vertice_sin_aristas_de_entrada(G)      # O(n + m) cada vez
        if v is None:
            return "NO-DAG"
        L.append(v)                                       # O(1)
        G = G.eliminar_vertice_y_aristas_salientes(v)     # O(1)
    return L                                              # O(1)
```

### Análisis formal de complejidad:
- **Tiempo de ejecución:** El bucle se ejecuta $n$ veces. En cada iteración, buscar un vértice con $\text{in-degree} = 0$ sin estructuras auxiliares requiere escanear la gráfica completa en $O(n + m)$ operaciones:
  $$T(n, m) = (n + 1) \cdot O(n) + n \cdot O(n + m) = O(n^2 + nm)$$
- **Espacio de memoria:** $S(n, m) = O(n)$ para la lista $L$.

---

## 3. Versión Iterativa Mejorada / Algoritmo de Kahn (`Topo-Iterativo-Mejorado`)

Optimiza el tiempo evitando reescanear la gráfica mediante el mantenimiento dinámico de:
1. Un arreglo `in-degree[w]` con el número de aristas de entrada pendientes de cada nodo.
2. Una estructura de datos $S$ (cola o pila) que almacena exclusivamente los nodos listos con `in-degree == 0`.

```python
def Topo_Iterativo_Mejorado(G):
    S = Cola()
    L = []
    
    # 1. Inicialización en O(n + m)
    for v in G.vertices:
        in_degree[v] = G.aristas_entrantes(v)
        if in_degree[v] == 0:
            S.meter(v)
            
    # 2. Bucle principal en O(n + m)
    while not S.esta_vacia():
        v = S.sacar()
        L.append(v)
        for (v, w) in G.aristas_salientes(v):
            in_degree[w] -= 1
            if in_degree[w] == 0:
                S.meter(w)
                
    # 3. Detección de ciclos
    if len(L) < n:
        return "NO-DAG"   # Quedaron nodos atrapados en ciclos
    else:
        return L
```

### Análisis formal de complejidad:
- **Inicialización:** Escanear la gráfica para calcular `in-degree` toma $O(n + m)$.
- **Extracción de vértices:** Cada vértice entra y sale de la cola $S$ exactamente una vez $\implies O(n)$ acumulado.
- **Actualización de aristas:** Cada arista $(v, w)$ se recorre una sola vez cuando se procesa su origen $v$. El decremento `in-degree[w] -= 1` toma $O(1)$ por arista $\implies O(m)$ acumulado.
- **Tiempo total:**
  $$T(n, m) = O(n + m)$$
- **Espacio total:**
  $$S(n, m) = O(n) \quad \text{para almacenar la cola } S \text{ y el vector } \text{in-degree}$$

---

## 4. Versión con Búsqueda en Profundidad (`TopoSort-DFS`)

Basada en los tiempos de finalización ($u.f$) de [[Búsqueda en profundidad|DFS]]:

```python
def TopoSort_DFS(G):
    L = []
    for u in G.V:
        color[u] = BLANCO
    tiempo = 0
    
    for u in G.V:
        if color[u] == BLANCO:
            DFS_Visit(G, u, tiempo, L)
    return L

def DFS_Visit(G, u, tiempo, L):
    tiempo += 1; u.d = tiempo; color[u] = GRIS
    for v in G.Adj[u]:
        if color[v] == BLANCO:
            DFS_Visit(G, v, tiempo, L)
        elif color[v] == GRIS:
            return "NO-DAG"   # Arista hacia atrás detectada
    tiempo += 1; u.f = tiempo; color[u] = NEGRO
    L.insertar_al_frente(u)   # Orden decreciente de u.f
```

### Lema de corrección:
Para toda arista $(u, v) \in E$, se cumple $u.f > v.f$:
1. $v$ gris: imposible en un DAG (arista hacia atrás $\implies$ ciclo).
2. $v$ blanco: la llamada a $v$ concluye antes de retornar a $u \implies u.f > v.f$.
3. $v$ negro: $v$ ya concluyó en el pasado ($v.f < \text{actual} < u.f$) $\implies u.f > v.f$.

Por ende, ordenar por tiempos de finalización decrecientes ($v_1.f > v_2.f > \dots > v_n.f$) garantiza un orden topológico estricto en tiempo $O(n + m)$ y espacio $O(n)$.

## Detección formal de ciclos

- En **Kahn:** Al vaciarse la cola $S$, la lista tiene longitud $|L| < n$.
- En **DFS:** Al examinar una arista $(u, v)$, el destino $v$ tiene color GRIS (arista hacia atrás).

## Relaciones

- Genera un: [[Ordenamiento topológico|Ordenamiento topológico]].
- Opera exclusivamente sobre un: [[Grafo dirigido acíclico|Grafo dirigido acíclico (DAG)]].
- Se implementa mediante: [[Búsqueda en profundidad|Búsqueda en profundidad (DFS)]] o [[Búsqueda en anchura|Búsqueda en anchura (BFS) / Kahn]].
- Se aplica a macro-escala sobre: [[Gráfica de componentes conexas|Gráfica de componentes conexas ($G_{cc}$)]].

## Procedencia

- Clases: [[2026-09-10 ADA - DAGs-y-ordenamiento-topologico|Clase del 10 de septiembre de 2026]] y [[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|Clase del 17 de septiembre de 2026]].
- Fuentes: Kleinberg & Tardos, *Algorithm Design*, Sección 3.6; Cormen et al. (CLRS), *Introduction to Algorithms*, Sección 22.4.
