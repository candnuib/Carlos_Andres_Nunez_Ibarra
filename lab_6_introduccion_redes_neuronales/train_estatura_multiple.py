#!/usr/bin/env python3
"""
Entrenamiento en PyTorch para predecir estatura a partir de edad, sexo y peso.
"""
from __future__ import annotations
import argparse
import os
from typing import Tuple
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split

class SimpleNet(nn.Module):
    """Red neuronal simple para regresión (3 entradas -> 1 salida)."""
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


def load_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {p}")
    df = pd.read_csv(p)
    
    # Convertimos 'M' a 1 y 'F' a 0
    df["sex_num"] = (df["sex"] == "M").astype(np.float32)
    
    # Extraemos las 3 características como entrada X
    x = df[["age", "sex_num", "weight"]].values.astype(np.float32)
    
    # Mantenemos height como variable objetivo a predecir Y
    y = df[["height"]].values.astype(np.float32)
    
    return x, y


def main() -> None:
    p = argparse.ArgumentParser(description="Entrena red con edad, sexo, peso -> estatura")
    repo_root = Path(__file__).resolve().parent.parent
    
    # Por defecto apuntamos al archivo NUEVO con múltiples variables
    default_data = str(repo_root / "data" / "datos_ninos.csv")
    default_out = str(repo_root / "models" / "estatura_model.pth")
    
    p.add_argument("--data", type=str, default=default_data)
    p.add_argument("--epochs", type=int, default=300)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--out", type=str, default=default_out)
    args = p.parse_args()

    # 1) Cargar datos
    x, y = load_data(args.data)

    # 2) Normalizar la entrada (z-score)
    x_mean, x_std = x.mean(axis=0), x.std(axis=0) + 1e-8
    x_norm = (x - x_mean) / x_std

    # Convertir a tensores
    X = torch.from_numpy(x_norm)
    Y = torch.from_numpy(y)

    # 3) Preparar dataset y dividir 80/20
    dataset = TensorDataset(X, Y)
    n_test = int(0.2 * len(dataset))
    n_train = len(dataset) - n_test
    train_set, test_set = random_split(dataset, [n_train, n_test])

    train_loader = DataLoader(train_set, batch_size=args.batch, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=args.batch)

    # 4) Configurar dispositivo
    device = torch.device("cpu")
    model = SimpleNet().to(device)

    # 5) Optimizador y pérdida
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.MSELoss()

    # 6) Bucle de entrenamiento
    for epoch in range(1, args.epochs + 1):
        model.train()
        running = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running += loss.item() * xb.size(0)
        train_loss = running / n_train

        # 7) Evaluación
        if epoch % 50 == 0 or epoch == 1:
            model.eval()
            with torch.no_grad():
                test_losses = []
                maes = []
                for xb, yb in test_loader:
                    xb, yb = xb.to(device), yb.to(device)
                    pred = model(xb)
                    test_losses.append(criterion(pred, yb).item() * xb.size(0))
                    maes.append(torch.abs(pred - yb).mean().item() * xb.size(0))
                test_loss = sum(test_losses) / n_test
                mae = sum(maes) / n_test
            print(f"Epoch {epoch:03d}  Train MSE: {train_loss:.4f}  Test MSE: {test_loss:.4f}  Test MAE: {mae:.4f}")

    # 8) Guardar modelo
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "x_mean": x_mean.tolist(),
        "x_std": x_std.tolist(),
    }, args.out)
    print(f"Modelo guardado en {args.out}")

if __name__ == "__main__":
    main()
