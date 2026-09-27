---
tipo: concepto
aliases:
  - Regla de asignación de Hoare
  - Assignment axiom
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica-de-hoare, asignacion]
---

# Axioma de asignación de Hoare

## Definición

Regla que obtiene la precondición de `V := E` sustituyendo en la postcondición $Q$ todas las apariciones libres de $V$ por la expresión $E$.

## Intuición

Después de la asignación, `V` contiene el valor de `E` calculado en el estado anterior. Para saber qué debía cumplirse antes, se reemplaza el valor final exigido para `V` por la expresión que lo producirá.

## Formulación

$$
\boxed{\{Q^{V}_{E}\}\ V:=E\ \{Q\}}.
$$

La convención usada en las notas de Programación Avanzada es

$$
Q^{V}_{E}\equiv Q[E/V],
$$

que se lee **“$Q$ con $V$ sustituida por $E$”**. Así, la precondición calculada es $P=Q^{V}_{E}$. La sustitución debe ser simultánea y evitar la captura de variables.

Las diapositivas representan intuitivamente la sustitución con el esquema $\{V=E,Q\}$: se usa $V=E$ para reemplazar $V$ dentro de $Q$; no se trata de afirmar la conjunción $V=E\land Q$ antes de ejecutar la asignación.

## Ejemplo mínimo

```text
Q: k = 12
instrucción: k := 4*a
Q^k_{4a}: 4*a = 12
precondición simplificada: a = 3
```

Por tanto:

$$
\{a=3\}\ k:=4a\ \{k=12\}.
$$

Otro ejemplo:

$$
\{i<3\}\ i:=2i\ \{i<6\}.
$$

## Contraejemplo o límites

No debe escribirse sin aclaración `i=i+1` después de `i:=i+1`: los dos lados referirían al mismo estado. La sustitución o una variable histórica $i_0$ elimina esa ambigüedad.

## Error típico: sustituir “hacia adelante”

La forma correcta parte de la postcondición $Q$. La regla falsa

$$
\{P\}\ V:=E\ \{P^{V}_{E}\}
$$

podría producir $\{x=0\}\ x:=1\ \{1=0\}$, lo cual revela el error. En cambio, para probar $\{?\}\ x:=1\ \{x=1\}$ se calcula $(x=1)^x_1$, que es $1=1$; por tanto la precondición más débil es $\top$.

## Mini ejercicio

Para $z:=3x-2$ y $Q:z>7$:

$$
(z>7)^z_{3x-2}\equiv3x-2>7\iff x>3.
$$

Comprueba con $x=4$ y con el valor frontera $x=3$.

## Cálculo de una postcondición en las diapositivas

Cuando la precondición $P$ fija los valores necesarios para evaluar $E$, las diapositivas 26–27 llaman $C^{E}_{\{P\}}$ al resultado de sustituir esos valores en la igualdad $C\equiv(V=E)$:

$$
\{P\}\ V:=E\ \left\{C^{E}_{\{P\}}\right\}.
$$

En esa convención, $Q=C^{E}_{\{P\}}$. El esquema auxiliar $\{E=\{P\},C\}$ de las diapositivas indica el reemplazo que debe efectuarse; no representa una conjunción lógica.

Por ejemplo:

$$
C^{4a}_{\{a=3\}}\equiv(k=4a)^{4a}_{\{a=3\}}\equiv k=12,
$$

y por ello $\{a=3\}\ k:=4a\ \{k=12\}$. Esta es una sustitución hacia adelante de valores conocidos, no la forma general de la postcondición más fuerte para una precondición arbitraria.

## Relaciones

- Calcula: [[Precondición más débil|Precondición más débil]].
- Es una regla para: [[Terna de Hoare|Terna de Hoare]].
- Requiere distinguir: [[Estado de programa|estado anterior y posterior]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 24–27 (láminas 78–81).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 14–16.
- Práctica interactiva: [[Guía paso a paso - Lógica de Hoare#2. Asignación sustituir desde la meta|Asignación: sustituir desde la meta]].
