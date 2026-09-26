---
tipo: concepto
aliases:
  - Grafo de condensación
  - Condensación de un grafo dirigido
  - Kernel DAG
  - Component DAG
  - G_cc
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|Clase: TopoSort con DFS y Componentes Fuertes]]"
tags:
  - concepto
  - algoritmos
  - grafos
  - dag
  - conectividad-fuerte
  - scc
---

# Gráfica de componentes conexas ($G_{cc}$)

## Definición

Dada una [[Grafo dirigido|gráfica dirigida]] $G = (V, E)$, su **gráfica de componentes conexas** $G_{cc} = (V_{cc}, E_{cc})$ (conocida también como *grafo de condensación*, *Kernel DAG* o *Component DAG*) es la gráfica cuyos vértices representan las [[Conectividad fuerte|componentes fuertemente conexas (SCC)]] de $G$, y cuyas aristas representan la conectividad dirigida entre componentes distintas:

1. **Conjunto de vértices:**
   $$V_{cc} = \{C_1, C_2, \dots, C_k\}$$
   donde cada $C_i \subseteq V$ es una componente fuertemente conexa maximal de $G$.
2. **Conjunto de aristas:** Para dos componentes distintas $X, Y \in V_{cc}$ ($X \neq Y$):
   $$(X, Y) \in E_{cc} \iff \exists u \in X, \; \exists v \in Y \quad \text{tal que } (u, v) \in E$$

No se permiten auto-aristas o bucles en $G_{cc}$ (las dependencias internas dentro de una misma componente quedan absorbidas dentro del supernodo). Si existen múltiples aristas de $X$ a $Y$ en $G$, se colapsan a una única macro-arista dirigida en $E_{cc}$.

---

## Teorema Fundamental: Aciclicidad de $G_{cc}$

> [!important] Teorema
> Para cualquier grafo dirigido $G$, su gráfica de componentes conexas $G_{cc}$ es **siempre un [[Grafo dirigido acíclico|grafo dirigido acíclico (DAG)]]**.

### Demostración por contradicción
1. Supongamos que $G_{cc}$ no es un DAG. Entonces existe un ciclo dirigido simple entre componentes:
   $$C_1 \to C_2 \to \dots \to C_r \to C_1 \quad (r \ge 2)$$
2. Por la definición de arista en $G_{cc}$, para cada paso del ciclo existe una arista $(u_i, v_{i+1}) \in E$ con $u_i \in C_i$ y $v_{i+1} \in C_{i+1}$ (y $(u_r, v_1) \in E$ con $u_r \in C_r$ y $v_1 \in C_1$).
3. Dado que cada componente $C_i$ es fuertemente conexa, dentro de $C_i$ existe un camino dirigido entre cualquier par de sus nodos.
4. Por lo tanto, podemos construir un camino dirigido desde cualquier nodo de $C_1$ hacia cualquier nodo de $C_2$, de ahí a $C_3$, y eventualmente regresar a $C_1$.
5. Esto implica que **todos los nodos de la unión** $C_1 \cup C_2 \cup \dots \cup C_r$ son mutuamente alcanzables entre sí en $G$.
6. Esto contradice la **maximalidad** de las componentes fuertemente conexas individuales $C_1, \dots, C_r$, pues deberían formar una única componente mayor.
7. Por lo tanto, $G_{cc}$ no puede contener ciclos dirigidos: **$G_{cc}$ es un DAG**. $\blacksquare$

---

## Propiedades y Casos Límite

1. **Si $G$ ya es un DAG:** Cada vértice es su propia componente ($|C_i| = 1$ para todo $i$). En este caso, $G_{cc}$ es idéntica (isomorfa) a $G$.
2. **Si $G$ es fuertemente conexo:** Todo el grafo forma una única componente ($k = 1$). Por tanto, $V_{cc} = \{C_1\}$ y $E_{cc} = \emptyset$.
3. **Ordenamiento topológico:** Como $G_{cc}$ es un DAG, **siempre admite al menos un [[Ordenamiento topológico|ordenamiento topológico]]** sobre sus supernodos. Esto permite procesar digrafos generales por etapas libres de dependencias circulares.

---

## Complejidad Computacional

Construir $G_{cc}$ a partir de $G$:
1. Calcular las SCCs usando el **algoritmo de Tarjan (1972)** o el de **Kosaraju-Sharir (1978)**: $O(n + m)$.
2. Asignar a cada nodo $u \in V$ un identificador de componente $\text{comp}[u] \in \{1, \dots, k\}$.
3. Recorrer las $m$ aristas $(u, v) \in E$: si $\text{comp}[u] \neq \text{comp}[v]$, agregar la macro-arista $(\text{comp}[u], \text{comp}[v])$ a $E_{cc}$ (usando una tabla hash o adyacencias para evitar duplicados): $O(n + m)$.

**Tiempo y espacio totales:** $O(n + m)$.

---

## Relaciones

- Vértices compuestos por: [[Conectividad fuerte|Componentes fuertemente conexas (SCC)]].
- Pertenece a la clase de grafos: [[Grafo dirigido acíclico|Grafo dirigido acíclico (DAG)]].
- Admite: [[Ordenamiento topológico|Ordenamiento topológico]] sobre sus componentes.
- Se construye mediante: [[Búsqueda en profundidad|Búsqueda en profundidad (DFS)]] (Tarjan / Kosaraju).

---

## Procedencia

- Clase: [[2026-09-17 ADA - toposort-dfs-y-componentes-fuertemente-conexas|Clase del 17 de septiembre de 2026]].
- Fuentes: Kleinberg & Tardos, *Algorithm Design*, Cap. 3; Cormen et al. (CLRS), *Introduction to Algorithms*, Sección 22.5.
