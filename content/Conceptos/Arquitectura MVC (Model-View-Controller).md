---
tipo: concepto
aliases:
  - MVC
  - Modelo Vista Controlador
area: programación avanzada
materias:
  - "[[Indice|Programación Avanzada]]"
estado: semilla
fuentes:
  - "[[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas]]"
tags: [concepto, programacion-avanzada, arquitectura, web]
---

# Arquitectura MVC (Model-View-Controller)

## Definición inicial

Patrón arquitectónico que separa la presentación, la lógica o datos del dominio y la coordinación de solicitudes.

## Componentes

- **Modelo:** estado y reglas del dominio.
- **Vista:** representación mostrada al usuario.
- **Controlador:** recibe eventos o solicitudes y coordina la respuesta.

## Ejemplo mínimo

En una aplicación web, un servlet recibe la solicitud, consulta servicios o JavaBeans y selecciona una JSP para presentar el resultado.

## Límite

MVC no determina por sí solo cómo organizar servicios, DTO, acceso a datos ni persistencia. Esas capas pertenecen a decisiones arquitectónicas adicionales.

## Relaciones

- Es un: [[Patrón de diseño|Patrón de sistema o arquitectura]].
- Organiza una: [[Arquitectura de software|Arquitectura de software]].

## Procedencia

- Clase: [[2026-08-13 ProgAv - Definiciones básicas y técnicas de programación|Definiciones básicas y técnicas de programación]].
- Fuente: diapositivas 18–20.

## Para completar

- [ ] Seguir una solicitud completa en el ejemplo de Eclipse.
- [ ] Comparar MVC clásico, MVC web y arquitectura por capas.

