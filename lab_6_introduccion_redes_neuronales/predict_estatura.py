#!/usr/bin/env python3
"""
Script de Inferencia: Usa el modelo entrenado para predecir la estatura
basada en edad, sexo y peso.
"""
import argparse
from pathlib import Path
import numpy as np
import torch
from torch import nn

# 1. Necesitamos definir la MISMA estructura de red que usamos para entrenar
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

def main():
    p = argparse.ArgumentParser(description="Predecir estatura con el modelo entrenado")
    
    # Argumentos para ingresar los datos del usuario
    p.add_argument("--edad", type=float, required=True, help="Edad en años (ej. 10.5)")
    p.add_argument("--sexo", type=str, required=True, choices=['M', 'F', 'm', 'f'], help="Sexo (M o F)")
    p.add_argument("--peso", type=float, required=True, help="Peso en kg (ej. 35.2)")
    
    # Ruta donde se guardó el modelo entrenado
    repo_root = Path(__file__).resolve().parent.parent
    default_model = str(repo_root / "models" / "estatura_model.pth")
    p.add_argument("--modelo", type=str, default=default_model, help="Ruta al archivo .pth")
    
    args = p.parse_args()

    # 2. Cargar el archivo .pth
    if not Path(args.modelo).exists():
        print(f"Error: No se encontró el modelo en {args.modelo}")
        print("Asegúrate de haber entrenado el modelo primero.")
        return

    print("Cargando modelo...")
    # weights_only=False es seguro aquí porque nosotros creamos el archivo
    checkpoint = torch.load(args.modelo, weights_only=False) 

    # 3. Restaurar la red y ponerla en modo "Evaluación"
    model = SimpleNet()
    model.load_state_dict(checkpoint["model_state"])
    model.eval() # IMPORTANTE: Le dice a PyTorch que no estamos entrenando

    # 4. Recuperar los valores de normalización
    x_mean = np.array(checkpoint["x_mean"], dtype=np.float32)
    x_std = np.array(checkpoint["x_std"], dtype=np.float32)

    # 5. Preparar los datos nuevos ingresados por el usuario
    sex_num = 1.0 if args.sexo.upper() == 'M' else 0.0
    
    # Crear un arreglo de Numpy con la forma [edad, sexo, peso]
    x_new = np.array([[args.edad, sex_num, args.peso]], dtype=np.float32)

    # Normalizar igual que en el entrenamiento: (X - media) / desviación
    x_norm = (x_new - x_mean) / x_std

    # Convertir a Tensor de PyTorch
    X_tensor = torch.from_numpy(x_norm)

    # 6. ¡Hacer la predicción!
    with torch.no_grad(): # No necesitamos calcular gradientes (ahorra memoria)
        prediccion = model(X_tensor)
        estatura_estimada = prediccion.item() # .item() saca el número del tensor

    print("\n" + "="*40)
    print("📋 DATOS INGRESADOS:")
    print(f"   Edad: {args.edad} años")
    print(f"   Sexo: {'Masculino' if sex_num == 1.0 else 'Femenino'}")
    print(f"   Peso: {args.peso} kg")
    print("-" * 40)
    print(f"🎯 ESTATURA PREDICHA: {estatura_estimada:.2f} cm")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
