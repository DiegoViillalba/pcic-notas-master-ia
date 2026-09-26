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
\boxed{\{Q[E/V]\}\ V:=E\ \{Q\}}.
$$

La sustitución debe ser simultánea y evitar la captura de variables.

## Ejemplo mínimo

```text
Q: k = 12
instrucción: k := 4*a
Q[4*a/k]: 4*a = 12
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
\{P\}\ V:=E\ \{P[E/V]\}
$$

podría producir $\{x=0\}\ x:=1\ \{1=0\}$, lo cual revela el error. En cambio, para probar $\{?\}\ x:=1\ \{x=1\}$ se calcula $(x=1)[1/x]$, que es $1=1$; por tanto la precondición más débil es $\top$.

## Mini ejercicio

Para $z:=3x-2$ y $Q:z>7$:

$$
Q[3x-2/z]\equiv3x-2>7\iff x>3.
$$

Comprueba con $x=4$ y con el valor frontera $x=3$.

## Relaciones

- Calcula: [[Precondición más débil|Precondición más débil]].
- Es una regla para: [[Terna de Hoare|Terna de Hoare]].
- Requiere distinguir: [[Estado de programa|estado anterior y posterior]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 24–27 (láminas 78–81).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 14–16.
- Práctica interactiva: [[Guía paso a paso - Lógica de Hoare#2. Asignación sustituir desde la meta|Asignación: sustituir desde la meta]].
