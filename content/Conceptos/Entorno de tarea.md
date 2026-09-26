---
tipo: concepto
aliases:
  - Task environment
  - Ambiente de tarea
  - PEAS
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-11 IA - Introduccion|Introducción a IA]]"
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, agentes]
---

# Entorno de tarea

## Definición

Descripción del problema en el que opera un agente mediante su indicador de desempeño, el ambiente, los actuadores y los sensores. Estos cuatro elementos corresponden al esquema conocido como PEAS, aunque la presentación no usó explícitamente ese acrónimo.

## Componentes

| Componente | Función |
|---|---|
| Indicador de desempeño | Define qué resultados cuentan como buen comportamiento. |
| Ambiente | Delimita el mundo externo relevante para la tarea. |
| Actuadores | Permiten que el agente ejecute acciones. |
| Sensores | Proporcionan percepciones del ambiente. |

## Ejemplo: conductor de taxi

| Desempeño | Ambiente | Actuadores | Sensores |
|---|---|---|---|
| Seguridad, rapidez, legalidad, comodidad y ganancias | Camino, tráfico y clientes | Acelerador, freno, volante y claxon | Cámaras, sonar, velocímetro, GPS y sensores del motor |

## Caracterización del ambiente

Además de identificar sus componentes, un ambiente puede clasificarse mediante contrastes como completamente o parcialmente observable, de agente único o multiagente, determinista o estocástico, episódico o secuencial, estático o dinámico, discreto o continuo y conocido o desconocido.

## Relaciones

- Condiciona el diseño de un: [[Agente racional|Agente racional]].
- Sus sensores producen percepciones utilizadas por un: [[Agente por reflejo|Agente por reflejo]].
- Su dinámica debe ser modelada por un: [[Agente planificador|Agente planificador]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositiva 5.
