---
tipo: concepto
aliases:
  - Expected utility
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-11 IA - Introduccion|Introducción a IA]]"
tags:
  - concepto
  - inteligencia-artificial
  - decision
---

# Utilidad esperada

## Definición

Valor promedio de una acción cuando sus resultados son inciertos. Cada resultado se pondera por su probabilidad y por la utilidad que representa para el agente.

La **utilidad** expresa qué tan deseable es un resultado según el objetivo del agente. Es **esperada** porque se calcula antes de conocer cuál resultado ocurrirá.

## Formulación

$$
EU(a)=\sum_s P(s\mid a,I)\,U(s),
$$

donde $a$ es una acción, $s$ un resultado posible, $I$ la información disponible, $P(s\mid a,I)$ su probabilidad y $U(s)$ su utilidad. Un agente racional elige una acción con utilidad esperada máxima.

## Ejemplo mínimo

Un taxi compara dos rutas:

- **Ruta segura:** llega a tiempo con utilidad $6$, así que $EU=6$.
- **Atajo:** llega antes con probabilidad $0.7$ y utilidad $10$, pero se retrasa con probabilidad $0.3$ y utilidad $0$.

$$
EU(\text{atajo})=0.7(10)+0.3(0)=7.
$$

Con estas probabilidades y preferencias, elegiría el atajo porque $7>6$.

## Supuestos y límites

- La decisión depende de que las probabilidades y las utilidades representen razonablemente el problema.
- Maximizar la utilidad esperada no garantiza el mejor resultado real: una decisión racional puede salir mal.
- Utilidad no significa necesariamente dinero; puede combinar seguridad, tiempo, comodidad u otros criterios.
- La actitud frente al riesgo debe quedar reflejada en la función de utilidad.

## Relaciones

- Es maximizada por un: [[Agente racional|Agente racional]].
- Depende del indicador de desempeño definido en el: [[Entorno de tarea|Entorno de tarea]].

## Procedencia

- Clase: [[2026-08-11 IA - Introduccion|Introducción a IA]].
- Fuente: Russell y Norvig, *Artificial Intelligence: A Modern Approach*, 4.ª ed., capítulo 16. Copia local: [[Artificial_inteliigence-A_modern_approach|Artificial Intelligence: A Modern Approach]].
