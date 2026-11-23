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

**Martes 10 de noviembre de 2026.** Apunte **autocontenido** sobre aprendizaje profundo: cada figura se describe y se redibuja, y cada cálculo se desarrolla completo. El plan de la materia llama a esta sesión «Redes neuronales»; el tema se amplía a modelos de lenguaje.

> [!summary] La idea que conecta toda la clase
> Una red profunda transforma sus entradas mediante varias etapas aprendidas. La retropropagación calcula cómo cambiar cada parámetro para reducir un error. En un modelo de lenguaje, estas transformaciones convierten tokens en representaciones contextuales y, finalmente, en probabilidades para el siguiente token.

**Cómo estudiar el apunte.** Lee primero la parte I, que construye la intuición sin depender de las ecuaciones. Después recorre la parte II para formalizar cada mecanismo. Las derivaciones, los ejemplos numéricos y los recursos interactivos son **complementos didácticos**, no resultados experimentales. Los laboratorios funcionan sin conexión y están incrustados junto al concepto correspondiente.

| Recorrido | Dónde se desarrolla |
|---|---|
| Softmax, profundidad y ReLU | 1 y 5–6 |
| Grafos computacionales, forward y backward | 2 y 7–8 |
| Evaluación, sesgo y varianza | 3 y 9 |
| Tokens, embeddings y autorregresión | 4 y 10–11 |
| Autoatención y transformer | 4 y 12–13 |
| Autosupervisión, transferencia, ajuste y RLHF | 4 y 14 |

## Parte I. Construir la intuición

## 1. Profundidad: aprender a describir antes de decidir

Imagina que queremos reconocer un objeto en una imagen. Una decisión directa a partir de todos los píxeles puede ser difícil. Podemos construir representaciones intermedias: combinaciones locales de píxeles, patrones, partes y, finalmente, evidencia para una clase. **Cada etapa vuelve a expresar la información de una forma útil para la siguiente.**

![Profundidad: transformar la representación antes de decidir](ia23-representaciones.svg)

**Ejemplo de cadena de etapas para clasificar imágenes.** Cuatro bloques consecutivos: detección de líneas y esquinas (Linear + ReLU), detección de formas (Linear + ReLU), detección de objetos (Linear + ReLU) y detección de clase (Linear + Softmax); a la salida se compara con el objetivo mediante una pérdida. La entrada son los datos y el objetivo es la etiqueta. Una red profunda general es simplemente una cadena más larga de pares Linear–nodo no lineal (cuatro en el esquema típico) seguida de la pérdida.

**Dos modelos de referencia previos.** (a) Regresión logística multinomial: Linear → Softmax → entropía cruzada, con tres grupos de puntos (rojo, verde y azul) separados por tres fronteras lineales que se encuentran en un punto. (b) Red de dos capas: Linear → Sigmoide → Linear → Softmax → entropía cruzada, aplicada a cuatro grupos de puntos en configuración tipo XOR: azules en las esquinas superior izquierda (cerca de $(-5,5)$) e inferior derecha (cerca de $(5,-5)$) y rojos en la superior derecha $(5,5)$ e inferior izquierda $(-5,-5)$; ninguna recta los separa, pero la capa oculta sí lo permite.

En una red profunda no tenemos que escribir manualmente todos esos detectores: el entrenamiento ajusta las transformaciones. La jerarquía de bordes, formas y objetos es una **intuición ilustrativa**; una capa real no tiene obligatoriamente una interpretación humana tan limpia.

Una capa realiza una combinación ponderada de sus entradas y aplica una activación. La combinación decide qué información reunir; la activación permite respuestas no lineales. Si solo encadenáramos transformaciones afines, muchas capas se podrían reducir a una sola. Tener más operaciones no bastaría para aumentar ese tipo de capacidad expresiva.

**Propiedades de ReLU y softplus.** $f_{\mathrm{relu}}(x)=\max(0,x)$ y $f_{\mathrm{sp}}(x)=\log(1+e^x)$. La gráfica de ReLU es cero para $x<0$ y la recta $y=x$ para $x>0$ (alcanza 10 en $x=10$); softplus la suaviza cerca de cero. ReLU es de las más usadas, sus derivadas no desaparecen en la región positiva, algunas neuronas pueden «morir» y técnicamente no es diferenciable en 0.

**ReLU como compuerta.** Deja pasar una entrada positiva y convierte una negativa en cero. En su región positiva no comprime progresivamente la señal como una sigmoide saturada. Sin embargo, una unidad que permanezca en la región negativa puede dejar de recibir gradiente por esa ruta: es la intuición de una neurona «muerta».

**Profundidad y anchura.** La profundidad cuenta etapas sucesivas; la anchura, unidades o características dentro de una etapa. No hay un número universal de capas que garantice buen aprendizaje. Hace unas dos décadas se solía añadir solo una capa sobre el modelo de regresión logística, con el foco puesto en optimización convexa y con pocos datos. Esa comparación histórica entre redes poco profundas y profundas es contexto, no una regla que prohíba redes profundas antes de cierta fecha. Una red con capas ocultas no lineales suele producir un problema de optimización no convexo.

**Conexión previa:** [[2026-10-27 IA - Aprendizaje supervisado y clasificacion|clasificación, XOR y redes neuronales]]. La capa oculta cambia la representación para que una decisión antes difícil se vuelva más sencilla.

## 2. Aprender: predecir, medir el error y repartir responsabilidades

Entrenar una red tiene tres acciones distintas:

1. **Forward:** pasar la entrada por las operaciones hasta obtener una predicción y una pérdida.
2. **Backward o retropropagación:** recorrer las dependencias en sentido inverso para saber cuánto influye cada parámetro en la pérdida.
3. **Actualización:** usar esos gradientes para cambiar los parámetros, por ejemplo con descenso de gradiente.

![Forward, backward y actualización son tres operaciones distintas](ia23-grafo-gradientes.svg)

La pérdida es un número que resume qué tan mala fue una predicción según el objetivo elegido. El gradiente indica cómo cambiaría ese número ante pequeñas variaciones de los parámetros. **Retropropagación calcula gradientes; el optimizador decide cómo usarlos.**

El grafo computacional registra operaciones y dependencias. Si una variable alimenta dos caminos que llegan a la pérdida, su influencia total reúne las contribuciones de ambos. No se «manda hacia atrás la respuesta correcta»: se propaga sensibilidad de la pérdida mediante la regla de la cadena.

Cada módulo de la red necesita tres funciones: **forward** (calcula $f(\mathbf x)$), **backward** (recibe el gradiente de la salida y devuelve el de la entrada) y su **derivada**, el Jacobiano $J_{\mathbf x}f(\mathbf x)$. Gráficamente, un nodo tiene una flecha de entrada y una de salida en el pase hacia adelante y las mismas con sentido contrario en el pase hacia atrás. En el grafo computacional, nodos de datos y de parámetros (varias entradas por cada operación) alimentan una cadena de operaciones que se bifurca y vuelve a unirse hasta una única pérdida. Para una capa $f$ con entrada $\mathbf x$ y parámetros $\theta$, el backward produce la derivada de la pérdida respecto de la salida de la capa, respecto de sus parámetros ($dL/d\theta$) y respecto de su entrada.

La composición de funciones puede ser secuencial, recursiva o en red. La misma idea se aplica a cadenas, bifurcaciones y parámetros compartidos. Una recurrencia se puede desplegar en el tiempo para formar el grafo que se diferencia.

## 3. Una pérdida baja no basta: evaluar fuera del entrenamiento

Memorizar los ejemplos observados no garantiza acertar en ejemplos nuevos. Distinguimos tres conjuntos:

| Conjunto | Para qué se usa |
|---|---|
| Entrenamiento | Ajustar parámetros |
| Validación | Elegir arquitectura, regularización, umbrales y momento de parada |
| Prueba | Estimar el desempeño final una vez tomadas esas decisiones |

**Subajuste:** el modelo o el entrenamiento no capturan la estructura relevante. **Sobreajuste:** el modelo se adapta a particularidades del conjunto de entrenamiento que no se sostienen en datos nuevos. Más capacidad puede reducir el error de entrenamiento y aumentar la sensibilidad a qué muestras se usaron.

La curva en U del error de validación frente a la complejidad ilustra un compromiso clásico entre sesgo y varianza; no es una ley universal que deba aparecer en toda red profunda. Una brecha grande entre entrenamiento y validación es una señal para investigar, no un diagnóstico suficiente por sí sola.

En clasificación, acertar mucho tampoco cuenta toda la historia: si casi todos los ejemplos son negativos, predecir siempre «negativo» puede dar una exactitud alta y detectar cero positivos. Necesitamos distinguir falsos positivos y falsos negativos; los formalizamos en la sección 9.

El diagnóstico de sesgo y varianza se suele ilustrar con dos gráficas. En la primera, el error de predicción (eje vertical, de 0 a 1.2) frente a la complejidad del modelo (grados de libertad, de 0 a 35): decenas de curvas azules de entrenamiento descienden de forma continua y su promedio llega cerca de 0.1, mientras que las curvas rojas de prueba descienden primero, alcanzan un mínimo cercano a 0.45–0.5 hacia 10–15 grados de libertad y luego suben. A la izquierda hay alto sesgo y baja varianza; a la derecha, bajo sesgo y alta varianza. En la segunda gráfica, flexibilidad (baja a alta) frente a interpretabilidad (baja a alta): de más interpretables y menos flexibles a menos interpretables y más flexibles aparecen selección de subconjuntos y lasso, mínimos cuadrados, modelos aditivos generalizados y árboles, bagging y boosting, máquinas de vectores de soporte y, por último, aprendizaje profundo.

## 4. Del texto a la predicción del siguiente token

El salto a los modelos de lenguaje mantiene el esquema de clasificación: hay una entrada, una representación aprendida y una distribución sobre posibles salidas. La clase que se predice es ahora un **token del vocabulario**.

### 4.1 Tokens y embeddings

Un token puede ser una palabra, un fragmento, un signo o una secuencia de bytes, según el tokenizador. Como ejemplo con un tokenizador de la familia GPT-3.5/GPT-4, el texto en inglés «Many words map to one token, but some don't: indivisible.» más «Unicode characters like emojis may be split into many tokens containing the underlying bytes:» (seguido de varios símbolos de bytes), más «Sequences of characters commonly found next to each other may be grouped together: 1234567890» (252 caracteres) se convierte en **57 tokens**: la mayoría de las palabras comunes (con su espacio previo) son un token, las palabras raras como «indivisible» se parten en fragmentos, los símbolos de bytes del emoji se dividen en varios tokens y los dígitos de «1234567890» se agrupan en trozos. Su lista de identificadores es:

`[8607, 4339, 2472, 311, 832, 4037, 11, 719, 1063, 1541, 956, 25, 3687, 23936, 382, 35020, 5885, 1093, 100166, 1253, 387, 6859, 1139, 1690, 11460, 8649, 279, 16940, 5943, 25, 11410, 97, 248, 9468, 237, 122, 271, 1542, 45045, 315, 5885, 17037, 1766, 1828, 311, 1855, 1023, 1253, 387, 41141, 3871, 25, 220, 4513, 10961, 16474, 15]`

Nótese que una misma palabra con el mismo espacio previo repite el identificador (por ejemplo 311, 5885, 1253 y 387 aparecen más de una vez) y que un emoji puede ocupar varios identificadores. El texto se transforma en identificadores discretos. Sus números identifican elementos del vocabulario: no expresan semejanza ni orden semántico.

**Flujo completo del ejemplo.** Entrada «The», « dog», « chased», « the» → tokenizar → identificadores one-hot $[791]$, $[5679]$, $[62920]$, $[279]$ → *embed* → un vector por token → la red *predice* un vector de salida → *un-embed* → identificador $[5041]$ → *un-tokenize* → « ball».

Un **embedding** sustituye cada identificador por un vector aprendido. La tabla inicial asocia el mismo vector al mismo token; las capas siguientes generan representaciones que dependen del contexto. Así, las representaciones de «banco» pueden diferir entre una conversación sobre dinero y una sobre sentarse.

Dos figuras ilustran esto. En un mapa bidimensional de embeddings, las palabras de transporte y lugares (train, bus, car, college, school, work) quedan juntas en la zona superior derecha; las preposiciones (on, in, with) cerca de ellas; los verbos de movimiento (walk, swim, run, go) en el centro; y los pronombres y funcionales (I, we, they, the, by, to) en la zona inferior izquierda. En un mapa de calor de vectores de características (valores de 0 a 1), las filas de «sea» y «ocean» tienen patrones casi iguales, igual que «football» y «soccer», y «I» y «we», mientras que las de grupos distintos difieren. La analogía clásica de Mikolov et al. (2013) es $\text{king}-\text{man}+\text{woman}\approx\text{queen}$: restar «man» a «king» da un vector de «realeza», que sumado a «woman» llega cerca de «queen».

Los dibujos en dos dimensiones son proyecciones de un espacio de mayor dimensión. Cercanía y analogías como «rey − hombre + mujer ≈ reina» ilustran relaciones que pueden aparecer; no son identidades exactas ni garantizan que cada coordenada tenga un significado interpretable.

### 4.2 Autorregresión: completar y volver a completar

Para continuar «El perro persigue la», el modelo asigna probabilidades a los posibles siguientes tokens. Un procedimiento de decodificación elige uno, por ejemplo «pelota», lo añade al contexto y repite. El modelo no necesita producir una oración completa en una sola decisión. Esquemáticamente, la misma red se aplica en cuatro pasos sucesivos: con «The» (y relleno) predice «dog»; con «The dog» predice «chased»; con «The dog chased» predice «the»; con «The dog chased the» predice «ball»; en cada paso la salida se concatena al contexto y se vuelve a alimentar.

En generación ordinaria se reutilizan los parámetros aprendidos. **Agregar un token al contexto no equivale a volver a entrenar la red.** En entrenamiento, el texto observado proporciona muchos pares «prefijo → siguiente token».

### 4.3 Atención: recuperar información del contexto

Una posición construye una consulta: qué información busca. Otras posiciones aportan claves para estimar compatibilidad y valores con información que mezclar. Los pesos de atención determinan cuánto contribuye cada valor a la representación resultante.

En «The dog chewed the bone because it was hungry», el contexto puede ayudar a relacionar «it» con «dog» (la atención de «it» se concentra sobre «dog» y, en menor grado, sobre «chewed» y «hungry»). Si la oración termina en «delicious», la atención de «it» se desplaza hacia «bone». En la versión en español, «El perro mordió el hueso porque estaba hambriento», «hambriento» se relaciona con «perro». Es una motivación lingüística, no una garantía de que una cabeza concreta aprenda exactamente esa regla. Varias cabezas permiten mezclas distintas; sus funciones no se asignan manualmente. Por ejemplo, una cabeza puede atender a la palabra previa y otra a referencias de pronombres.

Una figura típica de autoatención con seis entradas $x_1,\ldots,x_6$ muestra que la última posición ($x_6$) no condiciona por igual en todas las anteriores: con peso uniforme todas las flechas son iguales; con atención, solo algunas posiciones (por ejemplo $x_2$, $x_3$ y $x_5$) pesan más. En el esquema de una cabeza, cada entrada $x_i$ pasa por tres perceptrones multicapa que producen $k_i$, $q_i$ y $v_i$; los puntajes $s_i$ se forman con productos punto de consultas y claves; «normalizar y softmax» produce los pesos $a_i$; y la suma ponderada de los valores da la salida $x'$. La versión de varias cabezas replica ese bloque con parámetros propios, concatena las salidas $z_1,z_2,z_3$ y las pasa por un MLP.

### 4.4 Transformer y etapas de aprendizaje

El transformer combina atención, redes por posición, normalización y conexiones residuales. Un bloque transformer apila, de entrada a salida: normalización (LayerNorm), atención multicabeza, otra normalización y un MLP; el modelo completo repite $N$ bloques entre las etapas Tokenizar → Embed (entrada «The dog chased the») y Un-embed → Un-tokenize (salida «ball»). Un modelo causal impide que cada posición vea tokens futuros al predecir el siguiente. La sección 13 muestra un bloque simplificado y hace explícita esa restricción.

![Etapas de aprendizaje de un modelo de lenguaje](ia23-etapas-entrenamiento.svg)

Como ilustración de transferencia, un mismo modelo preentrenado procesa un texto y puede responder a la tarea 1 (predecir la siguiente palabra) o a la tarea 2 (predecir el sentimiento) cambiando solo el cabezal final. Otro ejemplo de autosupervisión en imágenes: se oculta un recuadro de una fachada (aparece en blanco) y la red lo rellena con contenido plausible a partir del contexto.

**Autosupervisión:** las etiquetas se obtienen de los propios datos, por ejemplo ocultando qué token viene después. **Transferencia:** reutilizar lo aprendido para otra tarea. **Ajuste supervisado con instrucciones:** aprender de pares de consulta y respuesta deseada. **RLHF:** una etapa adicional posible que utiliza retroalimentación humana para orientar el comportamiento mediante una señal de recompensa. El ajuste con instrucciones y RLHF son procesos distinguibles, aunque a menudo se presentan juntos.

## Parte II. Formalización matemática

## 5. Una red profunda como composición

*Notación y derivación complementarias.* Para una observación usamos vectores columna. Sea $d_0$ la dimensión de entrada y $d_l$ la anchura de la capa $l$:

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

Estas son las dos activaciones más comunes:

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

Para $K$ clases excluyentes, la última capa genera puntajes o *logits* $\mathbf z\in\mathbb R^K$:

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

*Derivación complementaria.* En una composición escalar $u=f(v)$, el gradiente que llega a $v$ es:

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

**Ejemplo didáctico escalar con salida binaria**, elegido para poder revisar todas las cuentas. Usamos una unidad oculta ReLU y una sigmoide de salida:

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

Fijemos cuál clase llamamos positiva:

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

La matriz de confusión tiene como filas la clase real (0, 1) y como columnas la predicha (0, 1): $TN$ y $TP$ son los aciertos (diagonal), $FP$ es el error tipo I y $FN$ el error tipo II. A su lado se leen: especificidad $=TN/(TN+FP)$ (fila real 0), recall o sensibilidad $=TP/(TP+FN)$ (fila real 1), precisión $=TP/(TP+FP)$ (columna predicha 1) y tasa negativa (valor predictivo negativo) $=TN/(FN+TN)$ (columna predicha 0).

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

*Notación complementaria.* Sea $V$ el tamaño del vocabulario y $d$ la dimensión del embedding. Para el identificador $t_i$, definimos una tabla aprendida $E\in\mathbb R^{V\times d}$:

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

La regla de la cadena de la probabilidad permite factorizar una secuencia:

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

*Ecuaciones complementarias.* Con $H\in\mathbb R^{T\times d}$ y una cabeza:

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

Este esquema didáctico muestra una variante **pre-LayerNorm** de un modelo solo decodificador. Omite dropout. No intenta representar todas las variantes de transformer.

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

Son decisiones sobre datos y objetivos de aprendizaje, no nombres de capas:

| Etapa | Señal de aprendizaje | Qué se ajusta |
|---|---|---|
| Preentrenamiento autosupervisado | Objetivos derivados de datos, como predecir la siguiente palabra, la palabra faltante o si dos imágenes están relacionadas | Representaciones y parámetros del modelo |
| Transferencia a otra tarea | Etiquetas u objetivos de la nueva tarea | Una cabeza nueva, parte del modelo o todo el modelo |
| Ajuste supervisado con instrucciones, SFT | Consulta y respuesta deseada | Probabilidad de respuestas de demostración |
| RLHF, cuando se usa | Recompensa relacionada con preferencias humanas | Política generadora de respuestas |

Para SFT, una pérdida usual suma entropías cruzadas sobre los tokens de la respuesta $y$, condicionados por la consulta $x$ y la respuesta previa. Puede enmascararse la consulta para que solo los tokens de respuesta contribuyan a la pérdida.

**RLHF como MDP**, en una formulación simplificada:

$$
s_t=(\text{consulta},t_1,\ldots,t_{t-1}),\qquad
a_t=t_t,\qquad
s_{t+1}=s_t\mathbin{\|}a_t,\qquad
\pi_\theta(a_t\mid s_t)=p_\theta(t_t\mid s_t).
$$

La transición concatena un token; un objetivo idealizado es $\max_\theta\mathbb E_{\pi_\theta}[\sum_t\gamma^tr_t]$. La recompensa puede llegar al final de la respuesta; no hace falta una calificación humana para cada token generado.

Una simplificación común usa calificaciones $+1/-1$ (los humanos califican la respuesta con $+1$ o $-1$). En el procedimiento de InstructGPT se distinguen demostraciones supervisadas, comparaciones de respuestas para entrenar un modelo de recompensa y optimización posterior de la política. **SFT no requiere por sí mismo aprendizaje por refuerzo.** [Ouyang et al., *Training language models to follow instructions with human feedback*](https://arxiv.org/abs/2203.02155).

Ejemplo de las dos tareas con la consulta «¿Cuál es la población de la UNAM?». Tarea 1 (predecir la siguiente palabra): una continuación posible es «Esa pregunta siempre me ha fascinado», plausible como texto pero inútil. Tarea 2 (generar texto útil): «Son 356,530 según Wikipedia». El ajuste se hace con ejemplos útiles de conversaciones humanas. Este ejemplo de consulta y respuesta sirve para ilustrar el formato de las respuestas; no debe tomarse como una cifra vigente ni como contenido factual que deba memorizarse.

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

- **Ampliación de atención y arquitectura:** Vaswani et al. (2017), [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762). Se distingue su arquitectura original del bloque causal pre-LN ilustrado aquí.
- **Ampliación de SFT y RLHF:** Ouyang et al. (2022), [*Training language models to follow instructions with human feedback*](https://arxiv.org/abs/2203.02155).
- Los cuatro diagramas y las tres animaciones son elaboraciones para este apunte. Los números de los laboratorios son ejemplos controlados, no mediciones de modelos comerciales.

> [!abstract] Idea para recordar
> Profundidad aprende representaciones; retropropagación conecta cada parámetro con una pérdida; validación comprueba si lo aprendido se sostiene fuera del entrenamiento. En lenguaje, los tokens se convierten en vectores, la atención incorpora contexto y una salida softmax permite repetir la decisión del siguiente token.
