---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: 2026-08-11
unidad: Introducción al análisis y diseño de algoritmos
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[Algoritmo|Algoritmo]]"
  - "[[Terminación de un algoritmo|Terminación de un algoritmo]]"
  - "[[Validez de un algoritmo|Validez de un algoritmo]]"
  - "[[Complejidad temporal|Complejidad temporal]]"
  - "[[Complejidad espacial|Complejidad espacial]]"
  - "[[Eficiencia algorítmica|Eficiencia algorítmica]]"
  - "[[Tiempo polinomial|Tiempo polinomial]]"
  - "[[Búsqueda lineal|Búsqueda lineal]]"
  - "[[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]]"
  - "[[Algoritmo voraz|Algoritmo voraz]]"
  - "[[Divide y vencerás|Divide y vencerás]]"
  - "[[Programación dinámica|Programación dinámica]]"
  - "[[Algoritmo aleatorio|Algoritmo aleatorio]]"
  - "[[Satisfacibilidad de circuitos|Satisfacibilidad de circuitos]]"
  - "[[P versus NP|P versus NP]]"
  - "[[Máquina de Turing|Máquina de Turing]]"
  - "[[Problema de la parada|Problema de la parada]]"
referencias:
  - Presentación introductoria del curso, diapositivas 1–38
tags:
  - clase
  - algoritmos
---

## Pregunta central

¿Qué propiedades permiten entender si un algoritmo funciona, si es eficiente y cómo puede diseñarse una solución nueva?

## Apuntes rápidos

- Un [[Algoritmo|algoritmo]] es una secuencia finita y bien definida de instrucciones para solucionar un problema; se puede pensar como una receta especificada con precisión.
- La algoritmia es un pilar de la computación y tiene aplicaciones en muchas áreas del conocimiento.
- El objetivo del curso no es memorizar todos los algoritmos, sino aprender técnicas generales para analizarlos y diseñarlos.
- Que un algoritmo produzca la respuesta correcta no garantiza que sea útil: también importa la cantidad de tiempo y memoria que requiere.

## Análisis de algoritmos

El análisis busca justificar cuatro propiedades principales:

| Propiedad                       | Pregunta                                       |
| ------------------------------- | ---------------------------------------------- |
| [[Terminación de un algoritmo]] | ¿Finaliza para cualquier entrada?              |
| [[Validez de un algoritmo]]     | ¿Calcula la salida correcta para toda entrada? |
| [[Complejidad temporal]]        | ¿Cuánto tiempo requiere al crecer la entrada?  |
| [[Complejidad espacial]]        | ¿Cuánta memoria de trabajo utiliza?            |

Estas técnicas deben poder aplicarse a cualquier tipo de algoritmo.

### Ejemplo: búsqueda en un arreglo

```text
Busca(A, n, x):
    para c = 1 hasta n:
        si A[c] = x:
            devolver c
    devolver NULL
```

- Termina porque el ciclo ejecuta como máximo $n$ iteraciones.
- Es válido porque revisa cada posición: devuelve una posición que contiene $x$ o `NULL` si $x$ no aparece.
- Ejecuta a lo más $dn$ instrucciones para alguna constante entera $d$; por ello tiene tiempo lineal, $O(n)$.
- Solo conserva el contador $c$ además de la entrada; usa espacio de trabajo constante, $O(1)$.

## Diseño de algoritmos

No es posible aprender todos los algoritmos, pero sí estudiar [[Paradigma de diseño de algoritmos|paradigmas de diseño]] reutilizables:

- [[Algoritmo voraz|Algoritmos voraces]].
- [[Divide y vencerás|Divide y vencerás]].
- [[Programación dinámica|Programación dinámica]].
- [[Algoritmo aleatorio|Algoritmos aleatorios]].

Estas técnicas funcionan como herramientas generales para resolver problemas en distintos ámbitos.

## Eficiencia y dificultad

En el curso se usará, a grandes rasgos, [[Tiempo polinomial|tiempo polinomial]] como criterio de [[Eficiencia algorítmica|eficiencia]]. La búsqueda en un arreglo es eficiente porque su tiempo es lineal.

### Ruta más corta por búsqueda exhaustiva

El algoritmo presentado enumera secuencias de ciudades, conserva las que forman un camino entre el origen y el destino y elige la de menor longitud. Aunque es correcto, puede examinar más de $n!$ caminos; por ejemplo, $30! \approx 2.65\times 10^{32}$. El problema sí admite algoritmos eficientes, de modo que la ineficiencia pertenece a ese enfoque concreto y no necesariamente al problema.

### Satisfacibilidad de circuitos

El procedimiento exhaustivo prueba hasta $2^n$ asignaciones de entrada y acepta cuando alguna hace verdadera la salida del circuito. Para $n=256$, el número de asignaciones es aproximadamente $1.16\times 10^{77}$. No se conoce un algoritmo de tiempo polinomial para este problema; esta dificultad conduce a la pregunta [[P versus NP|P = NP]].

## Límites de la computación

- Hay problemas para los que no existen soluciones eficientes en el modelo considerado; la presentación menciona ajedrez y Go como ejemplos de enorme dificultad.
- Hay problemas que no pueden resolverse algorítmicamente en general, como el [[Problema de la parada|problema de la parada]].
- Ante estas limitaciones puede ser necesario aceptar soluciones aproximadas, parciales o probabilísticas.

## Aclaraciones después de clase

- [x] **Tiempo polinomial.** Un algoritmo corre en tiempo polinomial si existen constantes $c>0$, $k\geq0$ y $n_0$ tales que, para toda entrada de tamaño $n\geq n_0$,

  $$
  T(n)\leq cn^k.
  $$

  En notación asintótica, esto equivale a escribir $T(n)=O(n^k)$ para alguna constante $k$. La presentación usa este criterio “a grandes rasgos” para distinguir algoritmos eficientes.

- [x] **Terminación, validez y corrección.** La presentación separa las preguntas “¿termina con cualquier entrada?” y “¿calcula la salida correcta para toda entrada?”. En terminología estándar, la **corrección parcial** garantiza que, si el algoritmo termina, su respuesta es correcta; la **corrección total** combina corrección parcial y terminación. En las diapositivas del curso, `validez` se utiliza para la propiedad de producir la salida correcta y se analiza junto con la terminación.

- [x] **Referencias.** La diapositiva 36 identifica como material principal *Algorithm Design*, de Kleinberg y Tardos, junto con sus diapositivas de Princeton. Los demás títulos ya registrados se conservan como referencias complementarias; la presentación no muestra otro título adicional legible.

- [x] **Política de uso de IA.** La diapositiva 38 la presenta como una política “anti-déficit cognitivo”: el promedio aprobatorio de los exámenes es requisito para aprobar el curso. Esto permite utilizar herramientas de IA, pero impide que sustituyan el dominio individual evaluado en los exámenes.

## Conceptos para extraer

- [[Algoritmo|Algoritmo]]
- [[Terminación de un algoritmo|Terminación de un algoritmo]]
- [[Validez de un algoritmo|Validez de un algoritmo]]
- [[Complejidad temporal|Complejidad temporal]]
- [[Complejidad espacial|Complejidad espacial]]
- [[Eficiencia algorítmica|Eficiencia algorítmica]]
- [[Tiempo polinomial|Tiempo polinomial]]
- [[Búsqueda lineal|Búsqueda lineal]]
- [[Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]]
- [[Algoritmo voraz|Algoritmo voraz]]
- [[Divide y vencerás|Divide y vencerás]]
- [[Programación dinámica|Programación dinámica]]
- [[Algoritmo aleatorio|Algoritmo aleatorio]]
- [[Satisfacibilidad de circuitos|Satisfacibilidad de circuitos]]
- [[P versus NP|P versus NP]]
- [[Máquina de Turing|Máquina de Turing]]
- [[Problema de la parada|Problema de la parada]]

## Referencias mencionadas

- Kleinberg, J. y Tardos, É., *Algorithm Design*.
- [Materiales de Kleinberg–Tardos de Princeton](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/).
- Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C., *Introduction to Algorithms*, 2.ª ed.
- Mitzenmacher, M. y Upfal, E., *Probability and Computing: Randomization and Probabilistic Techniques in Algorithms and Data Analysis*, 2.ª ed.
- Presentación introductoria de *Análisis y Diseño de Algoritmos 2027-I*, diapositivas 1–38.

## Resumen después de clase

Un algoritmo debe estudiarse tanto por su corrección como por los recursos que consume. La búsqueda lineal muestra cómo demostrar terminación y validez y cómo calcular complejidad temporal y espacial. Los paradigmas de diseño permiten crear soluciones sin memorizar algoritmos aislados. La comparación entre ruta más corta, satisfacibilidad y problemas no computables muestra que una solución correcta puede ser impráctica o incluso imposible de obtener algorítmicamente en general.

## Acciones adicionales

- [x] Resolver las dudas pendientes.
- [x] Contrastar las referencias y la política de IA con las diapositivas 36 y 38.
