---
tipo: guia-estudio
materia: "[[Indice|Programación Avanzada]]"
estado: procesada
fuente_externa: /Users/diegovillalba/Downloads/AllLectures.pdf
conceptos:
  - "[[Terna de Hoare|Terna de Hoare]]"
  - "[[Axioma de asignación de Hoare|Axioma de asignación de Hoare]]"
  - "[[Precondición más débil|Precondición más débil]]"
  - "[[Condición de verificación|Condición de verificación]]"
  - "[[Invariante de ciclo|Invariante de ciclo]]"
  - "[[Función variante|Función variante]]"
tags: [programacion-avanzada, logica-de-hoare, guia-estudio, paso-a-paso]
---

# Guía paso a paso — Lógica de Hoare

> [!abstract] Idea central
> Una terna de Hoare no ejecuta el programa: **demuestra una relación entre estados**. La ejecución avanza desde la entrada hacia la salida; la prueba de asignaciones suele construirse desde la postcondición hacia atrás.

## Ruta de estudio

1. Entender qué afirma \(\{P\}\,C\,\{Q\}\).
2. Aprender la sustitución correcta para una asignación.
3. Encadenar instrucciones mediante aserciones intermedias.
4. Separar las ramas de un condicional.
5. Anotar un ciclo con un invariante.
6. Convertir la prueba en [[Condición de verificación|condiciones de verificación]].
7. Añadir una [[Función variante|variante]] si se necesita corrección total.

<iframe src="hoare-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El recurso anterior permite recorrer una secuencia, un condicional y un ciclo paso por paso. Si no carga, los ejemplos completos aparecen también abajo.

---

## 1. ¿Qué afirma una terna?

\[
\{P\}\ C\ \{Q\}
\]

- \(P\): estados iniciales permitidos.
- \(C\): comando que transforma el estado.
- \(Q\): condición exigida al terminar.

En **corrección parcial** se lee:

> Si el estado inicial cumple \(P\) y \(C\) termina, el estado final cumple \(Q\).

No afirma que el programa vaya a terminar. Para obtener corrección total se demuestra además la terminación.

![[slide-5.png]]

### Ejemplo mínimo

\[
\{x=1\}\ x:=x+1\ \{x=2\}.
\]

1. Antes, el valor de \(x\) es \(1\).
2. La asignación evalúa \(x+1\) usando ese valor anterior.
3. Guarda \(2\) como valor nuevo de \(x\).
4. La postcondición \(x=2\) queda satisfecha.

> [!warning] No confundir validez y demostrabilidad
> \(\models \{P\}C\{Q\}\) significa que la terna es verdadera según la semántica. \(\vdash \{P\}C\{Q\}\) significa que puede derivarse con las reglas del sistema. La corrección (*soundness*) conecta ambas: todo lo demostrable debe ser válido.

---

## 2. Asignación: sustituir desde la meta

Para \(V:=E\) y postcondición \(Q\):

\[
\boxed{\{Q[E/V]\}\ V:=E\ \{Q\}}.
\]

Se sustituye **la variable asignada \(V\) por la expresión \(E\) dentro de \(Q\)**.

![[slide-15.png]]

### Ejemplo guiado

Completar:

\[
\{?\}\ k:=4a\ \{k=12\}.
\]

**Paso 1.** Variable asignada: \(V=k\).

**Paso 2.** Expresión: \(E=4a\).

**Paso 3.** Meta: \(Q\equiv k=12\).

**Paso 4.** Sustituir:

\[
Q[4a/k]\equiv 4a=12.
\]

**Paso 5.** Simplificar: \(a=3\).

\[
\boxed{\{a=3\}\ k:=4a\ \{k=12\}}.
\]

### La falacia “hacia adelante”

No se debe empezar con una \(P\) cualquiera y sustituir mecánicamente para fabricar la postcondición. Por ejemplo, una regla errónea podría “probar” \(\{x=0\}\ x:=1\ \{x=0\}\), aunque la asignación claramente deja \(x=1\).

![[slide-16.png]]

> [!tip] Prueba de cordura
> Después de calcular la precondición, elige un valor que la satisfaga, ejecuta la asignación y comprueba \(Q\). Esta prueba no sustituye la demostración, pero detecta rápido una sustitución invertida.

---

## 3. Secuencias: una condición intermedia une dos pruebas

\[
\frac{\{P\}C_1\{R\}\qquad \{R\}C_2\{Q\}}
{\{P\}C_1;C_2\{Q\}}.
\]

Para calcular \(R\), conviene retroceder desde \(Q\).

### Ejemplo guiado

```text
x := x + 1;
y := 2*x
```

Meta: \(y\ge10\).

1. Última instrucción:

   \[
   wlp(y:=2x,\ y\ge10)=2x\ge10\iff x\ge5.
   \]

2. Primera instrucción:

   \[
   wlp(x:=x+1,\ x\ge5)=x+1\ge5\iff x\ge4.
   \]

3. Terna completa:

   \[
   \boxed{\{x\ge4\}\ x:=x+1;\ y:=2x\ \{y\ge10\}}.
   \]

### Ejemplo del intercambio

Las variables auxiliares \(x_0,y_0\) nombran valores iniciales que no cambian:

```text
{X=x₀ ∧ Y=y₀}
R := X;
X := Y;
Y := R
{X=y₀ ∧ Y=x₀}
```

Las condiciones intermedias son:

```text
{X=x₀ ∧ Y=y₀}
R := X;
{R=x₀ ∧ Y=y₀}
X := Y;
{R=x₀ ∧ X=y₀}
Y := R
{Y=x₀ ∧ X=y₀}
```

![[slide-23.png]]

---

## 4. Condicionales: demostrar todos los caminos

\[
\frac{\{P\land B\}C_1\{Q\}\qquad\{P\land\neg B\}C_2\{Q\}}
{\{P\}\ \mathbf{if}\ B\ \mathbf{then}\ C_1\ \mathbf{else}\ C_2\ \{Q\}}.
\]

### Ejemplo guiado: valor absoluto

```text
if x >= 0 then y := x else y := -x
```

Queremos \(y\ge0\).

- Rama verdadera: de \(x\ge0\), `y := x` deja \(y\ge0\).
- Rama falsa: de \(x<0\), `y := -x` deja \(-x>0\), luego \(y\ge0\).
- Ambas alcanzan la misma \(Q\), así que:

\[
\{\top\}\ \mathbf{if}\ x\ge0\ \mathbf{then}\ y:=x\ \mathbf{else}\ y:=-x\ \{y\ge0\}.
\]

![[slide-27.png]]

---

## 5. Ciclos: invariante, salida y variante

Para corrección parcial:

\[
\frac{\{I\land B\}\ C\ \{I\}}
{\{I\}\ \mathbf{while}\ B\ \mathbf{do}\ C\ \{I\land\neg B\}}.
\]

![[slide-30.png]]

El invariante \(I\) debe pasar tres pruebas:

1. **Inicialización:** \(P\Rightarrow I\).
2. **Mantenimiento:** \(\{I\land B\}C\{I\}\).
3. **Salida:** \(I\land\neg B\Rightarrow Q\).

![[slide-33.png]]

### Método para inventarlo

Pregunta qué representa:

\[
\text{lo calculado hasta ahora}
+
\text{lo que falta}
=
\text{resultado deseado}.
\]

Para un factorial descendente:

```text
{X=n ∧ Y=1}
while X != 0 do
    Y := Y*X;
    X := X-1
{X=0 ∧ Y=n!}
```

- \(Y\): producto ya acumulado.
- \(X!\): trabajo que falta.
- \(n!\): resultado total.
- Invariante: \(Y\cdot X!=n!\).

> [!important] A veces hay que fortalecer el invariante
> En el factorial ascendente, \(Y=X!\) se conserva, pero al salir de `while X<N` solo sabemos \(X\ge N\). Agregar \(X\le N\) permite concluir \(X=N\) y por tanto \(Y=N!\).

### Terminar no es lo mismo que conservar

Para corrección total se añade una variante entera \(E\):

1. cuando la guarda es verdadera, \(E\ge0\);
2. cada iteración reduce estrictamente \(E\).

En el factorial ascendente puede usarse \(E=N-X\). No puede disminuir indefinidamente dentro de los enteros no negativos.

![[slide-85.png]]

---

## 6. De programa anotado a condiciones de verificación

Una herramienta de verificación separa el trabajo en tres partes:

1. Una persona propone aserciones intermedias e invariantes.
2. Un generador convierte el programa anotado en fórmulas lógicas.
3. Un demostrador comprueba esas fórmulas.

![[slide-49.png]]

Para

```text
{P} while B do {I} C {Q}
```

se generan:

\[
P\Rightarrow I,
\]

\[
I\land\neg B\Rightarrow Q,
\]

\[
\{I\land B\}\ C\ \{I\}.
\]

En corrección total también se exige que la variante sea no negativa y disminuya.

![[slide-67.png]]

La ventaja conceptual es que, al final, los comandos se han “compilado” y solo quedan afirmaciones de lógica o aritmética.

---

## 7. `wlp`, `wp` y `sp`

La fuente *AllLectures* usa esta convención precisa:

| Transformador | Dirección | Tipo de corrección |
|---|---|---|
| \(wlp(C,Q)\), *weakest liberal precondition* | hacia atrás | parcial |
| \(wp(C,Q)\), *weakest precondition* | hacia atrás | total |
| \(sp(C,P)\), *strongest postcondition* | hacia adelante | parcial |

Para código determinista sin ciclos, las ecuaciones de \(wp\) y \(wlp\) coinciden. La diferencia aparece cuando la terminación puede fallar.

\[
\{P\}C\{Q\}\iff P\Rightarrow wlp(C,Q),
\]

\[
[P]C[Q]\iff P\Rightarrow wp(C,Q).
\]

![[slide-70.png]]

---

## 8. Ejercicios graduados

### Ejercicio 1 · Una asignación

Encuentra la precondición más débil:

\[
\{?\}\ z:=3x-2\ \{z>7\}.
\]

> [!hint]- Pista
> Sustituye \(z\) por \(3x-2\) en \(z>7\).

> [!success]- Solución paso a paso
> \(3x-2>7\), luego \(3x>9\), así que \(x>3\). La terna es \(\{x>3\}\ z:=3x-2\ \{z>7\}\).

### Ejercicio 2 · Secuencia

Calcula la entrada mínima para terminar con \(b=14\):

```text
a := a + 2;
b := 2*a
```

> [!success]- Solución paso a paso
> 1. Antes de `b := 2*a`, se necesita \(2a=14\), es decir, \(a=7\).
> 2. Antes de `a := a+2`, se necesita \(a+2=7\), es decir, \(a=5\).
> 3. Resultado: \(\{a=5\}\ a:=a+2;\ b:=2a\ \{b=14\}\).

### Ejercicio 3 · Detectar una prueba falsa

¿Es válida \(\{x=0\}\ x:=x+1\ \{x=0\}\)? Explica el error sin ejecutar muchos casos.

> [!success]- Solución
> No. El axioma exige como precondición \((x+1)=0\), o sea \(x=-1\). La precondición dada \(x=0\) no implica \(x=-1\).

### Ejercicio 4 · Condicional

Demuestra que este programa deja \(m=\min(a,b)\):

```text
if a <= b then m := a else m := b
```

> [!success]- Solución paso a paso
> - Con \(a\le b\), sustituir \(m\) por \(a\) reduce la meta a \(a=\min(a,b)\), verdadera en esa rama.
> - Con \(a>b\), sustituir \(m\) por \(b\) reduce la meta a \(b=\min(a,b)\), verdadera en esa rama.
> - La regla condicional une ambas pruebas.

### Ejercicio 5 · Invariante

Para

```text
i := 0; s := 0;
while i < n do
    i := i + 1;
    s := s + i
```

usa \(I:s=i(i+1)/2\land0\le i\le n\) y demuestra inicialización, mantenimiento y salida.

> [!success]- Solución paso a paso
> 1. Inicialmente \(i=0,s=0\), luego \(s=0(0+1)/2\).
> 2. Si antes vale \(s=i(i+1)/2\), después de incrementar \(i' = i+1\) y sumar ese valor, \(s'=i(i+1)/2+(i+1)=(i+1)(i+2)/2=i'(i'+1)/2\).
> 3. Al salir, \(i\ge n\); con \(i\le n\) se obtiene \(i=n\).
> 4. Sustituir en \(I\) produce \(s=n(n+1)/2\).
> 5. La variante \(n-i\) es no negativa bajo la guarda y disminuye en uno; el ciclo termina.

---

## 9. Plantilla para resolver problemas

```text
1. Escribe P, C y Q sin ambigüedad.
2. Marca las variables que C modifica.
3. Si no hay ciclos, retrocede desde Q con sustituciones.
4. Si hay if, prueba B y ¬B por separado.
5. Si hay while, propone I:
   a) P ⇒ I
   b) {I ∧ B} C {I}
   c) I ∧ ¬B ⇒ Q
6. Para corrección total, agrega una variante E:
   a) I ∧ B ⇒ E ≥ 0
   b) el cuerpo disminuye E estrictamente
7. Simplifica las obligaciones lógicas.
8. Busca un contraejemplo si alguna implicación parece dudosa.
```

## Errores frecuentes

- Sustituir en la dirección equivocada.
- Usar el mismo símbolo para el valor anterior y el nuevo sin aclaración.
- Probar solo una rama del `if`.
- Mostrar que un candidato parece invariante en ejemplos, pero no demostrar mantenimiento.
- Olvidar combinar \(I\) con \(\neg B\) al salir.
- Confundir una propiedad preservada con una prueba de terminación.
- Usar `wp` para corrección parcial sin advertir que algunas fuentes reservan `wlp` para ese caso.

## Fuente

- `/Users/diegovillalba/Downloads/AllLectures.pdf`, páginas PDF 1–102 para lógica de Hoare básica, condiciones de verificación, precondiciones débiles y corrección total. Las capturas preservadas en `Recursos/AllLectures-Hoare/` corresponden a las páginas PDF 5, 15, 16, 23, 27, 30, 33, 49, 67, 70 y 85.
