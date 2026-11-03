---
tipo: concepto
aliases: [Gibbs sampling]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-15 IA - Muestreo en redes bayesianas]]"
  - "[[AI 16 muestreo en redes bayesianas.pdf]]"
tags: [concepto, inteligencia-artificial, muestreo, mcmc]
---

# Muestreo de Gibbs

## Pregunta

¿Cómo aproximamos una posterior actualizando una asignación compatible con la evidencia?

## Idea

Fijamos la evidencia y mantenemos un estado para todas las demás variables. En cada paso elegimos una variable no observada $X$ y la volvemos a sortear condicionada en los valores actuales del resto. Para calcular esa distribución solo hacen falta la CPT de $X$ y las CPT de sus hijos: los otros factores se cancelan al normalizar.

Gibbs es un método de cadena de Markov Monte Carlo. Las muestras consecutivas están correlacionadas, y la convergencia requiere que la cadena pueda explorar los estados relevantes y haya transcurrido suficiente tiempo. No equivale a generar muestras independientes.

## Ejemplo y procedencia

En la red de pasto mojado, $P(S\mid+c,+r,-w)\propto P(S\mid+c)P(-w\mid S,+r)$; de ahí $P(+s\mid+c,+r,-w)=1/91$. Véase [[2026-10-15 IA - Muestreo en redes bayesianas#7. Gibbs: actualizar un mundo en vez de comenzar de cero|la derivación de la clase]], diapositivas 18–20.
