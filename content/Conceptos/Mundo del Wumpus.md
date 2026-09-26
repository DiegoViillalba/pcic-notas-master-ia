---
tipo: concepto
aliases:
  - Wumpus World
  - Entorno del Wumpus
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-10 IA - Agentes logicos|Clase 9: Agentes lógicos]]"
tags:
  - concepto
  - inteligencia-artificial
  - entorno-de-tarea
  - peas
  - wumpus
---

# Mundo del Wumpus

## Definición

Entorno de prueba canónico en Inteligencia Artificial (propuesto originalmente por Gregory Yob en 1973 y adoptado por Russell & Norvig) diseñado para ilustrar la necesidad del razonamiento deductivo y la representación explícita del conocimiento en un [[Agente basado en conocimiento|agente basado en conocimiento]].

Consiste en una cuadrícula de cavernas (típicamente $4 \times 4$) donde el agente debe navegar para encontrar un lingote de oro y escapar con vida, evitando pozos sin fondo y un monstruo carnívoro inmóvil llamado Wumpus.

## Especificación PEAS del entorno

- **Rendimiento (Performance Measure):**
  - $+1000$ por salir de la cueva con el oro.
  - $-1000$ por caer en un pozo o ser devorado por el Wumpus.
  - $-1$ por cada acción ejecutada (costo de paso).
  - $-10$ por disparar la flecha.
- **Entorno (Environment):**
  - Cuadrícula $4 \times 4$ delimitada por muros.
  - La casilla $[1,1]$ es siempre el punto de partida seguro del agente.
  - El Wumpus y el oro se ubican en casillas seleccionadas al azar distintas de $[1,1]$.
  - Cada casilla distinta de $[1,1]$ tiene una probabilidad independiente ($p = 0.2$) de albergar un pozo.
- **Actuadores (Actuators):**
  - `Adelante`, `Girar a la izquierda` ($90^\circ$), `Girar a la derecha` ($90^\circ$).
  - `Tomar` el oro (si está en la misma casilla).
  - `Disparar` la flecha (línea recta en la dirección a la que apunta el agente; solo hay una flecha).
  - `Salir` (únicamente válido en $[1,1]$).
- **Sensores (Sensors):**
  - **Hedor (Stench):** Se percibe en la casilla del Wumpus y en las casillas adyacentes ortogonalmente.
  - **Brisa (Breeze):** Se percibe en las casillas adyacentes ortogonalmente a cualquier pozo.
  - **Brillo (Glitter):** Se percibe en la misma casilla que contiene el lingote de oro.
  - **Golpe (Bump):** Se percibe cuando el agente intenta caminar contra una pared perimetral.
  - **Grito (Scream):** Se escucha en toda la cueva si el Wumpus es abatido por la flecha.

## Formalización en lógica proposicional

La física del entorno se captura mediante fórmulas bicondicionales exactas para cada casilla $[x, y]$:

$$
B_{x,y} \iff \bigvee_{[i,j] \in \text{Adyacentes}(x,y)} P_{i,j}
$$

$$
S_{x,y} \iff \bigvee_{[i,j] \in \text{Adyacentes}(x,y)} W_{i,j}
$$

Adicionalmente, se formalizan los axiomas de unicidad (solo hay un Wumpus en todo el tablero):

$$
\bigvee_{x,y} W_{x,y} \quad \wedge \quad \bigwedge_{(x,y) \neq (i,j)} (\neg W_{x,y} \vee \neg W_{i,j})
$$

## ¿Por qué la búsqueda tradicional falla en el Wumpus?

En búsqueda clásica (como BFS, DFS o A*), el agente asume observabilidad total o al menos un espacio de estados totalmente formulable de antemano. En el Wumpus:
1. El agente **no ve** lo que hay en las casillas contiguas; solo percibe pistas indirectas locales.
2. Si el agente explorara a ciegas mediante ensayo y error, moriría con una probabilidad inaceptable al pisar un pozo o caer con el Wumpus (penalización $-1000$).
3. Solo un agente con una [[Base de conocimiento|Base de Conocimiento]] que mantenga sentencias del pasado y aplique [[Vinculación lógica|vinculación lógica]] puede demostrar matemáticamente si una casilla no visitada es $100\%$ segura antes de moverse.

## Relaciones

- Es el entorno de prueba para: [[Agente basado en conocimiento|Agente basado en conocimiento]].
- Se modela con: [[Lógica proposicional|Lógica proposicional]].
- Ilustra el valor de la: [[Vinculación lógica|Vinculación lógica]].
- Es un caso concreto de: [[Entorno de tarea|Entorno de tarea (PEAS)]].

## Procedencia

- Clase: [[2026-09-10 IA - Agentes logicos|Clase 9: Agentes lógicos]].
- Fuente: Russell & Norvig, *Artificial Intelligence: A Modern Approach* (4.ª ed.), Sección 7.2.
