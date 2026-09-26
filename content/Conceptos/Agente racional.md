---
tipo: concepto
aliases:
  - Rational agent
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-11 IA - Introduccion|Introducción a IA]]"
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, agentes]
---

# Agente racional

## Definición

Entidad que percibe un ambiente, actúa sobre él y selecciona una acción que maximiza su utilidad esperada con la información disponible.

## Intuición

La racionalidad describe la calidad de la decisión según lo que el agente percibe y conoce; no exige acertar siempre ni conocer de antemano el resultado real.

## Elementos

- **Percepciones:** información recibida por los sensores.
- **Acciones:** intervenciones disponibles mediante actuadores.
- **Indicador de desempeño:** criterio con el que se evalúa el comportamiento.
- **Ambiente:** mundo en el que el agente percibe y actúa.

## Regla de decisión

Si $A$ es el conjunto de acciones disponibles y $I$ la información del agente, la idea se resume como

$$
a^*\in\operatorname*{arg\,max}_{a\in A}\,\mathbb{E}[U\mid a,I].
$$

La percepción, el ambiente y el espacio de acciones determinan qué técnicas permiten aproximar esta elección.

## Ejemplo mínimo

Un conductor de taxi evalúa acciones como acelerar, frenar o girar según seguridad, rapidez, legalidad, comodidad y ganancias esperadas.

## Relaciones

- Opera en un: [[Entorno de tarea|Entorno de tarea]].
- Puede maximizar: [[Utilidad esperada|Utilidad esperada]].
- Puede implementarse como: [[Agente por reflejo|Agente por reflejo]] o [[Agente planificador|Agente planificador]], según el problema.

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 4–5.
