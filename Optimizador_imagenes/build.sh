#!/usr/bin/env bash
# Script para empaquetar la aplicación en un ejecutable independiente con PyInstaller

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ -d ".venv" ]; then
    PYINSTALLER=".venv/bin/pyinstaller"
else
    PYINSTALLER="pyinstaller"
fi

echo "Compilando ejecutable con PyInstaller..."
"$PYINSTALLER" --noconfirm --onedir --windowed \
    --name "OptimizadorWebP" \
    --add-data "core:core" \
    --add-data "gui:gui" \
    main.py

echo "--------------------------------------------------------"
echo "¡Compilación exitosa!"
echo "El ejecutable se encuentra en: dist/OptimizadorWebP/OptimizadorWebP"
echo "--------------------------------------------------------"
