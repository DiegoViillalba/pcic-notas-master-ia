---
tipo: concepto
aliases:
  - Triple de Hoare
  - Hoare triple
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica-de-hoare, verificacion-formal]
---

# Terna de Hoare

## Definición

Expresión $\{P\}C\{Q\}$ que especifica que, al ejecutar el código $C$ desde un estado que satisface $P$, todo estado final alcanzado satisface $Q$.

## Intuición

$P$ establece el contrato de entrada, $C$ transforma el estado y $Q$ establece el contrato de salida. La forma usual expresa corrección parcial: condiciona la salida a que la ejecución termine.

## Formulación

$$
\models\{P\}C\{Q\}
\iff
\forall s,s',\ P(s)\land\operatorname{Exec}(C,s,s')\Rightarrow Q(s').
$$

## Ejemplo mínimo

```text
{ y != 0 }
x := 1 / y
{ x = 1 / y }
```

Con notación histórica más precisa, el `y` de la postcondición es el valor inicial $y_0$.

## Contraejemplo o límites

La terna no afirma por sí sola que $P$ ocurra en la práctica ni que $C$ termine. Para corrección total debe demostrarse la terminación.

## Validez y demostrabilidad

Conviene distinguir:

$$
\models\{P\}C\{Q\}
$$

significa que la terna es verdadera según la semántica, mientras que

$$
\vdash\{P\}C\{Q\}
$$

significa que existe una derivación con las reglas de Hoare. La **corrección** del sistema exige que toda terna demostrable sea válida.

## Para practicar paso a paso

- [[Guía paso a paso - Lógica de Hoare#1. ¿Qué afirma una terna?|¿Qué afirma una terna?]]
- [[Guía paso a paso - Lógica de Hoare#8. Ejercicios graduados|Ejercicios graduados con soluciones]]

## Relaciones

- Utiliza: [[Aserción de programa|aserciones]] y [[Estado de programa|estados]].
- Su significado se divide en: [[Corrección parcial y corrección total|corrección parcial y total]].
- Se transforma con: [[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]].
- Para asignaciones usa: [[Axioma de asignación de Hoare|Axioma de asignación de Hoare]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 2–3 y 8–10 (láminas 56–57 y 62–64).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 4–12 y 92–102.
