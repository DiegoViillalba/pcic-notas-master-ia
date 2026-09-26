---
tipo: concepto
aliases:
  - Graph
  - Grafo matemático
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes: []
tags: [concepto, algoritmos, grafos, estructuras-discretas]
---

# Grafo

## Definición

Un **grafo** es una estructura matemática formada por un conjunto de **vértices** (o nodos) y un conjunto de **aristas** que conectan pares de vértices. Se escribe

$$G=(V,E),$$

donde $V$ es el conjunto de vértices y $E$ el conjunto de aristas.

## Intuición

Un grafo representa **entidades y relaciones**: los vértices son las entidades y las aristas indican qué entidades están relacionadas. Importa la conectividad, no la posición de los vértices en el dibujo.

## Ejemplo mínimo

Si $V=\{A,B,C\}$ y $E=\{\{A,B\},\{B,C\}\}$, entonces $A$ está conectado con $B$, y $B$ con $C$. Existe un camino de $A$ a $C$, aunque no haya una arista directa entre ellos.

## Elementos básicos

- **Vértice o nodo:** cada objeto representado.
- **Arista:** relación entre dos vértices.
- **Adyacencia:** dos vértices son adyacentes si una arista los une.
- **Grado:** número de aristas incidentes en un vértice. En grafos dirigidos se distingue entre grado de entrada y de salida.
- **Camino:** secuencia de vértices conectados por aristas.
- **Ciclo:** camino que vuelve al vértice inicial sin repetir aristas.
- **Componente conexa:** conjunto máximo de vértices entre los que existe algún camino.

## Tipos principales

| Tipo | Característica | Ejemplo |
|---|---|---|
| **No dirigido** | La relación es simétrica: $\{u,v\}=\{v,u\}$. | Una amistad. |
| **Dirigido (digrafo)** | Cada arista tiene orientación: $(u,v)$ no equivale a $(v,u)$. | Seguir a alguien en una red social. |
| **Ponderado** | Las aristas llevan un peso, costo o distancia. | Una red de carreteras con kilómetros. |
| **No ponderado** | Todas las conexiones se tratan por igual. | Contactos entre personas. |
| **Simple** | No tiene lazos ni aristas múltiples entre el mismo par de vértices. | Una red básica de colaboración. |
| **Multigrafo** | Permite varias aristas entre los mismos vértices. | Varias rutas aéreas entre dos ciudades. |
| **Conexo** | Existe un camino entre cada par de vértices. | Una red donde todos pueden comunicarse. |
| **Desconexo** | Tiene dos o más componentes sin caminos entre ellas. | Dos comunidades aisladas. |
| **Acíclico** | No contiene ciclos. | Un árbol genealógico simplificado. |
| **Cíclico** | Contiene al menos un ciclo. | Una ruta circular de transporte. |
| **Completo $K_n$** | Cada par de vértices distintos está conectado. | Un grupo donde todos se conocen. |
| **Bipartito** | Sus vértices se separan en dos grupos y las aristas solo cruzan entre ellos. | Estudiantes conectados con cursos. |
| **Árbol** | Grafo no dirigido, conexo y acíclico. | Una jerarquía de carpetas. |

> [!important] Las clasificaciones pueden combinarse
> Un grafo puede ser simultáneamente dirigido, ponderado, conexo y cíclico. “Tipo” no siempre significa una categoría excluyente.

## Explorador visual

Selecciona una familia para observar qué propiedad cambia. El dibujo es solo una representación: mover un nodo no modifica el grafo mientras sus aristas sigan siendo las mismas.

<iframe src="explorador-tipos-de-grafos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## Claves para entenderlos

1. **Pregunta primero qué representan los nodos y las aristas.** Esto traduce el problema real al lenguaje de grafos.
2. **Busca dirección y peso.** Determinan si una arista es recíproca y si atravesarla tiene costo.
3. **No confundas camino con arista.** Puede existir una ruta entre dos nodos aunque no sean adyacentes.
4. **Separa la forma dibujada de la estructura.** Dos dibujos diferentes pueden representar exactamente el mismo grafo.
5. **Observa ciclos y conectividad.** Estas propiedades suelen decidir qué algoritmos pueden utilizarse.

## Ejemplos de modelado

- **Mapa vial:** ciudades $\rightarrow$ vértices; carreteras $\rightarrow$ aristas; kilómetros $\rightarrow$ pesos.
- **Red social:** personas $\rightarrow$ vértices; amistad o seguimiento $\rightarrow$ aristas.
- **Prerrequisitos:** materias $\rightarrow$ vértices; “debe cursarse antes” $\rightarrow$ aristas dirigidas.
- **Asignación:** trabajadores y tareas $\rightarrow$ dos particiones; compatibilidad $\rightarrow$ aristas de un grafo bipartito.

## Contraejemplo o límites

Una tabla con nombres aislados no es todavía un grafo: hacen falta relaciones. Además, el dibujo de líneas que se cruzan no implica que exista un vértice en cada cruce; solo lo hay si está señalado como tal.

## Relaciones

- Un [[Árbol de búsqueda|árbol]] es un caso particular de grafo.
- Un [[Grafo de espacio de estados|grafo de espacio de estados]] representa estados y transiciones de un problema.
- La [[Búsqueda en árbol y búsqueda en grafo|búsqueda en grafo]] evita explorar repetidamente estados ya visitados.
- Los grafos bipartitos permiten expresar problemas de [[Emparejamiento perfecto|emparejamiento perfecto]] y [[Emparejamiento estable|emparejamiento estable]].

## En una frase

> Un grafo modela objetos como vértices y sus relaciones como aristas.
