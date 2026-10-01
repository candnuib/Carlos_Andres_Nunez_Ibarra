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

