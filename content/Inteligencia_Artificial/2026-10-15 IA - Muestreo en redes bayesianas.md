---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-15"
unidad: Razonamiento probabilístico y redes bayesianas
profesor: Carlos Hernández
estado: procesada
conceptos:
  - "[[Muestreo previo]]"
  - "[[Muestreo por rechazo]]"
  - "[[Verosimilitud con pesos]]"
  - "[[Muestreo de Gibbs]]"
referencias:
  - "[[AI 16 muestreo en redes bayesianas.pdf]]"
tags:
  - clase
  - inteligencia-artificial
  - redes-bayesianas
  - inferencia-aproximada
  - muestreo
---

# Muestreo en redes bayesianas: estimar una posterior con simulaciones

> [!summary] Pregunta central
> ¿Cómo aproximamos $P(Q\mid\mathbf e)$ cuando calcularla exactamente resulta costoso, y qué ocurre con las muestras cuando la evidencia es difícil de observar?

Continuación de [[2026-10-13 IA - Inferencia en redes bayesianas|inferencia exacta por enumeración y eliminación de variables]]. En la sesión del **15 de octubre de 2026**, la presentación «Clase 16: muestreo en redes Bayesianas» repasa primero el costo de la eliminación y después compara cuatro métodos de muestreo. La numeración «16» pertenece al PDF; la fecha y el número de clase del índice siguen la planeación del curso.

**Ruta de lectura.** Primero distinguimos muestrear de consultar una probabilidad, luego usamos una misma red para seguir muestreo previo, rechazo, verosimilitud con pesos y Gibbs. Las cuentas adicionales están identificadas como desarrollos de las CPT de las diapositivas, no como resultados impresos en ellas.

![[AI 16 muestreo en redes bayesianas.pdf]]

| Tema | Diapositivas | Sección |
|---|---:|---|
| Puente desde eliminación de variables | 2–6 | §1 |
| Idea de muestreo y uniforme | 7–9 | §2 |
| Muestreo previo y red de ejemplo | 10–11 | §§3–4 |
| Rechazo | 12–14 | §5 |
| Verosimilitud con pesos | 15–17 | §6 |
| Gibbs y su distribución local | 18–20 | §7 |
| Comparación, MCMC y siguiente tema | 21–23 | §§8–10 |

## 1. Por qué pasamos de inferencia exacta a aproximada

En eliminación de variables, multiplicamos factores y sumamos variables ocultas. Si un factor denso contiene $k$ variables de dominio $d$, puede tener $d^k$ entradas. El **orden de eliminación** determina qué factores intermedios aparecen: en la red $Z\to X_i\to Y_i$, eliminar primero las ramas $X_i$ produce resúmenes pequeños; eliminar $Z$ primero puede juntar todas las $X_i$ en una tabla exponencial. Este ejemplo se resolvió en [[2026-10-13 IA - Inferencia en redes bayesianas#12. El orden cambia el costo, aunque no cambie la respuesta|la clase anterior]].

Un **poliárbol** es una red cuyo grafo subyacente no contiene ciclos no dirigidos; permite un orden eficiente para inferencia exacta, medido respecto al tamaño de sus CPT. La diapositiva 4 también recuerda que, en redes generales, la inferencia exacta puede ser difícil aun si las CPT originales son pequeñas. **Muestrear no cambia el modelo:** cambia el modo de calcular una respuesta, aceptando error estadístico a cambio de evitar ciertos cálculos exactos grandes.

> [!note] Exactitud y costo
> Un estimador con pocas muestras puede ser rápido y poco preciso; para obtener más precisión suelen necesitarse más muestras. Tampoco es seguro que el muestreo sea siempre más rápido que una buena eliminación. La estructura de la red, la evidencia y la precisión requerida importan.

## 2. Qué significa muestrear

Una **muestra** es un resultado aleatorio generado según una distribución. Si repetimos el proceso $N$ veces, la frecuencia de un evento estima su probabilidad. Para muestras independientes de $P(X)$:

$$\widehat P(X=x)=\frac{1}{N}\sum_{i=1}^{N}\mathbf 1[x^{(i)}=x].$$

La indicadora vale 1 cuando la muestra cumple el evento y 0 en otro caso. Por la ley de los grandes números, la frecuencia converge a la probabilidad del modelo al aumentar $N$. **Convergencia no significa que una corrida finita dé exactamente el valor verdadero.** En inferencia de una red conocida, las muestras aproximan probabilidades que las CPT ya definen; la diapositiva 7 menciona además el uso distinto de muestras para aprender distribuciones desconocidas.

### 2.1 De un uniforme a una variable discreta

*Diapositiva 8.* Si $U\sim\operatorname{Uniforme}[0,1)$ y $P(C=\text{rojo})=0.6$, $P(C=\text{verde})=0.1$, $P(C=\text{azul})=0.3$, dividimos $[0,1)$ en intervalos de esas longitudes:

| Valor devuelto | Intervalo de $U$ | Longitud |
|---|---|---:|
| Rojo | $[0,0.6)$ | 0.6 |
| Verde | $[0.6,0.7)$ | 0.1 |
| Azul | $[0.7,1)$ | 0.3 |

Por ejemplo, $U=0.65$ devuelve verde. El mismo mecanismo sirve para cada fila de una CPT: elegimos la fila según los valores ya asignados a los padres y luego sorteamos el valor del hijo.

## 3. Una red para todos los métodos

*Diapositivas 10–11 y 16.* El ejemplo tiene $C$ = nublado, $S$ = aspersor, $R$ = lluvia y $W$ = pasto mojado:

```mermaid
flowchart TD
  C[Nublado C] --> S[Aspersor S]
  C --> R[Lluvia R]
  S --> W[Pasto mojado W]
  R --> W
```

Usaremos $+x$ para «$X$ es verdadero» y $-x$ para «$X$ es falso». Las CPT de las diapositivas son:

| Parámetro | Valor | Parámetro | Valor |
|---|---:|---|---:|
| $P(+c)$ | 0.5 | $P(+s\mid+c)$ | 0.1 |
| $P(+s\mid-c)$ | 0.5 | $P(+r\mid+c)$ | 0.8 |
| $P(+r\mid-c)$ | 0.2 |  |  |

| $S$ | $R$ | $P(+w\mid S,R)$ | $P(-w\mid S,R)$ |
|---|---|---:|---:|
| $+s$ | $+r$ | 0.99 | 0.01 |
| $+s$ | $-r$ | 0.90 | 0.10 |
| $-s$ | $+r$ | 0.90 | 0.10 |
| $-s$ | $-r$ | 0.01 | 0.99 |

Cada probabilidad complementaria se obtiene restando de 1. La conjunta se factoriza así:

$$P(c,s,r,w)=P(c)P(s\mid c)P(r\mid c)P(w\mid s,r).$$

**Valor de referencia calculado exactamente a partir de esas CPT.** Por ejemplo,

$$P(+w\mid+c)=0.1(0.8)(0.99)+0.1(0.2)(0.90)+0.9(0.8)(0.90)+0.9(0.2)(0.01)=0.747,$$

$$P(+w\mid-c)=0.5(0.2)(0.99)+0.5(0.8)(0.90)+0.5(0.2)(0.90)+0.5(0.8)(0.01)=0.553.$$

Como $P(+c)=P(-c)=0.5$, resulta $P(+w)=0.5(0.747)+0.5(0.553)=0.65$. Por Bayes:

$$\boxed{P(+c\mid+w)=\frac{P(+c,+w)}{P(+w)}=\frac{0.3735}{0.65}\approx0.574615.}$$

Estas cifras permiten juzgar si una estimación se acerca a la respuesta del **modelo**. No garantizan que las CPT describan perfectamente el clima real.

## 4. Muestreo previo: generar mundos completos

*Diapositivas 10–11.* Recorremos la red en **orden topológico**, de modo que los padres de cada nodo ya estén asignados:

```text
para cada muestra:
    C ← sortear de P(C)
    S ← sortear de P(S | C)
    R ← sortear de P(R | C)
    W ← sortear de P(W | S,R)
    devolver (C,S,R,W)
```

El orden entre $S$ y $R$ puede intercambiarse. La probabilidad de generar un mundo concreto es justamente el producto de sus CPT; por tanto, las muestras siguen la conjunta $P(C,S,R,W)$. Para estimar $P(+w)$ basta contar cuántos mundos traen $+w$ y dividir entre $N$.

**El pequeño lote de la diapositiva 11** contiene cinco mundos; cuatro tienen $+w$, así que da $\widehat P(+w)=4/5=0.8$, frente al valor exacto 0.65. Entre esos cuatro, tres tienen $+c$, de modo que el cociente observado $\widehat P(+c\mid+w)=3/4=0.75$. Esa diferencia es error de muestreo, no una nueva CPT. En el lote no hay ningún mundo con $-r,-w$, así que **no se puede estimar** $P(C\mid-r,-w)$ con él: el denominador empírico sería cero.

> [!important] Dos órdenes distintos
> El orden topológico permite **generar** una muestra porque conocemos los padres antes de sortear el hijo. El orden de **eliminación de variables** de la clase anterior busca mantener pequeñas las tablas de inferencia exacta. No son el mismo problema.

## 5. Muestreo por rechazo: conservar solo mundos compatibles

*Diapositivas 12–14.* Para estimar $P(Q\mid\mathbf e)$, generamos mundos completos por muestreo previo y contamos únicamente los que cumplen la evidencia. Para $P(C\mid+w)$:

```text
aceptados = 0; positivos = 0
repetir N veces:
    x ← muestra previa completa
    si x.W = verdadero:
        aceptados += 1
        si x.C = verdadero: positivos += 1
devolver positivos / aceptados, si aceptados > 0
```

La razón converge a $P(+c\mid+w)$: entre los mundos generados de la conjunta, filtramos precisamente los que satisfacen $+w$. Podemos descartar una muestra tan pronto como contradiga la evidencia y no necesitamos guardar todos los mundos.

El costo aparece cuando la evidencia es rara. La fracción aceptada se aproxima a $P(\mathbf e)$, por lo que, con $N$ intentos, esperamos alrededor de $NP(\mathbf e)$ muestras útiles. Si $P(\mathbf e)=0.001$, unos 1,000 intentos producen **en promedio** solo una muestra aceptada. La evidencia no participa en la generación: se usa después para filtrar. Si no se acepta ninguna, la razón $0/0$ queda indefinida; no la reemplazamos por cero.

## 6. Verosimilitud con pesos: fijar la evidencia y corregir el sesgo

*Diapositivas 15–17.* Ahora asignamos directamente el valor observado a cada variable de evidencia. Sorteamos solo las demás en orden topológico. Cada muestra recibe un peso inicial 1; por cada nodo observado $E_i=e_i$, multiplicamos por la probabilidad local de observar ese valor dados **los padres que quedaron en esa muestra**:

$$w(\mathbf z,\mathbf e)=\prod_{E_i\in\mathcal E}P(e_i\mid\operatorname{pa}(E_i)).$$

Para $P(C\mid+w)$, sorteamos $C,S,R$, fijamos $W=+w$ y damos peso $P(+w\mid S,R)$. Acumulamos pesos, no cantidades de filas:

$$\widehat P(+c\mid+w)=\frac{\sum_{i=1}^{N}w_i\mathbf 1[c^{(i)}=+c]}{\sum_{i=1}^{N}w_i},\quad\text{si }\sum_iw_i>0.$$

**Ejemplo de la diapositiva 16.** Si salen $+c,+s,+r$ y fijamos $+w$, el peso es $0.99$. En la diapositiva se fija **también** $+s$: para evidencia $+s,+w$, esa misma asignación recibe $w=0.1\times0.99=0.099$. El $0.1$ procede de $P(+s\mid+c)$; no es la probabilidad de muestrear $+c$.

### Por qué la corrección funciona

Llamemos $\mathbf z$ a las variables no observadas. La probabilidad con la que este procedimiento sortea $\mathbf z$ es

$$S_{\mathrm{LW}}(\mathbf z\mid\mathbf e)=\prod_{Z_i\notin\mathcal E}P(z_i\mid\operatorname{pa}(Z_i)).$$

Al multiplicarla por el peso recuperamos la conjunta:

$$
S_{\mathrm{LW}}(\mathbf z\mid\mathbf e)w(\mathbf z,\mathbf e)
=\prod_{Z_i\notin\mathcal E}P(z_i\mid\operatorname{pa}(Z_i))
\prod_{E_i\in\mathcal E}P(e_i\mid\operatorname{pa}(E_i))
=P(\mathbf z,\mathbf e).
$$

Los cocientes de sumas ponderadas se acercan así a la posterior. Esta es la igualdad que aparece abreviada en la diapositiva 17. No afirma que las muestras **sin peso** sigan la posterior.

**Límite práctico:** fijar una observación influye en sus descendientes al sortearlos, pero no modifica directamente el sorteo de sus ancestros. Si la evidencia favorece muy fuertemente unos pocos ancestros, muchas muestras obtendrán pesos diminutos. Como diagnóstico, el tamaño efectivo aproximado es $N_{\mathrm{ef}}=(\sum_iw_i)^2/\sum_iw_i^2$; puede ser mucho menor que $N$. Esta fórmula es una ampliación de estudio, no aparece en la presentación.

### Explorar las estimaciones

<iframe src="ia16-muestreo-red-bayesiana.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El explorador usa exactamente las CPT de §3. Permite comparar cómo cambia la estimación al repetir simulaciones: muestreo previo estima $P(+w)$; los otros métodos estiman $P(+c\mid+w)$. La línea horizontal indica el valor exacto para la consulta elegida. En rechazo se muestra cuántos mundos sobreviven; en verosimilitud con pesos, el tamaño efectivo aproximado; en Gibbs, las muestras después del calentamiento. Una corrida concreta puede alejarse temporalmente del valor exacto.

## 7. Gibbs: actualizar un mundo en vez de comenzar de cero

*Diapositivas 18–20.* Gibbs es un método de **cadena de Markov Monte Carlo** (MCMC). Fijamos permanentemente la evidencia, inicializamos los demás nodos con cualquier asignación válida y repetimos:

1. Elegir una variable **no observada** $X$.
2. Volver a sortear $X$ según $P(X\mid\text{valores actuales de las demás variables})$.
3. Mantener los demás valores, avanzar y contar estados de la cadena después de un período de calentamiento.

Para $P(S\mid+r)$, la diapositiva 19 fija $R=+r$ e inicia $C,S,W$; luego actualiza sucesivamente uno de esos nodos. La evidencia permanece fija en cada estado. **Las muestras consecutivas están correlacionadas**: no son nuevos mundos independientes como en muestreo previo.

### 7.1 Solo hace falta la manta de Markov

Para actualizar $X$, los factores que no mencionan $X$ son iguales para todos sus valores y se cancelan al normalizar. Basta usar su CPT y las CPT de sus hijos:

$$P(X=x\mid\text{resto})\propto P(x\mid\operatorname{pa}(X))\prod_{Y\in\operatorname{hijos}(X)}P(y\mid\operatorname{pa}(Y)).$$

Padres, hijos y otros padres de los hijos forman la **manta de Markov**. En la diapositiva 20 se actualiza $S$ dado $+c,+r,-w$:

$$P(S=s\mid+c,+r,-w)\propto P(s\mid+c)P(-w\mid s,+r).$$

Para $+s$, el peso local es $0.1(0.01)=0.001$; para $-s$, $0.9(0.10)=0.09$. Al normalizar:

$$\boxed{P(+s\mid+c,+r,-w)=\frac{0.001}{0.001+0.09}=\frac{1}{91}\approx0.010989.}$$

El factor $P(+c)P(+r\mid+c)$ aparece en ambos casos y se cancela. Esto muestra por qué no necesitamos enumerar toda la red para una actualización local.

### 7.2 Qué significa «en el límite»

Si la cadena puede recorrer los estados relevantes y mezcla adecuadamente, la frecuencia de estados se acerca a la posterior $P(Q\mid\mathbf e)$. **No hay garantía de que unas pocas iteraciones basten.** Se suele descartar un calentamiento inicial y vigilar la autocorrelación o comparar corridas. Con CPT deterministas puede haber estados entre los que la cadena no transite; en ese caso la afirmación de convergencia requiere cuidado. Estas precisiones completan la frase breve de las diapositivas 18 y 22.

## 8. Elegir y comparar los cuatro métodos

| Método | Cómo trata la evidencia | Qué cuenta | Dificultad dominante |
|---|---|---|---|
| Muestreo previo | No la fija | Frecuencias de mundos completos; útil para $P(Q)$ | Una posterior con evidencia rara requiere filtrar o usar otro método. |
| Rechazo | Genera sin ella y descarta incompatibles | Frecuencia entre muestras aceptadas | Se desperdician intentos si $P(\mathbf e)$ es pequeña. |
| Verosimilitud con pesos | Fija evidencia y multiplica probabilidades locales | Sumas de pesos por valor de la consulta | Pocos pesos pueden dominar; la evidencia no guía directamente a los ancestros. |
| Gibbs | Fija evidencia en una cadena y re-muestrea un nodo cada vez | Frecuencia de estados tras calentamiento | Muestras correlacionadas, mezcla lenta o estados inaccesibles. |

**Regla de lectura de un resultado:** junto con $\widehat P$, anotar consulta, evidencia, número de intentos o actualizaciones, muestras efectivamente útiles y método. «Se generaron 10,000 muestras» puede significar 10,000 intentos con pocos aceptados, 10,000 muestras ponderadas con pesos muy desiguales o 10,000 estados muy correlacionados.

## 9. Comprobaciones para estudiar

### A. Rechazo con evidencia rara

Si $P(\mathbf e)=0.02$ y generas 500 mundos por muestreo previo, ¿cuántos esperas conservar? ¿Es un número asegurado?

> [!check]- Solución A
> Esperamos $500(0.02)=10$. Es una media, no una garantía: la cantidad aceptada cambia entre corridas e incluso podría ser cero.

### B. Peso de una muestra

Con evidencia $+s,+w$ y una muestra donde $C=+c,R=+r$, ¿cuál es el peso?

> [!check]- Solución B
> $P(+s\mid+c)P(+w\mid+s,+r)=0.1(0.99)=0.099$. $C$ y $R$ se sortearon; por eso sus probabilidades no son factores del **peso**.

### C. Una actualización Gibbs

En el estado $+c,+r,-w$, ¿es más probable sortear $+s$ o $-s$ al actualizar $S$?

> [!check]- Solución C
> $-s$. Sus pesos locales son $0.09$ frente a $0.001$; tras normalizar, $P(-s\mid+c,+r,-w)=90/91\approx0.989011$.

### D. Detectar una estimación inválida

En rechazo, 1,000 intentos no produjeron ningún mundo compatible con la evidencia. ¿Cuál es la posterior estimada?

> [!check]- Solución D
> No está definida en esa corrida. El denominador es cero; hay que generar más intentos o elegir un método que aproveche mejor esa evidencia. Reportar 0 sería confundir «no observé casos» con «la probabilidad es cero».

### E. Diferenciar los costos

¿Por qué muestreo previo necesita un orden topológico, pero la eliminación de variables puede preferir otro orden?

> [!check]- Solución E
> Para sortear $X$ necesitamos conocer los valores de sus padres. En eliminación, cada paso reorganiza productos y sumas ya definidos; el orden se elige por el tamaño de los factores intermedios, no por la dirección de generación del grafo.

## 10. Alcance y siguiente clase

**Fuente principal:** [[AI 16 muestreo en redes bayesianas.pdf|AI 16 — Muestreo en redes bayesianas]], 23 diapositivas. El PDF contiene las CPT, los cuatro procedimientos y la derivación local de Gibbs. Las probabilidades exactas $0.65$, $0.574615$ y $1/91$, la discusión de muestras efectivas y las advertencias de convergencia son desarrollos hechos aquí a partir de ese material. El recurso interactivo reproduce el modelo con un generador pseudoaleatorio local y no consulta datos externos.

La última diapositiva anuncia **aprender la estructura de una red a partir de datos**. Es un problema distinto de esta clase: aquí la estructura y las CPT estaban dadas y queríamos responder consultas. Aprender estructura pregunta qué flechas y dependencias sostienen los datos.

## Resumen después de clase

El muestreo estima consultas mediante repeticiones. El muestreo previo genera mundos de la conjunta; rechazo conserva los compatibles con la evidencia; verosimilitud con pesos fija la evidencia y corrige con pesos; Gibbs mantiene un mundo compatible y actualiza variables mediante sus distribuciones locales. Cada método aproxima la misma posterior cuando se usa para la consulta adecuada, pero aprovecha la evidencia de manera distinta. La calidad de una estimación finita depende de cuántas muestras útiles aporta, no solo de cuántos pasos ejecuta.

## Acciones de estudio

- [ ] Reconstruir $P(+w)=0.65$ y $P(+c\mid+w)\approx0.574615$ desde las CPT.
- [ ] Explicar por qué una muestra de verosimilitud con evidencia $+s,+w$ pesa $P(+s\mid C)P(+w\mid S,R)$.
- [ ] Rehacer la actualización de $S$ de §7.1 y explicar qué factores se cancelan.
- [ ] En el explorador, repetir corridas con distinto tamaño y comparar aceptados, pesos efectivos y trayectoria de Gibbs.
