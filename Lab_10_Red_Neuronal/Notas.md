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
