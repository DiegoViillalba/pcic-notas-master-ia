---
tipo: clase
materia: "[[Indice|Programación Avanzada]]"
fecha: 2026-09-10
unidad: "Programación lógica en Prolog: hechos, unificación, backtracking y corte"
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[Prolog|Prolog]]"
  - "[[Unificación|Unificación]]"
  - "[[Backtracking en Prolog|Backtracking en Prolog]]"
  - "[[Corte (cut) en Prolog|Corte (cut) en Prolog]]"
  - "[[Negación como falla|Negación como falla]]"
  - "[[Cláusula de Horn|Cláusula de Horn]]"
referencias:
  - "[[Programación Avanzada Notas 9.pdf|Programación Avanzada Notas 9]]"
  - "[[console-gusta-atomos.png|Consola: consultas con átomos]]"
  - "[[console-gusta-variables.png|Consola: consultas con variables]]"
  - "[[console-mayusculas-variables.png|Consola: mayúsculas como variables]]"
  - "[[console-recibe-error-sintaxis.png|Consola: error de sintaxis con espacio]]"
tags:
  - clase
  - programacion-avanzada
  - programacion-logica
  - prolog
  - unificacion
  - backtracking
  - corte
---

![[Programación Avanzada Notas 9.pdf]]

# Hechos, unificación, backtracking y corte en Prolog

## Pregunta central

La clase pasada vimos que Prolog resuelve una consulta **reemplazando una meta por el cuerpo de una regla**, y que ese paso es una instancia de resolución sobre cláusulas de Horn. Hoy bajamos de la teoría a la práctica: ¿cómo se ven esos hechos y reglas realmente escritos en un archivo `.pl`?, ¿qué hace Prolog exactamente cuando una variable se **unifica** con un átomo?, ¿qué significa pedirle "otra respuesta" con `;`?, y ¿cómo se le indica a Prolog que **deje de buscar** alternativas con el corte `!`?

## Mapa de la clase

~~~mermaid
flowchart LR
    P["Instalar Prolog: SWI, Visual Prolog, GNU"] --> H["Hechos y reglas: Proposiciones.pl"]
    H --> N["Negación como falla: \\+"]
    H --> D["Una regla derivada: DaRegalo.pl"]
    D --> U["Unificación: MariaGusta.pl"]
    U --> B["Backtracking: pedir más soluciones con ;"]
    B --> M["Mayúscula = variable, minúscula = átomo"]
    U --> S["Simulador interactivo de consola"]
    B --> C["El corte !: podar alternativas"]
    C --> E["Ejemplos con corte: mayor, max, factorial, fib, potencia"]
~~~

Trabajamos directamente sobre los cuatro programas Prolog de la carpeta `Primera Parte`: `Proposiciones.pl`, `DaRegalo.pl`, `MariaGusta.pl` y `EjemplosProlog.pl`. *(Notas 9, láminas 164–170.)*

---

## 1. Instalar y ejecutar Prolog

Las diapositivas señalan tres implementaciones distintas de Prolog, todas gratuitas:

| Implementación | Sitio | Uso típico en el curso |
|---|---|---|
| **SWI-Prolog** | swi-prolog.org | La consola usada en los ejemplos de esta clase |
| **Visual Prolog** | visual-prolog.com | Entorno multiparadigma con IDE propio |
| **GNU Prolog** | gprolog.org | Compilador nativo (genera ejecutables) |

> [!tip] Cómo se carga un programa
> En SWI-Prolog, `File → Consult…` (o arrastrar el archivo) compila el `.pl` y muestra en verde algo como:
> `c:/Users/.../MariaGusta.pl compiled 0.00 sec, 4 clauses`
> A partir de ahí, el símbolo `?-` es el indicador de consulta.

---

## 2. Hechos y reglas: `Proposiciones.pl`

~~~prolog
% Hechos:
a.
b.
c.
d.
e :- fail.

% Reglas:
x :- a, b, c, d.
k :- a, b.
y :- b, \+ e, a.
z :- f, g, h.
w :- e, c, d.

m :- c, ( e ; a), d.
n :- c, ( \+ a; \+ e ), d.
o :- c, \+ a, d.
~~~

Esto conecta directamente con la notación de la clase pasada: cada hecho como `a.` es una cláusula de Horn sin cuerpo (`a ← true`), y cada regla `A :- B1, ..., Bn.` es `A ← B1 ∧ ... ∧ Bn`. `,` es **conjunción**, `;` es **disyunción**, y `\+` es [[Negación como falla|negación como falla]] (tiene éxito si el programa **no puede demostrar** su argumento).

### 2.1. Trazar cada regla a mano

| Consulta | ¿Éxito? | Justificación |
|---|:---:|---|
| `?- a.` `?- b.` `?- c.` `?- d.` | ✔ | Son hechos directos. |
| `?- e.` | ✘ | Su única regla es `fail`, que siempre falla. |
| `?- x.` | ✔ | `a, b, c, d` son todos hechos verdaderos. |
| `?- k.` | ✔ | `a` y `b` son hechos verdaderos. |
| `?- y.` | ✔ | `b` es verdadero; `\+ e` tiene éxito porque `e` es indemostrable; `a` es verdadero. |
| `?- z.` | ✘ | `f`, `g`, `h` no están definidos en el programa (Prolog los trata como falsos / los reporta como predicado desconocido). |
| `?- w.` | ✘ | Ya falla en la primera meta, `e`. |
| `?- m.` | ✔ | `c` es verdadero; en `(e ; a)` la primera opción `e` falla pero la segunda `a` tiene éxito; `d` es verdadero. |
| `?- n.` | ✔ | `c` es verdadero; en `(\+a ; \+e)` la primera opción `\+a` falla (porque `a` sí es demostrable), pero `\+e` tiene éxito; `d` es verdadero. |
| `?- o.` | ✘ | `c` es verdadero, pero `\+ a` falla porque `a` sí se puede demostrar. |

> [!important] `;` dentro de una regla no es lo mismo que pedir otra solución
> Aquí `( e ; a )` es **disyunción dentro del cuerpo de una regla**: Prolog prueba `e`, y si falla, prueba `a`. Es distinto del `;` que se escribe en la consola para pedir la *siguiente* solución de una consulta (sección 4). Ambos usan el mismo símbolo porque, internamente, pedir otra solución también es "probar la siguiente alternativa disponible".

---

## 3. Una regla derivada de un hecho: `DaRegalo.pl`

~~~prolog
% Jaime le da un regalo a María:
da( jaime, regalo, maria ).
recibe( maria, regalo) :- da( jaime, regalo, maria ).
~~~

Es el ejemplo más pequeño posible de la mecánica de la clase pasada: `recibe(maria, regalo)` no es un hecho, es una **meta que se resuelve** contra la regla, cuyo cuerpo es exactamente el hecho `da(jaime, regalo, maria)`. Al consultar `?- recibe(maria, regalo).`, Prolog sustituye la meta por el cuerpo de la regla, encuentra que coincide con el hecho, y responde `true.`.

---

## 4. Unificación y sustitución: `MariaGusta.pl`

~~~prolog
gusta( maria, helado ).
gusta( maria, leer ).
gusta( maria, cine ).

dar( juan, beso, maria ).
recibe( X, beso ) :- dar( juan, beso, X ).
~~~

**Unificar** dos términos significa encontrar una sustitución que los haga idénticos. Con solo tres hechos, ya aparecen los cuatro casos posibles:

| Consulta | Unificación | Resultado |
|---|---|---|
| `gusta( maria, leer ).` | átomo con átomo, coinciden | `true.` |
| `gusta( maria, chocolate ).` | átomo con átomo, **no** coinciden | `false.` |
| `gusta( Y, leer ).` | variable con átomo | `Y = maria.` |
| `gusta( maria, X ).` | átomo con variable, tres hechos posibles | `X = helado ; X = leer ; X = cine.` |
| `gusta( Y, X ).` | variable con variable, en ambas posiciones | tres soluciones, una por hecho |

![[console-gusta-atomos.png]]

### 4.1. Pedir más soluciones con `;`

Cada vez que se escribe `;` después de una respuesta, Prolog **retrocede** (backtracking) hasta el último hecho que aún no había probado y vuelve a unificar. Esto es exactamente enumerar, uno por uno, todos los puntos de elección que quedaron abiertos:

![[console-gusta-variables.png]]

### 4.2. La trampa de las mayúsculas

En Prolog, **cualquier identificador que empiece con mayúscula es una variable**, sin importar qué palabra sea. `Maria` y `maria` son símbolos completamente distintos: el primero es una variable libre, el segundo es la constante (átomo) definida en los hechos.

![[console-mayusculas-variables.png]]

> [!warning] `gusta( maria, Maria )` no pregunta "¿a María le gusta ella misma?"
> `Maria` (con mayúscula) es una variable nueva, sin relación con el átomo `maria` del primer argumento. La consulta simplemente pregunta "¿qué cosas le gustan a maria?", y por eso da las mismas tres respuestas que `gusta(maria, X)`, solo que la variable se llama distinto.

### 4.3. Un error de sintaxis clásico

~~~text
?- recibe ( X, beso ).
ERROR: Syntax error: Operator expected
~~~

![[console-recibe-error-sintaxis.png]]

En Prolog **no puede haber un espacio entre el nombre del predicado y el paréntesis de apertura**. `recibe( X, beso )` es una llamada al predicado `recibe/2`; `recibe ( X, beso )` es, sintácticamente, otra cosa (el analizador espera un operador después del átomo `recibe`), y por eso truena. Es uno de los errores más comunes al empezar con Prolog.

---

## 5. Simulador interactivo: consola y corte

<iframe src="prolog-unificacion-simulador.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

Usa los chips para lanzar cualquiera de las consultas de las secciones 4.1–4.3 (incluyendo el error de sintaxis) y pulsa «Siguiente solución ( ; )» para reproducir el backtracking exactamente como en la consola real. Más abajo, el segundo panel deja alternar entre "sin corte" y "con corte" para ver qué rama del árbol de búsqueda queda podada.

---

## 6. Programas y aridad: `EjemplosProlog.pl`

~~~prolog
% Obtiene el máximo de dos números:
maximo( X, Y, X ) :- X >= Y.
maximo( X, Y, Y ) :- X < Y.

mayor( X, Y, X ) :- X >= Y, !.
mayor( X, Y, Y ) :- X < Y.

max( X, Y, Y ) :- X < Y, !.
max( X, _, X ).

% Calcula Y = (X + 3) * 2:
sumar_3_y_duplicar( X, Y ) :- Y is (X+3) * 2.

% Factorial:
factorial(0, 1):- !.
factorial(N, F) :- N>0, N1 is N - 1, factorial(N1, F1), F is N * F1.

% Fibonacci:
fib( 1, 0 ):-!.
fib( 2, 1 ):-!.
fib( N, M ) :- N > 1, N1 is N - 1, N2 is N - 2, fib( N1, M1), fib( N2, M2), M is M1 + M2.

% Potencia:
potencia( 0, 0, 'No se puede calcular' ):- !.
potencia( X, 0, 1 ):- X =\= 0, !.
potencia( X, N, M ) :- N > 0, N1 is N - 1, potencia( X, N1, M1 ), M is X * M1.
~~~

### 6.1. `is` no es `=`

`Y is (X+3) * 2` **evalúa** la expresión aritmética del lado derecho y la unifica con `Y`. A diferencia de `=`, que solo intenta unificar sin evaluar, `is` obliga a que el lado derecho sea una expresión aritmética concreta (sin variables libres).

### 6.2. `maximo`/`mayor`/`max`: tres formas de resolver lo mismo

`maximo` no usa corte porque sus dos cláusulas tienen condiciones **mutuamente excluyentes** (`X ≥ Y` y `X < Y` nunca son ambas verdaderas): aunque Prolog dejara abierto un punto de elección, la segunda cláusula fallaría sola. `mayor` y `max` agregan `!` para **cerrar ese punto de elección de inmediato**, evitando que Prolog pierda tiempo intentando la alternativa que de todos modos iba a fallar. Es el mismo patrón que en `factorial`: un corte que solo mejora eficiencia (corte verde), no cambia qué se puede demostrar.

> [!note] El guion bajo `_` en `max( X, _, X )`
> `_` es una variable anónima: unifica con cualquier cosa, pero Prolog no se molesta en nombrarla ni en reportar su valor. Se usa cuando un argumento debe existir mientras se unifica, pero su valor no importa para el resto de la regla.

### 6.3. Recursión con caso base protegido por corte

`factorial`, `fib` y `potencia` comparten la misma forma: uno o más **casos base** con `!` (para que, una vez identificados, Prolog no siga buscando otra manera de resolverlos) y un **caso recursivo** que reduce el problema (`N1 is N - 1`) y confía en que la llamada recursiva ya lo resuelve. Es la misma idea de recursión que en las clases de `mc91` y Ackermann, ahora expresada como cláusulas lógicas en vez de sentencias `if/return`.

### 6.4. Entrada y salida

~~~prolog
lee_numero( X ) :- write( 'Introduce un número: '), nl, read( X ).

escr_cuadrado( X ) :- X2 is X*X,
                    write( 'El cuadrado de '),
                    write(X),
                    write( ' es '),
                    write(X2).

cuadrado :- lee_numero(X), escr_cuadrado(X).
~~~

`write/1` imprime un término, `nl` imprime un salto de línea y `read/1` lee un término de la entrada estándar. `cuadrado` **compone** dos predicados con `,`: primero pide un número y lo liga a `X`, luego usa esa misma `X` para calcular e imprimir su cuadrado.

---

## 7. Próximos temas (adelanto de las diapositivas)

Las láminas 168–170 ya anuncian lo que sigue en el curso, aunque todavía no se desarrolla con código propio en esta clase:

- **Listas en Prolog:** notación `[X|Xs]` (cabeza y cola), `[X,Y|Xs]`, `[]` (lista vacía) y `[X]` (un solo elemento).
- **Debug gráfico y en línea en SWI-Prolog.**
- **Aplicaciones:** dibujar una figura de un solo trazo sin levantar el lápiz (representación de conocimiento + operadores definidos por el programador), deducción lógica, el problema de la Zebra y derivadas simbólicas con Prolog.

---

## 8. Errores frecuentes

> [!warning] Confundir `,` de conjunción con `,` de lista de argumentos
> En `x :- a, b, c, d.` las comas separan **metas** (conjunción lógica). En `gusta( maria, helado )` las comas separan **argumentos** de un mismo predicado. Son usos distintos del mismo símbolo.

> [!warning] Espacio entre el predicado y el paréntesis
> `recibe ( X, beso )` truena; `recibe( X, beso )` funciona. Nunca debe haber espacio antes del paréntesis de apertura de una llamada a predicado.

> [!warning] Creer que una mayúscula inicial es una constante especial
> Cualquier identificador con mayúscula inicial (`Maria`, `Helado`, `X`, `N1`) es una **variable**. Las constantes (átomos) siempre empiezan con minúscula o van entre comillas.

> [!warning] Pensar que `\+ G` prueba que G es falso en general
> `\+ G` solo dice que el programa actual **no logra demostrar** `G`. Si `G` tiene variables libres, `\+ G` no las recorre ni las liga; solo indica si existe o no alguna forma de demostrar `G`.

> [!warning] Quitar un corte sin revisar qué backtracking dependía de él
> Si `factorial(0,1):-!.` pierde el corte, un programa que dependa de que `factorial` tenga **una sola** solución podría empezar a fallar de forma sutil al retroceder sobre él dentro de una conjunción más grande.

---

## 9. Comparación con la clase anterior

| | Resolución / SLD (8 de septiembre) | Hechos y ejecución concreta (10 de septiembre) |
|---|---|---|
| Nivel | Fundamento lógico: cláusulas, resolvente, refutación | Nivel de programa: sintaxis `.pl`, consola real |
| Unificación | UMG entre literales de dos cláusulas | Bindeos concretos (`X = maria`) mostrados por la consola |
| Alternativas | "El retroceso permite probar la otra regla" | `;` en consola, puntos de elección, corte `!` |
| Ejemplo | `r(X) :- t(X). r(X) :- q(X).` | `maximo`, `mayor`, `factorial`, `fib`, `potencia` |

---

## 10. Ejercicios de comprobación

1. Usando `Proposiciones.pl`, explica por qué `?- z.` no simplemente "falla": ¿qué mensaje adicional podría dar Prolog si `f`, `g` o `h` nunca se definieron en ningún lado del programa?
2. En el simulador, ejecuta `gusta(maria, Helado)` y cuenta cuántas soluciones da. ¿Por qué son las mismas tres que para `gusta(maria, X)`?
3. Reescribe `mayor/3` sin el corte. ¿Cambia el conjunto de respuestas para `?- mayor(3, 5, Z).`? ¿Cambia algo más?
4. ¿Qué imprime `?- potencia(2, 3, M).` paso a paso? Usa la plantilla de recursión de la sección 6.3.
5. ¿Por qué `read(X)` en `lee_numero` no es lo mismo que `X is 5`?

> [!check]- Respuestas breves
> 1. Prolog reportaría una advertencia de **predicado desconocido** (o simplemente fallaría silenciosamente según la configuración), porque `f`, `g` y `h` no tienen ningún hecho ni regla que los defina; no es que sean "falsos", es que no existen en el programa.
> 2. Da `Helado = helado`, `Helado = leer`, `Helado = cine`: `Helado` es una variable (empieza en mayúscula) exactamente igual que `X`; el nombre de la variable no afecta la unificación.
> 3. El conjunto de respuestas para esa consulta específica no cambia (las condiciones son excluyentes), pero sin el corte Prolog deja abierto un punto de elección inútil que se exploraría —y fallaría— si el programa pide otra solución con `;`.
> 4. `potencia(2,3,M)`: `N=3>0` → `N1=2`, `potencia(2,2,M1)` → (`N=2>0`→`N1=1`, `potencia(2,1,M1')` → (`N=1>0`→`N1=0`, `potencia(2,0,M1'')` = 1 por la segunda cláusula) → `M1' = 2*1 = 2`) → `M1 = 2*2 = 4`) → `M = 2*4 = 8`.
> 5. `read(X)` **unifica** `X` con lo que el usuario escriba en tiempo de ejecución (entrada externa); `X is 5` **evalúa** la expresión aritmética `5` y liga `X` a ese valor fijo dentro del programa. Uno depende de la entrada, el otro es determinista y fijo en el código.

---

## 11. Referencia diapositiva por diapositiva

| Diap. | Lámina | Contenido | Sección |
|---:|---:|---|---|
| 1 | 164 | Instalación: SWI-Prolog | §1 |
| 2 | 165 | Instalación: Visual Prolog | §1 |
| 3 | 166 | Instalación: GNU Prolog | §1 |
| 4 | 167 | Índice: proposiciones, unificación, programas en Prolog, corte, debug | §2–6 |
| 5 | 168 | Introducción a listas en Prolog | §7 |
| 6 | 169 | Aplicaciones: un trazo, deducción lógica | §7 |
| 7 | 170 | Zebra, derivadas simbólicas | §7 |

## Conceptos atómicos

- [[Backtracking en Prolog|Backtracking en Prolog]]
- [[Corte (cut) en Prolog|Corte (cut) en Prolog]]
- [[Negación como falla|Negación como falla]]

## Dudas para revisar

- [ ] ¿Cómo distingue SWI-Prolog un predicado indefinido de uno que simplemente falla (`existence_error` vs. `false`)?
- [ ] ¿Cuándo conviene usar `\+` en vez de reestructurar el programa para evitar la negación?
- [ ] ¿Qué forma tendrá `untrazo.pl` para el problema de dibujar una figura de un solo trazo? (adelantado en la lámina 169, sin código todavía).

## Resumen después de clase

Un programa Prolog concreto no es más que una lista de cláusulas de Horn escritas como hechos (`a.`) y reglas (`x :- a, b.`), tal como se formalizó la clase pasada. Al consultarlas, Prolog **unifica** la meta con la cabeza de cada cláusula candidata: átomo con átomo (coincide o no), variable con átomo (la variable se liga), o variable con variable. Cuando quedan varias cláusulas que pudieron haber servido, Prolog guarda **puntos de elección** y los recorre uno por uno cada vez que se pide otra solución con `;` — eso es backtracking. El corte `!` es la herramienta para decirle a Prolog "ya no explores otras alternativas desde aquí", y aparece sistemáticamente junto a los casos base de predicados recursivos (`factorial`, `fib`, `potencia`) para evitar retrocesos inútiles. Dos detalles de sintaxis marcan la diferencia entre un programa que corre y uno que truena: las mayúsculas siempre denotan variables, y nunca debe haber espacio entre un predicado y su paréntesis de apertura.

## Referencia

- [[Programación Avanzada Notas 9.pdf|Programación Avanzada Notas 9]], diapositivas 1–7 (láminas 164–170).
- Código fuente: `Proposiciones.pl`, `DaRegalo.pl`, `MariaGusta.pl`, `EjemplosProlog.pl` (carpeta `Primera Parte`).
- Capturas de consola: *Unificación y Sustitución.docx* — [[console-gusta-atomos.png|consultas con átomos]], [[console-gusta-variables.png|consultas con variables]], [[console-mayusculas-variables.png|mayúsculas como variables]], [[console-recibe-error-sintaxis.png|error de sintaxis]].
- Clase previa: [[2026-09-08 ProgAv - Resolucion y metas en Prolog|Resolución, reglas y metas en Prolog]].
