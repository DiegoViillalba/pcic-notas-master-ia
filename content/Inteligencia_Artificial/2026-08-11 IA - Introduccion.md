---
tipo: clase
materia: "[[Indice|Inteligencia Artificial]]"
fecha: 2026-08-11
unidad: Introducción y agentes racionales
profesor: Carlos Hernández
estado:
  - procesada
conceptos:
  - "[[Máquina de Turing|Máquina de Turing]]"
  - "[[Problema de la parada|Problema de la parada]]"
  - "[[Prueba de Turing|Prueba de Turing]]"
  - "[[Habitación china|Habitación china]]"
  - "[[IA fuerte e IA débil|IA fuerte e IA débil]]"
  - "[[Agente racional|Agente racional]]"
  - "[[Utilidad esperada|Utilidad esperada]]"
  - "[[Entorno de tarea|Entorno de tarea]]"
referencias:
  - "[[Artificial_inteliigence-A_modern_approach|Artificial Intelligence: A Modern Approach]]"
  - "[[AI 2 Agentes Inteligentes.pdf|AI 2 Agentes Inteligentes]]"
tags:
  - clase
  - inteligencia-artificial
---
![[AI 1 Introducción.pdf]]
# Clase 1 — Introducción a la inteligencia artificial

## Preguntas centrales

- ¿Qué es la inteligencia?
- ¿Qué es una máquina?
- ¿Por qué queremos que una máquina sea inteligente?
- ¿Puede pensar una máquina?

Estas preguntas no tienen una única respuesta aceptada. En la práctica, la inteligencia artificial estudia y construye sistemas capaces de percibir, razonar, aprender o actuar para resolver tareas. La definición cambia según si nos interesa imitar al ser humano, describir cómo piensa o construir agentes que elijan acciones racionales.

Una lectura útil para el curso es la siguiente:

- La **inteligencia** no se toma como una sola facultad, sino como un conjunto de capacidades para percibir, aprender, razonar y actuar eficazmente.
- Una **máquina** es un sistema físico o abstracto que ejecuta un procedimiento; la máquina de Turing ofrece el modelo formal más simple de esta idea.
- Queremos construir máquinas inteligentes para ampliar o automatizar nuestra capacidad de resolver problemas y tomar decisiones, especialmente cuando el número de posibilidades o la incertidumbre hacen difícil hacerlo manualmente.
- Preguntar si una máquina **piensa** depende del criterio utilizado. Podemos evaluar su conducta o la racionalidad de sus acciones, pero esas observaciones no resuelven por sí solas si posee comprensión o experiencia interna.

## Computabilidad y máquinas

Alan Turing formalizó la noción de computación mediante la [[Máquina de Turing|máquina de Turing]], un modelo matemático que permite precisar qué entendemos por un procedimiento algorítmico. Esta idea también permite hablar de los límites del cómputo.

El [[Problema de la parada|problema de la parada]] muestra uno de esos límites: no existe un algoritmo general que determine correctamente, para cualquier programa y cualquier entrada, si la ejecución terminará o continuará para siempre. Esto no significa que nunca podamos analizar un programa particular; significa que no puede existir un detector universal, automático y siempre correcto.

## Cuatro enfoques de la inteligencia artificial

Se presentaron dos ejes: **pensamiento frente a comportamiento** y **semejanza humana frente a racionalidad**. De su combinación surgen cuatro maneras de caracterizar el objetivo de la IA:

| Enfoque              | Pregunta guía                                                   | Método principal                                          |
| -------------------- | --------------------------------------------------------------- | --------------------------------------------------------- |
| Pensar como humanos  | ¿El sistema reproduce procesos mentales humanos?                | Modelado cognitivo, psicología y observación experimental |
| Actuar como humanos  | ¿Su comportamiento es indistinguible del humano?                | [[Prueba de Turing]]                         |
| Pensar racionalmente | ¿Obtiene conclusiones correctas a partir de lo que sabe?        | Lógica y leyes del pensamiento                            |
| Actuar racionalmente | ¿Elige la mejor acción posible según la información disponible? | Diseño de [[Agente racional]]                |

Pensar racionalmente no garantiza por sí solo actuar bien: una inferencia puede ser correcta y, aun así, llegar demasiado tarde o no considerar la incertidumbre. Por eso el curso adopta principalmente el enfoque de **actuar racionalmente**, que permite evaluar decisiones y resultados sin exigir que la máquina imite la mente humana.

## Pruebas y argumentos filosóficos

### Prueba de Turing

La [[Prueba de Turing|prueba de Turing]] fue propuesta como una manera operativa de evitar la vaguedad de la pregunta «¿puede pensar una máquina?». Un juez conversa por escrito con dos participantes ocultos, una persona y una máquina. Si de manera estadística, a partir de las respuestas, no puede distinguir de forma fiable cuál es la máquina, se considera que esta ha superado la prueba.

La prueba evalúa **comportamiento lingüístico indistinguible**, no demuestra directamente conciencia o comprensión. Para superarla, un sistema necesitaría al menos procesamiento de lenguaje natural, representación del conocimiento, razonamiento automático y aprendizaje. La prueba total de Turing añadiría percepción y acción en el mundo mediante visión computacional y robótica.

### Habitación china

En el argumento de la [[Habitación china|habitación china]], una persona que no entiende chino recibe símbolos y utiliza un libro de reglas para producir respuestas correctas en ese idioma. Desde fuera, su comportamiento puede parecer equivalente al de alguien que sí comprende chino; desde dentro, la persona solo manipula símbolos de acuerdo con reglas.

La conclusión propuesta por John Searle es que ejecutar correctamente un programa no basta para demostrar comprensión: la sintaxis, por sí sola, no garantiza semántica. El argumento cuestiona la idea de que pasar una prueba conductual sea suficiente para atribuir una mente a la máquina. No es una demostración aceptada de manera universal; existen objeciones, como la réplica de que la comprensión podría pertenecer al sistema completo y no a una de sus partes.

### IA fuerte e IA débil

La distinción entre [[IA fuerte e IA débil|IA fuerte e IA débil]] responde a una pregunta filosófica:

- **IA fuerte (dura en diapositivas):** sostiene que una máquina adecuadamente construida podría tener comprensión o estados mentales propios.
- **IA débil:** utiliza la computadora para simular o ejecutar capacidades inteligentes sin afirmar que posee conciencia o comprensión real.

«Débil» no significa poco capaz, y «fuerte» no es sinónimo exacto de IA general. Un sistema podría resolver muchas tareas y seguir considerándose IA débil si no afirmamos que realmente comprende lo que hace.

## Enfoque del curso: actuar racionalmente

Un [[Agente racional|agente racional]] es una entidad que percibe un ambiente y actúa sobre él. Para cada secuencia de percepciones, elige la acción que espera que maximice su indicador de desempeño, considerando la evidencia disponible y el conocimiento que posee.

Esto aclara la diferencia entre un agente **inteligente** y uno **racional**:

- **Inteligente** es una caracterización amplia que puede referirse a capacidades como aprender, razonar, comunicarse o adaptarse.
- **Racional** es un criterio técnico sobre la decisión: actuar de la mejor manera esperada con la información y los recursos disponibles.

Un agente racional no es omnisciente ni tiene que acertar siempre. Puede tomar una decisión razonable y obtener un mal resultado debido a información incompleta o a un ambiente incierto. La racionalidad se juzga por la decisión disponible en ese momento, no por conocer el futuro.

Cuando los resultados son inciertos, una forma de elegir es maximizar la [[Utilidad esperada|utilidad esperada]]. Si una acción $a$ puede producir resultados $s$, la idea general es

$$
EU(a)=\sum_s P(s\mid a,I)\,U(s),
$$

donde $I$ es la información disponible, $P(s\mid a,I)$ es la probabilidad del resultado y $U(s)$ representa qué tan deseable es. El agente compara las acciones y elige aquella con mayor utilidad esperada.

## Entorno de tarea

El diseño de un agente depende del [[Entorno de tarea|entorno de tarea]]. Este se especifica mediante el indicador de desempeño, el ambiente, los actuadores y los sensores. Además, puede caracterizarse con los siguientes contrastes:

| Propiedad | Distinción |
|---|---|
| Observabilidad | **Completamente observable** si los sensores muestran toda la información relevante; **parcialmente observable** si falta información o existe ruido. |
| Número de agentes | **Agente único** si basta modelar a un agente; **multiagente** si las decisiones de otros agentes afectan el resultado. |
| Incertidumbre | **Determinista** si el estado y la acción fijan el resultado; **estocástico** si los resultados se describen mediante probabilidades. |
| Dependencia temporal | **Episódico** si cada decisión puede tratarse por separado; **secuencial** si una acción afecta decisiones futuras. |
| Cambio durante la decisión | **Estático** si el ambiente no cambia mientras el agente decide; **dinámico** si continúa cambiando. |
| Representación | **Discreto** si estados, percepciones o acciones toman valores separados; **continuo** si varían dentro de intervalos. |
| Conocimiento | **Conocido** si el agente conoce las consecuencias de sus acciones; **desconocido** si debe aprenderlas. |

Estas propiedades no son simples etiquetas: condicionan qué tipo de agente y qué técnica de IA resultan adecuados.

## Ejemplo mínimo

Pensemos en un taxi autónomo. Percibe el camino mediante cámaras, GPS y otros sensores; actúa con el volante, el acelerador y los frenos; y puede ser evaluado por seguridad, rapidez, legalidad, comodidad y ganancias. Su entorno es parcialmente observable, multiagente, estocástico, secuencial, dinámico y continuo. Por eso no puede limitarse a seguir una regla fija: necesita tomar decisiones con información incompleta y comparar consecuencias posibles.

## Dudas resueltas

- Las distintas caracterizaciones de la inteligencia se organizan mediante los cuatro enfoques: pensar o actuar, de manera humana o racional.
- Un agente inteligente se describe por capacidades amplias; un agente racional se define por cómo selecciona acciones según su indicador de desempeño y la información disponible.
- La habitación china pretende mostrar que manipular símbolos correctamente no implica necesariamente comprender su significado, aunque esta conclusión es discutida.
- Russell y Norvig respaldan los cuatro enfoques, la prueba de Turing y el enfoque de agentes racionales. La presentación de la segunda clase confirma la definición de agente y la descripción del entorno de tarea utilizada en el curso.

> [!note] Referencia todavía por identificar
> En clase se mencionó un recurso de Berkeley, pero el material local no contiene su título ni su enlace exactos. Esta identificación documental queda pendiente y no cambia las definiciones desarrolladas en la nota.

## Relaciones

- La [[Prueba de Turing|prueba de Turing]] representa el enfoque de actuar como humanos y es cuestionada, desde la comprensión, por la [[Habitación china|habitación china]].
- La [[IA fuerte e IA débil|distinción entre IA fuerte e IA débil]] separa el desempeño observable de la afirmación de que existe una mente.
- El [[Problema de la parada|problema de la parada]] conecta la IA con los límites de la [[Máquina de Turing|computabilidad]].
- El [[Entorno de tarea|entorno de tarea]] determina qué necesita percibir y hacer un [[Agente racional|agente racional]].
- La [[Utilidad esperada|utilidad esperada]] permite comparar acciones cuando sus resultados son inciertos.

## Referencias

- Russell, Stuart J. y Norvig, Peter. *Artificial Intelligence: A Modern Approach*, 4.ª ed., capítulos 1 y 2. Copia local: [[Artificial_inteliigence-A_modern_approach|Artificial Intelligence: A Modern Approach]].
- [[AI 2 Agentes Inteligentes.pdf|AI 2 Agentes Inteligentes]], presentación de Carlos Hernández, diapositivas 4–5.
- Turing, Alan M. (1950). “Computing Machinery and Intelligence”. *Mind*, 59(236), 433–460.
- Searle, John R. (1980). “Minds, Brains, and Programs”. *Behavioral and Brain Sciences*, 3(3), 417–457. DOI: 10.1017/S0140525X00005756.

## Resumen después de clase

La inteligencia artificial puede abordarse desde cuatro perspectivas: pensar o actuar, de manera humana o racional. La prueba de Turing evalúa si una máquina actúa como una persona, mientras que la habitación china cuestiona que ese comportamiento sea suficiente para hablar de comprensión. El curso se concentra en agentes racionales: sistemas que perciben un entorno y eligen la mejor acción esperada según la información disponible y su indicador de desempeño. Qué decisión cuenta como racional depende tanto del objetivo como de las propiedades del ambiente en el que actúa el agente.
