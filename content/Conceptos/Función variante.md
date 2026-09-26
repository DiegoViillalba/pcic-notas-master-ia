---
tipo: concepto
aliases:
  - Variante de ciclo
  - Loop variant
  - Función de cota
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[Guía paso a paso - Lógica de Hoare|Guía paso a paso — Lógica de Hoare]]"
tags: [concepto, programacion, logica-de-hoare, terminacion, ciclos]
---

# Función variante

## Definición

Una **función variante** es una expresión entera que, mientras la guarda de un ciclo sea verdadera, permanece no negativa y disminuye estrictamente en cada iteración. Se usa para demostrar terminación.

## Obligaciones

Si $I$ es el invariante, $B$ la guarda, $C$ el cuerpo y $E$ la variante:

1. **Cota inferior:** $I\land B\Rightarrow E\ge0$.
2. **Descenso:** si antes de una vuelta $E=n$, después se cumple $E<n$.

Una sucesión estrictamente decreciente de enteros no negativos no puede ser infinita; por eso el ciclo termina.

## Ejemplo mínimo

```text
i := 0
while i < n do i := i + 1
```

Puede usarse:

$$
E=n-i.
$$

- Bajo $i<n$, $n-i>0$.
- Después de `i := i+1`, la variante vale $n-i-1$.
- Disminuye exactamente en uno.

## No confundir con el invariante

| Objeto | Pregunta que responde |
|---|---|
| [[Invariante de ciclo|Invariante]] | ¿Qué propiedad sigue siendo cierta? |
| Variante | ¿Por qué no puede haber infinitas vueltas? |

Una propiedad puede conservarse eternamente en un ciclo infinito. Por eso el invariante prueba corrección parcial, pero no terminación por sí solo.

## Contraejemplo

Que una cantidad disminuya no basta si puede bajar sin límite. Sobre los enteros, `i := i-1` hace disminuir $i$, pero no demuestra que `while true` termine. Hace falta una cota inferior bien fundada.

## Relaciones

- Completa la prueba de: [[Corrección parcial y corrección total|corrección total]].
- Acompaña a: [[Invariante de ciclo|invariante de ciclo]].
- Produce VCs adicionales en: [[Condición de verificación|condiciones de verificación]].

## Procedencia

- Fuente: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 79–91.
- Ejemplo completo: [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|Ciclos: invariante, salida y variante]].

