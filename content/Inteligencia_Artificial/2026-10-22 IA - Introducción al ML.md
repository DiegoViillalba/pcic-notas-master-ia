---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-22"
unidad: Aprendizaje automático
profesor: Carlos Hernández
estado: procesada
conceptos: []
referencias:
  - "[[AI 18 Aprendizaje máquina.pdf]]"
tags:
  - clase
  - inteligencia-artificial
  - aprendizaje-automatico
  - regresion-lineal
---

# Introducción al aprendizaje máquina y regresión

> [!summary] Pregunta central
> Hasta ahora usamos modelos para razonar y decidir. ¿Cómo aprendemos un modelo a partir de ejemplos y comprobamos que predice bien en datos nuevos?

La sesión del **22 de octubre de 2026** sigue la presentación «Clase 18: introducción a aprendizaje máquina». El 18 es el número de la presentación, mientras que el [[Indice|plan de curso]] asigna el 22 a esta fecha. Continúa la pregunta de [[2026-10-20 IA - Aprendizaje de redes bayesianas|la clase anterior]]: allí aprendimos parámetros y estructura de una red bayesiana; aquí abordamos el marco general y empezamos con regresión.

![[AI 18 Aprendizaje máquina.pdf]]

| Tema | Diapositivas |
|---|---:|
| Definición, tipos y proceso | 3–14 |
| Regresión lineal y mínimos cuadrados | 15–20 |
| Regresión polinomial y complejidad | 21–24 |
| Incertidumbre y procesos gaussianos | 25–27 |
| Ejercicio de demanda de energía | 28 |

## 1. Qué significa aprender

La definición de Tom Mitchell (diapositiva 5) identifica **tarea $T$**, **medida de desempeño $P$** y **experiencia $E$**: se aprende cuando el desempeño en $T$, medido con $P$, mejora gracias a $E$. Para predecir demanda eléctrica, $T$ podría ser estimar el consumo de un edificio, $P$ el error en casos no vistos y $E$ las mediciones previas de clima, ocupación y consumo.

| Tipo | Datos disponibles | Objetivo típico |
|---|---|---|
| **Supervisado** | Entradas y salidas conocidas (etiquetas) | Predecir salidas nuevas: regresión o clasificación |
| **No supervisado** | Entradas sin etiqueta objetivo | Descubrir grupos o estructura |
| **Por refuerzo** | Interacción, acciones y recompensas | Aprender una política que maximice recompensa acumulada |

Las diapositivas 7–8 anticipan regresión lineal y polinomial, regresión logística, redes neuronales, $k$-means y Q-learning. Son temas del curso, no métodos desarrollados todos en esta sesión.

### Representación, optimización y evaluación

Un método de aprendizaje requiere decidir **qué forma puede tener el modelo** (representación), **cómo elegir sus parámetros** (optimización) y **cómo medir su calidad** (evaluación). La diapositiva 10 enumera representaciones numéricas (regresión, redes neuronales), simbólicas (árboles y reglas), basadas en instancias (vecinos cercanos) y probabilísticas (Bayes ingenuo, redes bayesianas).

En la práctica (diapositiva 11) también se define el problema, se reúnen y limpian datos, se interpretan resultados y se integra el modelo en una aplicación. La presentación menciona **CRISP-DM** como ejemplo de proceso. Para medir generalización sin optimismo, los casos de evaluación deben quedar fuera del ajuste y de la selección del modelo.

## 2. Entradas, salidas y objetivo supervisado

Un ejemplo etiquetado es $(\mathbf{x}_i,y_i)$. La entrada $\mathbf{x}_i$ contiene **características** o predictores; $y_i$ es la **respuesta** (diapositivas 12 y 17). Las características pueden ser cuantitativas (velocidad), cualitativas (tipo de edificio) u ordinales (ocupación baja, media, alta). Las cualitativas necesitan una codificación adecuada antes de entrar en un modelo lineal.

- **Clasificación:** la salida es una clase, como *setosa*, *versicolor* o *virginica*, o uno de los dígitos $0,\ldots,9$. Escribir una clase como número no la convierte en una magnitud continua.
- **Regresión:** la salida es una cantidad numérica, como concentración de glucosa o demanda de energía.

Con $n$ ejemplos y $d$ columnas de diseño, agrupamos las entradas en $X\in\mathbb{R}^{n\times d}$ y las respuestas en $\mathbf{y}\in\mathbb{R}^{n}$. Aprendemos $\boldsymbol\theta$ con datos etiquetados para predecir $\hat y(\mathbf{x}_{\mathrm{nuevo}})$.

## 3. Regresión lineal y mínimos cuadrados

Para una característica escalar, la recta es $\hat y_i=\theta_0+\theta_1x_i$. Con varias características se añade una columna constante de unos para el **sesgo** o intercepto:

$$\mathbf{x}_i^{\mathsf T}=(1,x_{i1},\ldots,x_{i,d-1}),\qquad \hat y_i=\mathbf{x}_i^{\mathsf T}\boldsymbol\theta,\qquad \hat{\mathbf y}=X\boldsymbol\theta.$$

Aquí «lineal» significa **lineal en los parámetros $\boldsymbol\theta$**. La diapositiva 19 escribe «$x_{i1}=\theta_1$» para el sesgo; debe ser **$x_{i1}=1$**, con $\theta_1$ como coeficiente de esa columna (o $\theta_0$ si numeramos desde cero).

La función de costo de las diapositivas 18–20 suma errores al cuadrado:

$$J(\boldsymbol\theta)=\sum_{i=1}^{n}(y_i-\hat y_i)^2=\lVert\mathbf y-X\boldsymbol\theta\rVert_2^2.$$

Al expandir y derivar obtenemos

$$J=\mathbf y^{\mathsf T}\mathbf y-2\boldsymbol\theta^{\mathsf T}X^{\mathsf T}\mathbf y+\boldsymbol\theta^{\mathsf T}X^{\mathsf T}X\boldsymbol\theta,$$

$$\nabla_{\boldsymbol\theta}J=-2X^{\mathsf T}\mathbf y+2X^{\mathsf T}X\boldsymbol\theta=2X^{\mathsf T}(X\boldsymbol\theta-\mathbf y).$$

Igualando a cero resultan las **ecuaciones normales** $X^{\mathsf T}X\hat{\boldsymbol\theta}=X^{\mathsf T}\mathbf y$. Si $X$ tiene rango columna completo,

$$\boxed{\hat{\boldsymbol\theta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y.}$$

Si las columnas son dependientes, la inversa no existe; puede usarse la pseudoinversa o regularización. Para cálculo numérico suele ser mejor resolver con QR o SVD que formar explícitamente la inversa. **Aclaración:** la línea intermedia del gradiente en la diapositiva 20 omite el factor 2 del término cuadrático; la derivada anterior corresponde al $J$ definido allí, sin factor $1/2$.

## 4. Regresión polinomial y generalización

Si una recta no captura la relación, transformamos las entradas con $\boldsymbol\phi(\mathbf x)$ y mantenemos un modelo lineal en los coeficientes:

$$\hat y(\mathbf x)=\boldsymbol\phi(\mathbf x)^{\mathsf T}\boldsymbol\theta.$$

Para una entrada escalar, $\boldsymbol\phi(x)=(1,x,x^2)$ permite una parábola. Con dos variables, $(1,x_1,x_2,x_1^2,x_2^2)$ añade curvatura separada; $x_1x_2$ añadiría interacción. La diapositiva 21 llama «núcleos» a estas transformaciones, pero **añadir características explícitas** no es lo mismo que aplicar el *kernel trick* de métodos duales.

Las diapositivas 22–24 comparan datos generados por una relación cuadrática con modelos de distinta complejidad:

| Modelo | Qué sucede | Errores de entrenamiento y prueba |
|---|---|---|
| Grado 2, acorde con los datos | Captura la tendencia sin seguir cada fluctuación del ruido | Ambos se acercan al nivel impuesto por el ruido |
| Demasiado simple | **Subajuste**: no representa la curvatura | Ambos permanecen altos |
| Grado 25 | **Sobreajuste**: puede seguir el ruido | Entrenamiento bajo y prueba mayor, sobre todo con pocos datos |

La curva de prueba del modelo complejo baja al añadir ejemplos, pero más datos no garantizan corregir cualquier sobreajuste. La evaluación debe hacerse con casos separados y representativos del uso real.

### Explorar el ajuste

<iframe src="ia18-complejidad-regresion.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El recurso muestra una relación cuadrática con ruido. Cambia el grado y el número de ejemplos: el grado 1 no alcanza la curvatura, el grado 2 la representa y el grado 8 puede seguir fluctuaciones de una muestra pequeña. Compara el error de entrenamiento con el de prueba; pasar cerca de todos los puntos observados no garantiza una buena predicción.

## 5. Incertidumbre: procesos gaussianos

Una predicción puntual $\hat y$ no dice cuánto desconocemos en otras entradas. Las diapositivas 25–27 presentan los **procesos gaussianos (GP)** como distribuciones sobre funciones: para cualquier conjunto finito de entradas, sus valores tienen una distribución normal multivariada. Una media $\mu(x)$ y una covarianza $\kappa(x,x')$ describen el modelo.

Para entradas observadas $X$, nuevas entradas $X_*$ y valores latentes $\mathbf f$:

$$\begin{pmatrix}\mathbf f\\\mathbf f_*\end{pmatrix}\sim\mathcal N\!\left(\begin{pmatrix}\boldsymbol\mu\\\boldsymbol\mu_*\end{pmatrix},\begin{pmatrix}K&K_*\\K_*^{\mathsf T}&K_{**}\end{pmatrix}\right),$$

donde $K=\kappa(X,X)$, $K_*=\kappa(X,X_*)$ y $K_{**}=\kappa(X_*,X_*)$. Condicionando la normal conjunta en observaciones **sin ruido**:

$$\boxed{\boldsymbol\mu_{*\mid D}=\boldsymbol\mu_*+K_*^{\mathsf T}K^{-1}(\mathbf f-\boldsymbol\mu),\qquad \Sigma_{*\mid D}=K_{**}-K_*^{\mathsf T}K^{-1}K_*.}$$

La diapositiva propone $\kappa(x,x')=\sigma_f^2\exp\!\bigl(-\lVert x-x'\rVert^2/(2\ell^2)\bigr)$: $\sigma_f$ controla la amplitud y $\ell$ la escala de variación. **Si observamos $\mathbf y=\mathbf f+\boldsymbol\epsilon$ con ruido gaussiano de varianza $\sigma_n^2$**, se reemplaza $K^{-1}$ por $(K+\sigma_n^2I)^{-1}$ y $\mathbf f$ por $\mathbf y$ en la fórmula de la media; en la covarianza se reemplaza la misma inversa. Para predecir una observación nueva se suma $\sigma_n^2I$ a la covarianza latente. Esto distingue incertidumbre de la función y ruido de medición.

La media expresa la predicción y la varianza indica dónde el modelo es menos seguro. En el **aprendizaje activo** de la diapositiva 27 se eligen nuevas mediciones en zonas informativas, por ejemplo de alta incertidumbre, para reducirla.

## 6. Ejercicio: demanda de energía

*Diapositiva 28.* Se predice requerimiento de energía $y$ a partir de velocidad del viento $v$ y personas en el edificio $p$.

| $v$ | $p$ | $y$ |
|---:|---:|---:|
| 100 | 2 | 5 |
| 50 | 42 | 25 |
| 45 | 31 | 22 |
| 60 | 35 | 18 |

Con filas $(1,v,p)$ en $X$, mínimos cuadrados da, redondeando,

$$\hat{\boldsymbol\theta}\approx(24.9762,-0.2075,0.2092)^{\mathsf T},\qquad \hat y(v,p)=24.9762-0.2075v+0.2092p.$$

| Entrada $(v,p)$ | Sustitución | Predicción |
|---|---|---:|
| $(75,10)$ | $24.9762-0.2075(75)+0.2092(10)$ | $\approx11.50$ |
| $(300,-4)$ | $24.9762-0.2075(300)+0.2092(-4)$ | $\approx-38.12$ |

La segunda entrada está **fuera del rango observado** ($v$ fue 45–100) y tiene ocupación físicamente imposible. El resultado negativo es algebraicamente correcto, **no** una demanda de energía válida. Habría que validar entradas, reunir datos del rango de interés y considerar restricciones o un modelo adecuado. Cuatro ejemplos para tres parámetros solo ilustran el procedimiento, no establecen una relación confiable.

## Comprobaciones para estudiar

1. ¿En qué se distinguen clasificación y regresión?
   > [!check]- Respuesta
   > En clasificación se predice una clase; en regresión, una cantidad numérica.
2. ¿Por qué la regresión polinomial puede resolverse como regresión lineal?
   > [!check]- Respuesta
   > Porque $\hat y=\boldsymbol\phi(x)^{\mathsf T}\boldsymbol\theta$ es lineal en los coeficientes, aunque sea curva en $x$.
3. ¿Qué ecuación satisface un mínimo estacionario de $J=\lVert\mathbf y-X\boldsymbol\theta\rVert_2^2$?
   > [!check]- Respuesta
   > $X^{\mathsf T}X\boldsymbol\theta=X^{\mathsf T}\mathbf y$; la solución por inversa exige rango columna completo.
4. Si el error de entrenamiento es bajo y el de prueba alto, ¿qué sospechas?
   > [!check]- Respuesta
   > Sobreajuste: se aprendieron peculiaridades de la muestra que no generalizan.
5. ¿Qué representa la banda de incertidumbre de un GP?
   > [!check]- Respuesta
   > La dispersión de la distribución predictiva bajo sus supuestos de media, covarianza y ruido.

## Resumen después de clase

Aprender un modelo consiste en mejorar el desempeño de una tarea a partir de experiencia y exige representación, optimización y evaluación. En aprendizaje supervisado, la regresión predice cantidades y la clasificación categorías. Mínimos cuadrados ajusta una regresión lineal; las características polinomiales permiten curvas, aunque aumentar complejidad puede causar sobreajuste. Los procesos gaussianos añaden una distribución de posibles funciones y cuantifican la incertidumbre de la predicción.

## Acciones de estudio

- [ ] Rehacer las ecuaciones normales para una recta con intercepto.
- [ ] Recalcular el ejercicio y explicar por qué $(300,-4)$ no es una entrada válida en la práctica.
- [ ] Comparar errores de entrenamiento y prueba con distintos grados en el recurso interactivo.
- [ ] Distinguir incertidumbre de la función latente y ruido de una observación en un GP.
