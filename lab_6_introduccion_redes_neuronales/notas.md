PyTorch: predecir la estatura en niños a partir de su edad.
* Las redes neuronales aprenden relaciones no lineales entre variables.

Dataset sintético:
Archivo: data/estatura ninos.csv (columnas: age, height).
Tiene ∼500 muestras entre 0 y 18 años, generado con ruido para simular variabilidad real.

Modelo propuesto:
* Red neuronal pequeña: capas lineales + ReLU.
* Entrada: edad (normalizada), salida: estatura (cm).
* Pérdida: MSE. Optimizador: Adam.

Etrenamiento:
* División entrenamiento / prueba.
* Monitorizar pérdida y error medio absoluto (MAE).
* Guardar modelo y visualizar predicciones vs. reales.
