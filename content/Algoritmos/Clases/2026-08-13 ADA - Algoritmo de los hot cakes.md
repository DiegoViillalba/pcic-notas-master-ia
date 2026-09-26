---
tipo: clase
materia: "[[01_Materias/Algoritmos/Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
fecha: 2026-08-13
unidad: Análisis de corrección mediante invariantes
profesor: Armando Castañeda Rojano
estado: procesada
conceptos:
  - "[[03_Conceptos/Ordenamiento de hot cakes|Ordenamiento de hot cakes]]"
  - "[[03_Conceptos/Volteo de prefijo|Volteo de prefijo]]"
  - "[[03_Conceptos/Invariante de ciclo|Invariante de ciclo]]"
  - "[[03_Conceptos/Análisis de mejor y peor caso|Análisis de mejor y peor caso]]"
  - "[[03_Conceptos/Terminación de un algoritmo|Terminación de un algoritmo]]"
  - "[[03_Conceptos/Validez de un algoritmo|Validez de un algoritmo]]"
  - "[[03_Conceptos/Complejidad temporal|Complejidad temporal]]"
referencias:
  - El Algoritmo de los Hot Cakes, diapositivas 1–11
tags:
  - clase
  - algoritmos
---

## Pregunta central

¿Cómo demostrar que un algoritmo basado únicamente en voltear la parte superior de una pila ordena todos los hot cakes y termina?

## Apuntes rápidos

- La entrada es una pila de hot cakes de tamaños distintos; la meta es dejar el más grande abajo y el más pequeño arriba.
- La única operación permitida es introducir una pala a cierta profundidad y efectuar un [[03_Conceptos/Volteo de prefijo|volteo de prefijo]].
- El [[03_Conceptos/Ordenamiento de hot cakes|algoritmo de los hot cakes]] coloca en cada iteración al menos un hot cake adicional en la parte ya ordenada.
- El análisis separa dos preguntas: [[03_Conceptos/Terminación de un algoritmo|¿termina?]] y [[03_Conceptos/Validez de un algoritmo|¿produce la pila ordenada?]].
- La afirmación de progreso se expresa mediante un [[03_Conceptos/Invariante de ciclo|invariante]]: si al inicio hay $h$ hot cakes colocados correctamente, al final habrá por lo menos $h+1$.

## Definiciones y resultados

### Modelo del problema

Representamos la pila de arriba hacia abajo como

$$
A=(a_1,a_2,\ldots,a_n),
$$

donde el objetivo es $a_1<a_2<\cdots<a_n$. Un hot cake se considera ya colocado cuando pertenece al bloque ordenado que se está fijando desde el fondo; esta interpretación evita confundir una coincidencia aislada de posición con la parte que el algoritmo ya no volverá a modificar.

### Operación permitida

Para $1\leq k\leq n$, voltear en la posición $k$ invierte los primeros $k$ elementos:

$$
F_k(a_1,\ldots,a_k,a_{k+1},\ldots,a_n)
=(a_k,\ldots,a_1,a_{k+1},\ldots,a_n).
$$

### Algoritmo HotCakes

```
Mientras algún hot cake esté fuera del bloque ordenado:
    1. Busca el hot cake más grande aún no colocado.
       Mete la pala debajo de él y voltea para llevarlo arriba.
    2. Busca el hot cake más pequeño del bloque ya colocado.
       Voltea solo la parte que está arriba de él.
       Si el bloque está vacío, voltea la pila completa.
    3. Repite.
Entrega la pila.
```

El primer volteo lleva arriba al mayor hot cake pendiente. El segundo lo mueve al fondo de la parte todavía desordenada, justo encima del bloque que ya estaba colocado, sin alterar ese bloque.

![[Pasted image 20260817123014.png]]

### Implementación en python
```python
import numpy as np

a = np.array([2, 4, 1, 3])

def voltear(a, k):
    return a[:k+1][::-1]

pointer = len(a)

while pointer > 1:
    biggest = a[0]
    biggest_index = 0

    # 1. Buscar el valor máximo dentro de la porción actual
    for i in range(pointer):
        if a[i] > biggest:
            biggest = a[i]
            biggest_index = i

    # 2. Giro 1: Llevar el máximo al inicio (índice 0)
    a[:biggest_index + 1] = voltear(a, biggest_index)

    # 3. Giro 2: Llevar el máximo a su posición final en la sub-lista
    a[:pointer] = voltear(a, pointer - 1)

    # 4. Reducir el tamaño de búsqueda
    pointer -= 1

print("Arreglo ordenado:", a)
	
	

```


### Invariante y Progreso en Pancake Sort

* **Invariante (Sufijo ordenado):** Al inicio de cada iteración $t$, los últimos $h_t$ elementos forman un bloque fijo al fondo de la pila. Este sufijo ya está ordenado de menor a mayor y contiene los elementos más grandes del arreglo en sus posiciones definitivas.
* **Mecanismo de los dos volteos:** Operan exclusivamente sobre la porción superior no ordenada (los primeros $n - h_t$ elementos) sin alterar el sufijo ya fijado:
  1. **Primer volteo:** Lleva el máximo relativo al tope (índice $0$).
  2. **Segundo volteo:** Lo traslada a la base de la sección no ordenada, integrándolo inmediatamente al bloque fijado.
* **Condición de progreso ($h_{t+1} \geq h_t + 1$):** Cada iteración incrementa el tamaño del bloque ordenado en al menos un elemento, lo que garantiza formalmente que el algoritmo converge y termina en un máximo de $n - 1$ iteraciones.


### Terminación y validez

- **Terminación:** $h$ aumenta al menos en uno por iteración y está acotado por el número finito $n$ de hot cakes. Por ello el ciclo no puede continuar indefinidamente.
- **Validez:** el ciclo se detiene solo cuando no queda ningún hot cake fuera del bloque ordenado; en ese momento la pila completa cumple el orden objetivo.
- **Cota inmediata:** hay $O(n)$ iteraciones y a lo sumo dos usos de la pala por iteración. La cota temporal exacta depende de si se cuentan solo los volteos o también el costo de buscar y representar cada volteo.

## Ejemplo

Para la pila $[3,1,4,2]$, escrita de arriba hacia abajo:

```text
[3,1,4,2]  --voltear hasta 4-->  [4,1,3,2]
[4,1,3,2]  --voltear todo----->  [2,3,1,4]
[2,3,1,4]  --voltear hasta 3-->  [3,2,1,4]
[3,2,1,4]  --voltear sobre 4-->  [1,2,3,4]
```

Tras la primera iteración, el $4$ queda fijado al fondo. La segunda iteración conserva ese sufijo y deja ordenada toda la pila.

## Preguntas resueltas

### Número de usos de la pala

El conteo depende de una convención que la presentación deja abierta: si el hot cake buscado ya está arriba, introducir la pala debajo de él produce el volteo trivial $F_1$, que no cambia la pila.

Si **no se cuenta** $F_1$ y se omiten los volteos innecesarios, una iteración sobre una región de longitud $m$ utiliza:

- cero volteos si el mayor elemento pendiente ya ocupa la posición $m$;
- un volteo si está arriba, pero todavía debe enviarse a la posición $m$;
- dos volteos si está en una posición intermedia.

Con esta convención:

- El mínimo es **cero** para una entrada ya ordenada.
- Entre las entradas desordenadas, el mínimo es **un** volteo. Lo alcanzan las pilas que se ordenan invirtiendo un único prefijo, por ejemplo

  $$
  (k,k-1,\ldots,1,k+1,\ldots,n).
  $$

- El máximo para este algoritmo es

  $$
  2n-3.
  $$

  En las regiones de tamaños $n,n-1,\ldots,3$ pueden requerirse dos volteos; cuando solo quedan dos elementos, basta uno porque el mayor necesariamente está arriba si aún no ocupa su lugar. Una entrada de tamaño cuatro que alcanza la cota es

  $$
  (2,4,3,1),
  $$

  para la cual se ejecutan $F_2,F_4,F_2,F_3,F_2$.

Si **se cuenta** cada inserción de la pala descrita literalmente, incluido $F_1$, cada iteración usa dos veces la pala. En ese modelo, el mínimo sigue siendo cero para una pila ordenada, el mínimo no trivial es dos y la cota máxima es $2(n-1)$.

La implementación puede evitar el volteo trivial agregando la condición `if biggest_index != 0` antes del primer giro.

### Complejidad temporal

Aunque el número de volteos es $O(n)$, encontrar el máximo pendiente cuesta $O(m)$ en una región de tamaño $m$. Si además cada inversión del arreglo cuesta $O(m)$, el tiempo total es

$$
\sum_{m=2}^{n}O(m)=O(n^2).
$$

Esto ilustra por qué contar operaciones conceptuales y medir el tiempo de implementación son análisis distintos.

### Ordenar en el sentido opuesto

Para obtener una pila descendente de arriba hacia abajo, se conserva el mismo algoritmo y se sustituye “mayor elemento pendiente” por **menor elemento pendiente**. Cada iteración lleva el menor arriba y después lo coloca al fondo de la región no ordenada. Así se construye desde abajo el sufijo que contiene los elementos más pequeños.

### Variante que construye de arriba hacia abajo

Un volteo de prefijo no puede conservar inmóvil un prefijo ya ordenado durante cada movimiento: cualquier $F_k$ con $k>1$ modifica la cima. Sin embargo, es posible simular una inversión de sufijo y recuperar el prefijo fijado al final de cada secuencia.

Sea $F_k$ el volteo de los primeros $k$ elementos. Para invertir el sufijo que comienza en la posición $j$, se realizan consecutivamente

$$
F_n,\qquad F_{n-j+1},\qquad F_n.
$$

Por ejemplo,

```text
[a,b,c,d,e,f] -> [f,e,d,c,b,a] -> [c,d,e,f,b,a] -> [a,b,f,e,d,c]
```

El resultado invierte únicamente el sufijo que empieza en `c` y devuelve `[a,b]` a su lugar. Usando esta operación, una variante superior funciona así:

1. Mantiene un prefijo ordenado de longitud $h$, inicialmente $h=0$.
2. Busca el menor elemento restante en las posiciones $h+1,\ldots,n$.
3. Invierte el sufijo que empieza en su posición para llevarlo al fondo.
4. Invierte el sufijo que empieza en $h+1$ para colocarlo inmediatamente después del prefijo fijado.
5. Incrementa $h$ y repite.

En los límites de cada iteración, el prefijo ordenado aumenta en un elemento. La desventaja es que cada inversión de sufijo requiere hasta tres volteos de prefijo, por lo que esta variante usa más la pala que la construcción desde abajo.

## Conceptos para extraer

- [[03_Conceptos/Ordenamiento de hot cakes|Ordenamiento de hot cakes]]
- [[03_Conceptos/Volteo de prefijo|Volteo de prefijo]]
- [[03_Conceptos/Invariante de ciclo|Invariante de ciclo]]
- [[03_Conceptos/Análisis de mejor y peor caso|Análisis de mejor y peor caso]]

## Referencias mencionadas

- *El Algoritmo de los Hot Cakes*, diapositivas 1–11.

## Resumen después de clase

El problema de los hot cakes modela un ordenamiento en el que solo se pueden invertir prefijos de una pila. El algoritmo lleva arriba el mayor elemento pendiente y después lo coloca al fondo de la región desordenada. El invariante establece que cada iteración aumenta el bloque correctamente colocado, lo que justifica tanto el progreso como la terminación. El ejemplo también muestra que analizar un algoritmo requiere distinguir corrección, número de operaciones y costo de implementación.

## Acciones adicionales

- [x] Resolver las preguntas de mejor y peor caso bajo las dos convenciones para $F_1$.
- [x] Proponer y justificar la variante que construye la pila de arriba hacia abajo.


## Material empleado
![[algoritmos-hotckes.pdf]]
