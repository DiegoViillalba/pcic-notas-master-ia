---
tipo: concepto
aliases:
  - MRV
  - Minimum Remaining Values
  - Variable más restringida
  - Fail-first heuristic
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
estado: procesada
fuentes:
  - "[[2026-08-27 IA - CSP-Backtracking|CSP y backtracking]]"
  - "[[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]]"
  - "https://inst.eecs.berkeley.edu/~cs188/textbook/csp/ordering.html"
tags: [concepto, inteligencia-artificial, csp, heuristicas, ordenamiento]
---

# Heurística MRV

## La pregunta que responde

> **¿Qué variable no asignada conviene elegir ahora?**

MRV no decide qué valor probar ni elimina valores. Decide únicamente cuál será la siguiente variable del [[Backtracking|backtracking]].

> [!note] Prerrequisito mínimo
> Cada variable debe tener un **dominio actual**. Este dominio puede ser menor que el inicial porque [[Forward checking|forward checking]] o [[Algoritmo AC-3|AC-3]] ya eliminaron opciones.

## Definición

La heurística de **valores restantes mínimos** (*Minimum Remaining Values*, MRV) selecciona la variable no asignada con el menor número de valores legales:

$$
X^*=\arg\min_{X\text{ no asignada}}|D_{actual}(X)|.
$$

También se conoce como heurística de la **variable más restringida** o principio **fail first**.

## Intuición: descubrir pronto el fallo

Todas las variables tendrán que recibir un valor tarde o temprano. Si una de ellas casi no tiene opciones, posponerla puede llevarnos a construir una rama larga que de todos modos terminará fallando. MRV la atiende primero:

- si su dominio está vacío, el fallo se detecta inmediatamente;
- si tiene un único valor, la decisión está forzada;
- si tiene pocas alternativas, se resuelve pronto la zona más frágil del problema.

MRV no busca que la siguiente decisión sea fácil; busca que sea **informativa**.

## Ejemplo mínimo

Supongamos que, después de filtrar, quedan:

$$
D(A)=\{1,2,3\},\qquad D(B)=\{2\},\qquad D(C)=\{1,3\}.
$$

MRV elige $B$ porque $|D(B)|=1$. Si esa única opción conduce a un conflicto, se evita explorar combinaciones innecesarias de $A$ y $C$.

## Ejemplo: mapa de Australia

Tras asignar $WA=rojo$ y $NT=verde$, los dominios relevantes pueden quedar así:

| Variable | Dominio actual | Tamaño |
|---|---|---:|
| $SA$ | $\{azul\}$ | 1 |
| $Q$ | $\{rojo,azul\}$ | 2 |
| $NSW$ | $\{rojo,verde,azul\}$ | 3 |

MRV elige $SA$. La selección se basa en los dominios **actuales**, no en el hecho de que originalmente todas las regiones tenían tres colores.

## ¿Qué ocurre si hay empate?

Si varias variables tienen el mismo dominio mínimo, la **heurística de grado** suele actuar como desempate: se elige la variable involucrada en más restricciones con otras variables no asignadas. La intención es reducir el factor de ramificación de las decisiones futuras.

El orden recomendado es:

1. minimizar $|D_{actual}(X)|$ con MRV;
2. entre las empatadas, maximizar el número de vecinas no asignadas.

## Visualización básica

Abre primero la pestaña «Elegir variable: MRV». Lee la tabla de dominios de arriba hacia abajo y comprueba que la elección depende solo de su tamaño. Después cambia a LCV para distinguir las dos preguntas.

<iframe src="csp-mrv-lcv-fundamentos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## Del ejemplo a la búsqueda completa

En el laboratorio completo puedes activar y desactivar MRV. Para comparar con justicia, reinicia la simulación después de cambiar la opción y observa:

1. qué variable se selecciona en cada nivel;
2. cuántas ramas aparecen en el árbol;
3. qué tan pronto se detecta un dominio sin valores.

<iframe src="csp-mrv-lcv.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## Relación con filtrado y LCV

```mermaid
flowchart LR
  A["Asignación parcial"] --> F["Filtrar dominios"]
  F --> M["MRV elige variable"]
  M --> L["LCV ordena valores"]
  L --> P["Probar el primer valor"]
  P --> A
```

- El filtrado produce los tamaños de dominio que MRV compara.
- MRV elige la variable.
- [[Valor menos restrictivo|LCV]] ordena los valores de esa variable.

En particular, *forward checking* puede verse como una forma incremental y económica de mantener la información que MRV necesita.

## Límites

- Si todos los dominios tienen el mismo tamaño, MRV no distingue variables y necesita un desempate.
- Un dominio pequeño no garantiza que la variable forme parte del conflicto decisivo.
- Calcular y mantener dominios actuales tiene un costo, aunque normalmente se comparte con la propagación.
- MRV cambia el orden de exploración, pero no elimina el peor caso exponencial del CSP general.

## Error común

«Elegir la variable con más restricciones» no es la definición de MRV. Esa es la heurística de grado. MRV compara valores legales restantes; el grado solo suele usarse cuando esos tamaños empatan.

## Referencias

- Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], 4.ª ed., sección 5.3.1, p. 177.
- UC Berkeley CS 188, [«Ordering»](https://inst.eecs.berkeley.edu/~cs188/textbook/csp/ordering.html), sección 2.4.
- [[AI 5 Problemas de satisfacción de restricciones.pdf|Diapositivas: problemas de satisfacción de restricciones]].
- [[2026-08-27 IA - CSP-Backtracking|Apunte de clase: CSP y backtracking]], sección «Ordenamiento».
