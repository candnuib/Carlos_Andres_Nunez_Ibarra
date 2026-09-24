PyTorch: predecir la estatura en niños a partir de su edad.
* Las redes neuronales aprenden relaciones no lineales entre variables.

Dataset sintético:
Archivo: data/estatura ninos.csv (columnas: age, height).
Tiene ∼500 muestras entre 0 y 18 años, generado con ruido para simular variabilidad real.

<img width="131" height="364" alt="image" src="https://github.com/user-attachments/assets/2d84fa1c-da33-443b-bd67-9ce3b5e53d5e" />

Modelo propuesto:
* Red neuronal pequeña: capas lineales + ReLU.
* Entrada: edad (normalizada), salida: estatura (cm).
* Pérdida: MSE. Optimizador: Adam.

Etrenamiento:
* División entrenamiento / prueba.
* Monitorizar pérdida y error medio absoluto (MAE).
* Guardar modelo y visualizar predicciones vs. reales.
* 

Instalar dependencias:
pip install pandas numpy torch

Entrenar modeo:
python3 scripts/train_estatura.py --data data/estatura_ninos.csv --epochs 300

<img width="644" height="253" alt="image" src="https://github.com/user-attachments/assets/4108a206-1925-4576-9de5-c4e813e76128" />

Extencion de caracteristicas.

Para agregar sexo, el programa elije al azar entre "M" (Masculino) y "F" (Femenino) con un 50% de probabilidad para cada uno.

Para agregar peso, se usa una lógica similar a la de la estatura: crear una fórmula matemática que dependa de la edad ( hacer que varíe un poco dependiendo del sexo) y sumarle un "ruido" aleatorio para que se vea natural.

python3 data/generate_height_data_multiple.py --n 500 --out data/estatura_ninos.csv --seed 42

sexes = rng.choice(['M', 'F'], size=n): Esto crea una lista aleatoria de 'M' y 'F'.

is_male: Creamos una pequeña variable matemática que vale 1 si es niño y 0 si es niña. La usamos en las fórmulas de estatura y peso para agregarles un pequeñísimo incremento a los niños (simulando que estadísticamente hay una ligera diferencia). Esto es excelente si luego quieres entrenar un modelo de Inteligencia Artificial, porque el modelo intentará descubrir esa diferencia.

weights: Agregamos la fórmula de peso. Inicia en 3.0 kg (peso base de un bebé) y va subiendo conforme aumenta la edad, más un margen de error aleatorio de 2.5 kg (rng.normal(0, 2.5)) para que haya niños más delgados o más robustos de la misma edad.

<img width="216" height="367" alt="image" src="https://github.com/user-attachments/assets/fd1d53de-bfa8-468f-81dc-e8653baec4d4" />

Introducir regulacion y validacion cruzada:

<img width="647" height="235" alt="image" src="https://github.com/user-attachments/assets/11942b14-098e-4e91-81ca-e5507c51495e" />

