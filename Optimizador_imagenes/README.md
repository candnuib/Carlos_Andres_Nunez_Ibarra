# ⚡ Optimizador de Imágenes WebP para Web

Aplicación de escritorio desarrollada en Python diseñada específicamente para convertir, renombrar y comprimir imágenes masivamente al formato **WebP** con la mejor relación calidad/peso para páginas web.

---

## 🚀 Características Principales

1. **Optimización WebP de Alta Calidad**:
   - Compresión con el algoritmo más avanzado de WebP (`method 6`).
   - Control de calidad deslizable (por defecto 85%, el punto óptimo recomendado por Google).
   - Opción de compresión sin pérdidas (*Lossless*).
   - Reducción opcional de resolución máxima (ej. 1920x1080 px para web) manteniendo la proporción original.
   - Eliminación automática de metadatos pesados (*EXIF, GPS, cámara*) para aligerar la carga en páginas web.

2. **Nombres Personalizados y Formato de Ceros**:
   - **Nombre fijo**: Define un prefijo común (ej. `producto`, `foto_web`, `catalogo`). Si se deja vacío, conserva el nombre original.
   - **Cantidad de ceros configurable**: Permite elegir cuántos dígitos de relleno con ceros usar:
     - `1` dígito: `producto_1.webp`, `producto_2.webp`
     - `2` dígitos: `producto_01.webp`, `producto_02.webp`
     - `3` dígitos: `producto_001.webp`, `producto_002.webp`
     - `4` dígitos: `producto_0001.webp`, `producto_0002.webp`
   - **Número inicial**: Elige desde qué número empieza la secuencia (por ejemplo, desde 1 o desde 100).
   - **Vista previa en tiempo real**: Muestra inmediatamente cómo quedarán los archivos antes de procesarlos.

3. **Carpeta con Fecha Automática**:
   - Cada vez que procesas un paquete de imágenes, se genera automáticamente una nueva carpeta identificada con la fecha y hora:
     - Ejemplo: `WebP_Optimizadas_2026-11-09_10-05-30/`
   - Puedes usar la ubicación de las imágenes o elegir cualquier carpeta de destino personalizada.

4. **Interfaz Gráfica Intuitiva**:
   - Selección múltiple de archivos o carpetas completas.
   - Tabla con dimensiones originales, tamaño en KB/MB y estado en tiempo real.
   - Procesamiento en segundo plano (hilo independiente) sin que la interfaz se congele.
   - Ventana de estadísticas con ahorro total de peso y botón para abrir la carpeta directamente en el explorador de archivos.

---

## 📂 Estructura del Proyecto

```
Pruebas_antigravity/
├── core/
│   ├── converter.py           # Motor de compresión y procesamiento Pillow
│   └── naming.py              # Generación de nombres, ceros y carpetas fechadas
├── gui/
│   └── app.py                 # Interfaz gráfica moderna con Tkinter
├── main.py                    # Punto de entrada de la aplicación
├── iniciar.sh                 # Lanzador rápido para Linux (bash)
├── build.sh                   # Script para compilar el ejecutable en Linux
├── build_windows.bat          # Script para compilar el archivo .exe en Windows
├── requirements.txt           # Dependencias de Python
└── dist/
    └── OptimizadorWebP/       # Aplicación empaquetada como binario ejecutable
        └── OptimizadorWebP
```

---

## 💻 Formas de Ejecutar la Aplicación

### Opción 1: Ejecución directa con el script (Recomendada en Linux)
Simplemente ejecuta en la terminal o haz doble clic:
```bash
./iniciar.sh
```
O directamente con Python:
```bash
python3 main.py
```

### Opción 2: Usar el Ejecutable Binario Independiente (Linux)
Ya se encuentra compilado con PyInstaller dentro de la carpeta `dist`:
```bash
./dist/OptimizadorWebP/OptimizadorWebP
```

### Opción 3: Compilar el `.exe` para Windows
Si deseas ejecutar la aplicación en una computadora con Windows como archivo `.exe`:
1. Copia esta carpeta del proyecto a la máquina con Windows.
2. Abre la carpeta y haz doble clic sobre el archivo:
   ```cmd
   build_windows.bat
   ```
3. El archivo generado se creará en:
   ```
   dist\OptimizadorWebP\OptimizadorWebP.exe
   ```

---

## 📋 Formatos de Imagen Soportados

- JPEG / JPG / JFIF
- PNG (con transparencia completa)
- WebP
- BMP
- TIFF / TIF
- GIF (fotogramas estáticos)
- ICO
