---
tipo: concepto
aliases:
  - Search problem formulation
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Formulación de un problema de búsqueda

## Definición

Abstracción que especifica desde dónde comienza un agente, qué estados y acciones considera y cómo reconoce que alcanzó su objetivo.

## Componentes

| Componente | Definición | Ejemplo: Rumania |
|---|---|---|
| [[Espacio de estados|Espacio de estados]] | Configuraciones consideradas por el problema | Ciudades |
| Estado inicial | Configuración desde la que comienza la búsqueda | Arad |
| [[Función sucesor|Función sucesor]] | Acciones disponibles, estados resultantes y costos | Viajar por un camino a una ciudad adyacente |
| [[Prueba de meta|Prueba de meta]] | Condición que identifica el objetivo | ¿La ciudad actual es Bucarest? |

## Intuición

Formular es decidir qué detalles del mundo importan. La búsqueda opera sobre esta representación, no sobre toda la realidad.

## Ejemplo mínimo

En Magic 8, un estado es una configuración de ocho fichas y un hueco; una acción mueve una ficha adyacente al hueco y la prueba de meta compara la configuración actual con la deseada.

## Límites

Una formulación que elimina información necesaria puede producir planes inviables. Una que conserva demasiado detalle puede hacer inmanejable el espacio de búsqueda.

## Relaciones

- Es utilizada por un: [[Agente planificador|Agente planificador]].
- Se representa mediante un: [[Grafo de espacio de estados|Grafo de espacio de estados]].
- Puede explorarse mediante un: [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: *AI 2 Agentes Inteligentes*, diapositivas 10 y 17–18.
