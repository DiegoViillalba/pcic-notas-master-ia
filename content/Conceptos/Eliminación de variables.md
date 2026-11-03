---
tipo: concepto
aliases: [Variable elimination, VE]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-13 IA - Inferencia en redes bayesianas]]"
  - "[[AI 15 Inferencia en redes bayesianas.pdf]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf]]"
tags: [concepto, inteligencia-artificial, inferencia-probabilistica]
---

# Eliminación de variables

## Pregunta

¿Cómo calculamos una posterior exacta evitando construir primero toda la distribución conjunta?

## Definición e intuición

La eliminación de variables reorganiza una suma de productos de factores. Para cada variable oculta, multiplica todos los factores que la mencionan, suma sus valores y reemplaza los factores usados por el resumen obtenido. Después multiplica los factores restantes y normaliza sobre la consulta.

La propiedad distributiva permite dejar fuera de una suma lo que no depende de su variable. Guardar los resúmenes evita repetir subcálculos; es una forma de [[Programación dinámica|programación dinámica]].

## Formulación de un paso

Si $\mathcal F_V$ contiene todos los factores actuales que mencionan $V$:

$$h(S\setminus\{V\})=\sum_V\prod_{f\in\mathcal F_V}f,\qquad S=\bigcup_{f\in\mathcal F_V}\operatorname{scope}(f).$$

Se retira $\mathcal F_V$ de la lista y se agrega $h$. Los demás factores esperan.

## Ejemplo mínimo

En $R\to T\to L$, sean $P(r)=0.1$, $P(t\mid r)=0.8$, $P(t\mid\neg r)=0.1$, $P(l\mid t)=0.3$ y $P(l\mid\neg t)=0.1$.

1. Eliminar $R$: $P(t)=0.1(0.8)+0.9(0.1)=0.17$ y $P(\neg t)=0.83$.
2. Eliminar $T$: $P(l)=0.17(0.3)+0.83(0.1)=0.134$.
3. La respuesta completa es $P(L)=\langle0.134,0.866\rangle$.

La mayor tabla de producto usa dos variables y cuatro entradas. Formar primero la conjunta de tres booleanas necesitaría ocho entradas.

## Límites y confusiones

- Es un método exacto, al igual que [[Inferencia por enumeración]].
- El orden conserva la respuesta, pero cambia los factores intermedios y su costo.
- No se elimina la consulta; la evidencia se fija antes de operar.
- No se puede sumar una variable en un factor aislado si otros factores aún la mencionan.
- El costo puede ser exponencial: depende de los alcances y dominios de las tablas intermedias.

## Relaciones

- Opera sobre [[Factor probabilístico|factores probabilísticos]].
- Reorganiza los cálculos de [[Inferencia por enumeración]].
- Reutiliza subresultados como [[Programación dinámica]].

## Procedencia

- Clase: [[2026-10-13 IA - Inferencia en redes bayesianas|13 de octubre de 2026]], §§7–13, con laboratorios incrustados.
- Presentación AI 15, diapositivas 16–31.
- AIMA, 4.ª edición global, §§13.3.2–13.3.3, pp. 448–452.
