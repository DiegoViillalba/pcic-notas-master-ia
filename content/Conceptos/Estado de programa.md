---
tipo: concepto
aliases:
  - Estado computacional
  - Program state
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, semantica, verificacion-formal]
---

# Estado de programa

## Definición

Asignación de valores a las variables relevantes de un programa en un instante de su ejecución.

## Intuición

Ejecutar una instrucción transforma un estado en otro. Las aserciones describen conjuntos de estados posibles, no pasos de ejecución.

## Formulación

Un estado puede modelarse como una función $s:\mathrm{Var}\to\mathrm{Val}$. Se escribe:

$$
s\models P
$$

cuando los valores dados por $s$ hacen verdadera la aserción $P$.

## Ejemplo mínimo

```text
s0 = {x = 2, y = 5}
ejecutar x := x + 1
s1 = {x = 3, y = 5}
```

$s_0\models x\ge2$ y $s_1\models x=3$, pero $s_1\not\models x=2$.

## Contraejemplo o límites

Una condición parcial como $x\ge2$ no determina un solo estado: permite $x=2$, $x=5$ y muchos otros valores, además de múltiples valores para las variables no mencionadas.

## Relaciones

- Satisface o refuta: [[Aserción de programa|Aserción de programa]].
- Es transformado por el código en: [[Terna de Hoare|Terna de Hoare]].
- Requiere distinguir estado inicial y final al aplicar: [[Axioma de asignación de Hoare|Axioma de asignación de Hoare]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 5 y 7 (láminas 59 y 61).

