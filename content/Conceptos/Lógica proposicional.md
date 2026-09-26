---
tipo: concepto
aliases:
  - Propositional logic
  - Lógica booleana
  - Cálculo proposicional
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
  - formalismo
---

# Lógica proposicional

## Definición

Sistema formal de representación del razonamiento basado en sentencias declarativas (proposiciones) que afirman hechos del mundo que solo pueden ser verdaderos ($\text{True} / 1$) o falsos ($\text{False} / 0$). 

Posee un **compromiso ontológico** limitado a hechos y un **compromiso epistemológico** donde el agente cree que un hecho es verdadero, falso o desconocido ($T/F/\text{No sé}$).

## Sintaxis formal

La sintaxis define cuáles cadenas de caracteres constituyen fórmulas bien formadas mediante una gramática formal en forma Backus-Naur (BNF):

$$
\begin{aligned}
\text{Sentence} &\to \text{AtomicSentence} \mid \text{ComplexSentence} \\
\text{AtomicSentence} &\to \text{True} \mid \text{False} \mid P \mid Q \mid R \mid \dots \\
\text{ComplexSentence} &\to (\text{Sentence}) \mid [\text{Sentence}] \\
&\quad\mid \neg \text{Sentence} \\
&\quad\mid \text{Sentence} \wedge \text{Sentence} \\
&\quad\mid \text{Sentence} \vee \text{Sentence} \\
&\quad\mid \text{Sentence} \Rightarrow \text{Sentence} \\
&\quad\mid \text{Sentence} \Leftrightarrow \text{Sentence}
\end{aligned}
$$

### Precedencia de operadores

Para eliminar ambigüedad en fórmulas sin paréntesis, los conectores se evalúan en el siguiente orden estricto de precedencia:

$$
\neg \quad \succ \quad \wedge \quad \succ \quad \vee \quad \succ \quad \Rightarrow \quad \succ \quad \Leftrightarrow
$$

Por ejemplo, $\neg A \wedge B \Rightarrow C$ se interpreta inequívocamente como $((\neg A) \wedge B) \Rightarrow C$.

## Semántica

La semántica asigna significado determinando el valor de verdad de una fórmula con respecto a un [[Modelo en lógica proposicional|modelo]] $w$. La función de interpretación $I(f, w) \in \{0, 1\}$ se evalúa de forma composicional:

| $P$ | $Q$ | $\neg P$ | $P \wedge Q$ | $P \vee Q$ | $P \Rightarrow Q$ | $P \Leftrightarrow Q$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 |

> [!NOTE] Implicación material ($P \Rightarrow Q$)
> Es falsa **únicamente** cuando el antecedente $P$ es verdadero y el consecuente $Q$ es falso. Si $P$ es falso, la implicación es trivialmente verdadera en ese modelo (condición vacía).

## Ejemplo mínimo

En una sala con luz y alarma:
- $L$: "La luz está encendida".
- $A$: "La alarma está sonando".
- Fórmula compuesta: $f = (L \wedge \neg A) \Rightarrow \text{Seguro}$.
En un mundo $w = \{L: 1, A: 0, \text{Seguro}: 1\}$, evaluamos:
$I(\neg A, w) = 1 \implies I(L \wedge \neg A, w) = 1 \implies I(1 \Rightarrow 1, w) = 1$. La fórmula es satisfecha por el mundo $w$.

## Contraejemplo o límites

- **Falta de cuantificación y objetos:** La lógica proposicional no puede expresar de forma compacta afirmaciones generales como "todos los pozos producen brisa en sus casillas vecinas". Para un tablero de $4 \times 4$, se deben escribir manualmente 16 fórmulas proposicionales distintas ($B_{1,1} \leftrightarrow \dots, B_{1,2} \leftrightarrow \dots$).
- Para superar esta limitación expresiva, se introduce la **lógica de primer orden** (con objetos, predicados, funciones y cuantificadores $\forall, \exists$).

## Relaciones

- Es evaluada en un: [[Modelo en lógica proposicional|Modelo en lógica proposicional]].
- Estructura el contenido de una: [[Base de conocimiento|Base de conocimiento]].
- Su problema de satisfactibilidad es: [[Satisfacibilidad proposicional|Satisfacibilidad proposicional (SAT)]].
- Es la base para la deducción en el: [[Mundo del Wumpus|Mundo del Wumpus]].

## Procedencia

- Clase: [[2026-09-10 IA - Agentes logicos|Clase 9: Agentes lógicos]].
- Fuente: Russell & Norvig, *Artificial Intelligence: A Modern Approach* (4.ª ed.), Capítulo 7.
