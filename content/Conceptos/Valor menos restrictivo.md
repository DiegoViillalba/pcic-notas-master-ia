---
tipo: concepto
aliases:
  - LCV
  - Least Constraining Value
  - Valor menos restrictivo
  - Fail-last heuristic
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

# Valor menos restrictivo

## La pregunta que responde

> **Una vez elegida la variable, ¿qué valor conviene probar primero?**

LCV no selecciona variables y no descarta definitivamente los otros valores. Solo determina el orden en que el [[Backtracking|backtracking]] los intentará.

## Definición

La heurística del **valor menos restrictivo** (*Least Constraining Value*, LCV) prueba primero el valor que elimina menos opciones de los dominios de las variables vecinas no asignadas.

Si $D_v(Y)$ es el dominio que conservaría una vecina $Y$ después de probar temporalmente $X=v$, puede asignarse a cada candidato el costo

$$
\operatorname{costo}(v)=
\sum_{Y\in Vecinas(X)\text{ no asignadas}}
\bigl|D(Y)\setminus D_v(Y)\bigr|.
$$

LCV ordena los valores de menor a mayor costo.

## Intuición: conservar flexibilidad

Para encontrar una solución basta con que **un** valor conduzca a una rama completa. Por eso conviene intentar primero el candidato que deja más alternativas abiertas para el futuro. A esta idea se le llama a veces **fail last**.

Esto complementa a [[Heurística MRV|MRV]]:

- MRV busca descubrir pronto si una variable inevitablemente falla.
- LCV intenta que el valor elegido tenga mayor oportunidad de sobrevivir.

No hay contradicción: una heurística elige la variable y la otra ordena sus valores.

## Ejemplo paso a paso

En el mapa de Australia se han asignado $WA=rojo$ y $NT=verde$. Supongamos que ahora se debe asignar $Q$:

$$
D(Q)=\{rojo,azul\},\qquad D(SA)=\{azul\}.
$$

$SA$ y $NSW$ son vecinas no asignadas de $Q$.

### Candidato 1: $Q=rojo$

- `rojo` ya no pertenecía a $D(SA)$, así que $SA$ conserva $\{azul\}$;
- se elimina `rojo` de $D(NSW)$;
- costo total de poda: 1.

### Candidato 2: $Q=azul$

- se elimina el único valor de $D(SA)$, que queda vacío;
- también se elimina `azul` de $D(NSW)$;
- costo total de poda: 2 y la rama falla.

LCV prefiere $Q=rojo$. Este es el ejemplo utilizado por Russell y Norvig para mostrar que el valor aparentemente disponible no siempre conserva opciones futuras.

## Visualización básica

Abre la pestaña «Elegir valor: LCV» y alterna entre $Q=rojo$ y $Q=azul$. Compara primero el número de opciones eliminadas y después verifica si algún dominio queda vacío.

<iframe src="csp-mrv-lcv-fundamentos.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## Del ejemplo a la búsqueda completa

En el laboratorio completo, LCV modifica el orden de los candidatos de la variable seleccionada. Reinicia después de activar o desactivar la heurística y compara el orden registrado, los retrocesos y el tamaño del árbol.

<iframe src="csp-mrv-lcv.htm" style="width:100%;height:600px;border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>

## ¿Cómo se calcula en la práctica?

Para cada valor candidato puede realizarse una inferencia temporal:

1. asignar provisionalmente $X=v$;
2. ejecutar [[Forward checking|forward checking]], [[Algoritmo AC-3|AC-3]] u otro filtro;
3. contar cuántos valores vecinos fueron eliminados;
4. restaurar los dominios;
5. ordenar los candidatos por ese costo.

Una estimación más barata puede limitarse a contar conflictos directos. Una evaluación más profunda suele ordenar mejor, pero también consume más tiempo.

## Cuándo importa el orden

- **Encontrar una solución:** LCV puede hacer que una solución aparezca antes y evitar retrocesos.
- **Enumerar todas las soluciones:** el orden no cambia el conjunto final de soluciones ni evita visitar todas las ramas necesarias, aunque sí cambia cuándo se encuentra cada una.
- **Demostrar que no hay solución:** todos los valores tendrán que descartarse; LCV puede aportar menos beneficio.

## Límites

- Calcular el impacto de cada valor añade trabajo.
- El valor que poda menos ahora puede conducir a un conflicto más profundo.
- Muchos candidatos pueden empatar, especialmente en problemas simétricos.
- LCV cambia el orden, pero no garantiza una solución ni elimina el peor caso exponencial.

## Errores comunes

- Elegir el valor menos frecuente sin medir su efecto sobre los dominios vecinos.
- Confundir «menos restrictivo» con «más probable» sin definir una medida de impacto.
- Eliminar definitivamente los otros valores: LCV solo los reordena.
- Aplicar LCV antes de elegir la variable.

## Referencias

- Russell y Norvig, [[Artificial_inteliigence-A_modern_approach.pdf|Artificial Intelligence: A Modern Approach]], 4.ª ed., sección 5.3.1, pp. 177–178.
- UC Berkeley CS 188, [«Ordering»](https://inst.eecs.berkeley.edu/~cs188/textbook/csp/ordering.html), sección 2.4.
- [[AI 5 Problemas de satisfacción de restricciones.pdf|Diapositivas: problemas de satisfacción de restricciones]].
- [[2026-08-27 IA - CSP-Backtracking|Apunte de clase: CSP y backtracking]], sección «Ordenamiento».
