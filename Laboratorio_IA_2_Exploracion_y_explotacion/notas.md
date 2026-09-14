Experimento guiado.

Semilla 7:

python3 robot_exploracion_explotacion.py --modo exploracion --semilla 7

<img width="336" height="243" alt="image" src="https://github.com/user-attachments/assets/7f5a93c1-e2f6-4b2a-9654-c539d5924d67" />

python3 robot_exploracion_explotacion.py --modo explotacion --semilla 7

<img width="334" height="246" alt="image" src="https://github.com/user-attachments/assets/f7f2cc38-180c-4e13-b405-c812410af41c" />

Semilla 21:

python3 robot_exploracion_explotacion.py --modo exploracion --semilla 21

<img width="341" height="243" alt="image" src="https://github.com/user-attachments/assets/feca62c3-ae53-4beb-9e20-ccba984553f9" />

python3 robot_exploracion_explotacion.py --modo explotacion --semilla 21

<img width="339" height="245" alt="image" src="https://github.com/user-attachments/assets/adc41ce4-7be9-4a15-a70d-de1548e633d5" />

Semilla 42:

python3 robot_exploracion_explotacion.py --modo exploracion --semilla 42

<img width="346" height="241" alt="image" src="https://github.com/user-attachments/assets/f6fec003-8f9c-4fcc-9c35-de5e951a627c" />

python3 robot_exploracion_explotacion.py --modo explotacion --semilla 42

<img width="344" height="246" alt="image" src="https://github.com/user-attachments/assets/0a0ab5e7-7c9f-44f5-aa22-307bd9c194f6" />

Modificación a la tasa de mutacion.

<img width="373" height="82" alt="image" src="https://github.com/user-attachments/assets/482e73b3-5178-43dc-bf2b-a0df79dcd1a2" />

En este caso aumente la taza por lo tanto en mi predicción creo que el valor de diversidad aumentara notablemente en comparación a anteriores pruebas.

python3 robot_exploracion_explotacion.py --modo exploracion --semilla 42

<img width="344" height="244" alt="image" src="https://github.com/user-attachments/assets/a523d53f-a3e5-4cde-8c6a-01c06397972b" />

python3 robot_exploracion_explotacion.py --modo explotacion --semilla 42

<img width="337" height="248" alt="image" src="https://github.com/user-attachments/assets/0773b0df-476e-40b8-8cf8-ed40dae253ab" />

Al finalizar las pruebas, mi predicción con respecto al comportamiento fue acertada: la diversidad aumentó. Esto se debe a que aumenté la probabilidad de mutación en ambos escenarios (exploración y explotación). Sin hacer una prueba, puedo concluir que si yo bajo esa probabilidad, la diversidad será menor.

Respondiendo a las preguntas:

1. ¿Qué modo conserva más ADN diferente? ¿Por qué eso representa exploración?

El modo que conserva más ADN diferente es el de exploración. Esto es así porque la exploración busca mutar la mayor parte del ADN (el porcentaje de probabilidad de cambio es mayor), logrando así buscar nuevas y distintas soluciones, "mirando fuera de la caja".

2. ¿Una mayor diversidad garantiza llegar antes a la meta?

Literalmente no, pero sí es fundamental tener una diversidad para encontrar distintos caminos, teniendo la posibilidad de encontrar uno mejor. Para garantizar llegar antes a la meta se utiliza la explotación, la cual, en el pequeño rango de modificación que tiene, busca su mejor versión.

3. ¿Qué ocurre si la mutación es casi cero? ¿Y si se acerca a uno?

Si es casi cero, entonces el ADN no cambiará para nada y no habrá diversidad. En cambio, si esta mutación se acerca a uno, la diversidad será grandísima, ya que se perderán casi por completo las características anteriores.

4. ¿El fitness actual premia siempre el camino más corto? Propón una modificación y justifica su presión selectiva.

El fitness actual premia cuando se encuentra en una posición más cercana a la meta; por lo tanto, al mutar y mejorar, buscará una mayor premiación logrando encontrar el camino más corto o eficiente. Sí, propone una modificación buscando tener más recompensas.

Reto de modificacion.

Análisis actual:

Algoritmo Genético clásico aplicado a un problema de pathfinding (búsqueda de rutas). Tienes un tamaño de ADN fijo (14 pasos), una meta en la esquina opuesta y dos escenarios extremos: explorar mucho (mutación alta) o explotar lo conocido (mutación baja).

Análisis  para cada reto:

1. Agregar un obstáculo y penalizar las trayectorias que lo visiten
¿De qué trata? Imagina poner una "pared" o un "pozo" en medio del mapa (hecho en un previo ejemplo, en la coordenada (4,4)). Si un robot pasa por ahí, su puntaje (fitness) cae drásticamente casi matandolo.

El reto conceptual: Esto crea lo que en IA se llama un "mínimo local". Un robot que iba directo a la meta de repente se estrella. El algoritmo tendrá que aprender a rodearlo.

¿A quién afecta más? La explotación (baja mutación) podría quedarse atascada chocando con el obstáculo, porque le cuesta generar los múltiples cambios necesarios para rodearlo. La exploración podría rodearlo más fácil, pero le costaría mantener esa ruta sin arruinarla en la siguiente generación.

Veredicto: Es muy visual y divertido de ver en la terminal. Modifica el entorno.

2. Cambiar la meta y explicar si las dos presiones siguen encontrándola
¿De qué trata? Mover la meta de (7,7) a, digamos, (0,7) (arriba a la derecha) o (3,3) (casi en el centro).

El reto conceptual: El ADN de los robots tiene 14 comandos fijos. Si se mueve la meta a (3,3), el camino óptimo requiere solo 6 pasos. ¿Qué harán los robots en los 8 pasos restantes? ¡Se saldrán de la meta!

¿A quién afecta más? La función de evaluación actual premia llegar a la meta, pero también castiga quedarse quieto o repetir casillas. Cambiar la meta revelará si el algoritmo puede obligar al robot a "chocar contra una pared" a propósito para no alejarse de la meta, o si terminará bailando alrededor de ella.

Veredicto: Es la opción que menos código requiere, pero la que exige mayor análisis analítico e interpretación.

3. Agregar un costo por cada paso para favorecer rutas eficientes
¿De qué trata? Actualmente, si el robot llega a la meta, recibe sus puntos sin importar si llegó directo o si dio vueltas innecesarias (aunque penalizas un poco las visitas repetidas). Aquí, cada movimiento "gastaría energía".

El reto conceptual: Se trata de optimización pura. Se tendria que modificar la evaluación para que el robot se detenga al tocar la meta y cuente cuántos pasos usó, dándole un bono gigante a los que usaron menos pasos.

Veredicto: Es una aproximación muy realista a problemas de la vida real (como ahorrar gasolina o batería). Modifica la función de evaluación (fitness).

4. Tasa de mutación dinámica (Exploración al principio, explotación al final)
¿De qué trata? En lugar de tener una tasa fija de 0.50 (caos) o 0.05 (estancamiento), se empieza con una mutación alta. Conforme pasan las generaciones (o conforme mejora el puntaje), la mutación va bajando lentamente hasta llegar casi a cero.

El reto conceptual: Esto imita un concepto avanzado llamado Simulated Annealing (Recocido Simulado). Permite que el algoritmo mire "fuera de la caja" al principio para encontrar la ruta general, y luego se vuelva "perfeccionista" al final para no arruinar el buen camino encontrado.

Veredicto: Es la opción más enriquecedora a nivel de Diseño de Algoritmos de IA. Se obtiene "lo mejor de los dos mundos" y suele dar resultados increíblemente superiores. Modifica el "cerebro" (mecanismo evolutivo) del algoritmo.

Pruebas con el reto 4:

<img width="495" height="372" alt="image" src="https://github.com/user-attachments/assets/33671e67-dd3b-4420-ad82-4765442abaa8" />

Análisis de los Resultados
Explotación (Ganó en velocidad, falló en diversidad): Llegó a la meta en solo 7 generaciones. Al tener una mutación tan baja (0.05), en cuanto encontró un camino decente, lo explotó al máximo. Sin embargo, la diversidad final se desplomó a 37/80. Convergió prematuramente. En un entorno sin obstáculos esto funciona rápido, pero en un problema complejo, esta pérdida de diversidad genética lo haría estancarse en un mínimo local.

Exploración (Lenta pero dispersa): Tardó 27 generaciones. Con una tasa fija de 0.50, el algoritmo es demasiado caótico; literalmente destruye sus propias soluciones buenas antes de poder pulirlas, por lo que le cuesta mucho más "estabilizarse" sobre la meta.

Dinámico (El equilibrio perfecto): Resolvió el problema en 18 generaciones, pero el dato clave aquí es su diversidad final: 80/80. Al iniciar con una mutación altísima (0.60), esparció a los individuos por todo el espacio de búsqueda. Conforme se acercó a la meta y la tasa bajó, permitió pulir el camino sin matar la variedad de la población. Lograste optimizar la ruta manteniendo una capacidad de adaptación total.

Decidi volver a los parametros iniciales de 0.30 y 0.03. Probando este modelo con 3 distintas semillas:

python3 robot_exploracion_explotacion_reto.py --semilla 7

<img width="480" height="376" alt="image" src="https://github.com/user-attachments/assets/eff52392-3909-4499-92c4-c94ec5b764f2" />

python3 robot_exploracion_explotacion_reto.py --semilla 21

<img width="485" height="373" alt="image" src="https://github.com/user-attachments/assets/4a1c3843-0297-483e-b5f9-443347b8d259" />

python3 robot_exploracion_explotacion_reto.py --semilla 42

<img width="491" height="367" alt="image" src="https://github.com/user-attachments/assets/1cc10de2-38ae-4990-bf13-794d7222f7be" />

Conclusión:

"Al evaluar el algoritmo con múltiples semillas, se demostró que el desempeño de las estrategias depende fuertemente de la aleatoriedad inicial, habiendo casos (como la semilla 21) donde convergen al mismo tiempo. Sin embargo, el comportamiento consistente radica en la diversidad genética.
La estrategia de explotación es rápida pero sufre de convergencia prematura (su diversidad colapsa, acercándose a 1/80, creando clones). Por su parte, la estrategia dinámica logra resolver el laberinto manteniendo una diversidad máxima (80/80, individuos únicos). Aunque el modo dinámico puede tardar más generaciones en estabilizarse debido a su alto caos inicial, garantiza una exploración profunda del espacio de búsqueda sin quedarse atrapado en mínimos locales, consolidándose como la estrategia más robusta."
