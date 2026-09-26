---
tipo: clase
materia: "[[01_Materias/Algoritmos/Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: 2026-08-18
unidad: Emparejamiento estable
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[03_Conceptos/Emparejamiento estable|Emparejamiento estable]]"
  - "[[03_Conceptos/Emparejamiento perfecto|Emparejamiento perfecto]]"
  - "[[03_Conceptos/Par inestable|Par inestable]]"
  - "[[03_Conceptos/Algoritmo de Gale-Shapley|Algoritmo de Gale-Shapley]]"
  - "[[03_Conceptos/Aceptación diferida|Aceptación diferida]]"
  - "[[03_Conceptos/Socio válido|Socio válido]]"
  - "[[03_Conceptos/Óptimo para hospitales|Óptimo para hospitales]]"
  - "[[03_Conceptos/Pesimista para estudiantes|Pesimista para estudiantes]]"
  - "[[03_Conceptos/Emparejamiento con capacidades|Emparejamiento con capacidades]]"
referencias:
  - 01StableMatching.pdf, diapositivas 1–31
  - Kleinberg y Tardos, *Algorithm Design*, sección 1.1
tags: [clase, algoritmos]
---

## Pregunta central

¿Cómo asignar $n$ estudiantes a $n$ hospitales respetando las preferencias de ambos lados, de modo que ninguna pareja tenga incentivos para abandonar su asignación y pactar por su cuenta?

## Apuntes rápidos

- El problema ya no es ordenar una estructura, sino producir una asignación que sea [[03_Conceptos/Emparejamiento estable|estable]].
- El modelo inicial tiene $n$ hospitales, $n$ estudiantes, una plaza por hospital y preferencias estrictas y completas.
- El [[03_Conceptos/Algoritmo de Gale-Shapley|algoritmo de Gale–Shapley]] siempre termina y devuelve un emparejamiento perfecto y estable bajo esos supuestos.
- Si proponen los hospitales, la solución favorece a los hospitales entre todas las soluciones estables; si proponen los estudiantes, se invierte ese efecto.

## Desarrollo incremental de las diapositivas

### 1. Del ejemplo real al modelo (diapositivas 3–4)

El ejemplo es asignar egresados de medicina a hospitales. Hay dos conjuntos disjuntos del mismo tamaño:

$$H=\{h_1,\ldots,h_n\},\qquad S=\{s_1,\ldots,s_n\}.$$ 

Cada hospital ordena a los estudiantes de más a menos preferido; cada estudiante ordena los hospitales. Las listas son la **entrada**, no la solución. En la instancia de las diapositivas, Atlanta prefiere $Xavier \succ Yolanda \succ Zeus$, mientras Xavier prefiere $Boston \succ Atlanta \succ Chicago$.

### 2. Emparejamiento perfecto y estabilidad (diapositivas 5–8)

Un [[03_Conceptos/Emparejamiento perfecto|emparejamiento]] $M$ es un conjunto de pares $(h,s)$ en que ningún hospital ni estudiante aparece en más de un par. Es **perfecto** cuando usa a las $n$ personas de cada lado, así que $|M|=n$.

Para un par $(h,s)\notin M$, sea $M(h)$ el estudiante asignado a $h$ y $M(s)$ el hospital asignado a $s$. El par es [[03_Conceptos/Par inestable|inestable]] si:

$$s \succ_h M(h)\quad\text{y}\quad h \succ_s M(s).$$

Es decir, ambos prefieren al otro sobre su pareja actual; podrían mejorar mediante un acuerdo bilateral, por lo que el resultado no se sostiene. Un emparejamiento estable es uno perfecto sin pares inestables.

En $M=\{A\text{–}Z,B\text{–}Y,C\text{–}X\}$, $A\text{–}Y$ es inestable: Atlanta prefiere a Yolanda sobre Zeus y Yolanda prefiere Atlanta sobre Boston. En el ejercicio $\{A\text{–}X,B\text{–}Z,C\text{–}Y\}$, la respuesta es $B\text{–}X$.

### 3. Por qué el problema no es trivial (diapositiva 9)

Las preferencias no garantizan por sí solas que exista una asignación estable. En el **problema de compañeros de cuarto**, hay un único conjunto de $2n$ personas y cada una ordena a las demás; puede ocurrir que *todo* emparejamiento perfecto tenga un par inestable. La división bipartita hospitales–estudiantes es una hipótesis esencial para la garantía que veremos.

### 4. Gale–Shapley: aceptación diferida (diapositiva 11)

Los hospitales proponen en orden de preferencia y los estudiantes conservan provisionalmente la mejor oferta vista. Como una aceptación puede cambiar después, se llama [[03_Conceptos/Aceptación diferida|aceptación diferida]].

```text
M ← ∅
mientras exista un hospital h sin pareja que aún no haya propuesto a todos:
    s ← primera estudiante de la lista de h a quien h no ha propuesto
    si s no tiene pareja: agregar (h, s) a M
    si s tiene pareja con h' y prefiere h a h': reemplazar (h', s) por (h, s)
    en otro caso: s rechaza a h
devolver M
```

Lectura paso a paso:

1. Solo propone un hospital libre; por ello no puede tener dos compromisos.
2. Propone a la mejor opción que aún no lo rechazó.
3. Una estudiante libre acepta temporalmente.
4. Una estudiante comprometida compara: conserva al mejor hospital y rechaza el otro.
5. El rechazado continúa con la siguiente persona de su lista y nunca repite propuesta.

### 5. Ejecución sobre las listas de la clase

| Paso | Propuesta y decisión | Parejas provisionales |
|---:|---|---|
| 1 | $A\to X$; $X$ acepta | $A$–$X$ |
| 2 | $B\to Y$; $Y$ acepta | $A$–$X$, $B$–$Y$ |
| 3 | $C\to X$; $X$ prefiere $A$ y rechaza | $A$–$X$, $B$–$Y$ |
| 4 | $C\to Y$; $Y$ prefiere $B$ y rechaza | $A$–$X$, $B$–$Y$ |
| 5 | $C\to Z$; $Z$ acepta | $A$–$X$, $B$–$Y$, $C$–$Z$ |

El resultado es estable. Invariante útil: una estudiante que recibió una propuesta nunca vuelve a estar libre; solo cambia por una opción mejor. Los hospitales, en cambio, pueden bajar por sus listas tras ser rechazados.

### 6. Terminación (diapositiva 12)

Cada vuelta produce una propuesta nueva $(h,s)$. Hay solo $n^2$ pares posibles y ningún hospital repite propuesta, así que el algoritmo termina tras a lo sumo $n^2$ propuestas. Con listas e índices almacenados adecuadamente, el tiempo es $O(n^2)$ y el espacio adicional $O(n)$, sin contar las listas de entrada.

### 7. Por qué la salida es perfecta (diapositiva 13)

Primero, $M$ siempre es un emparejamiento: un hospital propone solo libre y una estudiante conserva como máximo un hospital. Supongamos que al terminar algún hospital $h$ quedó libre. Como ambos conjuntos tienen igual tamaño, también habría una estudiante $s$ libre. Una estudiante libre nunca recibió propuesta: al recibir una habría aceptado y después solo podría cambiar a una opción mejor. Pero $h$, al terminar libre, propuso a toda su lista, incluida $s$. Contradicción. Todos quedan emparejados.

### 8. Por qué la salida es estable (diapositiva 14)

Sea $M^*$ la salida y un par ausente $(h,s)$.

- Si $h$ nunca propuso a $s$, entonces su pareja final aparece antes que $s$ en su lista; $h$ no prefiere a $s$.
- Si $h$ propuso a $s$, ella lo rechazó entonces o lo reemplazó después. Como las estudiantes solo mejoran su pareja provisional, $s$ prefiere $M^*(s)$ a $h$.

En ambos casos falla una condición del par inestable. Así, $M^*$ es estable. Esto, junto con terminación y perfección, prueba el teorema de Gale–Shapley.

### 9. Múltiples soluciones estables y socios válidos (diapositivas 16–20)

Una instancia puede tener varios resultados estables. En el ejemplo, $\{A\text{–}X,B\text{–}Y,C\text{–}Z\}$ y $\{A\text{–}Y,B\text{–}X,C\text{–}Z\}$ son estables. Un [[03_Conceptos/Socio válido|socio válido]] es alguien con quien aparece en al menos un emparejamiento estable. Por ejemplo, $X$ y $Y$ son socios válidos de $A$ y $B$, pero $Z$ es el único socio válido de $C$.

La pregunta deja de ser solo «¿existe solución?» y pasa a ser «¿qué solución estable devuelve el mecanismo y a quién beneficia?».

### 10. Optimalidad para quien propone (diapositivas 21–24)

Cuando proponen hospitales, Gale–Shapley devuelve el [[03_Conceptos/Óptimo para hospitales|emparejamiento óptimo para hospitales]]: cada hospital recibe su mejor socio válido. El argumento formal toma la primera vez que un socio válido rechaza a un hospital; ese rechazo permite construir un par inestable en el supuesto emparejamiento estable donde eran pareja, contradicción.

La contraparte es que la salida es [[03_Conceptos/Pesimista para estudiantes|pesimista para estudiantes]]: cada estudiante recibe su peor socio válido. «Peor» es solo entre resultados estables; no significa que la asignación sea incorrecta. El lado que propone determina el sesgo: si proponen estudiantes, ellas obtienen su mejor socio válido. Con hospitales proponentes, informar preferencias reales es estrategia dominante para hospitales; para estudiantes no lo es en general.

### 11. Extensiones y límites (diapositiva 26)

El modelo admite participantes inaceptables, hospitales con varias plazas y números desiguales. Un par aceptable bloquea si el estudiante está libre o prefiere ese hospital y, a la vez, el hospital tiene plaza libre o prefiere al estudiante sobre alguien que ya tiene. La generalización hace que cada hospital conserve provisionalmente sus mejores candidatos hasta su capacidad.

Restricciones adicionales —por ejemplo, parejas que quieren coordinar dos plazas— pueden eliminar la garantía de existencia de una solución estable.

### 12. Contexto y aplicaciones (diapositivas 27–31)

- El National Resident Matching Program centralizó residencias médicas para evitar que las ofertas se adelantaran cada vez más.
- Shapley y Roth recibieron el Nobel de Economía de 2012 por aportaciones relacionadas con mercados de emparejamiento.
- Admisiones escolares y universitarias usan la extensión con capacidades.
- Variantes asignan usuarios a servidores de una CDN según latencia, pérdida de paquetes, costo y carga.

## Resultados que conviene saber demostrar

1. **Terminación:** no se repite una propuesta; hay como máximo $n^2$.
2. **Emparejamiento perfecto:** una estudiante comprometida nunca queda libre; un hospital libre final llevaría a contradicción.
3. **Estabilidad:** todo par no asignado es descartado porque uno de sus dos integrantes prefiere su pareja final.
4. **Sesgo:** el lado proponente obtiene su mejor socio entre los socios válidos.

## Dudas y precisiones para estudiar

- [ ] Simular la misma instancia eligiendo hospitales libres en distinto orden.
- [ ] Reconstruir con detalle la prueba de la «primera rejection» de un socio válido.
- [ ] Revisar qué cambia con empates en preferencias; aquí los rankings son estrictos.
- [ ] Comparar las versiones hospital-proponente y estudiante-proponente en una instancia con varias soluciones estables.

## Conceptos para extraer

- [[03_Conceptos/Emparejamiento estable|Emparejamiento estable]]
- [[03_Conceptos/Emparejamiento perfecto|Emparejamiento perfecto]]
- [[03_Conceptos/Par inestable|Par inestable]]
- [[03_Conceptos/Algoritmo de Gale-Shapley|Algoritmo de Gale–Shapley]]
- [[03_Conceptos/Aceptación diferida|Aceptación diferida]]
- [[03_Conceptos/Socio válido|Socio válido]]
- [[03_Conceptos/Óptimo para hospitales|Óptimo para hospitales]]
- [[03_Conceptos/Pesimista para estudiantes|Pesimista para estudiantes]]
- [[03_Conceptos/Emparejamiento con capacidades|Emparejamiento con capacidades]]

## Resumen después de clase

El problema de emparejamiento estable busca una asignación perfecta sin pares que prefieran pactar entre sí. Gale–Shapley usa propuestas y aceptaciones provisionales; termina en $O(n^2)$ propuestas y su salida es perfecta y estable. El lado que propone obtiene su mejor resultado entre las soluciones estables, por lo que el mecanismo importa tanto como el algoritmo. La clase conecta con hot cakes porque otra vez se exige una prueba explícita de terminación y validez, ahora con invariantes sobre propuestas y parejas provisionales.

## Referencias mencionadas

- Kevin Wayne, *Stable Matching*, diapositivas 1–31 (basadas en Kleinberg y Tardos).
- Jon Kleinberg y Éva Tardos, *Algorithm Design*, sección 1.1.
