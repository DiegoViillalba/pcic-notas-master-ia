---
tipo: clase
materia: "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: "2026-10-27"
unidad: Divide y vencerás
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - Divide y vencerás
  - Búsqueda binaria recursiva
  - Árbol de recurrencia
  - Conteo de inversiones
  - Par de puntos más cercano
referencias:
  - "05DivideAndConquerI.pdf, diapositivas 20–25 y 64–70 (material proporcionado para esta nota)"
tags:
  - clase
  - algoritmos
  - divide-y-venceras
  - recurrencias
---

# Clase 18 · Divide y vencerás I

## Pregunta central

¿Cómo cambia el tiempo de ejecución cuando cada llamada recursiva resuelve **un** subproblema de tamaño $n/2$ frente a **dos**, y cómo aprovechamos la división para contar inversiones?

> [!summary] Lo visto en clase
> Comenzamos con búsqueda binaria recursiva y probamos su corrección y su costo $O(\log n)$. Después estudiamos el árbol de recurrencia de un algoritmo con dos subproblemas y trabajo lineal al combinar, que da $O(n\log n)$. Aplicamos esta idea al conteo de inversiones; al final quedó planteado el problema del par de puntos más cercano. Las fotos del pizarrón permanecen junto a cada explicación.

## 1. Búsqueda binaria recursiva

La búsqueda binaria recibe un arreglo **ordenado** $A$, una clave $x$ y el intervalo de índices $[i,j]$. Compara $x$ con el elemento central y continúa solo en la mitad donde $x$ todavía podría estar.

![[Screenshot 2026-10-27 at 11.46.49 a.m..png]]

La foto muestra BBR($i,j,A,x$). Una versión completa, que también cubre el caso en que $x$ no aparece, es:

~~~text
BBR(i, j, A, x):
    si i > j: devolver -1
    mid ← ⌊(i + j) / 2⌋
    si x = A[mid]: devolver mid
    si x < A[mid]: devolver BBR(i, mid - 1, A, x)
    devolver BBR(mid + 1, j, A, x)
~~~

**Corrección y terminación.** El invariante es: si $x$ aparece en el intervalo original, toda posición donde aún podría encontrarse queda dentro de $A[i\ldots j]$. Si $x<A[mid]$, el orden descarta $mid$ y toda la mitad derecha; si $x>A[mid]$, descarta la izquierda. Si $i>j$, el intervalo está vacío y devolver $-1$ es correcto. En cada llamada recursiva el intervalo se acorta estrictamente, por lo que el algoritmo termina. La foto siguiente desarrolla sobre todo la **corrección por inducción en el tamaño del intervalo**; el argumento de terminación es este descenso de tamaño.

![[Screenshot 2026-10-27 at 12.00.41 p.m..png]]

> [!note] Detalle de la foto
> Allí se usa $i=j$ como caso base. Si se excluye el elemento central al llamar con $mid-1$ o $mid+1$, puede aparecer un intervalo vacío; por eso la condición $i>j$ debe tratarse explícitamente.

### Tiempo de ejecución

Solo se hace **una** llamada recursiva. Con costo constante $c$ por nivel, para $n\geq2$ se cumple $T(n)\leq T(\lfloor n/2\rfloor)+c$, con $T(1)=O(1)$. Al desplegar la recurrencia aparecen tamaños aproximados $n,n/2,n/4,\ldots,1$: hay $O(\log n)$ niveles, así que $T(n)=O(\log n)$.

![[Screenshot 2026-10-27 at 12.02.32 p.m..png]]

Las dos fotos siguientes prueban la misma cota **por inducción** para $n$ potencia de $2$, tomando $T(2)\leq c$:

![[Screenshot 2026-10-27 at 12.09.38 p.m..png]]

![[Screenshot 2026-10-27 at 12.09.49 p.m..png]]

Si $n>2$ y la hipótesis inductiva vale para $n/2$, entonces

$$
T(n)\leq T(n/2)+c\leq c\log_2(n/2)+c=c\log_2 n.
$$

Para tamaños que no son potencias de $2$, los redondeos cambian constantes, pero no la cota asintótica.

## 2. Dos llamadas recursivas: trabajo por nivel

En un algoritmo como *mergesort*, se resuelven **dos** mitades y se invierte $O(n)$ en combinarlas. La recurrencia del pizarrón es $T(n)\leq 2T(n/2)+cn$, con caso base constante.

![[Screenshot 2026-10-27 at 12.32.07 p.m..png]]

En el nivel $k$ hay $2^k$ subproblemas de tamaño $n/2^k$. Cada uno cuesta a lo sumo $c(n/2^k)$ fuera de la recursión; por tanto, **todo el nivel cuesta $cn$**. Hay $\log_2 n$ niveles hasta llegar a tamaño $1$, más $O(n)$ por las hojas. En consecuencia, $T(n)=O(n\log n)$.

![[Screenshot 2026-10-27 at 12.32.28 p.m..png]]

La cota también se verifica por inducción para potencias de $2$, con base $n=2$ y $C$ suficientemente grande. Si $T(n/2)\leq C(n/2)\log_2(n/2)$ y $C\geq c$, entonces

$$
T(n)\leq 2C\frac n2\log_2\!\frac n2+cn
=Cn\log_2 n-(C-c)n\leq Cn\log_2 n.
$$

**Comparación visual:** al cambiar entre una y dos llamadas, observa el costo total de cada nivel. En búsqueda binaria se suma una constante por nivel; con dos mitades se suma un costo proporcional a $n$ por nivel.

<iframe src="recurrencias-divide-y-venceras.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## 3. Conteo de inversiones

Una **inversión** es un par de posiciones $p<q$ tal que $A[p]>A[q]$. Por ejemplo, $[1,3,4,2,5]$ tiene dos: $(3,2)$ y $(4,2)$. Examinar todos los pares cuesta $\Theta(n^2)$.

Dividimos el arreglo en $A$ (mitad izquierda) y $B$ (derecha). Las inversiones quedan en tres grupos: dentro de $A$, dentro de $B$ y **cruzadas** (un elemento de $A$ mayor que uno de $B$). Las dos primeras se cuentan recursivamente.

![[Screenshot 2026-10-27 at 12.48.33 p.m..png]]

**Método preliminar del pizarrón.** Si cada llamada devuelve también su mitad ordenada, para cada $b\in B$ podemos usar búsqueda binaria en $A$ para hallar cuántos elementos de $A$ son mayores que $b$. Hay $O(n)$ elementos y cada búsqueda cuesta $O(\log n)$: combinar cuesta $O(n\log n)$. De ahí sale la recurrencia anotada en la foto,

$$
T(n)\leq 2T(n/2)+O(n\log n)=O(n\log^2 n).
$$

**Resumen de la mejora que se saltó en clase.** En lugar de buscar por separado cada $b$, se recorren simultáneamente las dos mitades ordenadas durante la mezcla. Si el siguiente elemento de $A$ es mayor que el siguiente de $B$, este último forma una inversión con **todos los elementos restantes de $A$**; se suma esa cantidad de una vez. Si son iguales, no se cuenta inversión. La mezcla y el conteo cruzado cuestan $O(n)$, por lo que la recurrencia pasa a $2T(n/2)+O(n)=O(n\log n)$. La función devuelve tanto la lista ordenada como el número total de inversiones.

## 4. Inicio del siguiente problema: par de puntos más cercano

Al final se planteó encontrar, entre $n$ puntos del plano, el par con menor distancia euclidiana. Comparar todos los pares cuesta $\Theta(n^2)$. La idea inicial de divide y vencerás es separar los puntos en dos mitades según su coordenada $x$ y resolver ambas recursivamente. Queda para la continuación el paso delicado: comprobar eficientemente si un par con un punto a cada lado es todavía más cercano.

## Resumen después de clase

La búsqueda binaria ilustra una recurrencia con una sola rama y profundidad logarítmica. Con dos ramas y trabajo lineal al combinar, cada nivel cuesta $O(n)$ y el total es $O(n\log n)$. En inversiones, contar los pares cruzados con búsquedas binarias da una primera solución $O(n\log^2 n)$; contarlos durante la mezcla reduce el tiempo a $O(n\log n)$. El par de puntos más cercano plantea otra aplicación en la que la dificultad está en combinar las respuestas de las dos mitades.

## Referencia

- Kevin Wayne, *5. Divide and Conquer I* (05DivideAndConquerI.pdf), diapositivas 20–25 (inversiones) y 64–70 (planteamiento del par más cercano). Material proporcionado para completar el apunte; las fotos documentan lo trabajado en clase.
