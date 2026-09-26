---
tipo: concepto
aliases:
  - Reflex agent
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, agentes]
---

# Agente por reflejo

## Definición

Agente que selecciona su siguiente acción a partir de la percepción actual, sin anticipar las consecuencias futuras de esa acción.

## Intuición

Responde con reglas inmediatas del tipo “si ocurre esto, haz aquello”. Puede conservar memoria o un modelo del mundo dentro de su estado actual, pero no realiza una búsqueda de consecuencias antes de actuar.

## Ejemplo mínimo

Un termostato enciende la calefacción cuando la temperatura percibida cae por debajo de un umbral, sin construir planes de estados futuros.

## Límites

Puede ser racional cuando la percepción actual basta para elegir bien y las reglas reflejas coinciden con el objetivo. Es insuficiente cuando una decisión requiere comparar consecuencias a varios pasos.

## Relaciones

- Es una posible arquitectura de: [[Agente racional|Agente racional]].
- Contrasta con: [[Agente planificador|Agente planificador]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositiva 7.
