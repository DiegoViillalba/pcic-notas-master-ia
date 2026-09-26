---
tipo: concepto
aliases:
  - Regla del if de Hoare
  - Regla de selección de Hoare
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]]"
tags: [concepto, programacion, logica-de-hoare, condicionales]
---

# Regla condicional de Hoare

## Definición

Regla que demuestra un condicional separando los estados que satisfacen \(B\) de los que satisfacen \(\neg B\). Cada camino debe garantizar una postcondición común \(Q\).

## Formulación

Con `else`:

$$
\frac{\{P\land B\}C_1\{Q\}\qquad\{P\land\neg B\}C_2\{Q\}}
{\{P\}\ \textbf{if }B\textbf{ then }C_1\textbf{ else }C_2\ \{Q\}}.
$$

Sin `else`, la rama falsa equivale a `skip`:

$$
\frac{\{P\land B\}C_1\{Q\}\qquad(P\land\neg B)\Rightarrow Q}
{\{P\}\ \textbf{if }B\textbf{ then }C_1\ \{Q\}}.
$$

## Intuición

\(B\) y \(\neg B\) cubren todos los resultados de evaluar la condición. Si ambos caminos terminan satisfaciendo \(Q\), el condicional completo garantiza \(Q\).

## Ejemplo mínimo

$$
\{\top\}\ \textbf{if }max<a\textbf{ then }max:=a\ \{max\ge a\}.
$$

- Si \(max<a\), la asignación deja \(max=a\).
- Si \(\neg(max<a)\), ya se cumple \(max\ge a\).

## Contraejemplo o límites

Verificar solo la rama con asignación es insuficiente. En un `if` sin `else`, el camino falso conserva el estado y debe satisfacer \(Q\) por implicación. La regla no prueba que evaluar \(B\) esté definido ni que las ramas terminen.

## Lista de comprobación

1. Escribir la guarda $B$ y su negación $\neg B$.
2. Agregar $P$ a las dos ramas.
3. Calcular las precondiciones de cada cuerpo hacia atrás.
4. Verificar que las dos ramas llegan a la **misma** $Q$.

Ejemplo resuelto: [[Guía paso a paso - Lógica de Hoare#4. Condicionales demostrar todos los caminos|valor absoluto paso a paso]].

## Relaciones

- Verifica: [[Terna de Hoare|ternas de Hoare]] con bifurcación.
- Usa dentro de las ramas: [[Axioma de asignación de Hoare|axioma de asignación]].
- Ajusta condiciones con: [[Regla de consecuencia de Hoare|regla de consecuencia]].
- Se integra en: [[Verificación formal de programas|verificación formal]].

## Procedencia

- Clase: [[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]].
- Fuente: *Programación Avanzada Notas 5*, diapositivas 13–19 (láminas 94–100).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 26–27 y 61–62.
