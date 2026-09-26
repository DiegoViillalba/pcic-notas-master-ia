---
tipo: concepto
aliases:
  - Invariante de código
  - Propiedad preservada por un programa
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]]"
tags: [concepto, programacion, logica-de-hoare, invariantes]
---

# Invariante de programa

## Definición

Aserción \(I\) que un fragmento \(C\) preserva:

$$
\{I\}\ C\ \{I\}.
$$

## Intuición

Las variables pueden cambiar, pero la relación descrita por \(I\) sigue siendo verdadera. Un invariante caracteriza una estructura estable, no necesariamente valores constantes.

## Ejemplo mínimo

El bloque:

~~~text
i := i + 1
r := 2 * r
~~~

preserva \(r=2^i\). Si \(r_0=2^{i_0}\), entonces:

$$
i_1=i_0+1,\qquad r_1=2r_0=2^{i_0+1}=2^{i_1}.
$$

## Contraejemplo o límites

Comprobar algunos valores no demuestra invariancia para todos los estados. Hace falta una prueba simbólica. Además, una propiedad preservada por el cuerpo de un ciclo no basta como invariante de ciclo si no se demuestra que vale antes de la primera iteración.

## Cuando aparece dentro de un ciclo

La preservación $\{I\}C\{I\}$ es solo una pieza. En un `while B do C` se usa la hipótesis más precisa $I\land B$, se prueba inicialización y se combina $I$ con $\neg B$ al salir. Para terminación se añade una [[Función variante|función variante]].

Desarrollo completo: [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|Ciclos: invariante, salida y variante]].

## Relaciones

- Se expresa mediante: [[Terna de Hoare|Terna de Hoare]].
- Se demuestra en secuencias con: [[Regla de composición de Hoare|Regla de composición de Hoare]].
- Caso especializado: [[Invariante de ciclo|Invariante de ciclo]].
- Ayuda en: [[Verificación formal de programas|Verificación formal de programas]].

## Procedencia

- Clase: [[2026-08-27 ProgAv - Composición, invariantes y condicionales de Hoare|Composición, invariantes y condicionales de Hoare]].
- Fuente: *Programación Avanzada Notas 5*, diapositivas 9–12 (láminas 90–93).
