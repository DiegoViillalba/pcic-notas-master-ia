---
tipo: concepto
aliases: [Algoritmo de aceptación diferida]
area: algoritmos
estado: desarrollado
tags: [concepto, algoritmos]
---
# Algoritmo de Gale-Shapley

## Definición

Algoritmo para hallar un [[Emparejamiento estable]] en un mercado bipartito con preferencias estrictas y completas.

## Funcionamiento

Un lado propone en orden de preferencia; el receptor conserva la mejor propuesta provisional y rechaza las demás.

## Propiedades

- Termina tras a lo sumo $n^2$ propuestas.
- Devuelve un emparejamiento perfecto y estable cuando ambos lados tienen $n$ participantes.
- Favorece al lado proponente: produce su solución estable óptima.

## Relaciones

- Implementa: [[Aceptación diferida]].
- Produce: [[Óptimo para hospitales]] cuando los hospitales proponen.
