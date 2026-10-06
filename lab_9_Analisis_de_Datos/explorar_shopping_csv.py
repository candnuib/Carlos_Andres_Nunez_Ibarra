from pathlib import Path
import pandas as pd

def main():
    # 1. Cargar el archivo
    ruta_csv = Path(__file__).with_name("shopping_trends_updated.csv")
    
    # Nota: Si tu CSV tiene una columna de fecha exacta, puedes agregar parse_dates=["NombreColumnaFecha"]
    datos = pd.read_csv(ruta_csv)

    # 2. Exploración básica
    print("Muestra de datos:")
    print(datos.head(), end="\n\n")

    print(f"Dimensiones (filas, columnas): {datos.shape}")
    print("\nTipos de columnas:")
    print(datos.dtypes)

    print("\nValores faltantes por columna:")
    print(datos.isna().sum())

    # 3. Resumen estadístico
    print("\nResumen numerico:")
    columnas_numericas = datos.select_dtypes(include="number")
    print(columnas_numericas.describe())

    # 4. Limpieza y preparación
    # Asumimos que las columnas clave para el análisis financiero son el monto de compra y el artículo.
    # Ajusta "Purchase Amount (USD)" y "Item Purchased" si los nombres varían en tu CSV.
    datos_limpios = datos.dropna(
        subset=["Item Purchased", "Purchase Amount (USD)"]
    ).copy()

    # Si tuvieras unidades y precio por separado, aquí harías la multiplicación. 
    # Como este dataset suele tener el total en "Purchase Amount (USD)", podemos crear 
    # una columna de impuesto a modo de ejemplo de transformación:
    datos_limpios["Impuesto_Estimado"] = datos_limpios["Purchase Amount (USD)"] * 0.16

    print(f"\nFilas originales: {len(datos)}")
    print(f"Filas utilizables: {len(datos_limpios)}")

    # 5. Filtrado de datos (Ventas de alto valor)
    # Filtramos compras mayores a $80 USD (equivalente a tu filtro de importe >= 10)
    ventas_grandes = datos_limpios[datos_limpios["Purchase Amount (USD)"] >= 80]
    print("\nCompras con monto de $80 USD o más:")
    # Mostramos solo algunas columnas para que no se sature la pantalla
    columnas_mostrar = ["Item Purchased", "Category", "Purchase Amount (USD)"]
    print(ventas_grandes[columnas_mostrar].sort_values("Purchase Amount (USD)", ascending=False).head(10).to_string(index=False))

    # 6. Agrupaciones (Por Categoría)
    por_categoria = datos_limpios.groupby("Category").agg(
        ventas_totales=("Purchase Amount (USD)", "sum"),
        edad_promedio=("Age", "mean"),
        numero_registros=("Item Purchased", "count"),
    )
    por_categoria = por_categoria.sort_values(
        "ventas_totales", ascending=False
    )

    print("\nResumen por categoría:")
    print(por_categoria.to_string())

    # 7. Agrupaciones (Por Ciudad o Ubicación)
    # En este dataset la columna suele llamarse "Location"
    por_ciudad = datos_limpios.groupby("Location")["Purchase Amount (USD)"].sum()
    print("\nVentas totales por ubicación (Top 10):")
    print(por_ciudad.sort_values(ascending=False).head(10).to_string())

if __name__ == "__main__":
    main()
