---
tipo: concepto
aliases:
  - Coupling
area: programación avanzada
materias:
  - "[[Indice|Programación Avanzada]]"
estado: semilla
fuentes:
  - "[[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas]]"
tags: [concepto, programacion-avanzada, diseño-modular]
---

# Acoplamiento

## Definición inicial

Medida cualitativa de cuánto conoce o depende una unidad de software de otras unidades y de sus detalles internos.

## Ejemplo mínimo

Un servicio que depende de una interfaz `Repositorio` está menos acoplado a la base de datos concreta que uno que construye consultas SQL directamente en todos sus métodos.

## Intuición

Cuanto más difícil sea cambiar una unidad sin modificar muchas otras, mayor es el acoplamiento.

## Relaciones

- Se analiza en la: [[Programación modular|Programación modular]].
- Se busca bajo sin sacrificar alta: [[Cohesión|Cohesión]].
- Las interfaces y la inyección de dependencias pueden reducirlo.

## Procedencia

- Clase: [[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas y técnicas de programación]].
- Fuente: diapositivas 13–14.

## Para completar

- [ ] Clasificar ejemplos de acoplamiento por datos, control y contenido.

