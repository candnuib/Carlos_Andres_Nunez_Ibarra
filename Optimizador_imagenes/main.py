#!/usr/bin/env python3
"""
Optimizador de Imágenes WebP para Web
Punto de entrada principal de la aplicación.
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gui.app import start_app

def main():
    try:
        start_app()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
