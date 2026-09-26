---
tipo: clase
materia: "[[Indice|Programación Avanzada]]"
fecha: 2026-08-18
unidad: Técnicas de solución de problemas
profesor: Gustavo Marquez Flores
estado: procesada
conceptos:
  - "[[Divide y vencerás|Divide y vencerás]]"
  - "[[QuickSort|QuickSort]]"
  - "[[Backtracking|Backtracking]]"
referencias:
  - "[[Programación Avanzada Notas 2.pdf|Programación Avanzada Notas 2]]"
  - "[[Algoritmo BackTracking y Divide-Venceras.pdf|Algoritmo BackTracking y Divide-Venceras]]"
  - "[[Qsort.PAS|Qsort.PAS]]"
tags:
  - clase
  - programacion-avanzada
  - divide-y-venceras
  - quicksort
  - backtracking
---

# Divide y vencerás, QuickSort y backtracking

![[Programación Avanzada Notas 2.pdf]]

## Pregunta central

¿Cómo permiten la descomposición recursiva y la exploración sistemática construir soluciones a problemas complejos, y cómo se materializan estas ideas en QuickSort?

## Mapa de la clase

Las dos técnicas estudiadas usan recursión, pero recorren estructuras distintas:

| Técnica | Estructura de la solución | Movimiento principal | Resultado típico |
|---|---|---|---|
| [[Divide y vencerás|Divide y vencerás]] | Subproblemas semejantes | dividir, resolver y combinar | una solución construida con soluciones parciales |
| [[Backtracking|Backtracking]] | Árbol de decisiones | elegir, avanzar, descartar y retroceder | una, todas o la mejor solución factible |

## Divide y vencerás

### Idea metodológica

Un problema $P$ puede tratarse con divide y vencerás cuando:

1. puede descomponerse en subproblemas $P_1,\ldots,P_k$;
2. los subproblemas son semejantes al original y de menor tamaño;
3. existe un **caso base** que se resuelve directamente;
4. las soluciones $S_1,\ldots,S_k$ pueden combinarse eficientemente para obtener la solución de $P$.

```text
resolver(P):
    si P es pequeño:
        devolver solucion_simple(P)
    dividir P en P1, ..., Pk
    para cada Pi:
        Si = resolver(Pi)
    devolver combinar(S1, ..., Sk)
```

La terminación depende de que cada llamada reduzca una medida bien fundada, por ejemplo el número de elementos. El costo suele expresarse mediante una recurrencia

$$
T(n)=\sum_{i=1}^{k}T(n_i)+D(n)+C(n),
$$

donde $D(n)$ es el costo de dividir y $C(n)$ el de combinar. Si hay $a$ subproblemas de tamaño aproximado $n/b$, se obtiene $T(n)=aT(n/b)+f(n)$.

> [!important]
> La recursión es un mecanismo de implementación; divide y vencerás es una estrategia de diseño. Un algoritmo recursivo no necesariamente divide el problema en subproblemas que luego combina.

### Ejemplos

- [[QuickSort|QuickSort]] particiona alrededor de un pivote y ordena recursivamente las regiones resultantes.
- La búsqueda binaria conserva solo la mitad que puede contener el dato; su combinación es trivial.
- La multiplicación de enteros grandes divide cada operando en una mitad alta y otra baja.

## Ejemplo desarrollado: QuickSort en Pascal

El programa `Qsort.PAS` genera 1000 enteros aleatorios y los ordena **in-place**. Para un intervalo inclusivo $[l,r]$, selecciona como pivote

$$
x=A\left[\left\lfloor\frac{l+r}{2}\right\rfloor\right].
$$

Después mantiene dos índices: $i$ avanza hasta encontrar un valor que no sea menor que el pivote y $j$ retrocede hasta encontrar uno que no sea mayor. Si $i\le j$, intercambia $A[i]$ y $A[j]$ y continúa. Cuando los índices se cruzan, quedan dos regiones pendientes: $[l,j]$ y $[i,r]$.

```pascal
i := l; j := r; x := a[(l+r) div 2];
repeat
  while a[i] < x do i := i + 1;
  while x < a[j] do j := j - 1;
  if i <= j then begin
    y := a[i]; a[i] := a[j]; a[j] := y;
    i := i + 1; j := j - 1;
  end;
until i > j;
if l < j then Sort(l, j);
if i < r then Sort(i, r);
```

### Invariante e interpretación

Durante la partición, los elementos ya recorridos a la izquierda no exceden al pivote y los ya recorridos a la derecha no son menores que él. El intercambio corrige un par situado en el lado equivocado. Las llamadas finales reciben intervalos estrictamente menores, lo que garantiza el progreso incluso cuando hay valores repetidos.

La complejidad depende del balance de las particiones:

$$
T(n)=T(k)+T(n-k-1)+\Theta(n).
$$

- particiones aproximadamente equilibradas: $\Theta(n\log n)$;
- particiones extremadamente desbalanceadas: $\Theta(n^2)$;
- memoria auxiliar: depende de la profundidad de la recursión, típicamente $O(\log n)$ y $O(n)$ en el peor caso.

El archivo desactiva las comprobaciones de rango y desbordamiento de pila (`{$R-,S-}`) para priorizar velocidad. Esto no mejora el algoritmo y elimina protecciones útiles durante el desarrollo.

### Comparación con la versión funcional

La versión Haskell de las diapositivas expresa la misma descomposición con listas nuevas:

```haskell
ordenaQS (x:xs) = ordenaQS menores ++ [x] ++ ordenaQS mayores
  where
    menores = [e | e <- xs, e < x]
    mayores = [e | e <- xs, e >= x]
ordenaQS [] = []
```

En Pascal se modifica un arreglo mediante índices e intercambios; en Haskell se describen listas menores y mayores sin mutar la entrada. Comparten la idea algorítmica, pero no el mismo comportamiento de memoria ni la misma estrategia exacta de partición.

## Búsqueda binaria: precisión de los límites

Para buscar en un intervalo inclusivo $[izq,der]$, el caso vacío correcto es $izq>der$. Si $m=\lfloor(izq+der)/2\rfloor$:

- si $X=A[m]$, se devuelve $m$;
- si $X<A[m]$, se busca en $[izq,m-1]$;
- si $X>A[m]$, se busca en $[m+1,der]$.

Reducir los límites en una unidad evita repetir el pivote y asegura la terminación. El algoritmo requiere que el arreglo esté ordenado y cuesta $O(\log n)$ comparaciones.

## Multiplicación de enteros grandes

Sea $s=\lfloor n/2\rfloor$ y $B=10^s$. Se descomponen

$$
u=Bw+x,\qquad v=By+z,
$$

y, por distributividad,

$$
uv=B^2wy+B(wz+xy)+xz.
$$

Las cuatro multiplicaciones $wy,wz,xy,xz$ se resuelven recursivamente hasta llegar a operandos pequeños. Este esquema ilustra correctamente divide y vencerás, aunque con cuatro subproblemas de mitad de tamaño conserva complejidad $\Theta(n^2)$ bajo el modelo elemental. El algoritmo de Karatsuba reduce las multiplicaciones recursivas de cuatro a tres y obtiene $\Theta(n^{\log_2 3})$.

## Backtracking

[[Backtracking|Backtracking]] construye una solución por etapas. En cada etapa genera opciones, acepta solo las que mantienen una solución parcial válida y profundiza. Si una rama ya no puede producir una solución, deshace la última decisión y prueba la siguiente.

```text
buscar(estado):
    si estado es solución:
        registrar o devolver estado
    para cada opción aplicable:
        aplicar(opción)
        si el estado parcial es prometedor:
            buscar(estado)
        deshacer(opción)
```

El espacio de búsqueda puede representarse como un árbol: cada nodo es una solución parcial y cada arista una decisión. El recorrido es típicamente en profundidad.

### Tres objetivos posibles

- **Encontrar una solución:** detenerse en la primera hoja válida.
- **Encontrar todas:** registrar cada solución y continuar explorando.
- **Encontrar la mejor:** conservar la mejor solución completa; si además se descartan ramas mediante cotas de calidad, el método se acerca a *branch and bound*.

### Condiciones y costo

Se necesita poder generar opciones, comprobar si una extensión es aceptable, reconocer una solución completa y deshacer decisiones. La poda de estados parciales inviables es lo que lo distingue de enumerar ciegamente todas las combinaciones. Sin una poda efectiva, con factor de ramificación $b$ y profundidad $d$, puede explorar $O(b^d)$ nodos.

## Errores conceptuales que conviene evitar

- **Divide y vencerás no es backtracking:** el primero combina subsoluciones necesarias; el segundo abandona alternativas inviables y prueba otras.
- **Caso base no es caso vacío:** el primero da una solución directa; el segundo indica que no quedan candidatos.
- **Elegir un pivote central no garantiza particiones equilibradas:** el valor situado en el centro del arreglo puede ser extremo.
- **QuickSort no siempre cuesta $O(n\log n)$:** esa es su complejidad esperada o típica con particiones razonables, no su peor caso.
- **Backtracking no tiene que enumerar todo:** puede detenerse al hallar una solución y podar ramas que ya son inviables.

## Preguntas de recuperación activa

1. ¿Cuáles son las tres fases de divide y vencerás y qué condición asegura que termine?
2. ¿Qué representa el pivote en QuickSort y qué queda garantizado cuando $i>j$?
3. ¿Por qué la búsqueda binaria debe llamar con $m-1$ o $m+1$?
4. ¿Qué cambia entre buscar una, todas o la mejor solución con backtracking?
5. ¿Qué información debe conservarse para deshacer una decisión?

## Conceptos atómicos completados

- [[Divide y vencerás|Divide y vencerás]]
- [[QuickSort|QuickSort]]
- [[Backtracking|Backtracking]]

## Referencias mencionadas

- [[Programación Avanzada Notas 2.pdf|Programación Avanzada Notas 2]], diapositivas 22-39.
- [[Algoritmo BackTracking y Divide-Venceras.pdf|Algoritmo BackTracking y Divide-Venceras]], páginas 1-2.
- [[Qsort.PAS|Qsort.PAS]], implementación de Borland International.

## Resumen después de clase

Divide y vencerás resuelve un problema al separarlo en subproblemas menores, resolverlos recursivamente y combinar sus resultados. QuickSort aplica la estrategia mediante una partición alrededor de un pivote; su rendimiento depende de qué tan balanceadas queden las regiones. La búsqueda binaria y la multiplicación de enteros grandes muestran otras formas de reducir el problema, con combinaciones triviales o algebraicas. Backtracking, en contraste, recorre un árbol de decisiones y deshace elecciones cuando una solución parcial deja de ser viable, lo que permite buscar una, todas o la mejor solución.
