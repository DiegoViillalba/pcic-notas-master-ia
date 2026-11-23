---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: 2026-11-03
unidad: Aprendizaje automático y decisiones secuenciales
profesor: Carlos Hernández
estado: procesada
aliases:
  - Aprendizaje por refuerzo - 3 de noviembre
referencias:
  - "[[AI 21 Aprendizaje por refuerzo.pdf]]"
  - https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/
  - https://inst.eecs.berkeley.edu/~cs188/textbook/rl/
tags:
  - clase
  - inteligencia-artificial
  - aprendizaje-por-refuerzo
  - mdp
  - bellman
  - programacion-dinamica
---

# Aprendizaje por refuerzo: de actuar a evaluar y mejorar políticas

> [!summary] Pregunta central
> ¿Cómo elegimos una acción cuando cambia tanto la recompensa inmediata como los estados y las oportunidades que tendremos después?

**Fecha del apunte: martes 3 de noviembre de 2026.** Se construye a partir de las **24 diapositivas** de «Clase 21: aprendizaje por refuerzo». La numeración de la presentación y la de sesiones del plan son distintas. Continúa en [[2026-11-05 IA - Aprendizaje por refuerzo II|la clase del 5 de noviembre: Monte Carlo, exploración, Q-learning y aproximación]].

**Alcance.** El material de clase desarrolla procesos de decisión de Markov (MDP), políticas, descuento, valores, Bellman, evaluación y mejora. Las derivaciones, ejercicios, SVG y laboratorios de esta nota son elaboración didáctica. Las conexiones con **Berkeley CS 188**, el curso que ya venimos usando, se enlazan donde ayudan. La sección de aprendizaje por muestras y Q-learning es un **complemento preparatorio**: la última diapositiva anuncia «RL 2».

## Material de clase y ruta de estudio

![[AI 21 Aprendizaje por refuerzo.pdf]]

| Pregunta | Diapositivas | Secciones de esta nota |
|---|---:|---|
| ¿Qué significa aprender mediante recompensas? | 1–3 | 1 |
| ¿Cómo describo el mundo y mi comportamiento? | 4–8 | 2–3 |
| ¿Cómo comparo recompensas presentes y futuras? | 9–11 | 4 |
| ¿Qué significan V, Q y la política óptima? | 12–16 | 5–6 |
| ¿Cómo calculo el valor de una política? | 17–19 | 7 |
| ¿Cuándo existen valores óptimos y convergen las iteraciones? | 20–21 | 8–9 |
| ¿Cómo uso los valores para mejorar lo que hago? | 22–23 | 10 |
| ¿Qué sigue si no conozco el modelo? | 24 | 11, complemento Berkeley |

Recorrido recomendado: entender el automóvil → experimentar con el descuento → hacer un respaldo de Bellman a mano → evaluar una política fija → mejorarla → distinguir planificación de aprendizaje.

## 1. Intuición: aprender a actuar es aprender consecuencias

En [[2026-10-27 IA - Aprendizaje supervisado y clasificacion|aprendizaje supervisado]] recibimos pares entrada–respuesta. Aquí una recompensa puede decirnos que una consecuencia fue favorable, sin revelar cuál era la mejor acción. Además, la decisión de hoy cambia los datos que veremos mañana. Si un automóvil acelera, avanza más, pero puede calentar su motor; una decisión rentable ahora puede eliminar oportunidades futuras.

![Aprender al actuar](ia21-ciclo-agente.svg)

**Lectura del diagrama:** en el instante $t$, el agente observa $S_t$, elige $A_t$ y recibe $R_{t+1}$ y $S_{t+1}$. Usaremos siempre esa convención: la recompensa con índice $t+1$ corresponde a la transición que comienza en $t$.

Una experiencia elemental es

$$
(S_t,A_t,R_{t+1},S_{t+1}).
$$

La recompensa evalúa una transición. La **política** determina cómo actuar. La **función de valor** estima cuán conveniente será comenzar en cierto estado y continuar actuando. Son tres objetos distintos.

> [!example] Recompensa alta no implica buena decisión
> «Fast» desde Cool da $+2$, frente a $+1$ de «Slow». Pero desde Warm, «Fast» lleva a Overheated y da $-10$. Una regla que solo busca velocidad ignora el estado y las consecuencias.

## 2. De la intuición al modelo: un MDP

### 2.1 El estado debe resumir lo necesario para decidir

**Intuición.** Si conocemos la temperatura actual del motor y la acción que aplicaremos, el modelo de clase no necesita reconstruir toda la historia del automóvil para predecir su próximo estado.

La **propiedad de Markov** exige que, dado el estado y la acción presentes, la historia no aporte información adicional sobre el siguiente estado y recompensa:

$$
\Pr(S_{t+1}=s',R_{t+1}=r\mid H_t,A_t=a)
=\Pr(S_{t+1}=s',R_{t+1}=r\mid S_t=s,A_t=a),
$$

donde $H_t=(S_0,A_0,R_1,\ldots,S_t)$ es la historia observada. Esto es una **hipótesis sobre la representación del estado**, no la afirmación de que todo sistema real carece de memoria. Si el desgaste acumulado cambia la dinámica aun con igual temperatura, habría que incluirlo en el estado.

### 2.2 Los ingredientes

Para el caso finito, estacionario y descontado que usaremos:

$$
\mathcal M=(\mathcal S,\{\mathcal A(s)\}_{s\in\mathcal S},T,R,\gamma,\rho_0).
$$

| Símbolo | Significado | Restricción o convención |
|---|---|---|
| $\mathcal S$ | Estados | El agente observa el estado del MDP |
| $\mathcal A(s)$ | Acciones disponibles en $s$ | Puede depender del estado |
| $T(s,a,s')$ | $\Pr(S_{t+1}=s'\mid S_t=s,A_t=a)$ | $T\geq0$, $\sum_{s'}T(s,a,s')=1$ |
| $R(s,a,s')$ | Recompensa esperada de esa transición | Puede ser negativa |
| $\gamma$ | Descuento | En el caso principal, $0\leq\gamma<1$ |
| $\rho_0$ | Distribución inicial | Un estado inicial fijo es un caso particular |

Si las recompensas son aleatorias, $R(s,a,s')=\mathbb E[R_{t+1}\mid s,a,s']$. La distribución conjunta $p(s',r\mid s,a)$ de la diapositiva 18 es una formulación más general; al tomar expectativas recuperamos la notación de la tabla.

**MDP y RL.** Un MDP describe el problema de decisión. Si nos dan $T$ y $R$, podemos **planificar**. Si desconocemos el modelo y debemos aprender mediante interacción, estamos en **aprendizaje por refuerzo**. La presentación introduce RL estudiando primero su modelo matemático.

Berkeley desarrolla esta formulación y la propiedad de Markov en [CS 188, §4.1](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/markov-decision-processes.html).

## 3. Ejemplo conductor: el automóvil

*Diapositivas 6–8; reconstrucción del grafo original.* Escribamos $C=$ Cool, $W=$ Warm y $O=$ Overheated. Las acciones son Slow y Fast. Usaremos $C$ como estado inicial para los ejemplos, aunque calcularemos valores para ambos estados no terminales.

![Modelo completo del automóvil](ia21-mdp-auto.svg)

| Estado | Acción | Sucesor | Probabilidad | Recompensa |
|---|---|---|---:|---:|
| $C$ | Slow | $C$ | $1$ | $+1$ |
| $C$ | Fast | $C$ | $0.5$ | $+2$ |
| $C$ | Fast | $W$ | $0.5$ | $+2$ |
| $W$ | Slow | $C$ | $0.5$ | $+1$ |
| $W$ | Slow | $W$ | $0.5$ | $+1$ |
| $W$ | Fast | $O$ | $1$ | $-10$ |

$O$ es terminal: su valor de continuación es cero. La penalización $-10$ se cobra **al entrar** en él. Si lo representamos como absorbente para completar una matriz, añadimos una transición ficticia $O\to O$ de recompensa cero; no repetimos la penalización.

### 3.1 Una política es una regla contingente

Un plan como «Fast, Fast, Slow» ignora que el primer Fast puede dejarnos en dos estados distintos. Una política permite reaccionar al estado alcanzado:

$$
\pi(C)=\text{Fast},\qquad \pi(W)=\text{Slow}.
$$

Una política **determinista** elige una acción $\pi(s)$. Una política **estocástica** especifica

$$
\pi(a\mid s)\geq0,\qquad \sum_{a\in\mathcal A(s)}\pi(a\mid s)=1.
$$

Por ejemplo, $\pi(\text{Fast}\mid C)=0.8$. La incertidumbre del entorno está en $T$; la aleatoriedad de nuestras decisiones está en $\pi$. Incluso una política determinista puede generar trayectorias aleatorias.

Una tabla de política explícita puede ejecutarse como un agente de reflejo: observar el estado y consultar la acción. Esa ejecución sencilla puede ser el resultado de una planificación extensa.

## 4. ¿Qué queremos maximizar? El retorno

### 4.1 De premios aislados a una suma temporal

La diapositiva 9 compara $[1,2,2]$ con $[2,3,4]$: con suma sin descuento ganan $9$ frente a $5$. Al comparar $[0,0,1]$ con $[1,0,0]$, ambas suman uno, pero un descuento positivo menor que uno favorece recibirlo antes.

![Descomposición del retorno](ia21-descuento.svg)

El **retorno descontado** desde $t$ es

$$
G_t=\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}
=R_{t+1}+\gamma G_{t+1}.
$$

La segunda igualdad sale de separar el primer término y factorizar $\gamma$ en el resto. Es el paso matemático que hará posible Bellman.

Para un episodio que termina en el tiempo $\tau$:

$$
G_t=\sum_{k=0}^{\tau-t-1}\gamma^kR_{t+k+1}.
$$

$\gamma=0$ atiende solo a la recompensa inmediata. Un $\gamma$ cercano a uno da más peso a consecuencias lejanas. **Descontar no equivale a explorar**: es una elección del objetivo temporal.

### 4.2 Por qué el descuento evita valores infinitos

Si $|R_{t+1}|\leq R_{\max}^{\mathrm{abs}}$ y $0\leq\gamma<1$, entonces

$$
|G_t|\leq\sum_{k=0}^{\infty}\gamma^k|R_{t+k+1}|
\leq\frac{R_{\max}^{\mathrm{abs}}}{1-\gamma}.
$$

En el automóvil, $R_{\max}^{\mathrm{abs}}=10$. Con $\gamma=0.9$, $|G_t|\leq100$. Es una cota general, no el valor exacto del automóvil.

Hay otras opciones: fijar un horizonte finito o formular un problema episódico con terminación y retorno bien definidos. En un horizonte finito, la mejor acción puede depender del **tiempo restante**: usamos $\pi_h(s)$ o incorporamos $h$ al estado.

> [!warning] Un estado terminal disponible no garantiza terminación
> En el automóvil, Slow desde Cool permanece allí para siempre. La política $\pi(C)=\text{Fast},\pi(W)=\text{Slow}$ tampoco llega a Overheated. Con $\gamma=1$ acumula recompensas positivas indefinidamente. Para garantizar un retorno esperado finito sin descuento hacen falta supuestos adicionales; con recompensas acotadas, un tiempo esperado de terminación finito es una condición suficiente. Terminar casi seguramente, por sí solo, no garantiza que ese tiempo esperado sea finito.

### Laboratorio 1. Cambiar cuánto pesa el futuro

<iframe src="ia21-lab-descuento.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Idea que debe quedar aunque el laboratorio no cargue:** una recompensa $m$ recibida después de $d$ demoras vale $\gamma^d m$. El laboratorio compara secuencias editables y dibuja la contribución de cada instante.

1. Usa $A=[1,0,0]$ y $B=[0,0,2]$. Antes de mover $\gamma$, predice cuál gana.
2. La frontera es $1=2\gamma^2$, es decir, $\gamma=1/\sqrt2\approx0.7071$.
3. Prueba un flujo constante de $+1$: con $\gamma=0.5$ su valor infinito es $2$; con $0.9$ es $10$; con $1$ diverge. Una suma de pocos términos nunca demuestra que el retorno infinito sea finito.

## 5. V, Q y política: tres preguntas diferentes

*Diapositivas 12–13 y 16.* Para una política fija $\pi$:

$$
V^\pi(s)=\mathbb E_\pi[G_t\mid S_t=s],
$$

$$
Q^\pi(s,a)=\mathbb E[G_t\mid S_t=s,A_t=a,\text{ seguir }\pi\text{ después}].
$$

| Objeto | Pregunta que responde |
|---|---|
| $R(s,a,s')$ | ¿Qué obtengo en esta transición? |
| $V^\pi(s)$ | ¿Qué espero obtener comenzando en $s$ y siguiendo $\pi$? |
| $Q^\pi(s,a)$ | ¿Qué espero obtener si primero fuerzo $a$ y después sigo $\pi$? |
| $\pi(s)$ | ¿Qué acción elijo en $s$? |

La versión óptima toma el mejor comportamiento admisible:

$$
V^*(s)=\max_\pi V^\pi(s),\qquad Q^*(s,a)=\max_\pi Q^\pi(s,a).
$$

En el caso finito descontado esos máximos se alcanzan. Entonces

$$
V^*(s)=\max_aQ^*(s,a),\qquad
\pi^*(s)\in\operatorname*{arg\,max}_aQ^*(s,a).
$$

**Máximo y argmáximo:** el primero es un número; el segundo es el conjunto de acciones que alcanzan ese número. Si hay empate, elegimos una de ellas o distribuimos probabilidad solo entre acciones maximizadoras. No asignamos probabilidad uno a cada acción empatada: dejaría de ser una distribución.

## 6. Bellman: presente más continuación

### 6.1 Primero, evaluar un comportamiento fijo

Aplicamos $G_t=R_{t+1}+\gamma G_{t+1}$ y condicionamos por la acción y el sucesor:

$$
\begin{aligned}
V^\pi(s)
&=\mathbb E_\pi[R_{t+1}+\gamma G_{t+1}\mid S_t=s]\\
&=\sum_a\pi(a\mid s)\sum_{s'}T(s,a,s')
\left[R(s,a,s')+\gamma V^\pi(s')\right].
\end{aligned}
$$

La suma interna promedia las consecuencias del entorno; la externa promedia las acciones de la política. Con una política determinista solo queda el término $a=\pi(s)$.

Si preferimos una recompensa dependiente solo de $(s,a)$, debemos definir

$$
r(s,a)=\sum_{s'}T(s,a,s')R(s,a,s'),
$$

y obtenemos la expresión de las diapositivas 17 y 19:

$$
V^\pi(s)=\sum_a\pi(a\mid s)\left[r(s,a)+\gamma\sum_{s'}T(s,a,s')V^\pi(s')\right].
$$

### 6.2 Después, elegir lo mejor

Si después de esta transición continuamos óptimamente:

$$
Q^*(s,a)=\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V^*(s')\right].
$$

Elegir la primera acción óptima da la **ecuación de optimalidad de Bellman**:

$$
\boxed{V^*(s)=\max_{a\in\mathcal A(s)}\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V^*(s')\right].}
$$

![Una actualización de Bellman](ia21-bellman-backup.svg)

**Lectura:** primero fijamos una acción, luego promediamos sus posibles resultados; finalmente comparamos acciones. El agente elige $a$, pero no elige qué $s'$ ocurre. Por eso $\max_a\mathbb E[\cdot\mid a]$ no se sustituye por una expectativa de máximos que permitiera decidir después de observar el azar.

La conexión con [[2026-09-08 IA - Incertidumbre y Expectimax|expectimax]] es directa: el nodo del estado maximiza, el nodo $(s,a)$ calcula una esperanza. La ventaja de programación dinámica es guardar un valor por estado en vez de volver a expandir cada historia que llega al mismo estado. Berkeley presenta esta conexión en [CS 188, §4.2](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/solve.html).

## 7. Evaluar una política: «¿qué pasa si sigo esta regla?»

*Diapositivas 17–19.* Fijamos

$$
\pi(C)=\text{Fast},\qquad\pi(W)=\text{Slow},\qquad V^\pi(O)=0.
$$

Sus ecuaciones son

$$
\begin{aligned}
V^\pi(C)&=2+\frac\gamma2V^\pi(C)+\frac\gamma2V^\pi(W),\\
V^\pi(W)&=1+\frac\gamma2V^\pi(C)+\frac\gamma2V^\pi(W).
\end{aligned}
$$

### 7.1 Resolver las ecuaciones exactamente

Restando obtenemos $V^\pi(C)-V^\pi(W)=1$. Sumando:

$$
(1-\gamma)\left[V^\pi(C)+V^\pi(W)\right]=3.
$$

Para $0\leq\gamma<1$:

$$
\boxed{V^\pi(C)=\frac{2-\gamma/2}{1-\gamma},\qquad
V^\pi(W)=\frac{1+\gamma/2}{1-\gamma}.}
$$

Con $\gamma=0.9$, $V^\pi(C)=15.5$ y $V^\pi(W)=14.5$. Con $\gamma=0.5$, son $3.5$ y $2.5$.

En forma matricial, para estados no terminales:

$$
V^\pi=r_\pi+\gamma P_\pi V^\pi,
\qquad (I-\gamma P_\pi)V^\pi=r_\pi,
$$

$$
P_\pi=\begin{pmatrix}0.5&0.5\\0.5&0.5\end{pmatrix},
\qquad r_\pi=\begin{pmatrix}2\\1\end{pmatrix}.
$$

Con $\gamma<1$ la solución es única. En una implementación se resuelve el sistema lineal; no hace falta formar explícitamente una inversa.

### 7.2 Evaluación iterativa: dejar que la continuación se propague

Comenzamos con $V_0^\pi=0$ y repetimos el lado derecho de Bellman usando **el vector completo del barrido anterior**:

$$
V_{k+1}^\pi(s)=\sum_a\pi(a\mid s)\sum_{s'}T(s,a,s')
\left[R(s,a,s')+\gamma V_k^\pi(s')\right].
$$

| Barrido $k$ | $V_k^\pi(C)$, $\gamma=0.9$ | $V_k^\pi(W)$, $\gamma=0.9$ | $V_k^\pi(C)$, $\gamma=1$ | $V_k^\pi(W)$, $\gamma=1$ |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 2 | 1 | 2 | 1 |
| 2 | 3.35 | 2.35 | 3.5 | 2.5 |
| 3 | 4.565 | 3.565 | 5 | 4 |
| Límite | 15.5 | 14.5 | $+\infty$ | $+\infty$ |

> [!warning] Qué muestran realmente los números de la diapositiva 19
> $V_1=(2,1,0)$ y $V_2=(3.5,2.5,0)$ son correctos con $\gamma=1$ y actualización sincrónica. Representan retornos de uno y dos pasos; **no** valores de una política infinita ya convergida. Para $k\geq1$, $V_k(C)=1.5k+0.5$ y $V_k(W)=1.5k-0.5$. Las ecuaciones estacionarias con $\gamma=1$ no tienen una solución finita para esta política.

La diapositiva 18 muestra una evaluación que actualiza valores **en el mismo vector**. Es una variante válida bajo condiciones apropiadas, pero sus valores intermedios pueden diferir. Para reproducir la diapositiva 19 y conservar la interpretación de horizonte $k$, aquí usamos dos vectores.

## 8. Encontrar valores óptimos: iteración de valores

**Intuición.** En vez de comprometernos con una regla, en cada respaldo comparamos todas las acciones. Inicializamos $V_0(s)=0$, dejamos $V_k(O)=0$ y hacemos

$$
Q_{k+1}(s,a)=\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V_k(s')\right],
$$

$$
\boxed{V_{k+1}(s)=\max_a Q_{k+1}(s,a).}
$$

$V_k(s)$ es el mejor retorno de los siguientes **$k$ pasos**, con valor terminal de horizonte cero. La ecuación de Bellman caracteriza un punto fijo; esta actualización es un algoritmo para aproximarlo.

### 8.1 Un respaldo completo, sin saltos

Con $\gamma=0.9$ y $V_0=0$:

$$
\begin{array}{ll}
Q_1(C,\text{Slow})=1,&Q_1(C,\text{Fast})=2,\\
Q_1(W,\text{Slow})=1,&Q_1(W,\text{Fast})=-10.
\end{array}
$$

Así $V_1=(2,1,0)$. Usando ese vector:

$$
\begin{aligned}
Q_2(C,\text{Slow})&=1+0.9(2)=2.8,\\
Q_2(C,\text{Fast})&=0.5[2+0.9(2)]+0.5[2+0.9(1)]=3.35,\\
Q_2(W,\text{Slow})&=0.5[1+0.9(2)]+0.5[1+0.9(1)]=2.35,\\
Q_2(W,\text{Fast})&=-10+0.9(0)=-10.
\end{aligned}
$$

Por lo tanto, $V_2=(3.35,2.35,0)$ y las acciones elegidas son Fast en Cool, Slow en Warm. En este ejemplo coinciden desde el principio con la política fija evaluada antes; **en general, evaluación de políticas e iteración de valores producen resultados distintos**.

Pseudocódigo sincrónico:

```text
V ← cero para todos los estados
repetir:
    anterior ← copia de V
    para cada estado no terminal s:
        para cada acción a:
            Q[a] ← Σ_s' T(s,a,s') [R(s,a,s') + γ anterior[s']]
        V[s] ← máximo_a Q[a]
    Δ ← máximo_s |V[s] − anterior[s]|
hasta cumplir el criterio de precisión
```

Después extraemos la política con **otro respaldo de un paso**:

$$
\pi_V(s)\in\operatorname*{arg\,max}_a\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V(s')\right].
$$

Si solo disponemos de $V(s)$, elegir una acción todavía requiere el modelo. Si disponemos de $Q(s,a)$, basta comparar las acciones. Véase [Berkeley CS 188, §4.3](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/value-iteration.html).

### Laboratorio 2. Bellman sobre el automóvil

<iframe src="ia21-lab-bellman.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Idea central:** un barrido usa únicamente los valores anteriores. El laboratorio deja alternar entre evaluar una política fija y maximizar, muestra los cuatro valores de acción usados en el último respaldo y permite inspeccionar el cálculo de una acción.

1. Con $\gamma=0.9$ y maximización, verifica $V_1=(2,1,0)$ y $V_2=(3.35,2.35,0)$.
2. Cambia a evaluación y elige Slow en ambos estados: el límite debe ser $(10,10,0)$.
3. Selecciona Fast en Cool y Slow en Warm con $\gamma=1$: reproduce la diapositiva 19 y observa que los valores siguen aumentando. El laboratorio permite barridos finitos, pero no declara convergencia.
4. Regresa a $0.9$ y ejecuta más barridos: el resultado debe acercarse a $(15.5,14.5,0)$.

## 9. Por qué converge: los errores futuros se atenúan

*Diapositiva 21, con desarrollo matemático.* Definamos el operador

$$
(BV)(s)=\max_a\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V(s')\right].
$$

La norma infinito mide el mayor error entre estados:

$$
\|V-W\|_\infty=\max_s|V(s)-W(s)|.
$$

Al comparar dos respaldos, las recompensas se cancelan. El promedio ponderado no puede superar el mayor error y el descuento lo multiplica por $\gamma$:

$$
\begin{aligned}
|(BV)(s)-(BW)(s)|
&\leq\max_a\left|\gamma\sum_{s'}T(s,a,s')[V(s')-W(s')]\right|\\
&\leq\gamma\|V-W\|_\infty.
\end{aligned}
$$

Así,

$$
\boxed{\|BV-BW\|_\infty\leq\gamma\|V-W\|_\infty.}
$$

Para $\gamma<1$, es una **contracción**: existe un único punto fijo $V^*$ y

$$
\|V_k-V^*\|_\infty\leq\gamma^k\|V_0-V^*\|_\infty.
$$

La misma idea funciona para el operador de una política fija. Esta demostración precisa el bosquejo de convergencia de clase. Con $\gamma=1$, el argumento deja de contraer y no basta para demostrar convergencia.

### 9.1 Pasar de «cambió poco» a una cota de error

Para iteración sincrónica, si

$$
\Delta_k=\|V_k-V_{k-1}\|_\infty,
$$

la suma de los cambios restantes se acota por una serie geométrica:

$$
\boxed{\|V^*-V_k\|_\infty\leq\frac{\gamma}{1-\gamma}\Delta_k.}
$$

Con $\gamma=0.9$, un cambio de $0.001$ certifica error en los valores de a lo sumo $0.009$. Esto no es directamente una cota del rendimiento de cualquier política extraída. Si usamos el **residuo** $\|BV-V\|_\infty$, la cota correspondiente es $\|V^*-V\|_\infty\leq\|BV-V\|_\infty/(1-\gamma)$.

Otro punto de vista, con $V_0=0$, consiste en acotar la cola omitida del retorno:

$$
\|V^*-V_k\|_\infty\leq\frac{\gamma^kR_{\max}^{\mathrm{abs}}}{1-\gamma}.
$$

Si todas las trayectorias terminan en a lo sumo $M$ pasos y la frontera terminal está correctamente definida, $M$ respaldos bastan. Ese argumento de horizonte acotado es distinto del de contracción.

## 10. Mejorar políticas: «¿puedo actuar mejor con lo que ya sé?»

*Diapositivas 20, 22–23.* Definimos dominancia por

$$
\pi\succeq\pi'\quad\Longleftrightarrow\quad V^\pi(s)\geq V^{\pi'}(s)\quad\text{para todo }s.
$$

Dos políticas pueden ser incomparables si una gana en unos estados y pierde en otros. Además, políticas distintas pueden tener idéntico valor: formalmente, esta relación es un **preorden** sobre políticas, y se convierte en orden parcial al identificar políticas con el mismo vector de valor.

En un MDP con estados y acciones finitos, recompensas acotadas y descuento $\gamma<1$, existe una política óptima **determinista y estacionaria** que maximiza el valor para todos los estados. Las afirmaciones de las diapositivas 16 y 20 deben leerse dentro de estos supuestos. En horizonte finito puede hacer falta depender del tiempo; en problemas generales o con restricciones adicionales no se trasladan automáticamente.

### 10.1 La mejora se hace con Q de la política actual

Primero calculamos $V^\pi$. Luego

$$
Q^\pi(s,a)=\sum_{s'}T(s,a,s')\left[R(s,a,s')+\gamma V^\pi(s')\right],
$$

$$
\pi_{\mathrm{nueva}}(s)\in\operatorname*{arg\,max}_aQ^\pi(s,a).
$$

Como la acción actual también estaba disponible,

$$
Q^\pi(s,\pi_{\mathrm{nueva}}(s))\geq V^\pi(s).
$$

**Por qué mejora a largo plazo:** el operador $B_{\pi_{\mathrm{nueva}}}$ es monótono, de modo que

$$
V^\pi\leq B_{\pi_{\mathrm{nueva}}}V^\pi
\leq B_{\pi_{\mathrm{nueva}}}^2V^\pi\leq\cdots
\longrightarrow V^{\pi_{\mathrm{nueva}}}.
$$

Por tanto $V^{\pi_{\mathrm{nueva}}}\geq V^\pi$ en todos los estados. Evaluar exactamente y mejorar repetidamente produce **iteración de políticas**. Conservar la acción actual si ya es maximizadora evita cambios innecesarios por empates.

![Ciclo de iteración de políticas](ia21-iteracion-politicas.svg)

**Idea del diagrama:** evaluar mantiene fija la política; mejorar mantiene fijo el vector de valor recién calculado. Si la política ya es codiciosa con respecto a su propio valor, satisface Bellman de optimalidad y es óptima. Berkeley organiza este ciclo en [CS 188, §4.4](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/policies-iteration.html).

### 10.2 Ejemplo completo con γ = 0.9

Comenzamos con $\pi_0=(\text{Slow},\text{Slow})$. Entonces $V^{\pi_0}(C)=V^{\pi_0}(W)=10$. La mejora compara

$$
\begin{array}{c|rr|l}
&\text{Slow}&\text{Fast}&\text{Acción elegida}\\\hline
C&1+0.9(10)=10&2+0.9(10)=11&\text{Fast}\\
W&1+0.9(10)=10&-10&\text{Slow}
\end{array}
$$

Obtenemos $\pi_1=(\text{Fast},\text{Slow})$. Al evaluarla, sus valores son $(15.5,14.5)$. Una nueva mejora da

$$
\begin{array}{c|rr|l}
&\text{Slow}&\text{Fast}&\text{Acción elegida}\\\hline
C&14.95&15.5&\text{Fast}\\
W&14.5&-10&\text{Slow}
\end{array}
$$

La política permanece igual: hemos verificado optimalidad en este MDP.

### Laboratorio 3. Evaluar, mejorar y comprobar estabilidad

<iframe src="ia21-lab-politicas.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Idea central:** partir de una política mala no impide mejorar. El laboratorio resuelve exactamente las dos ecuaciones no terminales y alterna evaluación y mejora, en lugar de mezclar ambas operaciones.

1. Con $\gamma=0.9$, comienza con Slow–Slow y reproduce las dos tablas anteriores.
2. Comienza con Fast–Fast. Su evaluación inicial es $V(C)=-50/11\approx-4.5455$, $V(W)=-10$. Observa qué acciones cambia la primera mejora.
3. Evalúa las cuatro políticas y comprueba que Fast–Slow domina a todas para este descuento.

| Algoritmo | Qué fija | Operación clave | Qué obtiene |
|---|---|---|---|
| Evaluación de políticas | $\pi$ | Esperanza según $\pi$ y $T$ | $V^\pi$ |
| Iteración de valores | Modelo $T,R$ | Respaldo con máximo en cada barrido | Aproximaciones a $V^*$ |
| Iteración de políticas | Modelo $T,R$ | Alterna evaluación y mejora | Política óptima |

Con transiciones densas, un barrido de valores cuesta $O(|\mathcal S|^2|\mathcal A|)$. Si cada acción tiene pocos sucesores, sumamos solo los de probabilidad no nula. En iteración de políticas hay además que resolver o aproximar un sistema por evaluación; menos mejoras de política no garantiza por sí solo menor costo total.

## 11. Complemento Berkeley: del modelo conocido a aprender de muestras

**Esta sección prepara la continuación; no se atribuye a las 24 diapositivas.** Hasta aquí conocemos las probabilidades y recompensas del automóvil. El problema de RL aparece cuando el agente necesita aprender sin recibir esas tablas. Berkeley hace esta separación explícita en [§5.1](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/rl.html).

![Del modelo a las muestras](ia21-planificacion-aprendizaje.svg)

### 11.1 Dos caminos para usar la experiencia

**Aprender un modelo:** contar transiciones permite estimar

$$
\widehat T(s,a,s')=\frac{N(s,a,s')}{N(s,a)},\qquad N(s,a)>0,
$$

y promediar recompensas para estimar $R$. Después se planifica sobre el modelo estimado. Si nunca hemos probado $(s,a)$, el cociente no está definido: necesitamos exploración o una regla previa. Este es el enfoque de [CS 188, §5.2](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/mbl.html).

**Aprender valores directamente:** una transición observada proporciona una muestra del objetivo «recompensa más continuación». Por ejemplo, **TD(0)** evalúa una política mediante

$$
V(s)\leftarrow V(s)+\alpha\left[r+\gamma V(s')-V(s)\right].
$$

En **Q-learning** aprendemos sobre acciones:

$$
\underbrace{y}_{\text{objetivo de una muestra}}=r+\gamma\max_{a'}Q(s',a'),
$$

$$
\boxed{Q(s,a)\leftarrow Q(s,a)+\alpha\left[y-Q(s,a)\right].}
$$

Si $s'$ es terminal, usamos $y=r$. Solo cambia la entrada visitada. $\alpha$ regula cuánto corregimos una estimación; $\gamma$ regula cuánto valoramos el futuro. Son parámetros distintos. Berkeley desarrolla ambos métodos en [§5.3](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/mfl.html).

### 11.2 Explorar para poder comparar

Una política $\varepsilon$-greedy explota una acción maximizadora con probabilidad $1-\varepsilon$ y, con probabilidad $\varepsilon$, elige uniformemente entre todas las acciones. Con dos acciones y máximo único, la mejor se elige con probabilidad $1-\varepsilon+\varepsilon/2$; la otra, con $\varepsilon/2$.

Un número finito de experiencias no garantiza haber aprendido el óptimo. Para la garantía clásica de Q-learning tabular descontado hacen falta, entre otras condiciones, visitar suficientemente todos los pares y tasas por par con $\sum_n\alpha_n=\infty$, $\sum_n\alpha_n^2<\infty$. Una tasa constante, útil para experimentar, no cumple esa garantía general. Véase la discusión de exploración en [CS 188, §5.4](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/eae.html).

### Laboratorio 4. Una muestra, un error y una actualización de Q

<iframe src="ia21-lab-qlearning.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

**Idea central:** el simulador usa el MDP para producir experiencias, pero la regla que actualiza $Q$ recibe únicamente $(s,a,r,s')$. Puedes tomar acciones manuales o dejar actuar a una política $\varepsilon$-greedy. La tasa es constante y el experimento no certifica convergencia.

1. Reinicia con $Q=0$, $\alpha=0.5$, $\gamma=0.9$; ejecuta Fast desde Cool. Sea cual sea el sucesor, $r=2$, $y=2$ y la nueva entrada es $Q(C,\text{Fast})=1$.
2. Reinicia y ejecuta Slow desde Cool: la entrada nueva debe ser $0.5$.
3. Ejecuta Fast desde Warm: el objetivo es $-10$, sin continuación del terminal.
4. Compara exploración cero y positiva. La semilla hace repetible cada experimento con iguales parámetros y acciones; cambiar la exploración cambia las trayectorias.

## 12. Errores frecuentes que conviene detectar al estudiar

| Confusión | Corrección |
|---|---|
| «La mejor acción da la recompensa inmediata mayor» | Se maximiza recompensa más continuación esperada |
| «El entorno elige la peor rama» | En un MDP promediamos con $T$; no es minimax |
| «Q es una probabilidad» | Q es un retorno esperado y puede ser negativo |
| «Una política es una trayectoria fija» | Es una regla para cada estado; la trayectoria depende del azar |
| «Como hay terminal, toda política termina» | Puede haber ciclos que nunca lo alcancen |
| «V terminal debe ser −10» | Aquí $-10$ se cobra al entrar; la continuación terminal es cero |
| «Los dos barridos de γ = 1 muestran convergencia» | Son valores de horizontes finitos, crecientes sin límite |
| «Evaluar incluye elegir las mejores acciones» | Evaluar fija $\pi$; mejorar compara acciones |
| «Iteración de valores ya aprende del entorno» | Usa el modelo conocido; las muestras aparecen en RL |
| «La mejor política siempre es única» | Puede haber empates y varias políticas con igual valor |

## 13. Autoevaluación con soluciones

### A. Reconstruir una distribución

Desde Warm con Slow, ¿cuáles son los posibles sucesores? ¿Cuánto suma su probabilidad?

> [!answer]- Solución
> Cool y Warm con $0.5$ cada uno; suman uno. La recompensa es $+1$ en ambos casos. Overheated no es sucesor de esa pareja estado–acción.

### B. Hacer un respaldo a mano

Con $V(C)=4$, $V(W)=2$, $V(O)=0$ y $\gamma=0.5$, calcula los cuatro valores de acción y las acciones codiciosas.

> [!answer]- Solución
> $Q(C,\text{Slow})=3$, $Q(C,\text{Fast})=3.5$, $Q(W,\text{Slow})=2.5$, $Q(W,\text{Fast})=-10$. Las acciones son Fast y Slow. El nuevo vector de valores es $(3.5,2.5,0)$.

### C. Distinguir evaluación de optimalidad

¿Por qué $V(C)=V(W)=10$ con $\gamma=0.9$ no demuestra que la política Slow–Slow sea óptima?

> [!answer]- Solución
> Esos valores satisfacen Bellman para esa política. Sin embargo, $Q^{\pi}(C,\text{Fast})=11>10$, por lo que otra acción mejora el valor. Satisfacer la ecuación de evaluación no implica satisfacer la de optimalidad.

### D. Detectar un supuesto roto

¿Qué impide aplicar la garantía de contracción al ejemplo de la diapositiva 19?

> [!answer]- Solución
> Usa $\gamma=1$, y la política Fast–Slow no termina. No hay factor de contracción menor que uno ni retorno total finito. Los respaldos siguen siendo válidos para horizontes finitos.

### E. Separar parámetros

En Q-learning, con $Q(s,a)=3$, $r=1$, $\max_{a'}Q(s',a')=4$, $\gamma=0.9$ y $\alpha=0.2$, ¿cuál es la actualización?

> [!answer]- Solución
> $y=1+0.9(4)=4.6$; el error es $1.6$ y $Q_{\mathrm{nuevo}}=3+0.2(1.6)=3.32$. No se modifica toda la tabla.

## 14. Fuentes y cómo continuar

**Material principal:** Carlos Hernández, [[AI 21 Aprendizaje por refuerzo.pdf|Clase 21: aprendizaje por refuerzo]], 24 diapositivas. El grafo del automóvil y las iteraciones de $\gamma=1$ se verificaron visualmente en las diapositivas 6 y 17–19. Las precisiones sobre terminación, empates y alcance de las garantías se explicitan en esta nota.

**UC Berkeley, CS 188 — Introduction to Artificial Intelligence**, fuentes oficiales consultadas el **16 de noviembre de 2026**:

| Recurso | Para qué usarlo |
|---|---|
| [§4.1 Markov Decision Processes](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/markov-decision-processes.html) | Revisar formulación, descuento y representación del automóvil |
| [§4.2 Solving Markov Decision Processes](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/solve.html) | Conectar V, Q, Bellman y expectimax |
| [§4.3 Value Iteration](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/value-iteration.html) | Profundizar en respaldos, contracción y extracción de política |
| [§4.4 Policy Iteration](https://inst.eecs.berkeley.edu/~cs188/textbook/mdp/policies-iteration.html) | Comparar evaluación y mejora |
| [§5.1 Reinforcement Learning](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/rl.html) | Distinguir planificación con modelo de aprendizaje |
| [§5.2 Model-Based Learning](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/mbl.html) | Estimar transiciones mediante conteos |
| [§5.3 Model-Free Learning](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/mfl.html) | Continuar con TD y Q-learning |
| [§5.4 Exploration and Exploitation](https://inst.eecs.berkeley.edu/~cs188/textbook/rl/eae.html) | Estudiar el compromiso entre aprender y aprovechar |
| [Proyecto 3, otoño 2026: Reinforcement Learning](https://inst.eecs.berkeley.edu/~cs188/fa26/projects/proj3/) | Practicar después con Gridworld y los agentes del curso; es material adicional, no una tarea asignada aquí |

## 15. Ideas que deben permanecer

Una acción cambia el premio presente y la distribución de oportunidades futuras. El estado de un MDP resume la información necesaria para modelar esas consecuencias. El retorno permite compararlas, y Bellman lo descompone en recompensa inmediata más continuación descontada. Evaluar una política calcula qué produce; mejorarla usa esa evaluación para elegir acciones más convenientes. Con un modelo conocido hacemos planificación; cuando debemos obtener información actuando, entramos en aprendizaje por refuerzo.

### Lista de dominio

- [ ] Puedo reconstruir las seis transiciones del automóvil sin ver la tabla.
- [ ] Puedo explicar por qué una política reacciona al estado y un plan fijo no basta.
- [ ] Puedo derivar Bellman a partir de $G_t=R_{t+1}+\gamma G_{t+1}$.
- [ ] Puedo obtener $V_1$ y $V_2$ y distinguir $\gamma=0.9$ de $\gamma=1$.
- [ ] Puedo resolver la evaluación de Fast–Slow como un sistema de dos ecuaciones.
- [ ] Puedo mejorar Slow–Slow y comprobar que Fast–Slow es estable.
- [ ] Puedo explicar qué información falta para pasar de planificación a RL.
