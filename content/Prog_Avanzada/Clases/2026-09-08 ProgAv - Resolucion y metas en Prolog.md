---
tipo: clase
materia: "[[01_Materias/Prog_Avanzada/Indice|Programación Avanzada]]"
fecha: 2026-09-08
unidad: Programación lógica, resolución y Prolog
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[03_Conceptos/Prolog|Prolog]]"
  - "[[03_Conceptos/Cláusula de Horn|Cláusula de Horn]]"
  - "[[03_Conceptos/Resolución de primer orden|Resolución de primer orden]]"
  - "[[03_Conceptos/Resolución SLD|Resolución SLD]]"
  - "[[03_Conceptos/Unificación|Unificación]]"
referencias:
  - "[[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/regla-y-meta-en-prolog.jpeg|Demostración de regla y meta en Prolog]]"
  - "[[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-1.jpg|Ejemplo de resolución 1]]"
  - "[[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-2.jpg|Ejemplo de resolución 2]]"
  - "[[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-3.jpg|Ejemplo de resolución 3]]"
tags:
  - clase
  - programacion-avanzada
  - programacion-logica
  - prolog
  - resolucion
  - clausulas-horn
---

# Resolución, reglas y metas en Prolog

> [!summary] Pregunta central
> ¿Por qué Prolog puede ejecutar una regla reemplazando una meta por las premisas de esa regla, y cómo se relaciona este procedimiento con una demostración por refutación mediante resolución?

## Idea principal

Un programa lógico describe conocimiento mediante **hechos** y **reglas**. Una consulta se convierte en una lista de **metas pendientes**. Prolog intenta demostrarla seleccionando una meta, unificándola con la cabeza de una regla y sustituyéndola por el cuerpo de esa regla. Este paso operacional no es un truco del lenguaje: es una instancia de la regla lógica de resolución aplicada a [[03_Conceptos/Cláusula de Horn|cláusulas de Horn]].

La búsqueda termina de dos maneras:

- **Éxito:** ya no quedan metas; aparece la meta vacía, equivalente a la cláusula vacía $\square$ en la refutación.
- **Fallo de una rama:** ninguna cláusula del programa puede resolver la meta seleccionada; Prolog retrocede para intentar otra regla.

---

## 1. Notación mínima

### Átomos, literales y cláusulas

Un **átomo** es una expresión como $R(X)$ o $mortal(socrates)$. Un **literal** es un átomo o su negación. Una **cláusula** es una disyunción de literales:

$$\neg S(X)\vee T(X).$$

Esta cláusula tiene una lectura equivalente como implicación:

$$S(X)\to T(X),$$

y como regla de Prolog:

~~~prolog
t(X) :- s(X).
~~~

En general, la regla

$$A\leftarrow B_1,\ldots,B_m$$

abrevia

$$B_1\land\cdots\land B_m\to A,$$

y en forma clausal se escribe

$$A\vee\neg B_1\vee\cdots\vee\neg B_m.$$

La **cabeza** es $A$ y el **cuerpo** contiene $B_1,\ldots,B_m$. Una regla de esta forma es una cláusula definida: contiene exactamente un literal positivo.

### Metas

La consulta conjunta

~~~prolog
?- a1, a2, ..., an.
~~~

se representa como la cláusula objetivo

$$\leftarrow A_1,A_2,\ldots,A_n,$$

equivalente a

$$\neg A_1\vee\neg A_2\vee\cdots\vee\neg A_n.$$

La flecha hacia la izquierda puede leerse como: «todavía falta demostrar estas metas».

> [!important] Dos objetos que no deben confundirse
> El **programa** contiene cláusulas definidas (hechos y reglas). La **consulta** produce una cláusula objetivo, sin literales positivos. La ejecución conecta ambos objetos mediante resolución.

---

## 2. Regla general de resolución

Si dos cláusulas contienen literales complementarios que pueden unificarse, esos literales se eliminan y el unificador se aplica a todo lo restante. Sean

$$C\vee L \qquad\text{y}\qquad D\vee\neg L',$$

y sea $\theta$ un unificador de $L$ y $L'$. Entonces:

$$
\frac{C\vee L,\qquad D\vee\neg L'}{(C\vee D)\theta}.
$$

El resultado se llama **resolvente**. En lógica proposicional los literales complementarios deben coincidir exactamente; en primer orden basta con que exista una sustitución que los vuelva iguales.

> [!example] Unificación rápida
> $mortal(X)$ y $mortal(socrates)$ unifican con $\theta=\{X/socrates\}$. En cambio, $p(a)$ y $p(b)$ no unifican si $a$ y $b$ son constantes distintas.

---

## 3. De una regla y una meta al siguiente objetivo

Supongamos que el programa contiene una regla cuya cabeza puede unificarse con la meta seleccionada $A_k$:

$$A\leftarrow B_1,\ldots,B_m,$$

y que el objetivo actual es

$$\leftarrow A_1,\ldots,A_{k-1},A_k,A_{k+1},\ldots,A_n.$$

Primero se renombran las variables de la regla si hace falta, para que sean independientes de las del objetivo. Después se calcula

$$\theta=UMG(A,A_k),$$

donde UMG significa **unificador más general**. El siguiente objetivo es:

$$
\boxed{
\leftarrow
(A_1,\ldots,A_{k-1},B_1,\ldots,B_m,A_{k+1},\ldots,A_n)\theta
}
$$

Es decir: se elimina la meta resuelta $A_k$ y, en su lugar, se insertan las premisas que todavía deben demostrarse.

### Por qué esta sustitución es resolución

La regla equivale a:

$$A\vee\neg B_1\vee\cdots\vee\neg B_m,$$

y el objetivo equivale a:

$$\neg A_1\vee\cdots\vee\neg A_k\vee\cdots\vee\neg A_n.$$

Al resolver $A$ con $\neg A_k$ se cancelan esos dos literales. Queda:

$$
(\neg A_1\vee\cdots\vee\neg A_{k-1}
\vee\neg B_1\vee\cdots\vee\neg B_m
\vee\neg A_{k+1}\vee\cdots\vee\neg A_n)\theta,
$$

que, regresando a notación de metas, es justamente el objetivo enmarcado arriba.

> [!note] Caso de un hecho
> Un hecho $A$ puede verse como $A\leftarrow true$. Al resolverlo, $A_k$ se reemplaza por un cuerpo vacío. Si era la última meta, obtenemos la meta vacía y la consulta tiene éxito.

---

## 4. Ejemplo de resolución general por refutación

Sea

$$
S=\left\{
R(X)\vee S(X),\;
\neg S(X)\vee T(X),\;
\neg T(X)\vee R(X)
\right\}.
$$

Queremos probar:

$$S\models R(X).$$

La prueba por refutación agrega la negación de la conclusión, $\neg R(X)$, y busca derivar $\square$:

$$
\begin{aligned}
C_1 &: R(X)\vee S(X),\\
C_2 &: \neg S(X)\vee T(X),\\
C_3 &: \neg T(X)\vee R(X),\\
C_4 &: \neg R(X).
\end{aligned}
$$

Una derivación posible es:

$$
\begin{array}{rcll}
C_4, C_3 &\Rightarrow& \neg T(X) & \text{se elimina }R(X),\\
\neg T(X), C_2 &\Rightarrow& \neg S(X) & \text{se elimina }T(X),\\
\neg S(X), C_1 &\Rightarrow& R(X) & \text{se elimina }S(X),\\
R(X), C_4 &\Rightarrow& \square. &
\end{array}
$$

Como $S\cup\{\neg R(X)\}$ es inconsistente, concluimos:

$$\boxed{S\models R(X).}$$

> [!note] Refutación frente a esquema de búsqueda
> Una **refutación** muestra una secuencia que sí alcanza $\square$. El **esquema de búsqueda** contiene también las elecciones alternativas que el algoritmo pudo haber intentado. Por eso el segundo suele ser mucho más ancho que la prueba final.

---

## 5. El mismo mecanismo restringido a Prolog

Considérese el programa clausal:

$$
P=\left\{
\neg S(X)\vee T(X),\;
\neg T(X)\vee R(X),\;
\neg Q(X)\vee R(X),\;
S(X)
\right\}.
$$

Su escritura como programa es:

~~~prolog
t(X) :- s(X).
r(X) :- t(X).
r(X) :- q(X).
s(X).
~~~

La consulta es:

~~~prolog
?- r(X).
~~~

La cláusula objetivo inicial es $\leftarrow R(X)$, o de forma disyuntiva, $\neg R(X)$. Si elegimos la regla $R(X)\leftarrow T(X)$, la derivación SLD es:

$$
\begin{aligned}
G_0 &: \leftarrow R(X)\\
G_1 &: \leftarrow T(X)\\
G_2 &: \leftarrow S(X)\\
G_3 &: \square
\end{aligned}
$$

Interpretación paso a paso:

1. Para demostrar $R(X)$ basta demostrar $T(X)$.
2. Para demostrar $T(X)$ basta demostrar $S(X)$.
3. $S(X)$ es un hecho; no deja submeta pendiente.
4. La lista de metas queda vacía y la consulta tiene éxito.

La otra regla para $R(X)$ produciría la meta $\leftarrow Q(X)$. Como el programa no contiene un hecho ni una regla cuya cabeza sea $Q$, esa rama falla. El retroceso permite regresar y probar la alternativa basada en $T(X)$.

> [!warning] El orden sí importa operacionalmente
> Lógicamente, reordenar cláusulas no cambia el conjunto de consecuencias. En Prolog habitual, sin embargo, se selecciona la meta más a la izquierda y se prueban las cláusulas en el orden del programa mediante búsqueda en profundidad. Un orden desafortunado puede hacer la ejecución lenta o incluso no terminante.

---

## 6. Explorador paso a paso

<iframe src="../../prog_avanzada/recursos/resolucion-prolog-paso-a-paso.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

El recurso permite alternar entre la refutación general y la derivación SLD. En ambos casos se elimina un par de literales complementarios; la diferencia es que SLD mantiene una **meta central** y siempre resuelve contra una cláusula del programa, lo que reduce drásticamente el espacio de búsqueda.

---

## 7. Resolución general vs. resolución SLD

| Aspecto | Resolución general | Resolución SLD / Prolog |
|---|---|---|
| Cláusulas permitidas | Cláusulas arbitrarias | Cláusulas definidas + una meta |
| Elección | Puede resolver diversos pares de cláusulas | Resuelve una meta con una regla del programa |
| Forma de la derivación | Árbol o grafo amplio | Derivación lineal por rama |
| Dirección intuitiva | Buscar una contradicción | Reducir metas a submetas |
| Éxito | Se deriva $\square$ | La lista de metas queda vacía |
| Alternativas | Muchas combinaciones posibles | Se exploran mediante retroceso |

La «L» de SLD significa **lineal**: cada nuevo resolvente se obtiene del objetivo anterior y una cláusula del programa. La «S» recuerda que existe una **regla de selección** para escoger cuál meta resolver. La «D» alude a **cláusulas definidas**.

---

## 8. Errores frecuentes

1. **Agregar la conclusión en vez de negarla.** En refutación se trabaja con $S\cup\{\neg F\}$.
2. **Confundir conjunción de metas con disyunción clausal.** $\leftarrow A,B$ representa $\neg A\vee\neg B$, no $A\vee B$.
3. **Olvidar aplicar el unificador al resto.** La sustitución $\theta$ afecta todo el resolvente, no solo el par eliminado.
4. **No renombrar variables entre cláusulas.** Dos variables con el mismo nombre en reglas distintas no tienen por qué ser la misma variable.
5. **Confundir falla de una rama con falsedad lógica.** Una elección puede fallar aunque otra rama sí demuestre la consulta.
6. **Creer que una búsqueda que no termina equivale a falso.** Prolog puede quedarse atrapado en una rama infinita antes de alcanzar una alternativa exitosa.

---

## 9. Comprobación rápida

> [!question]- ¿Qué meta queda al resolver $\leftarrow padre(X,Z),ancestro(Z,Y)$ con el hecho $padre(ana,luis)$?
> La primera meta unifica con el hecho mediante $\theta=\{X/ana,Z/luis\}$. Queda $\leftarrow ancestro(luis,Y)$.

> [!question]- ¿Qué significa obtener $\square$ en una refutación?
> Que el conjunto formado por el programa y la negación de la consulta es insatisfactible; por tanto, la consulta se sigue lógicamente del programa.

> [!question]- ¿Por qué la búsqueda de Prolog es más estrecha que el esquema de resolución general?
> Porque solo resuelve el objetivo actual contra cláusulas definidas del programa y selecciona una meta concreta; no combina libremente cualquier par de cláusulas derivadas.

## Resumen después de clase

Una regla de Prolog $A\leftarrow B_1,\ldots,B_m$ es la cláusula de Horn $A\vee\neg B_1\vee\cdots\vee\neg B_m$. Una consulta es una cláusula objetivo formada por las negaciones de las metas pendientes. Resolver la cabeza $A$ contra una meta seleccionada $A_k$ elimina esa meta y agrega el cuerpo de la regla, aplicando el unificador más general. La resolución SLD restringe la resolución general para producir derivaciones lineales guiadas por metas; Prolog añade una estrategia concreta de selección, orden y retroceso.

## Fuentes de la clase

- [[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/regla-y-meta-en-prolog.jpeg|Demostración manuscrita: regla y meta en Prolog]].
- [[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-1.jpg|Ejemplo de refutación y esquema de búsqueda]].
- [[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-2.jpg|Programa clausal y meta para Prolog]].
- [[01_Materias/Prog_Avanzada/Recursos/Fuentes-2026-09-08/ejemplo-resolucion-3.jpg|Refutación y búsqueda restringida en Prolog]].

