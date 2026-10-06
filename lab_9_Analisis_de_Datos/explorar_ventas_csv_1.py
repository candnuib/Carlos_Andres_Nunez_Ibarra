from pathlib import Path
import pandas as pd

def main():
    ruta_csv = Path(__file__).with_name("ventas_sinteticas.csv")
    datos = pd.read_csv(ruta_csv, parse_dates=["fecha"])
    
    print("Muestra de datos:")
    print(datos.head(), end="\n\n")
    print(f"Dimensiones (filas, columnas): {datos.shape}")
    
    print("\nTipos de columnas:")
    print(datos.dtypes)
    
    print("\nValores faltantes por columna:")
    print(datos.isna().sum())
    
    print("\nResumen numerico:")
    columnas_numericas = datos.select_dtypes(include="number")
    print(columnas_numericas.describe())
    
    datos_limpios = datos.dropna(
        subset=["unidades", "precio_unitario"]
    ).copy()
    
    datos_limpios["importe"] = (
        datos_limpios["unidades"] * datos_limpios["precio_unitario"]
    )
    
    print(f"\nFilas originales: {len(datos)}")
    print(f"Filas utilizables: {len(datos_limpios)}")
    
    # 1. CAMBIO DE FILTRO: Filas con más de 4 unidades
    mas_de_4_unidades = datos_limpios[datos_limpios["unidades"] > 4]
    print("\nVentas con más de 4 unidades:")
    print(
        mas_de_4_unidades.sort_values("unidades", ascending=False).to_string(
            index=False
        )
    )
    
    # Resumen por categoría
    por_categoria = datos_limpios.groupby("categoria").agg(
        ventas_totales=("importe", "sum"),
        unidades_totales=("unidades", "sum"),
        numero_registros=("producto", "count"),
    )
    por_categoria = por_categoria.sort_values(
        "ventas_totales", ascending=False
    )
    print("\nResumen por categoria:")
    print(por_categoria.to_string())
    
    # 2. AGRUPACIÓN Y COMPARACIÓN POR CIUDAD
    por_ciudad = datos_limpios.groupby("ciudad").agg(
        ventas_totales=("importe", "sum"),
        unidades_totales=("unidades", "sum"),
        numero_registros=("producto", "count"),
    )
    por_ciudad = por_ciudad.sort_values("ventas_totales", ascending=False)
    print("\nComparación de importe total por ciudad:")
    print(por_ciudad.to_string())

if __name__ == "__main__":
    main()
