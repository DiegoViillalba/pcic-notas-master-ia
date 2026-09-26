---
tipo: concepto
aliases:
  - Tree search and graph search
  - Graph search
  - Tree search
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Búsqueda I]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Búsqueda en árbol y búsqueda en grafo

## Búsqueda en árbol

Expande nodos sin recordar todos los estados alcanzados. Dos planes que llegan al mismo estado producen nodos distintos, por lo que puede repetir trabajo o seguir indefinidamente un ciclo.

## Búsqueda en grafo

Mantiene un registro de estados alcanzados y evita generar de nuevo aquellos que ya conoce. Si importan los costos, no basta con marcar un estado: también se conserva el menor costo conocido y se actualiza cuando aparece un camino mejor.

## Comparación

| Criterio | Árbol | Grafo |
|---|---|---|
| Estados repetidos | Puede generar varias copias | Los detecta mediante el estado |
| Ciclos | Pueden crear ramas infinitas | Se cortan al reconocer estados alcanzados |
| Memoria | Menor, porque no guarda todos los estados | Mayor, por el registro de alcanzados |
| Trabajo repetido | Frecuente | Se reduce o elimina |

## Ejemplo mínimo

Si existen las transiciones $S\to A$, $A\to S$ y $A\to G$, la búsqueda en árbol puede producir la rama infinita $S,A,S,A,\ldots$. La búsqueda en grafo registra $S$ y $A$, descarta el regreso a $S$ y puede continuar hacia la meta $G$.

## Esquema común

```text
frontera <- {nodo inicial}
alcanzados <- {estado inicial: costo 0}  # omitir en búsqueda en árbol

mientras frontera no esté vacía:
    nodo <- extraer según la estrategia
    si nodo satisface la meta: devolver su plan
    para cada hijo de nodo:
        si es búsqueda en árbol: insertar hijo
        si es búsqueda en grafo y el estado es nuevo o el camino es mejor:
            actualizar alcanzados e insertar o actualizar hijo
devolver fallo
```

La estructura de la [[Frontera de búsqueda|frontera]] decide qué nodo se extrae. El registro de alcanzados decide si la exploración es en árbol o en grafo.

## Límite

Buscar en grafo no garantiza por sí solo completitud ni optimalidad: estas propiedades también dependen del orden de extracción y del tratamiento de caminos más baratos.

## Relaciones

- Exploran un: [[Espacio de estados|Espacio de estados]]
- Administran una: [[Frontera de búsqueda|Frontera de búsqueda]]
- Generan: [[Nodo de búsqueda|Nodos de búsqueda]]

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 19–20; la clase introduce la repetición de estados y los ciclos. El registro de alcanzados completa la comparación operacional.
