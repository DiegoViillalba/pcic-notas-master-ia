---
tipo: concepto
aliases:
  - Classification of mathematical models
area: modelación matemática
materias:
  - "[[Indice|Modelación Matemática]]"
estado: procesada
fuentes:
  - "[[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]]"
tags: [concepto, modelacion-matematica]
---

# Clasificación de modelos matemáticos

## Idea central

Las clasificaciones describen dimensiones distintas de un modelo. **Determinista o estocástico** indica cómo se representa la incertidumbre; **continuo o discreto** indica cómo cambia el tiempo o el estado. Por eso un modelo puede pertenecer a una categoría de cada dimensión.

## Determinista y estocástico

| Tipo | Definición | Ejemplo |
|---|---|---|
| Determinista | Las mismas condiciones y parámetros producen la misma salida. | Enfriamiento con temperatura ambiente y coeficiente fijos. |
| Estocástico | Incluye variables aleatorias; una misma entrada puede producir realizaciones distintas. | Llegadas de vehículos por minuto con distribución de Poisson. |

## Continuo y discreto

| Tipo | Definición | Formulación frecuente | Ejemplo |
|---|---|---|---|
| Continuo | La variable puede cambiar en cualquier instante o tomar valores en un continuo. | Ecuación diferencial | $dP/dt=rP$ |
| Discreto | La variable se actualiza por pasos o toma valores separados. | Ecuación en diferencias | $P_{n+1}=1.05P_n$ |

Siempre conviene precisar **qué** es continuo o discreto: el tiempo, el estado o ambos.

## Clasificación cruzada

|  | Determinista | Estocástico |
|---|---|---|
| Continuo | Temperatura descrita por una ecuación diferencial | Trayectoria continua afectada por ruido aleatorio |
| Discreto | Población actualizada por generaciones | Cola con llegadas aleatorias por minuto |

## Utilidad y límites

La clasificación orienta el método de análisis y el costo de cómputo: un modelo estocástico suele requerir muchas realizaciones y análisis estadístico; uno continuo puede necesitar discretización numérica. Estas etiquetas no indican por sí mismas que un modelo sea mejor ni más realista.

## Relaciones

- Clasifica un [[Modelo matemático|modelo matemático]].
- Un modelo continuo puede aproximarse mediante el [[Método de Euler|método de Euler]].
- Muchas realizaciones forman un [[Experimento computacional|experimento computacional]].

## Procedencia

- Clase: [[2026-08-12 ModMat - Definicion-de-problemas|Definición de problemas]].
