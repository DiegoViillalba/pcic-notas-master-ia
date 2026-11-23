---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-09-29"
unidad: Razonamiento probabilístico y redes bayesianas
profesor: Carlos Hernández
estado: procesada
conceptos:
  - Variable aleatoria
  - Distribución conjunta
  - Marginalización
  - Probabilidad condicional
  - Independencia condicional
  - Regla de la cadena
  - Red bayesiana
  - D-separación
referencias:
  - "[[AI 13 introducción agentes probabilísticos.pdf|Presentación de la clase 13]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/"
tags:
  - clase
  - inteligencia-artificial
  - probabilidad
  - redes-bayesianas
  - independencia-condicional
  - d-separacion
---

# Agentes Probabilisticos

> [!summary] Pregunta central
> ¿Cómo representa un agente lo que desconoce, actualiza sus creencias cuando observa evidencia y aprovecha la estructura del problema para evitar una tabla exponencial de posibilidades?

Esta nota desarrolla las **32 diapositivas** de la presentación. Las definiciones y los ejemplos de temperatura, clima y alarma proceden de ese material. Las derivaciones detalladas, ejercicios y visualizaciones amplían la explicación; los complementos de Berkeley se identifican con enlaces a las secciones correspondientes de **CS 188**. La inferencia por enumeración y las tripletas adicionales sirven de apoyo y preparación: la presentación anuncia que la inferencia continuará en la siguiente sesión.

![[AI 13 introducción agentes probabilísticos.pdf]]

## Ruta de estudio incremental

1. **Representar:** variable → dominio → distribución → distribución conjunta.
2. **Consultar:** sumar posibilidades → incorporar evidencia → normalizar.
3. **Simplificar:** reconocer independencia → aplicar regla de la cadena → eliminar dependencias innecesarias.
4. **Modelar:** construir un grafo acíclico y sus tablas locales → recuperar la conjunta.
5. **Interpretar:** distinguir conexiones directas e indirectas → estudiar cadenas → introducir d-separación.

## 1. De dónde venimos y por qué aparece la incertidumbre

*Diapositivas 1–6.* La sesión abre con dudas de la tarea 3 y comentarios sobre el avance del curso; la presentación no registra cuáles fueron esas dudas ni sus respuestas. Después plantea la transición de búsqueda, juegos y agentes lógicos hacia incertidumbre y aprendizaje.

| Tema anterior | Qué representábamos | Qué agregamos ahora |
|---|---|---|
| [[2026-08-20 IA - Algoritmos de busqueda\|Búsqueda]] | Estados y transiciones del modelo | Incertidumbre sobre el estado o el resultado de una acción |
| [[2026-09-08 IA - Incertidumbre y Expectimax\|Juegos y Expectimax]] | Resultados posibles y valores esperados | Un modelo explícito para calcular las probabilidades |
| [[2026-09-10 IA - Agentes logicos\|Agentes lógicos]] | Hechos, reglas y consecuencias | Grados de creencia sobre hechos no observados |
| [[2026-09-24 IA - CNF\|Representación y planificación]] | Conocimiento y acciones con precondiciones y efectos | Evidencia incompleta, sensores imperfectos y resultados inciertos |

Los apuntes iniciales describían las implementaciones previas como completamente deterministas. Conviene matizarlo: **ya habíamos encontrado incertidumbre en Expectimax**. El cambio de esta clase es estudiar cómo representar y relacionar las probabilidades, en vez de recibirlas simplemente como datos de un árbol de juego.

### Paso 1: separar el mundo de lo que sabe el agente

Una proposición como «está lloviendo» puede tener un valor verdadero o falso en el mundo, aunque el agente no lo conozca. Asignar $P(R=\mathrm{true})=0.3$  ( donde $R =$ Rain) expresa incertidumbre del agente; no significa que la proposición sea «30 % verdadera» en lógica clásica.

La incertidumbre puede aparecer porque:

- faltan observaciones: no vemos si llueve en el destino;
- las mediciones tienen ruido: un detector puede producir falsos positivos;
- las acciones tienen resultados variables: salir a la misma hora no garantiza el mismo tiempo de viaje;
- el modelo omite variables: tráfico, accidentes, obras o cambios de ruta.

Un proceso determinista también puede ser incierto **para quien desconoce sus entradas**. La frase de la diapositiva 5 sobre la falta de certeza es una motivación, no una afirmación de que todo proceso sea necesariamente aleatorio.

### Paso 2: pasar de demostrar a estimar

En lógica preguntamos si $KB\models\alpha$. En probabilidad preguntamos cuánto apoyo tiene una hipótesis dada la información disponible:

$$P(\alpha\mid e).$$

Aquí $e$ es la **evidencia observada**. Por ejemplo, una llamada del vecino es evidencia de una alarma, pero no prueba por sí sola que haya ocurrido un robo.

### Paso 3: conectar las creencias con una acción

El modelo probabilístico estima resultados; para elegir una acción también hacen falta preferencias o costos. Como puente con Expectimax:

$$a^*\in\arg\max_a\sum_s P(s\mid e,a)U(a,s).$$

**Ejemplo didáctico:** llevar paraguas cuesta 1 unidad de incomodidad; no llevarlo cuesta 10 si llueve y 0 si no llueve. Si $p=P(R=\mathrm{true}\mid e)$, los costos esperados son $1$ y $10p$. Conviene llevarlo cuando $p>0.1$; si $p=0.1$, ambas acciones empatan. La probabilidad informa la decisión, pero el umbral depende del costo.

Este puente sigue la idea de maximizar utilidad esperada en [CS 188, §7.1 Utilities](https://inst.eecs.berkeley.edu/~cs188/textbook/vpis/utilities.html). No es un nuevo desarrollo de teoría de utilidad dentro de esta presentación.

## 2. Variables aleatorias, dominios y resultados

*Diapositiva 7.* Una **variable aleatoria** representa un aspecto del mundo cuyo valor puede ser desconocido. Formalmente es una función:

$$X:\Omega\longrightarrow E,$$

donde $\Omega$ contiene los resultados elementales del experimento y $E$ es el espacio de valores de la variable. Para cada $\omega\in\Omega$, la función devuelve un valor $X(\omega)$.

| Variable | Pregunta | Dominio ilustrativo |
|---|---|---|
| $R$ | ¿Llueve? | $\{\mathrm{true},\mathrm{false}\}$ |
| $T$ | ¿La temperatura es fría o cálida? | $\{\mathrm{cold},\mathrm{hot}\}$ |
| $D$ | ¿Cuánto tardamos en llegar a la UNAM? | $[0,\infty)$, por ejemplo en minutos |

La presentación utiliza $T$ para **temperatura**; en el ejemplo posterior $P(T,R,U)$ se utilizará para **tráfico**. Son ejemplos distintos y se indicará el significado en cada caso.

### Notación que debemos distinguir

- $X$: la variable.
- $x$: un valor concreto de su dominio.
- $X=x$: un evento, es decir, el conjunto de resultados donde la variable toma ese valor.
- $P(X)$: la distribución completa.
- $P(X=x)$: una probabilidad particular.

Se puede abreviar $P(W=\mathrm{rain})$ como $P(\mathrm{rain})$ cuando queda claro qué variable está involucrada. Para variables booleanas, $+b$ significa $B=\mathrm{true}$ y $-b$ significa $B=\mathrm{false}$.

> [!note] Discreto y continuo
> Las tablas de esta clase corresponden a variables discretas. Si $D$ es continuo, se describe con una densidad $f_D$ y las probabilidades de intervalos se obtienen integrando: $P(a\leq D\leq b)=\int_a^b f_D(t)\,dt$. En un modelo puramente continuo, $P(D=d)=0$ para un valor exacto; una densidad no es una probabilidad puntual. El símbolo $\infty$ indica que no hay una cota superior, no un tiempo de viaje observable.

## 3. Una distribución asigna masa a las alternativas

*Diapositiva 8.* Para una variable discreta:

$$P(X=x)\geq 0,\qquad \sum_{x\in\mathrm{Dom}(X)}P(X=x)=1.$$

La primera condición impide probabilidades negativas; la segunda exige repartir toda la masa entre las alternativas del dominio. De ambas se deduce $P(X=x)\leq1$.

Las tablas de la diapositiva son:

| Temperatura $T$ | $P(T)$ |
|---|---:|
| hot | 0.5 |
| cold | 0.5 |

| Clima $W$ | $P(W)$ |
|---|---:|
| sun | 0.6 |
| rain | 0.1 |
| fog | 0.3 |
| meteor | 0.0 |

En este modelo, $0.6+0.1+0.3+0=1$. Un cero excluye ese resultado **del modelo**; no constituye una prueba universal de imposibilidad física.

> [!warning] Las diapositivas cambian de ejemplo
> En las diapositivas 9–10 el dominio de $W$ se reduce a $\{\mathrm{sun},\mathrm{rain}\}$ y la probabilidad marginal de lluvia será **0.4**. Esa conjunta es otro modelo: no debe mezclarse con la tabla anterior, donde la lluvia tiene probabilidad **0.1**.

## 4. Distribución conjunta: una fila por mundo posible

*Diapositiva 9.* Una distribución conjunta especifica la probabilidad de **cada asignación completa** de un conjunto de variables:

$$P(X_1=x_1,\ldots,X_n=x_n)\equiv P(x_1,\ldots,x_n).$$

La coma representa conjunción de eventos. $P(T=\mathrm{hot},W=\mathrm{sun})$ es la probabilidad de que ocurran ambos a la vez.

La conjunta que se usa en las diapositivas 9–11 es:

| $T$ | $W$ | $P(T,W)$ |
|---|---|---:|
| hot | sun | 0.4 |
| hot | rain | 0.1 |
| cold | sun | 0.2 |
| cold | rain | 0.3 |

**Construcción mental, paso a paso:**

1. $T$ tiene dos valores y $W$ tiene dos valores.
2. Formamos las cuatro combinaciones del producto cartesiano.
3. Asignamos una masa no negativa a cada combinación.
4. Comprobamos que $0.4+0.1+0.2+0.3=1$.

Para cualquier conjunta discreta:

$$\sum_{x_1}\cdots\sum_{x_n}P(x_1,\ldots,x_n)=1.$$

### ¿Cuánto ocupa la tabla?

Con $n$ variables y dominios de tamaño $d$, hay **$d^n$ filas**. Si los dominios son distintos, hay $\prod_i d_i$ filas. La distribución sin restricciones tiene $d^n-1$ parámetros libres, porque la normalización determina el último.

| Variables booleanas | Filas de la conjunta |
|---:|---:|
| 2 | 4 |
| 5 | 32 |
| 10 | 1 024 |
| 20 | 1 048 576 |
| 30 | 1 073 741 824 |

Agregar una variable booleana **duplica** el número de filas. Esta dificultad motivará las redes bayesianas.

## 5. Marginalizar: sumar lo que no preguntamos

*Diapositiva 10.* Si solo queremos conocer $T$, agrupamos las filas que comparten su valor y sumamos sobre todos los valores de $W$:

$$P(T=t)=\sum_wP(T=t,W=w).$$

Aplicándolo a la tabla:

$$\begin{aligned}
P(T=\mathrm{hot})&=0.4+0.1=0.5,\\
P(T=\mathrm{cold})&=0.2+0.3=0.5.
\end{aligned}$$

Si queremos conocer $W$, eliminamos $T$ mediante una suma:

$$\begin{aligned}
P(W=\mathrm{sun})&=0.4+0.2=0.6,\\
P(W=\mathrm{rain})&=0.1+0.3=0.4.
\end{aligned}$$

**No borramos filas ni tomamos un promedio.** Sumamos las posibilidades mutuamente excluyentes de la variable que dejamos de consultar. Tampoco elegimos la fila más probable: eso respondería otra pregunta.

## 6. Condicionar: restringir por evidencia y normalizar

*Complemento necesario para las diapositivas 14–16.* Marginalizar significa que no sabemos o no nos interesa el valor de una variable. Condicionar significa que **sí conocemos un valor observado**.

Para $P(W=w)>0$:

$$P(T=t\mid W=w)=\frac{P(T=t,W=w)}{P(W=w)}.$$

### Ejemplo: temperatura dado que llueve

1. **Seleccionar evidencia:** conservamos las filas con $W=\mathrm{rain}$.
2. **Obtener pesos:** hot tiene peso $0.1$ y cold tiene peso $0.3$.
3. **Calcular la masa de la evidencia:** $P(\mathrm{rain})=0.1+0.3=0.4$.
4. **Normalizar:** dividimos cada peso entre $0.4$.

$$P(\mathrm{hot}\mid\mathrm{rain})=0.25,\qquad
P(\mathrm{cold}\mid\mathrm{rain})=0.75.$$

Ahora ambas probabilidades suman 1. En cambio, $0.1$ y $0.3$ eran probabilidades conjuntas y sumaban la probabilidad de la evidencia, no 1.

### La dirección de la condición importa

$$P(\mathrm{rain}\mid\mathrm{cold})=\frac{0.3}{0.5}=0.6,$$

mientras que $P(\mathrm{cold}\mid\mathrm{rain})=0.75$. Los numeradores coinciden, pero los denominadores describen poblaciones distintas.

La regla del producto y la regla de Bayes se obtienen de la definición:

$$P(x,y)=P(x\mid y)P(y)=P(y\mid x)P(x),$$

$$P(x\mid y)=\frac{P(y\mid x)P(x)}{P(y)}.$$

En Bayes, $P(x)$ es la creencia previa, $P(y\mid x)$ la verosimilitud de la evidencia bajo la hipótesis, $P(y)$ la masa de esa evidencia y $P(x\mid y)$ la creencia posterior. La verosimilitud, considerada como función de $x$ con $y$ fijo, no tiene por qué sumar 1 sobre las hipótesis.

> [!note] Conexión con Berkeley
> [CS 188, §6.1 Probability Rundown](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/probability.html) reúne estas operaciones y la notación de independencia. Su función en esta nota es conectar las tablas de la presentación con las expresiones condicionales posteriores. Una consulta puede combinar selección de evidencia, sumas sobre variables ocultas y normalización; si la evidencia tiene probabilidad cero, el cociente condicional no está definido.

### Construcción paso a paso con áreas: de la conjunta a la marginal y la condicional

**Idea guía:** un cuadrado de **área 1** contiene todos los mundos posibles; la probabilidad de un evento es el **área** de su región. Con esa imagen, conjunta, marginalización y condicionamiento son tres movimientos distintos sobre la *misma* tabla.

<iframe src="probabilidad-areas-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

*Recórrela con el control deslizante (pasos 1–7). Cada paso de abajo corresponde al mismo paso de la visualización.*

**Si no carga:** la tabla de partida es

| | sun | rain | $P(T)$ |
|---|---:|---:|---:|
| **hot** | 0.4 | 0.1 | 0.5 |
| **cold** | 0.2 | 0.3 | 0.5 |
| $P(W)$ | 0.6 | 0.4 | 1 |

**Paso 1 · Todo el espacio.** El cuadrado completo es la incertidumbre total del agente: área $=1$.

**Paso 2 · Cortar por una variable.** Un corte vertical por $W$ da dos franjas cuyos **anchos** son $0.6$ (sun) y $0.4$ (rain).

**Paso 3 · Distribución conjunta $P(T,W)$.** Cortamos cada columna por $T$. Cada celda es un **mundo completo** y su área es *ancho × alto*:

$$P(\mathrm{hot},\mathrm{sun})=\underbrace{P(\mathrm{sun})}_{\text{ancho}}\cdot\underbrace{P(\mathrm{hot}\mid\mathrm{sun})}_{\text{alto}}=0.6\cdot\tfrac23=0.4.$$

Las cuatro áreas suman 1. *Ya aparece, sin decirlo, la regla del producto $P(t,w)=P(w)P(t\mid w)$: la condicional es la proporción de alto dentro de una columna.*

**Paso 4 · Marginalizar $W$ (olvidar el clima).** Se **reagrupan las mismas piezas por temperatura**. Las áreas no cambian; solo dejamos de distinguir sun de rain:

$$P(\mathrm{hot})=0.4+0.1=0.5,\qquad P(\mathrm{cold})=0.2+0.3=0.5.$$

**Paso 5 · Marginalizar $T$.** Mismo movimiento en la otra dirección: se agrupa por columna.

$$P(\mathrm{sun})=0.4+0.2=0.6,\qquad P(\mathrm{rain})=0.1+0.3=0.4.$$

Las marginales son los **márgenes de la tabla**, y geométricamente los anchos (o alturas) de las franjas. Marginalizar nunca descarta área: por eso el resultado ya suma 1.

**Paso 6 · Condicionar: observo $W=\mathrm{rain}$.** La evidencia **elimina los mundos incompatibles**: la franja *sun* sale del cuadro. Lo que sobrevive tiene área $0.4$, que es exactamente $P(\mathrm{rain})$. Todavía **no es una distribución**, porque no suma 1.

**Paso 7 · Renormalizar.** Dividir entre $P(\mathrm{rain})$ equivale a **ampliar** la franja hasta ocupar todo el cuadrado. Las proporciones no cambian; las alturas son ahora $P(T\mid\mathrm{rain})$:

$$P(\mathrm{hot}\mid\mathrm{rain})=\frac{0.1}{0.4}=0.25,\qquad P(\mathrm{cold}\mid\mathrm{rain})=\frac{0.3}{0.4}=0.75.$$

#### Resumen: dos movimientos distintos

| | Marginalizar (pasos 4–5) | Condicionar (pasos 6–7) |
|---|---|---|
| Geometría | **Reagrupar** las piezas; el área total sigue siendo 1 | **Descartar** piezas y **ampliar** lo que queda |
| Qué sabe el agente | No conoce (o ignora) la otra variable | **Observó** la otra variable |
| Fórmula | $P(t)=\sum_w P(t,w)$ | $P(t\mid w)=\dfrac{P(t,w)}{P(w)}$ |
| ¿Normalizar? | No | Sí: lo que sobrevive suma $P(w)<1$ |
| Con la tabla | $P(\mathrm{cold})=0.5$ | $P(\mathrm{cold}\mid\mathrm{rain})=0.75$ |

> [!tip] Independencia, geométricamente
> Si $T$ y $W$ son independientes, **todas las columnas se cortan a la misma altura**: la línea que separa hot de cold queda horizontal de lado a lado. Entonces ampliar la franja *rain* no cambia nada: $P(T\mid W)=P(T)$. Activa «T y W independientes» en la visualización y compara el paso 7.

### Visualización · Conjunta, marginal y condicional

<iframe src="probabilidad-conjunta-marginal-condicional.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Cómo estudiarla:** selecciona la consulta $T$ y evidencia $W=\mathrm{rain}$; recorre los pasos para ver $0.1$ y $0.3$ convertirse en $0.25$ y $0.75$. Quita la evidencia para recuperar la marginal. El control de dependencia interpola entre las dos tablas de la diapositiva 14 manteniendo sus marginales.

**Si no carga:** marginalizar suma todas las filas compatibles con el valor consultado; condicionar selecciona las filas compatibles con la evidencia y divide sus pesos entre la masa total seleccionada. En este ejemplo, $P(\mathrm{cold})=0.5$ pero $P(\mathrm{cold}\mid\mathrm{rain})=0.75$.

## 7. Un modelo probabilístico es una simplificación consultable

*Diapositivas 11–12.* En esta clase, un modelo probabilístico consiste en variables, dominios y una distribución conjunta sobre sus asignaciones.

No contiene necesariamente todas las variables del mundo ni todas sus interacciones. La elección depende de las preguntas que pretendemos responder. Un modelo de trayectos que incluya lluvia y tráfico puede ser útil aunque omita el color de cada automóvil.

Conviene separar tres tareas, retomando la diapositiva 19:

| Tarea | Pregunta |
|---|---|
| Modelado | ¿Qué variables y relaciones conviene incluir? |
| Representación | ¿Cómo almacenamos la distribución y sus supuestos? |
| Inferencia | ¿Qué probabilidades se siguen del modelo y la evidencia? |

El aprendizaje, al que apunta la transición inicial, podrá estimar probabilidades o estructura a partir de datos. **Inferir con un modelo dado y aprender ese modelo son problemas distintos.**

## 8. Independencia: cuándo una variable no aporta información sobre otra

*Diapositivas 14 y 21.* $X$ e $Y$ son independientes, $X\perp Y$, si:

$$\forall x,y:\quad P(x,y)=P(x)P(y).$$

Para valores $y$ con $P(y)>0$, esto equivale a:

$$P(x\mid y)=P(x).$$

La condición debe cumplirse **para todas las asignaciones**, no solamente para una fila. La independencia es una propiedad de la distribución.

### Comparar las dos tablas de la presentación

La diapositiva 14 mantiene las marginales $P(T)=(0.5,0.5)$ y $P(W)=(0.6,0.4)$, pero compara dos conjuntas:

| $T$ | $W$ | $P_1(T,W)$: dependiente | $P_2(T,W)$: independiente |
|---|---|---:|---:|
| hot | sun | 0.4 | 0.3 |
| hot | rain | 0.1 | 0.2 |
| cold | sun | 0.2 | 0.3 |
| cold | rain | 0.3 | 0.2 |

Para $P_1$:

$$P_1(\mathrm{hot},\mathrm{sun})=0.4\ne0.5(0.6)=0.3.$$

Una sola desigualdad basta para refutar independencia. Para $P_2$, cada fila es el producto de sus marginales, así que $T\perp W$.

**Conclusión:** conocer las marginales no determina la conjunta; falta saber cómo se relacionan las variables. No podemos multiplicar marginales sin justificar independencia.

## 9. Independencia condicional: qué información deja de ser necesaria

*Diapositivas 15 y 21.* Escribimos $X\perp Y\mid Z$ cuando, para cada valor $z$ con $P(z)>0$:

$$P(x,y\mid z)=P(x\mid z)P(y\mid z).$$

En los casos donde las condiciones tienen probabilidad positiva, equivale a:

$$P(x\mid y,z)=P(x\mid z).$$

Una vez que sabemos $z$, conocer además $y$ no modifica la distribución de $X$.

### Ejemplo de lluvia, tráfico y paraguas

En este ejemplo tomamos $R=$ lluvia, $T=$ tráfico y $U=$ uso de paraguas. Podemos **suponer**:

$$T\perp U\mid R.$$

![[ia29-lluvia-trafico-paraguas.svg]]

**Lectura del grafo:** lluvia es el padre común de tráfico y uso de paraguas. El dibujo representa el supuesto del modelo; la ausencia de una flecha entre sus hijos no garantiza independencia sin observar la lluvia.

La lluvia influye en ambos, pero una vez conocida la lluvia, el paraguas no añade información sobre el tráfico dentro de este modelo. Esto omite otras causas compartidas y debe revisarse si los datos contradicen el supuesto.

Sin observar $R$, ver paraguas puede informar sobre lluvia y, por esa vía, sobre tráfico. Por ello:

$$T\perp U\mid R\quad\text{no implica}\quad T\perp U.$$

Tampoco la independencia marginal implica siempre independencia condicional: observar un efecto común puede relacionar dos causas. Volveremos a ello al introducir d-separación.

## 10. Regla de la cadena: primero exactitud, después simplificación

*Diapositivas 16 y 23.* La regla del producto aplicada repetidamente da:

$$P(x_1,\ldots,x_n)=\prod_{i=1}^{n}P(x_i\mid x_1,\ldots,x_{i-1}),$$

donde el primer factor es $P(x_1)$. Se usan condicionales definidos en los eventos de probabilidad positiva; las ramas de masa cero no contribuyen a la conjunta.

### Paso 1: descomponer sin asumir independencia

Para el orden $R,T,U$:

$$\begin{aligned}
P(t,r,u)&=P(r)P(t,u\mid r)\\
&=P(r)P(t\mid r)P(u\mid r,t).
\end{aligned}$$

Esta igualdad no requiere $T\perp U\mid R$. Cambiar el orden de las variables cambia los factores, pero no la probabilidad de la asignación completa.

### Paso 2: declarar el supuesto del modelo

Si $U\perp T\mid R$, entonces:

$$P(u\mid r,t)=P(u\mid r).$$

### Paso 3: sustituir y obtener tablas menores

$$\boxed{P(t,r,u)=P(r)P(t\mid r)P(u\mid r).}$$

Para variables booleanas, una conjunta general necesita 7 parámetros libres. Esta factorización requiere 1 para $R$, 2 para $T\mid R$ y 2 para $U\mid R$: **5**. El ahorro proviene del supuesto de independencia condicional, no de escribir la misma tabla con otros símbolos.

## 11. Por qué una conjunta completa es difícil de almacenar y aprender

*Diapositiva 17.* La explosión de filas afecta dos aspectos:

1. **Representar:** hay que guardar una probabilidad por cada asignación.
2. **Estimar:** hacen falta datos suficientes para distinguir muchas combinaciones; algunas aparecerán pocas veces o nunca.

Una frecuencia empírica nula puede deberse a falta de observaciones. No justifica por sí sola declarar un evento imposible.

Si cada variable interactúa directamente con pocas otras, podemos estimar y almacenar tablas locales. Esto reduce parámetros bajo los supuestos adecuados, aunque **una representación compacta no garantiza que cualquier inferencia sea rápida**.

## 12. Redes bayesianas: grafo más tablas locales

*Diapositivas 18–20 y 24–25.* Una red bayesiana discreta tiene dos componentes:

1. Un **grafo dirigido acíclico**, o DAG, con un nodo por variable.
2. Una distribución $P(X_i\mid\mathrm{Pa}(X_i))$ para cada nodo, representada por una **tabla de probabilidad condicional** o CPT.

$\mathrm{Pa}(X_i)$ es el conjunto de padres: los nodos con flechas que entran en $X_i$. Una raíz no tiene padres y su tabla es una marginal $P(X_i)$.

### Cómo leer un grafo

- Los nodos representan variables, cada una con su dominio.
- Un nodo observado tiene un valor asignado por la evidencia; uno no observado conserva alternativas.
- Las flechas especifican qué variables aparecen como padres en las tablas locales.
- El grafo expresa supuestos de independencia condicional; no almacena los números.
- Un DAG admite un orden topológico: los padres aparecen antes que sus hijos.

La analogía con CSP de la diapositiva 24 es útil: ambos usan grafos para expresar relaciones locales. En un CSP una restricción permite o prohíbe combinaciones; aquí una CPT asigna probabilidades a los valores del hijo para cada configuración de padres.

### Una CPT debe normalizar por configuración de padres

Si $X$ es booleano:

$$P(X=\mathrm{true}\mid p)+P(X=\mathrm{false}\mid p)=1$$

**para cada** configuración $p$ de sus padres. La suma de toda la columna de probabilidades a través de configuraciones distintas no tiene por qué ser 1.

> [!note] Flechas y causalidad
> [CS 188, §6.3 Bayesian Network Representation](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/representation.html) presenta el DAG y las CPT como una representación de la conjunta. Una interpretación causal es posible con supuestos adicionales; el grafo probabilístico por sí solo no demuestra causalidad. Observar $Y=y$ tampoco equivale automáticamente a intervenir y fijar $Y$.

La referencia de la diapositiva 25 a un proceso «causal» con ruido debe leerse con esa salvedad. Las flechas tampoco obligan a que haya dependencia numérica: una CPT puede ignorar efectivamente un padre.

## 13. De la regla de la cadena a la semántica de la red

*Diapositivas 26–27.* Tomemos un orden topológico $X_1,\ldots,X_n$.

**Paso 1.** Expandimos usando la regla de la cadena:

$$P(x_1,\ldots,x_n)=\prod_iP(x_i\mid x_1,\ldots,x_{i-1}).$$

**Paso 2.** La red supone que los padres hacen innecesaria la información adicional de las variables anteriores:

$$P(x_i\mid x_1,\ldots,x_{i-1})=P(x_i\mid\mathrm{pa}(X_i)).$$

**Paso 3.** Sustituimos en cada factor:

$$\boxed{P(x_1,\ldots,x_n)=\prod_iP(x_i\mid\mathrm{pa}(X_i)).}$$

$\mathrm{Pa}(X_i)$ denota el conjunto de variables; $\mathrm{pa}(X_i)$, sus valores en la asignación particular.

**¿Por qué el producto está normalizado?** Al sumar sobre todas las asignaciones, eliminamos primero los nodos hoja. Para cada configuración de sus padres, la suma de su CPT es 1. Repetimos en orden topológico inverso hasta llegar a las raíces; queda 1. El DAG y las tablas válidas definen así una conjunta válida.

### Qué distribuciones admite un grafo

La frase «no toda red puede representar toda conjunta» se refiere a un **grafo fijo**: si impone $X\perp Y$, no representa una conjunta que viole esa independencia. Un DAG completo según un orden de variables sí puede representar cualquier conjunta discreta mediante la regla de la cadena, pero pierde el ahorro estructural.

### Regla local de independencia

Cada nodo es independiente de sus **no descendientes que no son sus padres**, dados sus padres. Un descendiente es un nodo al que se llega siguiendo flechas desde el nodo original.

Como complemento de [CS 188, §6.4 Structure of Bayes Nets](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/structure.html), la **manta de Markov** de un nodo reúne sus padres, sus hijos y los otros padres de sus hijos. Dados esos nodos, el resto de la red no añade información sobre él. Es otra independencia que se obtiene de la estructura.

## 14. Ejemplo completo: robo, terremoto, alarma y llamadas

*Diapositiva 13, retomada después de construir las definiciones.* Las cinco variables booleanas son:

| Variable | Significado |
|---|---|
| $B$ | Burglary: ocurre un robo |
| $E$ | Earthquake: ocurre un terremoto |
| $A$ | Alarm: suena la alarma |
| $J$ | John calls: John llama |
| $M$ | Mary calls: Mary llama |

![[ia29-red-alarma.svg]]

**Lectura del grafo:** las flechas entran desde los padres de cada tabla. Robo y terremoto son raíces; las dos llamadas comparten la alarma como padre.

El modelo admite falsas alarmas, fallas de detección y llamadas aun cuando no suena la alarma.

### 14.1 Las tablas de la presentación

Las raíces tienen $P(+b)=0.001$ y $P(+e)=0.002$. Sus complementos son $P(-b)=0.999$ y $P(-e)=0.998$.

| $B$ | $E$ | $P(+a\mid B,E)$ | $P(-a\mid B,E)$ |
|---|---|---:|---:|
| true | true | 0.95 | 0.05 |
| true | false | 0.94 | 0.06 |
| false | true | 0.29 | 0.71 |
| false | false | 0.001 | 0.999 |

| $A$ | $P(+j\mid A)$ | $P(-j\mid A)$ | $P(+m\mid A)$ | $P(-m\mid A)$ |
|---|---:|---:|---:|---:|
| true | 0.9 | 0.1 | 0.7 | 0.3 |
| false | 0.05 | 0.95 | 0.01 | 0.99 |

Por ejemplo, $P(+a\mid-b,-e)=0.001$ es una falsa alarma bajo ausencia de ambas causas modeladas. No es $P(-b,-e\mid+a)$.

### 14.2 Aplicar la factorización

Primero, la regla de la cadena en el orden $B,E,A,J,M$:

$$P(b,e,a,j,m)=P(b)P(e\mid b)P(a\mid b,e)P(j\mid b,e,a)P(m\mid b,e,a,j).$$

Después, los supuestos de la red permiten simplificar:

$$\boxed{P(b,e,a,j,m)=P(b)P(e)P(a\mid b,e)P(j\mid a)P(m\mid a).}$$

Esto supone $B\perp E$, $J\perp\{B,E\}\mid A$ y $M\perp\{B,E,J\}\mid A$.

### 14.3 Calcular un mundo concreto

Queremos la probabilidad de que **no** haya robo ni terremoto, suene la alarma, John llame y Mary no llame:

$$\begin{aligned}
P(-b,-e,+a,+j,-m)
&=0.999(0.998)(0.001)(0.9)(0.3)\\
&=0.00026919054.
\end{aligned}$$

Multiplicamos un factor por nodo. El factor de Mary es $0.3$, porque la asignación dice que **no llama** y la alarma sí suena.

### 14.4 Contar lo que ahorramos

Una conjunta de cinco booleanos tiene 32 filas y 31 parámetros libres. La red requiere:

$$\underbrace{1}_{B}+\underbrace{1}_{E}+\underbrace{4}_{A\mid B,E}
+\underbrace{2}_{J\mid A}+\underbrace{2}_{M\mid A}=10$$

parámetros libres. Si guardamos también los complementos, las CPT contienen 20 probabilidades. **Filas o números almacenados y parámetros libres son conteos distintos.**

En general, un nodo con $d_i$ valores y padres de tamaños $d_j$ necesita $(d_i-1)\prod_{X_j\in\mathrm{Pa}(X_i)}d_j$ parámetros libres. Para $n$ booleanos con a lo sumo $k$ padres por nodo, el total es a lo sumo $n2^k$; el beneficio es grande cuando $k$ permanece pequeño.

### 14.5 Consulta de apoyo: ¿hubo robo si ambos llaman?

Esta es una ampliación para preparar la siguiente sesión. [CS 188, §6.2 Probability Inference](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/inference.html) organiza la enumeración en tres operaciones: seleccionar evidencia, sumar variables ocultas y normalizar.

Para $P(B\mid+j,+m)$:

- **Consulta:** $B$.
- **Evidencia:** $J=\mathrm{true}$ y $M=\mathrm{true}$.
- **Ocultas:** $E$ y $A$, porque no se observan ni se preguntan.

Primero calculamos dos pesos, uno por valor de $B$:

$$w_b=P(b)\sum_eP(e)\sum_aP(a\mid b,e)P(+j\mid a)P(+m\mid a).$$

Con robo, la probabilidad de alarma tras sumar sobre terremoto es:

$$P(+a\mid+b)=0.002(0.95)+0.998(0.94)=0.94002.$$

Si suena la alarma, ambas llamadas tienen probabilidad $0.9(0.7)=0.63$; si no suena, $0.05(0.01)=0.0005$. Entonces:

$$w_{+b}=0.001\,[0.94002(0.63)+0.05998(0.0005)]=0.00059224259.$$

Sin robo:

$$P(+a\mid-b)=0.002(0.29)+0.998(0.001)=0.001578,$$

$$w_{-b}=0.999\,[0.001578(0.63)+0.998422(0.0005)]=0.001491857649.$$

La masa de la evidencia es la suma de ambos pesos:

$$P(+j,+m)=w_{+b}+w_{-b}=0.002084100239.$$

Normalizamos:

$$\boxed{P(+b\mid+j,+m)=\frac{0.00059224259}{0.002084100239}\approx0.28417.}$$

La probabilidad sube de **0.1 %** a aproximadamente **28.42 %**. Las llamadas aportan información, pero no certeza; las falsas alarmas y llamadas sin alarma siguen siendo explicaciones posibles.

### Visualización · Construir y consultar la red de alarma

<iframe src="red-bayesiana-alarma-interactiva.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Cómo estudiarla:** observa primero las CPT. Después fija $J=+$ y $M=+$, consulta $B$ y revisa las filas compatibles y sus pesos. Selecciona una fila para ver el producto que construye ese mundo. Prueba luego observar $A=+$ y agregar $E=+$: el terremoto ofrece una explicación alternativa de la alarma.

**Si no carga:** la conjunta se calcula multiplicando $P(B)P(E)P(A\mid B,E)P(J\mid A)P(M\mid A)$. Para consultar una variable se suman las filas compatibles con la evidencia y se normaliza. Ambas llamadas producen $P(+b\mid+j,+m)\approx0.28417$ bajo las tablas de la presentación.

## 15. Otros escenarios de la presentación: fuego y caries

### 15.1 Fuego, humo y alarma

*Diapositiva 22.* La imagen muestra fuego, humo y un detector; no fija un DAG ni una CPT. Una **propuesta de modelado** es:

![[ia29-fuego-humo-alarma.svg]]

**Lectura del diagrama:** arriba, la alarma responde al humo; abajo, humo y alarma son efectos del fuego. Cada propuesta expresa una independencia distinta.

Esta propuesta expresa que el detector responde al humo y supone:

$$A\perp F\mid H,\qquad P(F,H,A)=P(F)P(H\mid F)P(A\mid H).$$

**Interpretación:** si ya sabemos cuánto humo hay, saber además que hay fuego no modifica la probabilidad de alarma en este modelo. Si la alarma también utiliza un sensor de calor, esa suposición podría ser incorrecta y convendría incluir una relación adicional o una variable de calor.

Un modelo alternativo con $F\to H$ y $F\to A$ supone $H\perp A\mid F$. No son el mismo supuesto. Elegir flechas exige precisar cómo funciona el escenario, no solo dibujar los objetos presentes.

### 15.2 Caries, dolor y detección

*Diapositiva 24.* Aquí sí se muestra el grafo:

![[ia29-red-caries.svg]]

**Lectura del grafo:** el dolor y la detección son dos observaciones de una causa común. No hay una flecha directa entre ellas, pero pueden aportar información una sobre otra cuando no conocemos la caries.

La factorización es:

$$P(C,T,K)=P(C)P(T\mid C)P(K\mid C),$$

y el supuesto es $T\perp K\mid C$. Sin observar $C$, un dolor puede informar sobre caries y, por esa vía, sobre la detección. **Dos hijos de una causa común pueden estar relacionados aunque no tengan una flecha entre ellos.** La presentación no proporciona probabilidades para este ejemplo.

## 16. Supuestos directos y consecuencias adicionales: cadena de cuatro nodos

*Diapositiva 28.* El grafo es:

![[ia29-cadena-cuatro-nodos.svg]]

**Lectura del diagrama:** arriba el camino transmite información indirecta; abajo se fija $Z$ como evidencia y el único camino entre $X$ y $W$ queda bloqueado. El nodo relleno representa una observación.

La regla de la cadena completa da:

$$P(x,y,z,w)=P(x)P(y\mid x)P(z\mid x,y)P(w\mid x,y,z).$$

El grafo introduce los supuestos locales $Z\perp X\mid Y$ y $W\perp\{X,Y\}\mid Z$, por lo que:

$$P(x,y,z,w)=P(x)P(y\mid x)P(z\mid y)P(w\mid z).$$

Además se puede obtener $X\perp W\mid Y$. En efecto:

$$\begin{aligned}
P(w\mid x,y)
&=\sum_zP(w,z\mid x,y)\\
&=\sum_zP(w\mid z)P(z\mid y)\\
&=P(w\mid y).
\end{aligned}$$

La expresión final no depende de $x$. También $X\perp\{Z,W\}\mid Y$ y $Y\perp W\mid Z$. La estructura contiene consecuencias que van más allá de leer cada CPT por separado.

## 17. Cadena de tres nodos: conexión indirecta y bloqueo por evidencia

*Diapositivas 29 y 31.* Consideremos $X\to Y\to Z$: presión baja → lluvia → tráfico.

![[ia29-cadena-presion-lluvia-trafico.svg]]

**Lectura del diagrama:** compara la misma cadena antes y después de conocer la lluvia. La evidencia conserva las flechas del modelo y bloquea el paso de información adicional entre los extremos.

### Pregunta 1: ¿el grafo garantiza $X\perp Z$?

**No.** La información puede pasar por $Y$. La ausencia de una flecha directa entre $X$ y $Z$ no garantiza independencia.

**Contraejemplo construido:** tomamos booleanos con $P(X=1)=0.5$, $Y=X$ y $Z=Y$. La distribución factoriza según la cadena, pero:

$$P(X=1,Z=1)=0.5\ne0.5(0.5)=0.25.$$

Un contraejemplo basta para mostrar que la independencia no está garantizada. Esto no demuestra que toda parametrización del grafo tenga dependencia.

### Pregunta 2: ¿garantiza $X\perp Z\mid Y$?

**Sí.** La factorización de la cadena es:

$$P(x,y,z)=P(x)P(y\mid x)P(z\mid y).$$

Para $P(x,y)>0$:

$$\begin{aligned}
P(z\mid x,y)
&=\frac{P(x,y,z)}{P(x,y)}\\
&=\frac{P(x)P(y\mid x)P(z\mid y)}{P(x)P(y\mid x)}\\
&=P(z\mid y).
\end{aligned}$$

Una vez conocida la lluvia, la presión baja ya no añade información sobre tráfico **en este modelo**. Esta es la cancelación que desarrolla la diapositiva 31.

> [!note] Dos factorizaciones en la diapositiva 31
> Bajo el dibujo aparece $P(y)P(x\mid y)P(z\mid y)$, mientras que la demostración usa $P(x)P(y\mid x)P(z\mid y)$. Ambas son iguales porque $P(x)P(y\mid x)=P(y)P(x\mid y)$. La segunda sigue las flechas de la cadena; la primera también puede representarse con la bifurcación $X\leftarrow Y\to Z$. Comparten la independencia $X\perp Z\mid Y$, pero esa equivalencia probabilística no identifica la dirección causal del mundo.

## 18. D-separación: leer independencia mediante caminos

*Diapositiva 30 y complemento para la 31.* La presentación propone estudiar tripletas, componerlas en casos mayores y obtener un criterio gráfico. [CS 188, §6.5 D-Separation](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/d-separation.html) desarrolla ese criterio: si la evidencia bloquea todos los caminos entre dos nodos, su independencia condicional está garantizada para cualquier distribución que factorice según el DAG. Si queda un camino activo, la estructura no garantiza independencia; los valores de las tablas todavía pueden producirla en casos particulares.

### 18.1 Las tres tripletas

![[ia29-tripletas-d-separacion.svg]]

**Lectura del diagrama:** compara las dos columnas de cada fila. Observar el centro bloquea cadenas y causas comunes; en un efecto común activa el camino. «Activo» indica que la independencia no está garantizada por la estructura.

| Patrón | Sin observar el nodo central | Observando el nodo central |
|---|---|---|
| Cadena $X\to Y\to Z$ | Camino activo | Camino bloqueado |
| Causa común $X\leftarrow Y\to Z$ | Camino activo | Camino bloqueado |
| Efecto común o colisionador $X\to Y\leftarrow Z$ | Camino bloqueado si tampoco se observa un descendiente de $Y$ | Camino activo |

En la cadena y la causa común, $X\perp Z\mid Y$. En el colisionador de tres nodos, $X\perp Z$ antes de observar el efecto. Observar $Y$, o un descendiente suyo, puede activar la relación entre las causas.

**Ejemplo propio de efecto común:** dos fallas independientes $X$ y $Z$ hacen que un indicador se encienda cuando ocurre al menos una: $Y=X\lor Z$. Si el indicador está encendido y descubrimos que $X=0$, necesariamente $Z=1$. Si sabemos que $X=1$, $Z$ ya no es necesario para explicar el indicador. Condicionar cambió la relación entre las causas.

En la red de alarma, $B\to A\leftarrow E$ tiene esta estructura. Con las CPT de la presentación:

$$P(+b\mid+a)\approx0.37355,$$

$$P(+b\mid+a,+e)\approx0.00327.$$

El terremoto ofrece una explicación alternativa de la alarma. Este efecto se conoce como **explicación alternativa** o *explaining away*; no es una ley de que toda observación de un colisionador siempre reduzca cualquier probabilidad.

![[ia29-colisionador-descendiente.svg]]

**Lectura del diagrama:** $Y$ sigue sin observarse, pero conocer su descendiente $D$ activa el camino $X\to Y\leftarrow Z$. Las marcas de evidencia no representan nuevas aristas.

### 18.2 Procedimiento para un grafo mayor

Para consultar $X\perp Z\mid\mathcal E$, con los extremos fuera del conjunto observado:

1. Busca los caminos entre $X$ y $Z$ ignorando temporalmente la dirección de las flechas.
2. En cada camino, examina las tripletas consecutivas.
3. Un nodo interno **no colisionador** bloquea el camino si está observado.
4. Un **colisionador**, donde ambas flechas del camino entran al nodo, bloquea el camino si ni él ni ninguno de sus descendientes está observado.
5. El camino está activo si ningún nodo interno lo bloquea.
6. Si **todos** los caminos están bloqueados, hay d-separación. Si al menos uno sigue activo, la independencia no está garantizada por el grafo.

Un nodo puede ser colisionador en un camino y no serlo en otro: importa la orientación de las dos aristas usadas en esa tripleta. Observar más variables no siempre bloquea más caminos, porque también puede activar colisionadores.

### Visualización · Evidencia, caminos y tripletas

<iframe src="independencia-d-separacion-interactiva.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Cómo estudiarla:** en la cadena, compara los extremos sin evidencia y luego observa el nodo central. Cambia a efecto común y repite: observar el centro activa el camino. En el ejemplo con descendiente, observa solo $D$ para activar el colisionador. Los valores numéricos son ejemplos didácticos, no CPT adicionales de la presentación.

**Si no carga:** observar el centro bloquea cadenas y causas comunes; observar un efecto común o alguno de sus descendientes puede activar un camino. La independencia se garantiza únicamente cuando todos los caminos entre los extremos quedan bloqueados.

## 19. Qué queda para la siguiente clase

*Diapositiva 32.* La presentación anuncia cómo resolver consultas y realizar inferencia. La continuación se encuentra en [[2026-10-06 IA - Redes bayesianas|Redes bayesianas del 6 de octubre]].

Ya podemos construir y leer un modelo; después interesará evitar repetir cálculos al responder muchas consultas. El ejemplo de enumeración de esta nota muestra el procedimiento básico, pero no desarrolla eliminación de variables ni muestreo.

## 20. Fórmulas que conviene poder reconstruir

| Operación | Expresión | Condición o interpretación |
|---|---|---|
| Normalizar pesos | $P(x)=w_x/\sum_{x'}w_{x'}$ | Pesos no negativos y suma positiva |
| Marginalizar | $P(x)=\sum_yP(x,y)$ | Sumar las alternativas de $Y$ |
| Condicionar | $P(x\mid y)=P(x,y)/P(y)$ | $P(y)>0$ |
| Regla del producto | $P(x,y)=P(x\mid y)P(y)$ | Descomponer una conjunta |
| Bayes | $P(x\mid y)=P(y\mid x)P(x)/P(y)$ | Invertir una condición |
| Independencia | $P(x,y)=P(x)P(y)$ | Para todas las asignaciones |
| Independencia condicional | $P(x,y\mid z)=P(x\mid z)P(y\mid z)$ | En cada estrato de $Z$ con masa positiva |
| Regla de la cadena | $P(x_1,\ldots,x_n)=\prod_iP(x_i\mid x_{<i})$ | No introduce independencia |
| Red bayesiana | $P(\mathbf x)=\prod_iP(x_i\mid\mathrm{pa}(X_i))$ | Requiere los supuestos del DAG |
| Enumeración | $P(Q\mid e)=\alpha\sum_{\mathbf h}P(Q,e,\mathbf h)$ | $\mathbf h$: ocultas; $\alpha=1/P(e)$ |

## 21. Errores frecuentes y preguntas de comprobación

- **Confundir marginal con condicional:** $P(\mathrm{cold})=0.5$ y $P(\mathrm{cold}\mid\mathrm{rain})=0.75$ responden preguntas distintas.
- **Invertir una condición sin Bayes:** $P(A\mid B)$ no suele ser $P(B\mid A)$.
- **Multiplicar marginales por costumbre:** se requiere independencia; para una CPT se multiplica según la factorización de la red.
- **Eliminar una condición sin justificarlo:** la regla de la cadena mantiene todas las anteriores; los supuestos permiten quitar algunas.
- **Confundir ausencia de arista con independencia:** puede haber caminos indirectos activos.
- **Afirmar que un camino activo prueba dependencia:** solamente demuestra que el grafo no garantiza independencia.
- **Interpretar flechas como prueba de causalidad:** es una afirmación adicional al modelo probabilístico.
- **Olvidar normalizar o condicionar sobre masa cero:** seleccionar filas no produce por sí solo una distribución posterior válida.

### Ejercicios con solución

1. **Conjunta de temperatura y clima:** calcula $P(\mathrm{hot}\mid\mathrm{sun})$. **Solución:** $0.4/(0.4+0.2)=2/3$.
2. **Independencia:** ¿las marginales $(0.5,0.5)$ y $(0.6,0.4)$ bastan para identificar la conjunta? **Solución:** no; las dos tablas de la diapositiva 14 tienen esas marginales y distinta dependencia.
3. **Tamaño:** ¿cuántas filas tiene una conjunta de diez variables con tres valores cada una? **Solución:** $3^{10}=59\,049$, con $59\,048$ parámetros libres sin otras restricciones.
4. **Alarma:** calcula $P(+a)$ sumando sobre las raíces. **Solución:** $0.001(0.002)(0.95)+0.001(0.998)(0.94)+0.999(0.002)(0.29)+0.999(0.998)(0.001)=0.002516442$.
5. **Alarma:** ¿$J$ y $M$ son independientes dado $A$? **Solución:** sí bajo el DAG; $P(j,m\mid a)=P(j\mid a)P(m\mid a)$. Sin observar $A$, esa independencia no está garantizada.
6. **Cadena $X\to Y\to Z\to W$:** ¿qué ocurre al observar $Z$ en una consulta entre $X$ y $W$? **Solución:** bloquea el único camino, así que $X\perp W\mid Z$.
7. **Colisionador $X\to Y\leftarrow Z$, $Y\to D$:** ¿observar $D$ puede relacionar $X$ y $Z$? **Solución:** sí, activa el colisionador porque $D$ es descendiente de $Y$; la independencia deja de estar garantizada.

### Autoevaluación

- [ ] Puedo construir una conjunta pequeña y verificar su normalización.
- [ ] Distingo sumar una variable de fijarla como evidencia.
- [ ] Derivo una condicional y la regla de Bayes a partir de la conjunta.
- [ ] Demuestro o refuto independencia usando las tablas.
- [ ] Separo la regla de la cadena de los supuestos de independencia.
- [ ] Leo padres y CPT, y calculo la probabilidad de un mundo completo.
- [ ] Identifico consulta, evidencia y variables ocultas.
- [ ] Explico por qué observar una cadena y observar un colisionador tienen efectos distintos.

## Correspondencia con toda la presentación

| Diapositivas | Contenido | Desarrollo en esta nota |
|---|---|---|
| 1–3 | Comentarios, portada y agenda | Introducción y §1; no se inventan respuestas de tarea |
| 4–6 | Transición e incertidumbre | §1 |
| 7 | Variables y dominios | §2 |
| 8 | Distribuciones individuales | §3 |
| 9 | Conjuntas y tamaño | §4 |
| 10 | Marginales | §5; apoyo condicional en §6 |
| 11–12 | Modelo, simplificación y consultas | §7 |
| 13 | Red de alarma, grafo y todas las CPT | §14 |
| 14 | Independencia y comparación de tablas | §8 |
| 15 | Independencia condicional | §9 |
| 16 | Regla de la cadena y simplificación | §10 |
| 17 | Dificultad de representar y aprender | §11 |
| 18–20 | Redes, tareas y semántica | §7 y §12 |
| 21 | Independencia como propiedad de la distribución | §8–9 |
| 22 | Fuego, humo y alarma | §15.1 |
| 23 | Repetición de cadena e independencia | §10 |
| 24 | Nodos, aristas y ejemplo de caries | §12 y §15.2 |
| 25 | DAG y tablas condicionales | §12 |
| 26 | Factorización y capacidad de representación | §13 |
| 27 | Supuestos locales y adicionales | §13 |
| 28 | Cadena de cuatro nodos | §16 |
| 29 | Independencia: prueba y contraejemplo | §17 |
| 30 | Introducción a d-separación | §18 |
| 31 | Cadena presión–lluvia–tráfico y demostración | §17 |
| 32 | Continuación con inferencia | §19 |

## Referencias y alcance

- **Material de clase:** [[AI 13 introducción agentes probabilísticos.pdf|AI 13: introducción a agentes probabilísticos]], 32 diapositivas. La portada dice «Clase 13»; la fecha de esta nota sigue el registro del vault.
- **Berkeley CS 188:** [textbook](https://inst.eecs.berkeley.edu/~cs188/textbook/), §§[6.1](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/probability.html), [6.2](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/inference.html), [6.3](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/representation.html), [6.4](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/structure.html) y [6.5](https://inst.eecs.berkeley.edu/~cs188/textbook/bayes-nets/d-separation.html). El vínculo con decisiones se apoya en [§7.1](https://inst.eecs.berkeley.edu/~cs188/textbook/vpis/utilities.html). Consultado el 6 de octubre de 2026.
- Las visualizaciones usan las tablas de la presentación para temperatura/clima y alarma. Sus controles exploran el modelo; el interpolador de dependencia y los modelos numéricos de tripletas son construcciones didácticas.
- El texto de CS 188 se publica con licencia [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Estas explicaciones son una elaboración de estudio, con atribución a los materiales señalados.

## Resumen después de clase

Un agente probabilístico representa incertidumbre mediante distribuciones sobre mundos posibles. La conjunta permite responder consultas mediante sumas y condicionamiento, pero crece exponencialmente con el número de variables. Las independencias condicionales permiten factorizarla en tablas locales organizadas por un DAG. Una red bayesiana combina esas tablas y supuestos; las conexiones indirectas y la evidencia determinan qué independencias puede garantizar. La clase termina con cadenas y la introducción a d-separación, preparando la inferencia de las siguientes sesiones.
