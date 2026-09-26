---
tipo: clase
materia: "[[01_Materias/Algoritmos/Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: 2026-08-11
unidad: Introducción al análisis y diseño de algoritmos
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[03_Conceptos/Algoritmo|Algoritmo]]"
  - "[[03_Conceptos/Terminación de un algoritmo|Terminación de un algoritmo]]"
  - "[[03_Conceptos/Validez de un algoritmo|Validez de un algoritmo]]"
  - "[[03_Conceptos/Complejidad temporal|Complejidad temporal]]"
  - "[[03_Conceptos/Complejidad espacial|Complejidad espacial]]"
  - "[[03_Conceptos/Eficiencia algorítmica|Eficiencia algorítmica]]"
  - "[[03_Conceptos/Tiempo polinomial|Tiempo polinomial]]"
  - "[[03_Conceptos/Búsqueda lineal|Búsqueda lineal]]"
  - "[[03_Conceptos/Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]]"
  - "[[03_Conceptos/Algoritmo voraz|Algoritmo voraz]]"
  - "[[03_Conceptos/Divide y vencerás|Divide y vencerás]]"
  - "[[03_Conceptos/Programación dinámica|Programación dinámica]]"
  - "[[03_Conceptos/Algoritmo aleatorio|Algoritmo aleatorio]]"
  - "[[03_Conceptos/Satisfacibilidad de circuitos|Satisfacibilidad de circuitos]]"
  - "[[03_Conceptos/P versus NP|P versus NP]]"
  - "[[03_Conceptos/Máquina de Turing|Máquina de Turing]]"
  - "[[03_Conceptos/Problema de la parada|Problema de la parada]]"
referencias:
  - Presentación introductoria del curso, diapositivas 1–38
tags:
  - clase
  - algoritmos
---

## Pregunta central

¿Qué propiedades permiten entender si un algoritmo funciona, si es eficiente y cómo puede diseñarse una solución nueva?

## Apuntes rápidos

- Un [[03_Conceptos/Algoritmo|algoritmo]] es una secuencia finita y bien definida de instrucciones para solucionar un problema; se puede pensar como una receta especificada con precisión.
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

No es posible aprender todos los algoritmos, pero sí estudiar [[03_Conceptos/Paradigma de diseño de algoritmos|paradigmas de diseño]] reutilizables:

- [[03_Conceptos/Algoritmo voraz|Algoritmos voraces]].
- [[03_Conceptos/Divide y vencerás|Divide y vencerás]].
- [[03_Conceptos/Programación dinámica|Programación dinámica]].
- [[03_Conceptos/Algoritmo aleatorio|Algoritmos aleatorios]].

Estas técnicas funcionan como herramientas generales para resolver problemas en distintos ámbitos.

## Eficiencia y dificultad

En el curso se usará, a grandes rasgos, [[03_Conceptos/Tiempo polinomial|tiempo polinomial]] como criterio de [[03_Conceptos/Eficiencia algorítmica|eficiencia]]. La búsqueda en un arreglo es eficiente porque su tiempo es lineal.

### Ruta más corta por búsqueda exhaustiva

El algoritmo presentado enumera secuencias de ciudades, conserva las que forman un camino entre el origen y el destino y elige la de menor longitud. Aunque es correcto, puede examinar más de $n!$ caminos; por ejemplo, $30! \approx 2.65\times 10^{32}$. El problema sí admite algoritmos eficientes, de modo que la ineficiencia pertenece a ese enfoque concreto y no necesariamente al problema.

### Satisfacibilidad de circuitos

El procedimiento exhaustivo prueba hasta $2^n$ asignaciones de entrada y acepta cuando alguna hace verdadera la salida del circuito. Para $n=256$, el número de asignaciones es aproximadamente $1.16\times 10^{77}$. No se conoce un algoritmo de tiempo polinomial para este problema; esta dificultad conduce a la pregunta [[03_Conceptos/P versus NP|P = NP]].

## Límites de la computación

- Hay problemas para los que no existen soluciones eficientes en el modelo considerado; la presentación menciona ajedrez y Go como ejemplos de enorme dificultad.
- Hay problemas que no pueden resolverse algorítmicamente en general, como el [[03_Conceptos/Problema de la parada|problema de la parada]].
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

- [[03_Conceptos/Algoritmo|Algoritmo]]
- [[03_Conceptos/Terminación de un algoritmo|Terminación de un algoritmo]]
- [[03_Conceptos/Validez de un algoritmo|Validez de un algoritmo]]
- [[03_Conceptos/Complejidad temporal|Complejidad temporal]]
- [[03_Conceptos/Complejidad espacial|Complejidad espacial]]
- [[03_Conceptos/Eficiencia algorítmica|Eficiencia algorítmica]]
- [[03_Conceptos/Tiempo polinomial|Tiempo polinomial]]
- [[03_Conceptos/Búsqueda lineal|Búsqueda lineal]]
- [[03_Conceptos/Paradigma de diseño de algoritmos|Paradigma de diseño de algoritmos]]
- [[03_Conceptos/Algoritmo voraz|Algoritmo voraz]]
- [[03_Conceptos/Divide y vencerás|Divide y vencerás]]
- [[03_Conceptos/Programación dinámica|Programación dinámica]]
- [[03_Conceptos/Algoritmo aleatorio|Algoritmo aleatorio]]
- [[03_Conceptos/Satisfacibilidad de circuitos|Satisfacibilidad de circuitos]]
- [[03_Conceptos/P versus NP|P versus NP]]
- [[03_Conceptos/Máquina de Turing|Máquina de Turing]]
- [[03_Conceptos/Problema de la parada|Problema de la parada]]

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
