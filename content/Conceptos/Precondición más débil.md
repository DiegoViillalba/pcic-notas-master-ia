---
tipo: concepto
aliases:
  - Weakest precondition
  - wp
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica-de-hoare, verificacion-formal]
---

# Precondición más débil

## Definición

La precondición más débil es la condición menos restrictiva que debe cumplir el estado inicial para garantizar una postcondición $Q$. En la convención precisa de Dijkstra:

- $wlp(C,Q)$ (*weakest liberal precondition*) corresponde a **corrección parcial**;
- $wp(C,Q)$ (*weakest precondition*) corresponde a **corrección total** e incluye terminación.

Para código determinista sin ciclos, las ecuaciones de $wp$ y $wlp$ coinciden; muchas notas introductorias escriben simplemente `wp` aunque estén verificando solo corrección parcial.

## Intuición

Se fija primero la salida deseada y se pregunta qué debía ser verdad justo antes de cada instrucción. Así se verifica el programa en orden inverso a su ejecución.

## Formulación

Para una asignación, la misma ecuación vale para ambos transformadores (si evaluar $E$ termina):

$$
T(V:=E,Q)=Q^{V}_{E}\equiv Q[E/V],\qquad T\in\{wp,wlp\}.
$$

Para una secuencia:

$$
T(C_1;C_2,Q)=T(C_1,T(C_2,Q)).
$$

Para un condicional determinista:

$$
T(\mathbf{if}\ B\ \mathbf{then}\ C_1\ \mathbf{else}\ C_2,Q)
=
(B\Rightarrow T(C_1,Q))\land(\neg B\Rightarrow T(C_2,Q)).
$$

## Ejemplo mínimo

```text
código: x := x+1; y := 2*x
Q:      y > 10

wlp(y := 2*x, y > 10) = x > 5
wlp(x := x+1, x > 5)  = x > 4
```

## Contraejemplo o límites

No es obligatorio declarar exactamente la condición más débil. Para corrección parcial basta cualquier $P$ tal que $P\Rightarrow wlp(C,Q)$; para corrección total se requiere $P\Rightarrow wp(C,Q)$.

## Relaciones

- Para asignaciones utiliza: [[Axioma de asignación de Hoare|Axioma de asignación de Hoare]].
- Se compara mediante: [[Fortaleza lógica de una aserción|Fortaleza lógica de una aserción]].
- Permite demostrar: [[Terna de Hoare|ternas de Hoare]].
- Se relaciona con la generación de: [[Condición de verificación|condiciones de verificación]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 23–27 (láminas 77–81); el nombre `wp` explicita la idea presentada de deducir la precondición desde la postcondición.
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 70–77; allí se reserva `wlp` para corrección parcial y `wp` para corrección total.
- Ejercicios: [[Guía paso a paso - Lógica de Hoare#3. Secuencias una condición intermedia une dos pruebas|Secuencias paso a paso]].
