---
tipo: concepto
aliases: [Likelihood weighting]
area: inteligencia-artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-10-15 IA - Muestreo en redes bayesianas]]"
  - "[[AI 16 muestreo en redes bayesianas.pdf]]"
tags: [concepto, inteligencia-artificial, muestreo]
---

# Verosimilitud con pesos

## Pregunta

¿Cómo usar la evidencia durante la generación sin sesgar una posterior?

## Idea

Fijamos los valores observados y sorteamos los demás nodos en orden topológico. Cada mundo recibe el peso $w=\prod_{E_i\in\mathcal E}P(e_i\mid\operatorname{pa}(E_i))$. Estimamos la posterior con el cociente de las sumas de pesos asignadas a cada valor de la consulta.

La distribución de generación por sí sola no es la posterior. Multiplicar la probabilidad de generación por $w$ recupera la masa conjunta $P(\mathbf z,\mathbf e)$. Si casi todos los pesos son diminutos, el número efectivo de muestras puede ser bajo aunque se hayan generado muchos mundos.

## Ejemplo y procedencia

Con evidencia $+s,+w$ en la red de la clase, un mundo $+c,+s,+r,+w$ pesa $P(+s\mid+c)P(+w\mid+s,+r)=0.1(0.99)=0.099$. Véase [[2026-10-15 IA - Muestreo en redes bayesianas#6. Verosimilitud con pesos: fijar la evidencia y corregir el sesgo|la explicación completa]], diapositivas 15–17.
