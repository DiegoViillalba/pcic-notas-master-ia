---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-27"
unidad: Aprendizaje automático
profesor: Carlos Hernández
estado: procesada
conceptos: []
referencias:
  - "[[AI 19 Aprendizaje supervisado.pdf]]"
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

Este apunte corresponde al **27 de octubre de 2026** y sigue la presentación «Clase 19: aprendizaje supervisado - clasificación» proporcionada para la sesión. El [[Indice|plan del curso]] anunciaba *aprendizaje no supervisado* para el 27 y *supervisado* para el 29; aquí se prioriza el contenido del PDF, sin asumir que la planeación se actualizó. Continúa [[2026-10-22 IA - Introducción al ML|la clase de regresión]]: ahora la salida es una **categoría**, no una cantidad real.

![[AI 19 Aprendizaje supervisado.pdf]]

| Tema | Diapositivas |
|---|---:|
| Clasificación y frontera de decisión | 3–5 |
| Regresión logística y su optimización | 6–12 |
| Neuronas, capas, entropía cruzada y softmax | 13–21 |
| Ejemplo de clases en esquinas opuestas | 22–25 |
| Aprendizaje por lotes y en línea; aproximación universal | 27–30 |

## 1. De regresión a clasificación

En aprendizaje supervisado observamos pares $(\mathbf{x}_i,y_i)$. En la clase anterior, $y_i$ era real y una regresión predecía un número. En **clasificación**, $y_i$ pertenece a un conjunto de clases: por ejemplo, $0$ o $1$. Buscamos una función que asigne una clase a una entrada nueva y, si es posible, una probabilidad asociada.

Para dos características $\mathbf{x}=(x_1,x_2)^\mathsf T$, una función de decisión afín es

$$z(\mathbf{x})=w_1x_1+w_2x_2+b=\mathbf{w}^{\mathsf T}\mathbf{x}+b.$$

La **frontera de decisión** es el conjunto $z(\mathbf{x})=0$: una recta en dos dimensiones y un hiperplano en más dimensiones. La regla $\hat y=1$ si $z\geq0$, y $\hat y=0$ si $z<0$, separa los dos semiespacios. La diapositiva 5 escribe el sesgo como $w_3$; $b$ representa la misma constante. Cambiar los pesos gira la frontera; cambiar $b$ la desplaza. Una sola recta solo puede resolver patrones *linealmente separables*.

### Explorar una frontera

<iframe src="ia19-frontera-clasificacion.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Mueve los coeficientes y alterna entre datos separables y el patrón XOR. En el primer caso puede encontrarse una recta que deje las clases en lados distintos. En XOR, los dos ejemplos de cada clase ocupan esquinas diagonales: **ninguna recta** separa correctamente los cuatro. La intensidad del fondo representa $P(y=1\mid\mathbf{x})$, no la certeza de que el modelo sea correcto.

## 2. Regresión logística binaria

La **sigmoide** transforma el puntaje $z\in\mathbb R$ en un valor entre 0 y 1:

$$\sigma(z)=\frac{1}{1+e^{-z}},\qquad \pi_i=P(y_i=1\mid\mathbf{x}_i,\boldsymbol\theta)=\sigma(\mathbf{x}_i^\mathsf T\boldsymbol\theta).$$

Incluimos una primera componente $1$ en $\mathbf{x}_i$ para incorporar el sesgo en $\boldsymbol\theta$. Como $\sigma(0)=1/2$, el umbral de probabilidad $1/2$ corresponde exactamente a $\mathbf{x}^\mathsf T\boldsymbol\theta=0$ (diapositiva 7). Si $z$ es grande y positivo, $\pi$ se acerca a 1; si es grande y negativo, se acerca a 0. El **logit** es la transformación inversa, $\log(\pi/(1-\pi))=z$; no es otro nombre de la sigmoide.

Suponiendo ejemplos condicionalmente independientes, cada etiqueta sigue una Bernoulli:

$$P(\mathbf y\mid X,\boldsymbol\theta)=\prod_{i=1}^{n}\pi_i^{y_i}(1-\pi_i)^{1-y_i},\qquad y_i\in\{0,1\}.$$

Maximizar esta verosimilitud equivale a minimizar la **entropía cruzada binaria** o log-verosimilitud negativa:

$$\boxed{J(\boldsymbol\theta)=-\sum_{i=1}^{n}\left[y_i\log\pi_i+(1-y_i)\log(1-\pi_i)\right].}$$

Si se divide entre $n$, cambia la escala de la pérdida y del gradiente, pero no su minimizador. Para un ejemplo con $y=1$, la pérdida es $-\log\pi$; si el modelo asigna una probabilidad pequeña a la clase correcta, paga una penalización grande. En la diapositiva 8 aparece $\pi=1+e^{-x\theta}$: falta el recíproco. La definición correcta es $\pi=1/(1+e^{-x\theta})$.

### Gradiente y curvatura

Usando $\sigma'(z)=\sigma(z)(1-\sigma(z))$ y $\boldsymbol\pi=(\pi_1,\ldots,\pi_n)^\mathsf T$:

$$\boxed{\nabla J(\boldsymbol\theta)=X^\mathsf T(\boldsymbol\pi-\mathbf y)},\qquad
\boxed{\nabla^2J(\boldsymbol\theta)=X^\mathsf T\operatorname{diag}\!\bigl(\pi_i(1-\pi_i)\bigr)X.}$$

Para cualquier vector $\mathbf v$, $\mathbf v^\mathsf T\nabla^2J\mathbf v=\sum_i\pi_i(1-\pi_i)(\mathbf x_i^\mathsf T\mathbf v)^2\geq0$: la pérdida es **convexa** en los parámetros. La diapositiva 9 afirma «positiva definida»; en general solo podemos asegurar **semidefinida positiva**. Es definida positiva si $X$ tiene rango columna completo y todas las probabilidades están estrictamente entre 0 y 1 para parámetros finitos. En datos perfectamente separables y sin regularización, el mínimo de la pérdida puede no alcanzarse con pesos finitos: los coeficientes crecen mientras la pérdida se acerca a cero.

## 3. Descenso de gradiente

Para minimizar $J$, partimos de $\boldsymbol\theta_0$ y actualizamos en dirección descendente:

$$\boxed{\boldsymbol\theta_{k+1}=\boldsymbol\theta_k-\alpha_k\nabla J(\boldsymbol\theta_k)},\qquad \alpha_k>0.$$

Esto es el caso $\mathbf p_k=-\nabla J(\boldsymbol\theta_k)$ de la regla general $\boldsymbol\theta_{k+1}=\boldsymbol\theta_k+\alpha_k\mathbf p_k$. Para un gradiente no nulo, $\mathbf p_k^\mathsf T\nabla J=-\|\nabla J\|^2<0$; por ello es una dirección de descenso **local**. Un paso demasiado grande todavía puede aumentar la pérdida. La búsqueda lineal elige $\alpha_k$ sobre esa dirección; también puede fijarse o adaptarse. Se repite hasta cumplir una condición de paro, como cambio pequeño de pérdida, norma pequeña del gradiente o un límite de iteraciones. La diapositiva 12 invierte verbalmente la condición al decir «mientras condición_de_paro»; el ciclo continúa **mientras no** se cumpla.

## 4. De una neurona a una red

Una neurona calcula $z=\mathbf w^\mathsf T\mathbf x+b$ y aplica una **activación** $a=\phi(z)$. Una capa completa calcula $\mathbf z=W\mathbf x+\mathbf b$ y luego $\mathbf a=\phi(\mathbf z)$ componente a componente. Aunque la presentación llama «lineal» a la capa, con sesgo es estrictamente una transformación **afín** (diapositiva 16).

Si encadenamos solo capas afines, toda la composición vuelve a ser afín. Las activaciones no lineales permiten aprender fronteras curvas o combinaciones de regiones. Una sigmoide saturada tiene derivada cercana a cero; al propagar gradientes por muchas capas, esto puede dificultar el aprendizaje. «Las derivadas desaparecen» en la diapositiva 17 describe un riesgo de saturación, no algo que ocurra en toda red o para toda entrada.

Una red con una capa oculta para dos clases puede escribirse como

$$\mathbf h=\phi(W_1\mathbf x+\mathbf b_1),\qquad
\pi=\sigma(\mathbf w_2^\mathsf T\mathbf h+b_2).$$

La capa oculta crea nuevas características; la salida convierte el puntaje final en probabilidad. Los parámetros de todas las capas se ajustan con gradientes calculados mediante la regla de la cadena (*retropropagación*). La presentación muestra la arquitectura, pero no desarrolla esa derivación.

### Entropía cruzada y estabilidad numérica

Para dos clases se usa la pérdida binaria de la sección 2. Calcular $\log\sigma(z)$ y $\log(1-\sigma(z))$ de forma ingenua puede causar problemas numéricos cuando $|z|$ es grande. Una forma estable que trabaja directamente con el puntaje es

$$\ell(z,y)=\max(z,0)-yz+\log\bigl(1+e^{-|z|}\bigr).$$

Por tanto, la afirmación de la diapositiva 18 sobre inestabilidad se refiere al **cálculo ingenuo**, no a la entropía cruzada como objetivo matemático.

## 5. Más de dos clases: softmax

Si hay $K$ clases mutuamente excluyentes, una capa produce puntajes $z_1,\ldots,z_K$ y **softmax** los normaliza:

$$p_j=\frac{e^{z_j}}{\sum_{k=1}^{K}e^{z_k}},\qquad \sum_{j=1}^{K}p_j=1.$$

Con una etiqueta *one-hot* $\mathbf t$, la pérdida es $-\sum_jt_j\log p_j=-\log p_{\text{clase correcta}}$. La sigmoide binaria es equivalente a un softmax de dos puntajes en cuanto a la probabilidad de una clase. Para calcular softmax de forma estable, se resta $m=\max_kz_k$ a todos los puntajes: $p_j=e^{z_j-m}/\sum_ke^{z_k-m}$. La combinación softmax con entropía cruzada simplifica el gradiente con respecto a los puntajes a $\mathbf p-\mathbf t$.

**Alcance de la equivalencia:** si los puntajes son directamente afines en $\mathbf x$, tenemos regresión logística multinomial. Si antes hay capas ocultas no lineales, se trata de una red neuronal con salida softmax; la última capa usa la misma pérdida, pero el modelo completo ya no es regresión logística multinomial (diapositiva 20).

## 6. El ejemplo de las cuatro esquinas

Las diapositivas 22–25 colocan cuatro grupos en esquinas: una clase en la diagonal superior izquierda e inferior derecha, y la otra en la diagonal opuesta. Es la estructura de **XOR**. Un único hiperplano no puede asignar ambas esquinas diagonales a una clase y las otras dos a la otra. La red del ejemplo combina dos unidades ocultas para transformar el espacio y formar una región de decisión que sí puede separar esos grupos. Las imágenes muestran una construcción ilustrativa, no una prueba de que cualquier entrenamiento llegue a esos pesos.

## 7. Tamaño de los lotes y capacidad de aproximación

La diapositiva 27 compara cómo se calcula una actualización de parámetros:

| Modalidad | Datos usados en cada paso | Consecuencia práctica |
|---|---|---|
| **Batch** o lote completo | Todos los $n$ ejemplos | Gradiente estable, pero cada paso cuesta más |
| **Online** o estocástico | Un ejemplo | Pasos baratos y ruidosos; permite datos que llegan continuamente |
| **Mini-batch** | Un subconjunto | Compromiso entre costo y variación del gradiente |

En todos los casos se aplica $\boldsymbol\theta\leftarrow\boldsymbol\theta-\eta\,\widehat{\nabla J}$. Las expresiones concretas de la diapositiva 27 usan residuos $y_i-\mathbf x_i^\mathsf T\boldsymbol\theta$ y corresponden a **mínimos cuadrados**, no al gradiente de entropía cruzada de la regresión logística. Para logística se reemplaza el residuo por $y_i-\pi_i$ en cada contribución. Si $J$ se define como promedio, también se promedia el gradiente del lote.

El **teorema de aproximación universal** citado en la diapositiva 28 afirma, bajo hipótesis adecuadas, que una red de una capa oculta con suficientes unidades puede aproximar arbitrariamente bien funciones continuas en un dominio compacto. Habla de **existencia y capacidad expresiva**: no asegura que descenso de gradiente encuentre los pesos, que una red pequeña baste ni que generalice fuera de los datos observados.

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
