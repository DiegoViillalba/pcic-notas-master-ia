---
tipo: clase
materia: "[[Indice|Modelación Matemática]]"
fecha: 2026-08-17
unidad: Modelos dinámicos continuos y discretos
profesor: Alicia de la Mora
estado: procesada
conceptos:
  - "[[Balance de tasas|Balance de tasas]]"
  - "[[Crecimiento exponencial|Crecimiento exponencial]]"
  - "[[Crecimiento logístico|Crecimiento logístico]]"
  - "[[Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]]"
  - "[[Método de Euler|Método de Euler]]"
referencias: []
tags:
  - clase
  - modelacion-matematica
  - ecuaciones-diferenciales
  - metodos-numericos
---

# Modelos de cambio y método de Euler

## Pregunta central

¿Cómo se traduce una descripción verbal de cambio en un modelo continuo o discreto y cómo se aproxima una ecuación diferencial mediante el método de Euler?

## Del fenómeno a la ecuación

Para formular un modelo dinámico conviene seguir cuatro pasos:

1. Definir la variable de estado y sus unidades.
2. Identificar qué aumenta y qué disminuye esa variable.
3. Escribir una relación de [[Balance de tasas|balance de tasas]].
4. Especificar la condición inicial y revisar que las unidades sean consistentes.

En tiempo continuo, una tasa de cambio se expresa mediante una derivada:

$$
\text{cambio}=\text{entradas}-\text{salidas}+\text{generación}-\text{consumo}.
$$

En tiempo discreto, el mismo razonamiento produce una regla de actualización:

$$
x_{n+1}=x_n+\text{incrementos durante el paso}-\text{decrementos durante el paso}.
$$

> [!important]
> El signo y las unidades forman parte del modelo. Si $x$ se mide en litros y $t$ en minutos, cada término de $dx/dt$ debe medirse en litros por minuto.

## Crecimiento exponencial y logístico

### Recursos ilimitados: crecimiento exponencial

Si la rapidez de crecimiento es proporcional a la población presente,

$$
\frac{dP}{dt}=rP, \qquad P(0)=P_0,
$$

la solución es

$$
P(t)=P_0e^{rt}.
$$

Este modelo supone que la tasa per cápita $r$ permanece constante. Es útil en etapas iniciales, pero no incorpora competencia ni escasez de recursos.

### Recursos limitados: crecimiento logístico

Para mejorar el modelo exponencial se introduce una capacidad de carga $K$:

$$
\frac{dP}{dt}=rP\left(1-\frac{P}{K}\right),
\qquad P(0)=P_0.
$$

Aquí:

- $P(t)$ es la población;
- $r$ es la tasa de crecimiento intrínseca, con unidades de tiempo$^{-1}$;
- $K$ es la capacidad de carga, con las mismas unidades que $P$;
- $1-P/K$ reduce el crecimiento conforme la población se acerca a $K$.

Separando variables e imponiendo la condición inicial se obtiene

$$
P(t)=\frac{K}{1+\left(\frac{K-P_0}{P_0}\right)e^{-rt}}
=\frac{KP_0e^{rt}}{K+P_0(e^{rt}-1)}.
$$

Para $r>0$ y $P_0>0$, los equilibrios son $P=0$ y $P=K$. Si $0<P_0<K$, la población crece hacia $K$; si $P_0>K$, decrece hacia $K$. En ambos casos,

$$
\lim_{t\to\infty}P(t)=K.
$$

## Ejemplos de formulación continua

### Enfriamiento de una taza de café

Una taza de café se encuentra inicialmente a $90\,{}^\circ\mathrm C$ en una habitación cuya temperatura permanece en $20\,{}^\circ\mathrm C$. La [[Ley de enfriamiento de Newton|ley de enfriamiento de Newton]] supone que la rapidez de cambio es proporcional a la diferencia respecto del ambiente.

Sean

$$
T(t)=\text{temperatura del café}, \qquad T_a=20\,{}^\circ\mathrm C.
$$

Como el café está más caliente que el ambiente y debe enfriarse,

$$
\frac{dT}{dt}=-\kappa(T-T_a),
\qquad T(0)=90,
\qquad \kappa>0.
$$

La solución es

$$
T(t)=20+70e^{-\kappa t}.
$$

Sin una medición adicional de temperatura y tiempo no puede determinarse el valor numérico de $\kappa$.

### Tanque con entrada y fuga

Un tanque contiene inicialmente $100$ L. Entran $8$ L/min y la fuga es proporcional al volumen, con $k=0.3$ min$^{-1}$. Si $V(t)$ es el volumen en litros,

$$
\frac{dV}{dt}
=\underbrace{8}_{\text{entrada}}
-\underbrace{0.3V}_{\text{salida}},
\qquad V(0)=100.
$$

El volumen de equilibrio satisface $0=8-0.3V^*$, por lo que

$$
V^*=\frac{8}{0.3}\approx 26.67\ \mathrm L.
$$

La solución

$$
V(t)=\frac{80}{3}+\frac{220}{3}e^{-0.3t}
$$

muestra que el volumen desciende desde $100$ L y se aproxima a $26.67$ L. El modelo supone que la entrada y el coeficiente de fuga permanecen constantes.

## Ejemplos de formulación discreta

### Colonia de insectos

Una población inicial de $200$ individuos aumenta $15\%$ por generación. Si $P_n$ es la población en la generación $n$,

$$
P_{n+1}=P_n+0.15P_n=1.15P_n,
\qquad P_0=200.
$$

Por iteración,

$$
P_n=200(1.15)^n.
$$

Este es un modelo discreto de crecimiento exponencial. Supone una tasa fija y ausencia de migración o factores externos.

### Cuenta bancaria

Una cuenta inicia con $10\,000$ unidades monetarias. Al final de cada mes gana $1\%$ de interés y después recibe un depósito de $500$. Si $S_n$ es el saldo antes de aplicar esas operaciones,

$$
S_{n+1}=1.01S_n+500,
\qquad S_0=10\,000.
$$

El orden importa: si el depósito se hiciera antes de calcular el interés, la recurrencia sería $S_{n+1}=1.01(S_n+500)$.

## Método de Euler

Para el problema de valor inicial

$$
\frac{dy}{dt}=f(t,y),
\qquad y(t_0)=y_0,
$$

la expansión de Taylor alrededor de $t_n$ es

$$
y(t_n+h)=y(t_n)+hy'(t_n)+\frac{h^2}{2}y''(\xi_n),
$$

para algún $\xi_n\in(t_n,t_n+h)$. Al sustituir $y'=f(t,y)$ y descartar los términos de orden $h^2$ se obtiene el [[Método de Euler|método de Euler explícito]]:

$$
t_{n+1}=t_n+h,
\qquad
y_{n+1}=y_n+h f(t_n,y_n).
$$

Geométricamente, se avanza una distancia $h$ usando como aproximación la recta tangente en el punto actual.

### Un paso aplicado al café

Si, solo para ilustrar el procedimiento, se toma $\kappa=0.1$ min$^{-1}$ y $h=1$ min, entonces

$$
f(T)=-0.1(T-20).
$$

Desde $T_0=90$:

$$
T_1=90+1[-0.1(90-20)]=83\,{}^\circ\mathrm C,
$$

$$
T_2=83+1[-0.1(83-20)]=76.7\,{}^\circ\mathrm C.
$$

Reducir $h$ suele disminuir el error, pero aumenta el número de pasos y el costo computacional. Además, un paso demasiado grande puede producir resultados inestables o físicamente absurdos.

## Comprobaciones de un modelo de cambio

- ¿Cada variable y parámetro está definido con unidades?
- ¿Las condiciones iniciales están especificadas?
- ¿Los signos de entradas y salidas son correctos?
- ¿Todos los términos de una ecuación tienen unidades compatibles?
- ¿El tiempo es continuo o discreto?
- ¿Los equilibrios y el comportamiento límite tienen sentido físico?
- ¿El tamaño de paso numérico es apropiado?

## Ejercicios resueltos

- [x] Desarrollar varias iteraciones de Euler y compararlas con la solución exacta de la ley de enfriamiento.
- [x] Estudiar cómo cambia el error al usar $h=1$, $0.5$ y $0.1$.
- [x] Resolver la ecuación logística a mano mediante separación de variables.

### Euler frente a la solución exacta

Para el modelo del café con $T_a=20$, $T_0=90$ y $\kappa=0.1$ min$^{-1}$,

$$
\frac{dT}{dt}=-0.1(T-20),
\qquad
T(t)=20+70e^{-0.1t}.
$$

Al aplicar Euler con $h=1$ min se obtiene la recurrencia

$$
T_{n+1}=T_n-0.1(T_n-20)=0.9T_n+2.
$$

Las primeras iteraciones muestran que la aproximación queda por debajo de la solución exacta:

| $t$ (min) | Euler, $h=1$ | Solución exacta | Error absoluto |
|---:|---:|---:|---:|
| 0 | 90.000 | 90.000 | 0.000 |
| 1 | 83.000 | 83.339 | 0.339 |
| 2 | 76.700 | 77.311 | 0.611 |
| 3 | 71.030 | 71.857 | 0.827 |
| 4 | 65.927 | 66.922 | 0.995 |

Si se define la diferencia respecto del ambiente como $E_n=T_n-20$, la actualización se simplifica a

$$
E_{n+1}=(1-0.1h)E_n.
$$

Por lo tanto, después de $n$ pasos,

$$
T_n=20+70(1-0.1h)^n.
$$

Esta expresión permite comparar distintos tamaños de paso en el mismo tiempo final. Para $t=10$ min, la solución exacta es

$$
T(10)=20+70e^{-1}\approx45.7516,{}^\circ\mathrm C.
$$

| Paso $h$ | Número de pasos | Aproximación $T_h(10)$ | Error absoluto | Error relativo |
|---:|---:|---:|---:|---:|
| 1 | 10 | 44.4075 | 1.3441 | 2.9378 % |
| 0.5 | 20 | 45.0940 | 0.6575 | 1.4372 % |
| 0.1 | 100 | 45.6223 | 0.1293 | 0.2826 % |

Al reducir $h$ por un factor cercano a diez, el error también disminuye aproximadamente por ese factor. Esto coincide con que Euler tiene error global de orden $O(h)$.

En este modelo, la aproximación converge al equilibrio únicamente si

$$
|1-\kappa h|<1,
$$

es decir, si $0<\kappa h<2$. Para que la temperatura se acerque al ambiente sin oscilaciones ni valores físicamente extraños, conviene además exigir $0<\kappa h\leq1$.

### Solución logística mediante separación de variables

Partimos del modelo

$$
\frac{dP}{dt}=rP\left(1-\frac{P}{K}\right),
\qquad P(0)=P_0.
$$

Para $P\neq0$ y $P\neq K$, se separan las variables:

$$
\frac{dP}{P(1-P/K)}=r\,dt.
$$

Como

$$
\frac{1}{P(1-P/K)}
=\frac{K}{P(K-P)}
=\frac{1}{P}+\frac{1}{K-P},
$$

se integra en ambos lados:

$$
\int\left(\frac{1}{P}+\frac{1}{K-P}\right)dP
=\int r\,dt.
$$

Así,

$$
\ln|P|-\ln|K-P|=rt+C,
$$

y, al combinar los logaritmos,

$$
\frac{P}{K-P}=Ce^{rt}.
$$

La condición inicial determina

$$
C=\frac{P_0}{K-P_0}.
$$

Finalmente, al despejar $P$,

$$
P(t)
=\frac{KCe^{rt}}{1+Ce^{rt}}
=\frac{K}{1+\left(\frac{K-P_0}{P_0}\right)e^{-rt}}
=\frac{KP_0e^{rt}}{K+P_0(e^{rt}-1)}.
$$

Las soluciones de equilibrio $P(t)=0$ y $P(t)=K$ deben considerarse por separado porque al dividir entre $P(K-P)$ se excluyeron temporalmente esos dos casos.

## Conceptos extraídos

- [[Balance de tasas|Balance de tasas]]
- [[Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]]
- [[Método de Euler|Método de Euler]]

## Conceptos relacionados actualizados

- [[Crecimiento exponencial|Crecimiento exponencial]]
- [[Crecimiento logístico|Crecimiento logístico]]

## Referencias mencionadas

- No se registró bibliografía externa durante la clase; las formulaciones se reconstruyeron a partir de los apuntes.

## Resumen después de clase

Una descripción verbal de cambio puede transformarse en un modelo al definir variables, condiciones iniciales y un balance entre entradas y salidas. En tiempo continuo este balance conduce a ecuaciones diferenciales, como los modelos de enfriamiento, fuga y crecimiento logístico; en tiempo discreto produce recurrencias, como las de una población por generaciones o una cuenta bancaria. El modelo logístico mejora el crecimiento exponencial al incorporar una capacidad de carga. Cuando no se usa una solución analítica, el método de Euler permite aproximar la evolución mediante pasos sobre la recta tangente, aunque su precisión y estabilidad dependen del tamaño de paso.
