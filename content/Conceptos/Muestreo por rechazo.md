---
tipo: concepto
aliases: [Rejection sampling]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-15 IA - Muestreo en redes bayesianas]]"
  - "[[AI 16 muestreo en redes bayesianas.pdf]]"
tags: [concepto, inteligencia-artificial, muestreo]
---

# Muestreo por rechazo

## Pregunta

¿Cómo estimamos $P(Q\mid\mathbf e)$ a partir de muestras de la conjunta?

## Idea

Generamos mundos mediante [[Muestreo previo|muestreo previo]] y conservamos solo los que coinciden con la evidencia. La fracción de mundos aceptados con $Q=q$ estima $P(Q=q\mid\mathbf e)$. Si no se acepta ninguno, la estimación queda indefinida.

La fracción aceptada tiende a $P(\mathbf e)$: una evidencia rara desperdicia casi todos los intentos porque no guía la generación. Con $N$ intentos esperamos $NP(\mathbf e)$ muestras útiles, aunque la cantidad real fluctúa.

## Procedencia

[[2026-10-15 IA - Muestreo en redes bayesianas#5. Muestreo por rechazo: conservar solo mundos compatibles|Clase del 15 de octubre]], diapositivas 12–14.
