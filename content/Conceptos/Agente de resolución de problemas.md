---
tipo: concepto
aliases:
  - Problem-solving agent
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-13 IA - Resolviendo problemas con búsqueda I|Búsqueda I]]"
tags: [concepto, inteligencia-artificial, busqueda]
---

# Agente de resolución de problemas

## Definición

Agente que transforma una meta en un problema de búsqueda, encuentra una secuencia de acciones que la alcanza y después ejecuta esa secuencia.

## Intuición

Cuando la mejor acción no es evidente, el agente no actúa de inmediato: representa las alternativas y busca un camino desde su estado actual hasta una meta.

## Ciclo del agente

1. Actualiza su estado a partir de lo que percibe.
2. Formula una meta.
3. Construye una [[Formulación de un problema de búsqueda|formulación de búsqueda]].
4. Busca una secuencia de acciones que llegue a la meta.
5. Ejecuta la primera acción y continúa con el plan; si el mundo cambia, puede tener que buscar de nuevo.

## Supuestos sobre el entorno

La versión básica funciona mejor en ambientes observables, conocidos, deterministas, discretos y estáticos. Bajo estos supuestos, el agente puede anticipar el resultado de cada acción y ejecutar una solución sin corregirla a cada paso.

## Ejemplo mínimo

Para viajar de Arad a Bucarest, el agente usa las ciudades como estados y los caminos como acciones. Busca una ruta que termine en Bucarest y luego comienza a recorrerla.

## Límites y confusiones

- Encontrar una solución no implica encontrar la de menor costo; eso depende del algoritmo utilizado.
- Si una acción produce un resultado inesperado, el plan calculado puede dejar de ser válido.
- No es cualquier agente con una meta: se caracteriza por formular el problema y buscar una secuencia de acciones antes de ejecutarla.

## Relaciones

- Es un tipo de: [[Agente planificador|Agente planificador]].
- Puede actuar racionalmente como: [[Agente racional|Agente racional]].
- Utiliza una: [[Formulación de un problema de búsqueda|Formulación de un problema de búsqueda]].
- Genera un: [[Árbol de búsqueda|Árbol de búsqueda]].

## Procedencia

- Clase: [[2026-08-13 IA - Resolviendo problemas con búsqueda I|Agentes y búsqueda]].
- Fuente: Russell y Norvig, *Artificial Intelligence: A Modern Approach*, 4.ª ed., capítulo 3. Copia local: [[Artificial_inteliigence-A_modern_approach|Artificial Intelligence: A Modern Approach]].
