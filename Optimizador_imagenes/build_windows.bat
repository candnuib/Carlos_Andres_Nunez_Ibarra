@echo off
REM Script para compilar el ejecutable .exe en Windows con PyInstaller
echo Compilando OptimizadorWebP.exe para Windows...

python -m pip install -r requirements.txt
pyinstaller --noconfirm --onedir --windowed --name "OptimizadorWebP" --add-data "core;core" --add-data "gui;gui" main.py

echo.
echo --------------------------------------------------------
echo Compilacion finalizada.
echo El ejecutable se encuentra en: dist\OptimizadorWebP\OptimizadorWebP.exe
echo --------------------------------------------------------
pause
