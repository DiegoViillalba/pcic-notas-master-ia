---
tipo: concepto
aliases:
  - Directed graph
  - Digrafo
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
  - digrafos
---

# Grafo dirigido

## Definición

Un **grafo dirigido** o **digrafo** $G = (V, E)$ consiste en un conjunto de vértices $V$ y un conjunto de aristas dirigidas (o arcos) $E$, donde cada arista es un **par ordenado** de vértices:

$$
e = (u, v) \in E
$$

Se interpreta que la arista sale del vértice $u$ (origen o cola) y entra al vértice $v$ (destino o cabeza). A diferencia de los grafos no dirigidos, la existencia de $(u, v)$ no implica la existencia de $(v, u)$.

## Grados en digrafos

Para cada vértice $v \in V$:
- **Grado de entrada ($\text{in-degree}(v)$):** Número de aristas que entran a $v$:
  $$\text{in-degree}(v) = |\{u \in V \mid (u, v) \in E\}|$$
- **Grado de salida ($\text{out-degree}(v)$):** Número de aristas que salen de $v$:
  $$\text{out-degree}(v) = |\{w \in V \mid (v, w) \in E\}|$$

Lema del apretón de manos para digrafos:
$$
\sum_{v \in V} \text{in-degree}(v) = \sum_{v \in V} \text{out-degree}(v) = m = |E|
$$

## Aplicaciones canónicas

| Red / Dominio | Vértice | Arista dirigida $(u \to v)$ |
|---|---|---|
| **World Wide Web** | Página web | Hipervínculo de la página $u$ hacia $v$ (base de PageRank). |
| **Transporte** | Intersección | Calle de sentido único hacia $v$. |
| **Redes tróficas** | Especie | Relación de presa a depredador ($u$ es comido por $v$). |
| **Citas académicas** | Artículo científico | El artículo $u$ cita al artículo $v$. |
| **Llamadas telefónicas** | Persona | La persona $u$ llamó a la persona $v$. |
| **Flujo de control** | Bloque de código | Salto condicional o secuencial hacia $v$. |
| **Precedencia** | Tarea / Módulo | La tarea $u$ debe completarse antes de iniciar $v$. |

## Grafo reverso ($G^{rev}$)

Dado un digrafo $G = (V, E)$, su **grafo reverso** (o transpuesto) $G^{rev} = (V, E^{rev})$ tiene los mismos vértices pero invierte el sentido de cada arista:

$$
E^{rev} = \{(v, u) \mid (u, v) \in E\}
$$

La construcción de $G^{rev}$ toma tiempo $O(m + n)$ y es una herramienta algorítmica fundamental para analizar alcanzabilidad hacia un nodo destino.

## Relaciones

- Es la base para analizar: [[Conectividad fuerte|Conectividad fuerte]].
- Cuando no tiene ciclos dirigidos, se denomina: [[Grafo dirigido acíclico|Grafo dirigido acíclico (DAG)]].
- Contrasta con: [[Grafo|Grafo no dirigido]].

## Procedencia

- Clase: [[2026-09-08 ADA - biparticion-y-grafos-dirigidos|Clase del 8 de septiembre de 2026]].
- Fuente: Kleinberg & Tardos, *Algorithm Design*, Capítulo 3, Sección 3.5 (*Connectivity in Directed Graphs*).
