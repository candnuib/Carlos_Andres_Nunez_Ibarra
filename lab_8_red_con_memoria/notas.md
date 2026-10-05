INTELIGENCIA ARTIFCIAL.

Laboratorio 8

Redes con memoria sensorial para romper ciclos en navegacion reactiva

Problema del robot reactivo:
En el laboratorio anterior, el robot respondia a la observacion actual. Si la secuencia de decisiones se repite, el robot puede quedar atrapado en un ciclo aunque la situacion local no haya cambiado.

Solucion:

La idea clave es que la decision depende no solo del presente, sino tambien del pasado reciente. 
La red ya no decide solo con el presente, sino con memoria de corto plazo.

Como funciona:

El entorno genera sensaciones; el agente actua; la accion modifica el entorno; el ciclo se repite

Consecuencia

La politica puede detectar secuencias repetitivas y evitar caer en ciclos locales.

Entradas: sensores actuales, sensores anteriores y accion previa.

Capa oculta: combina la informacion para aprender patrones locales.

Salidas: un valor por cada accion {U, D, L, R}.

Decision: se elige la salida con mayor valor mediante arg máx.

Interpretacion:
La red usa el presente y el paso anterior para decidir hacia donde moverse.

La red compara todas las opciones con el estado presente y reciente.

Con memoria el agente puede reconocer que:
la observacion actual es parecida a la anterior, la accion anterior fue la misma, la secuencia se vuelve circular.

Hipotesis

Una red con entrada de memoria sensorial y accion previa reducira la frecuencia de ciclos y mejorara la capacidad de navegacion local en entornos con obstaculos.

Objetivo experimental: comparar la red basica contra la red con memoria.

* La memoria sensorial hace que la decision sea menos reactiva pura.
* El robot valora no solo lo que ve, sino lo que ya hizo.
* La red aprende una politica con dependencia temporal.
* Esto es una forma simple de inteligencia sensoriomotora.

Laboratorio IA 8: Redes con memoria sensorial para romper ciclos en navegacion reactiva

Extender la base de la red neuronal evolutiva para que el robot recuerde su estado reciente y reduzca la probabilidad de quedar atrapado en ciclos. La tarea consiste en revisar la estructura de los laboratorios previos y modificar la implementacion entregada, manteniendo la misma logica general del robot, el fitness y la evolucion genetica.

Continuidad con las clases anteriores

El laboratorio conserva el mundo del robot usado en las sesiones anteriores: una cuadricula, un punto
de inicio, una meta, obstaculos, sensores locales y una funcion de fitness. La progresion es:

* En las primeras clases se evoluciono una secuencia de movimientos.
* Despues se incorporaron obstaculos y se compararon mutacion y cruce.
* Con la percepcion local, el robot paso a consultar el entorno antes de decidir.
* En el laboratorio 7 se reemplazo la tabla de reglas por una red neuronal.
* En este laboratorio se conserva esa base, pero se agrega memoria temporal para que el robot recuerde su estado anterior y la ultima accion.

La evolucion sigue seleccionando comportamientos por fitness. Lo que cambia es la representacion del estado de entrada: antes la red solo observaba el presente; ahora ademas incorpora lo visto y hecho en el instante anterior.

No se trata de reescribir el robot desde cero. La tarea es identificar que parte del codigo anterior se conserva y que parte debe cambiar para incluir memoria temporal y evitar ciclos.

La entrada total queda formada por 12 valores:

* 4 sensores actuales,
* 4 sensores anteriores,
* 4 bits de la accion previa (codificacion one-hot).

Esto funciona como una ventana temporal de corto alcance. El robot ya no decide solo con el presente, sino con una memoria reciente del estado.


