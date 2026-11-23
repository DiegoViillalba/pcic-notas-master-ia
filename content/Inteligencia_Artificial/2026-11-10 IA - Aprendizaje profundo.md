---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: 2026-11-10
unidad: Aprendizaje automático
profesor: Carlos Hernández
estado: procesada
aliases:
  - Aprendizaje profundo
  - Redes neuronales profundas y transformers
  - Inteligencia artificial - 10 de noviembre
referencias:
  - "[[AI 23 Aprendizaje profundo.pdf]]"
  - https://arxiv.org/abs/1706.03762
  - https://arxiv.org/abs/2203.02155
tags:
  - clase
  - inteligencia-artificial
  - aprendizaje-profundo
  - redes-neuronales
  - retropropagacion
  - transformers
  - modelos-de-lenguaje
---

# Aprendizaje profundo: de aprender representaciones a generar lenguaje

**Martes 10 de noviembre de 2026.** Apunte basado en las **39 diapositivas** de «Clase 23: aprendizaje profundo». El plan de la materia llama a esta sesión «Redes neuronales»; el PDF amplía el tema a modelos de lenguaje. Su fecha de creación también corresponde al 10 de noviembre.

> [!summary] La idea que conecta toda la clase
> Una red profunda transforma sus entradas mediante varias etapas aprendidas. La retropropagación calcula cómo cambiar cada parámetro para reducir un error. En un modelo de lenguaje, estas transformaciones convierten tokens en representaciones contextuales y, finalmente, en probabilidades para el siguiente token.

**Cómo estudiar el apunte.** Lee primero la parte I, que construye la intuición sin depender de las ecuaciones. Después recorre la parte II para formalizar cada mecanismo. Las derivaciones, los ejemplos numéricos y los recursos interactivos son **complementos didácticos**, no transcripciones de resultados experimentales de las diapositivas. Los laboratorios funcionan sin conexión y están incrustados junto al concepto correspondiente.

| Recorrido del PDF | Diapositivas | Dónde se desarrolla |
|---|---:|---|
| Softmax, profundidad y ReLU | 3–8 | 1 y 5–6 |
| Grafos computacionales, forward y backward | 9–12 | 2 y 7–8 |
| Evaluación, sesgo y varianza | 13–14 | 3 y 9 |
| Tokens, embeddings y autorregresión | 15–26 | 4 y 10–11 |
| Autoatención y transformer | 27–32 | 4 y 12–13 |
| Autosupervisión, transferencia, ajuste y RLHF | 33–38 | 4 y 14 |
| Presentación y cierre | 1–2, 39 | Contexto de la sesión |

## Parte I. Construir la intuición

## 1. Profundidad: aprender a describir antes de decidir

*Diapositivas 3–8.* Imagina que queremos reconocer un objeto en una imagen. Una decisión directa a partir de todos los píxeles puede ser difícil. Podemos construir representaciones intermedias: combinaciones locales de píxeles, patrones, partes y, finalmente, evidencia para una clase. **Cada etapa vuelve a expresar la información de una forma útil para la siguiente.**

![Profundidad: transformar la representación antes de decidir](ia23-representaciones.svg)

En una red profunda no tenemos que escribir manualmente todos esos detectores: el entrenamiento ajusta las transformaciones. La jerarquía de bordes, formas y objetos de la diapositiva 8 es una **intuición ilustrativa**; una capa real no tiene obligatoriamente una interpretación humana tan limpia.

Una capa realiza una combinación ponderada de sus entradas y aplica una activación. La combinación decide qué información reunir; la activación permite respuestas no lineales. Si solo encadenáramos transformaciones afines, muchas capas se podrían reducir a una sola. Tener más operaciones no bastaría para aumentar ese tipo de capacidad expresiva.

**ReLU como compuerta.** Deja pasar una entrada positiva y convierte una negativa en cero. En su región positiva no comprime progresivamente la señal como una sigmoide saturada. Sin embargo, una unidad que permanezca en la región negativa puede dejar de recibir gradiente por esa ruta: es la intuición de una neurona «muerta».

**Profundidad y anchura.** La profundidad cuenta etapas sucesivas; la anchura, unidades o características dentro de una etapa. No hay un número universal de capas que garantice buen aprendizaje. La comparación histórica de la diapositiva 5 es contexto, no una regla que prohíba redes profundas antes de cierta fecha. Una red con capas ocultas no lineales suele producir un problema de optimización no convexo.

**Conexión previa:** [[2026-10-27 IA - Aprendizaje supervisado y clasificacion|clasificación, XOR y redes neuronales]]. La capa oculta cambia la representación para que una decisión antes difícil se vuelva más sencilla.

## 2. Aprender: predecir, medir el error y repartir responsabilidades

*Diapositivas 9–12.* Entrenar una red tiene tres acciones distintas:

1. **Forward:** pasar la entrada por las operaciones hasta obtener una predicción y una pérdida.
2. **Backward o retropropagación:** recorrer las dependencias en sentido inverso para saber cuánto influye cada parámetro en la pérdida.
3. **Actualización:** usar esos gradientes para cambiar los parámetros, por ejemplo con descenso de gradiente.

![Forward, backward y actualización son tres operaciones distintas](ia23-grafo-gradientes.svg)

La pérdida es un número que resume qué tan mala fue una predicción según el objetivo elegido. El gradiente indica cómo cambiaría ese número ante pequeñas variaciones de los parámetros. **Retropropagación calcula gradientes; el optimizador decide cómo usarlos.**

El grafo computacional registra operaciones y dependencias. Si una variable alimenta dos caminos que llegan a la pérdida, su influencia total reúne las contribuciones de ambos. No se «manda hacia atrás la respuesta correcta»: se propaga sensibilidad de la pérdida mediante la regla de la cadena.

La diapositiva 11 habla de composición secuencial, recursiva y en red. La misma idea se aplica a cadenas, bifurcaciones y parámetros compartidos. Una recurrencia se puede desplegar en el tiempo para formar el grafo que se diferencia.

## 3. Una pérdida baja no basta: evaluar fuera del entrenamiento

*Diapositivas 13–14.* Memorizar los ejemplos observados no garantiza acertar en ejemplos nuevos. Distinguimos tres conjuntos:

| Conjunto | Para qué se usa |
|---|---|
| Entrenamiento | Ajustar parámetros |
| Validación | Elegir arquitectura, regularización, umbrales y momento de parada |
| Prueba | Estimar el desempeño final una vez tomadas esas decisiones |

**Subajuste:** el modelo o el entrenamiento no capturan la estructura relevante. **Sobreajuste:** el modelo se adapta a particularidades del conjunto de entrenamiento que no se sostienen en datos nuevos. Más capacidad puede reducir el error de entrenamiento y aumentar la sensibilidad a qué muestras se usaron.

La curva en U de la diapositiva 14 ilustra un compromiso clásico entre sesgo y varianza; no es una ley universal que deba aparecer en toda red profunda. Una brecha grande entre entrenamiento y validación es una señal para investigar, no un diagnóstico suficiente por sí sola.

En clasificación, acertar mucho tampoco cuenta toda la historia: si casi todos los ejemplos son negativos, predecir siempre «negativo» puede dar una exactitud alta y detectar cero positivos. Necesitamos distinguir falsos positivos y falsos negativos; los formalizamos en la sección 9.

## 4. Del texto a la predicción del siguiente token

*Diapositivas 15–38.* El salto a los modelos de lenguaje mantiene el esquema de clasificación: hay una entrada, una representación aprendida y una distribución sobre posibles salidas. La clase que se predice es ahora un **token del vocabulario**.

### 4.1 Tokens y embeddings

Un token puede ser una palabra, un fragmento, un signo o una secuencia de bytes, según el tokenizador. El texto se transforma en identificadores discretos. Sus números identifican elementos del vocabulario: no expresan semejanza ni orden semántico.

Un **embedding** sustituye cada identificador por un vector aprendido. La tabla inicial asocia el mismo vector al mismo token; las capas siguientes generan representaciones que dependen del contexto. Así, las representaciones de «banco» pueden diferir entre una conversación sobre dinero y una sobre sentarse.

Los dibujos en dos dimensiones son proyecciones de un espacio de mayor dimensión. Cercanía y analogías como «rey − hombre + mujer ≈ reina» ilustran relaciones que pueden aparecer; no son identidades exactas ni garantizan que cada coordenada tenga un significado interpretable.

### 4.2 Autorregresión: completar y volver a completar

Para continuar «El perro persigue la», el modelo asigna probabilidades a los posibles siguientes tokens. Un procedimiento de decodificación elige uno, por ejemplo «pelota», lo añade al contexto y repite. El modelo no necesita producir una oración completa en una sola decisión.

En generación ordinaria se reutilizan los parámetros aprendidos. **Agregar un token al contexto no equivale a volver a entrenar la red.** En entrenamiento, el texto observado proporciona muchos pares «prefijo → siguiente token».

### 4.3 Atención: recuperar información del contexto

Una posición construye una consulta: qué información busca. Otras posiciones aportan claves para estimar compatibilidad y valores con información que mezclar. Los pesos de atención determinan cuánto contribuye cada valor a la representación resultante.

En «El perro mordió el hueso porque estaba hambriento», el contexto puede ayudar a relacionar «hambriento» con «perro». Es una motivación lingüística, no una garantía de que una cabeza concreta aprenda exactamente esa regla. Varias cabezas permiten mezclas distintas; sus funciones no se asignan manualmente.

### 4.4 Transformer y etapas de aprendizaje

El transformer combina atención, redes por posición, normalización y conexiones residuales. Un modelo causal impide que cada posición vea tokens futuros al predecir el siguiente. La sección 13 muestra un bloque simplificado y hace explícita esa restricción.

![Etapas de aprendizaje de un modelo de lenguaje](ia23-etapas-entrenamiento.svg)

**Autosupervisión:** las etiquetas se obtienen de los propios datos, por ejemplo ocultando qué token viene después. **Transferencia:** reutilizar lo aprendido para otra tarea. **Ajuste supervisado con instrucciones:** aprender de pares de consulta y respuesta deseada. **RLHF:** una etapa adicional posible que utiliza retroalimentación humana para orientar el comportamiento mediante una señal de recompensa. El ajuste con instrucciones y RLHF son procesos distinguibles; la diapositiva 37 los presenta juntos.

## Parte II. Formalización matemática

## 5. Una red profunda como composición

*Diapositivas 4–6 y 9–12; notación y derivación complementarias.* Para una observación usamos vectores columna. Sea $d_0$ la dimensión de entrada y $d_l$ la anchura de la capa $l$:

$$
\mathbf a^{(0)}=\mathbf x\in\mathbb R^{d_0},\qquad
\mathbf z^{(l)}=W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)},\qquad
\mathbf a^{(l)}=\phi_l\!\left(\mathbf z^{(l)}\right).
$$

Aquí $W^{(l)}\in\mathbb R^{d_l\times d_{l-1}}$, $\mathbf b^{(l)}\in\mathbb R^{d_l}$ y $\phi_l$ actúa componente a componente en las capas ocultas usuales. Los parámetros son $\theta=\{W^{(l)},\mathbf b^{(l)}\}_{l=1}^L$. La salida puede usar softmax, que acopla sus componentes.

Cada capa afín tiene $d_ld_{l-1}+d_l$ parámetros. Por ejemplo, una arquitectura $2\to3\to2$ tiene $(3\cdot2+3)+(2\cdot3+2)=17$ parámetros. Aquí contamos dos capas parametrizadas; no contamos la entrada. Distintas fuentes cuentan las capas de otra manera.

**Por qué necesitamos no linealidad.** Si omitimos las activaciones:

$$
W_2(W_1\mathbf x+\mathbf b_1)+\mathbf b_2
=\underbrace{W_2W_1}_{\widetilde W}\mathbf x
+\underbrace{W_2\mathbf b_1+\mathbf b_2}_{\widetilde{\mathbf b}}.
$$

La composición sigue siendo afín. Con activaciones no lineales podemos construir funciones que esa sola transformación no representa.

### 5.1 ReLU y softplus

La diapositiva 7 muestra ambas:

$$
\operatorname{ReLU}(z)=\max(0,z),\qquad
\operatorname{ReLU}'(z)=
\begin{cases}0,&z<0,\\1,&z>0.\end{cases}
$$

En $z=0$ ReLU no tiene derivada ordinaria; en implementación se adopta una convención, habitualmente cero. Para la alternativa suave:

$$
\operatorname{softplus}(z)=\log(1+e^z),\qquad
\operatorname{softplus}'(z)=\sigma(z)=\frac{1}{1+e^{-z}}.
$$

ReLU evita la saturación en la región positiva, pero **no garantiza** que el gradiente de toda la red no desaparezca o explote: también intervienen los pesos y las rutas de propagación. «Neurona muerta» suele indicar que una unidad permanece inactiva para las entradas relevantes; estar inactiva para una sola muestra no basta para llamarla muerta.

## 6. Softmax y entropía cruzada: de puntajes a una pérdida

*Diapositiva 3.* Para $K$ clases excluyentes, la última capa genera puntajes o *logits* $\mathbf z\in\mathbb R^K$:

$$
p_k=\operatorname{softmax}(\mathbf z)_k
=\frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}},\qquad
\sum_{k=1}^Kp_k=1.
$$

Si $\mathbf y$ es la etiqueta one-hot y $c$ la clase correcta:

$$
\ell(\mathbf z,\mathbf y)
=-\sum_{k=1}^Ky_k\log p_k
=-\log p_c
=\log\sum_{j=1}^Ke^{z_j}-z_c.
$$

Usamos logaritmos naturales. Una probabilidad mayor de la clase correcta produce menor pérdida. Para $\mathbf z=(2,1,0)$ obtenemos $\mathbf p\approx(0.6652,0.2447,0.0900)$; si la primera clase es correcta, $\ell\approx0.4076$.

**Estabilidad numérica.** Con $m=\max_jz_j$:

$$
\log\sum_je^{z_j}=m+\log\sum_je^{z_j-m},\qquad
p_k=\frac{e^{z_k-m}}{\sum_je^{z_j-m}}.
$$

Restar el máximo evita exponenciar números positivos enormes. Una implementación conjunta de log-softmax y entropía cruzada evita calcular de forma ingenua el logaritmo de una probabilidad que redondeó a cero.

**Gradiente que usaremos en backward.** La derivada de log-sum-exp respecto de $z_k$ es $p_k$, y la de $-\mathbf y^\mathsf T\mathbf z$ es $-y_k$. Por tanto:

$$
\boxed{\nabla_{\mathbf z}\ell=\mathbf p-\mathbf y.}
$$

> [!important] Alcance de la equivalencia con regresión logística
> Si $\mathbf z=W\mathbf x+\mathbf b$, tenemos regresión logística multinomial. Si $\mathbf z$ depende de capas ocultas no lineales, conservamos softmax y la misma pérdida en la salida, pero el modelo completo es una red neuronal, con una optimización generalmente no convexa.

Para $n$ ejemplos, un objetivo usual es $J(\theta)=\frac1n\sum_i\ell_i(\theta)+\lambda\Omega(\theta)$. La penalización $\Omega$ es un complemento de regularización; no forma parte obligatoria de la definición de softmax.

## 7. Retropropagación: aplicar la regla de la cadena eficientemente

*Diapositivas 9–12; derivación complementaria.* En una composición escalar $u=f(v)$, el gradiente que llega a $v$ es:

$$
\frac{\partial\ell}{\partial v}
=\frac{\partial\ell}{\partial u}\frac{\partial u}{\partial v}.
$$

Con vectores, si $\mathbf u=f(\mathbf v)$, usamos el producto del Jacobiano transpuesto por el gradiente entrante:

$$
\nabla_{\mathbf v}\ell=J_f(\mathbf v)^\mathsf T\nabla_{\mathbf u}\ell.
$$

Esto evita construir explícitamente grandes Jacobianos cuando podemos calcular el producto de manera directa. El forward conserva los valores intermedios que necesitarán las derivadas locales.

Para capas ocultas afines con activación componente a componente, definimos $\boldsymbol\delta^{(l)}=\partial\ell/\partial\mathbf z^{(l)}$. Si la salida es softmax con entropía cruzada:

$$
\boldsymbol\delta^{(L)}=\mathbf p-\mathbf y,
$$

$$
\boxed{
\boldsymbol\delta^{(l)}=
\left((W^{(l+1)})^\mathsf T\boldsymbol\delta^{(l+1)}\right)
\odot\phi_l'\!\left(\mathbf z^{(l)}\right)
},\qquad l=L-1,\ldots,1.
$$

El símbolo $\odot$ indica multiplicación componente a componente. Luego:

$$
\boxed{
\frac{\partial\ell}{\partial W^{(l)}}
=\boldsymbol\delta^{(l)}(\mathbf a^{(l-1)})^\mathsf T,
\qquad
\frac{\partial\ell}{\partial\mathbf b^{(l)}}=\boldsymbol\delta^{(l)}
}.
$$

**Comprobación de dimensiones:** $(d_l\times1)(1\times d_{l-1})$ produce la forma $d_l\times d_{l-1}$ de $W^{(l)}$. Si una variable o parámetro aparece en varios caminos del grafo, se **suman** sus contribuciones.

Para un mini-batch $B$, se promedian los gradientes de los ejemplos y se añade el término de regularización si existe. Descenso de gradiente actualiza:

$$
\theta\leftarrow\theta-\eta\widehat{\nabla_\theta J},\qquad \eta>0.
$$

Todos los gradientes de un paso se calculan con los mismos parámetros anteriores. Un paso demasiado grande puede aumentar la pérdida. Retropropagación no garantiza encontrar el mínimo global.

## 8. Un ejemplo completo: forward, backward y una actualización

**Ejemplo didáctico escalar con salida binaria**, elegido para poder revisar todas las cuentas. No es el experimento de una diapositiva. Usamos una unidad oculta ReLU y una sigmoide de salida:

$$
z_1=w_1x+b_1,\quad h=\operatorname{ReLU}(z_1),\quad
z_2=w_2h+b_2,\quad p=\sigma(z_2),
$$

$$
\ell=-y\log p-(1-y)\log(1-p).
$$

Tomamos $x=2$, $y=1$, $w_1=0.5$, $b_1=0.1$, $w_2=-1$, $b_2=0.2$.

### 8.1 Forward

$$
z_1=1.1,\quad h=1.1,\quad z_2=-0.9,\quad
p\approx0.2890505,\quad\ell\approx1.2411539.
$$

El modelo asigna poca probabilidad a la etiqueta correcta. Para sigmoide con entropía cruzada binaria, $\partial\ell/\partial z_2=p-y$:

### 8.2 Backward

$$
\delta_2\approx-0.7109495,\qquad
\frac{\partial\ell}{\partial w_2}=\delta_2h\approx-0.7820445,\qquad
\frac{\partial\ell}{\partial b_2}=\delta_2.
$$

Como $z_1>0$, la derivada de ReLU es uno:

$$
\delta_1=\delta_2w_2\cdot1\approx0.7109495,\qquad
\frac{\partial\ell}{\partial w_1}=\delta_1x\approx1.4218990,\qquad
\frac{\partial\ell}{\partial b_1}=\delta_1.
$$

### 8.3 Actualización y nueva predicción

Con $\eta=0.1$, y actualizando simultáneamente:

$$
w_1'\approx0.3578101,\quad b_1'\approx0.0289050,\quad
w_2'\approx-0.9217956,\quad b_2'\approx0.2710950.
$$

El nuevo forward da $p'\approx0.3976647$ y $\ell'\approx0.9221461$. La pérdida de **este ejemplo** disminuye; eso no demuestra una mejora en datos no vistos.

**Animación del cálculo.** Avanza una operación a la vez o reproduce un ciclo completo. Cambia a la unidad inactiva para ver que el gradiente hacia $w_1,b_1$ queda en cero mientras el sesgo de salida todavía puede aprender.

<iframe src="ia23-backprop.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Si el recurso no carga:** forward calcula valores, backward multiplica derivadas locales y la actualización resta los gradientes. Una ReLU negativa bloquea la contribución del ejemplo a los parámetros anteriores por esa ruta.

## 9. Evaluación: matriz de confusión, sesgo y varianza

*Diapositivas 13–14.* Fijemos cuál clase llamamos positiva:

| Real / Predicha | Negativa | Positiva |
|---|---:|---:|
| Negativa | $TN$: verdadero negativo | $FP$: falso positivo |
| Positiva | $FN$: falso negativo | $TP$: verdadero positivo |

$$
\begin{aligned}
\operatorname{exactitud}&=\frac{TP+TN}{TP+TN+FP+FN},\\
\operatorname{precision}&=\frac{TP}{TP+FP},\\
\operatorname{recall}=\operatorname{sensibilidad}&=\frac{TP}{TP+FN},\\
\operatorname{especificidad}&=\frac{TN}{TN+FP},\\
F_1&=\frac{2\,\operatorname{precision}\,\operatorname{recall}}
{\operatorname{precision}+\operatorname{recall}}
=\frac{2TP}{2TP+FP+FN}.
\end{aligned}
$$

«Precisión» traduce aquí *precision*, no *accuracy*. La tasa de falsos positivos es $FP/(TN+FP)$ y la de falsos negativos es $FN/(TP+FN)$. Si un denominador es cero, hay que explicitar la convención usada para reportar esa métrica.

**Ejemplo:** $TP=8$, $FP=2$, $FN=4$, $TN=86$. Exactitud $=94\%$, precisión $=80\%$, recall $\approx66.7\%$, especificidad $\approx97.7\%$ y $F_1\approx72.7\%$. Una exactitud alta convive con perder un tercio de los positivos. Cambiar el umbral puede cambiar estos valores sin volver a entrenar la red.

### 9.1 Una formalización del compromiso sesgo-varianza

**Complemento para regresión con pérdida cuadrática**, no una identidad automática para entropía cruzada. Supongamos $Y=f^*(x)+\varepsilon$, con ruido de media cero, varianza $\sigma_\varepsilon^2$ e independiente del conjunto de entrenamiento $D$. Para un $x$ fijo:

$$
\mathbb E_{D,\varepsilon}\left[(Y-\widehat f_D(x))^2\right]
=\underbrace{\left(\mathbb E_D[\widehat f_D(x)]-f^*(x)\right)^2}_{\text{sesgo}^2}
+\underbrace{\mathbb E_D\!\left[(\widehat f_D(x)-\mathbb E_D[\widehat f_D(x)])^2\right]}_{\text{varianza}}
+\underbrace{\sigma_\varepsilon^2}_{\text{ruido irreducible}}.
$$

El sesgo mide error sistemático del predictor promedio; la varianza, cuánto cambia al cambiar los datos de entrenamiento. Este «sesgo» estadístico no es el parámetro $\mathbf b$ de una capa. Regularización y parada temprana pueden ayudar a generalizar; sus decisiones se toman con validación, conservando prueba para la evaluación final.

## 10. Embeddings: de identificadores a vectores

*Diapositivas 18–24; notación complementaria.* Sea $V$ el tamaño del vocabulario y $d$ la dimensión del embedding. Para el identificador $t_i$, definimos una tabla aprendida $E\in\mathbb R^{V\times d}$:

$$
\mathbf e_i=E_{t_i,:},\qquad
H^{(0)}_{i,:}=\mathbf e_i+\mathbf r_i.
$$

Ahora usamos **filas para posiciones de la secuencia**: $H^{(0)}\in\mathbb R^{T\times d}$ y $\mathbf r_i$ representa información de posición en este esquema aditivo. Buscar una fila de $E$ equivale a multiplicar un vector one-hot por la tabla, pero no exige materializar ese vector enorme.

La similitud coseno entre dos vectores no nulos es:

$$
\operatorname{cos}(\mathbf u,\mathbf v)
=\frac{\mathbf u^\mathsf T\mathbf v}{\|\mathbf u\|\,\|\mathbf v\|}.
$$

Es una medida geométrica, no una probabilidad de que dos palabras signifiquen lo mismo. La tabla $E$ da embeddings iniciales; las capas producen estados contextuales $H^{(1)},\ldots,H^{(L)}$.

## 11. Autorregresión y objetivo autosupervisado

*Diapositivas 25–26 y 33–36.* La regla de la cadena de la probabilidad permite factorizar una secuencia:

$$
\boxed{p_\theta(t_1,\ldots,t_T)=\prod_{i=1}^T p_\theta(t_i\mid t_{<i}).}
$$

El prefijo vacío se puede representar con un símbolo de inicio. En cada posición, un estado contextual genera $V$ logits y softmax produce una distribución sobre el vocabulario. La pérdida de entrenamiento causal es:

$$
J_{\mathrm{LM}}(\theta)
=-\frac1N\sum_{\text{secuencias }s}\sum_{i\in\mathcal I_s}
\log p_\theta(t_i\mid t_{<i}),
$$

donde $\mathcal I_s$ contiene las posiciones objetivo válidas y $N=\sum_s|\mathcal I_s|$. Las posiciones de relleno se excluyen. Cada token observado funciona como etiqueta, por eso no necesitamos que alguien etiquete manualmente cada siguiente token.

**Entrenamiento y generación difieren.** Durante el entrenamiento conocemos la secuencia y usamos los prefijos reales (*teacher forcing*). Una máscara causal permite calcular muchas predicciones en paralelo sin revelar el futuro a cada posición. Durante la generación, cada token nuevo depende de los ya elegidos.

Podemos elegir el máximo de la distribución (*greedy*) o muestrear. Con temperatura $\tau>0$, $p_j^{(\tau)}\propto e^{z_j/\tau}$; una temperatura baja concentra la distribución. La regla de decodificación es distinta del entrenamiento y de los pesos de atención.

**Animación de autorregresión.** Observa cómo una decisión amplía el prefijo y cambia la distribución siguiente. Las probabilidades son inventadas para la explicación; no provienen de un modelo entrenado. El laboratorio usa elección greedy y termina con un token de fin.

<iframe src="ia23-autorregresion.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Si el recurso no carga:** prefijo → distribución de siguiente token → elección → concatenación → nuevo prefijo. Los parámetros permanecen fijos durante esta demostración.

## 12. Autoatención: consultas, claves, valores y máscara causal

*Diapositivas 27–30; ecuaciones complementarias.* Con $H\in\mathbb R^{T\times d}$ y una cabeza:

$$
Q=HW_Q,\qquad K=HW_K,\qquad V_{\!a}=HW_V,
$$

$$
Q,K\in\mathbb R^{T\times d_k},\qquad V_{\!a}\in\mathbb R^{T\times d_v}.
$$

Usamos $V_{\!a}$ para los valores de atención y reservamos $V$ sin subíndice para el tamaño del vocabulario. El puntaje entre consulta $i$ y clave $j$ es $s_{ij}=\mathbf q_i^\mathsf T\mathbf k_j/\sqrt{d_k}$. La atención causal se calcula como:

$$
M_{ij}=\begin{cases}0,&j\le i,\\-\infty,&j>i,\end{cases}
\qquad
A=\operatorname{softmax}_{\text{por fila}}\left(\frac{QK^\mathsf T}{\sqrt{d_k}}+M\right),
\qquad O=AV_{\!a}.
$$

Para cada posición $i$, $o_i=\sum_{j\le i}\alpha_{ij}v_j$. Cada fila de $A$ suma uno; las posiciones futuras tienen peso cero. La posición $i$ puede verse a sí misma porque su salida predice $t_{i+1}$, que todavía no se le muestra.

El escalamiento por $\sqrt{d_k}$ controla la magnitud de los puntajes. Las claves determinan compatibilidad; los valores son lo que se mezcla. En varias cabezas, cada una usa sus propias proyecciones; se concatenan las salidas y se aplica una proyección $W_O$. Estas operaciones y la máscara se describen en [Vaswani et al., secciones 3.2–3.3](https://arxiv.org/html/1706.03762v7#S3.SS2).

### 12.1 Cuenta mínima de una fila

Sean $d_k=2$, $q=(1,0)$ y tres claves $k_1=(1,0)$, $k_2=(0,1)$, $k_3=(1,1)$. Si consultamos desde la **segunda** posición:

$$
\mathbf s=(1/\sqrt2,\;0,\;1/\sqrt2),\qquad
\mathbf s+\mathbf m=(1/\sqrt2,\;0,\;-\infty),
$$

$$
\boldsymbol\alpha\approx(0.6698,\;0.3302,\;0).
$$

Con $v_1=(1,0)$ y $v_2=(0,1)$, la salida es $o\approx(0.6698,0.3302)$. Aunque $k_3$ fuera compatible, la máscara impide usar información futura.

**Animación de atención causal.** El laboratorio usa un conjunto propio de vectores pequeños, mostrado dentro del recurso. Selecciona una posición y reproduce: puntajes → máscara → softmax → mezcla. No es una visualización de pesos aprendidos por un LLM real.

<iframe src="ia23-atencion-causal.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Si el recurso no carga:** la consulta puntúa las claves; la máscara elimina el futuro antes de softmax; los pesos normalizados mezclan valores. Estos pesos intermedios no son las probabilidades finales del siguiente token.

## 13. Un bloque transformer causal

*Diapositivas 31–32.* Este esquema didáctico muestra una variante **pre-LayerNorm** de un modelo solo decodificador. Omite dropout. Es coherente con el orden de normalización de la figura de la diapositiva 31; no intenta representar todas las variantes de transformer.

![Transformer causal con bloque pre-LayerNorm simplificado](ia23-transformer-causal.svg)

$$
\widetilde H=H+\operatorname{MHA}_{\mathrm{causal}}(\operatorname{LN}(H)),
\qquad
H'=\widetilde H+\operatorname{FFN}(\operatorname{LN}(\widetilde H)).
$$

La FFN aplica la misma red a cada posición por separado; por ejemplo, con ReLU:

$$
\operatorname{FFN}(U)=\operatorname{ReLU}(UW_1+\mathbf b_1)W_2+\mathbf b_2.
$$

Las sumas residuales conservan un camino directo para la información y el gradiente. La normalización actúa sobre las características de cada posición. Tras apilar bloques, una proyección al vocabulario y softmax producen probabilidades. El artículo original de 2017 presenta un transformer **codificador-decodificador** y usa normalización después de la suma residual; no es exactamente el bloque dibujado aquí. [Vaswani et al., sección 3.1](https://arxiv.org/html/1706.03762v7#S3.SS1).

**Conexión con el principio del apunte:** la atención mezcla información entre posiciones; la FFN transforma características en cada posición; las capas repetidas construyen representaciones cada vez más útiles para la predicción.

## 14. Preentrenamiento, transferencia, instrucciones y RLHF

*Diapositivas 33–38.* Son decisiones sobre datos y objetivos de aprendizaje, no nombres de capas:

| Etapa | Señal de aprendizaje | Qué se ajusta |
|---|---|---|
| Preentrenamiento autosupervisado | Objetivos derivados de datos, como siguiente token | Representaciones y parámetros del modelo |
| Transferencia a otra tarea | Etiquetas u objetivos de la nueva tarea | Una cabeza nueva, parte del modelo o todo el modelo |
| Ajuste supervisado con instrucciones, SFT | Consulta y respuesta deseada | Probabilidad de respuestas de demostración |
| RLHF, cuando se usa | Recompensa relacionada con preferencias humanas | Política generadora de respuestas |

Para SFT, una pérdida usual suma entropías cruzadas sobre los tokens de la respuesta $y$, condicionados por la consulta $x$ y la respuesta previa. Puede enmascararse la consulta para que solo los tokens de respuesta contribuyan a la pérdida.

**RLHF como MDP**, siguiendo la simplificación de la diapositiva 38:

$$
s_t=(\text{consulta},t_1,\ldots,t_{t-1}),\qquad
a_t=t_t,\qquad
s_{t+1}=s_t\mathbin{\|}a_t,\qquad
\pi_\theta(a_t\mid s_t)=p_\theta(t_t\mid s_t).
$$

La transición concatena un token; un objetivo idealizado es $\max_\theta\mathbb E_{\pi_\theta}[\sum_t\gamma^tr_t]$. La recompensa puede llegar al final de la respuesta; no hace falta una calificación humana para cada token generado.

La diapositiva usa calificaciones $+1/-1$ como simplificación. En el procedimiento de InstructGPT se distinguen demostraciones supervisadas, comparaciones de respuestas para entrenar un modelo de recompensa y optimización posterior de la política. **SFT no requiere por sí mismo aprendizaje por refuerzo.** [Ouyang et al., *Training language models to follow instructions with human feedback*](https://arxiv.org/abs/2203.02155).

El dato de población de la UNAM de la diapositiva 37 sirve como ejemplo de formato de respuesta; no lo tomamos como una cifra vigente ni como contenido factual que deba memorizarse.

**Conexión previa:** [[2026-11-05 IA - Aprendizaje por refuerzo II|políticas, recompensas y aproximación de funciones]]. En lenguaje, la política elige tokens y la red comparte parámetros entre muchísimos prefijos.

## Comprobaciones para estudiar

1. ¿Por qué cinco capas afines sin activación pueden reducirse a una sola?
   > [!check]- Respuesta
   > La composición de transformaciones afines sigue siendo afín. Cambia la parametrización, pero no crea por sí sola una función no lineal de la entrada.

2. Una ReLU recibió un valor negativo. ¿Qué pasa con el gradiente de ese ejemplo hacia su entrada?
   > [!check]- Respuesta
   > Es cero por esa ruta. Eso no demuestra que la unidad esté inactiva para todos los ejemplos ni que los parámetros posteriores no puedan aprender.

3. ¿Cuál es la diferencia entre retropropagación y descenso de gradiente?
   > [!check]- Respuesta
   > La primera calcula derivadas de la pérdida; el segundo utiliza esas derivadas para actualizar parámetros.

4. Si $\mathbf p=(0.7,0.2,0.1)$ y la clase correcta es la segunda, ¿cuál es el gradiente respecto de los logits?
   > [!check]- Respuesta
   > $\mathbf p-\mathbf y=(0.7,-0.8,0.1)$. La pérdida es $-\log(0.2)\approx1.6094$.

5. En el ejemplo de la sección 8, ¿por qué disminuye $w_1$ aunque la etiqueta correcta sea uno?
   > [!check]- Respuesta
   > Porque $w_2$ es negativo: disminuir la activación oculta puede aumentar el logit de salida. El signo del cambio depende de toda la ruta, no solo de la etiqueta.

6. Si hay 99 negativos y un positivo, ¿qué obtiene el clasificador que siempre predice negativo?
   > [!check]- Respuesta
   > Exactitud del 99 % y recall de la clase positiva de 0 %. Su precisión positiva tiene denominador cero y requiere una convención de reporte.

7. ¿Los pesos de atención son las probabilidades del siguiente token?
   > [!check]- Respuesta
   > No. Normalizan contribuciones de posiciones del contexto. Las probabilidades de salida se calculan después, sobre el vocabulario.

8. ¿Por qué la diagonal de la máscara causal está permitida?
   > [!check]- Respuesta
   > La representación de la posición $i$ puede usar el token $t_i$ para predecir $t_{i+1}$. Lo que se oculta es el futuro respecto de esa posición.

9. ¿Qué proporciona las etiquetas en la predicción autosupervisada del siguiente token?
   > [!check]- Respuesta
   > El propio texto: se desplazan los objetivos una posición respecto de la entrada, respetando la máscara causal y excluyendo relleno.

10. ¿Generar un token, hacer SFT y hacer RLHF cambian el modelo de la misma manera?
    > [!check]- Respuesta
    > Generar usa los parámetros y amplía el contexto; SFT ajusta parámetros con demostraciones; RLHF puede ajustarlos para aumentar una recompensa vinculada a preferencias.

## Práctica breve

- [ ] Recalcular el forward y los cuatro gradientes de la sección 8 sin consultar el resultado.
- [ ] Explicar qué cambia si $z_1<0$ y verificarlo en la animación.
- [ ] Dibujar una máscara causal de $4\times4$ y marcar qué representación predice cada siguiente token.
- [ ] Calcular precisión y recall al aumentar un falso positivo o un falso negativo en el ejemplo de la sección 9.
- [ ] Explicar en voz alta la cadena: tokenización → embeddings → contexto → logits → softmax → siguiente token.

## Material y fuentes

- **Fuente principal:** [[AI 23 Aprendizaje profundo.pdf|presentación de la clase, 39 diapositivas]]. Las referencias numéricas del apunte corresponden a páginas del PDF.
- **Ampliación de atención y arquitectura:** Vaswani et al. (2017), [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762). Se distingue su arquitectura original del bloque causal pre-LN ilustrado aquí.
- **Ampliación de SFT y RLHF:** Ouyang et al. (2022), [*Training language models to follow instructions with human feedback*](https://arxiv.org/abs/2203.02155).
- Los cuatro diagramas y las tres animaciones son elaboraciones para este apunte. Los números de los laboratorios son ejemplos controlados, no mediciones de modelos comerciales.

> [!abstract] Idea para recordar
> Profundidad aprende representaciones; retropropagación conecta cada parámetro con una pérdida; validación comprueba si lo aprendido se sostiene fuera del entrenamiento. En lenguaje, los tokens se convierten en vectores, la atención incorpora contexto y una salida softmax permite repetir la decisión del siguiente token.
