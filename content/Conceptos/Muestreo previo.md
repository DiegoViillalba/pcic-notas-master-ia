---
tipo: concepto
aliases: [Prior sampling, Forward sampling]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-15 IA - Muestreo en redes bayesianas]]"
  - "[[AI 16 muestreo en redes bayesianas.pdf]]"
tags: [concepto, inteligencia-artificial, muestreo]
---

# Muestreo previo

## Pregunta

¿Cómo generamos un mundo completo según la distribución conjunta de una red bayesiana?

## Idea

Recorremos los nodos en orden topológico y sorteamos cada $X_i$ de $P(X_i\mid\operatorname{pa}(X_i))$, usando los valores de sus padres ya sorteados. La probabilidad de generar $\mathbf x$ es $\prod_iP(x_i\mid\operatorname{pa}(X_i))=P(\mathbf x)$.

Para estimar $P(Q=q)$, contamos la fracción de mundos con $Q=q$. Si necesitamos una posterior con evidencia, las muestras no la incorporan por sí mismas; podemos filtrar con [[Muestreo por rechazo|rechazo]] o usar otro procedimiento.

## Ejemplo y procedencia

En la red $C\to S$, $C\to R$, $S,R\to W$, sorteamos $C$, después $S$ y $R$, y finalmente $W$. Véase [[2026-10-15 IA - Muestreo en redes bayesianas#4. Muestreo previo: generar mundos completos|la clase del 15 de octubre]], diapositivas 10–11.
