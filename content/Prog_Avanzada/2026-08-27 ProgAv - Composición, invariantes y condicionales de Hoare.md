---
tipo: clase
materia: "[[Indice|Programación Avanzada]]"
fecha: 2026-08-27
unidad: Composición, invariantes y condicionales en lógica de Hoare
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[Terna de Hoare|Terna de Hoare]]"
  - "[[Axioma de asignación de Hoare|Axioma de asignación de Hoare]]"
  - "[[Precondición más débil|Precondición más débil]]"
  - "[[Regla de composición de Hoare|Regla de composición de Hoare]]"
  - "[[Invariante de programa|Invariante de programa]]"
  - "[[Regla condicional de Hoare|Regla condicional de Hoare]]"
  - "[[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]]"
referencias:
  - "[[Programación Avanzada Notas 5.pdf|Programación Avanzada Notas 5]]"
tags:
  - clase
  - programacion-avanzada
  - verificacion-formal
  - logica-de-hoare
  - invariantes
  - condicionales
---
![[Programación Avanzada Notas 5.pdf]]
# Composición, invariantes y condicionales de Hoare

## Pregunta central

¿Cómo se demuestra paso a paso que una secuencia de asignaciones o un condicional transforma cualquier estado inicial permitido en un estado que satisface la postcondición?

## Mapa de la clase

~~~mermaid
flowchart LR
    A["Axioma de asignación"] --> WP["Calcular precondiciones hacia atrás"]
    WP --> SEC["Composición secuencial"]
    SEC --> R["Aserciones intermedias"]
    SEC --> INV["Propiedades preservadas"]
    INV --> IP["Invariante de programa"]
    A --> IF["Reglas para condicionales"]
    IF --> T["Rama verdadera"]
    IF --> F["Rama falsa"]
    T --> Q["Postcondición común Q"]
    F --> Q
~~~

La idea unificadora es que la ejecución avanza de izquierda a derecha, pero la demostración suele construirse de derecha a izquierda. Se parte de la postcondición deseada, se calcula qué debía ser cierto antes de la última instrucción y se repite hasta llegar al inicio. Cuando el flujo se divide por una condición, se demuestra cada camino por separado y ambos deben terminar garantizando la misma postcondición. *(Diap. 1–19; láminas 82–100.)*

---

## 1. Herramienta básica: sustitución en una asignación

Para una asignación $V:=E$, el [[Axioma de asignación de Hoare|axioma de asignación]] establece:

$$
\boxed{\{Q^{V}_{E}\}\ V:=E\ \{Q\}}.
$$

$Q^{V}_{E}\equiv Q[E/V]$ significa sustituir en $Q$ cada aparición libre de $V$ por $E$; se lee “$Q$ con $V$ sustituida por $E$”. El resultado es la [[Precondición más débil|precondición más débil]] que garantiza $Q$.

> [!important] Sentido de la sustitución
> No se “despeja el programa”. Se imagina el valor que tendrá la variable después de la asignación y se reemplaza ese valor dentro de la postcondición.

~~~mermaid
flowchart RL
    Q["Postcondición Q"] --> S["Sustituir V por E"]
    S --> WP["Q con E en lugar de V"]
    WP --> H["Precondición de V := E"]
~~~

En las fórmulas siguientes, $\top$ representa la aserción vacía `{ }`: no impone ninguna restricción y es verdadera para todo estado.

---

## 2. Ejercicios de asignación

### Ejemplo a: precondición de $j:=i+1$

Se quiere completar:

$$
\{P\}\ j:=i+1\ \{j>0\}.
$$

**Paso 1.** Identificar $V=j$, $E=i+1$ y $Q:(j>0)$.

**Paso 2.** Sustituir $j$ por $i+1$:

$$
(j>0)^j_{i+1}\equiv(i+1)>0.
$$

**Paso 3.** Simplificar:

$$
i+1>0\iff i>-1.
$$

Por tanto:

$$
\boxed{\{i>-1\}\ j:=i+1\ \{j>0\}}.
$$

~~~mermaid
flowchart RL
    Q["Se desea j mayor que 0"] --> S["Sustituir j por i + 1"]
    S --> I["i + 1 mayor que 0"]
    I --> P["i mayor que -1"]
~~~

Comprobación: $i=-0.5$ produce $j=0.5>0$; $i=-1$ produce $j=0$, que no cumple la desigualdad estricta.

### Ejemplo b: precondición de $y:=x^2$

$$
\{P\}\ y:=x^2\ \{y>1\}.
$$

**Paso 1.** Sustituir $y$ por $x^2$:

$$
P:(x^2>1).
$$

**Paso 2.** Resolver:

$$
x^2>1\iff |x|>1\iff x<-1\lor x>1.
$$

Así:

$$
\boxed{\{x<-1\lor x>1\}\ y:=x^2\ \{y>1\}}.
$$

~~~mermaid
flowchart TD
    Q["Se desea y mayor que 1"] --> S["Sustituir y por x al cuadrado"]
    S --> A["x al cuadrado mayor que 1"]
    A --> B{"¿En qué región está x?"}
    B -->|"x menor que -1"| OK1["Sirve"]
    B -->|"x entre -1 y 1"| NO["No sirve"]
    B -->|"x mayor que 1"| OK2["Sirve"]
~~~

Los extremos $x=-1$ y $x=1$ se excluyen porque producen $y=1$, no $y>1$.

### Ejemplo c: postcondición de $x:=x^2$

$$
\{x>2\}\ x:=x^2\ \{Q\}.
$$

Para distinguir momentos, escribimos $x_0$ para el valor inicial y $x_1$ para el final:

1. $x_0>2$.
2. La asignación produce $x_1=x_0^2$.
3. $x_0>2\Rightarrow x_0^2>4$.
4. Por tanto, $x_1>4$.

$$
\boxed{\{x>2\}\ x:=x^2\ \{x>4\}}.
$$

~~~mermaid
flowchart LR
    S0["Inicio: x0 mayor que 2"] --> C["x := x al cuadrado"]
    C --> E["x1 = x0 al cuadrado"]
    E --> Q["Final: x1 mayor que 4"]
~~~

> [!note]
> En una terna se reutiliza normalmente $x$, pero $x_0,x_1$ evita confundir el valor anterior con el posterior.

### Ejemplo d: precondición de $x:=1/x$

$$
\{P\}\ x:=\frac1x\ \{x\ge0\}.
$$

**Paso 1.** Sustituir $x$ por $1/x$: $\frac1x\ge0$.

**Paso 2.** Incluir el dominio: $x\ne0$.

**Paso 3.** Analizar signos:

$$
\left(\frac1x\ge0\right)\land x\ne0\iff x>0.
$$

Por tanto:

$$
\boxed{\{x>0\}\ x:=1/x\ \{x\ge0\}}.
$$

~~~mermaid
flowchart TD
    X["Valor inicial x"] --> D{"¿x es cero?"}
    D -->|"Sí"| U["La división no está definida"]
    D -->|"No"| SG{"¿x es positivo?"}
    SG -->|"Sí"| POS["El recíproco es positivo; cumple"]
    SG -->|"No"| NEG["El recíproco es negativo; no cumple"]
~~~

---

## 3. Concatenación de código

La concatenación $C_1;C_2$ ejecuta primero $C_1$ y después $C_2$. El estado final de $C_1$ se convierte en el inicial de $C_2$. La [[Regla de composición de Hoare|regla de composición]] es:

$$
\frac{\{P\}\ C_1\ \{R\}\qquad \{R\}\ C_2\ \{Q\}}
{\{P\}\ C_1;C_2\ \{Q\}}.
$$

$R$ es la **aserción intermedia**.

~~~mermaid
flowchart LR
    P["P"] --> C1["Ejecutar C1"]
    C1 --> R["Condición intermedia R"]
    R --> C2["Ejecutar C2"]
    C2 --> Q["Q"]
~~~

Para más instrucciones se aplica la regla repetidamente. Las aserciones intermedias suelen calcularse desde $Q$ hacia atrás.

---

## 4. Ejemplo: mitad de una suma

Demostrar:

$$
\{\top\}\ c:=a+b;\ c:=c/2\ \left\{c=\frac{a+b}{2}\right\}.
$$

**Paso 1. Última instrucción.** Sustituir $c$ por $c/2$:

$$
\frac c2=\frac{a+b}{2}\iff c=a+b.
$$

$$
\{c=a+b\}\ c:=c/2\ \left\{c=\frac{a+b}{2}\right\}. \tag{1}
$$

**Paso 2. Primera instrucción.** Sustituir $c$ por $a+b$:

$$
(a+b)=(a+b)\iff\top.
$$

$$
\{\top\}\ c:=a+b\ \{c=a+b\}. \tag{2}
$$

**Paso 3.** Componer (2) y (1):

$$
\boxed{\{\top\}\ c:=a+b;\ c:=c/2\ \left\{c=\frac{a+b}{2}\right\}}.
$$

~~~mermaid
flowchart LR
    P["Sin restricción"] --> A["c := a + b"]
    A --> R["c = a + b"]
    R --> B["c := c / 2"]
    B --> Q["c = (a + b) / 2"]
    Q -. "verificar hacia atrás" .-> R
    R -. "verificar hacia atrás" .-> P
~~~

La tautología explica por qué no hace falta restringir $a$ o $b$, suponiendo que dividir entre $2$ esté definido.

---

## 5. Ejemplo: construir $1+r+r^2$

$$
\{\top\}\ s:=1;\ s:=s+r;\ s:=s+r^2\ \{s=1+r+r^2\}.
$$

Se supone que $r$ no cambia.

**Paso 1.** Retroceder por $s:=s+r^2$:

$$
(s=1+r+r^2)[s+r^2/s]\iff s=1+r.
$$

$$
\{s=1+r\}\ s:=s+r^2\ \{s=1+r+r^2\}. \tag{1}
$$

**Paso 2.** Retroceder por $s:=s+r$:

$$
(s=1+r)[s+r/s]\iff s=1.
$$

$$
\{s=1\}\ s:=s+r\ \{s=1+r\}. \tag{2}
$$

**Paso 3.** Retroceder por $s:=1$:

$$
(s=1)[1/s]\iff1=1\iff\top.
$$

$$
\{\top\}\ s:=1\ \{s=1\}. \tag{3}
$$

**Paso 4.** Componer (3), (2) y (1).

~~~mermaid
flowchart LR
    P["Sin restricción"] --> C1["s := 1"]
    C1 --> R1["s = 1"]
    R1 --> C2["s := s + r"]
    C2 --> R2["s = 1 + r"]
    R2 --> C3["s := s + r al cuadrado"]
    C3 --> Q["s = 1 + r + r al cuadrado"]
~~~

Cada aserción intermedia registra cuánto de la postcondición ya se construyó.

---

## 6. Ejemplo: intercambiar variables

$$
\{a=A\land b=B\}\ h:=a;\ a:=b;\ b:=h\ \{a=B\land b=A\}.
$$

$A$ y $B$ representan valores iniciales y no cambian.

**Paso 1.** Antes de $b:=h$:

$$
(a=B\land b=A)[h/b]\iff a=B\land h=A.
$$

$$
\{a=B\land h=A\}\ b:=h\ \{a=B\land b=A\}. \tag{1}
$$

**Paso 2.** Antes de $a:=b$:

$$
(a=B\land h=A)[b/a]\iff b=B\land h=A.
$$

$$
\{b=B\land h=A\}\ a:=b\ \{a=B\land h=A\}. \tag{2}
$$

**Paso 3.** Antes de $h:=a$:

$$
(b=B\land h=A)[a/h]\iff b=B\land a=A.
$$

$$
\{a=A\land b=B\}\ h:=a\ \{h=A\land b=B\}. \tag{3}
$$

**Paso 4.** Concatenar (3), (2) y (1).

~~~mermaid
flowchart LR
    S0["Inicio: a = A; b = B"] --> C1["h := a"]
    C1 --> S1["h = A; b = B"]
    S1 --> C2["a := b"]
    C2 --> S2["a = B; h = A"]
    S2 --> C3["b := h"]
    C3 --> S3["Final: a = B; b = A"]
~~~

$h$ conserva el valor inicial de $a$, que se perdería al ejecutar $a:=b$.

---

## 7. Invariante de un programa

Un [[Invariante de programa|invariante de programa]] para un bloque $C$ es una aserción $I$ preservada:

$$
\{I\}\ C\ \{I\}.
$$

No exige que las variables conserven sus valores; exige que se conserve la **relación** expresada por $I$.

Es decir, para cualquier aserción que es a la vez , pre condición y post condición de un código se le denomina invariante.

~~~mermaid
flowchart LR
    S0["El estado inicial satisface I"] --> C["El bloque cambia el estado"]
    C --> S1["El estado final también satisface I"]
~~~

### Ejemplo: preservar $r=2^i$

Demostrar que $I:r=2^i$ es invariante de:

~~~text
i := i + 1
r := r * 2
~~~

$$
\{r=2^i\}\ i:=i+1;\ r:=2r\ \{r=2^i\}.
$$

**Paso 1.** Retroceder por $r:=2r$:

$$
(r=2^i)[2r/r]\iff2r=2^i\iff r=2^{i-1}.
$$

$$
\{r=2^{i-1}\}\ r:=2r\ \{r=2^i\}. \tag{1}
$$

**Paso 2.** Retroceder por $i:=i+1$:

$$
r=2^{(i+1)-1}\iff r=2^i.
$$

$$
\{r=2^i\}\ i:=i+1\ \{r=2^{i-1}\}. \tag{2}
$$

**Paso 3.** Componer:

$$
\boxed{\{r=2^i\}\ i:=i+1;\ r:=2r\ \{r=2^i\}}.
$$

~~~mermaid
flowchart LR
    A["Antes: r = 2 elevado a i"] --> C1["i := i + 1"]
    C1 --> M["r = 2 elevado a i - 1 con el nuevo i"]
    M --> C2["r := 2r"]
    C2 --> B["Después: r = 2 elevado a i"]
~~~

Con valores históricos:

$$
r_0=2^{i_0},\qquad i_1=i_0+1,\qquad r_1=2r_0=2^{i_0+1}=2^{i_1}.
$$

Comprobaciones:

- $i=2,r=4$ produce $i=3,r=8=2^3$.
- $i=6,r=64$ produce $i=7,r=128=2^7$.

~~~mermaid
flowchart TD
    E1["i = 2; r = 4"] --> B1["Incrementar i; duplicar r"]
    B1 --> F1["i = 3; r = 8"]
    E2["i = 6; r = 64"] --> B2["Incrementar i; duplicar r"]
    B2 --> F2["i = 7; r = 128"]
~~~

> [!note] Relación con los ciclos
> Si el bloque es el cuerpo de un ciclo y la propiedad también vale antes de la primera iteración, entonces funciona como [[Invariante de ciclo|invariante de ciclo]].

---

## 8. Regla para `if` sin `else`

En `if B then C1`:

1. Si $B$ es verdadera, se ejecuta $C_1$.
2. Si $B$ es falsa, el estado queda igual.

La [[Regla condicional de Hoare|regla condicional]] es:

$$
\frac{
\{P\land B\}\ C_1\ \{Q\}
\qquad
(P\land\neg B)\Rightarrow Q
}
{\{P\}\ \textbf{if }B\textbf{ then }C_1\ \{Q\}}.
$$

La segunda premisa representa la rama `skip`.

~~~mermaid
flowchart TD
    P["Estado satisface P"] --> B{"¿B es verdadera?"}
    B -->|"Sí: P y B"| C1["Ejecutar C1"]
    B -->|"No: P y no B"| SKIP["No hacer nada"]
    C1 --> Q1["Probar Q"]
    SKIP --> Q2["Probar que Q ya se cumplía"]
    Q1 --> Q["Q"]
    Q2 --> Q
~~~

### Ejemplo: actualizar un máximo

Demostrar:

$$
\{\top\}\ \textbf{if }(max<a)\textbf{ then }max:=a\ \{max\ge a\}.
$$

$P=\top$, $B:(max<a)$, $Q:(max\ge a)$.

Es decir:
$$
 \underbrace{max<a}_{\text{ANTES}} \quad\xrightarrow{\;max:=a\;}\quad \underbrace{max=a}_{\text{DESPUÉS}} \quad\Rightarrow\quad \underbrace{max\ge a}_{\text{DESPUÉS}}. 
$$

**Rama falsa.**  $\neg (max<a)$
En un orden total:

$$
\neg(max<a)\iff max\ge a.
$$

Como no cambia el estado:

$$
(\{\top\}\land\neg(max<a))\Rightarrow max\ge a. \tag{1}
$$

**Rama verdadera.** $(max<a)$

Buscamos demostrar que:
$$
\{max<a\}\  max := a\ \{max \geq a\}
$$

Demostrando la precondición:
$$
P = \{Q^V_E\} = \{(max\geq a)\}^{max}_{a} \ = \{max = a , max \geq a\} = \{a\geq a\}
$$

Con lo que obtenemos que por debilitamiento:
$$
\{a= a\} \implies \{a \geq a\}
$$
Asi que podemos fortalecer:
$$
\{a = a\} \max:=a \{max \geq a\}
$$
Lo cual es una tautología:

$$
\{\top\}\ max:=a\ \{max\ge a\}.
$$

Como cualquier aseveración fortalece la vacía entonces: $max<a\Rightarrow\top$, por consecuencia:

$$
\{max<a\}\ max:=a\ \{max\ge a\}. \tag{2}
$$

Las dos ramas garantizan la misma postcondición:

$$
\boxed{\{\top\}\ \textbf{if }(max<a)\textbf{ then }max:=a\ \{max\ge a\}}.
$$

~~~mermaid
flowchart TD
    I["Valores max y a"] --> B{"¿max es menor que a?"}
    B -->|"Sí"| ASG["max := a"]
    ASG --> EQ["max = a"]
    EQ --> Q["max mayor o igual que a"]
    B -->|"No"| GE["max ya era mayor o igual que a"]
    GE --> Q
~~~

---

## 9. Regla para `if` con `else`

Para `if B then C1 else C2`, ambas ramas ejecutan código:

$$
\frac{
\{P\land B\}\ C_1\ \{Q\}
\qquad
\{P\land\neg B\}\ C_2\ \{Q\}
}
{\{P\}\ \textbf{if }B\textbf{ then }C_1\textbf{ else }C_2\ \{Q\}}.
$$

~~~mermaid
flowchart TD
    P["Estado satisface P"] --> B{"Evaluar B"}
    B -->|"Verdadera"| C1["Ejecutar C1 con P y B"]
    B -->|"Falsa"| C2["Ejecutar C2 con P y no B"]
    C1 --> Q1["Probar Q"]
    C2 --> Q2["Probar Q"]
    Q1 --> Q["Postcondición común Q"]
    Q2 --> Q
~~~

$P$ acompaña a ambas ramas; lo adicional es $B$ o $\neg B$. Las dos deben establecer $Q$, o una condición más fuerte que implique $Q$.

### Ejemplo complementario: máximo de dos valores

No aparece desarrollado en las diapositivas, pero aplica la regla:

~~~text
if a >= b then max := a else max := b
~~~

Se desea $Q:(max\ge a\land max\ge b)$.

- Si $a\ge b$, $max:=a$ produce $Q$.
- Si $a<b$, $max:=b$ produce $Q$.

~~~mermaid
flowchart TD
    S["Valores a y b"] --> D{"¿a es mayor o igual que b?"}
    D -->|"Sí"| A["max := a"]
    D -->|"No"| B["max := b"]
    A --> Q["max domina a y b"]
    B --> Q
~~~

---

## 10. Método general de demostración

### Para una secuencia

1. Escribir la postcondición final $Q$.
2. Tomar la última asignación y calcular $Q^{V}_{E}$.
3. Usar el resultado como postcondición de la instrucción anterior.
4. Repetir hasta llegar al principio.
5. Verificar que la precondición declarada implica la calculada.
6. Unir las ternas con la regla de composición.

~~~mermaid
flowchart RL
    Q["Postcondición final Q"] --> W3["wp de la última instrucción"]
    W3 --> R2["Condición intermedia R2"]
    R2 --> W2["wp de la instrucción anterior"]
    W2 --> R1["Condición intermedia R1"]
    R1 --> W1["wp de la primera instrucción"]
    W1 --> P0["Precondición calculada"]
    P["Precondición dada"] --> IMP["Comprobar P implica P0"]
    P0 --> IMP
~~~

### Para un condicional

1. Identificar $P$, $B$ y $Q$.
2. Demostrar $\{P\land B\}C_1\{Q\}$.
3. En la rama falsa, añadir $\neg B$.
4. Sin `else`, probar $(P\land\neg B)\Rightarrow Q$.
5. Con `else`, demostrar $\{P\land\neg B\}C_2\{Q\}$.
6. Concluir con la regla condicional.

---

## 11. Precisiones importantes

> [!warning] Dominio
> En $x:=1/x$, además de sustituir, debe exigirse $x\ne0$. Toda operación parcial aporta obligaciones de dominio.

> [!note] Aserción vacía
> `{ }` representa $\top$, la aserción verdadera para todo estado; no una condición imposible.

> [!note] Valores anteriores y posteriores
> En $x:=x^2$, el lado derecho usa el valor anterior y el izquierdo recibe el nuevo. $x_0,x_1$ elimina la ambigüedad.

> [!note] Invariante de bloque y de ciclo
> $\{I\}C\{I\}$ prueba preservación por un bloque. Para un ciclo también debe demostrarse que $I$ vale antes de la primera iteración.

> [!note] `if` sin `else`
> La rama falsa no desaparece: ejecuta `skip`, por lo que $P\land\neg B$ debe implicar $Q$.

---

## 12. Complemento de `AllLectures`: del programa anotado a la prueba

Una secuencia larga se vuelve más fácil cuando se inserta una aserción en cada punto importante. Por ejemplo, el intercambio queda anotado así:

```text
{X=x₀ ∧ Y=y₀}
R := X;
{R=x₀ ∧ Y=y₀}
X := Y;
{R=x₀ ∧ X=y₀}
Y := R
{Y=x₀ ∧ X=y₀}
```

**Paso 1.** Cada asignación se demuestra con sustitución.

**Paso 2.** La postcondición de un renglón coincide con la precondición del siguiente.

**Paso 3.** La regla de composición elimina las aserciones intermedias y deja la terna del programa completo.

![[slide-23.png]]

En un condicional no hay una sola condición intermedia: hay dos obligaciones, una bajo $B$ y otra bajo $\neg B$. Ambas deben llegar a la misma $Q$.

![[slide-27.png]]

### Ejercicio corto

Demuestra $\{\top\}\ \mathbf{if}\ a\le b\ \mathbf{then}\ m:=a\ \mathbf{else}\ m:=b\ \{m=\min(a,b)\}$.

> [!success]- Solución paso a paso
> 1. Rama $a\le b$: sustituir $m$ por $a$ reduce la meta a $a=\min(a,b)$.
> 2. Rama $a>b$: sustituir $m$ por $b$ reduce la meta a $b=\min(a,b)$.
> 3. Las dos fórmulas son verdaderas bajo la guarda de su rama.
> 4. La regla condicional une ambas derivaciones.

Véase también [[Guía paso a paso - Lógica de Hoare#4. Condicionales demostrar todos los caminos|la explicación guiada de condicionales]].

## 13. Referencia diapositiva por diapositiva

| Diap. | Lámina | Contenido | Sección |
|---:|---:|---|---|
| 1 | 82 | Precondiciones de $j:=i+1$ y $y:=x^2$ | §2 a–b |
| 2 | 83 | Postcondición de $x:=x^2$; precondición de $x:=1/x$ | §2 c–d |
| 3 | 84 | Concatenación de código | §3 |
| 4 | 85 | Regla de concatenación y ejemplo de la media | §3–4 |
| 5 | 86 | Demostración de la media | §4 |
| 6 | 87 | Inicio del ejemplo $1+r+r^2$ | §5 |
| 7 | 88 | Fin del polinomio e inicio del intercambio | §5–6 |
| 8 | 89 | Demostración del intercambio | §6 |
| 9 | 90 | Invariante y ejemplo $r=2^i$ | §7 |
| 10 | 91 | Demostración formal del invariante | §7 |
| 11 | 92 | Casos $i=2$ e $i=6$ | §7 |
| 12 | 93 | Comprobación algebraica | §7 |
| 13 | 94 | `if` sin `else` | §8 |
| 14 | 95 | Regla y diagrama sin `else` | §8 |
| 15 | 96 | Ejemplo del máximo | §8 |
| 16 | 97 | Rama verdadera y consecuencia | §8 |
| 17 | 98 | Conclusión del ejemplo | §8 |
| 18 | 99 | `if` con `else` | §9 |
| 19 | 100 | Regla y diagrama con `else` | §9 |

## Conceptos atómicos

- [[Terna de Hoare|Terna de Hoare]]
- [[Axioma de asignación de Hoare|Axioma de asignación de Hoare]]
- [[Precondición más débil|Precondición más débil]]
- [[Regla de composición de Hoare|Regla de composición de Hoare]]
- [[Invariante de programa|Invariante de programa]]
- [[Invariante de ciclo|Invariante de ciclo]]
- [[Regla condicional de Hoare|Regla condicional de Hoare]]
- [[Regla de consecuencia de Hoare|Regla de consecuencia de Hoare]]

## Dudas para revisar

- [x] ¿Cómo se extienden estas reglas al `while` y cómo se demuestra terminación? Véase [[Guía paso a paso - Lógica de Hoare#5. Ciclos invariante salida y variante|Ciclos: invariante, salida y variante]].
- [ ] ¿Qué notación usará el curso para `skip`?
- [ ] ¿Los ejercicios asumen números reales, racionales o punto flotante?

## Resumen después de clase

El axioma de asignación permite calcular precondiciones por sustitución y demostrar desde la salida hacia la entrada. La composición conecta instrucciones mediante aserciones intermedias, como en la media, el polinomio y el intercambio. Un invariante es una relación preservada aun cuando cambien los valores individuales. En un condicional se analizan por separado $B$ y $\neg B$, y ambos caminos deben garantizar la misma postcondición.

## Referencia

- [[Programación Avanzada Notas 5.pdf|Programación Avanzada Notas 5]], diapositivas 1–19 (láminas 82–100).
- `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 23–33 (composición, condicionales, regla de `while` e invariantes).
