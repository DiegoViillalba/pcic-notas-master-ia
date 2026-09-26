---
tipo: concepto
aliases:
  - Planning agent
  - Agente que planea
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, agentes, planeacion]
---

# Agente planificador

## Definición

Agente que elige acciones comparando hipótesis sobre sus consecuencias y su capacidad para acercar el mundo a una meta formulada.

## Requisitos

- Un modelo de cómo evoluciona el mundo.
- Una meta que describa cómo debería ser el mundo.
- Un mecanismo para considerar “¿qué pasaría si ejecuto esta acción?”.

## Ejemplo mínimo

Para viajar de Arad a Bucarest, el agente considera secuencias de ciudades conectadas antes de ejecutar el primer desplazamiento.

## Límites

La calidad del plan depende de la fidelidad del modelo y de la formulación de la meta. Considerar consecuencias también aumenta el costo de cómputo frente a una respuesta refleja.

## Relaciones

- Es una posible arquitectura de: [[Agente racional|Agente racional]].
- Contrasta con: [[Agente por reflejo|Agente por reflejo]].
- Utiliza una: [[Formulación de un problema de búsqueda|Formulación de un problema de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositiva 8.
