---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: "2026-10-29"
unidad: Aprendizaje automático
profesor: Carlos Hernández
estado: procesada
conceptos: []
referencias:
tags:
  - clase
  - inteligencia-artificial
  - aprendizaje-no-supervisado
  - clustering
---

# Aprendizaje no supervisado: agrupamiento y jerarquías

> [!summary] Pregunta central
> Si los datos no tienen etiquetas, ¿cómo descubrimos grupos, elegimos una noción de semejanza y evaluamos si el resultado tiene sentido?

Este apunte trata el **aprendizaje no supervisado** de la sesión del **29 de octubre de 2026**. El [[Indice|plan del curso]] aún asigna «aprendizaje supervisado» a ese día; el contenido es el efectivamente visto. Continúa la [[2026-10-27 IA - Aprendizaje supervisado y clasificacion|clase de clasificación]] contrastando datos con y sin etiquetas. La nota es autocontenida: las definiciones, las fórmulas y los ejemplos numéricos se desarrollan completos. Al final se hace una **introducción** al aprendizaje por refuerzo, tema de la siguiente clase.


| Tema | Sección |
|---|---|
| Aprendizaje sin etiquetas y tareas posibles | §1 |
| Distancias, prototipos y vecino más cercano | §2 |
| k-means, otros métodos y silueta | §§3–4 |
| Agrupamiento jerárquico y *linkage* | §5 |
| Transición a aprendizaje por refuerzo | §6 |

## 1. Aprender estructura sin etiquetas

En aprendizaje **supervisado**, cada ejemplo incluye una respuesta conocida $y_i$. En el **no supervisado** observamos solo $\mathbf x_1,\ldots,\mathbf x_n$ y buscamos estructura útil: grupos, variables latentes, dimensiones relevantes o relaciones entre variables. La ausencia de etiquetas facilita reunir datos, pero también hace que «un grupo correcto» dependa de la **representación, distancia y finalidad** del análisis. Ejemplos: subpoblaciones celulares, patrones de compra, clases de estrellas y correlaciones entre acciones.

| Tarea | Pregunta | Ejemplos |
|---|---|---|
| Agrupamiento (*clustering*) | ¿Cuántos grupos existen? Agrupar datos en $K$ grupos; dado un dato nuevo, colocarlo en un grupo | descubrir un nuevo tipo de estrella a partir de medidas astrofísicas; agrupar usuarios por compras o comportamiento para enviar promociones; descubrir subpoblaciones de células en datos de citometría de flujo |
| Variables latentes (ocultas) | Reducción de dimensionalidad | — |
| Estructura de grafos | Descubrir un conjunto de variables correlacionadas | modelar correlaciones entre acciones para estrategias de trading; predicción de tráfico en vías rápidas |

El aprendizaje no supervisado quizá es más común que el supervisado y más aplicable porque no requiere etiquetas, pero cada ejemplo contiene relativamente poca información.

A veces se escribe $p(x_i\mid\theta)$ y se le describe como una «función de etiquetado». Conviene separar las ideas: $p(x\mid\theta)$ es un **modelo de densidad**; una función $g(x)\in\{1,\ldots,K\}$ **asigna grupos**. Se puede usar un modelo probabilístico para obtener asignaciones, pero no son la misma función. Tampoco hay una clase verdadera implícita en cada grupo hallado.

Dos problemas distintos guían la sesión:

1. **Asignar una observación nueva** a grupos o clases ya representados por prototipos.
2. **Construir los grupos** a partir de datos sin etiquetas.

## 2. La distancia determina qué se parece

Para vectores $x,y\in\mathbb R^d$, la familia de normas $p$ ($p\geq1$) induce distancias

$$
d_p(x,y)=\|x-y\|_p=\left(\sum_{j=1}^{d}|x_j-y_j|^p\right)^{1/p},\qquad d_\infty(x,y)=\max_j|x_j-y_j|.
$$

En particular, $L_1$ suma diferencias absolutas y $L_2$ mide distancia euclidiana. Una **métrica** cumple $d(x,y)\geq0$, $d(x,y)=0\Leftrightarrow x=y$, simetría y desigualdad triangular $d(x,z)\leq d(x,y)+d(y,z)$ . La forma de las regiones de cercanía cambia al cambiar la norma ($L_1$ da regiones en forma de rombo, $L_2$ circulares y $L_\infty$ cuadradas; al dibujar las «bolas» unitarias, cada norma da su figura, anidadas para distintos $p$), y con ella pueden cambiar los vecinos y las asignaciones.

> [!warning] Cuidado con la «norma 0»
> A veces se llama «norma 0» a $\sum_j\mathbf1(x_j=y_j)$. Esa suma **cuenta coincidencias**, de modo que aumenta cuando dos vectores se parecen y no vale cero para $x=y$. Una distancia para atributos categóricos es la **distancia de Hamming** $d_H(x,y)=\sum_j\mathbf1(x_j\ne y_j)$. La llamada «norma $L_0$» en contextos de dispersidad cuenta componentes **no nulas** de $x-y$; técnicamente no es una norma.

Antes de usar distancias, hay que decidir qué características representan el problema y cómo escalarlas: una variable medida en miles puede dominar a otra medida entre 0 y 1. La elección de escala puede cambiar los grupos incluso con el mismo algoritmo. Para datos mixtos o categóricos, la distancia euclidiana puede ser inadecuada.

### Prototipos y vecinos

Con un prototipo $\mu_j$ por grupo $C_j$, asignamos una nueva observación por cercanía:

$$
g(x)=\operatorname*{arg\,min}_{j\in\{1,\ldots,K\}}d(x,\mu_j).
$$

Con un único prototipo $y_i$ por clase $C_i$ ($1\le i\le m$), $d_i=\|x-y_i\|=\sqrt{(x-y_i)^\mathsf T(x-y_i)}$ y un clasificador de distancia mínima asigna $x$ a $C_j$ con $d_j=\min_i\|x-y_i\|$; la frontera de decisión entre dos prototipos es la mediatriz de su segmento. Con dos clases de puntos (cuadrados azules y triángulos rojos) y un punto nuevo, el vecino más cercano decide su clase, y con $k$ mayor se mira un círculo más amplio. Si una clase tiene varias formas o regiones separadas, puede requerir **varios prototipos**. El **vecino más cercano** (NN) usa cada ejemplo almacenado como referencia; $k$-NN vota entre los $k$ vecinos más próximos. Estos métodos presuponen ejemplos *clasificados a priori*: **NN y k-NN son clasificadores supervisados en ese caso**, aunque aparezcan aquí para explicar asignación por distancia. El $K$ de k-means es el **número de grupos**; el $k$ de k-NN es el **número de vecinos**.

## 3. k-means: generar grupos con centroides

El algoritmo de **Lloyd** busca una partición $C_1,\ldots,C_K$ y centroides $\mu_j$ que reduzcan la suma de distancias euclidianas **al cuadrado**:

$$
J(C,\mu)=\sum_{j=1}^{K}\sum_{x_i\in C_j}\|x_i-\mu_j\|_2^2,\qquad \mu_j=\frac{1}{|C_j|}\sum_{x_i\in C_j}x_i.
$$

En pseudocódigo (*Lloyd*, entrada $D\subset\mathbb R^d$ y $K$; salida: medias $\mu_1,\dots,\mu_K$): inicializar $\mu_1,\dots,\mu_K$ al azar; repetir: asignar cada $x\in D$ al grupo $\arg\min_jd(x,\mu_j)^2$, y para $j=1..K$ hacer $D_j\leftarrow\{x$ asignados a $j\}$ y $\mu_j\leftarrow\frac1{|D_j|}\sum_{x\in D_j}x$; hasta que $\mu_1,\dots,\mu_K$ no cambien; devolver $\mu$. En resumen:

1. Elegir $K$ y centroides iniciales.
2. **Asignar** cada punto al centroide más cercano.
3. **Actualizar** cada centroide con la media de los puntos asignados.
4. Repetir hasta que las asignaciones o los centroides dejen de cambiar (o se alcance un límite de iteraciones).

Cada uno de los pasos 2 y 3 no aumenta $J$; el algoritmo termina en una solución **local**, que puede depender de la inicialización. Minimizar $J$ sobre todas las particiones, $\arg\min_C\sum_{i=1}^k\sum_{x_j\in C_i}\|x_j-\mu_i\|^2$, es un problema NP-difícil, de modo que encontrar el óptimo global es difícil en general. Por eso conviene ejecutar varias inicializaciones y comparar resultados. Un grupo vacío requiere una regla de reinicialización o manejo explícito.

**Ejemplo mínimo.** Para puntos unidimensionales $\{0,1,4,5\}$, $K=2$ y centros iniciales $(0,4)$, la asignación produce $C_1=\{0,1\}$ y $C_2=\{4,5\}$. La actualización da $\mu_1=0.5$ y $\mu_2=4.5$; entonces $J=4(0.5)^2=1$. La siguiente asignación no cambia y se detiene.

### Explorar las iteraciones

<iframe src="ia20-kmeans-lloyd.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El recurso permite cambiar $K$ y avanzar alternadamente por **asignación** y **actualización**. Observa cómo se mueven los centroides y cómo cambia $J$ después de cada fase completa. Los colores son grupos calculados, no etiquetas verdaderas.

**Límite geométrico.** k-means suele favorecer grupos compactos alrededor de centroides y puede fallar con anillos, medias lunas, densidades diferentes o ruido. En conjuntos de ejemplo con dos anillos concéntricos, dos medias lunas entrelazadas, nubes gaussianas de distinto tamaño, grupos pequeños y puntos uniformes, DBSCAN recupera los anillos y las medias lunas, mientras k-means corta esas formas en trozos por líneas rectas; en nubes compactas ambos coinciden. Conviene contrastar sus resultados con **DBSCAN**, que agrupa por densidad y puede dejar puntos como ruido; requiere elegir vecindad y mínimo de vecinos. Ningún método es universalmente mejor: depende de la estructura que se busca.

## 4. Evaluar un agrupamiento sin etiquetas

La **silueta** compara, para cada punto $x_i$, su separación interna y externa:

$$
a(i)=\text{distancia media de }x_i\text{ a los demás puntos de su grupo},
$$
$$
b(i)=\min_{C\ne C(i)}\ \text{distancia media de }x_i\text{ a los puntos de }C,
$$
$$
\boxed{s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}\in[-1,1].}
$$

Si $a=1$ y $b=4$, $s=0.75$: el punto está más cerca, en promedio, de su propio grupo. Un valor cercano a **0** indica frontera difusa; uno **negativo** sugiere que está más cerca de otro grupo. El promedio de $s(i)$ resume el conjunto, pero no sustituye la interpretación del problema. Para un grupo de un solo punto, $a(i)$ no está definido; muchas implementaciones toman $s(i)=0$ por convención. La fórmula requiere al menos dos grupos.

## 5. Agrupamiento jerárquico y dendrogramas

Un **dendrograma** muestra agrupaciones anidadas: las hojas son observaciones y cada nodo interno une dos grupos. La altura de la unión representa la distancia de *linkage* usada en ese paso. Un corte horizontal produce una partición; la jerarquía por sí sola **describe las observaciones** y no especifica cómo asignar un punto nuevo.

La distancia entre **puntos** no determina por sí sola la distancia entre **grupos**. Para conjuntos $A,B$ y una distancia base $d$:

| *Linkage* | $L(A,B)$ | Efecto habitual |
|---|---|---|
| Simple | $\min_{x\in A,y\in B}d(x,y)$ | Puede formar cadenas por pares cercanos |
| Completo | $\max_{x\in A,y\in B}d(x,y)$ | Favorece grupos compactos |
| Promedio | $\frac{1}{|A||B|}\sum_{x\in A,y\in B}d(x,y)$ | Equilibra extremos |
| Centroide | $d(\bar x_A,\bar x_B)$ | Compara las medias de los grupos |

Casos especiales: si $A=\{x\}$ y $B=\{y\}$ todos los *linkages* coinciden con $\mathrm{Dis}(x,y)$; si $A=\{x\}$, $B=\{y,z\}$ y $\mathrm{Dis}(x,y)<\mathrm{Dis}(x,z)$, entonces simple $=\mathrm{Dis}(x,y)$, completo $=\mathrm{Dis}(x,z)$, promedio $=(\mathrm{Dis}(x,y)+\mathrm{Dis}(x,z))/2$ y centroide $=\mathrm{Dis}(x,(y+z)/2)$. Si $A=\{0\}$ y $B=\{3,5\}$ en la recta con distancia absoluta, los cuatro valores son, respectivamente, **3, 5, 4 y 4**. Así se ve que la altura de unión depende de la regla elegida.

**Ejemplo de dendrograma.** Con los puntos $A=0$, $B=1$, $C=5$, $D=6$ en la recta y *linkage* simple, el algoritmo aglomerativo une primero $A$ con $B$ (distancia 1) y $C$ con $D$ (distancia 1), y después los dos grupos resultantes, cuya distancia es $\min d=5-1=4$:

```text
altura
  4 ┤      ┌────────┴────────┐
    │      │                 │
  1 ┤   ┌──┴──┐           ┌──┴──┐
    │   │     │           │     │
  0 ┴───A     B           C     D
      (x=0) (x=1)       (x=5) (x=6)
```

Un corte horizontal a altura 2 produce dos grupos, $\{A,B\}$ y $\{C,D\}$; un corte a altura 0.5 produce cuatro grupos. En *linkage* de centroide pueden aparecer inversiones: una unión posterior puede tener altura menor que una anterior.

El método **aglomerativo** comienza con un grupo por punto y fusiona repetidamente los dos grupos más cercanos; construye de abajo hacia arriba. El **divisivo** empieza con todos los puntos juntos y los divide; por ejemplo, mediante bisecciones sucesivas con k-means ($K=2$) o mediante una división basada en disimilitudes. Algoritmos: el **aglomerativo** inicializa cada punto como grupo; repite: elegir el par de grupos más similar $(j,k)=\arg\min d$ entre los disponibles, fusionarlos en $C_\ell=C_j\cup C_k$, marcar $j,k$ como no disponibles, habilitar $\ell$ y actualizar la matriz de disimilitud; hasta que no queden grupos por fusionar. El **divisivo por bisección con k-means** parte de $S=\{\{1,\dots,N\}\}$; repite: elegir el grupo $G$ de mayor diámetro, dividirlo con k-means ($K=2$) en $G_1,G_2$ y reemplazar $G$ por ambos; hasta cumplir un criterio de paro (p. ej., número de grupos deseado). El **divisivo basado en disimilitud** empieza con $G=\{1,\dots,N\}$ y $H=\emptyset$: calcula para cada $i\in G$ la disimilitud media $d_i^G$ a los demás de $G$, mueve de $G$ a $H$ el de mayor $d^G_i$, y luego repite: para cada $i\in G$ compara $d_i^G$ con la disimilitud media $d_i^H$ a $H$ y mueve a $H$ el $i$ con mayor $d_i^G-d_i^H$, hasta que el criterio de paro se cumpla; devuelve $G$ y $H$. A diferencia de k-means, el método jerárquico no exige fijar $K$ antes de construir el árbol, aunque sí hay que elegir un corte para obtener $K$ grupos.

**En la práctica**, selección de características y reducción de dimensionalidad pueden hacer más útiles tanto las distancias como las visualizaciones; también pueden perder información, así que deben justificarse con el objetivo del análisis.

## 6. Puente hacia aprendizaje por refuerzo

El último tema cambia de escenario: un **agente** toma acciones, observa consecuencias y recibe recompensas. No se trata de descubrir grupos en un conjunto fijo de datos, sino de aprender a **decidir** a partir de interacción. Un agente recibe retroalimentación en forma de recompensas y debe actuar para maximizar su valor esperado; todo el aprendizaje se basa en los ejemplos observados. Aplicaciones: vehículos autónomos, automatización industrial, trading automático, procesamiento de lenguaje natural, videojuegos, robótica, marketing, colocación de recursos, control de semáforos, manufactura y balanceo de cargas. El ejemplo de rejilla (4 columnas por 3 filas, con la casilla de inicio abajo a la izquierda en $(1,1)$, una pared en $(2,2)$, una recompensa $+1$ en $(4,3)$ y una penalización $-1$ en $(4,2)$) tiene paredes y acciones inciertas: al pedir «norte», el agente va al norte con probabilidad $0.8$, al oeste con $0.1$ y al este con $0.1$; si encuentra una pared, permanece en su estado. Recompensas pequeñas por paso y recompensas terminales hacen que importe la secuencia de decisiones.

Un **proceso de decisión de Markov (MDP)** se describe mediante estados $S$, acciones $A$, transiciones $T(s,a,s')=P(s'\mid s,a)$, recompensa $R(s,a,s')$, estado inicial y posiblemente estados terminales. Se busca una **política** $\pi:S\to A$ que maximice la recompensa acumulada esperada. El criterio exacto necesita además precisar horizonte o descuento; todavía no se desarrolla en esta sesión. En planificación con MDP se conocen $T$ y $R$; en aprendizaje por refuerzo al menos uno se desconoce y debe aprenderse o sortearse mediante experiencia. La siguiente clase continúa este tema.

## Comprobaciones para estudiar

1. ¿Por qué cambiar la escala de una característica puede alterar k-means?  
   > [!check]- Respuesta
   > Porque cambia las distancias a los centroides y, por tanto, las asignaciones y las medias posteriores.
2. ¿Qué diferencia hay entre el $K$ de k-means y el $k$ de k-NN?  
   > [!check]- Respuesta
   > $K$ fija el número de grupos a construir; $k$ fija cuántos ejemplos etiquetados votan al clasificar uno nuevo.
3. Si $a(i)=4$ y $b(i)=2$, ¿cuál es la silueta?  
   > [!check]- Respuesta
   > $s(i)=(2-4)/4=-0.5$: el punto está, en promedio, más cerca de otro grupo.
4. ¿Qué cambia entre *linkage* simple y completo?  
   > [!check]- Respuesta
   > Simple usa el par de puntos más cercano entre grupos; completo usa el par más lejano.
5. ¿Qué información adicional aparece en aprendizaje por refuerzo?  
   > [!check]- Respuesta
   > Acciones, transiciones y recompensas a lo largo del tiempo; se aprende una política de decisión.

## Resumen después de clase

El aprendizaje no supervisado busca estructura en datos sin respuestas etiquetadas. El agrupamiento exige elegir características y una distancia; k-means alterna asignaciones y medias para reducir la suma de errores cuadrados, mientras que el agrupamiento jerárquico organiza observaciones en un dendrograma según una regla de *linkage*. La silueta ayuda a evaluar separación y cohesión, pero la utilidad final depende del problema. La clase termina introduciendo agentes que aprenden de recompensas.

## Acciones de estudio

- [ ] Rehacer a mano dos iteraciones de Lloyd con $K=2$ y calcular $J$.
- [ ] Comparar siluetas de puntos bien asignados y puntos en frontera.
- [ ] Calcular los cuatro *linkages* para dos grupos pequeños y dibujar un dendrograma aglomerativo.
- [ ] Explicar por qué vecino más cercano con etiquetas es supervisado y por qué el MDP introduce un problema distinto.
