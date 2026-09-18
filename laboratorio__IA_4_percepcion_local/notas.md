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

Reto de modificacion.

Documentación de los Efectos_
1. Efecto de agregar la dirección de la meta a la observación
* Antes: El robot navegaba a ciegas buscando patrones locales. Era como intentar salir de un bosque espeso mirando solo a un metro de distancia.
* Ahora: Al agregar el cuadrante de la meta (2 bits extra), dotamos al robot de una brújula o "gradiente global".
* Efecto: El entrenamiento converge mucho más rápido a la meta. El robot aprende fácilmente heurísticas lógicas como: "Si el frente está libre y la meta está abajo a la derecha, muévete a la derecha o abajo". Esto disminuye radicalmente las caminatas aleatorias y reduce el "sobreajuste", ya que el algoritmo depende del instinto direccional en vez de memorizar celdas.

2. Efecto de incorporar la memoria de la última acción
* Antes: La percepción del entorno era un Autómata Finito sin memoria temporal. Si el robot entraba en una esquina sin salida y su regla para esa esquina era "Derecha", y la celda a la derecha le devolvía el estado idéntico con la regla "Izquierda", se quedaba rebotando indefinidamente.
* Ahora: El estado actual sabe "de dónde viene" (ej. Sensores=Esquina, Memoria=Venir de Arriba).
* Efecto: Permite romper la simetría temporal. El robot puede aprender reglas como: "Si estoy en un pasillo libre y vengo de la Izquierda, sigue a la Derecha. Pero si vengo de la Derecha, sigue a la Izquierda". Elimina drásticamente el tartamudeo (rebotar entre dos celdas contiguas).

3. Explicación de los ciclos al cambiar el número máximo de pasos (de 18 a 40)
* Antes: Con 18 pasos (en un camino mínimo de 14), el robot apenas tenía tiempo de desviar su trayectoria. Si había un ciclo, el algoritmo detenía la simulación prematuramente y cortaba el ciclo antes de que se notara.
* Ahora: Al elevar los pasos a 40, le damos tiempo suficiente al robot para cometer errores, rodear grandes obstáculos, y, si la política no es buena, entrar en macro-ciclos.
* Los ciclos observados: Gracias a la memoria temporal añadida, ya no vemos micro-ciclos de 2 pasos (A -> B -> A). Lo que se observa ahora (durante el entrenamiento de políticas imperfectas) son ciclos amplios (A -> B -> C -> D -> A), como rodear un bloque 2x2. Estos ciclos ocurren porque, eventualmente, el robot agota las combinaciones temporales en una región libre sin información local que lo guíe de manera distinta, y las reglas codificadas cierran un bucle (ej. la brújula apunta al Sur, pero un obstáculo enorme en U lo hace rodear perpetuamente hacia la izquierda).

4. Comparativa de la misma política en una segunda distribución de obstáculos
* En el código original: Una política que lograba llegar a la meta memorizaba el patrón exacto de paredes de ese mapa en particular. Al llevarla a un mapa distinto, fallaba espectacularmente en los primeros 5 pasos.
* Con estas modificaciones: Al evaluar el mismo ADN entrenado en el MAPA 1 dentro del MAPA 2, la supervivencia mejora notablemente. El robot no solo avanza en la dirección general correcta (gracias al sensor de meta), sino que es capaz de bordear obstáculos básicos que no había visto antes (gracias a la combinación de sensores y memoria).
* Conclusión de la prueba: La política ha evolucionado de un memorizador de rutas a un solucionador heurístico reactivo. Aunque todavía puede atascarse en callejones en forma de "U" muy profundos en el MAPA 2 (debido a su falta de mapeo espacial o memoria profunda), ahora es una política generalizable que puede resolver múltiples configuraciones sencillas con un único genoma.

