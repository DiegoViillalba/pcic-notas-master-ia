---
tipo: concepto
aliases:
  - Condición de verificación
  - Verification condition
  - VC
area: programacion
materias:
  - "[[Indice|Programación Avanzada]]"
estado: procesada
fuentes:
  - "[[Guía paso a paso - Lógica de Hoare|Guía paso a paso — Lógica de Hoare]]"
tags: [concepto, programacion, logica-de-hoare, verificacion-formal]
---

# Condición de verificación

## Definición

Una **condición de verificación** (VC) es una fórmula lógica cuya validez basta para justificar un paso de la prueba de un programa anotado. El generador de VCs elimina los comandos y deja obligaciones de lógica o aritmética.

## Proceso

1. Una persona anota el programa con condiciones intermedias e invariantes.
2. Un generador produce VCs mecánicamente.
3. Un demostrador automático o una persona prueba cada VC.

Para una asignación:

$$
\{P\}\ V:=E\ \{Q\}
$$

genera:

$$
P\Rightarrow Q[E/V].
$$

Para un ciclo anotado:

```text
{P} while B do {I} C {Q}
```

genera al menos:

$$
P\Rightarrow I,
$$

$$
I\land\neg B\Rightarrow Q,
$$

y las VCs de:

$$
\{I\land B\}\ C\ \{I\}.
$$

## Ejemplo mínimo

Para

$$
\{x=0\}\ x:=x+1\ \{x=1\},
$$

la VC es:

$$
x=0\Rightarrow x+1=1,
$$

que es válida.

## Límites

El generador puede ser mecánico, pero elegir un invariante útil normalmente requiere entender el algoritmo. Si las anotaciones son demasiado débiles, las VCs no permiten llegar a la postcondición; si son incorrectas, alguna VC falla.

## Relaciones

- Formaliza pruebas de: [[Terna de Hoare|ternas de Hoare]].
- Usa: [[Axioma de asignación de Hoare|sustitución]], [[Regla condicional de Hoare|ramas]] e [[Invariante de ciclo|invariantes]].
- Para corrección total agrega una: [[Función variante|función variante]].

## Procedencia

- Fuente: `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 47–69.
- Desarrollo guiado: [[Guía paso a paso - Lógica de Hoare#6. De programa anotado a condiciones de verificación|De programa anotado a condiciones de verificación]].

