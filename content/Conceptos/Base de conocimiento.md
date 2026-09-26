---
tipo: concepto
aliases:
  - Knowledge Base
  - KB
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-09-10 IA - Agentes logicos|Clase 9: Agentes lógicos]]"
tags:
  - concepto
  - inteligencia-artificial
  - logica
  - representacion-conocimiento
---

# Base de conocimiento

## Definición

Conjunto de sentencias expresadas en un lenguaje formal (por ejemplo, [[Lógica proposicional|lógica proposicional]]) que representan los hechos, leyes y axiomas que un agente asume como verdaderos sobre su entorno.

Desde el punto de vista semántico, una base de conocimiento representa la conjunción lógica de todas sus sentencias componentes.

## Formulación y espacio de modelos

Si $KB = \{f_1, f_2, \dots, f_k\}$, el conjunto de [[Modelo en lógica proposicional|modelos]] o mundos posibles en los que $KB$ es verdadera corresponde a la **intersección** de los modelos de cada una de sus fórmulas:

$$
M(KB) = \bigcap_{f \in KB} M(f)
$$

### Adición de conocimiento y reducción de incertidumbre

Añadir una nueva fórmula $f$ a la base ($KB \Leftarrow KB \cup \{f\}$) tiene un efecto monotónico de filtrado sobre el espacio de mundos posibles:

$$
M(KB \cup \{f\}) = M(KB) \cap M(f)
$$

- Si $M(KB) \subseteq M(f)$, la fórmula ya era implicada; la base **"ya lo sabía"** y el espacio de modelos no cambia.
- Si $M(KB) \cap M(f) = \emptyset$, la fórmula es una **contradicción** con los hechos conocidos ("¡no lo creo!").
- Si $\emptyset \subsetneq M(KB) \cap M(f) \subsetneq M(KB)$, la fórmula aporta información contingente; el agente **"aprende algo nuevo"** y se descartan los mundos incompatibles.

## Ejemplo mínimo

Supongamos dos variables: $\text{Rain}$ (llueve) y $\text{Wet}$ (el suelo está mojado), con $2^2 = 4$ modelos iniciales.

1. Inicialmente $KB = \emptyset \implies M(KB) = \{w_1, w_2, w_3, w_4\}$.
2. Añadimos la regla $f_1 = \text{Rain} \to \text{Wet}$. Sus modelos son $M(f_1) = \{(0,0), (0,1), (1,1)\}$. Se descarta $(1,0)$.
3. Añadimos el hecho perceptivo $f_2 = \text{Rain}$. Sus modelos son $M(f_2) = \{(1,0), (1,1)\}$.
4. La intersección final es:
   $$
   M(KB) = M(f_1) \cap M(f_2) = \{(1,1)\}
   $$
   El agente ahora sabe con certeza que llueve y que el suelo está mojado.

## Contraejemplo o límites

- **Base insatisfactible:** Si $M(KB) = \emptyset$, la base contiene una contradicción interna. Por el principio de explosión (*ex contradictione quodlibet*), una base contradictoria vincula lógicamente cualquier sentencia, volviéndose inútil para la toma de decisiones.
- **Monotonicidad:** En la lógica clásica, añadir sentencias nunca recupera modelos descartados previamente. Si un agente necesita revocar creencias ante nueva evidencia incompatible, requiere lógicas no monotónicas o marcos probabilísticos.

## Relaciones

- Es el núcleo de un: [[Agente basado en conocimiento|Agente basado en conocimiento]].
- Se define sobre el conjunto de: [[Modelo en lógica proposicional|Modelos en lógica proposicional]].
- Permite responder preguntas mediante: [[Vinculación lógica|Vinculación lógica]].
- Su consistencia se verifica mediante: [[Satisfacibilidad proposicional|Satisfacibilidad proposicional]].

## Procedencia

- Clase: [[2026-09-10 IA - Agentes logicos|Clase 9: Agentes lógicos]].
- Fuente: Russell & Norvig, *Artificial Intelligence: A Modern Approach* (4.ª ed.), Capítulo 7.
