Experimento guiado:
1. Ejecuta el modo comparativo con las semillas 7, 21 y 42.
2. Registra llegada, generaciones, puntaje, choques o intentos bloqueados, pasos utiles y diversidad.
3. Observa si la politica llega a la meta o repite un ciclo.
4. Compara mutacion y cruce con el mismo presupuesto de generaciones.
5. Cambia una sola penalizacion del fitness y repite una semilla.

python3 robot_percepcion.py --no-guardar --semilla 7 --sin-pausa

<img width="574" height="112" alt="image" src="https://github.com/user-attachments/assets/452eea5f-57e9-46fc-8ba4-af5d87e17c6e" />

python3 robot_percepcion.py --no-guardar --semilla 21 --sin-pausa

<img width="579" height="112" alt="image" src="https://github.com/user-attachments/assets/279991b9-641b-4978-a72a-ec7caeb9fbbe" />

python3 robot_percepcion.py --no-guardar --semilla 42 --sin-pausa

<img width="576" height="110" alt="image" src="https://github.com/user-attachments/assets/b4a32dd4-2544-4e97-969a-ad1602a3c716" />

Hice la prueba con la semilla 42 de quitarle el no guardar y me genero dos archivos.

<img width="450" height="73" alt="image" src="https://github.com/user-attachments/assets/8de90a1a-bc77-48c0-8e0e-8d8077695634" />

Dentro del archivo pude analiar y ver cada corrida, y en muchos casos ocurre que vuelve.

Para el punto 5, modifique el fitness penalizando cuando hace visitas repetidas.

<img width="288" height="25" alt="image" src="https://github.com/user-attachments/assets/0387dd3f-3523-4e1a-b928-8d8fb1073631" />

Al volver a correr la semilla 42 dio como resultado:

<img width="584" height="103" alt="image" src="https://github.com/user-attachments/assets/1c497c98-d102-472a-be4e-db97c1768743" />

1. Que diferencia hay entre evolucionar una ruta y evolucionar una politica?

Evolucionar una ruta significa buscar una secuencia fija e inalterable de movimientos (por ejemplo: Arriba, Derecha, Derecha, Abajo). Es un plan ciego que el robot recibe antes de empezar y solo funciona si el robot parte de un inicio específico y el mapa nunca cambia. No podiendo modificarlo en el recorrido.
 
Evolucionar una política significa buscar un conjunto de reglas de comportamiento. El robot no memoriza un camino, sino que aprende qué hacer frente a cada estímulo local (por ejemplo: "Si hay un obstáculo arriba y a la izquierda, muévete a la derecha"). La siguiente accion depende de lo que el robot observa en el momento.

2. Por que una politica local puede entrar en un ciclo?

El robot toma decisiones basándose exclusivamente en su percepción inmediata (su observación de 4 bits). Carece de memoria sobre las celdas que ya visitó. Si el robot llega a una posición, ejecuta una acción, y esa acción lo lleva de vuelta a un estado sensorial idéntico que dispara la acción opuesta, se quedará rebotando o atrapado en un bucle infinito entre las mismas celdas (razón por la cual el código implementa un límite de PASOS_MAXIMOS y penaliza las visitas_repetidas en la función de fitness).

3. Que informacion pierde el robot al no conocer su posicion exacta?

Al carecer de coordenadas exactas, el robot pierde por completo el contexto global:
* Dirección y distancia a la meta: No sabe hacia dónde avanzar para acercarse al objetivo, operando únicamente por "instinto" local.
* Historial de navegación: No sabe dónde ha estado, lo que le impide reconocer si está caminando en círculos.
* Mapa general: No puede anticipar callejones sin salida que estén más allá de la celda adyacente que perciben sus sensores.

4. El cruce combina rutas completas o reglas de percepcion? Que efecto puede tener?

La función cruzar combina reglas de percepción, no rutas completas. Intercambia fragmentos del ADN de longitud 16 entre dos padres.
* Efecto positivo: Puede crear un individuo superior combinando buenos "reflejos" de ambos. Un padre podría tener la regla perfecta para avanzar en     espacios abiertos, mientras que el otro tiene la regla perfecta para bordear esquinas.
* Efecto negativo: Puede ser destructivo. Romper el ADN a la mitad puede separar un conjunto de reglas que dependían unas de otras para maniobrar       alrededor de una estructura de obstáculos compleja, produciendo un hijo que se atasca fácilmente. Tomando las caracteristicas negativas de los        padres.

5. Una politica que funciona en este mapa funcionaria necesariamente en otro mapa?

No necesariamente funcionaría. Debido a que la función evaluar(adn) prueba a los individuos única y exclusivamente en el entorno definido por INICIO, META y OBSTACULOS, el algoritmo genético es muy propenso a sufrir de sobreajuste (overfitting).
La política ganadora probablemente no aprendió a "navegar laberintos en general", sino que evolucionó las respuestas exactas para las situaciones visuales locales en el orden específico que requiere este mapa en particular. En un mapa nuevo, el robot podría encontrarse con configuraciones sensoriales para las cuales su política tiene acciones subóptimas o que generan bucles.

