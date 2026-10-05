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

Fitness y algoritmo evolutivo

En cada generacion:
1. Se evalua toda la poblacion.
2. Se ordenan los individuos por fitness.
3. Se conservan seis elites.
4. Se seleccionan padres entre los mejores individuos.
5. Se aplica cruce en un punto y mutacion gaussiana sobre los pesos.
6. Se completa la siguiente poblacion hasta llegar a 40 individuos.
Por defecto se ejecutan 40 generaciones y la semilla es aleatoria. Se puede fijar una semilla para reproducir un experimento concreto.

Ejecutar el laboratorio

Ejecucion normal, con 40 generaciones, semilla aleatoria y animacion:

python3 robot_red_neuronal_memoria.py

<img width="528" height="182" alt="image" src="https://github.com/user-attachments/assets/f6c4dfde-f00a-44bc-a148-ed288975fa87" />

Ejecucion reproducible y sin pausa entre cuadros:

<img width="642" height="92" alt="image" src="https://github.com/user-attachments/assets/1515345b-e4e8-4423-a127-0d9fbb67f247" />

Guardar la red separa dos fases del trabajo: primero se aprende una politica y despues se prueba esa misma politica bajo nuevas condiciones.

Probar en un mapa distinto
1. Ejecuta una evolucion y guarda mejor_red.pt.

python3 robot_red_neuronal_memoria.py --generaciones 40 --guardar-mejor mejor_red.pt

<img width="507" height="176" alt="image" src="https://github.com/user-attachments/assets/d45fd2cc-e6a5-4753-a879-49848219a851" />

<img width="633" height="82" alt="image" src="https://github.com/user-attachments/assets/a1595253-a0fe-4fcf-905b-2b5250b41965" />


2. Cambia manualmente OBSTACULOS, INICIO o META en el archivo.

3. Conserva el mismo TAMANO y evita colocar inicio o meta sobre un obstaculo.

<img width="366" height="177" alt="image" src="https://github.com/user-attachments/assets/25c66a94-faa2-4023-a551-00a79f9e67ef" />

4. Ejecuta con -cargar-red mejor_red.pt.

python3 robot_red_neuronal_memoria.py --cargar-red mejor_red.pt              

<img width="520" height="184" alt="image" src="https://github.com/user-attachments/assets/4c943655-9b4a-48a1-b9de-30a19e4ad1ab" />
   
5. Registra si la red llega, cuantos pasos usa, cuantos choques produce y si entra en un ciclo.

La red no logra llegar, aun con la modificacion de poder recordar sigue entrando en un ciclo.

Para que la comparacion sea valida, no se deben cambiar los pesos entre las dos pruebas. Solo se
modifica el mapa.

¿La memoria sensorial reduce la cantidad de ciclos?

Sí. Al expandir las entradas para incluir los sensores anteriores y la acción previa, el vector de información que procesa la red neuronal cambia en cada instante temporal, incluso si la ubicación física es la misma. Esto significa que cuando el robot se topa con un muro por segunda vez consecutiva, la red neuronal "ve" una entrada distinta a la primera vez (porque ahora incluye el historial del choque previo), lo que le permite calcular y emitir una orden de movimiento diferente, rompiendo así la repetición matemática.

¿La red aprende a escapar de patrones repetitivos?

Sí, impulsada por el mecanismo de selección del algoritmo evolutivo. Los individuos de la población cuyas redes neuronales ignoran la memoria y siguen repitiendo acciones frente a un muro terminan con un fitness bajo y son descartados. Por el contrario, las redes que mutan sus pesos para darle importancia a los datos pasados, cambiando su acción cuando detectan que el estado actual y el anterior son casi idénticos, logran avanzar más, obtienen un fitness superior y heredan esta capacidad a las siguientes generaciones.

¿La red con memoria llega a la meta en mapas más complejos?

Sí. Los mapas complejos suelen incluir geometrías como esquinas, cuellos de botella o formas en "U" que actúan como trampas locales. Un agente puramente reactivo se estanca en estas geometrías porque sus sensores frontales y laterales inmediatos le indican que está rodeado. Al tener memoria a corto plazo, el agente puede detectar que lleva varios pasos sin progreso real, lo que le permite tomar decisiones contraintuitivas (como retroceder o alejarse temporalmente de la meta) para rodear el obstáculo y resolver el laberinto.

¿Qué pasa si el fitness penaliza la repetición de posiciones y secuencias?

La evolución del modelo se vuelve mucho más agresiva hacia la exploración. Al restar puntos de fitness cada vez que el robot pisa la misma coordenada (X, Y) o repite un bucle de acciones (como Izquierda-Derecha-Izquierda-Derecha), el algoritmo castiga directamente las políticas estáticas. Esto fuerza a la red neuronal a depender fuertemente de su memoria sensorial para asegurarse de probar siempre rutas nuevas, evitando el sobreajuste a un solo camino y resultando en una política de navegación más generalizable y fluida.

Diseño del ejercicio

La idea es que ustedes trabajen sobre la base ya entregada y realicen cambios puntuales, sin reconstruir todo el proyecto desde cero. Se sugiere:

1. Revisar el codigo de los laboratorios previos y la base del laboratorio 8 entregada para identificar donde se define la observacion de la red y como se toma la accion.

2. Modificar la entrada de la red para incluir st−1 y at−1 .

Actualmente, la red neuronal recibe solo los sensores actuales. Se debe modificar la función o clase que crea la red para que acepte más entradas. Se tienes 4 sensores y 4 acciones posibles, la nueva entrada será de 12 neuronas: Sensores actuales: 4 valores. Sensores anteriores: 4 valores. Acción anterior: 4 valores 


3. Mantener el algoritmo genetico y la funcion de fitness, ajustando solo lo necesario para penalizar bucles.

4. Entrenar una poblacion de redes con memoria sensorial.
   
5. Guardar la mejor red.
    
6. Cambiar el mapa o la posicion inicial.
    
7. Probar la misma red sin volver a evolucionar.
    
8. Comparar exito, choques, pasos y ciclos.

Conclusión: La Importancia de la Memoria Temporal en la Navegación Autónoma

El desarrollo de este laboratorio demuestra que la verdadera inteligencia en la navegación autónoma no depende únicamente de la percepción instantánea, sino de la capacidad de contextualizar el presente a través del pasado reciente. Al evolucionar de un agente puramente reactivo a uno con memoria temporal, comprobamos que dotar al modelo de un historial a corto plazo —recordar qué observó y qué acción ejecutó en el instante anterior— es el mecanismo fundamental para resolver el problema de los ciclos sensoriomotores.

Mientras que un robot reactivo queda atrapado en bucles infinitos al recibir la misma lectura sensorial frente a un obstáculo o esquina, la integración de la memoria temporal le otorga al modelo la capacidad de reconocer sus propios patrones de repetición. Al detectar que una secuencia de movimientos no está generando un cambio en el entorno, la red neuronal puede tomar decisiones alternativas y escapar de la trampa.

En definitiva, este ejercicio nos confirma que construir sobre la base de modelos previos para añadir una dimensión temporal es un paso crucial hacia la generalización. La memoria temporal transforma una política rígida, propensa a atascarse, en una estrategia de navegación dinámica, adaptable y mucho más robusta frente a entornos desconocidos o modificados.
