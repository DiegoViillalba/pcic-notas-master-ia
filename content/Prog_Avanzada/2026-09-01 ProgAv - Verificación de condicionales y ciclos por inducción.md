---
tipo: clase
materia: "[[Indice|Programación Avanzada]]"
fecha: 2026-09-01
unidad: Verificación de condicionales y ciclos mediante inducción
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[Terna de Hoare|Terna de Hoare]]"
  - "[[Regla condicional de Hoare|Regla condicional de Hoare]]"
  - "[[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]]"
  - "[[Inducción matemática aplicada a ciclos|Inducción matemática aplicada a ciclos]]"
  - "[[Invariante de ciclo|Invariante de ciclo]]"
  - "[[Corrección parcial y corrección total|Corrección parcial y corrección total]]"
referencias:
  - "[[Programación Avanzada Notas 6.pdf|Programación Avanzada Notas 6]]"
tags:
  - clase
  - programacion-avanzada
  - verificacion-formal
  - logica-de-hoare
  - induccion
  - invariantes
  - ciclos
---
![[Programación Avanzada Notas 6.pdf]]

# Verificación de condicionales y ciclos por inducción

## Pregunta central

¿Cómo pasamos de demostrar que **cada rama** de un condicional es correcta a demostrar que una propiedad se conserva durante **cualquier número de iteraciones** de un ciclo?

## Mapa de la clase

~~~mermaid
flowchart LR
    H["Terna de Hoare"] --> IF["Separar B y no B"]
    IF --> R1["Probar rama verdadera"]
    IF --> R2["Probar rama falsa"]
    R1 --> Q["Postcondición común Q"]
    R2 --> Q
    Q --> W["Verificar ciclos while"]
    W --> IND["Inducción sobre el número de iteraciones"]
    IND --> INV["Invariante de ciclo"]
    INV --> EXIT["Invariante + condición de salida"]
    EXIT --> POST["Postcondición"]
    W --> VAR["Variante decreciente"]
    VAR --> TERM["Terminación"]
~~~

La primera parte completa la verificación de condicionales con **else**. La segunda introduce la [[Inducción matemática aplicada a ciclos|inducción matemática]] como herramienta para demostrar que una relación entre variables sigue siendo cierta después de $0,1,2,\ldots$ iteraciones. Esa relación persistente es el [[Invariante de ciclo|invariante del ciclo]]. *(Diap. 1–17; láminas 101–117.)*

---

## 1. Recordatorio: demostrar un **if** significa cubrir todos sus caminos

Para el programa:

~~~text
if B then C1 else C2
~~~

la regla condicional de Hoare es:

$$
\frac{
\{P\land B\}\ C_1\ \{Q\}
\qquad
\{P\land\neg B\}\ C_2\ \{Q\}
}
{\{P\}\ \mathbf{if}\ B\ \mathbf{then}\ C_1\ \mathbf{else}\ C_2\ \{Q\}}.
$$

La estructura de la prueba es sencilla:

1. En la rama verdadera sabemos $P\land B$.
2. En la rama falsa sabemos $P\land\neg B$.
3. Cada rama puede ejecutar instrucciones distintas.
4. Ambas deben terminar garantizando la misma postcondición $Q$.

> [!important]
> No basta con que el programa produzca el resultado esperado en algunos valores. La prueba debe cubrir todas las entradas admitidas por $P$ y los dos posibles resultados de evaluar $B$.

---

## 2. Ejemplo gradual: elegir el mayor de dos valores

Queremos demostrar:

$$
\boxed{
\{\top\}\
\mathbf{if}\ a>b\ \mathbf{then}\ m:=a\ \mathbf{else}\ m:=b
\ \{m\ge a\land m\ge b\}
}.
$$

Aquí:

$$
P=\top,
\qquad B:(a>b),
\qquad Q:(m\ge a\land m\ge b).
$$

### 2.1. Antes de las fórmulas: intuición con números

- Si $a=7$ y $b=3$, la condición es verdadera y se asigna $m:=7$.
- Si $a=2$ y $b=5$, la condición es falsa y se asigna $m:=5$.
- Si $a=b=4$, la condición $a>b$ es falsa y se asigna $m:=b=4$.

En los tres casos, $m$ no es menor que ninguno de los dos valores.

### 2.2. Rama verdadera: $a>b$

**P.D.** $\{a>b\}  \ m := a \ \{(m\geq a) \land (m\geq b)\}$

La asignación es $m:=a$. Calculamos hacia atrás desde $Q$, sustituyendo $m$ por $a$:

$$
Q^{m}_{a}
=
(a\ge a)\land(a\ge b).
$$

La primera parte, $a\ge a$, siempre es cierta. Además debilitando tenemos:

$$
a>b\Rightarrow a\ge b.
$$

Por la regla de consecuencia:

$$
\boxed{\{a>b\}\ m:=a\ \{m\ge a\land m\ge b\}}.
$$

### 2.3. Rama falsa: $\neg(a>b)$

En un orden total, negar $a>b$ equivale a afirmar $b\ge a$. La asignación es $m:=b$. Sustituyendo $m$ por $b$:

$$
Q^{m}_{b}
=
(b\ge a)\land(b\ge b).
$$

$b\ge b$ siempre es cierta y la condición de la rama ya proporciona $b\ge a$. Por tanto:

$$
\boxed{\{\neg(a>b)\}\ m:=b\ \{m\ge a\land m\ge b\}}.
$$

### 2.4. Unir las ramas

Las dos ramas establecen $Q$, así que la regla condicional permite concluir:

$$
\boxed{
\{\top\}\
\mathbf{if}\ a>b\ \mathbf{then}\ m:=a\ \mathbf{else}\ m:=b
\ \{m\ge a\land m\ge b\}
}.
$$

~~~mermaid
flowchart TD
    S["Cualquier par a, b"] --> C{"¿a es mayor que b?"}
    C -->|"Sí"| A["m := a"]
    C -->|"No"| B["m := b"]
    A --> QA["m = a y a es mayor que b"]
    B --> QB["m = b y b es mayor o igual que a"]
    QA --> Q["m es mayor o igual que a y b"]
    QB --> Q
~~~

---

## 3. Ejemplo con una rama imposible

Ahora la precondición ya afirma que $a>b$:

$$
\boxed{
\{a>b\}\
\mathbf{if}\ a>b\ \mathbf{then}\ m:=a\ \mathbf{else}\ m:=b
\ \{m=a\}
}.
$$

Notemos como en nuestro problema:
$$
P  : \{a>b\}\ \qquad B : \{a>b\}\ \qquad C: m:=a \qquad Q = \{m = a\}
$$
### Rama verdadera

Buscamos demostrar que:
$$
\{a >b\} \ m := a \ \{ m= a\}
$$
Mediante el esquema de demostración usado anteriormente tenemos:
$$
P = \{Q^V_E\} = \{(m = a)^{m}_a\} = \{a = a\} = \{\top\}
$$
Es decir, se cumple que:
$$
\therefore \{\top\} \ m := a \ \{m = a\}
$$
Convenientemente, notemos como la precondición de la rama es:

$$
\{(a>b)\land(a>b)\} = \{\top\}
$$

Así para nuestra definición 

$$
\{P\land B\}\ C_1\ \{Q\}
$$
La asignación $m:=a$ garantiza directamente $m=a$:

$$
\{a>b\}\ m:=a\ \{m=a\}.
$$

### Rama falsa

Buscamos demostrar que 
$$
\neg\{a >b\} \ m := b \ \{ m= a\}
$$

En esta ocasión se cumple que para la precondición

$$
P = \{Q^V_E\} = \{(m = a)^{m}_b\} = \{b = a\} 
$$

Lo que nos permite denotarlo como 

$$
\therefore \{b =a\} \ m := a \ \{m = a\}
$$
Para lo que podemos garantizar que: 

$$
\{\neg (b >a ) \land \neg(a > b)\} \implies \{b= a\}
$$

Para conseguir el argumento buscado, notemos que:

$$
a > b \implies a \geq b \equiv \neg (b>a)
$$
Es decir, debilitando la precondición anterior tenemos que se cumple:

$$
\{ (a >b ) \land \neg(a > b)\} \implies \{ (a \geq b ) \land \neg(a > b)\}
$$
Con lo cual conseguimos la forma buscada por nuestra definición.

Para darle sentido notemos como precondición de esta rama sería:

$$
(a>b)\land\neg(a>b)=\bot.
$$

No existe un estado que satisfaga simultáneamente ambas partes. La rama es **inalcanzable** para cualquier entrada permitida. Por ello, la terna de esa rama **es verdadera vacíamente**:

$$
\{\bot\}\ m:=b\ \{m=a\}.
$$

Así, el condicional completo garantiza $m=a$.

> [!note] Una contradicción no significa que el programa falló
> Significa que ese camino no puede ejecutarse desde la precondición dada. Esta idea simplifica muchas pruebas de programas.

---

## 4. Del condicional al ciclo

En un condicional hay un número finito de caminos y se prueba cada uno. En un ciclo, el cuerpo puede ejecutarse una cantidad no fijada de veces:

~~~text
0 veces, 1 vez, 2 veces, ..., n veces
~~~

No podemos escribir una prueba separada para cada $n$. Necesitamos una sola demostración que cubra todos los casos. Ahí aparece la inducción matemática.

### Microejemplo: un contador

~~~text
x := 0
while x < 3
    x := x + 1
~~~

Si $x_n$ es el valor después de $n$ iteraciones:

| $n$ | $x_n$ |
|---:|---:|
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

La tabla sugiere $x_n=n$. Pero observar cuatro filas no demuestra la fórmula. La inducción permite probarla para todo $n$ que alcance el ciclo.

---

## 5. Inducción matemática aplicada a un programa

Para demostrar una proposición $P(n)$ para todo $n\ge k$, se prueban dos piezas:

1. **Caso base:** $P(k)$ es verdadera.
2. **Paso inductivo:** para un $n\ge k$ arbitrario, suponemos $P(n)$ y demostramos $P(n+1)$.

Entonces se concluye:

$$
\forall n\ge k,\ P(n).
$$

En un ciclo que comienza contando en $0$, la correspondencia es:

| Inducción | Ejecución del ciclo |
|---|---|
| $P(0)$ | Estado antes de ejecutar el cuerpo por primera vez |
| Hipótesis $P(n)$ | Relación cierta después de $n$ iteraciones |
| Paso $P(n)\Rightarrow P(n+1)$ | Una ejecución del cuerpo conserva la relación |
| $P(n)$ para todo $n$ | La relación es un invariante |

~~~mermaid
flowchart LR
    B["Estado inicial: P(0)"] --> I1["Ejecutar una vez"]
    I1 --> P1["P(1)"]
    P1 --> I2["Ejecutar una vez"]
    I2 --> P2["P(2)"]
    P2 --> D["..."]
    D --> PN["P(n)"]
    PN --> STEP["El cuerpo preserva P"]
    STEP --> PN1["P(n+1)"]
~~~

> [!important]
> La hipótesis de inducción no afirma que $P(n)$ sea cierta “porque sí”. Se la supone temporalmente para un $n$ arbitrario y se usa para demostrar que el siguiente estado también satisface la propiedad.

---

## 6. Primer ciclo: calcular un cuadrado mediante sumas

La función de las diapositivas es:

~~~text
Cuadrado(A):
    C := 0
    D := 0
    while D != A
        C := C + A
        D := D + 1
    return C
~~~

Para corrección total supondremos $A\in\mathbb Z$ y $A\ge0$. $C$ es el acumulador y $D$ cuenta cuántas veces hemos sumado $A$.

### 6.1. Construir la conjetura con un caso pequeño

Sea $A=4$:

| Iteraciones $n$ | $C_n$ | $D_n$ | Comprobación |
|---:|---:|---:|---|
| 0 | 0 | 0 | $0=0\cdot4$ |
| 1 | 4 | 1 | $4=1\cdot4$ |
| 2 | 8 | 2 | $8=2\cdot4$ |
| 3 | 12 | 3 | $12=3\cdot4$ |
| 4 | 16 | 4 | $16=4\cdot4$ |

El patrón es:

$$
C_n=nA,
\qquad
D_n=n.
$$

Al eliminar $n$, obtenemos una relación directa entre las variables del programa:

$$
\boxed{I:\ C_n=D_nA}.
$$

Esta igualdad es el invariante.

### Explorador de los dos ciclos

<iframe src="invariantes-ciclos-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El explorador muestra el estado después de cada iteración. Los valores cambian, pero la igualdad resaltada se conserva. En el primer algoritmo, $D$ cuenta las sumas ya realizadas; en el segundo, $M$ cuenta los factores que aún faltan.

### 6.2. Demostración del invariante

**Caso base, $n=0$.** Antes de entrar al ciclo:

$$
C_0=0,
\qquad
D_0=0.
$$

Por tanto:

$$
C_0=0=D_0A.
$$

**Hipótesis de inducción.** Supongamos que después de $n$ iteraciones:

$$
C_n=D_nA.
$$

**Paso inductivo.** Una iteración adicional produce:

$$
C_{n+1}=C_n+A,
\qquad
D_{n+1}=D_n+1.
$$

Usando la hipótesis:

$$
\begin{aligned}
C_{n+1}
&=C_n+A\\
&=D_nA+A\\
&=(D_n+1)A\\
&=D_{n+1}A.
\end{aligned}
$$

Se demostró $P(n)\Rightarrow P(n+1)$. Por inducción:

$$
\boxed{\forall n\ge0,\ C_n=D_nA}.
$$

### 6.3. Usar la salida para obtener el resultado

El invariante por sí solo no dice que $C=A^2$. Hay que combinarlo con la condición de salida.

Como $D$ parte de $0$, aumenta de uno en uno y $A\ge0$, al terminar se cumple $D=A$. Entonces:

$$
C=DA=AA=A^2.
$$

Por tanto, la función devuelve el cuadrado de $A$.

### 6.4. ¿Por qué termina?

Mientras el ciclo continúa, $D<A$. La cantidad:

$$
V=A-D
$$

es un entero no negativo y disminuye exactamente en $1$ en cada iteración. No puede disminuir indefinidamente, así que el ciclo llega a $D=A$.

> [!warning] Dominio necesario
> Si $A<0$, $D$ comienza en $0$ y solo aumenta; nunca alcanzará $A$. La prueba del resultado sería solo condicional a que terminara. Exigir $A\ge0$ permite demostrar también la terminación.

---

## 7. Segundo ciclo: descubrir que calcula una potencia

La subrutina recibe $N$ y $M$ no negativos y modifica $M$:

~~~text
Potencia(N, M):
    R := 1
    while M > 0
        R := R * N
        M := M - 1
    return R
~~~

Para distinguir el exponente original del valor mutable, llamaremos:

- $M_0$: exponente recibido al entrar;
- $M_n$: valor que queda después de $n$ iteraciones;
- $R_n$: acumulador después de $n$ iteraciones.

### 7.1. Empezar con un ejemplo: $N=2,\ M_0=5$

| $n$ | $R_n$ | $M_n$ | Producto conservado $R_n2^{M_n}$ |
|---:|---:|---:|---:|
| 0 | 1 | 5 | $1\cdot2^5=32$ |
| 1 | 2 | 4 | $2\cdot2^4=32$ |
| 2 | 4 | 3 | $4\cdot2^3=32$ |
| 3 | 8 | 2 | $8\cdot2^2=32$ |
| 4 | 16 | 1 | $16\cdot2=32$ |
| 5 | 32 | 0 | $32\cdot1=32$ |

Cada iteración mueve un factor $N$ desde la parte “pendiente” hacia $R$. Se observa:

$$
R_n=N^n,
\qquad
M_n=M_0-n.
$$

Eliminamos $n=M_0-M_n$:

$$
R_n=N^{M_0-M_n}.
$$

Una forma más útil, que evita dividir potencias, es:

$$
\boxed{I:\ R_nN^{M_n}=N^{M_0}}.
$$

La igualdad dice: **resultado acumulado × trabajo pendiente = resultado total esperado**.

### 7.2. Caso base

Antes de la primera iteración:

$$
R_0=1,
\qquad
M_0=M_0.
$$

Entonces:

$$
R_0N^{M_0}=1\cdot N^{M_0}=N^{M_0}.
$$

### 7.3. Paso inductivo

Supongamos que después de $n$ iteraciones:

$$
R_nN^{M_n}=N^{M_0}.
$$

Si el cuerpo vuelve a ejecutarse, $M_n>0$, y produce:

$$
R_{n+1}=R_nN,
\qquad
M_{n+1}=M_n-1.
$$

Comprobamos el invariante en el nuevo estado:

$$
\begin{aligned}
R_{n+1}N^{M_{n+1}}
&=(R_nN)N^{M_n-1}\\
&=R_nN^{M_n}\\
&=N^{M_0}.
\end{aligned}
$$

Por inducción, la relación se conserva durante todo el ciclo.

> [!tip] Prueba sin división
> Las diapositivas despejan $R_n=N^{M_0}/N^{M_n}$. La forma multiplicativa $R_nN^{M_n}=N^{M_0}$ es más robusta porque no necesita dividir por $N^{M_n}$ y deja visible la idea de “calculado × pendiente”.

### 7.4. Salida y resultado

El ciclo termina cuando $M_n=0$. Sustituimos en el invariante:

$$
R_nN^0=N^{M_0}.
$$

Como $N^0=1$:

$$
\boxed{R_n=N^{M_0}}.
$$

La subrutina calcula $N$ elevado al exponente original $M_0$.

### 7.5. Terminación

La variante es el propio $M$:

$$
V=M.
$$

Si $M_0\ge0$, durante el ciclo $M>0$ y cada iteración resta $1$. Por tanto, tras exactamente $M_0$ iteraciones se alcanza $M=0$.

---

## 8. Método para inventar un invariante

Los invariantes rara vez aparecen por adivinación pura. Un procedimiento útil es:

1. **Nombrar los estados.** Usar $X_n$ para el valor de $X$ después de $n$ iteraciones.
2. **Trazar pocos casos.** Calcular $n=0,1,2,3$ con números pequeños.
3. **Buscar una fórmula con $n$.** Por ejemplo, $C_n=nA$ o $M_n=M_0-n$.
4. **Eliminar $n$.** Combinar las fórmulas para obtener una relación entre variables del programa.
5. **Conservar los datos originales.** Si una entrada se modifica, nombrar su valor inicial, como $M_0$.
6. **Probar inicialización y mantenimiento.** Los ejemplos sugieren; la inducción demuestra.
7. **Combinar con la salida.** $I\land\neg B$ debe implicar la postcondición.
8. **Buscar una variante.** Una cantidad entera no negativa que disminuya prueba terminación.

~~~mermaid
flowchart TD
    T["Trazar 0, 1, 2, 3 iteraciones"] --> F["Formular variables en función de n"]
    F --> E["Eliminar n"]
    E --> I["Invariante candidato I"]
    I --> B{"¿Vale al inicio?"}
    B -->|"No"| T
    B -->|"Sí"| M{"¿El cuerpo preserva I?"}
    M -->|"No"| F
    M -->|"Sí"| X["Combinar I con la condición de salida"]
    X --> Q["Postcondición"]
~~~

---

## 9. Corrección parcial frente a corrección total

Para un ciclo **while $B$ do $C$**, una demostración completa separa dos obligaciones:

### Corrección parcial

1. El invariante $I$ vale antes del ciclo.
2. Si $I\land B$ vale antes del cuerpo, $I$ vuelve a valer después:

$$
\{I\land B\}\ C\ \{I\}.
$$

3. Al salir, $I\land\neg B$ implica la postcondición $Q$.

### Terminación

Se exhibe una variante $V$ que:

- toma valores en los enteros no negativos mientras el ciclo continúa;
- disminuye estrictamente en cada iteración.

En esta clase:

| Programa | Invariante principal | Condición al salir | Variante |
|---|---|---|---|
| Cuadrado por sumas | $C=DA$ | $D=A$ | $A-D$ |
| Potencia por productos | $RN^M=N^{M_0}$ | $M=0$ | $M$ |

$$
\boxed{
\text{corrección total}
=
\text{invariante y salida correctos}
+
\text{terminación}
}
$$

---

## 10. Errores frecuentes

> [!warning] Probar solo ejemplos
> Una tabla ayuda a descubrir el patrón, pero no sustituye el caso base ni el paso inductivo.

> [!warning] Confundir valor inicial y valor actual
> En el algoritmo de potencia, $M$ cambia. La respuesta debe expresarse con el exponente original $M_0$, no con el $M$ final, que vale $0$.

> [!warning] Olvidar el estado de cero iteraciones
> El invariante debe ser cierto antes de ejecutar el cuerpo. Por eso el caso base suele ser $n=0$.

> [!warning] Creer que el invariante ya es la postcondición
> $C=DA$ solo se convierte en $C=A^2$ cuando también sabemos que el ciclo salió con $D=A$.

> [!warning] Demostrar el resultado pero no la terminación
> Sin una variante o argumento equivalente solo se obtiene corrección parcial: “si termina, el resultado es correcto”.

---

## 11. Plantilla reutilizable

Para verificar un ciclo:

~~~text
1. Especificar la precondición P y la postcondición Q.
2. Nombrar el valor original de cualquier entrada que vaya a cambiar.
3. Trazar unas pocas iteraciones y proponer el invariante I.
4. Inicialización: demostrar P => I.
5. Mantenimiento: demostrar {I y B} cuerpo {I}.
6. Salida: demostrar I y no B => Q.
7. Terminación: encontrar una variante entera no negativa que disminuya.
~~~

Esta plantilla conecta la inducción con la lógica de Hoare: el caso base prueba la inicialización y el paso inductivo prueba el mantenimiento.

---

## 12. Ejercicios de comprobación

1. En el ciclo del cuadrado, usa $A=3$ y escribe los estados $(C,D)$ desde $n=0$ hasta la salida. Verifica $C=DA$ en cada fila.
2. En el ciclo de potencia, usa $N=3$ y $M_0=4$. ¿Qué valor tiene $RN^M$ después de cada iteración?
3. Explica por qué $R=N^M$ **no** es un invariante del segundo ciclo.
4. ¿Qué falla en la terminación de **Cuadrado(A)** si $A=-2$?
5. En la terna con precondición $a>b$, ¿por qué no necesitamos que la asignación $m:=b$ produzca realmente $m=a$?

> [!check]- Respuestas breves
> 1. $(0,0),(3,1),(6,2),(9,3)$; en todos, $C=3D$.
> 2. Siempre vale $3^4=81$: $1\cdot3^4,3\cdot3^3,9\cdot3^2,27\cdot3,81\cdot1$.
> 3. Tanto $R$ como $M$ cambian en sentidos opuestos; por ejemplo, al inicio $R=1$ y $N^M=N^{M_0}$. La relación conservada es $RN^M=N^{M_0}$.
> 4. $D$ empieza en $0$ y aumenta; nunca alcanza $-2$.
> 5. La precondición de la rama falsa es $(a>b)\land\neg(a>b)$, una contradicción; esa rama es inalcanzable.

---

## 13. Complemento de `AllLectures`: las obligaciones de un ciclo

La notación compacta de la regla de `while` se traduce en preguntas concretas. Para

```text
{P} while B do {I} C {Q}
```

hay que demostrar:

1. **Entrada:** $P\Rightarrow I$.
2. **Preservación:** $\{I\land B\}C\{I\}$.
3. **Salida útil:** $I\land\neg B\Rightarrow Q$.

![[slide-67.png]]

Para corrección total se agregan dos obligaciones sobre una variante entera $E$:

4. $I\land B\Rightarrow E\ge0$.
5. Una vuelta del cuerpo reduce $E$ estrictamente.

![[slide-85.png]]

### Ejemplo paso a paso: sumar de 1 a $n$

```text
i := 0; s := 0;
while i < n do
    i := i + 1;
    s := s + i
```

Proponemos

\[
I:\ s=\frac{i(i+1)}2\land0\le i\le n,
\qquad E=n-i.
\]

1. Con $i=0,s=0$, el invariante es cierto.
2. Si vale antes de la vuelta, después $i'=i+1$ y
   \[
   s'=s+i'=\frac{i(i+1)}2+(i+1)=\frac{(i+1)(i+2)}2.
   \]
3. Al salir, $i\ge n$; combinado con $i\le n$, resulta $i=n$.
4. Entonces $s=n(n+1)/2$.
5. $E=n-i$ es no negativa bajo la guarda y disminuye en uno.

Con esto quedan demostradas corrección parcial **y** terminación.

<iframe src="hoare-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 14. Referencia diapositiva por diapositiva

| Diap. | Lámina | Contenido | Sección |
|---:|---:|---|---|
| 1–4 | 101–104 | Verificación del máximo de dos valores | §2 |
| 5–7 | 105–107 | Condicional con precondición $a>b$ | §3 |
| 8 | 108 | Principio de inducción matemática | §5 |
| 9–12 | 109–112 | Cuadrado mediante sumas e invariante $C_n=D_nA$ | §6 |
| 13 | 113 | Definición de invariante e inicio de potencia | §7 |
| 14–17 | 114–117 | Invariante y prueba del algoritmo de potencia | §7 |

## Conceptos atómicos

- [[Regla condicional de Hoare|Regla condicional de Hoare]]
- [[Inducción matemática aplicada a ciclos|Inducción matemática aplicada a ciclos]]
- [[Invariante de ciclo|Invariante de ciclo]]
- [[Corrección parcial y corrección total|Corrección parcial y corrección total]]

## Dudas para revisar

- [x] ¿Cuál es la regla formal de Hoare para **while** y cómo se deriva de estas tres obligaciones? Véanse §13 y [[Condición de verificación|Condición de verificación]].
- [ ] ¿Qué convención adopta el curso para $0^0$ cuando el exponente inicial es cero?
- [ ] ¿Cómo cambia el invariante de potencia rápida cuando el exponente se divide entre dos?

## Resumen después de clase

Un condicional se verifica demostrando una postcondición común en las ramas $B$ y $\neg B$; una rama contradictoria puede ser inalcanzable. Para un ciclo se usa inducción sobre el número de iteraciones: el caso base establece el invariante antes de comenzar y el paso inductivo demuestra que una ejecución del cuerpo lo conserva. Al terminar, el invariante se combina con la negación de la guarda para obtener la postcondición. Una variante decreciente añade la prueba de terminación y convierte la corrección parcial en corrección total.

## Referencia

- [[Programación Avanzada Notas 6.pdf|Programación Avanzada Notas 6]], diapositivas 1–17 (láminas 101–117).
- `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 28–35 y 47–91 (regla de `while`, invención de invariantes, condiciones de verificación y corrección total).
