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

<img width="131" height="364" alt="image" src="https://github.com/user-attachments/assets/776fa83b-ee69-4e3c-93ee-776bc1483e62" />

