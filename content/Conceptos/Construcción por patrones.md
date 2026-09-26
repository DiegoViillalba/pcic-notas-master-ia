---
tipo: concepto
aliases: [Solución por patrones]
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Clase del 20 de agosto]]"
tags: [concepto, algoritmos, patrones]
---

# Construcción por patrones

## Definición

Técnica que identifica una regularidad en soluciones conocidas y la convierte en una regla capaz de generar nuevas soluciones sin enumerar todo el espacio de búsqueda.

## Ejemplo

En cuadros mágicos de orden impar, el método siamés mueve cada número arriba y a la derecha con envoltura; si la casilla está ocupada, baja desde la posición actual. Para órdenes múltiplos de cuatro se puede llenar en secuencia y complementar posiciones según bloques $4\times4$.

## Ventaja y límite

Una construcción suele ser mucho más rápida que [[Backtracking|backtracking]], pero normalmente vale solo para una familia bien definida y debe verificarse o demostrarse que preserva las restricciones.

## Relaciones

- Se aplica a [[Cuadro mágico|cuadros mágicos]].
- Contrasta con enumerar alternativas mediante un árbol de decisiones.

## Procedencia

[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Ocho reinas y cuadros mágicos]].
