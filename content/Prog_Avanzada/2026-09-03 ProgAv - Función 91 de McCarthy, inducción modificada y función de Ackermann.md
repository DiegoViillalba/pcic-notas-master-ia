---
tipo: clase
materia: "[[Indice|Programación Avanzada]]"
fecha: 2026-09-03
unidad: Recursión doble, inducción modificada y función de Ackermann
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[Función 91 de McCarthy|Función 91 de McCarthy]]"
  - "[[Principio de inducción matemática modificado|Principio de inducción matemática modificado]]"
  - "[[Función de Ackermann|Función de Ackermann]]"
  - "[[Terna de Hoare|Terna de Hoare]]"
  - "[[Inducción matemática aplicada a ciclos|Inducción matemática aplicada a ciclos]]"
referencias:
  - "[[Programación Avanzada Notas 7.pdf|Programación Avanzada Notas 7]]"
  - "[[Programación funcion 91 McCarthy Visual Studio.pdf|Programación función 91 McCarthy en Visual Studio]]"
tags:
  - clase
  - programacion-avanzada
  - recursion
  - induccion
  - verificacion-formal
  - logica-de-hoare
---
![[Programación Avanzada Notas 7.pdf]]
![[Programación funcion 91 McCarthy Visual Studio.pdf]]

# Función 91 de McCarthy, inducción modificada y función de Ackermann

## Pregunta central

Hasta la clase anterior probamos ciclos: la inducción avanzaba **hacia adelante**, contando iteraciones desde 0. ¿Qué hacemos cuando la recursión no cuenta iteraciones de forma obvia, se llama **a sí misma dos veces** (`mc91(mc91(n+11))`) y, para valores pequeños, primero se **aleja** de la condición de paro antes de acercarse a ella? La función 91 de John McCarthy es el ejemplo clásico para responder esto, y la función de Ackermann lleva la misma idea al extremo.

## Mapa de la clase

~~~mermaid
flowchart LR
    F["Función 91 de McCarthy"] --> D["Definición por casos"]
    D --> T["Traza a mano: f(1), f(12), f(23)..."]
    T --> C["Implementación en C#"]
    C --> S["Simulador de pila de llamadas"]
    S --> IM["Inducción modificada (baja desde k=100)"]
    IM --> P["Demostración: f(x)=91 para x≤100"]
    P --> A["Función de Ackermann"]
    A --> A1["A(1,z)=z+2"]
    A1 --> A2["A(2,z)=2z+3"]
    A2 --> A3["A(3,z)=2^(z+3)-3"]
    A3 --> A4["A(4,z): torre de 2"]
    A --> H["Ternas de Hoare sobre A(x,y)"]
~~~

Trabajamos con dos funciones que se llaman a sí mismas más de una vez por rama (recursión doble) y que, por eso, no se prestan a la inducción "iteración por iteración" de la clase pasada. Ambas se demuestran con una variante del principio de inducción: en vez de subir desde un caso base pequeño, se **baja** desde un techo fijo `k`, apoyándose en que la hipótesis ya vale para todos los valores *mayores* que el que se está probando. *(Notas 7, láminas 118–138.)*

---

## 1. John McCarthy y el porqué del ejemplo

> [!info] John Patrick McCarthy (4 de septiembre de 1927 – 24 de octubre de 2011)
> Considerado uno de los padres de la Inteligencia Artificial: acuñó el término en la Conferencia de Dartmouth (1956), creó el lenguaje **Lisp** y recibió el **Premio Turing en 1971**.

McCarthy propuso en 1970 una función deliberadamente "incómoda" para la verificación de programas: su definición es trivial de escribir, pero su recursión no decrece de forma evidente, así que no es obvio que **termine** ni que siempre regrese el mismo número. Es el ejemplo de libro de texto para practicar inducción sobre funciones recursivas antes de enfrentar casos reales más complejos.

## 2. Definición de la función 91

$$
f(x)=
\begin{cases}
x-10 & \text{si } x>100\[4pt]
f\big(f(x+11)\big) & \text{si } x\le 100
\end{cases}
$$

**Objetivo de la clase:** demostrar que

$$
\boxed{f(x)=91\ \ \forall\ x\in\mathbb{Z},\ x\le100 \qquad\text{y}\qquad f(x)=x-10\ \ \forall\ x>100.}
$$

La segunda parte es inmediata: es literalmente la definición cuando `x > 100`. Toda la dificultad está en la primera.

### 2.1. Antes de la prueba formal: seguir la recursión a mano

Para \(x=1\), sustituyendo la definición una y otra vez (Notas 7, lámina 119–120):

~~~text
f(1)  = f( f(12) )
      = f( f( f(23) ) )
      = f( f( f( f(34) ) ) )
      = f( f( f( f( f(45) ) ) ) )
      = ...
      = f( f( f( f( f( f( f( f( f(89) ) ) ) ) ) ) ) )
      = ...  ?
~~~

Cada sustitución **suma 11** al argumento interno y **agrega un nivel** de anidamiento. Esto sigue así hasta que un argumento interno supera 100; solo entonces empieza a "colapsar" restando 10 en cada paso hacia afuera. No es obvio, con solo esta traza, que el resultado final sea siempre 91 — por eso hace falta una demostración, no una tabla de ejemplos.

> [!tip] Verlo en movimiento
> El simulador de la sección 4 reproduce exactamente esta expansión y colapso para cualquier `n` que elijas, mostrando la pila de llamadas creciendo y luego resolviéndose de adentro hacia afuera.

## 3. Implementación en C# (proyecto `Funcion91JohnMcCarthy`)

~~~csharp
public static int mc91( int n )
{
    if (n > 100)
    {
        return n - 10;
    }
    else
    {
        return mc91( mc91( n + 11 ) );
    }
}
~~~

Lectura línea por línea:

| Línea | Qué hace | Relación con la definición |
|---|---|---|
| `if (n > 100)` | separa el caso base del recursivo | `x > 100` |
| `return n - 10;` | caso base, sin más llamadas | `f(x) = x - 10` |
| `return mc91( mc91( n + 11 ) );` | **dos** llamadas anidadas: primero `mc91(n+11)`, y su resultado vuelve a pasar por `mc91` | `f(f(x+11))` |

> [!warning] Recursión doble, no simple
> A diferencia de un ciclo o de una recursión de cola (`return f(n-1)`), aquí el valor de retorno de la llamada interna **es el argumento** de la llamada externa. No se puede "desenrollar" en un ciclo `while` sencillo; hay que razonar sobre una pila de llamadas.

El código completo del proyecto agrega una lista (`myL`) y una función `PrintValues` para depurar visualmente la pila con `Console.Write`, pero esa parte está deshabilitada por comentarios en la versión final; el algoritmo esencial es el mostrado arriba.

### 3.1. Salida del programa (`Main`)

~~~csharp
static void Main( string[] args )
{
    for (int i = 1; i <= 120; i++)
    {
        Console.WriteLine( "McCarthy91 de " + i + " es " + Program.mc91(i) );
    }
    Console.ReadKey();
}
~~~

Al ejecutar el proyecto en Visual Studio se obtiene, entre otros:

~~~text
McCarthy91 de 1 es 91
McCarthy91 de 2 es 91
   ...
McCarthy91 de 100 es 91
McCarthy91 de 101 es 91
McCarthy91 de 102 es 92
McCarthy91 de 103 es 93
   ...
McCarthy91 de 120 es 110
~~~

La tabla confirma el patrón que vamos a demostrar: **91 exactamente hasta x = 101**, y a partir de **x = 102** la salida crece como `x − 10` (coincide con la definición porque en `x = 101`, `101 − 10 = 91` también).

## 4. Simulador interactivo de la pila de llamadas

<iframe src="funcion91-mccarthy-simulador.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Usa los valores sugeridos (`n=1`, `n=45`, `n=89`, `n=96`, `n=100`, `n=111`) o escribe cualquier entero entre 1 y 130. Observa:

- Con `n > 100` la pila tiene **una sola llamada**: entra y regresa de inmediato (caso base).
- Con `n ≤ 100` la pila **crece** (llamadas en color verde, sin resolver) hasta que algún argumento interno supera 100, y luego se **resuelve de adentro hacia afuera** (color ámbar), siempre terminando en 91.
- Entre más cerca esté `n` de 100, menos niveles de pila se necesitan; entre más lejos (como `n = 1`), más niveles — pero siempre termina.

## 5. El principio de inducción modificado

La inducción de la clase pasada demuestra \(P(n)\) para todo \(n\ge k\) subiendo desde un caso base pequeño. Aquí necesitamos lo contrario: demostrar \(P(x)\) para todo \(x\le k\), **bajando** desde un techo fijo. El principio se adapta así:

> [!important] Principio de inducción modificado
> Sea \(k\) un entero fijo (positivo, negativo o cero). Para demostrar que \(P(n)\) es verdadera para toda \(n\le k\), basta demostrar:
> 1. **Paso básico:** \(P(k)\) es verdadera.
> 2. **Paso inductivo:** para toda \(n<k\), si \(P(m)\) es verdadera para **todo** \(m\) tal que \(n<m\le k\) (hipótesis de inducción), entonces \(P(n)\) es verdadera.
>
> Entonces \(P(n)\) es verdadera para toda \(n\le k\).

Gráficamente, la hipótesis de inducción cubre todo el tramo entre el punto que se está probando y el techo \(k\), no solo el vecino inmediato:

~~~mermaid
flowchart LR
    subgraph tramo [" "]
    direction LR
    N["n"] -.-> M1["..."] -.-> K["k"]
    end
    N -->|"se quiere probar"| PN["P(n)"]
    M1 -.->|"hipótesis: ya vale para todo m con n < m ≤ k"| HYP["P(m)"]
~~~

Esta variante es exactamente lo que necesitamos: para probar `f(x) = 91` con `x` chica, la demostración usa que la propiedad **ya es válida para valores más grandes** que `x` (hasta el techo `k = 100`), porque `mc91` siempre llama con argumentos mayores (`x+11`, y luego un resultado que —se supone por hipótesis— es 91, mayor que `x`).

## 6. Demostración: `f(x) = 91` para todo entero `x ≤ 100`

Sea \(P(x)\): *"la función obtiene \(f(x)=91\ \forall\) entero \(x\le100\), y \(f(x)=x-10\) para \(x>100\)"*. Se aplica el principio de inducción modificado con techo \(k=100\).

### 6.1. Paso básico: \(x = 100\)

$$
f(100)=f\big(f(111)\big)=f(101)=91.
$$

(\(111>100\Rightarrow f(111)=111-10=101\); y \(101>100\Rightarrow f(101)=101-10=91\).) El caso base es cierto.

### 6.2. Hipótesis de inducción

Sea \(x<100\) arbitraria. Suponemos que la propiedad ya vale para **todo** \(m\) con \(x<m\le100\):

$$
\forall\, m,\ x<m\le100:\quad f(m)=91.
$$

### 6.3. Paso inductivo

Como \(x<100\), por definición \(f(x)=f\big(f(x+11)\big)\). Hay exactamente dos casos, según dónde caiga \(x+11\):

**Caso a) \(x+11>100\).**

$$
f(x)=f\big(f(x+11)\big)=f\big((x+11)-10\big)=f(x+1).
$$

Como \(x+1>x\) y \(x+1\le100\) (porque \(x<100\)), la hipótesis de inducción aplica directamente: \(f(x+1)=91\). Por lo tanto \(f(x)=91\).

**Caso b) \(x+11\le100\).**

$$
f(x)=f\big(f(x+11)\big)=f(91),
$$

porque \(x+11>x\) y \(x+11\le100\), así que la hipótesis da \(f(x+11)=91\). Falta evaluar \(f(91)\): como \(x+11\le100\Rightarrow x\le89<91\), tenemos \(91>x\) y \(91\le100\), de modo que la **misma** hipótesis de inducción da \(f(91)=91\). Por lo tanto \(f(x)=91\).

En ambos casos \(f(x)=91\), lo que completa el paso inductivo.

$$
\boxed{\therefore\ f(x)=91\ \ \forall\ \text{entero } x\le100.}
$$

> [!note] Por qué hacía falta la hipótesis "para todo m mayor", y no solo "para x+1"
> El caso (b) necesita el valor de \(f\) en **dos** puntos distintos mayores que \(x\) (\(x+11\) y luego \(91\)), no solo en el sucesor inmediato. Por eso la inducción simple ("si vale en \(n\), vale en \(n+1\)") no alcanza aquí: se necesita la versión fuerte/modificada, que supone la propiedad en **todo** el tramo \((x,k]\).

## 7. Generalizando: la función de Ackermann

> [!info] Wilhelm Ackermann (29 de marzo de 1896 – 24 de diciembre de 1962)
> En 1928 construyó una función doblemente recursiva que crece muchísimo más rápido que cualquier función exponencial fija, usada históricamente para mostrar los límites de ciertas nociones de "función primitiva recursiva".

Definición habitual con dos variables:

$$
A(m,n)=
\begin{cases}
n+1 & \text{si } m=0\\
A(m-1,\,1) & \text{si } m>0 \text{ y } n=0\\
A\big(m-1,\,A(m,\,n-1)\big) & \text{si } m>0 \text{ y } n>0
\end{cases}
$$

o, de forma equivalente:

$$
\begin{aligned}
A(0,y)&=y+1 &&\text{(1)}\\
A(x+1,0)&=A(x,1) &&\text{(2)}\\
A(x+1,y+1)&=A\big(x,\,A(x+1,y)\big) &&\text{(3)}
\end{aligned}
$$

Igual que `mc91`, cada rama recursiva llama a `A` con argumentos que, en algún sentido, "avanzan hacia" un caso ya resuelto — aquí se demuestra con **inducción sobre dos variables**: primero sobre \(m\) (o \(x\)), y dentro de cada paso, una inducción anidada sobre \(n\) (o \(y\)).

### 7.1. `A(1, z) = z + 2` — inducción sobre `z`

**Base**, \(z=0\): \(A(1,0)=A(0,1)\) por (2) \(=1+1=2=0+2\).

**Hipótesis:** \(A(1,n)=n+2\).

**Paso:**
$$
A(1,n+1)\overset{(3)}{=}A\big(0,A(1,n)\big)\overset{\text{hip.}}{=}A(0,n+2)\overset{(1)}{=}(n+2)+1=(n+1)+2.
$$

$$\therefore\ A(1,z)=z+2.$$

### 7.2. `A(2, z) = 2z + 3` — inducción sobre `z`, usando el resultado anterior

**Base**, \(z=0\): \(A(2,0)=A(1,1)=1+2=3=2\cdot0+3\).

**Paso:**
$$
A(2,n+1)=A\big(1,A(2,n)\big)\overset{\text{hip.}}{=}A(1,2n+3)\overset{\S7.1}{=}(2n+3)+2=2(n+1)+3.
$$

$$\therefore\ A(2,z)=2z+3.$$

### 7.3. `A(3, z) = 2^(z+3) − 3`

**Base:** \(A(3,0)=A(2,1)=2\cdot1+3=5=2^{0+3}-3\).

**Paso:**
$$
A(3,n+1)=A\big(2,A(3,n)\big)=2\big(2^{n+3}-3\big)+3=2^{(n+1)+3}-3.
$$

### 7.4. `A(4, z)`: una torre de potencias de 2

$$
A(4,z)=\underbrace{2^{2^{\cdot^{\cdot^{2}}}}}_{z+2\text{ veces}}-3.
$$

Por ejemplo, \(A(4,1)=2^{2^{2}}-13=65533\) y \(A(4,2)=2^{65536}-3\), un número con **19 729 dígitos**. La tabla de las diapositivas resume el crecimiento:

| \(m\backslash n\) | 0 | 1 | 2 | 3 | fórmula |
|---:|---:|---:|---:|---:|---|
| 0 | 1 | 2 | 3 | 4 | \(n+1\) |
| 1 | 2 | 3 | 4 | 5 | \(n+2\) |
| 2 | 3 | 5 | 7 | 9 | \(2n+3\) |
| 3 | 5 | 13 | 29 | 61 | \(2^{n+3}-3\) |
| 4 | 13 | 65533 | \(2^{65536}-3\) | … | torre de 2 |

> [!warning] Por qué el proyecto `Ackermann` truena con `StackOverflowException`
> Cada llamada recursiva de `A(m, n)` con `m ≥ 3` y `n` moderada abre una cantidad astronómica de llamadas anidadas antes de tocar un caso base. Según el análisis de las diapositivas, `A(4,2)` ya supera "el número de partículas del universo elevado a la potencia 200", y `A(5,2)` ni siquiera cabría representarse en el universo físico. Ningún lenguaje con pila de tamaño finito puede evaluarlo por recursión directa.

### 7.5. Otra propiedad, con inducción sobre **dos** variables a la vez

$$
\forall\, x,y\in\mathbb{N}_0:\quad y+1\le A(x,y).
$$

Se demuestra por inducción sobre \(x\) (paso base \(x=0\)), y **dentro** del paso inductivo sobre \(x\), se hace una segunda inducción sobre \(y\). Esta anidación —una inducción dentro de otra— es la misma herramienta que usamos para `mc91`, llevada a dos variables en vez de una.

## 8. Ternas de Hoare sobre la función de Ackermann

Con los resultados ya demostrados (§7.1 y §7.2) podemos verificar programas que *usan* `A` como si fuera una función de biblioteca, sin volver a probarla:

$$
\{x=1\}\ \ w:=A(x,y)\ \ \{w=y+2\}
\qquad\qquad
\{x=2\}\ \ w:=A(x,y)\ \ \{w=2y+3\}
$$

Usando el axioma de asignación hacia atrás, \(Q[w/A(x,y)]=\{A(x,y)=y+2\}\); esa terna es válida por el axioma de asignación. Como ya se demostró que \(x=1\Rightarrow A(x,y)=y+2\), la regla de consecuencia cierra la prueba:

$$
\frac{\{A(x,y)=y+2\}\ w:=A(x,y)\ \{w=y+2\} \qquad x=1\Rightarrow A(x,y)=y+2}{\{x=1\}\ w:=A(x,y)\ \{w=y+2\}}.
$$

El mismo patrón, sustituyendo \(y+2\) por \(2y+3\) y usando §7.2, prueba la segunda terna.

> [!note] Complemento de `AllLectures`: evaluar la expresión también debe terminar
> El axioma de asignación para **corrección total** supone que evaluar el lado derecho termina. En `w := A(x,y)`, demostrar solo el valor matemático de \(A(x,y)\) no basta si todavía no se ha justificado que la llamada recursiva termina para las entradas permitidas. Conviene separar: **(1)** el lema que calcula el resultado, **(2)** el argumento bien fundado de terminación y **(3)** la regla de consecuencia. Véase [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|invariante y variante]] para el análogo iterativo.

> [!tip] La utilidad de haber demostrado A(1,z) y A(2,z) por separado
> Una vez fijado un teorema (`A(1,z) = z+2`), se vuelve una pieza reutilizable: en la verificación de un programa ya no hay que "desenrollar" la recursión de Ackermann, solo aplicar el teorema y la regla de consecuencia — exactamente igual que usar un lema ya probado en una demostración matemática más grande.

---

## 9. Comparación: inducción "hacia adelante" vs. modificada

| | Ciclos (clase anterior) | `mc91` y Ackermann (esta clase) |
|---|---|---|
| Dirección | Sube desde \(k\) (p. ej. \(n=0\)) | Baja desde un techo \(k\) fijo |
| Qué crece | El número de iteraciones ya hechas | — el argumento puede subir *temporalmente* antes de resolverse |
| Hipótesis | \(P(n)\) para un \(n\) fijo anterior | \(P(m)\)\ para **todo** \(m\) entre \(x\) y el techo \(k\) |
| Qué demuestra | Un invariante se conserva | Una llamada recursiva siempre termina en el mismo valor |
| Ejemplo | `C = D·A` en `Cuadrado(A)` | `f(x) = 91` en `mc91` |

---

## 10. Errores frecuentes

> [!warning] Confundir "recursión que se aleja del caso base" con "recursión que no termina"
> `mc91(1)` primero sube hasta argumentos como 89, 100, 111... antes de bajar. Verla crecer no significa que diverja; hay que demostrar que el crecimiento está acotado (aquí, por el `+11` contra el `>100`).

> [!warning] Usar inducción simple donde hace falta la modificada/fuerte
> El caso (b) de la demostración necesita el valor de \(f\) en dos puntos distintos mayores que \(x\) (no solo en \(x+1\)). Una hipótesis "solo vale para el siguiente" no alcanza.

> [!warning] Olvidar que la hipótesis de inducción tiene un rango, no un solo punto
> En la inducción modificada, la hipótesis cubre "todo \(m\) con \(x<m\le k\)", no un único valor. Aplicarla correctamente significa verificar, en cada uso, que el valor que se sustituye cae dentro de ese rango.

> [!warning] Tratar `A(m,n)` como si tuviera un solo caso base
> Tiene tres cláusulas (\(m=0\); \(m>0,n=0\); \(m>0,n>0\)), y demostrar una propiedad general requiere inducción **anidada**: sobre \(m\) primero, y sobre \(n\) dentro de cada paso.

---

## 11. Plantilla reutilizable: demostrar una función recursiva con inducción modificada

~~~text
1. Escribir P(x): la propiedad que se quiere probar sobre f(x).
2. Elegir el techo k a partir del cual el caso base de f es directo.
3. Paso básico: demostrar P(k) evaluando f(k) directamente con la definición.
4. Hipótesis de inducción: suponer P(m) para todo m con x < m ≤ k.
5. Paso inductivo: tomar x < k arbitraria, expandir f(x) con la definición,
   y separar en tantos casos como sea necesario según dónde caigan
   los argumentos intermedios.
6. En cada caso, verificar que los argumentos usados en la hipótesis
   están realmente en el rango (x, k] antes de aplicarla.
7. Concluir P(x) en cada caso; por inducción, P(x) vale para todo x ≤ k.
~~~

---

## 12. Ejercicios de comprobación

1. Usa el simulador con `n = 45` y cuenta cuántos niveles alcanza la pila antes de empezar a resolverse.
2. En el paso inductivo de `mc91`, ¿por qué el caso (b) necesita evaluar `f(91)` y no otro número?
3. Calcula a mano `A(2, 3)` usando la fórmula `A(2,z) = 2z+3` y verifica sustituyendo en la definición original `A(x+1,y+1) = A(x, A(x+1,y))`.
4. ¿Por qué la terna `{x=1} w:=A(x,y) {w=y+2}` no podría demostrarse solo con el axioma de asignación, sin la regla de consecuencia?
5. ¿Qué diferencia hay entre la hipótesis de inducción usada la clase pasada (ciclos) y la usada hoy (funciones recursivas)?

> [!check]- Respuestas breves
> 1. Para `n=45`: `45+11=56`, y así sucesivamente sumando 11 hasta superar 100 (56, 67, 78, 89, 100, 111); son 6 niveles de expansión antes de que aparezca el primer valor mayor que 100.
> 2. Porque en ese caso `x+11 ≤ 100`, y por la definición `f(x) = f(f(x+11))`; por hipótesis `f(x+11)=91`, así que el argumento externo que falta evaluar es exactamente `f(91)`.
> 3. Por la fórmula, `A(2,3) = 2·3+3 = 9`. Verificación con la definición original: `A(2,3) = A(1+1, 2+1) = A(1, A(2,2))`. Primero `A(2,2) = 2·2+3 = 7`; luego `A(1,7) = 7+2 = 9` (usando `A(1,z)=z+2`). Coincide: `9 = 9`. ✓
> 4. Porque el axioma de asignación solo produce `{A(x,y)=y+2} w:=A(x,y) {w=y+2}`; para llegar a la precondición deseada `{x=1}` hace falta el teorema `x=1 ⇒ A(x,y)=y+2`, demostrado aparte, y combinarlo exige la regla de consecuencia.
> 5. La de ciclos avanza contando iteraciones ya ejecutadas (hacia adelante, desde 0). La de hoy baja desde un techo fijo y su hipótesis cubre un rango completo de valores mayores, no solo el "siguiente" inmediato.

---

## 13. Referencia diapositiva por diapositiva

| Fuente | Diap. | Lámina | Contenido | Sección |
|---|---:|---:|---|---|
| Notas 7 | 1 | 118 | Definición de la función 91 y semblanza de McCarthy | §1–2 |
| Notas 7 | 2–3 | 119–120 | Traza a mano de `f(1)` y planteamiento por inducción | §2.1 |
| Notas 7 | 4 | 121 | Principio de inducción modificado | §5 |
| Notas 7 | 5–9 | 122–125 | Demostración completa de `f(x)=91` | §6 |
| Notas 7 | 10–11 | 126–127 | Introducción a la función de Ackermann | §7 |
| Notas 7 | 12–19 | 128–133 | `A(1,z)…A(4,z)` y tabla de crecimiento | §7.1–7.4 |
| Notas 7 | 20–21 | 134–135 | Ternas de Hoare sobre `A(x,y)` | §8 |
| Notas 7 | 22–24 | 136–138 | Inducción sobre dos variables: `y+1 ≤ A(x,y)` | §7.5 |
| VS McCarthy | 1–18 | — | Proyecto `Funcion91JohnMcCarthy`: creación, código y ejecución en Visual Studio | §3 |

## Conceptos atómicos

- [[Función 91 de McCarthy|Función 91 de McCarthy]]
- [[Principio de inducción matemática modificado|Principio de inducción matemática modificado]]
- [[Función de Ackermann|Función de Ackermann]]

## Dudas para revisar

- [ ] ¿Cómo se formaliza en general la equivalencia entre "inducción fuerte" e "inducción modificada hacia abajo"?
- [ ] ¿Qué variante (cantidad que decrece) justificaría formalmente la terminación de `mc91`, más allá del argumento informal de la demostración?
- [ ] ¿Existe una versión no recursiva (iterativa) de `mc91` que el curso vaya a pedir programar?

## Resumen después de clase

La función 91 de McCarthy y la función de Ackermann comparten un mismo reto: se llaman a sí mismas más de una vez por rama, y sus argumentos pueden crecer antes de resolverse, así que la inducción "hacia adelante" de los ciclos no aplica directamente. El **principio de inducción modificado** resuelve esto probando primero un caso base en un techo fijo `k` y luego bajando: la hipótesis de inducción para un valor `x` supone la propiedad ya demostrada para *todo* valor mayor hasta `k`, no solo para el siguiente. Con esa herramienta se demuestra que `mc91(x) = 91` para todo `x ≤ 100` separando dos casos según dónde caiga `x+11`, y se construyen en cascada los resultados cerrados de Ackermann (`A(1,z)=z+2`, `A(2,z)=2z+3`, `A(3,z)=2^(z+3)-3`, `A(4,z)` como torre de potencias), cada uno apoyado en el anterior. Los resultados ya probados se reutilizan como lemas dentro de ternas de Hoare, evitando repetir la inducción cada vez que la función aparece dentro de un programa.

## Referencia

- [[Programación Avanzada Notas 7.pdf|Programación Avanzada Notas 7]], diapositivas 1–24 (láminas 118–138).
- [[Programación funcion 91 McCarthy Visual Studio.pdf|Programación función 91 McCarthy en Visual Studio]], proyecto `Funcion91JohnMcCarthy`.
- Código fuente: `Funcion91JohnMcCarthy/Program.cs` (proyecto de Visual Studio adjunto).
- `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 79–91 (corrección total y terminación de evaluaciones).
- McCarthy, J. (1970). *The 91-function*, ejemplo clásico de verificación de programas recursivos.
- Ackermann, W. (1928). Función doblemente recursiva usada como ejemplo canónico de crecimiento no primitivo-recursivo.
