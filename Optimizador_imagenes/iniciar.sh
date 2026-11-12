#!/usr/bin/env bash
# Script para iniciar la aplicación Optimizador WebP

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar si el entorno virtual existe
if [ -d ".venv" ]; then
    PYTHON_EXEC=".venv/bin/python3"
else
    PYTHON_EXEC="python3"
fi

echo "Iniciando Optimizador de Imágenes WebP..."
"$PYTHON_EXEC" main.py
