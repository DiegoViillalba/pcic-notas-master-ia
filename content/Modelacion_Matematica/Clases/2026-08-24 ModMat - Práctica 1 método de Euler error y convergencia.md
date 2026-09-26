---
tipo: clase
materia: "[[01_Materias/Modelacion_Matematica/Indice|Modelación Matemática]]"
fecha: 2026-08-24
unidad: Métodos numéricos para problemas de valor inicial
profesor: Alicia de la Mora
estado:
  - por-capturar
  - por-revisar
  - por-procesar
conceptos:
  - "[[03_Conceptos/Método de Euler|Método de Euler]]"
  - "[[03_Conceptos/Ley de enfriamiento de Newton|Ley de enfriamiento de Newton]]"
  - "[[03_Conceptos/Solución analítica y solución numérica|Solución analítica y solución numérica]]"
  - "[[03_Conceptos/Experimento computacional|Experimento computacional]]"
referencias:
  - Práctica1_MMyCHPC_Euler_clase.ipynb
tags:
  - clase
  - modelacion-matematica
  - metodos-numericos
  - metodo-de-euler
---

# Práctica 1. Modelación, método de Euler, error y convergencia

**Curso:** Modelación Matemática y Computacional I HPC

**Tema:** Solución numérica de problemas de valor inicial mediante el método de Euler

## Pregunta central

¿Cómo se aproxima un problema de valor inicial mediante el método de Euler y cómo se estudian su error y convergencia?

## Apuntes rápidos

- 

## Material de clase y actividades

# 1. Problemas de valor inicial

Muchas leyes de evolución pueden expresarse mediante una ecuación diferencial ordinaria de primer orden:

$$
\frac{dy}{dt}=f(t,y).
$$

La ecuación describe la razón de cambio de una cantidad $y$ con respecto al tiempo $t$. Sin embargo, esta ecuación por sí sola generalmente representa una familia de soluciones. Para seleccionar una solución particular necesitamos conocer el valor de la variable en algún instante:

$$
y(t_0)=y_0.
$$

El problema

$$
\boxed{
\frac{dy}{dt}=f(t,y),\qquad y(t_0)=y_0
}
$$

se denomina **problema de valor inicial (PVI)**.

En un método numérico no intentamos construir de inmediato una fórmula válida para todo $t$. En su lugar, aproximamos la solución en una colección de puntos

$$
t_0,\ t_1,\ t_2,\ldots,t_N.
$$

Si utilizamos una malla uniforme,

$$
t_{n+1}=t_n+h,
$$

donde $h>0$ se llama tamaño de paso.

La notación

$$
y_n
$$

representará una aproximación numérica de la solución exacta $y(t_n)$. En general,

$$
y_n\neq y(t_n).
$$

Esta diferencia será central en el estudio del error.


# 2. Método de Euler

Supongamos, por un momento, que la solución exacta $y(t)$ es suficientemente suave. Queremos relacionar el valor de la solución en $t_n$ con su valor un paso después,

$$
t_{n+1}=t_n+h.
$$

La expansión de Taylor de $y(t_n+h)$ alrededor de $t_n$ es

$$
y(t_n+h)
=
y(t_n)
+h\,y'(t_n)
+\frac{h^2}{2}y''(t_n)
+\frac{h^3}{3!}y'''(t_n)+\cdots.
$$

Como $t_{n+1}=t_n+h$,

$$
y(t_{n+1})
=
y(t_n)
+h\,y'(t_n)
+\frac{h^2}{2}y''(t_n)+\cdots.
$$

Pero el PVI nos dice que

$$
y'(t)=f(t,y(t)).
$$

Por tanto,

$$
y'(t_n)=f(t_n,y(t_n)),
$$

y podemos escribir

$$
y(t_{n+1})
=
y(t_n)
+h f(t_n,y(t_n))
+\frac{h^2}{2}y''(t_n)+\cdots.
$$

Si conservamos solamente los dos primeros términos,

$$
y(t_{n+1})
\approx
y(t_n)+h f(t_n,y(t_n)).
$$

Finalmente, en el cálculo numérico sustituimos los valores exactos desconocidos por aproximaciones:

$$
y_{n+1}=y_n+h\,f(t_n,y_n)
$$

Esta es la fórmula del método de Euler explícito.


## 2.1 Interpretación geométrica

En el punto $(t_n,y_n)$, la ecuación diferencial proporciona una pendiente

$$
m_n=f(t_n,y_n).
$$

La recta con esa pendiente que pasa por $(t_n,y_n)$ es

$$
y-y_n=f(t_n,y_n)(t-t_n).
$$

Si evaluamos esta recta en $t_{n+1}=t_n+h$,

$$
y_{n+1}-y_n
=
f(t_n,y_n)\,h,
$$

de donde

$$
y_{n+1}
=
y_n+h f(t_n,y_n).
$$


## Actividad 1. Deducción

Sin copiar simplemente la fórmula final:

1. Escribe la expansión de Taylor de $y(t_{n+1})$ alrededor de $t_n$ hasta el término de segundo orden.
2. Sustituye $y'(t_n)$ utilizando la ecuación diferencial.
3. Identifica el término que se omite al construir Euler.
4. Explica con tus palabras por qué Euler puede interpretarse como una aproximación lineal local.
5. Indica qué información requiere Euler para calcular $y_{n+1}$.

La respuesta debe mostrar el desarrollo, no únicamente $y_{n+1}=y_n+h f(t_n,y_n)$.


### Actividad 1

Escribe aquí tu deducción. Utiliza ecuaciones en Markdown/LaTeX.

**Hint:** tu desarrollo debe contener un término proporcional a $h^2$ antes de llegar a la fórmula de Euler.


# 3. Modelo: enfriamiento en un ambiente cuya temperatura cambia

Consideremos un recipiente con líquido caliente. Inicialmente,

$$
T(0)=90\,^\circ\mathrm{C}.
$$

El recipiente se encuentra en una habitación cuya temperatura no permanece constante. Durante las primeras cinco horas se aproxima mediante

$$
T_a(t)=20+2t,
$$

donde:

- $t$ se mide en horas;
- $T_a(t)$ se mide en grados Celsius.

La rapidez con la que cambia la temperatura del líquido es proporcional a la diferencia entre su temperatura y la temperatura del ambiente. La constante de intercambio térmico es

$$
k=0.6\ \mathrm{h}^{-1}.
$$

La ley de enfriamiento de Newton puede expresarse como

$$
\frac{dT}{dt}=-k\bigl(T-T_a(t)\bigr).
$$

¿Por qué aparece un signo negativo? Si el líquido está más caliente que el ambiente, entonces

$$
T-T_a(t)>0,
$$

y físicamente esperamos que la temperatura del líquido disminuya:

$$
\frac{dT}{dt}<0.
$$

El signo negativo garantiza precisamente este comportamiento.


## 3.1 Construcción del PVI

Sustituyendo

$$
k=0.6,\qquad T_a(t)=20+2t,
$$

obtenemos

$$
\boxed{
\frac{dT}{dt}
=
-0.6\left[T-(20+2t)\right]
}
$$

con condición inicial

$$T(0)=90.
$$

Por tanto, nuestra función es

$$
f(t,T)=-0.6\left[T-(20+2t)\right].
$$


## Actividad 2. Interpretación del modelo

Responde antes de programar:

1. ¿Cuál es la variable independiente?
2. ¿Cuál es la variable dependiente?
3. ¿Cuáles son las unidades de $dT/dt$?
4. Verifica dimensionalmente que $k(T-T_a)$ tiene las mismas unidades que $dT/dt$.
5. ¿Qué ocurriría con el signo de $dT/dt$ si el líquido estuviera más frío que el ambiente?
6. ¿Qué representa físicamente el caso $T=T_a(t)$ en un instante determinado?


### Actividad 2


**Hint:** Si $T=T_a(t)$ en un instante obliga a que ambas temperaturas permanezcan iguales posteriormente cuando $T_a$ cambia con $t$.


# 4. Aplicación del método de Euler

Antes de escribir código, realicemos algunos pasos manualmente.

Para nuestro modelo,

$$
T_{n+1}
=
T_n+h\left[-0.6\left(T_n-(20+2t_n)\right)\right].
$$

Utilizaremos

$$
h=0.5\text{ h},\qquad T_0=90,\qquad t_0=0.
$$


## Actividad 3. Iteraciones

Calcula manualmente $T_1,T_2,T_3,T_4$ usando $h=0.5$.

Completa una tabla de la forma:

| $n$ | $t_n$ | $T_n$ | $T_a(t_n)$ | $f(t_n,T_n)$ | $T_{n+1}$ |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 90 |  |  |  |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

Muestra al menos una sustitución completa en la fórmula de Euler.


### Actividad 3

Completa la tabla anterior. Verifica tus cuatro iteraciones antes de compararlas con el código.

Incluye aquí al menos una sustitución completa:

$$
T_{n+1}=\cdots
$$


# 5. Algoritmo

Un método numérico debe traducirse en una secuencia inequívoca de operaciones.

Para una función general

$$
y'=f(t,y),\qquad y(t_0)=y_0,
$$

Euler requiere repetir:

$$
y_{n+1}=y_n+h f(t_n,y_n),
$$

$$
t_{n+1}=t_n+h.
$$

Un esquema básico sería:

1. guardar $t_0$ y $y_0$;
2. evaluar $f(t_n,y_n)$;
3. calcular $y_{n+1}$;
4. avanzar el tiempo;
5. guardar los nuevos valores;
6. repetir hasta llegar a $t_f$.


Si

$$
N=\frac{t_f-t_0}{h}
$$

no es entero, no podemos efectuar exactamente $N$ iteraciones. En esta práctica escogeremos valores de $h$ que dividan exactamente el intervalo, pero en una implementación general este detalle debe tratarse explícitamente.


## Actividad 4. Pseudocódigo

Escribe pseudocódigo para una función que reciba

$$
f,\ t_0,\ y_0,\ t_f,\ h
$$

y regrese dos arreglos con los tiempos y las aproximaciones numéricas.

Tu algoritmo debe indicar dónde:

- se calcula el número de pasos;
- se crea la malla;
- se almacena la condición inicial;
- se evalúa la pendiente;
- se actualiza $y$;
- se regresan los resultados.


### Actividad 4

```text
función Euler(f, t0, y0, tf, h)

    # Completar

fin función
```

No escribas todavía Python: primero representa la lógica del algoritmo.


```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
```


# 6. Implementación del modelo

La función matemática del problema es

$$
f(t,T)=-0.6[T-(20+2t)].
$$

Separar el modelo del método numérico es una buena práctica de programación:

- `f(t,T)` describe el fenómeno;
- `euler(...)` describe el método numérico.

Así, la misma implementación de Euler puede utilizarse posteriormente con otras ecuaciones diferenciales.


```python
def f_temperatura(t, T):
    # TODO 1:
    # Calcular la temperatura ambiente Ta(t) = 20 + 2t.
    Ta = None

    # TODO 2:
    # Regresar -0.6*(T - Ta).
    return None


def euler(f, t0, y0, tf, h):
    """Implementa aquí el método de Euler explícito."""

    # TODO 1: calcular cuántos pasos se necesitan.
    N = None

    # TODO 2: crear arreglos para t y y con N+1 elementos.
    # t = ...
    # y = ...

    # TODO 3: almacenar la condición inicial.
    # t[0] = ...
    # y[0] = ...

    # TODO 4: construir un ciclo for.
    # En cada paso:
    #   a) calcular t[n+1]
    #   b) evaluar f(t[n], y[n])
    #   c) calcular y[n+1]

    # TODO 5: regresar ambos arreglos.
    # return t, y

    raise NotImplementedError("Completa la función euler antes de continuar.")
```


### Comprobació

Cuando termines tu función, resuelve solamente hasta $t=2$ con $h=0.5$ y compara los primeros cuatro pasos con los resultados que calculaste manualmente.

Si no coinciden, corrige el código antes de continuar.


```python
# Descomenta cuando tu función euler esté terminada.

# t_test, T_test = euler(f_temperatura, 0.0, 90.0, 2.0, 0.5)
# pd.DataFrame({"t": t_test, "T_Euler": T_test})
```


# 7. Primer experimento: efecto del tamaño de paso

Resolveremos el modelo en

$$
0\le t\le5
$$

con diferentes tamaños de paso:

$$
h=1,\qquad 0.5,\qquad 0.25,\qquad 0.125.
$$

Antes de ejecutar el experimento, piensa:

- al disminuir $h$, ¿aumentará o disminuirá el número de pasos?
- ¿esperas que las curvas numéricas se acerquen entre sí?
- ¿por qué una malla más fina suele producir una mejor aproximación?


```python
h_values = [1.0, 0.5, 0.25, 0.125]

# TODO:
# 1. crea una figura;
# 2. recorre h_values;
# 3. llama a tu función euler;
# 4. grafica cada aproximación;
# 5. agrega título, etiquetas, leyenda y cuadrícula.

# Tu código aquí.
```


### Análisis


Explica:

1. qué ocurre con el número de pasos cuando $h$ disminuye;
2. qué cambia en las curvas;
3. por qué este experimento sugiere pero todavía no demuestra cuantitativamente convergencia;
4. cuál es el costo computacional de disminuir $h$.


# 8. Solución analítica del modelo

Para estudiar el error necesitamos una referencia. En este caso particular el PVI puede resolverse analíticamente.

Partimos de

$$
T'=-0.6[T-(20+2t)].
$$

Distribuyendo,

$$
T'=-0.6T+12+1.2t,
$$

por lo que

$$
\boxed{
T'+0.6T=12+1.2t.
}
$$

Esta es una ecuación diferencial lineal de primer orden

$$
T'+p(t)T=q(t),
$$

con

$$
p(t)=0.6.
$$

El factor integrante es

$$
\mu(t)=e^{\int 0.6\,dt}=e^{0.6t}.
$$

Multiplicando toda la ecuación por $e^{0.6t}$,

$$
e^{0.6t}T'+0.6e^{0.6t}T
=
(12+1.2t)e^{0.6t}.
$$

El lado izquierdo es

$$
\frac{d}{dt}\left(e^{0.6t}T\right).
$$

Por tanto,

$$
\frac{d}{dt}\left(e^{0.6t}T\right)
=
(12+1.2t)e^{0.6t}.
$$

Integramos ambos lados:

$$
e^{0.6t}T
=
\int (12+1.2t)e^{0.6t}\,dt+C.
$$

Al efectuar la integración y aplicar $T(0)=90$, se obtiene

$$
T(t)=\frac{56}{3}+2t+\frac{214}{3}e^{-0.6t}.
$$


## Verificación de la solución exacta

Una fórmula obtenida analíticamente no debe aceptarse sin revisión.

### Condición inicial

$$
T(0)
=
\frac{56}{3}
+\frac{214}{3}
=
\frac{270}{3}
=
90.
$$

### Derivada

$$
T'(t)
=
2
-\frac{214}{3}(0.6)e^{-0.6t}.
$$

Al sustituir $T(t)$ en

$$
-0.6[T-(20+2t)]
$$

se obtiene la misma expresión. Por tanto, la función satisface tanto la ecuación diferencial como la condición inicial.


```python
def solucion_exacta(t):
    """Solución analítica del modelo de temperatura."""
    return 56/3 + 2*t + (214/3)*np.exp(-0.6*t)

print("T_exacta(0) =", solucion_exacta(0.0))
print("T_exacta(5) =", solucion_exacta(5.0))
```


# 9. Error

Es importante distinguir conceptos.

## 9.1 Error de la aproximación en un punto

Si $T(t_n)$ es el valor exacto y $T_n$ es la aproximación numérica,

$$
e_n=T(t_n)-T_n.
$$

El **error absoluto** es

$$
\boxed{
E_{\mathrm{abs},n}
=
|T(t_n)-T_n|.
}
$$

El **error relativo** es

$$
\boxed{
E_{\mathrm{rel},n}
=
\frac{|T(t_n)-T_n|}{|T(t_n)|},
}
$$

siempre que $T(t_n)\neq0$.

El error porcentual es

$$
E_{\%}=100E_{\mathrm{rel}}.
$$

Estos errores comparan directamente la solución numérica con una referencia exacta. No deben confundirse automáticamente con el error local de truncamiento.


# 10. Error local de truncamiento

Con Taylor:

$$
y(t_{n+1})
=
y(t_n)
+h f(t_n,y(t_n))
+\frac{h^2}{2}y''(\xi_n),
$$

para algún $\xi_n\in(t_n,t_{n+1})$.

Euler conserva

$$
y(t_n)+h f(t_n,y(t_n))
$$

y omite el término restante. El error cometido en un solo paso ideal, suponiendo que iniciamos ese paso desde el valor exacto, es entonces proporcional a

$$
h^2.
$$

Por eso decimos que el error local de truncamiento de Euler es

$$O(h^2).
$$

El símbolo $O(h^2)$ no significa que el error sea exactamente $h^2$. Significa que, para $h$ suficientemente pequeño, su magnitud puede acotarse por una constante multiplicada por $h^2$.


# 11. Error global y orden del método

En un intervalo de longitud fija,

$$
[t_0,t_f],
$$

el número de pasos es aproximadamente

$$
N\sim\frac{t_f-t_0}{h}.
$$

Por tanto,

$$
N=O\left(\frac1h\right).
$$

Aunque cada paso introduce un error local de orden $O(h^2)$, realizamos del orden de $1/h$ pasos. De manera intuitiva,

$$
O(h^2)\,O(1/h)=O(h).
$$

Bajo las hipótesis matemáticas apropiadas, el error global del método de Euler satisface

$$E_{\mathrm{global}}=O(h).
$$

Por esta razón decimos que Euler es un método de primer orden.


```python
# Construye una tabla de errores en t=5.

h_values_error = np.array([1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125])
T5_exacta = solucion_exacta(5.0)

filas = []

for h in h_values_error:
    # TODO:
    # t_num, T_num = ...
    # error_abs = ...
    # error_rel = ...
    # error_porcentual = ...
    #
    # filas.append([...])
    pass

# TODO: crea un DataFrame con las columnas:
# h, N, T_Euler(5), T_exacta(5),
# Error absoluto, Error relativo, Error (%)

# tabla_error = ...
# tabla_error
```


## Actividad 5. Diferencia entre error local y error global

Explica con tus propias palabras por qué no existe contradicción entre

$$
\tau_n=O(h^2)
$$

para el error local y

$$
E_n=O(h)
$$

para el error global.

Tu explicación debe distinguir explícitamente:

- un solo paso;
- muchos pasos;
- acumulación/propagación del error;
- intervalo de integración fijo.


### Actividad 5

Desarrolla la explicación en un párrafo matemáticamente preciso. Deben aparecer las expresiones

$$
O(h^2),\qquad O(1/h),\qquad O(h).
$$

No basta con multiplicarlas: explica qué representa cada una.


# 12. Convergencia

Decimos que un método numérico converge si, al refinar la malla,

$$
h\rightarrow0,
$$

la solución numérica se aproxima a la solución exacta:

$$
\max_n|y(t_n)-y_n|\rightarrow0.
$$

La convergencia no significa simplemente que “la gráfica se ve bien”. Es una propiedad cuantitativa.

Si el error se comporta como

$$
E(h)\approx Ch^p,
$$

el exponente $p$ es el orden de convergencia.

Para dos pasos consecutivos $h$ y $h/2$,

$$
E(h)\approx Ch^p,
$$

$$
E(h/2)\approx C(h/2)^p.
$$

Dividiendo,

$$
\frac{E(h)}{E(h/2)}
\approx 2^p.
$$

Así,

$$
\boxed{
p\approx
\frac{\ln(E(h)/E(h/2))}{\ln 2}.
}
$$

Para Euler esperamos

$$
p\approx1.
$$


# 13. Gráfica log-log y orden experimental

A partir de

$$
E(h)\approx Ch^p,
$$

tomamos logaritmos:

$$
\log E
=
\log C+p\log h.
$$

Esto tiene la forma de una recta

$$
Y=a+pX,
$$

con

$$
X=\log h,\qquad Y=\log E.
$$

Por tanto, si graficamos el error contra $h$ en escala log-log, la pendiente debería aproximarse al orden del método.

Para Euler esperamos una pendiente cercana a

$$1.
$$


```python
# ORDEN EXPERIMENTAL
#
# Usa los errores de tu tabla para calcular:
#
# p = ln(E(h)/E(h/2)) / ln(2)
#
# Construye una tabla con:
# h, E(h), E(h)/E(h/2), p experimental

# Tu código aquí.
```


```python
# GRÁFICA LOG-LOG
#
# 1. Obtén log(h) y log(E).
# 2. Usa np.polyfit(..., ..., 1) para ajustar una recta.
# 3. La primera componente del resultado será la pendiente.
# 4. Grafica los datos y reporta el valor de p.

# Tu código aquí.
```


### Análisis de convergencia

Responde:

1. ¿Los valores de $p$ se acercan a $1$?
2. ¿La pendiente log-log es compatible con el orden teórico de Euler?
3. ¿Qué relación empírica entre $E$ y $h$ sugieren tus resultados?
4. ¿Por qué los cocientes pueden no ser exactamente iguales a $2$?


# 14. Preguntas

Responde con argumentos, no únicamente con una palabra o fórmula.

1. ¿Qué información utiliza Euler para avanzar de $t_n$ a $t_{n+1}$?
2. ¿Por qué se dice que es un método explícito?
3. ¿De dónde surge matemáticamente la fórmula de Euler?
4. ¿Qué relación existe entre la curvatura de una solución y el error local?
5. ¿Cuál es la diferencia entre $y(t_n)$ y $y_n$?
6. ¿Cuál es la diferencia entre error absoluto, error relativo y error local de truncamiento?
7. ¿Por qué Euler tiene error local $O(h^2)$ pero error global $O(h)$?
8. ¿Qué significa afirmar que un método converge?
9. ¿Qué significa afirmar que Euler es de orden uno?
10. Si reducimos $h$ a la mitad, ¿qué esperamos que ocurra aproximadamente con el error global?
11. ¿Qué costo computacional tiene reducir $h$?
12. ¿Por qué el análisis de estabilidad impide elegir $h$ únicamente por comodidad?
13. En el modelo térmico, ¿qué significado físico tiene el signo de $T'(t)$?
14. ¿Qué ventajas tiene separar en el código la función del modelo y la implementación del método?


### Respuestas



## Dudas

- [ ] 

## Conceptos para extraer

- [[Problema de valor inicial]]
- [[Error local de truncamiento]]
- [[Error global]]
- [[Convergencia de un método numérico]]
- [[Orden de convergencia]]

## Referencias mencionadas

- Notebook de clase: `Práctica1_MMyCHPC_Euler_clase.ipynb`

## Resumen después de clase

En 3–5 oraciones, ¿qué aprendí y cómo se conecta con clases anteriores?

## Acciones adicionales

- [ ] Completar las actividades y celdas de código durante la clase.
- [ ] Resolver dudas pendientes.

