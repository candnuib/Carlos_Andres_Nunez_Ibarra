#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador didáctico de datos sintéticos: edad, sexo -> estatura, peso

Este script crea un CSV con cuatro columnas: `age` (años), `sex` (M/F), `height` (cm) y `weight` (kg).

Uso básico:
    python3 data/generate_height_data.py --n 500 --out data/datos_ninos.csv --seed 42
"""

import argparse
import os

import numpy as np
import pandas as pd


def generate(n: int, seed: int = 42) -> pd.DataFrame:
        """Genera un DataFrame con `n` muestras de edad, sexo, estatura y peso.
        """
        rng = np.random.default_rng(seed)

        # 1) Generar edades en años (0 a 18)
        ages = rng.uniform(0, 18, size=n)

        # 2) Generar sexo (50% probabilidad de M o F)
        sexes = rng.choice(['M', 'F'], size=n)
        
        # Variable auxiliar: 1 si es M, 0 si es F (para hacer pequeños ajustes en la fórmula)
        is_male = (sexes == 'M').astype(int)

        # 3) Generar estaturas con relación no lineal + factor sexo + ruido
        # Añadimos un pequeño extra de altura (ej. 2 cm en promedio) si es niño, solo para 
        # que un modelo de Machine Learning tenga algo que aprender de la variable 'sex'.
        heights = 45 + 5.2 * ages + 0.08 * (ages ** 2) + (is_male * 2.0) + rng.normal(0, 3.0, size=n)

        # 4) Generar pesos (en kilogramos)
        # Un bebé nace pesando aprox 3 kg. Usamos una fórmula basada en la edad + ruido.
        weights = 3.0 + 2.2 * ages + 0.1 * (ages ** 2) + (is_male * 1.5) + rng.normal(0, 2.5, size=n)

        # 5) Empaquetar y redondear
        df = pd.DataFrame({
                "age": np.round(ages, 2),
                "sex": sexes,
                "height": np.round(heights, 2),
                "weight": np.round(weights, 2)
        })
        return df


def main() -> None:
        """Interfaz de línea de comandos."""
        p = argparse.ArgumentParser(description="Generador de datos sintéticos")
        p.add_argument("--n", type=int, default=500, help="Número de muestras")
        # Cambié el nombre por defecto del archivo para que refleje los nuevos datos
        p.add_argument("--out", type=str, default="data/datos_ninos.csv", help="Archivo CSV de salida")
        p.add_argument("--seed", type=int, default=42, help="Semilla aleatoria para reproducibilidad")
        args = p.parse_args()

        # Generar DataFrame
        df = generate(args.n, seed=args.seed)

        # Asegurarse de que la carpeta de salida exista
        out_dir = os.path.dirname(args.out) or "."
        os.makedirs(out_dir, exist_ok=True)

        # Guardar CSV sin índice
        df.to_csv(args.out, index=False)
        print(f"Generado {len(df)} muestras en {args.out}")


if __name__ == "__main__":
        main()
