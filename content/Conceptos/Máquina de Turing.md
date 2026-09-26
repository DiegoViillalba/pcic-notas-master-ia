---
tipo: concepto
aliases:
  - Turing machine
area: inteligencia artificial
materias:
  - "[[Indice|Inteligencia Artificial]]"
  - "[[Indice Analisis y diseño de algoritmos|Análisis y Diseño de Algoritmos]]"
estado: semilla
fuentes:
  - "[[2026-08-11 IA - Introduccion|Introducción a IA]]"
  - "[[2026-08-11 ADA - Introducción al curso|Introducción a algoritmos]]"
tags:
  - concepto
  - inteligencia-artificial
  - computabilidad
  - algoritmos
---

# Máquina de Turing

## Definición

La máquina de Turing es un modelo matemático abstracto que nos permite definir una máquina teórica capaz de realizar cualquier cómputo expresable mediante un [[Algoritmo]]. Propuesta por el matemático Alan Turing, es una herramienta conceptual que nos permite determinar los límites de lo que las computadoras pueden o no resolver.

## Componentes

La máquina está compuesta por cuatro elementos fundamentales:

- Una cinta infinitamente larga que funge como memoria del sistema. Puede almacenar símbolos de un alfabeto finito.
- Un cabezal de lectura y escritura, capaz de recorrer la cinta de izquierda a derecha, una casilla a la vez. Tiene la capacidad de leer el símbolo actual, borrarlo y escribir uno nuevo.
- Un registro de estados: un almacén interno del estado actual de la máquina, que representa la situación o el contexto en el que se encuentra.
- Una tabla de transición: es el símil de un programa; corresponde al conjunto de instrucciones que le dicen a la máquina qué hacer basándose en el estado actual y el símbolo que está leyendo.
## Funcionamiento

El funcionamiento es un ciclo mecánico continuo que sigue una lógica estrictamente matemática de "Si pasa X, haz Y":

1. **Inicio:** Se introduce la cadena de datos en la cinta y la cabeza se coloca en la primera casilla. La máquina arranca en un "Estado Inicial" predeterminado.
2. **Lectura:** La cabeza lee el símbolo de la casilla actual.
3. **Consulta:** La máquina busca en su tabla de transición la regla que coincida exactamente con su _Estado Actual_ + _Símbolo Leído_.
4. **Ejecución:** La máquina ejecuta la regla (escribe, se mueve y cambia de estado).
5. **Ciclo o Parada:** El proceso se repite casilla por casilla hasta que la máquina llega a un "Estado de Parada" (un estado final donde no hay más instrucciones). El resultado final del cálculo queda escrito en la cinta.

---

## Importancia

La Máquina de Turing revolucionó la ciencia y la filosofía por tres razones fundamentales:

- **Definió el concepto de "Algoritmo":** Antes de Turing, la humanidad no tenía una definición matemática formal de lo que significaba "calcular de forma mecánica". Él demostró que cualquier proceso de cálculo puede desglosarse en pasos lógicos increíblemente simples.
- **La Máquina Universal de Turing:** Turing demostró que se podía construir una máquina específica cuya cinta contuviera las instrucciones de _otras_ máquinas de Turing, sentando las bases para la existencia de una computadora programable.
- **La Tesis de Church-Turing:** Propone que todo procedimiento de cálculo que pueda realizarse de manera efectiva puede ser ejecutado por una Máquina de Turing. Si un problema no puede ser resuelto por una Máquina de Turing, ninguna computadora convencional podrá resolverlo.
- **[[Problema de la parada]] (Halting Problem):** Turing demostró matemáticamente que existen problemas lógicos imposibles de resolver para cualquier computadora. Probó que no se puede diseñar un algoritmo general que determine si _cualquier_ programa se detendrá o se quedará ciclado para siempre, estableciendo límites fundamentales para la tecnología y la lógica humana.

---

## Límites y relaciones

- Se relaciona con: [[Problema de la parada|Problema de la parada]]
- Se diferencia de:

## Procedencia

- Clase: [[2026-08-11 IA - Introduccion|Introducción a IA]]
- Clase: [[2026-08-11 ADA - Introducción al curso|Introducción a algoritmos]]
- Fuente: presentación introductoria de *Análisis y Diseño de Algoritmos*, diapositiva 3.
- Fuente de la clase de IA: por verificar.
