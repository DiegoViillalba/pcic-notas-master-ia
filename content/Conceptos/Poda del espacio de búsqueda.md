---
tipo: concepto
aliases: [Poda, Pruning]
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Clase del 20 de agosto]]"
tags: [concepto, algoritmos, busqueda]
---

# Poda del espacio de búsqueda

## Definición

Descarte anticipado de una solución parcial cuando ya se puede demostrar que ninguna de sus extensiones satisfará las restricciones.

## Intuición

Podar un nodo elimina todo el subárbol que nacería de él. En las ocho reinas se poda al repetir columna o diagonal; en un cuadro mágico se puede podar cuando una suma parcial excede la constante mágica.

## Límite

Una prueba de poda debe ser segura: si descarta un estado que todavía podía conducir a una solución, el algoritmo queda incompleto. Una poda débil conserva la corrección, pero explora más nodos.

## Relaciones

- Es el mecanismo de eficiencia central de [[Backtracking|backtracking]].
- En optimización, las cotas de calidad conducen a *branch and bound*.

## Procedencia

[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Ocho reinas y cuadros mágicos]].
