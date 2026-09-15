Experimento guiado.

1. Antes de ejecutar, predice que variante llegara antes y cual conservara mas diversidad.

Yo creo que el que la opcion con mutacion + cruce

2. Ejecuta el modo comparativo con las semillas 7, 21 y 42.

python3 robot_obstaculos.py --semilla 7 --sin-pausa

<img width="730" height="106" alt="image" src="https://github.com/user-attachments/assets/725299af-bab2-4195-bc1e-0b987d74221c" />

python3 robot_obstaculos.py --semilla 21 --sin-pausa

<img width="722" height="104" alt="image" src="https://github.com/user-attachments/assets/f736fb56-7351-4f0b-8f53-8a45d33fe87a" />

python3 robot_obstaculos.py --semilla 42 --sin-pausa

<img width="727" height="100" alt="image" src="https://github.com/user-attachments/assets/9cddeeaf-9ed1-4857-898b-c21d00f58e9f" />


4. Compara los resultados de varias semillas. No uses una sola corrida para armar que un metodo
es mejor.

python3 robot_obstaculos.py --semilla 18 --sin-pausa

<img width="582" height="84" alt="image" src="https://github.com/user-attachments/assets/8677b0bb-1bdd-4977-9473-ffd87505b7a1" />

python3 robot_obstaculos.py --semilla 1 --sin-pausa 

<img width="585" height="83" alt="image" src="https://github.com/user-attachments/assets/ac130e61-294c-4f65-8c43-01a87c6ac40b" />

python3 robot_obstaculos.py --semilla 51 --sin-pausa

<img width="579" height="84" alt="image" src="https://github.com/user-attachments/assets/279de78a-31f2-42f4-a843-f23495b15ef0" />

5. Cambia una sola penalizacion del fitness y repite el experimento.

Aumente la penalizacion por visitas repetidas.

<img width="307" height="33" alt="image" src="https://github.com/user-attachments/assets/a91d5c9e-7830-49ca-8169-8b3082a1c6be" />

Resultados semilla 7 con modificacion:

<img width="610" height="79" alt="image" src="https://github.com/user-attachments/assets/89029fbe-ee00-4b91-bd37-8bd2f2a593d0" />

Resultados semilla 21 con modificacion:

<img width="581" height="88" alt="image" src="https://github.com/user-attachments/assets/2c6f5613-bb32-42b6-a64e-6d04bbf34a91" />

Resultados semilla 42 con modificacion:

<img width="581" height="85" alt="image" src="https://github.com/user-attachments/assets/d73405ca-f3a7-40bb-8ae5-8cb19c7f212f" />

1. Por que un robot cercano a la meta puede tener peor puntaje que otro mas lejano?

Porque fue penalizado a lo largo de su recorrido por las caracteristicas del fitness ya sea si choca o tiene visitas repetidas. ademas de que el que esta al inicio tiene sus puntos iniciales intactos.

2. Que ventaja aporta combinar dos padres en lugar de copiar uno solo?

Que se analizan dos rutas que lograron llegar a la meta, solo que se modifica casi la mitad de estos genes. Logrando la explotacion y exploracion.

4. La mayor diversidad final implica necesariamente una mejor solucion?

No necesariamente, pero si hay ma posibilidades de que en esa diversidad este la mejor solucion.

5. Que parte del programa representa el problema y que parte representa el algoritmo de
busqueda?

El problema esta en los obstaculos, ya que al chocar con ellos, se penaliza.
El algoritmo de busqueda esta en la mutacion y cruce. Logrando buscar nuevos caminos para solucionar el problema.

Reto modificacion:

1. Cambiar la posición de dos obstáculos
De qué trata: Modificar un par de coordenadas en la lista OBSTACULOS asegurándoce de no crear un muro cerrado que haga imposible llegar a la meta.

Enfoque: Se centra en el entorno. Lo interesante aquí es observar cómo el algoritmo se adapta a un laberinto distinto.

2. Modificar la longitud del ADN y explicar el efecto
De qué trata: Cambiar la variable LONGITUD_ADN (actualmente en 18) a un número mayor o menor, y analizar qué pasa.

Enfoque: Se centra en los límites del individuo. Si se acorta mucho, el robot físicamente no tendrá suficientes pasos para llegar (se quedará sin "gasolina"). Si se alarga demasiado (ej. 100 pasos), el espacio de combinaciones posibles crece tanto que al algoritmo le costará mucho más tiempo converger en una solución.

3. Implementar cruce uniforme (Uniform Crossover)
De qué trata: Modificar la función cruzar. Actualmente usa "cruce de un punto" (corta a los padres por la mitad y pega el inicio de uno con el final del otro). El cruce uniforme consiste en lanzar una moneda para cada gen (cada paso); así, el paso 1 puede ser del Padre A, el paso 2 del Padre B, el paso 3 del Padre B, el paso 4 del Padre A, etc.

Enfoque: Se centra en los operadores genéticos.

4. Cambiar una recompensa/penalización del fitness
De qué trata: Modificar los valores dentro de la función evaluar(adn). Por ejemplo, castigar los choques con -100 en lugar de -30, o premiar más dar pasos útiles.

Enfoque: Al cambiar estos valores se altera la "presión selectiva". Si se castigan demasiado los choques, los robots podrían volverse "miedosos" y preferir quedarse quietos en el inicio para no perder puntos. Se tienes que encontrar un equilibrio y justificar por qué el cambio funciona (o por qué hace que el algoritmo falle).

5. Registrar la mejor puntuación por generación y describir su evolución
De qué trata: El código ya guarda un historial de los puntos, pero tendrías que agregar código para imprimir una tabla, exportar un archivo CSV o hacer una gráfica simple en la terminal que muestre cómo va subiendo el puntaje generación tras generación.

Enfoque: Se centra en el análisis de datos. Se observa cómo la puntuación sube rapidísimo en las primeras generaciones y luego se estanca cuando encuentra el camino óptimo (convergencia).

Se selecciono el reto 5.

python3 robot_obstaculos_reto.py  --modo mutacion --sin-pausa

<img width="398" height="194" alt="image" src="https://github.com/user-attachments/assets/283dfbde-73a8-441c-b8f1-99cab64ce994" />

python3 robot_obstaculos_reto.py  --modo cruce --sin-pausa

<img width="409" height="164" alt="image" src="https://github.com/user-attachments/assets/1a469979-dd0c-48a2-ac78-5df92dd5b679" />

Semilla 7
<img width="397" height="191" alt="image" src="https://github.com/user-attachments/assets/bb90d872-685d-4b44-a333-605b8fd03668" />

semilla 7
<img width="416" height="177" alt="image" src="https://github.com/user-attachments/assets/64e38dc1-abd1-4024-8f9d-564e326b88fb" />



<img width="601" height="116" alt="image" src="https://github.com/user-attachments/assets/92969ffd-4a24-4138-b6c2-253fe7f7be15" />

tabla
<img width="595" height="109" alt="image" src="https://github.com/user-attachments/assets/e3aa472c-0ad3-4081-b2ab-239d99f008d4" />
