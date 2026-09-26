---
tipo: concepto
aliases:
  - Demostración formal de programas
  - Formal program verification
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, verificacion-formal, correccion]
---

# Verificación formal de programas

## Definición

Uso de especificaciones matemáticas y reglas lógicas para demostrar que un programa satisface propiedades para todos los estados de entrada permitidos.

## Intuición

Una prueba ordinaria ejecuta algunos ejemplos; la verificación formal razona sobre el conjunto completo descrito por la precondición. La conclusión depende tanto del código como de la especificación elegida.

## Formulación

Para un programa $C$ y una especificación $P,Q$, se busca demostrar:

$$
\forall s,s',\quad P(s)\land \operatorname{Exec}(C,s,s')\Rightarrow Q(s').
$$

Si además toda ejecución que parte de $P$ termina, se obtiene corrección total.

## Ejemplo mínimo

```text
entrada n con n >= 0
r <- raiz(n)
salida r con r >= 0 y r*r = n
```

La demostración debe cubrir todo $n\ge0$, no solo valores probados.

## Contraejemplo o límites

La verificación funcional no implica eficiencia temporal, bajo consumo de memoria ni ausencia de fallos fuera de los supuestos del modelo.

## Relaciones

- Se expresa mediante: [[Terna de Hoare|Terna de Hoare]].
- Distingue: [[Corrección parcial y corrección total|corrección parcial y corrección total]].
- Se apoya en: [[Aserción de programa|aserciones]] y [[Estado de programa|estados de programa]].
- Complementa, pero no sustituye, las pruebas de software.

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 1–3 (láminas 55–57).

