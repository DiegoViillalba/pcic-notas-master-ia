---
tipo: concepto
aliases:
  - Uninformed search
  - Blind search
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Búsqueda I]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Búsqueda no informada

## Definición

Familia de estrategias que exploran usando únicamente la formulación del problema: estado inicial, acciones, sucesores, prueba de meta y costos. No emplean una heurística que estime qué tan cerca está un estado de la meta.

## Información disponible

- **Sí utiliza:** profundidad, orden de generación y costo acumulado $g(n)$, según la estrategia.
- **No utiliza:** una estimación externa del costo restante ni conocimiento específico sobre la dirección de la meta.

## Estrategias

| Estrategia | Regla de extracción | Frontera | Conviene cuando… |
|---|---|---|---|
| [[Búsqueda en anchura|Búsqueda en anchura (BFS)]] | Menor profundidad | Cola FIFO | Se busca una solución con pocos pasos y los costos son iguales |
| [[Búsqueda en profundidad|Búsqueda en profundidad (DFS)]] | Nodo más profundo | Pila LIFO | La memoria es limitada y se aceptan riesgos de ramas profundas |
| [[Búsqueda de profundidad iterativa|Profundidad iterativa (IDS)]] | DFS con límites crecientes | Pila acotada | Se necesita completitud con memoria lineal |
| [[Búsqueda de costo uniforme|Búsqueda de costo uniforme (UCS)]] | Menor costo acumulado $g(n)$ | Cola de prioridad | Los costos son distintos y se necesita el camino de menor costo |

## Comparación

La estrategia cambia el orden, no el espacio explorado. BFS es óptima solo con costos de paso iguales; DFS no garantiza la solución más corta y puede perderse en una rama infinita; UCS es óptima si los costos de paso están acotados por un valor positivo. Las condiciones y cotas se resumen en [[Criterios de evaluación de algoritmos de búsqueda|Criterios de evaluación]].

## Ejemplo común

Considérese $S\to A$ con costo $1$, $A\to G$ con costo $5$, $S\to B$ con costo $4$, $B\to G$ con costo $1$ y $A\to C\to G$ con costos $1$ y $1$.

- **BFS** devuelve una meta a profundidad $2$; cuál de las rutas encuentra primero depende del orden de los hijos.
- **DFS** sigue la primera rama disponible y su resultado también depende del orden.
- **UCS** devuelve $S\to A\to C\to G$, cuyo costo total es $3$, aunque contiene más pasos.

## Límite

“No informada” no significa aleatoria ni ignorante: UCS usa costos reales y las tres estrategias requieren una formulación correcta. Solo significa que no disponen de una heurística sobre el costo restante.

## Relaciones

- Utiliza una: [[Frontera de búsqueda|Frontera de búsqueda]]
- Se evalúa mediante: [[Criterios de evaluación de algoritmos de búsqueda|Criterios de evaluación]]
- Se contrapone con la búsqueda informada, que utiliza una [[Heurística|heurística]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 10 y 17–20, para la formulación y el árbol de búsqueda. Las estrategias se completaron como preparación indicada al final de la clase.
