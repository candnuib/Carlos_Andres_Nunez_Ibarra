Impacto de los Parámetros Libres en el Aprendizaje de una Red Neuronal

Geometrı́a del Espacio de Solución Teórico y Dinámica de Optimización

Red Neuronal de Demanda (red neuronal.py)

Para hacer funcionar el programa de ejemplo se tuvo que descargar lalibreria scikit-learn

from sklearn.model_selection import train_test_split
ModuleNotFoundError: No module named 'sklearn'

pip install scikit-learn

En el ejemplo al correr el programa, se ve a la salida informacion muy importante con respecto a los datos del .csv

<img width="647" height="290" alt="image" src="https://github.com/user-attachments/assets/7de0c8d6-d75a-4845-9a03-efbdc3591f28" />

<img width="592" height="421" alt="image" src="https://github.com/user-attachments/assets/da373e33-e231-402e-a500-6cd55d052274" />

Ahora con el .csv que descarge como ejemplo, la tarea era hacer este proceso para predecir un dato, lo primero que hice fue analizar los datos del .csv con el programa pasado, el cual te dice las columnad y el tipo de dato que hay en cada uno, asi encuentro los valores numericos para entrenar la red.

<img width="355" height="402" alt="image" src="https://github.com/user-attachments/assets/36484cbe-5bfd-45ad-b3e4-2a5d30239769" />

<img width="634" height="198" alt="image" src="https://github.com/user-attachments/assets/988713e4-b2dd-4946-bc1b-d957cf1eac88" />

<img width="511" height="380" alt="image" src="https://github.com/user-attachments/assets/65216e29-16fa-403d-bc58-4fb64edf1aca" />

Al encontrar que hay solo 3 valores numericos, se empezo entrenando con ellos, este fue el resultado.

<img width="604" height="300" alt="image" src="https://github.com/user-attachments/assets/2c2dcc04-00bd-4881-a3ac-671f3c768517" />

<img width="590" height="404" alt="image" src="https://github.com/user-attachments/assets/8ba6a687-c18a-4f91-8df8-b1aea4183b72" />

Error Absoluto Medio (MAE): 20.7 pedidos
* Interpretación: En promedio, las predicciones del modelo se desvían en +-21 unidades respecto al valor real de la demanda observada. Esto indica el margen de error operativo que tiene la red al intentar estimar las cantidades.

Coeficiente de Determinación ($R^2$): -0.007
* Interpretación: El modelo muestra un rendimiento débil, con un porcentaje de explicación del $-1\%$. Al ubicarse ligeramente por debajo de cero, el resultado demuestra que las variables de entrada seleccionadas no logran capturar un patrón predictivo útil, comportándose de manera muy similar o incluso inferior a una estrategia de predicción basada únicamente en el promedio histórico.

Al ser muy copas variables, decidi agregar otras mas, el problemas con estas es que son de texto, la ventaja es que son de si o no, utilice una funcion la cual las conviere a 0 o 1 y con esos datos lo volvi a entrenar.

Resultado:

<img width="647" height="284" alt="image" src="https://github.com/user-attachments/assets/243211bb-1094-47e7-9a9f-3344fc552397" />

<img width="589" height="411" alt="image" src="https://github.com/user-attachments/assets/896abaf4-0381-41f1-bfaa-7f87912d8842" />

Efecto contraproducente de la complejidad: Contrario a la suposición general de que incorporar más información mejora automáticamente el rendimiento, al añadir nuevas variables de entrada (como las de dos estados) el Coeficiente de Determinación ($R^2$) empeoró, descendiendo hasta un valor de -0.041.

Saturación por ruido: Al introducir características que no guardan una correlación matemática fuerte o directa con la variable objetivo, la red neuronal procesa información redundante o dispersa. Esto genera ruido estadístico que dificulta el aprendizaje de los pesos y reduce la capacidad de generalización del modelo.

Naturaleza de los datos: Este comportamiento confirma que el cuello de botella del modelo no radica en la falta de variables, sino en la naturaleza de los datos de comportamiento de compra analizados, los cuales carecen de un patrón predictivo estricto que permita estimar con precisión el gasto a partir de dichos atributos.

Ahora agrege la columna de genero, con la misma dinamica de convertir el valor de texto a valor numerico y ahora mejoro, por lo que concluyo que el genero si impacta directamente en la correlacion de los datos.

<img width="643" height="303" alt="image" src="https://github.com/user-attachments/assets/072be301-12fe-41d7-ac06-fdf419f0d3fb" />

<img width="579" height="412" alt="image" src="https://github.com/user-attachments/assets/18121b65-af69-40c9-83fb-513cd1b7b64d" />

Ahora solo deje valores numericos y agrege solo la variable de genero y el resutado mejoro drasticamente.

<img width="642" height="241" alt="image" src="https://github.com/user-attachments/assets/ce5ad265-52e3-44ad-aa2a-c0082b36be65" />

<img width="581" height="363" alt="image" src="https://github.com/user-attachments/assets/73bc9c1b-b9a0-4cbd-84aa-66e471afddcd" />

Hice la prueba de modificar las epocas a 200 y el entrenamiento empeoro.

Cuando aumentar las épocas hace que el modelo empeore, por lo general se debe a un problema de sobreajuste (overfitting): la red neuronal empieza a memorizar el ruido de los datos en lugar de aprender patrones reales.

<img width="592" height="105" alt="image" src="https://github.com/user-attachments/assets/748c804e-9d17-48ed-a989-d90dae47a712" />

Modifique la tasa de aprendizaje de 0.1 a 0.001

<img width="578" height="104" alt="image" src="https://github.com/user-attachments/assets/80ce5b1d-6ccc-44ad-b84a-5c36ee9ae79a" />

Grafique los datos de mi mejor prueba y se ve asi: con el programa graficar_aprendizaje.py

<img width="642" height="150" alt="image" src="https://github.com/user-attachments/assets/f95208dc-d8a6-44ff-8b1d-e6d246a24c9c" />


<img width="1961" height="1594" alt="curva_aprendizaje" src="https://github.com/user-attachments/assets/85912e8c-0569-41ef-a16b-bba991cca9b6" />
