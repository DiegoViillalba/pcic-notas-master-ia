---
tipo: concepto
aliases:
  - Inducción para verificar ciclos
  - Inducción sobre iteraciones
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-09-01 ProgAv - Verificación de condicionales y ciclos por inducción|Verificación de condicionales y ciclos por inducción]]"
tags: [concepto, programacion, verificacion-formal, induccion, ciclos]
---

# Inducción matemática aplicada a ciclos

## Definición

Técnica para demostrar que una propiedad \(P(n)\) del estado de un programa es cierta después de cualquier número \(n\ge0\) de iteraciones de un ciclo.

## Correspondencia con el ciclo

1. **Caso base \(P(0)\):** la propiedad vale antes de ejecutar el cuerpo.
2. **Hipótesis \(P(n)\):** se supone que vale después de \(n\) iteraciones.
3. **Paso \(P(n)\Rightarrow P(n+1)\):** una ejecución del cuerpo conserva la propiedad.

Cuando se prueban estas obligaciones, \(P\) es un [[Invariante de ciclo|invariante de ciclo]].

## Ejemplo mínimo

En el ciclo:

~~~text
C := 0
D := 0
while D != A
    C := C + A
    D := D + 1
~~~

la propiedad es \(P(n):C_n=D_nA\).

- Base: \(C_0=0=D_0A\).
- Paso: si \(C_n=D_nA\), entonces

$$
C_{n+1}=C_n+A=(D_n+1)A=D_{n+1}A.
$$

## Límites

La inducción demuestra preservación, pero no basta por sí sola para concluir el resultado ni la terminación. También hacen falta la condición de salida y, para corrección total, una variante decreciente.

## Relaciones

- Produce: [[Invariante de ciclo|invariantes de ciclo]].
- Se expresa con: [[Terna de Hoare|ternas de Hoare]].
- Distingue: [[Corrección parcial y corrección total|corrección parcial y total]].

## Procedencia

- Clase: [[2026-09-01 ProgAv - Verificación de condicionales y ciclos por inducción|Verificación de condicionales y ciclos por inducción]].
- Fuente: *Programación Avanzada Notas 6*, diapositivas 8–17 (láminas 108–117).

