INTELIGENCIA ARTIFICIAL.

Podemos conservar la percepcion local y cambiar la forma en que el robot representa su
politica?

Análisis:

1. Percepción Local:

Los sensores del robot hacen su trabajo. Simulando un entorno en Python o usando sensores físicos en un microcontrolador, los datos recopilados sobre el entorno inmediato (ej. "hay un obstáculo" o "el camino esta libre") no cambian. Esos datos crudos siguen siendo la forma en que el robot "ve" el mundo.

2. Representación de la Política:

La "política" es el cerebro del robot, un mecanismo que toma los datos de los sensores y decide qué acción ejecutar.
En un modelo anterior el "ADN" del robot representaba una cadena de movimientos directos (ej. [ U, D, R, L ]) que mutaba si habia obstáculo en frente para evitalo.
Con una Red Neuronal, la política ahora es una función matemática estructurada en capas.
Los datos de los sensores se conectan directamente a las neuronas de entrada.
Las decisiones del movimiento salen de las neuronas de salida.
En el medio, las capas ocultas procesan la información.

3. Al combinar redes neuronales con algoritmos evolutivos (llamado Neuroevolución), el ADN cambia de forma:

El ADN ya no es una lista de pasos, ahora son los pesos (weights) y sesgos (biases) de la red neuronal.
Cuando el robot navega por la ruta y choca o llega a la meta, evalúas su fitness igual que antes. Al momento de hacer los cruces genéticos y las mutaciones para la siguiente generación, lo que estás cruzando y mutando son los valores de las conexiones neuronales de los robots más aptos.

Respuesta:

"Sí, podemos conservar la percepción local usando los mismos datos de los sensores como las entradas (inputs) del sistema. Lo que cambia es la representación de la política: dejamos atrás las secuencias estáticas o reglas rígidas y pasamos a usar una red neuronal para mapear esas entradas hacia las acciones (outputs). En nuestro modelo evolutivo, el 'ADN' que cruzamos y mutamos ya no son listas de movimientos, sino que pasa a ser el conjunto de pesos y conexiones de la red neuronal de cada robot."

El sensor (hardware/percepción) y la política (software/decisión) son módulos independientes que ayudan a diseñar arquitecturas.

Se conserva:
* La cuadrucula y los obstaculos.
* Los sensores U, D, L y R.
* El recorrido del robot.
* El fitness y el algoritmo evolutivo.

Cambia:
* La tabla de reglas desaparece.
* Cada individuo es una red.
* Los genes son pesos numericos.
* Se usa PyTorch para decidir.

Idea central: 
La evolucion sigue buscando una buena politica; ahora la politica esta parametrizada por una
red neuronal.

4 sensores -> 8 neuronas + ReLU -> 4 valores de accion

Decision:
La red calcula un valor para U, D, L y R. El robot ejecuta la accion con mayor valor mediante argmax.

Representacion: 
En la politica tabular evolucionabamos reglas. Aqui evolucionamos todos los pesos de la red.

Logica: 
Cuatro entradas representan la percepcion local; la capa oculta combina la informacion y cuatro salidas compiten por controlar el siguiente movimiento.

Durante el entrenamiento:
* Se prueban muchas redes.
* Se conserva la mejor.
* La evolucion puede terminar.

Despues del entrenamiento:
* Se guardan los pesos en mejor_red.pt.
* Se carga la misma politica.
* Se prueba en otro mapa.

Separar aprender y probar: 
Esto permite medir si la politica funciona solo en el mapa de entrenamiento o si responde bien a una nueva distribucion de obstaculos.

Laboratorio IA 7: Red neuronal pequena y evolucion por algoritmo genetico.

Construir una red neuronal pequena con PyTorch que controle al robot de percepcion local y evolucionar sus pesos mediante un algoritmo genetico. El mejor individuo se guardara en disco para probarlo posteriormente sobre un mapa modificado a mano.

El algoritmo evolutivo sigue seleccionando comportamientos por fitness. Lo que cambia es la representacion del individuo: antes eran comandos o reglas; ahora son los pesos de una red neuronal.

Comprobacion instalacion:
<img width="644" height="61" alt="image" src="https://github.com/user-attachments/assets/645e7e26-ee49-4d84-9a77-725713f9831e" />

Ejecutar el laboratorio

python3 robot_red_neuronal_evolutiva.py

<img width="532" height="390" alt="image" src="https://github.com/user-attachments/assets/e1ed5c50-6e5a-46fc-b2a0-355f4061ec4c" />

python3 robot_red_neuronal_evolutiva.py \\
--semilla 7 --generaciones 40 --sin-pausa

<img width="520" height="385" alt="image" src="https://github.com/user-attachments/assets/2f91b8b9-3be0-40c0-8ea8-b07e34dfeee6" />

Guardar y cargar el mejor individuo

python3 robot_red_neuronal_evolutiva.py \\
--generaciones 40 --guardar-mejor mejor_red.pt

<img width="495" height="319" alt="image" src="https://github.com/user-attachments/assets/f3bb194d-2dc5-4d14-8d99-95ce4e085dae" />

<img width="556" height="43" alt="image" src="https://github.com/user-attachments/assets/7506092d-482e-4376-9adf-7318cc18d410" />

Para cargarlo sin evolucionar otra vez:

python3 robot_red_neuronal_evolutiva.py \\
--cargar-red mejor_red.pt

<img width="496" height="166" alt="image" src="https://github.com/user-attachments/assets/cd166200-e92e-4c5d-bc68-d9951d82c92b" />

Guardar la red separa dos fases del trabajo: primero se aprende una politica y despues se prueba esa misma politica bajo nuevas condiciones.

Probar en un mapa distinto.

Cambio de OBSTACULOS, INICIO o META en el archivo.

<img width="388" height="161" alt="image" src="https://github.com/user-attachments/assets/5f9d818b-79e0-438e-8142-4622f635432b" />

Ya modificado se vuelve a compilar el codigo para caegar sin evolucionar, tomando la mejor red.

<img width="652" height="196" alt="image" src="https://github.com/user-attachments/assets/7523ec1e-baf7-4fc4-a749-460cf8260f17" />


<img width="526" height="324" alt="image" src="https://github.com/user-attachments/assets/a7699a8d-8684-466b-86e0-c4c288488898" />

1\. ¿Qué se conserva entre la clase de percepción local y este laboratorio?

Se conserva **la percepción local a través de los sensores del robot**. Los datos que los sensores recopilan sobre el entorno inmediato siguen siendo las entradas (*inputs*) del sistema. También se conserva el objetivo conceptual o la métrica de evaluación (*fitness*) para medir el desempeño del robot. Lo que cambia no son los sensores, sino el mecanismo de toma de decisiones (la política), que pasa de ser una lista estática de reglas/movimientos a una red neuronal.


2\. ¿Qué información representa un peso de la red que antes representaba una regla?

Antes, una regla condicional o tabla de decisión asociaba de forma directa una lectura sensorial con una acción fija.

Ahora, **un peso de la red representa la intensidad e influencia matemática de una conexión entre neuronas**. En conjunto con las capas ocultas y los sesgos (*biases*), los pesos determinan cuánto influye cada señal de los sensores en las neuronas de salida (motores o acciones). Los pesos transforman reglas rígidas "si-entonces" en un mapeo funcional continuo entre percepción y acción.

3\. ¿Por qué una red entrenada en un mapa puede fallar en otro mapa?

La red falla porque se ajustó exclusivamente a las condiciones y trayectoria del mapa inicial. Si las entradas de la red solo incluyen lecturas locales inmediatas sin referencia a la posición de la meta, el modelo simplemente **asoció configuraciones de sensores con movimientos que eran exitosos en la geometría de ese mapa específico**. Al cambiar la salida, la meta y agregar nuevos obstáculos, el robot se enfrenta a combinaciones de lecturas no vistas durante el entrenamiento, lo que provoca decisiones erróneas o bloqueos.

4\. ¿La política aprendida generaliza o solo memoriza respuestas locales?

En la configuración actual de tu laboratorio, **la política solo memoriza respuestas o patrones locales adaptados al escenario de entrenamiento**. Al haber entrenado en una sola ruta fija y carecer de información global sobre dónde está el objetivo, la red neuronal no aprende el concepto abstracto de "navegar hacia una meta", sino únicamente a reaccionar ante la secuencia concreta de obstáculos de ese mapa en particular.

5\. ¿Qué cambios permitirían que el robot conociera la dirección de la meta?

Para que el robot entienda hacia dónde dirigirse independientemente del mapa, se pueden implementar las siguientes modificaciones:

* **Agregar la dirección de la meta a las entradas (** **inputs** **) de la red:** Incluir valores sensoriales que indiquen el ángulo o vector relativo hacia la meta (por ejemplo: *"la meta está a 45° a la izquierda"*) y la distancia que falta para llegar.
* **Entrenar en entornos variables (multiescenario):** Cambiar aleatoriamente el punto de inicio, la posición de la meta y la ubicación de los obstáculos durante cada generación del entrenamiento. Esto fuerza a la red a no memorizar un mapa, sino a aprender a priorizar el vector de la meta mientras esquiva bloqueos.
* **Ajustar la función de evaluación (** **fitness** **):** Recompensar a la red en cada paso en función de la reducción del ángulo y distancia hacia la meta, promoviendo que la política aprenda la dirección correcta.

Experimento y tabla de resultados

Semilla 7.

python3 robot_red_neuronal_evolutiva.py  --semilla 7 --generaciones 40 --sin-pausa --guardar-mejor mejor_red.pt

<img width="543" height="174" alt="image" src="https://github.com/user-attachments/assets/5c677ab3-b0f6-4824-ad6e-71bb652301d3" />

python3 robot_red_neuronal_evolutiva.py --cargar-red mejor_red_7.pt

<img width="511" height="173" alt="image" src="https://github.com/user-attachments/assets/8699f216-39f6-4f9a-b155-612be1167fe5" />

python3 robot_red_neuronal_evolutiva_1.py --cargar-red mejor_red_7.pt

<img width="499" height="175" alt="image" src="https://github.com/user-attachments/assets/feae740d-b496-4baa-96f4-f111fcaf18b8" />

Semilla 21.

<img width="541" height="181" alt="image" src="https://github.com/user-attachments/assets/8068f5f2-6636-4634-b61e-3b3000251111" />

python3 robot_red_neuronal_evolutiva_1.py --cargar-red mejor_red_21.pt

<img width="495" height="329" alt="image" src="https://github.com/user-attachments/assets/0c52b60b-c098-4862-bb2a-7fa7baecb72b" />

Semilla 42.

python3 robot_red_neuronal_evolutiva.py  --semilla 42 --generaciones 40 --sin-pausa --guardar-mejor mejor_red_42.pt

<img width="498" height="170" alt="image" src="https://github.com/user-attachments/assets/995a7a0c-ec02-4121-a37e-36a66f03c972" />

python3 robot_red_neuronal_evolutiva_1.py --cargar-red mejor_red_42.pt

<img width="510" height="326" alt="image" src="https://github.com/user-attachments/assets/8e71fec3-04d0-45d0-984f-c8818dd4523c" />

Análisis de la Prueba: Comportamiento ante un Entorno Modificado

En esta prueba, tomamos el mejor modelo (la mejor red neuronal) obtenido tras entrenar a nuestra población en un mapa original utilizando una semilla específica. Este individuo había demostrado ser altamente eficiente (alto fitness) para llegar a la meta en su entorno de entrenamiento.

Sin embargo, para evaluar su robustez, alteramos las condiciones del mapa: cambiamos el punto de inicio, movimos la meta y bloqueamos la ruta original con un muro. Ante este nuevo escenario, el modelo falló y quedó atrapado en un bucle infinito de colisiones y oscilaciones contra el muro.

¿Por qué ocurrió esto?

El fracaso se debe a la naturaleza de la política puramente reactiva que desarrolló el modelo:

Falta de memoria (Estado oculto): La red neuronal toma decisiones basándose únicamente en las lecturas instantáneas de sus sensores en ese preciso momento temporal, sin guardar un registro de sus acciones o estados pasados.

El Bucle Sensorial: Al acercarse al nuevo muro, los sensores detectan el obstáculo a corta distancia. La red procesa esta entrada y emite una orden de movimiento según los pesos que aprendió en el mapa original. Como el camino está bloqueado, el robot no avanza significativamente; por lo tanto, en el siguiente instante de tiempo, la lectura de los sensores es idéntica a la anterior. Al recibir la misma entrada, la red neuronal emite exactamente la misma salida, creando un ciclo repetitivo del que el robot no puede escapar.

Conclusión: Evolución, Percepción Local y Generalización

El comportamiento observado en esta prueba nos deja una lección fundamental sobre cómo interactúan el diseño de los sensores, los algoritmos evolutivos y la capacidad de adaptación de un modelo:

Sobre la Evolución (El problema del Sobreajuste): El algoritmo evolutivo hizo exactamente lo que le pedimos: maximizar el fitness en el entorno de entrenamiento. La evolución optimizó los pesos de la red neuronal para resolver ese mapa en particular, encontrando atajos y patrones específicos de esa ruta. El modelo no evolucionó para "saber navegar", sino que evolucionó para "memorizar" una ruta específica, convirtiéndose en un sistema frágil ante los cambios.

Sobre la Percepción Local (La miopía del robot): Los sensores proporcionan una percepción estrictamente local. El robot solo "ve" lo que tiene a su lado o frente a él en un radio muy limitado, pero carece de un mapa global. La percepción local es excelente para la evasión reactiva de obstáculos inmediatos, pero es insuficiente para la navegación compleja a largo plazo si no está acompañada de algún tipo de memoria o estado interno (como redes neuronales recurrentes) que le permita al robot inferir que está atascado y debe buscar una ruta alternativa.

Sobre la Generalización (El objetivo final de la IA): Esta prueba ilustra un fallo clásico de generalización. Un modelo generaliza bien cuando puede aplicar lo aprendido a escenarios que nunca ha visto. Nuestro robot fracasó al generalizar porque su política reactiva estaba sobrentrenada para un conjunto muy específico de estados sensoriales. Para lograr una verdadera generalización en el futuro, no basta con cambiar el mapa en la prueba; necesitamos someter a la población a entornos aleatorios y cambiantes durante el proceso evolutivo, forzando así al ADN (la red neuronal) a desarrollar estrategias de navegación universales en lugar de memorizar un solo camino.
