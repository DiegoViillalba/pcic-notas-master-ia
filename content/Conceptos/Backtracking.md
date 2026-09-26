---
tipo: concepto
aliases:
  - Vuelta atrás
  - Retroceso
area: algoritmos
materias:
  - "[[Indice|Programación Avanzada]]"
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Clase del 18 de agosto]]"
  - "[[2026-08-20 ProgAv - Ocho reinas y cuadros mágicos|Clase del 20 de agosto]]"
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
tags: [concepto, algoritmos, busqueda, recursion]
---

# Backtracking

## Definición

Técnica de búsqueda que construye soluciones parciales, extiende únicamente las que todavía pueden conducir a una solución y deshace la última decisión cuando una rama resulta inviable.

## Intuición

El espacio de candidatos forma un árbol. Se recorre normalmente en profundidad: elegir equivale a bajar un nivel; detectar una incompatibilidad permite podar el subárbol; deshacer la elección permite visitar la siguiente rama.

## Formulación

```text
backtrack(estado):
    si estado es solución: registrar(estado)
    para cada opción aplicable:
        aplicar(opción)
        si estado es prometedor: backtrack(estado)
        deshacer(opción)
```

Sin poda efectiva, un árbol con factor de ramificación $b$ y profundidad $d$ puede requerir $O(b^d)$ exploraciones.

## Ejemplo mínimo

Para ubicar reinas sin ataques, se coloca una reina por fila. Si una columna o diagonal ya está ocupada, esa opción se descarta. Cuando una fila no admite ninguna posición, se retira la reina anterior y se prueba otra columna.

## Contraejemplo o límites

No todo recorrido exhaustivo es backtracking: debe haber una solución parcial que pueda extenderse y una prueba que permita rechazar extensiones. En espacios grandes y con poca poda puede ser impráctico.

## Relaciones

- Se utiliza en: problemas de satisfacción de restricciones, permutaciones y rompecabezas.
- Ejemplos: [[Problema de las ocho reinas|ocho reinas]] y enumeración de [[Cuadro mágico|cuadros mágicos]].
- Su eficiencia depende de la [[Poda del espacio de búsqueda|poda del espacio de búsqueda]].
- En un CSP puede combinarse con [[Forward checking|forward checking]], [[Heurística MRV|MRV]] y [[Valor menos restrictivo|LCV]].
- Contrasta con: [[Divide y vencerás|divide y vencerás]], que combina subsoluciones en vez de abandonar alternativas.
- Requiere conocer: recursión y búsqueda en profundidad.
- Se especializa para optimización mediante cotas en *branch and bound*.

## Procedencia

- Clase: [[2026-08-18 ProgAv - Divide y vencerás, QuickSort y backtracking|Divide y vencerás, QuickSort y backtracking]].
- Fuente: *Programación Avanzada Notas 2*, diapositivas 33-39; *Algoritmo BackTracking y Divide-Venceras*, páginas 1-2.
