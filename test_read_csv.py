import pandas as pd
import os

print(f"Directorio actual: {os.getcwd()}")

compras_path = 'data/compras_usdt.csv'
ventas_path = 'data/ventas_usdt.csv'
conversiones_path = 'data/conversiones_fiat.csv'

print(f"\n--- LEYENDO COMPRAS ({compras_path}) ---")
if os.path.exists(compras_path):
    try:
        df_compras = pd.read_csv(compras_path)
        print(f"Columnas: {df_compras.columns.tolist()}")
        print(f"Primeras 5 filas:\n{df_compras.head().to_string()}")
        print(f"Total filas: {len(df_compras)}")
        print(f"Total USDT Comprado: {df_compras['Cantidad_USDT_Comprada'].sum() if 'Cantidad_USDT_Comprada' in df_compras.columns else 'Columna no encontrada'}")
    except Exception as e:
        print(f"Error leyendo compras: {e}")
else:
    print("Archivo de compras NO ENCONTRADO.")

print(f"\n--- LEYENDO VENTAS ({ventas_path}) ---")
if os.path.exists(ventas_path):
    try:
        df_ventas = pd.read_csv(ventas_path)
        print(f"Columnas: {df_ventas.columns.tolist()}")
        print(f"Primeras 5 filas:\n{df_ventas.head().to_string()}")
        print(f"Total filas: {len(df_ventas)}")
        print(f"Total USDT Vendido: {df_ventas['Cantidad_USDT_Vendida'].sum() if 'Cantidad_USDT_Vendida' in df_ventas.columns else 'Columna no encontrada'}")
    except Exception as e:
        print(f"Error leyendo ventas: {e}")
else:
    print("Archivo de ventas NO ENCONTRADO.")

print(f"\n--- LEYENDO CONVERSIONES ({conversiones_path}) ---")
if os.path.exists(conversiones_path):
    try:
        df_conversiones = pd.read_csv(conversiones_path)
        print(f"Columnas: {df_conversiones.columns.tolist()}")
        print(f"Primeras 5 filas:\n{df_conversiones.head().to_string()}")
        print(f"Total filas: {len(df_conversiones)}")
    except Exception as e:
        print(f"Error leyendo conversiones: {e}")
else:
    print("Archivo de conversiones NO ENCONTRADO.")
