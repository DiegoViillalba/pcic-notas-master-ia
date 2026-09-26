---
tipo: concepto
aliases:
  - Corrección parcial
  - Corrección total
  - Partial and total correctness
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, correccion, terminacion, logica-de-hoare]
---

# Corrección parcial y corrección total

## Definición

La corrección parcial garantiza que, si un programa termina desde un estado permitido, su resultado cumple la postcondición. La corrección total añade que el programa efectivamente termina para toda entrada permitida.

## Intuición

“Si termina, responde bien” y “termina y responde bien” son afirmaciones distintas. Los ciclos y la recursión obligan a justificar ambas.

## Formulación

$$
\text{corrección total}
=
\text{corrección parcial}
+
\text{terminación}.
$$

```text
demostrar_total(P, C, Q):
    demostrar que {P} C {Q} es parcialmente correcta
    demostrar que toda ejecución de C iniciada en P termina
```

## Ejemplo mínimo

Un ciclo que busca un elemento puede devolver una posición correcta siempre que termine; eso solo prueba corrección parcial. Una cota que haga avanzar el índice hasta `n` prueba además terminación.

En `while i<n do i:=i+1`, $E=n-i$ es una [[Función variante|variante]]: bajo la guarda es positiva y cada vuelta la reduce en uno.

## Contraejemplo o límites

Un ciclo infinito satisface vacíamente una terna de corrección parcial para cualquier postcondición, porque nunca existe estado final; no es totalmente correcto.

## Relaciones

- Se expresa mediante: [[Terna de Hoare|Terna de Hoare]].
- La corrección total requiere: [[Terminación de un algoritmo|Terminación de un algoritmo]].
- Los ciclos suelen usar: [[Invariante de ciclo|Invariante de ciclo]].
- La terminación de ciclos puede probarse con: [[Función variante|Función variante]].
- Una herramienta expresa las obligaciones como: [[Condición de verificación|condiciones de verificación]].
- Se relaciona con: [[Validez de un algoritmo|Validez de un algoritmo]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 10–11 (láminas 64–65).
- Precisión: en la diapositiva 11, “no incluyan ciclos o recursiones” debe leerse “incluyan ciclos o recursiones”.
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 79–91.
- Práctica: [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|demostración paso a paso de un ciclo]].
