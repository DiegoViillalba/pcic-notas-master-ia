---
tipo: concepto
aliases:
  - Halting problem
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: procesada
fuentes:
  - "[[2026-08-11 IA - Introduccion|Introducción a IA]]"
  - "[[2026-08-11 ADA - Introducción al curso|Introducción a algoritmos]]"
tags:
  - concepto
  - inteligencia-artificial
  - computabilidad
  - algoritmos
  - indecidibilidad
---

# Problema de la parada

## Definición

El **problema de la parada** pregunta si existe un algoritmo que, al recibir la descripción de cualquier programa y una entrada para ese programa, determine correctamente si la ejecución terminará o continuará para siempre.

La respuesta es negativa: no existe un procedimiento algorítmico general que resuelva correctamente todos los casos posibles. Por ello, el problema de la parada es **indecidible**.

## Intuición

Es posible analizar muchos programas concretos. Por ejemplo, resulta sencillo comprobar que un ciclo con un contador acotado termina o que un ciclo incondicional sin una instrucción de salida no lo hace.

La dificultad aparece al exigir un analizador **universal, automático y siempre correcto**. Un programa puede recibir a otro programa como dato, simularlo e incluso examinar lo que ocurriría cuando ese programa se ejecuta sobre su propia descripción. Esta autorreferencia permite construir un caso que contradice cualquier supuesto detector perfecto.

## Formulación

Sea $\langle M\rangle$ la codificación de una [[Máquina de Turing|máquina de Turing]] $M$ y sea $w$ una entrada. El lenguaje de la parada se define como

$$
\mathrm{HALT}=\{\langle M,w\rangle \mid M \text{ se detiene al ejecutarse con } w\}.
$$

Decidir $\mathrm{HALT}$ requeriría una máquina total $H$ que, para todo par $\langle M,w\rangle$, terminara y respondiera

$$
H(\langle M\rangle,w)=
\begin{cases}
1, & \text{si } M(w) \text{ se detiene},\\
0, & \text{si } M(w) \text{ no se detiene}.
\end{cases}
$$

El resultado de Turing implica que tal decisor no existe.

## Idea de la demostración

La demostración utiliza contradicción y diagonalización.

1. Se supone que existe el detector perfecto $H$ descrito anteriormente.
2. Utilizando $H$, se construye un programa $D$ que recibe la descripción de un programa $P$ y hace lo contrario de lo que $H$ predice para $P$ ejecutado sobre sí mismo:

```text
D(P):
    si H(P, P) afirma que P se detiene:
        ejecutar un ciclo infinito
    en otro caso:
        detenerse
```

3. Se ejecuta $D$ con su propia descripción, es decir, se evalúa $D(D)$.

Entonces aparecen únicamente dos posibilidades:

- Si $H(D,D)$ afirma que $D(D)$ se detiene, la definición de $D$ hace que entre en un ciclo infinito.
- Si $H(D,D)$ afirma que $D(D)$ no se detiene, la definición de $D$ hace que se detenga.

En ambos casos, $H$ se equivoca. Esto contradice la hipótesis de que era un detector universal y siempre correcto; por lo tanto, $H$ no puede existir.

La paradoja del mentiroso puede servir como analogía de la autorreferencia, pero la demostración formal depende de esta construcción diagonal.

## Ejemplo mínimo

Un analizador particular podría reconocer correctamente los siguientes casos:

```text
para i desde 1 hasta 10:
    imprimir(i)
```

Este programa termina porque el número de iteraciones está acotado. También puede reconocer que el siguiente programa no termina:

```text
mientras verdadero:
    continuar
```

El teorema no impide resolver estos ejemplos. Afirma que ningún analizador puede decidir correctamente la terminación de **todos** los programas y entradas posibles.

## Consecuencias y límites

- La indecidibilidad es distinta de la ineficiencia: no significa que el problema requiera demasiado tiempo, sino que no existe un algoritmo total que lo decida en general.
- El problema es reconocible: si un programa termina, puede simularse hasta observar su parada. Cuando no termina, esa simulación puede continuar indefinidamente sin certificar el resultado.
- Las herramientas de análisis estático pueden garantizar la terminación para ciertas clases de programas, usar aproximaciones conservadoras o responder “desconocido”; lo que no pueden hacer es ser completas y correctas para todos los programas.
- El resultado no afirma que sea imposible demostrar la terminación de un programa específico.

## Relaciones

- Se formula mediante: [[Máquina de Turing|Máquina de Turing]].
- Delimita qué problemas pueden resolverse mediante un: [[Algoritmo|Algoritmo]].
- Se diferencia de: [[P versus NP|P versus NP]], que pregunta por eficiencia entre problemas decidibles, no por la existencia de un algoritmo decisor.
- Se relaciona con: computabilidad, diagonalización, autorreferencia y el teorema de Rice.

## Procedencia

- Clase: [[2026-08-11 IA - Introduccion|Introducción a IA]].
- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción a algoritmos]].
- Fuente de clase: presentación introductoria de *Análisis y Diseño de Algoritmos*, diapositiva 20.
- Fuente primaria: Alan M. Turing, “On Computable Numbers, with an Application to the Entscheidungsproblem”, 1936.
