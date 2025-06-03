#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Seguimiento P2P Cripto - USDT
Autor: AI Assistant
Fecha: 2024

Este script realiza seguimiento de transacciones de compra y venta de USDT,
calcula P&L usando Costo Promedio Ponderado (CPP), y rastrea flujo de fiat.
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Tuple

class P2PTracker:
    BINANCE_FEE_UYU = 0.0016  # 0.16%
    BINANCE_FEE_USD = 0.0028  # 0.28%

    def __init__(self):
        # Inventario USDT
        self.inventario_usdt_cantidad = 0.0
        self.inventario_usdt_costo_total_usd = 0.0
        
        # Seguimiento de fiat
        self.fiat_tracker = {}  # {ID_Venta: {datos_fiat}}
        self.conversion_fiat_tracker = {}  # {ID_Conversion: {datos_conversion}}
        
        # DataFrames
        self.df_compras = None
        self.df_ventas = None
        self.df_conversiones = None
        
        # DataFrames con cálculos
        self.df_compras_calc = None
        self.df_ventas_calc = None
        
        # Transacciones combinadas ordenadas
        self.transacciones_ordenadas = []

    def cargar_datos(self, archivo_compras: str, archivo_ventas: str, archivo_conversiones: str = None):
        """Carga los datos desde archivos CSV"""
        print("🟡 Cargando datos...")
        
        try:
            # Cargar compras
            if os.path.exists(archivo_compras):
                self.df_compras = pd.read_csv(archivo_compras)
                self.df_compras['Fecha_Compra'] = pd.to_datetime(self.df_compras['Fecha_Compra'])
                if 'Plataforma' not in self.df_compras.columns:
                    self.df_compras['Plataforma'] = 'Otro' # Retrocompatibilidad
                self.df_compras['Plataforma'] = self.df_compras['Plataforma'].astype(str).str.lower()
                print(f"✅ Cargadas {len(self.df_compras)} compras")
            else:
                print(f"⚠️  Archivo de compras no encontrado: {archivo_compras}")
                self.df_compras = pd.DataFrame(columns=['ID_Compra', 'Fecha_Compra', 'Cantidad_USDT_Comprada', 'Moneda_Pago', 'Precio_Unitario_Moneda_Pago', 'Tasa_Cambio_UYU_USD_Compra', 'Fuente_De_Fondos_Fiat', 'Comisiones_Compra_Moneda_Pago', 'Plataforma']) # Asegurar que el df vacío tenga todas las columnas esperadas
            
            # Cargar ventas
            if os.path.exists(archivo_ventas):
                self.df_ventas = pd.read_csv(archivo_ventas)
                self.df_ventas['Fecha_Venta'] = pd.to_datetime(self.df_ventas['Fecha_Venta'])
                if 'Plataforma' not in self.df_ventas.columns:
                    self.df_ventas['Plataforma'] = 'Otro' # Retrocompatibilidad
                self.df_ventas['Plataforma'] = self.df_ventas['Plataforma'].astype(str).str.lower()
                print(f"✅ Cargadas {len(self.df_ventas)} ventas")
            else:
                print(f"⚠️  Archivo de ventas no encontrado: {archivo_ventas}")
                self.df_ventas = pd.DataFrame(columns=['ID_Venta', 'Fecha_Venta', 'Cantidad_USDT_Vendida', 'Moneda_Recibida', 'Precio_Unitario_Moneda_Recibida', 'Tasa_Cambio_UYU_USD_Venta', 'Comisiones_Venta_Moneda_Recibida', 'Plataforma']) # Asegurar que el df vacío tenga todas las columnas esperadas
            
            # Cargar conversiones (opcional)
            if archivo_conversiones and os.path.exists(archivo_conversiones):
                self.df_conversiones = pd.read_csv(archivo_conversiones)
                self.df_conversiones['Fecha_Conversion'] = pd.to_datetime(self.df_conversiones['Fecha_Conversion'])
                print(f"✅ Cargadas {len(self.df_conversiones)} conversiones de fiat")
            else:
                self.df_conversiones = pd.DataFrame()
                print("ℹ️  No se encontraron conversiones de fiat")
                
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            raise

    def calcular_preliminares_compras(self):
        """Calcula valores preliminares para las compras"""
        if self.df_compras.empty:
            self.df_compras_calc = pd.DataFrame(columns=list(self.df_compras.columns) + ['Costo_Total_Moneda_Pago', 'Costo_Total_en_USD', 'Costo_Adquisicion_Unitario_USD']) # Asegurar columnas incluso si está vacío inicialmente
            return
            
        print("🟡 Calculando preliminares de compras...")
        
        # Crear copia para cálculos
        self.df_compras_calc = self.df_compras.copy()
        
        # Asegurar que la columna Plataforma exista si df_compras_calc se creó a partir de un df_compras vacío pero con columnas definidas
        if 'Plataforma' not in self.df_compras_calc.columns:
            self.df_compras_calc['Plataforma'] = 'Otro'
        else:
            self.df_compras_calc['Plataforma'] = self.df_compras_calc['Plataforma'].astype(str).str.lower()

        # Rellenar comisiones NaN con 0 para el cálculo inicial
        self.df_compras_calc['Comisiones_Compra_Moneda_Pago'] = self.df_compras_calc['Comisiones_Compra_Moneda_Pago'].fillna(0)
        
        # Calcular comisiones de Binance si es necesario
        # Si la plataforma es Binance y la comisión manual es 0, se calcula automáticamente.
        def calcular_comision_compra(row):
            # Asegurarse que la plataforma no sea NaN o similar antes de .lower()
            plataforma_val = str(row['Plataforma']).lower() if pd.notna(row['Plataforma']) else 'otro'
            
            if plataforma_val == 'binance' and row['Comisiones_Compra_Moneda_Pago'] == 0:
                cantidad_usdt_comprada = row['Cantidad_USDT_Comprada']
                precio_unitario = row['Precio_Unitario_Moneda_Pago']
                tasa_comision_binance = 0
                
                if row['Moneda_Pago'] == 'UYU':
                    tasa_comision_binance = P2PTracker.BINANCE_FEE_UYU
                elif row['Moneda_Pago'] == 'USD':
                    tasa_comision_binance = P2PTracker.BINANCE_FEE_USD
                
                if tasa_comision_binance > 0:
                    comision_en_usdt = cantidad_usdt_comprada * tasa_comision_binance
                    valor_comision_en_moneda_pago = comision_en_usdt * precio_unitario
                    return valor_comision_en_moneda_pago
            return row['Comisiones_Compra_Moneda_Pago'] # Devuelve la original si no se calcula o no es Binance

        self.df_compras_calc['Comisiones_Compra_Moneda_Pago'] = self.df_compras_calc.apply(calcular_comision_compra, axis=1)
        
        # Costo total en moneda de pago
        self.df_compras_calc['Costo_Total_Moneda_Pago'] = (
            self.df_compras_calc['Cantidad_USDT_Comprada'] * 
            self.df_compras_calc['Precio_Unitario_Moneda_Pago'] + 
            self.df_compras_calc['Comisiones_Compra_Moneda_Pago']
        )
        
        # Costo total en USD
        self.df_compras_calc['Costo_Total_en_USD'] = self.df_compras_calc.apply(
            lambda row: row['Costo_Total_Moneda_Pago'] if row['Moneda_Pago'] == 'USD' 
            else row['Costo_Total_Moneda_Pago'] / row['Tasa_Cambio_UYU_USD_Compra'], 
            axis=1
        )
        
        # Costo de adquisición unitario en USD
        self.df_compras_calc['Costo_Adquisicion_Unitario_USD'] = (
            self.df_compras_calc['Costo_Total_en_USD'] / 
            self.df_compras_calc['Cantidad_USDT_Comprada']
        )
        
        print(f"✅ Preliminares de compras calculados")

    def calcular_preliminares_ventas(self):
        """Calcula valores preliminares para las ventas"""
        if self.df_ventas.empty:
            self.df_ventas_calc = pd.DataFrame(columns=list(self.df_ventas.columns) + ['Ingreso_Total_Moneda_Recibida', 'Ingreso_Neto_en_USD', 'Costo_Base_USD_de_USDT_Vendido', 'Ganancia_Perdida_USDT_en_USD'])
            return
            
        print("🟡 Calculando preliminares de ventas...")
        
        # Crear copia para cálculos
        self.df_ventas_calc = self.df_ventas.copy()

        if 'Plataforma' not in self.df_ventas_calc.columns:
            self.df_ventas_calc['Plataforma'] = 'Otro'
        else:
            self.df_ventas_calc['Plataforma'] = self.df_ventas_calc['Plataforma'].astype(str).str.lower()
        
        # Rellenar comisiones NaN con 0
        self.df_ventas_calc['Comisiones_Venta_Moneda_Recibida'] = self.df_ventas_calc['Comisiones_Venta_Moneda_Recibida'].fillna(0)

        # Calcular comisiones de Binance si es necesario
        # Si la plataforma es Binance y la comisión manual es 0, se calcula automáticamente.
        def calcular_comision_venta(row):
            plataforma_val = str(row['Plataforma']).lower() if pd.notna(row['Plataforma']) else 'otro'

            if plataforma_val == 'binance' and row['Comisiones_Venta_Moneda_Recibida'] == 0:
                cantidad_usdt_vendida = row['Cantidad_USDT_Vendida']
                precio_unitario = row['Precio_Unitario_Moneda_Recibida']
                tasa_comision_binance = 0
                
                if row['Moneda_Recibida'] == 'UYU':
                    tasa_comision_binance = P2PTracker.BINANCE_FEE_UYU
                elif row['Moneda_Recibida'] == 'USD':
                    tasa_comision_binance = P2PTracker.BINANCE_FEE_USD
                
                if tasa_comision_binance > 0:
                    comision_en_usdt = cantidad_usdt_vendida * tasa_comision_binance
                    valor_comision_en_moneda_recibida = comision_en_usdt * precio_unitario
                    return valor_comision_en_moneda_recibida
            return row['Comisiones_Venta_Moneda_Recibida'] # Devuelve la original si no se calcula o no es Binance

        self.df_ventas_calc['Comisiones_Venta_Moneda_Recibida'] = self.df_ventas_calc.apply(calcular_comision_venta, axis=1)

        # Ingreso total en moneda recibida
        self.df_ventas_calc['Ingreso_Total_Moneda_Recibida'] = (
            self.df_ventas_calc['Cantidad_USDT_Vendida'] * 
            self.df_ventas_calc['Precio_Unitario_Moneda_Recibida'] - 
            self.df_ventas_calc['Comisiones_Venta_Moneda_Recibida']
        )
        
        # Ingreso neto en USD
        self.df_ventas_calc['Ingreso_Neto_en_USD'] = self.df_ventas_calc.apply(
            lambda row: row['Ingreso_Total_Moneda_Recibida'] if row['Moneda_Recibida'] == 'USD' 
            else row['Ingreso_Total_Moneda_Recibida'] / row['Tasa_Cambio_UYU_USD_Venta'], 
            axis=1
        )
        
        # Inicializar columnas para cálculos posteriores
        self.df_ventas_calc['Costo_Base_USD_de_USDT_Vendido'] = 0.0
        self.df_ventas_calc['Ganancia_Perdida_USDT_en_USD'] = 0.0
        
        print(f"✅ Preliminares de ventas calculados")

    def crear_transacciones_ordenadas(self):
        """Crea una lista de transacciones ordenadas cronológicamente"""
        print("🟡 Ordenando transacciones cronológicamente...")
        
        transacciones = []
        
        # Agregar compras
        if not self.df_compras_calc.empty:
            for idx, row in self.df_compras_calc.iterrows():
                transacciones.append({
                    'fecha': row['Fecha_Compra'],
                    'tipo': 'compra',
                    'data': row,
                    'idx': idx
                })
        
        # Agregar ventas
        if not self.df_ventas_calc.empty:
            for idx, row in self.df_ventas_calc.iterrows():
                transacciones.append({
                    'fecha': row['Fecha_Venta'],
                    'tipo': 'venta',
                    'data': row,
                    'idx': idx
                })
        
        # Ordenar por fecha
        self.transacciones_ordenadas = sorted(transacciones, key=lambda x: x['fecha'])
        print(f"✅ {len(self.transacciones_ordenadas)} transacciones ordenadas")

    def procesar_cpp_y_pl(self):
        """Procesa todas las transacciones aplicando CPP y calculando P&L"""
        print("🟡 Procesando CPP y P&L...")
        
        for transaccion in self.transacciones_ordenadas:
            if transaccion['tipo'] == 'compra':
                self._procesar_compra(transaccion)
            elif transaccion['tipo'] == 'venta':
                self._procesar_venta(transaccion)
        
        print(f"✅ CPP y P&L procesados")

    def _procesar_compra(self, transaccion):
        """Procesa una compra individual"""
        data = transaccion['data']
        
        # Actualizar inventario
        self.inventario_usdt_cantidad += data['Cantidad_USDT_Comprada']
        self.inventario_usdt_costo_total_usd += data['Costo_Total_en_USD']
        
        # Rastrear fiat usado
        self._rastrear_fiat_usado_compra(data)
        
        print(f"📈 Compra procesada: {data['Cantidad_USDT_Comprada']} USDT")

    def _procesar_venta(self, transaccion):
        """Procesa una venta individual"""
        data = transaccion['data']
        idx = transaccion['idx']
        
        cantidad_vendida = data['Cantidad_USDT_Vendida']
        ingreso_neto_usd_venta = data['Ingreso_Neto_en_USD']

        # Añadir Costo_Promedio_Ponderado_USD al df_ventas_calc si no existe (para casos de venta sin stock)
        if 'Costo_Promedio_Ponderado_USD' not in self.df_ventas_calc.columns:
            self.df_ventas_calc['Costo_Promedio_Ponderado_USD'] = 0.0

        if self.inventario_usdt_cantidad == 0 or self.inventario_usdt_cantidad < cantidad_vendida:
            print(f"⚠️  Advertencia: Venta ID {data['ID_Venta']} de {cantidad_vendida} USDT. Stock insuficiente ({self.inventario_usdt_cantidad} USDT) en {data['Fecha_Venta']}. P&L no se calculará con CPP real.")
            # Se podría asignar un CPP de 0 o NaN, y el P&L sería simplemente el ingreso.
            self.df_ventas_calc.loc[idx, 'Costo_Base_USD_de_USDT_Vendido'] = 0 # O un valor que indique que no se pudo calcular
            self.df_ventas_calc.loc[idx, 'Ganancia_Perdida_USDT_en_USD'] = ingreso_neto_usd_venta # O NaN
            self.df_ventas_calc.loc[idx, 'Costo_Promedio_Ponderado_USD'] = 0.0 # O pd.NA
            # No se descuenta del inventario si no hay suficiente para cubrirlo completamente según CPP
            # O se podría optar por vender lo que hay y registrar el resto como una pérdida/problema.
            # Por ahora, la venta se registra, pero su P&L y efecto en CPP son problemáticos.
            self._rastrear_fiat_generado_venta(data, idx) # Rastrear fiat incluso si el P&L es problemático
            return
        
        # Calcular CPP actual
        cpp_actual = self.inventario_usdt_costo_total_usd / self.inventario_usdt_cantidad
        
        # Calcular costo base de USDT vendido
        costo_base_usd = cantidad_vendida * cpp_actual
        
        # Calcular ganancia/pérdida
        ganancia_perdida = ingreso_neto_usd_venta - costo_base_usd
        
        # Actualizar DataFrame de ventas
        self.df_ventas_calc.loc[idx, 'Costo_Base_USD_de_USDT_Vendido'] = costo_base_usd
        self.df_ventas_calc.loc[idx, 'Ganancia_Perdida_USDT_en_USD'] = ganancia_perdida
        self.df_ventas_calc.loc[idx, 'Costo_Promedio_Ponderado_USD'] = cpp_actual # Almacenar CPP usado para esta venta
        
        # Actualizar inventario
        self.inventario_usdt_costo_total_usd -= costo_base_usd
        self.inventario_usdt_cantidad -= cantidad_vendida
        
        # Rastrear fiat generado
        self._rastrear_fiat_generado_venta(data, idx)
        
        print(f"📉 Venta procesada: {data['Cantidad_USDT_Vendida']} USDT, P&L: ${ganancia_perdida:.2f}")

    def _rastrear_fiat_generado_venta(self, data, idx):
        """Rastrea el fiat generado por una venta"""
        id_venta = data['ID_Venta']
        
        self.fiat_tracker[id_venta] = {
            'Moneda_Generada': data['Moneda_Recibida'],
            'Monto_Neto_Generado_Moneda_Original': data['Ingreso_Total_Moneda_Recibida'],
            'Monto_Fiat_Utilizado_Moneda_Original': 0.0,
            'Monto_Fiat_Disponible_Moneda_Original': data['Ingreso_Total_Moneda_Recibida'],
            'Estado_Fiat': 'Disponible',
            'Fecha_Venta': data['Fecha_Venta']
        }

    def _rastrear_fiat_usado_compra(self, data):
        """Rastrea el uso de fiat en una compra"""
        fuente = data.get('Fuente_De_Fondos_Fiat', '')
        
        if fuente.startswith('Venta_ID_'):
            id_venta_ref = fuente.replace('Venta_ID_', '')
            if id_venta_ref in self.fiat_tracker:
                # Actualizar uso de fiat
                monto_usado = data['Costo_Total_Moneda_Pago']
                self.fiat_tracker[id_venta_ref]['Monto_Fiat_Utilizado_Moneda_Original'] += monto_usado
                self.fiat_tracker[id_venta_ref]['Monto_Fiat_Disponible_Moneda_Original'] -= monto_usado
                
                # Actualizar estado
                if self.fiat_tracker[id_venta_ref]['Monto_Fiat_Disponible_Moneda_Original'] <= 0:
                    self.fiat_tracker[id_venta_ref]['Estado_Fiat'] = 'Totalmente Usado'
                else:
                    self.fiat_tracker[id_venta_ref]['Estado_Fiat'] = 'Parcialmente Usado'

    def procesar_conversiones_fiat(self):
        """Procesa las conversiones de fiat"""
        if self.df_conversiones.empty:
            return
            
        print("🟡 Procesando conversiones de fiat...")
        
        for idx, row in self.df_conversiones.iterrows():
            id_conversion = row['ID_Conversion']
            id_venta_asociada_val = str(row.get('ID_Venta_Asociada', '')).strip()
            notas_val = str(row.get('Notas', '')).strip()
            
            # Registrar la conversión
            self.conversion_fiat_tracker[id_conversion] = {
                'Moneda_Origen': row['Moneda_Origen'],
                'Cantidad_Origen': row['Cantidad_Origen'],
                'Moneda_Destino': row['Moneda_Destino'],
                'Cantidad_Destino': row['Cantidad_Destino'],
                'Fecha_Conversion': row['Fecha_Conversion'],
                'ID_Venta_Asociada': id_venta_asociada_val,
                'Notas': notas_val
            }
            
            # Si proviene de una venta específica y el ID de venta es válido
            if id_venta_asociada_val and id_venta_asociada_val.upper() != 'N/A':
                if id_venta_asociada_val in self.fiat_tracker:
                    self.fiat_tracker[id_venta_asociada_val]['Estado_Fiat'] = 'Convertido'
                # else: # Opcional: advertir si el ID de venta asociado no se encuentra
                    # print(f"⚠️ Advertencia: ID de Venta Asociada '{id_venta_asociada_val}' para Conversión '{id_conversion}' no encontrado en fiat_tracker.")
        
        print(f"✅ {len(self.df_conversiones)} conversiones procesadas")

    def generar_reportes(self):
        """Genera los reportes CSV"""
        print("🟡 Generando reportes...")
        
        report_dir = '../data/reports/'
        os.makedirs(report_dir, exist_ok=True) # Asegurar que el directorio de reportes exista

        # Reporte de P&L de Ventas
        if self.df_ventas_calc is not None and not self.df_ventas_calc.empty:
            columnas_reporte_ventas = [
                'ID_Venta', 'Fecha_Venta', 'Cantidad_USDT_Vendida', 
                'Moneda_Recibida', 'Precio_Unitario_Moneda_Recibida', 'Tasa_Cambio_UYU_USD_Venta',
                'Ingreso_Total_Moneda_Recibida', 'Ingreso_Neto_en_USD', 
                'Costo_Promedio_Ponderado_USD', 'Costo_Base_USD_de_USDT_Vendido', 
                'Ganancia_Perdida_USDT_en_USD', 'Plataforma'
            ]
            
            # Asegurarse que todas las columnas existan, añadiendo las que falten con pd.NA
            df_reporte_ventas = self.df_ventas_calc.copy()
            for col in columnas_reporte_ventas:
                if col not in df_reporte_ventas.columns:
                    df_reporte_ventas[col] = pd.NA 
            
            filepath_ventas_pl = os.path.join(report_dir, 'reporte_ventas_pl.csv')
            try:
                df_reporte_ventas[columnas_reporte_ventas].to_csv(filepath_ventas_pl, index=False)
                print(f"✅ Reporte de P&L de ventas guardado en '{filepath_ventas_pl}'")
            except Exception as e:
                print(f"❌ Error guardando reporte P&L: {e}")
                print("Dataframe de ventas para reporte:")
                print(df_reporte_ventas[columnas_reporte_ventas].head())
                print("Columnas disponibles en df_reporte_ventas:", df_reporte_ventas.columns.tolist())

        else:
            print("ℹ️  No hay datos de ventas calculados para generar reporte de P&L.")

        # Reporte de Flujo de Fiat
        if self.fiat_tracker:
            df_flujo_fiat = pd.DataFrame.from_dict(self.fiat_tracker, orient='index')
            df_flujo_fiat.index.name = 'ID_Venta'
            if not df_flujo_fiat.empty:
                filepath_flujo_fiat = os.path.join(report_dir, 'reporte_flujo_fiat.csv')
                try:
                    df_flujo_fiat.to_csv(filepath_flujo_fiat, index=False)
                    print(f"✅ Reporte de flujo de fiat guardado en '{filepath_flujo_fiat}'")
                except Exception as e:
                    print(f"❌ Error guardando reporte de flujo de fiat: {e}")
            else:
                print("ℹ️  No hay datos de flujo de fiat para generar reporte.")
        else: # Añadido para el caso en que self.fiat_tracker esté vacío
            print("ℹ️  No hay datos en fiat_tracker para generar reporte de flujo de fiat.")
            
        print("✅ Reportes generados.")

def crear_archivos_ejemplo():
    """Crea archivos CSV de ejemplo si no existen."""
    print("🟡 Verificando archivos de ejemplo...")

    archivos_a_verificar = {
        '../data/compras_usdt.csv': {
            'columnas': ['ID_Compra', 'Fecha_Compra', 'Cantidad_USDT_Comprada', 'Moneda_Pago', 'Precio_Unitario_Moneda_Pago', 'Tasa_Cambio_UYU_USD_Compra', 'Fuente_De_Fondos_Fiat', 'Comisiones_Compra_Moneda_Pago', 'Plataforma'],
            'data': [
                ['C1', '2023-01-01 10:00:00', 100.0, 'UYU', 39.5, 39.5, 'Ahorros UYU', 0.0, 'binance'],
                ['C2', '2023-01-05 15:30:00', 50.0, 'USD', 1.01, 1.0, 'Ahorros USD', 0.0, 'otro'],
            ]
        },
        '../data/ventas_usdt.csv': {
            'columnas': ['ID_Venta', 'Fecha_Venta', 'Cantidad_USDT_Vendida', 'Moneda_Recibida', 'Precio_Unitario_Moneda_Recibida', 'Tasa_Cambio_UYU_USD_Venta', 'Comisiones_Venta_Moneda_Recibida', 'Plataforma'],
            'data': [
                ['V1', '2023-01-10 12:00:00', 70.0, 'UYU', 40.5, 40.0, 0.0, 'binance'],
            ]
        },
        '../data/conversiones_fiat.csv': {
            'columnas': ['ID_Conversion', 'Fecha_Conversion', 'Moneda_Origen', 'Cantidad_Origen', 'Moneda_Destino', 'Cantidad_Destino', 'ID_Venta_Asociada', 'Notas'],
            'data': [
                ['CF1', '2023-01-11 09:00:00', 'UYU', 2835.0, 'USD', 70.0, 'V1', 'Conversion de UYU de venta V1 a USD'],
            ]
        }
    }

    algun_archivo_creado = False
    for archivo_path, info in archivos_a_verificar.items():
        directorio = os.path.dirname(archivo_path)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"📂 Directorio creado: {directorio}")

        if not os.path.exists(archivo_path):
            print(f"⏳ Creando archivo de ejemplo: {archivo_path}")
            df_ejemplo = pd.DataFrame(info['data'], columns=info['columnas'])
            
            # Convertir columnas de fecha a datetime si es necesario y luego a string en formato ISO
            if 'Fecha_Compra' in df_ejemplo.columns:
                 df_ejemplo['Fecha_Compra'] = pd.to_datetime(df_ejemplo['Fecha_Compra']).dt.strftime('%Y-%m-%d %H:%M:%S')
            if 'Fecha_Venta' in df_ejemplo.columns:
                df_ejemplo['Fecha_Venta'] = pd.to_datetime(df_ejemplo['Fecha_Venta']).dt.strftime('%Y-%m-%d %H:%M:%S')
            if 'Fecha_Conversion' in df_ejemplo.columns:
                df_ejemplo['Fecha_Conversion'] = pd.to_datetime(df_ejemplo['Fecha_Conversion']).dt.strftime('%Y-%m-%d %H:%M:%S')

            df_ejemplo.to_csv(archivo_path, index=False)
            algun_archivo_creado = True
            print(f"✅ Archivo de ejemplo creado: {archivo_path}")
        else:
            print(f"ℹ️  Archivo encontrado: {archivo_path}")

    if algun_archivo_creado:
        print("✨ ¡Archivos CSV de ejemplo creados/verificados! Por favor, revísalos y modifícalos con tus datos reales.")
    else:
        print("✅ Todos los archivos de datos ya existen.")

def main():
    print("🚀 Iniciando P2P Tracker Script...")
    
    # Verificar y crear archivos de ejemplo si es necesario
    # Esto asegura que los directorios data/ y data/reports/ existan si son creados por primera vez aquí.
    crear_archivos_ejemplo()

    tracker = P2PTracker()
    
    # Cargar datos
    tracker.cargar_datos(
        archivo_compras='../data/compras_usdt.csv', 
        archivo_ventas='../data/ventas_usdt.csv', 
        archivo_conversiones='../data/conversiones_fiat.csv'
    )
    
    # Realizar cálculos
    tracker.calcular_preliminares_compras()
    tracker.calcular_preliminares_ventas()
    tracker.crear_transacciones_ordenadas()
    tracker.procesar_cpp_y_pl()
    tracker.procesar_conversiones_fiat()
    
    # Generar reportes
    tracker.generar_reportes()
    
    print(f"\n🎉 ¡Procesamiento completado exitosamente!")

if __name__ == "__main__":
    main() 