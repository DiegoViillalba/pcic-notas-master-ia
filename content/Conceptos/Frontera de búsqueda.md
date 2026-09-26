---
tipo: concepto
aliases:
  - Search frontier
  - Fringe
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Búsqueda I]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Frontera de búsqueda

## Definición

Colección de nodos generados que todavía no han sido expandidos. Representa los caminos conocidos que la búsqueda puede continuar explorando.

## Operaciones

- **Insertar:** añadir los nodos producidos al expandir un nodo.
- **Extraer:** elegir y retirar el siguiente nodo según la estrategia.
- **Actualizar:** reemplazar la entrada de un estado cuando se descubre un camino de menor costo, si la estrategia lo requiere.
- **Comprobar vaciedad:** si no quedan nodos y no se encontró una meta, la búsqueda falla.

La detección de estados repetidos corresponde al registro de alcanzados de la búsqueda en grafo; no es una propiedad automática de la frontera.

## Estructuras de datos

| Estructura | Criterio de selección | Estrategia asociada |
|---|---|---|
| Cola FIFO | Primero en entrar, primero en salir | Búsqueda en anchura (BFS) |
| Pila LIFO | Último en entrar, primero en salir | Búsqueda en profundidad (DFS) |
| Cola de prioridad | Menor costo acumulado $g(n)$ | Búsqueda de costo uniforme (UCS) |

## Ejemplo mínimo

Si al expandir $S$ se generan $A$ y $B$, la frontera queda $[A,B]$. Después:

- una cola FIFO extrae $A$ y conserva $B$ antes de los hijos de $A$;
- una pila LIFO extrae el último nodo insertado;
- una cola de prioridad extrae el nodo con menor $g(n)$, sin importar cuándo se insertó.

## Invariante útil

Todo nodo de la frontera fue generado pero no expandido. Un nodo deja la frontera al ser extraído; sus sucesores pueden incorporarse después.

## Relaciones

- Contiene: [[Nodo de búsqueda|Nodos de búsqueda]]
- Determina el comportamiento de una: [[Búsqueda no informada|Búsqueda no informada]]
- Se complementa con: [[Búsqueda en árbol y búsqueda en grafo|Búsqueda en árbol y búsqueda en grafo]]

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 19–20, para nodos y expansión. Las estructuras de frontera completan el mecanismo de las estrategias no informadas.
