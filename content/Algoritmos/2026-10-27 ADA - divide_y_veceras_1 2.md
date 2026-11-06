---
tipo: clase
materia:
fecha: "2026-10-27"
unidad:
profesor:
estado:
  - por-capturar
  - por-revisar
  - por-procesar
conceptos: []
referencias: []
tags:
  - clase
---
## Pregunta central

¿Qué problema o idea intenta explicar esta clase?

## Apuntes rápidos

- Iniciamos con las slides de divide y vencerás
- comenzamos ablando de busqueda binaria recursiva

![[Screenshot 2026-10-27 at 11.46.49 a.m..png]]


Relaizando inun analisis fe timepo tenemo 
$T(n) \leq T(n/2)+c$

$T(2) \leq c$



dESARROLLAMOS LA PRUENA DE TERMINACION DEL ALGORTIMO

![[Screenshot 2026-10-27 at 12.00.41 p.m..png]]

Desarrrollamos la metodologir de recursive unfolding, donde por nivelees necionamos como en el nivel 0 (la llamad de la funcion), mencionamos lnumero de isntruccione suqe se realizan, podeteriorementes e suman las isntrucciones por nivel
![[Screenshot 2026-10-27 at 12.02.32 p.m..png]]


tambien se puede hacer por induccion 

![[Screenshot 2026-10-27 at 12.09.38 p.m..png]]
![[Screenshot 2026-10-27 at 12.09.49 p.m..png]]

Posterioremente para el arol de inducción odemos ver que determinaod de la forma
![[Screenshot 2026-10-27 at 12.32.07 p.m..png]]

Donde en la frmula tenemos :

![[Screenshot 2026-10-27 at 12.32.28 p.m..png]]
$$
= O (nlog(n
))
$$
Probar por idccion en n
$$
T(n) \leq cnlog_2(n)
$$

Depsues avanzamos contado de inversiones en las notads

Conteo de inversiones 
se desarrollo el algoritmo en tardos, vemos

![[Screenshot 2026-10-27 at 12.48.33 p.m..png]]


lo acabamos , nos vamos a saltar la siguietne seccincon un resumen y comenzaremoa calcualr el conjunto de puntos ams cercanos
## Definiciones y resultados


### Concepto o resultado

Explicación:

$$
% Ecuación, si corresponde
$$

## Ejemplo

Problema, procedimiento y resultado.

## Dudas

- [ ] 

## Conceptos para extraer

- [[Concepto atómico]]

## Referencias mencionadas

- 

## Resumen después de clase

En 3–5 oraciones, ¿qué aprendí y cómo se conecta con clases anteriores?

## Acciones adicionales

- [ ] Resolver dudas pendientes.
