---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-27"
unidad: Aprendizaje automático
profesor: Carlos Hernández
estado: procesada
conceptos: []
referencias:
tags:
  - clase
  - inteligencia-artificial
  - aprendizaje-supervisado
  - clasificacion
  - regresion-logistica
  - redes-neuronales
---

# Aprendizaje supervisado: clasificación y redes neuronales

> [!summary] Pregunta central
> ¿Cómo aprendemos, a partir de ejemplos etiquetados, una frontera que clasifique observaciones nuevas? ¿Cuándo basta una frontera lineal y qué aporta una capa oculta?

Este apunte corresponde al **27 de octubre de 2026** y trata la **clasificación supervisada**. El [[Indice|plan del curso]] anunciaba *aprendizaje no supervisado* para el 27 y *supervisado* para el 29; aquí se sigue el contenido efectivamente visto en clase. La nota es autocontenida: las fórmulas, las figuras y el ejemplo de las cuatro esquinas se desarrollan completos. Continúa [[2026-10-22 IA - Introducción al ML|la clase de regresión]]: ahora la salida es una **categoría**, no una cantidad real.


| Tema | Sección |
|---|---|
| Clasificación y frontera de decisión | §1 |
| Regresión logística y su optimización | §§2–3 |
| Neuronas, capas, entropía cruzada y softmax | §§4–5 |
| Ejemplo de clases en esquinas opuestas | §6 |
| Aprendizaje por lotes y en línea; aproximación universal | §7 |

## 1. De regresión a clasificación

En aprendizaje supervisado observamos pares $(\mathbf{x}_i,y_i)$. En la clase anterior, $y_i$ era real y una regresión predecía un número. En **clasificación**, $y_i$ pertenece a un conjunto de clases: por ejemplo, $0$ o $1$. Buscamos una función que asigne una clase a una entrada nueva y, si es posible, una probabilidad asociada.

Para dos características $\mathbf{x}=(x_1,x_2)^\mathsf T$, una función de decisión afín es

$$
z(\mathbf{x})=w_1x_1+w_2x_2+b=\mathbf{w}^{\mathsf T}\mathbf{x}+b.
$$

La **frontera de decisión** es el conjunto $z(\mathbf{x})=0$: una recta en dos dimensiones y un hiperplano en más dimensiones. La regla $\hat y=1$ si $z\geq0$, y $\hat y=0$ si $z<0$, separa los dos semiespacios. Para dos clases de patrones $C_1$ y $C_2$ separables por una recta, se ajusta $d(\mathbf x)$ de modo que $d(\mathbf x)>0$ para todo $\mathbf x\in C_1$ y $d(\mathbf x)<0$ para todo $\mathbf x\in C_2$: entonces $d$ es una **función de decisión lineal**. El sesgo puede escribirse como un tercer peso $w_3$; $b$ representa la misma constante. Cambiar los pesos gira la frontera; cambiar $b$ la desplaza. Una sola recta solo puede resolver patrones *linealmente separables*.

### Explorar una frontera

<iframe src="ia19-frontera-clasificacion.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Mueve los coeficientes y alterna entre datos separables y el patrón XOR. En el primer caso puede encontrarse una recta que deje las clases en lados distintos. En XOR, los dos ejemplos de cada clase ocupan esquinas diagonales: **ninguna recta** separa correctamente los cuatro. La intensidad del fondo representa $P(y=1\mid\mathbf{x})$, no la certeza de que el modelo sea correcto.

## 2. Regresión logística binaria

La **sigmoide** transforma el puntaje $z\in\mathbb R$ en un valor entre 0 y 1:

$$
\sigma(z)=\frac{1}{1+e^{-z}},\qquad \pi_i=P(y_i=1\mid\mathbf{x}_i,\boldsymbol\theta)=\sigma(\mathbf{x}_i^\mathsf T\boldsymbol\theta).
$$

Incluimos una primera componente $1$ en $\mathbf{x}_i$ para incorporar el sesgo en $\boldsymbol\theta$. Como $\sigma(0)=1/2$, el umbral de probabilidad $1/2$ corresponde exactamente a $\mathbf{x}^\mathsf T\boldsymbol\theta=0$ . La sigmoide es una curva en S, creciente, con asíntotas 0 y 1, y puede escribirse también como $\sigma(z)=e^{z}/(e^{z}+1)$. Si $z$ es grande y positivo, $\pi$ se acerca a 1; si es grande y negativo, se acerca a 0. El **logit** es la transformación inversa, $\log(\pi/(1-\pi))=z$; no es otro nombre de la sigmoide.

Suponiendo ejemplos condicionalmente independientes, cada etiqueta sigue una Bernoulli:

$$
P(\mathbf y\mid X,\boldsymbol\theta)=\prod_{i=1}^{n}\pi_i^{y_i}(1-\pi_i)^{1-y_i},\qquad y_i\in\{0,1\}.
$$

Maximizar esta verosimilitud equivale a minimizar la **entropía cruzada binaria** o log-verosimilitud negativa:

$$
\boxed{J(\boldsymbol\theta)=-\sum_{i=1}^{n}\left[y_i\log\pi_i+(1-y_i)\log(1-\pi_i)\right].}
$$

Si se divide entre $n$, cambia la escala de la pérdida y del gradiente, pero no su minimizador. Para un ejemplo con $y=1$, la pérdida es $-\log\pi$; si el modelo asigna una probabilidad pequeña a la clase correcta, paga una penalización grande. Con $\pi_i=1/(1+e^{-\mathbf x_i^\mathsf T\boldsymbol\theta})$, la verosimilitud es $\prod_i\bigl(\tfrac{1}{1+e^{-\mathbf x_i\boldsymbol\theta}}\bigr)^{y_i}\bigl(1-\tfrac{1}{1+e^{-\mathbf x_i\boldsymbol\theta}}\bigr)^{1-y_i}$ con $\mathbf x_i\boldsymbol\theta=\theta_0+\sum_{j=1}^d\theta_jx_{ij}$. Como curvas: para $y=1$ la pérdida $-\log\pi$ cae hacia 0 cuando $\pi\to1$ y crece sin cota cuando $\pi\to0$; para $y=0$, $-\log(1-\pi)$ es el reflejo simétrico. Un error frecuente es escribir $\pi=1+e^{-x\theta}$, omitiendo el recíproco. La definición correcta es $\pi=1/(1+e^{-x\theta})$.

### Gradiente y curvatura

Usando $\sigma'(z)=\sigma(z)(1-\sigma(z))$ y $\boldsymbol\pi=(\pi_1,\ldots,\pi_n)^\mathsf T$:

$$
\boxed{\nabla J(\boldsymbol\theta)=X^\mathsf T(\boldsymbol\pi-\mathbf y)},\qquad
\boxed{\nabla^2J(\boldsymbol\theta)=X^\mathsf T\operatorname{diag}\!\bigl(\pi_i(1-\pi_i)\bigr)X.}
$$

Para cualquier vector $\mathbf v$, $\mathbf v^\mathsf T\nabla^2J\mathbf v=\sum_i\pi_i(1-\pi_i)(\mathbf x_i^\mathsf T\mathbf v)^2\geq0$: la pérdida es **convexa** en los parámetros. A veces se afirma que es «positiva definida»; en general solo podemos asegurar **semidefinida positiva**. Es definida positiva si $X$ tiene rango columna completo y todas las probabilidades están estrictamente entre 0 y 1 para parámetros finitos. En datos perfectamente separables y sin regularización, el mínimo de la pérdida puede no alcanzarse con pesos finitos: los coeficientes crecen mientras la pérdida se acerca a cero.

## 3. Descenso de gradiente

Para minimizar $J$, partimos de $\boldsymbol\theta_0$ y actualizamos en dirección descendente:

$$
\boxed{\boldsymbol\theta_{k+1}=\boldsymbol\theta_k-\alpha_k\nabla J(\boldsymbol\theta_k)},\qquad \alpha_k>0.
$$

Esto es el caso $\mathbf p_k=-\nabla J(\boldsymbol\theta_k)$ de la regla general $\boldsymbol\theta_{k+1}=\boldsymbol\theta_k+\alpha_k\mathbf p_k$. Para un gradiente no nulo, $\mathbf p_k^\mathsf T\nabla J=-\|\nabla J\|^2<0$; por ello es una dirección de descenso **local**. Un paso demasiado grande todavía puede aumentar la pérdida. La búsqueda lineal elige $\alpha_k$ sobre esa dirección; también puede fijarse o adaptarse. El algoritmo es: dados $f$, $\nabla f$ y $\mathbf x_0$, hacer $\mathbf x_k=\mathbf x_0$ y, mientras no se cumpla la condición de paro, calcular $\mathbf p_k=-\nabla f(\mathbf x_k)$, calcular el tamaño de paso $\alpha_k$ y actualizar $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf p_k$. En los métodos de búsqueda directa, $\alpha$ se obtiene resolviendo $\min_{\alpha>0}f(\mathbf x_k+\alpha\mathbf p_k)$. Se repite hasta cumplir una condición de paro, como cambio pequeño de pérdida, norma pequeña del gradiente o un límite de iteraciones. Al escribir el pseudocódigo, cuidado con la condición: el ciclo continúa **mientras no** se cumpla la condición de paro.

## 4. De una neurona a una red

Una red artificial busca reflejar observaciones neurofisiológicas, no reproducir su dinámica; es fácil de componer, representa computación simple y tiene conexiones que inhiben y excitan. Las neuronas de una capa se llaman **unidades** y los parámetros, **pesos**; las activaciones se llaman también no linealidades. Una neurona calcula $z=\mathbf w^\mathsf T\mathbf x+b$ y aplica una **activación** $a=\phi(z)$. Una capa completa calcula $\mathbf z=W\mathbf x+\mathbf b$ y luego $\mathbf a=\phi(\mathbf z)$ componente a componente. Aunque suele llamarse «capa lineal», con sesgo es estrictamente una transformación **afín**.

Si encadenamos solo capas afines, toda la composición vuelve a ser afín. Las activaciones no lineales permiten aprender fronteras curvas o combinaciones de regiones. Una sigmoide saturada tiene derivada cercana a cero; al propagar gradientes por muchas capas, esto puede dificultar el aprendizaje. La frase «las derivadas desaparecen» describe un riesgo de saturación, no algo que ocurra en toda red o para toda entrada.

Una red con una capa oculta para dos clases puede escribirse como

$$
\mathbf h=\phi(W_1\mathbf x+\mathbf b_1),\qquad
\pi=\sigma(\mathbf w_2^\mathsf T\mathbf h+b_2).
$$

La capa oculta crea nuevas características; la salida convierte el puntaje final en probabilidad. Los parámetros de todas las capas se ajustan con gradientes calculados mediante la regla de la cadena (*retropropagación*). Aquí solo describimos la arquitectura; la derivación de la retropropagación se desarrolla en [[2026-11-10 IA - Aprendizaje profundo|la clase de aprendizaje profundo]].

### Entropía cruzada y estabilidad numérica

Para dos clases se usa la pérdida binaria de la sección 2. Calcular $\log\sigma(z)$ y $\log(1-\sigma(z))$ de forma ingenua puede causar problemas numéricos cuando $|z|$ es grande. Una forma estable que trabaja directamente con el puntaje es

$$
\ell(z,y)=\max(z,0)-yz+\log\bigl(1+e^{-|z|}\bigr).
$$

Por tanto, la afirmación habitual sobre inestabilidad se refiere al **cálculo ingenuo**, no a la entropía cruzada como objetivo matemático.

## 5. Más de dos clases: softmax

Si hay $K$ clases mutuamente excluyentes, una capa produce puntajes $z_1,\ldots,z_K$ y **softmax** los normaliza:

$$
p_j=\frac{e^{z_j}}{\sum_{k=1}^{K}e^{z_k}},\qquad \sum_{j=1}^{K}p_j=1.
$$

Para dos puntajes $[x,0]$, softmax da $[e^x/(e^x+e^0),\,e^0/(e^x+e^0)]=[\sigma(x),1-\sigma(x)]$. Softmax también produce estimaciones de probabilidad y también se satura (derivadas cercanas a cero). Con una etiqueta *one-hot* $\mathbf t$, la pérdida es $-\sum_jt_j\log p_j=-\log p_{\text{clase correcta}}$. La sigmoide binaria es equivalente a un softmax de dos puntajes en cuanto a la probabilidad de una clase. Para calcular softmax de forma estable, se resta $m=\max_kz_k$ a todos los puntajes: $p_j=e^{z_j-m}/\sum_ke^{z_k-m}$. La combinación softmax con entropía cruzada simplifica el gradiente con respecto a los puntajes a $\mathbf p-\mathbf t$.

**Alcance de la equivalencia:** si los puntajes son directamente afines en $\mathbf x$, tenemos regresión logística multinomial. Si antes hay capas ocultas no lineales, se trata de una red neuronal con salida softmax; la última capa usa la misma pérdida, pero el modelo completo ya no es regresión logística multinomial.

## 6. El ejemplo de las cuatro esquinas

La arquitectura usada es: capa lineal, sigmoide, segunda capa lineal, softmax y entropía cruzada (dos capas). Los datos son cuatro nubes de puntos en el cuadrado $[-7.5,7.5]^2$; las nubes de una misma diagonal comparten clase.

Colocamos cuatro grupos de puntos en las esquinas de un cuadrado, con centros aproximados en $(\pm5,\pm5)$. La **clase A** ocupa la diagonal superior izquierda $(-5,5)$ e inferior derecha $(5,-5)$; la **clase B** ocupa la diagonal opuesta, $(5,5)$ y $(-5,-5)$:

```text
   x2
    ^
  A |  B        A = esquina superior izquierda e inferior derecha
 ---+---> x1    B = esquina superior derecha e inferior izquierda
  B |  A
```

Es la estructura de **XOR**: un único hiperplano no puede asignar ambas esquinas diagonales a una clase y las otras dos a la otra. La red del ejemplo tiene una capa oculta de dos neuronas con activación sigmoide, $\mathbf h=\sigma(W\mathbf x+\mathbf b)$, con

$$
W=\begin{pmatrix}-1&1\\1&-1\end{pmatrix},\qquad\mathbf b=\begin{pmatrix}-4\\-4\end{pmatrix},
$$

es decir, $z_1=-x_1+x_2-4$ y $z_2=x_1-x_2-4$. Cada neurona oculta mide de qué lado de una diagonal está el punto. Evaluando en el centro de cada esquina:

| Esquina (clase) | $(x_1,x_2)$ | $z_1$ | $z_2$ | $h_1=\sigma(z_1)$ | $h_2=\sigma(z_2)$ |
|---|---|---:|---:|---:|---:|
| Superior izquierda (A) | $(-5,5)$ | $6$ | $-14$ | $\approx1$ | $\approx0$ |
| Inferior derecha (A) | $(5,-5)$ | $-14$ | $6$ | $\approx0$ | $\approx1$ |
| Superior derecha (B) | $(5,5)$ | $-4$ | $-4$ | $\approx0.018$ | $\approx0.018$ |
| Inferior izquierda (B) | $(-5,-5)$ | $-4$ | $-4$ | $\approx0.018$ | $\approx0.018$ |

En el espacio oculto $(h_1,h_2)$, las dos esquinas de la clase A quedan en $(1,0)$ y $(0,1)$, mientras que las dos de la clase B **colapsan** cerca del origen $(0.018,0.018)$. Ahora una sola recta separa las clases: por ejemplo, la neurona de salida $s=h_1+h_2-0.5$ es positiva para A (≈ $0.5$) y negativa para B (≈ $-0.46$). Así, la capa oculta transforma un problema no separable linealmente en uno separable, y en el plano original la región de decisión es una banda diagonal que contiene a la clase B entre dos fronteras.

Al proyectar los puntos sobre cada neurona oculta, el eje $h_1$ y el eje $h_2$ separan una de las esquinas A de las demás y las esquinas B quedan juntas cerca de $(0,0)$; la salida lineal de la segunda capa ordena las clases sobre un solo eje y, en el plano original, el fondo coloreado muestra una banda diagonal que separa las dos clases. Este es un ejemplo ilustrativo de que una red con una capa oculta puede resolver XOR; los pesos de la capa de salida son un ejemplo de elección posible, no una prueba de que cualquier entrenamiento llegue a ellos.

## 7. Tamaño de los lotes y capacidad de aproximación

Hay tres formas de calcular cada actualización de parámetros:

| Modalidad | Datos usados en cada paso | Consecuencia práctica |
|---|---|---|
| **Batch** o lote completo | Todos los $n$ ejemplos | Gradiente estable, pero cada paso cuesta más |
| **Online** o estocástico | Un ejemplo | Pasos baratos y ruidosos; permite datos que llegan continuamente |
| **Mini-batch** | Un subconjunto | Compromiso entre costo y variación del gradiente |

En todos los casos se aplica $\boldsymbol\theta\leftarrow\boldsymbol\theta-\eta\,\widehat{\nabla J}$. En el mini-batch del ejemplo se suman 20 ejemplos. Las curvas de pérdida contra número de iteración (hasta 100) son suaves con lote completo y más ruidosas con gradiente estocástico, aunque ambas descienden. Para **mínimos cuadrados**, cada contribución usa el residuo $y_i-\mathbf x_i^\mathsf T\boldsymbol\theta$; para el gradiente de entropía cruzada de la regresión logística se reemplaza el residuo por $y_i-\pi_i$ en cada contribución. Si $J$ se define como promedio, también se promedia el gradiente del lote.

El **teorema de aproximación universal** afirma, bajo hipótesis adecuadas, que una red de una capa oculta con suficientes unidades puede aproximar arbitrariamente bien funciones continuas en un dominio compacto. Habla de **existencia y capacidad expresiva**: Dicho de forma más precisa: para cualquier función continua del hipercubo $[0,1]^d$ en los reales y cualquier $\varepsilon>0$, existe una red con sigmoides y una capa oculta cuyo error es a lo sumo $\varepsilon$. Intuitivamente, una suma ponderada de sigmoides desplazadas (escalones suaves) y de las «lomas» que resultan de restarlas aproxima una curva poligonal arbitraria, y con más unidades el ajuste mejora. Redes grandes pueden *aproximar*, pero no *representar* exactamente, cualquier función suave. Además, no asegura que descenso de gradiente encuentre los pesos, que una red pequeña baste ni que generalice fuera de los datos observados.

Hace unos 20 años se usaba solo una capa adicional sobre el modelo de regresión logística, con énfasis en optimización convexa y pocos datos; hoy se emplean redes profundas, optimización no convexa y grandes cantidades de datos.

## Comprobaciones para estudiar

1. ¿Qué representa $\mathbf w^\mathsf T\mathbf x+b=0$ en clasificación binaria?
   > [!check]- Respuesta
   > La frontera donde la sigmoide vale $1/2$; a cada lado cambia la clase predicha con ese umbral.
2. Si $y=1$ y el modelo predice $\pi=0.01$, ¿la pérdida es pequeña o grande?
   > [!check]- Respuesta
   > Grande: $-\log(0.01)\approx4.61$.
3. ¿Por qué dos capas afines sin activación no resuelven XOR?
   > [!check]- Respuesta
   > Su composición sigue siendo afín y conserva una frontera lineal.
4. ¿Qué asegura la hessiana semidefinida positiva de la regresión logística?
   > [!check]- Respuesta
   > Que la pérdida es convexa en sus parámetros; no garantiza por sí sola un minimizador finito y único.
5. ¿Qué cambia entre batch, online y mini-batch?
   > [!check]- Respuesta
   > El número de ejemplos usados para estimar cada gradiente y, por ello, el costo y la variación de cada paso.

## Resumen después de clase

La clasificación supervisada aprende una regla a partir de pares etiquetados. La regresión logística aplica una sigmoide a un puntaje afín y ajusta sus pesos minimizando entropía cruzada, normalmente con métodos basados en gradientes. Una red neuronal añade transformaciones y activaciones no lineales para representar fronteras que un hiperplano no puede, como XOR. Softmax extiende la salida probabilística a varias clases. El tamaño del lote cambia cómo se estiman los gradientes; la capacidad de aproximación de una red no equivale a una garantía de entrenamiento o generalización.

## Acciones de estudio

- [ ] Derivar $\nabla J=X^\mathsf T(\boldsymbol\pi-\mathbf y)$ para la regresión logística.
- [ ] Encontrar una frontera para los datos separables y comprobar en el recurso por qué falla con XOR.
- [ ] Explicar con un ejemplo cuándo se satura la sigmoide y cómo afecta a su derivada.
- [ ] Distinguir una salida softmax directamente afín de una red con capa oculta.
