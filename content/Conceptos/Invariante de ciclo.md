---
tipo: concepto
aliases:
  - Invariante de bucle
  - Loop invariant
area: algoritmos
materias:
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]"
  - "[[2026-09-01 ProgAv - Verificación de condicionales y ciclos por inducción|Verificación de condicionales y ciclos por inducción]]"
tags: [concepto, algoritmos, correccion]
---

# Invariante de ciclo

## Definición

Propiedad que es verdadera antes de iniciar un ciclo y que se conserva después de cada iteración.

## Intuición

Resume aquello que el algoritmo ya ha conseguido y que las iteraciones futuras no deben destruir. Sirve como puente entre los pasos locales del ciclo y la afirmación global de corrección.

## Formulación

Para un estado $s_t$ al inicio de la iteración $t$, una propiedad $P$ es invariante si se justifican:

1. **Inicialización:** $P(s_0)$.
2. **Mantenimiento:** $P(s_t)\Rightarrow P(s_{t+1})$.
3. **Terminación:** $P$ junto con la condición de salida implica la poscondición buscada.

En el algoritmo de los hot cakes puede usarse:

$$
P(h): \text{los }h\text{ hot cakes del fondo forman un sufijo ordenado y definitivo}.
$$

Además, cada iteración garantiza el progreso $h_{t+1}\ge h_t+1$.

## Ejemplo mínimo

En una búsqueda lineal, antes de examinar la posición $i$, el valor buscado no aparece en las posiciones $1,\ldots,i-1$ ya revisadas.

## Contraejemplo o límites

Una propiedad observada en varios ejemplos no es un invariante hasta demostrar su inicialización y mantenimiento. La desigualdad $h_{t+1}>h_t$ expresa progreso; por sí sola no sustituye la propiedad estructural que se conserva.

## Plantilla de Hoare

Para `while B do C`, un candidato $I$ debe satisfacer:

$$
P\Rightarrow I,
\qquad
\{I\land B\}C\{I\},
\qquad
I\land\neg B\Rightarrow Q.
$$

Una heurística útil es escribir el invariante como una relación entre **lo hecho hasta ahora**, **lo que falta** y **el resultado final**. En el factorial descendente, $Y$ es el producto acumulado, $X!$ es lo que falta y $Y\cdot X!=n!$ permanece constante.

Para demostrar terminación se necesita además una [[Función variante|función variante]]; no forma parte del invariante.

## Relaciones

- Se utiliza para demostrar: [[Validez de un algoritmo|Validez de un algoritmo]].
- Combinado con una medida de progreso permite justificar: [[Terminación de un algoritmo|Terminación de un algoritmo]].
- Se aplica en: [[Ordenamiento de hot cakes|Ordenamiento de hot cakes]].
- Requiere conocer: [[Inducción matemática aplicada a ciclos|inducción matemática]] y especificación de ciclos.
- Se traduce a: [[Condición de verificación|condiciones de verificación]].

## Procedencia

- Clase: [[2026-08-13 ADA - Algoritmo de los hot cakes|Algoritmo de los hot cakes]]
- Fuente: *El Algoritmo de los Hot Cakes*.
- Página o sección: diapositivas 7–9.
- Clase: [[2026-09-01 ProgAv - Verificación de condicionales y ciclos por inducción|Verificación de condicionales y ciclos por inducción]].
- Fuente: *Programación Avanzada Notas 6*, diapositivas 9–17 (láminas 109–117).
- Fuente complementaria: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 28–35 y 67–69.
- Práctica: [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|Ciclos: invariante, salida y variante]].

## Pregunta de repaso

- ¿Qué expresión entera no negativa disminuye en cada vuelta del ciclo estudiado?
