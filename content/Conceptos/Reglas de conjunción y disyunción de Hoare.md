---
tipo: concepto
aliases:
  - Regla de conjunción de Hoare
  - Regla de disyunción de Hoare
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]]"
tags: [concepto, programacion, logica-de-hoare, inferencia]
---

# Reglas de conjunción y disyunción de Hoare

## Definición

Reglas que combinan dos ternas demostradas para el mismo código, reuniendo sus precondiciones y postcondiciones mediante conjunción o disyunción.

## Intuición

La conjunción acumula garantías cuando ambas hipótesis son válidas; la disyunción reúne dos casos alternativos ya demostrados.

## Formulación

$$
\frac{\{P_1\}C\{Q_1\}\qquad\{P_2\}C\{Q_2\}}
{\{P_1\land P_2\}C\{Q_1\land Q_2\}},
$$

$$
\frac{\{P_1\}C\{Q_1\}\qquad\{P_2\}C\{Q_2\}}
{\{P_1\lor P_2\}C\{Q_1\lor Q_2\}}.
$$

## Ejemplo mínimo

```text
si se demostró {P1} C {Q1} y {P2} C {Q2}:
    bajo P1 y P2, conservar Q1 y Q2
    bajo P1 o P2, conservar Q1 o Q2
```

Para `i := i+1`, combinar la relación $i=i_0+1$ con la preservación de positividad permite derivar $i>1$ cuando $i_0>0$.

## Contraejemplo o límites

Las dos premisas deben referirse al mismo comando $C$. Además, `i=i+1` es ambigua si no se diferencia el valor anterior $i_0$ del posterior.

## Uso paso a paso

- Usa **conjunción** cuando necesitas acumular dos garantías del mismo programa.
- Usa **disyunción** cuando ya probaste casos alternativos de entrada.
- Después simplifica la salida con la [[Regla de consecuencia de Hoare|regla de consecuencia]].

Para ver cómo estas reglas encajan con asignaciones, secuencias y ramas, consulta [[Guía paso a paso - Lógica de Hoare|la guía paso a paso]].

## Relaciones

- Combinan: [[Terna de Hoare|ternas de Hoare]].
- Su resultado puede simplificarse con: [[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]].
- Utilizan conectivos entre: [[Aserción de programa|aserciones]].

## Procedencia

- Clase: [[2026-08-25 ProgAv - Ternas de Hoare y demostración formal|Ternas de Hoare y demostración formal]].
- Fuente: *Programación Avanzada Notas 4 2027*, diapositivas 20–22 (láminas 74–76).
