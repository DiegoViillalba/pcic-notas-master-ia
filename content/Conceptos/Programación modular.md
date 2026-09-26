---
tipo: concepto
aliases:
  - Modular programming
area: programación avanzada
materias:
  - "[[Indice|Programación Avanzada]]"
estado: semilla
fuentes:
  - "[[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas]]"
tags: [concepto, programacion-avanzada, diseño-modular]
---

# Programación modular

## Definición inicial

Técnica que divide un programa en unidades con nombre, responsabilidad e interfaz definidas, capaces de desarrollarse y probarse parcialmente por separado.

## Ejemplo mínimo

Un módulo `facturación` puede exponer `calcular_total()` sin revelar cómo almacena descuentos o impuestos.

## Criterios iniciales

- Responsabilidad identificable.
- Comunicación explícita mediante parámetros o interfaces.
- Pruebas aisladas.
- Detalles internos ocultos cuando no son necesarios fuera del módulo.

## Relaciones

- Busca alta: [[Cohesión|Cohesión]].
- Busca bajo: [[Acoplamiento|Acoplamiento]].

## Procedencia

- Clase: [[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas y técnicas de programación]].
- Fuente: diapositivas 9 y 12.

## Para completar

- [ ] Distinguir módulo, función, clase, paquete y componente.

