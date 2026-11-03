---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-06"
unidad: Razonamiento probabilístico y redes bayesianas
profesor: Carlos Hernández
estado: procesada
conceptos:
  - Red bayesiana
  - Tabla de probabilidad condicional
  - Factorización de la distribución conjunta
  - Independencia condicional
  - Propiedad de Markov local
  - D-separación
  - Colisionador
  - Explicación alternativa
  - Manto de Markov
referencias:
  - "[[AI 14 Redes Bayesianas independencia.pdf]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/d-separation.html"
  - "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/resources/readings/"
tags:
  - clase
  - inteligencia-artificial
  - redes-bayesianas
  - independencia-condicional
  - d-separacion
---

# Redes bayesianas: independencia y d-separación

> [!summary] Pregunta central
> ¿Cómo podemos saber, mirando un grafo, cuándo una observación vuelve irrelevante otra variable y cuándo, por el contrario, crea una relación entre variables que antes eran independientes?

Continuación de [[2026-09-29 IA - Agentes-probabilisticos|la introducción a agentes probabilísticos]]. El eje de esta clase es **leer las independencias que garantiza una estructura de red bayesiana**. Las probabilidades numéricas ayudan a entender las reglas; la inferencia general queda como puente hacia la siguiente sesión.

La presentación se titula «Clase 16: redes Bayesianas independencia», aunque el archivo se llama «AI 14». Se conserva la fecha del apunte existente, **6 de octubre**; el índice distingue la planeación del curso del material desarrollado.

![[AI 14 Redes Bayesianas independencia.pdf]]

## Ruta de estudio y relación con las diapositivas

| Paso | Idea que debemos dominar | Diapositivas | Sección |
|---|---|---|---|
| 1 | Qué representa una red y cómo recupera la conjunta | 6–9, 12–15 | §§1–2 |
| 2 | Independencia marginal, condicional y supuestos locales | 10–11, 16–18 | §§3–4 |
| 3 | Cadena, causa común y efecto común | 19–22 | §§5–6 |
| 4 | Caminos activos y d-separación | 23–26 | §7 |
| 5 | Resolver los tres ejemplos completos | 27–29 | §8 |
| 6 | Comprender las restricciones de la topología | 30–31 | §10 |
| Ampliación | Ejemplo del MIT y conexión con AIMA | Complemento | §§9 y 11 |

**Fuentes de apoyo.** AIMA significa *Artificial Intelligence: A Modern Approach*, de Russell y Norvig: utilizamos la 4.ª edición global que ya está en el vault, §§13.1–13.2.1. Berkeley CS 188 organiza los patrones y las consultas gráficas; MIT 6.034 aporta el ejemplo de causas alternativas de un ladrido. Las derivaciones, números didácticos y diagramas recreados se identifican en cada sección.

## 1. Una red bayesiana es un grafo más distribuciones locales

*Diapositivas 7–9 y 13–15.* Una **red bayesiana** contiene:

1. Un grafo dirigido acíclico, o **DAG**, con un nodo por variable aleatoria.
2. El dominio de cada variable.
3. Una distribución $P(X_i\mid\operatorname{Pa}(X_i))$ por nodo. Para variables discretas se representa mediante una **tabla de probabilidad condicional**, CPT.

Una raíz no tiene padres y necesita una distribución previa $P(X_i)$. Para cualquier configuración de los padres, las probabilidades de todos los valores del hijo suman 1.

Si el orden $X_1,\ldots,X_n$ es **topológico** —los padres aparecen antes que sus hijos—, la regla de la cadena siempre permite escribir:

$$P(x_1,\ldots,x_n)=\prod_{i=1}^{n}P(x_i\mid x_1,\ldots,x_{i-1}).$$

La red agrega supuestos de independencia que permiten reemplazar todos los predecesores por los padres:

$$P(x_i\mid x_1,\ldots,x_{i-1})=P(x_i\mid\operatorname{pa}(X_i)).$$

Por tanto, la distribución representada es:

$$\boxed{P(x_1,\ldots,x_n)=\prod_{i=1}^{n}P(x_i\mid\operatorname{pa}(X_i)).}$$

Aquí $\operatorname{Pa}(X_i)$ es el conjunto de variables padre y $\operatorname{pa}(X_i)$ sus valores en la asignación concreta.

> [!important] Qué significa una flecha
> Las flechas participan en la factorización y en las garantías de independencia. Por sí solas **no demuestran causalidad**, ni obligan a que exista dependencia numérica para todas las CPT. Una interpretación causal requiere supuestos adicionales sobre el proceso que genera los datos.

Esta descripción coincide con [Berkeley CS 188, §6.3](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/representation.html) y con AIMA, §13.2, pp. 432–438 de la edición global.

### Ejemplo 1: lluvia, tráfico y paraguas

*Diapositiva 12; desarrollo numérico didáctico.* $R$: llueve; $T$: hay tráfico; $U$: una persona lleva paraguas. Suponemos que, una vez conocida la lluvia, saber si hay tráfico no aporta información adicional sobre el paraguas.

![[ia14-lluvia-trafico-paraguas.svg]]

**Paso 1.** La regla de la cadena, sin ninguna independencia, da:

$$P(r,t,u)=P(r)P(t\mid r)P(u\mid r,t).$$

**Paso 2.** La estructura afirma $U\perp T\mid R$, de modo que:

$$P(u\mid r,t)=P(u\mid r).$$

**Paso 3.** La representación se simplifica:

$$P(r,t,u)=P(r)P(t\mid r)P(u\mid r).$$

**Paso 4.** Con $P(r)=0.3$, $P(t\mid r)=0.8$ y $P(u\mid r)=0.9$:

$$P(r,t,u)=0.3(0.8)(0.9)=0.216.$$

Este producto corresponde a **una asignación completa**, «llueve, hay tráfico y lleva paraguas». Para obtener una marginal tendríamos que sumar las asignaciones de las variables que no interesan. El grafo no garantiza $T\perp U$ sin conocer $R$: ambos pueden aportar información sobre la lluvia.

## 2. La red de alarma: construir una probabilidad desde cinco tablas

*Diapositiva 6; AIMA, figura 13.2.* Usamos $B$: robo, $E$: terremoto, $A$: alarma, $J$: John llama y $M$: Mary llama. Todas son booleanas. Una letra minúscula, como $b$, abrevia el evento $B=\mathrm{true}$; $\neg b$ significa $B=\mathrm{false}$.

![[ia14-red-alarma.svg]]

### Paso 1: leer los padres

Las raíces son $B$ y $E$; $\operatorname{Pa}(A)=\{B,E\}$; $\operatorname{Pa}(J)=\operatorname{Pa}(M)=\{A\}$. La conjunta es:

$$P(B,E,A,J,M)=P(B)P(E)P(A\mid B,E)P(J\mid A)P(M\mid A).$$

### Paso 2: leer las CPT de la diapositiva

$$P(b)=0.001,\qquad P(e)=0.002.$$

| $B$ | $E$ | $P(a\mid B,E)$ |
|---|---|---:|
| Verdadero | Verdadero | 0.95 |
| Verdadero | Falso | 0.94 |
| Falso | Verdadero | 0.29 |
| Falso | Falso | 0.001 |

| $A$ | $P(j\mid A)$ | $P(m\mid A)$ |
|---|---:|---:|
| Verdadero | 0.90 | 0.70 |
| Falso | 0.05 | 0.01 |

Cada probabilidad del valor falso es el complemento de la correspondiente entrada. Por ejemplo, $P(\neg m\mid a)=0.30$.

### Paso 3: elegir un mundo y multiplicar

Queremos que suene la alarma y llamen ambos, sin robo ni terremoto:

$$\begin{aligned}
P(\neg b,\neg e,a,j,m)
&=P(\neg b)P(\neg e)P(a\mid\neg b,\neg e)P(j\mid a)P(m\mid a)\\
&=(0.999)(0.998)(0.001)(0.90)(0.70)\\
&=0.00062811126.
\end{aligned}$$

No debemos multiplicar $P(j)$ y $P(m)$: las tablas disponibles son las probabilidades **condicionadas a la alarma**.

### Paso 4: distinguir una conjunta de una posterior

Como anticipo de inferencia, una consulta diferente es «¿hubo robo, dado que ambos llaman?»:

$$P(b\mid j,m)=\frac{\displaystyle\sum_{e,a}P(b,e,a,j,m)}{\displaystyle\sum_{b',e,a}P(b',e,a,j,m)}.$$

Para cada valor $b'$ del robo, definimos $q_{b'}=P(a\mid b')$ sumando el terremoto:

$$q_b=(0.002)(0.95)+(0.998)(0.94)=0.94002,$$
$$q_{\neg b}=(0.002)(0.29)+(0.998)(0.001)=0.001578.$$

Ahora sumamos los dos valores de la alarma. Si suena, la probabilidad de ambas llamadas es $0.90(0.70)=0.63$; si no suena, es $0.05(0.01)=0.0005$. Los pesos conjuntos son:

$$\begin{aligned}
w_b&=0.001\,[0.63q_b+0.0005(1-q_b)]\\
&=0.00059224259,\\
w_{\neg b}&=0.999\,[0.63q_{\neg b}+0.0005(1-q_{\neg b})]\\
&=0.001491857649.
\end{aligned}$$

Normalizamos:

$$P(b\mid j,m)=\frac{w_b}{w_b+w_{\neg b}}\approx0.284172.$$

La probabilidad previa era 0.1 % y la posterior es aproximadamente 28.42 %. Las llamadas son evidencia de robo a través de la alarma; el cálculo conserva las explicaciones alternativas y los falsos positivos.

### Laboratorio: inspeccionar los factores y las sumas

<iframe src="red-bayesiana-alarma-interactiva.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Selecciona **«Ambos llaman»** y compara los dos pesos con el cálculo anterior. Después elige **«Suena la alarma»** y **«Alarma y terremoto»**: obtendrás $P(b\mid a)\approx0.373551$ y $P(b\mid a,e)\approx0.003268$. Conocer un terremoto ofrece otra explicación para la alarma y reduce la creencia en robo. Aunque el recurso se creó para el apunte anterior, sus CPT coinciden con la diapositiva 6 de esta clase.

## 3. Independencia marginal y condicional: dos preguntas distintas

*Diapositivas 10–11.* Para variables discretas:

$$X\perp Y\quad\Longleftrightarrow\quad P(x,y)=P(x)P(y)\quad\text{para todo }x,y.$$

Cuando $P(y)>0$, equivale a $P(x\mid y)=P(x)$: conocer $Y$ no cambia la distribución de $X$.

La independencia condicional es:

$$X\perp Y\mid Z\quad\Longleftrightarrow\quad P(x,y\mid z)=P(x\mid z)P(y\mid z),$$

para todos los valores $x,y,z$ con $P(z)>0$. Equivalentemente, $P(x\mid y,z)=P(x\mid z)$ cuando el condicionamiento tiene probabilidad positiva.

La expresión se refiere a **todos los valores posibles de $Z$**, no solamente a un valor observado en un ejemplo. Tampoco basta una coincidencia para una sola entrada de una tabla para demostrar independencia de las variables.

> [!important] Condicionar puede quitar o crear dependencia
> De $X\perp Y$ no se deduce $X\perp Y\mid Z$. De $X\perp Y\mid Z$ tampoco se deduce $X\perp Y$. Los tres patrones gráficos mostrarán ambas situaciones.

### Fuego, humo y alarma: primero decidir qué modelo estamos suponiendo

La diapositiva 11 plantea el escenario sin fijar una única estructura. Dos modelos razonables son:

![[ia29-fuego-humo-alarma.svg]]

- **El fuego produce humo y activa un detector térmico:** $H\leftarrow F\rightarrow A$. La hipótesis es $H\perp A\mid F$.
- **Un detector de humo activa la alarma:** $F\rightarrow H\rightarrow A$. La hipótesis es $F\perp A\mid H$.

En ambos modelos puede haber asociación entre los extremos sin evidencia, pero **se condiciona una variable diferente**. Para escoger el grafo hacen falta detalles del mecanismo o supuestos del modelo. Si el fuego puede activar directamente la alarma además de hacerlo a través del humo, habría que considerar también $F\rightarrow A$ y se perdería la segunda garantía.

## 4. Independencias locales y conexiones indirectas

*Diapositivas 16–18; AIMA, §13.2.1.* La **propiedad de Markov local** establece que cada variable es independiente de sus otros no descendientes dados sus padres:

$$X_i\perp\bigl(\operatorname{NoDesc}(X_i)\setminus\operatorname{Pa}(X_i)\bigr)\mid\operatorname{Pa}(X_i).$$

Un descendiente es un nodo al que podemos llegar siguiendo flechas desde $X_i$. Aquí «otros no descendientes» excluye también al propio nodo. La afirmación se hace sobre el conjunto completo, no únicamente sobre cada variable por separado.

### Ejemplo 2: la cadena de cuatro nodos de la diapositiva 17

![[ia14-cadena-cuatro.svg]]

**Paso 1.** Aplicamos la regla de la cadena en el orden $X,Y,Z,W$:

$$P(x,y,z,w)=P(x)P(y\mid x)P(z\mid x,y)P(w\mid x,y,z).$$

**Paso 2.** Las hipótesis locales son $Z\perp X\mid Y$ y $W\perp\{X,Y\}\mid Z$.

**Paso 3.** Sustituimos:

$$P(x,y,z,w)=P(x)P(y\mid x)P(z\mid y)P(w\mid z).$$

**Paso 4.** Buscamos consecuencias adicionales. También se garantiza $X\perp W\mid Y$ y $X\perp W\mid Z$: cualquiera de esos nodos intermedios bloquea el único camino. Son consecuencias globales que veremos sistemáticamente con d-separación.

**Paso 5.** Evitamos una conclusión falsa: la ausencia de la arista $X\rightarrow Z$ **no** garantiza $X\perp Z$. Todavía existe el camino indirecto $X\rightarrow Y\rightarrow Z$.

## 5. Dos patrones que se bloquean al observar el nodo central

*Diapositivas 19–21.* Cada camino largo se estudia mediante tripletas consecutivas. Primero entendemos dos casos donde el nodo central **no recibe las dos puntas de flecha del camino**.

### 5.1 Cadena: $X\rightarrow Y\rightarrow Z$

En el ejemplo de la diapositiva 20, $X$ es baja presión, $Y$ lluvia y $Z$ tráfico.

![[ia14-cadena-presion.svg]]

**Paso 1: factorizar.** $P(x,y,z)=P(x)P(y\mid x)P(z\mid y)$.

**Paso 2: observar el medio.** Al fijar $Y=y$, la red deja de necesitar $X$ para predecir $Z$:

$$\begin{aligned}
P(z\mid x,y)
&=\frac{P(x)P(y\mid x)P(z\mid y)}{P(x)P(y\mid x)}\\
&=P(z\mid y).
\end{aligned}$$

Por tanto, $\boxed{X\perp Z\mid Y}$. La igualdad se aplica donde el denominador es positivo.

**Paso 3: comprobar por qué no hay garantía marginal.** Elegimos números didácticos:

$$P(x)=0.5,\quad P(y\mid x)=0.8,\quad P(y\mid\neg x)=0.2,$$
$$P(z\mid y)=0.9,\qquad P(z\mid\neg y)=0.1.$$

Sin observar $Y$, debemos sumar sus valores:

$$P(z\mid x)=0.8(0.9)+0.2(0.1)=0.74,$$
$$P(z\mid\neg x)=0.2(0.9)+0.8(0.1)=0.26.$$

Como son diferentes, en esta distribución $X$ y $Z$ son dependientes. Pero, si sabemos que llueve, $P(z\mid x,y)=P(z\mid\neg x,y)=0.9$.

**Regla:** una cadena está activa si el nodo central no se observa y bloqueada si se observa. También se aplica al recorrerla en sentido inverso: $X\leftarrow Y\leftarrow Z$.

### 5.2 Causa común o bifurcación: $X\leftarrow Y\rightarrow Z$

En la diapositiva 21, $Y$ es la proximidad de una entrega, $X$ un foro activo y $Z$ un laboratorio lleno.

![[ia14-causa-comun.svg]]

**Paso 1: factorizar.** $P(x,y,z)=P(y)P(x\mid y)P(z\mid y)$.

**Paso 2: condicionar.** Dividimos por $P(y)$:

$$P(x,z\mid y)=P(x\mid y)P(z\mid y).$$

Esto demuestra $\boxed{X\perp Z\mid Y}$.

**Paso 3: ver la asociación al desconocer la causa.** Para una versión didáctica, usamos:

$$P(y)=0.2,\quad P(x\mid y)=0.9,\quad P(x\mid\neg y)=0.1,$$
$$P(z\mid y)=0.8,\qquad P(z\mid\neg y)=0.2.$$

Entonces:

$$P(x)=0.2(0.9)+0.8(0.1)=0.26,$$
$$P(z)=0.2(0.8)+0.8(0.2)=0.32,$$
$$P(x,z)=0.2(0.9)(0.8)+0.8(0.1)(0.2)=0.16.$$

Pero $P(x)P(z)=0.0832\ne0.16$. Por ello, ver el foro activo cambia la probabilidad de encontrar lleno el laboratorio:

$$P(z\mid x)=\frac{0.16}{0.26}\approx0.615385\ne0.32.$$

Al conocer la entrega, ese aporte informativo desaparece: $P(z\mid x,y)=P(z\mid y)=0.8$.

**Regla:** una causa común sigue la misma regla de bloqueo que la cadena. Observar su nodo central bloquea el camino.

## 6. Efecto común: observar puede abrir un camino

*Diapositiva 22.* El tercer patrón invierte la regla anterior:

$$R\rightarrow T\leftarrow B.$$

$R$ es lluvia, $B$ un partido y $T$ tráfico. El nodo $T$ es un **colisionador** porque recibe las dos puntas de flecha **en este camino**. Añadimos el reporte $T'$ para anticipar la diapositiva 27.

![[ia14-efecto-comun.svg]]

### Paso 1: demostrar la independencia sin observar el efecto

Para la tripleta aislada:

$$P(r,b,t)=P(r)P(b)P(t\mid r,b).$$

Al marginalizar el tráfico:

$$\begin{aligned}
P(r,b)&=P(r)P(b)\sum_tP(t\mid r,b)\\
&=P(r)P(b).
\end{aligned}$$

Por tanto, $\boxed{R\perp B}$. El descendiente $T'$ no cambia esta conclusión mientras se mantenga sin observar: al sumarlo, su distribución condicional suma 1.

### Paso 2: construir un contraejemplo al observar el efecto

**Modelo didáctico deliberadamente simple:** $P(r)=P(b)=0.5$ y hay tráfico exactamente cuando llueve o hay partido, $T=R\lor B$.

| $R$ | $B$ | $T$ | Probabilidad conjunta |
|---|---|---|---:|
| Falso | Falso | Falso | 0.25 |
| Falso | Verdadero | Verdadero | 0.25 |
| Verdadero | Falso | Verdadero | 0.25 |
| Verdadero | Verdadero | Verdadero | 0.25 |

Al observar tráfico sobreviven tres mundos equiprobables:

$$P(b\mid t)=\frac{2}{3}.$$

Si además sabemos que llueve, el tráfico ya está explicado y el partido conserva su previa:

$$P(b\mid t,r)=\frac{1}{2}.$$

Si sabemos que **no** llueve, el partido es la única explicación dentro de este modelo:

$$P(b\mid t,\neg r)=1.$$

Estas probabilidades distintas prueban que, para esta CPT, $R$ y $B$ son dependientes dado $T$. Se suele llamar **explicación alternativa** o *explaining away*: una explicación conocida reduce la necesidad de otra. El sentido y la intensidad de la asociación dependen de la CPT; d-separación no los calcula.

### Paso 3: observar un descendiente también abre el colisionador

Si el reporte $T'$ informa sobre $T$, observarlo también puede relacionar lluvia y partido, aunque no observemos el tráfico directamente. La regla gráfica es:

$$\boxed{\text{Un colisionador se activa si se observa él o alguno de sus descendientes.}}$$

Esto retira la garantía de independencia incluso si una CPT particular hace que el reporte sea poco informativo o completamente independiente del tráfico. La garantía se decide por la estructura; la relación efectiva depende de los parámetros.

> [!note] El rol depende del camino
> En $R\rightarrow T\leftarrow B$, $T$ es colisionador. En $R\rightarrow T\rightarrow T'$, ese mismo nodo $T$ es un no colisionador. Por eso observarlo abre el primer camino y bloquea el segundo.

## 7. D-separación: combinar las reglas sin perder caminos

*Diapositivas 23–26.* Dadas variables $X,Y$ y un conjunto de evidencia $\mathcal E$, buscamos si la estructura obliga a que $X\perp Y\mid\mathcal E$. Suponemos que los extremos consultados no pertenecen a la evidencia.

Un **camino** se obtiene recorriendo aristas sin exigir seguir su dirección, pero **conservando las puntas de flecha** para clasificar cada tripleta. Por ejemplo, en $L\rightarrow R\rightarrow T\leftarrow B$, podemos recorrer de $L$ a $B$ aunque la última arista apunte desde $B$.

| Patrón en el camino | Nodo central sin observar | Nodo central observado |
|---|---|---|
| Cadena $X\rightarrow Y\rightarrow Z$ | Activo | Bloqueado |
| Causa común $X\leftarrow Y\rightarrow Z$ | Activo | Bloqueado |
| Colisionador $X\rightarrow Y\leftarrow Z$ | Bloqueado si tampoco se observa un descendiente | Activo |

En la última fila, **observar un descendiente de $Y$ también activa la tripleta**, aunque $Y$ permanezca sin observar. En las dos primeras, observar solamente un descendiente no sustituye a observar el nodo central.

### Procedimiento manual

1. Escribir los extremos y el conjunto exacto de evidencia.
2. Marcar las variables observadas; tanto un valor verdadero como uno falso cuentan como observación.
3. Enumerar todos los caminos simples entre los extremos, ignorando la dirección para recorrerlos.
4. En cada camino, revisar los nodos internos: ¿reciben las dos puntas de flecha de ese camino?
5. Un no colisionador bloquea si está observado. Un colisionador bloquea si ni él ni ningún descendiente están observados.
6. Un camino está activo solamente si **todos** sus nodos internos permiten el paso.
7. Si **todos los caminos** están bloqueados, hay d-separación y la independencia está garantizada. Un solo camino activo basta para que la garantía desaparezca.

Una arista directa no tiene nodos internos que podamos bloquear mediante evidencia en otros nodos. Dos componentes desconectados no tienen caminos que revisar y están d-separados sin evidencia.

> [!warning] Dos precisiones sobre las diapositivas
> En la diapositiva 24, el «intento 1» contiene una inversión en la frase sobre nodos conectados; es un intento provisional y no debe memorizarse como regla. Además, sombrear y quitar todos los nodos observados falla ante colisionadores: observarlos puede abrir caminos. En la diapositiva 26, la conclusión rigurosa cuando hay un camino activo es **«independencia no garantizada por el grafo»**; afirmar dependencia de una distribución concreta requiere revisar sus CPT o construir un contraejemplo.

### Explorador: de una tripleta a los tres ejemplos de clase

<iframe src="ia14-d-separacion-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Recorre primero cadena, causa común y efecto común. Después selecciona los ejemplos 2 y 3: el explorador enumera los caminos y explica cada bloqueo. En el ejemplo 3 compara **sin evidencia → observar $R$ → observar $R$ y $S$**: primero hay un camino activo, después ninguno y finalmente vuelve a abrirse uno. El grafo y las reglas siguen siendo suficientes para entender esta transición si el recurso no carga.

La secuencia por tripletas se apoya en [Berkeley CS 188, §6.5](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/d-separation.html). Enumerar todos los caminos sirve para practicar en estos grafos pequeños; para redes grandes existen procedimientos más eficientes.

## 8. Los tres ejemplos de las diapositivas, resueltos paso a paso

### 8.1 Ejemplo 1: un colisionador y su descendiente

*Diapositiva 27.* La red es $R\rightarrow T\leftarrow B$, $T\rightarrow T'$. **$T'$ es otra variable**, por ejemplo un reporte posterior de tráfico; no es la negación de $T$.

![[ia14-efecto-comun.svg]]

Solo hay un camino simple entre $R$ y $B$: $R\rightarrow T\leftarrow B$.

| Consulta | Análisis del único camino | ¿Independencia garantizada? |
|---|---|---|
| $R\perp B$ | $T$ es colisionador sin evidencia propia ni descendiente | Sí |
| $R\perp B\mid T$ | Se observa el colisionador $T$ y se abre | No |
| $R\perp B\mid T'$ | El descendiente observado $T'$ abre $T$ | No |

Para $R\perp T'\mid T$, el camino relevante cambia a $R\rightarrow T\rightarrow T'$. Ahora $T$ es un no colisionador observado, así que queda bloqueado y **sí se garantiza independencia**. La función de un nodo se decide en el camino que estamos analizando.

### 8.2 Ejemplo 2: abrir un colisionador no elimina otros bloqueos

*Diapositiva 28.* Las aristas son $L\rightarrow R$, $R\rightarrow D$, $R\rightarrow T$, $B\rightarrow T$ y $T\rightarrow T'$.

![[ia14-ejemplo2.svg]]

Para recordar el escenario, $L$ puede representar baja presión; $R$, lluvia; $D$, goteo; $B$, partido; $T$, tráfico; y $T'$, su reporte. La solución depende de las flechas, no de esos nombres.

**Consulta 1: $L\perp T'\mid T$.**

1. El único camino es $L\rightarrow R\rightarrow T\rightarrow T'$.
2. $R$ y $T$ son no colisionadores en ese camino.
3. $T$ está observado, por lo que bloquea.
4. **Sí se garantiza independencia.**

**Consultas 2–4: relación entre $L$ y $B$.** El único camino simple es $L\rightarrow R\rightarrow T\leftarrow B$. $R$ es un no colisionador y $T$ un colisionador.

| Evidencia | Estado de $R$ | Estado de $T$ | Resultado |
|---|---|---|---|
| Ninguna | Deja pasar | Bloquea | $L\perp B$ garantizada |
| $T$ | Deja pasar | Abierto por observación directa | Independencia no garantizada |
| $T'$ | Deja pasar | Abierto por descendiente observado | Independencia no garantizada |

**Consulta 5: $L\perp B\mid T,R$.**

1. Observar $T$ abre el colisionador.
2. Observar $R$ bloquea la tripleta $L\rightarrow R\rightarrow T$.
3. El camino completo permanece bloqueado: basta un bloqueo.
4. **Sí se garantiza independencia.**

La rama $R\rightarrow D$ no genera un segundo camino simple hacia $B$. No debemos inventar recorridos que vuelvan al mismo nodo para «rodear» un bloqueo.

### 8.3 Ejemplo 3: dos caminos y evidencia que cambia la respuesta

*Diapositiva 29.* $R$: lluvia; $T$: tráfico; $D$: goteo del techo; $S$: tristeza. La conjunta es:

$$P(r,t,d,s)=P(r)P(t\mid r)P(d\mid r)P(s\mid t,d).$$

![[ia14-ejemplo3-dos-caminos.svg]]

Entre $T$ y $D$ hay exactamente dos caminos simples:

- **Superior:** $T\leftarrow R\rightarrow D$, una causa común.
- **Inferior:** $T\rightarrow S\leftarrow D$, un efecto común.

| Consulta | Camino por $R$ | Camino por $S$ | ¿Independencia garantizada? |
|---|---|---|---|
| $T\perp D$ | Activo: causa común no observada | Bloqueado: colisionador no observado | No |
| $T\perp D\mid R$ | Bloqueado por $R$ observado | Bloqueado por $S$ no observado | Sí |
| $T\perp D\mid R,S$ | Bloqueado por $R$ observado | Activo por $S$ observado | No |

**Lectura paso a paso.** Sin evidencia, tráfico y goteo pueden informar sobre la misma lluvia. Al conocer la lluvia, el camino superior se bloquea y no hay otro activo. Pero si además sabemos que la persona está triste, tráfico y goteo vuelven a ser posibles explicaciones alternativas de ese efecto; el camino inferior se abre.

> [!important] Más evidencia no conserva necesariamente la independencia
> $T\perp D\mid R$ no permite concluir $T\perp D\mid R,S$. Agregar condiciones puede abrir un colisionador. Siempre hay que repetir el análisis con el conjunto de evidencia completo.

## 9. Complemento MIT 6.034: perro, ladrón y mapache

Las [*Probabilistic Inference Notes* de Patrick Winston, pp. 1–2](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/3e6200ca84af05d95712045abedce9e9_MIT6_034F10_bayes.pdf) comienzan con 1000 observaciones de un perro, un ladrón y un mapache. Retomamos sus conteos y desarrollamos las consultas para ilustrar un colisionador.

![[ia14-mit-perro-mapache.svg]]

En esta sección $B$: ladrón, $R$: mapache y $D$: perro ladra. Las letras se reutilizan respecto del ejemplo anterior, pero **representan otras variables**.

| $D$ ladra | $B$ ladrón | $R$ mapache | Conteo |
|---|---|---|---:|
| Falso | Falso | Falso | 405 |
| Falso | Falso | Verdadero | 225 |
| Falso | Verdadero | Falso | 0 |
| Falso | Verdadero | Verdadero | 0 |
| Verdadero | Falso | Falso | 45 |
| Verdadero | Falso | Verdadero | 225 |
| Verdadero | Verdadero | Falso | 50 |
| Verdadero | Verdadero | Verdadero | 50 |

### Paso 1: verificar las previas y la independencia

$$P(b)=\frac{100}{1000}=0.1,\quad P(r)=\frac{500}{1000}=0.5,$$
$$P(b,r)=\frac{50}{1000}=0.05=P(b)P(r).$$

Las otras combinaciones de las dos causas tienen probabilidades $0.05,0.45,0.45$, correspondientes a $(b,\neg r)$, $(\neg b,r)$ y $(\neg b,\neg r)$. Todas coinciden con el producto de sus marginales. Así, esta tabla es compatible con las raíces independientes del grafo $B\rightarrow D\leftarrow R$.

### Paso 2: recuperar la CPT del ladrido

$$P(d\mid b,r)=P(d\mid b,\neg r)=1,$$
$$P(d\mid\neg b,r)=\frac{225}{225+225}=0.5,$$
$$P(d\mid\neg b,\neg r)=\frac{45}{405+45}=0.1.$$

Ahora podemos reconstruir cualquier fila como $P(b)P(r)P(d\mid b,r)$. Por ejemplo, $P(\neg b,\neg r,\neg d)=0.9(0.5)(0.9)=0.405$.

### Paso 3: escuchar el ladrido y actualizar el mapache

Hay $45+225+50+50=370$ ladridos, de los cuales $225+50=275$ ocurren con mapache:

$$P(r\mid d)=\frac{275}{370}\approx0.743243.$$

La observación aumenta la probabilidad de mapache de 50 % a 74.32 %.

### Paso 4: agregar una causa conocida y comprobar la dependencia

Si además sabemos que había un ladrón:

$$P(r\mid d,b)=\frac{50}{50+50}=0.5.$$

Como $0.5\ne0.743243$, el mapache y el ladrón **son dependientes dado el ladrido en esta distribución**. El ladrón ya explica el ladrido y reduce la necesidad de atribuirlo al mapache. Aquí tenemos tanto la explicación gráfica como una comprobación numérica.

**Conexión con la clase:** es el mismo patrón que robo → alarma ← terremoto y lluvia → tráfico ← partido. Cambian el escenario y las CPT; la regla del colisionador permanece.

## 10. Lo que la topología garantiza y lo que los parámetros agregan

*Diapositivas 18 y 30–31.* Debemos distinguir dos afirmaciones:

$$X\text{ e }Y\text{ d-separados por }\mathcal E\quad\Longrightarrow\quad X\perp Y\mid\mathcal E$$

en **toda distribución que factorice según ese grafo**.

Si existe un camino activo, la estructura deja de obligar a la independencia. Puede haber CPT que generen dependencia y otras que produzcan independencia adicional. No necesitamos el supuesto de fidelidad para concluir independencia por d-separación; sí necesitaríamos condiciones adicionales para identificar siempre caminos activos con dependencias de una distribución concreta.

### Un contraejemplo muestra la diferencia

Para la estructura $X\rightarrow Y\rightarrow Z$, tomemos $X$ como una moneda justa:

- Si $Y=X$ y $Z=Y$, los extremos coinciden siempre. $P(X=1,Z=1)=0.5$, pero $P(X=1)P(Z=1)=0.25$: son dependientes.
- Si cada CPT asigna probabilidad $0.5$ al valor verdadero, con independencia del valor de sus padres, los tres nodos resultan mutuamente independientes. Las aristas siguen presentes, pero esas CPT no usan la información de sus padres.

Ambos modelos respetan la factorización de la cadena. Por ello, **«no garantizada»** es la respuesta general correcta para la independencia marginal de sus extremos.

### Cuántos parámetros ahorramos

Si la variable $X_i$ tiene $r_i$ valores y sus padres tienen $q_i$ configuraciones, una CPT sin restricciones adicionales necesita $(r_i-1)q_i$ parámetros libres. El total es:

$$N_{\mathrm{BN}}=\sum_i(r_i-1)\prod_{X_j\in\operatorname{Pa}(X_i)}r_j.$$

Para $n$ variables booleanas con a lo sumo $k$ padres, son a lo sumo $n2^k$ parámetros. La conjunta sin restricciones necesita $2^n-1$.

| Representación de cinco variables booleanas | Parámetros libres |
|---|---:|
| Conjunta sin restricciones | $2^5-1=31$ |
| Cadena de cinco nodos | $1+2+2+2+2=9$ |
| Red de alarma | $1+1+4+2+2=10$ |
| DAG completo en un orden topológico | $1+2+4+8+16=31$ |

Los números cuentan **parámetros libres**, no todas las entradas de tablas con ambos valores del hijo. Una fila booleana solo necesita un número porque el otro es su complemento.

Agregar una arista que preserve la aciclicidad permite representar al menos las distribuciones anteriores —basta hacer que la CPT ignore al nuevo padre— y puede permitir otras nuevas. El costo es una tabla mayor. Un DAG completo en un orden topológico puede representar cualquier distribución discreta sobre esas variables, pero pierde el ahorro general de la estructura escasa. Si una configuración de padres tiene probabilidad cero, su fila puede definirse arbitrariamente sin cambiar la conjunta.

## 11. Ampliación AIMA: manto de Markov y otra forma de verificar d-separación

Estos dos resultados proceden de AIMA, §13.2.1, pp. 436–438. Amplían las diapositivas sin ser requisitos para resolver sus tres ejemplos.

### 11.1 Manto de Markov

El **manto de Markov** de un nodo contiene sus padres, sus hijos y los otros padres de sus hijos. Dado ese conjunto, el nodo es independiente de los demás nodos de la red.

En la red de alarma:

- $\operatorname{MB}(B)=\{A,E\}$: su hijo $A$ y el otro padre de ese hijo, $E$. Por ello, $B\perp\{J,M\}\mid A,E$.
- $\operatorname{MB}(J)=\{A\}$: conocida la alarma, John es independiente de $B,E,M$ en este modelo.

**Por qué aparece el otro padre.** Observar el hijo $A$ abre el colisionador $B\rightarrow A\leftarrow E$. Por eso no basta una lista universal formada solo por padres e hijos: los otros padres de los hijos también forman parte del manto.

La propiedad local y el manto de Markov se presentan también en [Berkeley CS 188, §6.4](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/structure.html).

### 11.2 Método del subgrafo ancestral y moralización

Para consultar $X\perp Y\mid\mathcal E$ también podemos:

1. Conservar solo $X,Y,\mathcal E$ y todos sus ancestros.
2. Conectar entre sí a los padres que comparten un hijo: **moralizar**.
3. Convertir las aristas en no dirigidas.
4. Quitar los nodos de evidencia. Si ya no queda conexión entre $X$ y $Y$, están d-separados.

**Comprobación en $R\rightarrow T\leftarrow B$, $T\rightarrow T'$.**

- Para consultar $R\perp B$ sin evidencia, el subgrafo ancestral solo conserva $R,B$. No queda conexión y se garantiza independencia.
- Para consultar $R\perp B\mid T'$, debemos conservar $T'$ y sus ancestros, incluidos $T,R,B$. La moralización conecta $R$ con $B$ porque comparten el hijo $T$. Aunque retiremos la evidencia $T'$, esa conexión permanece y no hay garantía de independencia.

El orden de los pasos es crucial: **primero restringimos a los ancestros de la consulta y la evidencia**. Moralizar todo el grafo sin esa restricción daría una respuesta incorrecta en la primera consulta.

## 12. Práctica guiada con soluciones

Antes de desplegar cada solución, escribe extremos, evidencia y todos los caminos. El resultado debe incluir el nodo que bloquea o abre cada camino, no solo «sí» o «no».

### A. Cadena $X\rightarrow Y\rightarrow Z\rightarrow W$

1. ¿Se garantiza $X\perp W\mid Y$?
2. ¿Se garantiza $X\perp Z\mid W$?

> [!check]- Solución A
> 1. Sí. El único camino $X\rightarrow Y\rightarrow Z\rightarrow W$ queda bloqueado por el no colisionador observado $Y$.
> 2. No. En $X\rightarrow Y\rightarrow Z$, $Y$ sigue sin observar. $W$ es un descendiente fuera del camino y observarlo no bloquea $Y$.

### B. Red de alarma

3. ¿Se garantiza $J\perp M\mid A$?
4. ¿Se garantiza $B\perp E\mid J$?

> [!check]- Solución B
> 3. Sí. La causa común $J\leftarrow A\rightarrow M$ queda bloqueada por $A$ observado.
> 4. No. $J$ es descendiente del colisionador $A$ y observarlo abre $B\rightarrow A\leftarrow E$.

### C. Ejemplo 2 de clase

5. ¿Se garantiza $D\perp B\mid T$?
6. ¿Se garantiza $D\perp B\mid T,R$?

> [!check]- Solución C
> El único camino es $D\leftarrow R\rightarrow T\leftarrow B$.
> 5. No. $T$ observado abre el colisionador y $R$ sin observar deja pasar.
> 6. Sí. Aunque $T$ se abre, $R$ observado bloquea el camino.

### D. Ejemplo 3 de clase

7. ¿Se garantiza $T\perp D\mid S$?
8. ¿Existe un conjunto de evidencia entre los otros nodos que garantice $R\perp T$?

> [!check]- Solución D
> 7. No. $T\leftarrow R\rightarrow D$ sigue activo y $T\rightarrow S\leftarrow D$ se activa al observar $S$.
> 8. No. La arista directa $R\rightarrow T$ carece de nodos internos que podamos bloquear. Esto no impide que una CPT particular produzca independencia adicional.

## 13. Errores que conviene detectar al estudiar

| Error | Corrección |
|---|---|
| «No hay flecha directa, por tanto son independientes» | También debemos revisar los caminos indirectos. |
| «Solo se recorren caminos en dirección de las flechas» | Se recorren sin dirección y se conservan las puntas para clasificar tripletas. |
| «Todo nodo observado bloquea» | Un colisionador observado abre; un no colisionador observado bloquea. |
| «Un nodo con dos padres siempre es colisionador» | Solo lo es en un camino que utiliza dos aristas con puntas hacia ese nodo. |
| «Bloqueé un camino y terminé» | La garantía exige bloquearlos todos. |
| «Un camino abierto demuestra dependencia numérica» | Solo demuestra que el grafo no garantiza independencia. |
| «Agregar evidencia mantiene la independencia» | Puede abrir colisionadores, incluso mediante descendientes. |
| «Observar falso equivale a no observar» | Tanto verdadero como falso son valores conocidos y cuentan como evidencia. |
| «Las CPT cambian cuando observo» | La evidencia actualiza la distribución posterior; las CPT del modelo permanecen. |

## Avisos incluidos en el material

Las diapositivas 1–4 contienen comentarios sobre el examen y el proyecto. La propuesta debe identificar equipo, problema, hipótesis, datos o simulador y metodología, con un máximo de dos páginas y seis integrantes. El esquema de pitch incluye propósito, problema, mercado, solución, producto y componente de IA, competencia, modelo de negocio, equipo y finanzas. Se registran como información de la presentación; no se indican fechas adicionales de entrega. La diapositiva 32 anuncia **inferencia** como siguiente tema.

## Referencias y continuación

- **Material principal:** [[AI 14 Redes Bayesianas independencia.pdf|AI 14 — Redes bayesianas: independencia]], especialmente diapositivas 6–31.
- **AIMA:** Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], 4.ª edición global, §§13.1–13.2.1; §13.3.1 para el puente de enumeración. [Índice oficial de la edición global](https://aima.cs.berkeley.edu/global-index.html). En la 3.ª edición, el tema corresponde al capítulo 14.
- **Berkeley CS 188:** [§6.3 Representación](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/representation.html), [§6.4 Estructura](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/structure.html) y [§6.5 D-separación](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/d-separation.html). Para continuar: [§6.6 Inferencia exacta](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/elimination.html).
- **MIT 6.034, Patrick Winston:** [Probabilistic Inference Notes](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/3e6200ca84af05d95712045abedce9e9_MIT6_034F10_bayes.pdf), pp. 1–2 para los conteos del perro y pp. 4–5 para factorización; [Lecture 22: Probabilistic Inference II](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/resources/lecture-22-probabilistic-inference-ii/) para continuar con modelos e inferencia.

## Resumen después de clase

Una red bayesiana representa una conjunta mediante un DAG y distribuciones condicionadas a los padres. La d-separación permite leer las independencias que toda distribución compatible con esa estructura debe cumplir. Observar el nodo central de una cadena o causa común bloquea el camino, mientras que observar un colisionador o su descendiente puede abrirlo. En redes con varios caminos hay que bloquearlos todos; si queda uno activo, la independencia deja de estar garantizada y la relación numérica depende de las CPT.
