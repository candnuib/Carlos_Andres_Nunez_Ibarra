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
