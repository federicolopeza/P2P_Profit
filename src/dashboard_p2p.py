#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard P2P Cripto - USDT (Dashboard P2P Interactivo)
Autor: AI Assistant
Fecha: 2024

Dashboard interactivo para seguimiento P2P USDT
"""

import pandas as pd
import os
import sys # <--- Añadir import sys
from datetime import datetime
from typing import Dict, List, Tuple
# import json # No se utiliza

# Importar la función para crear ejemplos desde el script tracker
from script_p2p_tracker import crear_archivos_ejemplo as crear_ejemplos_desde_tracker

# --- Definición de rutas ---
# Obtener la ruta absoluta del script actual (dashboard_p2p.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Asumiendo que la estructura es P2P_Profit/src/dashboard_p2p.py y data está en P2P_Profit/data/
BASE_DIR = os.path.dirname(SCRIPT_DIR) # Esto sería P2P_Profit/
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports') # Asumiendo que reports está dentro de data
BACKUPS_DIR = os.path.join(DATA_DIR, 'backups') # Asumiendo que backups está dentro de data

# Añadir SCRIPT_DIR al sys.path para importaciones locales si es necesario
# Por ejemplo, si 'script_p2p_tracker' está en el mismo directorio 'src'
# sys.path.insert(0, SCRIPT_DIR) # Descomentar si hay módulos locales en src/

# Rutas a los archivos de datos principales
COMPRAS_CSV = os.path.join(DATA_DIR, 'compras_usdt.csv')
VENTAS_CSV = os.path.join(DATA_DIR, 'ventas_usdt.csv')
CONVERSIONES_CSV = os.path.join(DATA_DIR, 'conversiones_fiat.csv')
LOG_ERRORES_TXT = os.path.join(BASE_DIR, 'log_errores_dashboard.txt') # Log en el directorio base

# Rutas para reportes (ejemplos)
REPORTE_FLUJO_FIAT_CSV = os.path.join(REPORTS_DIR, 'reporte_flujo_fiat.csv')
REPORTE_VENTAS_PL_CSV = os.path.join(REPORTS_DIR, 'reporte_ventas_pl.csv')

# Asegurarse de que los directorios de datos, reportes y backups existan
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)
# --- Fin Definición de rutas ---

class P2PDashboard:
    def __init__(self):
        # Estado
        self.data_loaded = False
        self.calculations_done = False
        
        # Base de datos simple
        self.datos = {
            'compras': [],
            'ventas': [],
            'conversiones': [],
            'resumen': {}
        }

    def mostrar_menu_principal(self):
        """Menú principal elegante"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            self.mostrar_estado_rapido()
            
            print("\n" + "┌─" + "─"*50 + "─┐")
            print("│" + " "*18 + "MENÚ PRINCIPAL" + " "*19 + "│")
            print("├─" + "─"*50 + "─┤")
            print("│  1️⃣  📝 Gestionar Datos" + " "*26 + "│")
            print("│  2️⃣  📊 Ver Resumen" + " "*30 + "│") 
            print("│  3️⃣  📈 Análisis Detallado" + " "*23 + "│")
            print("│  4️⃣  🔧 Herramientas" + " "*29 + "│")
            print("│  5️⃣  ❌ Salir" + " "*34 + "│")
            print("└─" + "─"*50 + "─┘")
            
            opcion = input("\n👉 Selecciona opción: ").strip()
            
            if opcion == '1':
                self.menu_gestionar_datos()
            elif opcion == '2':
                self.menu_resumen()
            elif opcion == '3':
                self.menu_analisis()
            elif opcion == '4':
                self.menu_herramientas()
            elif opcion == '5':
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
                input("Presiona Enter para continuar...")

    def limpiar_pantalla(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_header(self):
        """Header elegante"""
        print("╔" + "═"*60 + "╗")
        print("║" + " "*15 + "🎯 P2P CRYPTO TRACKER" + " "*24 + "║")
        print("║" + " "*18 + "Dashboard P2P Interactivo" + " "*17 + "║")
        print("╚" + "═"*60 + "╝")

    def mostrar_estado_rapido(self):
        """Muestra estado rápido sin cálculos complejos"""
        self.cargar_datos_rapido()
        
        print(f"\n📊 Estado: {len(self.datos['compras'])} compras | " + 
              f"{len(self.datos['ventas'])} ventas | " +
              f"{len(self.datos['conversiones'])} conversiones")
        
        if self.datos['compras'] or self.datos['ventas']:
            print("🟢 Datos disponibles")
        else:
            print("🔴 Sin datos - usa 'Gestionar Datos' para empezar")

    def cargar_datos_rapido(self):
        """Carga rápida solo para contar registros"""
        # print(f"DEBUG: CWD en cargar_datos_rapido: {os.getcwd()}") # Ya no es tan relevante
        # print(f"DEBUG: Intentando leer compras desde: {os.path.abspath(COMPRAS_CSV)}")
        # print(f"DEBUG: Intentando leer ventas desde: {os.path.abspath(VENTAS_CSV)}")
        # print(f"DEBUG: Intentando leer conversiones desde: {os.path.abspath(CONVERSIONES_CSV)}")

        try:
            if os.path.exists(COMPRAS_CSV):
                df = pd.read_csv(COMPRAS_CSV)
                if 'Plataforma' in df.columns:
                    df['Plataforma'] = df['Plataforma'].astype(str).str.lower()
                self.datos['compras'] = df.to_dict('records')
            else: # Asegurar que la lista se vacíe si el archivo no existe o es borrado
                self.datos['compras'] = []
                # print(f"DEBUG: Archivo {COMPRAS_CSV} NO encontrado.") # Opcional: log más informativo
            
            if os.path.exists(VENTAS_CSV):
                df = pd.read_csv(VENTAS_CSV)
                if 'Plataforma' in df.columns:
                    df['Plataforma'] = df['Plataforma'].astype(str).str.lower()
                self.datos['ventas'] = df.to_dict('records')
            else:
                self.datos['ventas'] = []
                # print(f"DEBUG: Archivo {VENTAS_CSV} NO encontrado.")
                
            if os.path.exists(CONVERSIONES_CSV):
                df = pd.read_csv(CONVERSIONES_CSV)
                self.datos['conversiones'] = df.to_dict('records')
            else:
                self.datos['conversiones'] = []
                # print(f"DEBUG: Archivo {CONVERSIONES_CSV} NO encontrado.")
            
            self.data_loaded = True
        except Exception as e: # Ser más específico con la excepción podría ser bueno, pero por ahora capturamos general
            print(f"Error al cargar datos rápido: {e}")
            self.data_loaded = False
            self.datos = {'compras': [], 'ventas': [], 'conversiones': [], 'resumen': {}}

    def menu_gestionar_datos(self):
        """Menú de gestión de datos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            
            print("\n" + "┌─" + "─"*50 + "─┐")
            print("│" + " "*18 + "GESTIONAR DATOS" + " "*17 + "│")
            print("├─" + "─"*50 + "─┤")
            print("│  1️⃣  ➕ Nueva Compra" + " "*26 + "│")
            print("│  2️⃣  ➖ Nueva Venta" + " "*28 + "│")
            print("│  3️⃣  🔄 Nueva Conversión" + " "*23 + "│")
            print("│  4️⃣  📋 Ver Datos Actuales" + " "*21 + "│")
            print("│  5️⃣  ⬅️  Volver" + " "*33 + "│")
            print("└─" + "─"*50 + "─┘")
            
            opcion = input("\n👉 Selecciona opción: ").strip()
            
            if opcion == '1':
                self.form_compra()
            elif opcion == '2':
                self.form_venta()
            elif opcion == '3':
                self.form_conversion()
            elif opcion == '4':
                self.ver_datos_actuales()
            elif opcion == '5':
                break
            else:
                print("❌ Opción inválida")
                input("Presiona Enter para continuar...")

    def form_compra(self):
        """Formulario de compra simplificado"""
        self.limpiar_pantalla()
        print("╔" + "═"*40 + "╗")
        print("║" + " "*12 + "📈 NUEVA COMPRA" + " "*13 + "║")
        print("╚" + "═"*40 + "╝")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('compra')
            nuevo_id = f"C{ultimo_id + 1:03d}"
            print(f"\n🆔 ID: {nuevo_id}")
            
            # Datos básicos
            cantidad = float(input("🪙 Cantidad USDT: "))
            moneda = input("💰 Moneda (USD/UYU): ").upper()
            precio = float(input(f"💵 Precio por USDT en {moneda}: "))
            plataforma = input("🏦 Plataforma (Binance/WhatsApp/Otro): ").strip().lower()

            tasa_cambio_compra = 1.0
            if moneda == 'UYU':
                tasa_cambio_compra = float(input(f"💱 Tasa de Cambio UYU a USD para esta compra (ej: 39.5): "))
            
            fuente_fondos = input("📊 Fuente de Fondos Fiat (ej: Capital Nuevo, Venta_ID_V001, Conversion_ID_CF1): ").strip()
            
            comisiones = 0.0
            if plataforma == 'binance':
                print(f"ℹ️ Para Binance, las comisiones se calcularán automáticamente.")
            # Para otras plataformas (ej. WhatsApp, Otro), las comisiones permanecen en 0.0
            # Si se necesitara ingresar comisiones para estas, se añadiría lógica aquí.

            # Calcular costo
            costo = cantidad * precio # Costo base 
            print(f"\n💰 Costo base (sin comisiones): {costo:.2f} {moneda}")
            
            if input("\n✅ ¿Guardar? (s/n): ").lower().startswith('s'):
                self.guardar_compra_simple(nuevo_id, cantidad, moneda, precio, plataforma, comisiones, tasa_cambio_compra, fuente_fondos)
                print("🎉 ¡Compra guardada!")
            
        except ValueError:
            print("❌ Error en los datos")
        
        input("\nPresiona Enter para continuar...")

    def form_venta(self):
        """Formulario de venta simplificado"""
        self.limpiar_pantalla()
        print("╔" + "═"*40 + "╗")
        print("║" + " "*13 + "📉 NUEVA VENTA" + " "*13 + "║")
        print("╚" + "═"*40 + "╝")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('venta')
            nuevo_id = f"V{ultimo_id + 1:03d}"
            print(f"\n🆔 ID: {nuevo_id}")
            
            # Datos básicos
            cantidad = float(input("🪙 Cantidad USDT: "))
            moneda = input("💰 Moneda (USD/UYU): ").upper()
            precio = float(input(f"💵 Precio por USDT en {moneda}: "))
            plataforma = input("🏦 Plataforma (Binance/WhatsApp/Otro): ").strip().lower()

            tasa_cambio_venta = 1.0
            if moneda == 'UYU':
                tasa_cambio_venta = float(input(f"💱 Tasa de Cambio UYU a USD para esta venta (ej: 40.2): "))

            comisiones = 0.0
            if plataforma == 'binance':
                print(f"ℹ️ Para Binance, las comisiones se calcularán automáticamente.")
            # Para otras plataformas (ej. WhatsApp, Otro), las comisiones permanecen en 0.0

            # Calcular ingreso
            ingreso = cantidad * precio # Ingreso base
            print(f"\n💰 Ingreso base (sin comisiones): {ingreso:.2f} {moneda}")
            
            if input("\n✅ ¿Guardar? (s/n): ").lower().startswith('s'):
                self.guardar_venta_simple(nuevo_id, cantidad, moneda, precio, plataforma, comisiones, tasa_cambio_venta)
                print("🎉 ¡Venta guardada!")
            
        except ValueError:
            print("❌ Error en los datos")
        
        input("\nPresiona Enter para continuar...")

    def form_conversion(self):
        """Formulario de conversión simplificado"""
        self.limpiar_pantalla()
        print("╔" + "═"*40 + "╗")
        print("║" + " "*10 + "🔄 NUEVA CONVERSIÓN" + " "*11 + "║")
        print("╚" + "═"*40 + "╝")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('conversion')
            nuevo_id = f"CF{ultimo_id + 1:03d}"
            print(f"\n🆔 ID: {nuevo_id}")
            
            # Datos básicos
            origen = input("💱 Moneda origen (USD/UYU): ").upper()
            cant_origen = float(input(f"💰 Cantidad {origen}: "))
            destino = 'UYU' if origen == 'USD' else 'USD'
            cant_destino = float(input(f"💰 Cantidad {destino} recibida: "))
            id_venta_asociada = input("🔗 ID Venta Asociada (o N/A si no aplica): ").strip()
            notas = input("📝 Notas (opcional): ").strip()
            
            # Mostrar tasa
            tasa = cant_destino / cant_origen if cant_origen != 0 else 0 # Tasa destino/origen
            if origen == 'UYU' and destino == 'USD': # Si es UYU a USD, la tasa es UYU por USD
                tasa = cant_origen / cant_destino if cant_destino != 0 else 0
                print(f"\n📊 Tasa: {tasa:.4f} UYU/USD")
            elif origen == 'USD' and destino == 'UYU': # Si es USD a UYU, la tasa es UYU por USD
                tasa = cant_destino / cant_origen if cant_origen != 0 else 0
                print(f"\n📊 Tasa: {tasa:.4f} UYU/USD")
            else: # Caso genérico, podría ser USD/USD o UYU/UYU (no debería ocurrir)
                 print(f"\n📊 Tasa calculada: {tasa:.4f} {destino}/{origen}")
            
            if input("\n✅ ¿Guardar? (s/n): ").lower().startswith('s'):
                self.guardar_conversion_simple(nuevo_id, origen, cant_origen, destino, cant_destino, id_venta_asociada, notas)
                print("🎉 ¡Conversión guardada!")
            
        except ValueError:
            print("❌ Error en los datos")
        
        input("\nPresiona Enter para continuar...")

    def menu_resumen(self):
        """Resumen rápido y elegante"""
        self.limpiar_pantalla()
        self.mostrar_header()
        
        print("\n" + "┌─" + "─"*50 + "─┐")
        print("│" + " "*19 + "RESUMEN RÁPIDO" + " "*17 + "│")
        print("└─" + "─"*50 + "─┘")
        
        if not self.data_loaded:
            self.cargar_datos_rapido()
        
        if not self.datos['compras'] and not self.datos['ventas']:
            print("\n📝 No hay datos aún")
            print("   Usa 'Gestionar Datos' para empezar")
        else:
            # Resumen básico
            total_compras = len(self.datos['compras'])
            total_ventas = len(self.datos['ventas'])
            
            print(f"\n📊 TRANSACCIONES")
            print(f"   📈 Compras: {total_compras}")
            print(f"   📉 Ventas: {total_ventas}")
            print(f"   🔄 Conversiones: {len(self.datos['conversiones'])}")
            
            # Solo calcular si hay datos
            if self.datos['compras']:
                usdt_comprado = sum(c.get('Cantidad_USDT_Comprada', 0) for c in self.datos['compras'])
                print(f"\n🪙 USDT Comprado Total: {usdt_comprado:.2f}")
            
            if self.datos['ventas']:
                usdt_vendido = sum(v.get('Cantidad_USDT_Vendida', 0) for v in self.datos['ventas'])
                print(f"🪙 USDT Vendido Total: {usdt_vendido:.2f}")
            
            # Última transacción
            if self.datos['compras'] or self.datos['ventas']:
                print(f"\n📅 ÚLTIMA ACTIVIDAD")
                if self.datos['compras']:
                    ultima_compra = self.datos['compras'][-1]
                    print(f"   📈 Última compra: {ultima_compra.get('ID_Compra', 'N/A')}")
                if self.datos['ventas']:
                    ultima_venta = self.datos['ventas'][-1]
                    print(f"   📉 Última venta: {ultima_venta.get('ID_Venta', 'N/A')}")
        
        print(f"\n" + "─"*52)
        print("1️⃣  🔢 Cálculos Avanzados")
        print("2️⃣  ⬅️  Volver")
        
        opcion = input("\n👉 Opción: ").strip()
        if opcion == '1':
            self.calculos_avanzados()

    def calculos_avanzados(self):
        """Cálculos opcionales más detallados"""
        self.limpiar_pantalla()
        print("╔" + "═"*50 + "╗")
        print("║" + " "*15 + "🔢 CALCULANDO..." + " "*17 + "║")
        print("╚" + "═"*50 + "╝")
        
        print("\n⏳ Procesando datos...")
        
        try:
            from script_p2p_tracker import P2PTracker
            tracker = P2PTracker()
            
            if os.path.exists(COMPRAS_CSV) and os.path.exists(VENTAS_CSV):
                tracker.cargar_datos(COMPRAS_CSV, VENTAS_CSV, CONVERSIONES_CSV)
                tracker.calcular_preliminares_compras()
                tracker.calcular_preliminares_ventas()
                tracker.crear_transacciones_ordenadas()
                tracker.procesar_cpp_y_pl()
                
                # Mostrar resultados principales
                self.limpiar_pantalla()
                print("╔" + "═"*50 + "╗")
                print("║" + " "*12 + "📊 ANÁLISIS COMPLETO" + " "*17 + "║")
                print("╚" + "═"*50 + "╝")
                
                if hasattr(tracker, 'df_ventas_calc') and not tracker.df_ventas_calc.empty:
                    total_pl = tracker.df_ventas_calc['Ganancia_Perdida_USDT_en_USD'].sum()
                    print(f"\n💰 P&L Total: ${total_pl:.2f} USD")
                    
                    cpp_actual = (tracker.inventario_usdt_costo_total_usd / tracker.inventario_usdt_cantidad 
                                 if tracker.inventario_usdt_cantidad > 0 else 0)
                    print(f"📊 CPP Actual: ${cpp_actual:.4f}")
                    print(f"🪙 Stock USDT (Registrado): {tracker.inventario_usdt_cantidad:.2f}")
                    
                    if total_pl > 0:
                        print("🟢 ¡Operaciones rentables!")
                    elif total_pl < 0:
                        print("🔴 Pérdidas acumuladas")
                    else:
                        print("⚪ Break even")
                else:
                    print("\n📝 Necesitas al menos una venta para el análisis P&L")
            else:
                print("\n❌ Faltan archivos de datos")
                
        except Exception as e:
            print(f"\n❌ Error en cálculos: {str(e)[:50]}...")
        
        input("\nPresiona Enter para continuar...")

    def menu_analisis(self):
        """Menú de análisis detallado"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            
            print("\n" + "┌─" + "─"*50 + "─┐")
            print("│" + " "*16 + "ANÁLISIS DETALLADO" + " "*16 + "│")
            print("├─" + "─"*50 + "─┤")
            print("│  1️⃣  📈 Ver Compras" + " "*28 + "│")
            print("│  2️⃣  📉 Ver Ventas" + " "*29 + "│")
            print("│  3️⃣  🔄 Ver Conversiones" + " "*23 + "│")
            print("│  4️⃣  🔢 Dashboard Completo" + " "*21 + "│")
            print("│  5️⃣  ⬅️  Volver" + " "*33 + "│")
            print("└─" + "─"*50 + "─┘")
            
            opcion = input("\n👉 Selecciona opción: ").strip()
            
            if opcion == '1':
                self.ver_compras()
            elif opcion == '2':
                self.ver_ventas()
            elif opcion == '3':
                self.ver_conversiones()
            elif opcion == '4':
                self.dashboard_completo()
            elif opcion == '5':
                break
            else:
                print("❌ Opción inválida")
                input("Presiona Enter para continuar...")

    def ver_compras(self):
        """Vista simplificada de compras"""
        self.limpiar_pantalla()
        print("╔" + "═"*60 + "╗")
        print("║" + " "*23 + "📈 COMPRAS" + " "*28 + "║")
        print("╚" + "═"*60 + "╝")
        
        if not self.datos['compras']:
            print("\n📝 No hay compras registradas")
        else:
            print(f"\n{'ID':<8} {'Fecha':<12} {'USDT':<10} {'Moneda':<8} {'Precio':<10}")
            print("─" * 60)
            
            for compra in self.datos['compras'][-10:]:  # Solo últimas 10
                fecha = compra.get('Fecha_Compra', 'N/A')[:10]
                print(f"{compra.get('ID_Compra', 'N/A'):<8} {fecha:<12} "
                      f"{compra.get('Cantidad_USDT_Comprada', 0):<10.2f} "
                      f"{compra.get('Moneda_Pago', 'N/A'):<8} "
                      f"{compra.get('Precio_Unitario_Moneda_Pago', 0):<10.4f}")
        
        input("\nPresiona Enter para continuar...")

    def ver_ventas(self):
        """Vista simplificada de ventas"""
        self.limpiar_pantalla()
        print("╔" + "═"*60 + "╗")
        print("║" + " "*24 + "📉 VENTAS" + " "*28 + "║")
        print("╚" + "═"*60 + "╝")
        
        if not self.datos['ventas']:
            print("\n📝 No hay ventas registradas")
        else:
            print(f"\n{'ID':<8} {'Fecha':<12} {'USDT':<10} {'Moneda':<8} {'Precio':<10}")
            print("─" * 60)
            
            for venta in self.datos['ventas'][-10:]:  # Solo últimas 10
                fecha = venta.get('Fecha_Venta', 'N/A')[:10]
                print(f"{venta.get('ID_Venta', 'N/A'):<8} {fecha:<12} "
                      f"{venta.get('Cantidad_USDT_Vendida', 0):<10.2f} "
                      f"{venta.get('Moneda_Recibida', 'N/A'):<8} "
                      f"{venta.get('Precio_Unitario_Moneda_Recibida', 0):<10.4f}")
        
        input("\nPresiona Enter para continuar...")

    def ver_conversiones(self):
        """Vista simplificada de conversiones"""
        self.limpiar_pantalla()
        print("╔" + "═"*60 + "╗")
        print("║" + " "*20 + "🔄 CONVERSIONES" + " "*25 + "║")
        print("╚" + "═"*60 + "╝")
        
        if not self.datos['conversiones']:
            print("\n📝 No hay conversiones registradas")
        else:
            print(f"\n{'ID':<8} {'Fecha':<12} {'De':<8} {'A':<8} {'Tasa':<10}")
            print("─" * 60)
            
            for conv in self.datos['conversiones']:
                fecha = conv.get('Fecha_Conversion', 'N/A')[:10]
                tasa = (conv.get('Cantidad_Origen', 0) / conv.get('Cantidad_Destino', 1))
                print(f"{conv.get('ID_Conversion', 'N/A'):<8} {fecha:<12} "
                      f"{conv.get('Moneda_Origen', 'N/A'):<8} "
                      f"{conv.get('Moneda_Destino', 'N/A'):<8} "
                      f"{tasa:<10.4f}")
        
        input("\nPresiona Enter para continuar...")

    def dashboard_completo(self):
        """Dashboard completo (el original) como opción"""
        self.limpiar_pantalla()
        print("╔" + "═"*50 + "╗")
        print("║" + " "*10 + "🔢 DASHBOARD COMPLETO" + " "*17 + "║")
        print("╚" + "═"*50 + "╝")
        
        print("\n⚠️  Esto ejecutará el dashboard completo original")
        print("    (puede ser lento con muchos datos)")
        
        if input("\n¿Continuar? (s/n): ").lower().startswith('s'):
            try:
                from script_p2p_tracker import P2PTracker
                tracker = P2PTracker()
                tracker.cargar_datos(COMPRAS_CSV, VENTAS_CSV, CONVERSIONES_CSV)
                tracker.calcular_preliminares_compras()
                tracker.calcular_preliminares_ventas()
                tracker.crear_transacciones_ordenadas()
                tracker.procesar_cpp_y_pl()
                tracker.procesar_conversiones_fiat()
                tracker.generar_reportes()
                
                input("\n\nPresiona Enter para continuar...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Presiona Enter para continuar...")

    def menu_herramientas(self):
        """Herramientas básicas"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            
            print("\n" + "┌─" + "─"*50 + "─┐")
            print("│" + " "*18 + "HERRAMIENTAS" + " "*20 + "│")
            print("├─" + "─"*50 + "─┤")
            print("│  1️⃣  📁 Estado de Archivos" + " "*21 + "│")
            print("│  2️⃣  📝 Crear Datos de Ejemplo" + " "*18 + "│")
            print("│  3️⃣  📤 Exportar Backup" + " "*25 + "│")
            print("│  4️⃣  ⬅️  Volver" + " "*33 + "│")
            print("└─" + "─"*50 + "─┘")
            
            opcion = input("\n👉 Selecciona opción: ").strip()
            
            if opcion == '1':
                self.estado_archivos()
            elif opcion == '2':
                self.crear_ejemplos()
            elif opcion == '3':
                self.backup()
            elif opcion == '4':
                break
            else:
                print("❌ Opción inválida")
                input("Presiona Enter para continuar...")

    def ver_datos_actuales(self):
        """Vista rápida de datos actuales"""
        self.limpiar_pantalla()
        print("╔" + "═"*50 + "╗")
        print("║" + " "*16 + "📋 DATOS ACTUALES" + " "*16 + "║")
        print("╚" + "═"*50 + "╝")
        
        self.cargar_datos_rapido()
        
        print(f"\n📈 Compras: {len(self.datos['compras'])}")
        print(f"📉 Ventas: {len(self.datos['ventas'])}")
        print(f"🔄 Conversiones: {len(self.datos['conversiones'])}")
        
        # Mostrar últimas transacciones
        if self.datos['compras']:
            print(f"\n📈 Última compra: {self.datos['compras'][-1].get('ID_Compra', 'N/A')}")
        if self.datos['ventas']:
            print(f"📉 Última venta: {self.datos['ventas'][-1].get('ID_Venta', 'N/A')}")
        
        input("\nPresiona Enter para continuar...")

    # Métodos de utilidad simplificados
    def obtener_ultimo_id(self, tipo: str) -> int:
        """Obtiene el último ID numérico de un tipo de archivo"""
        archivo_map = {
            'compra': COMPRAS_CSV,
            'venta': VENTAS_CSV,
            'conversion': CONVERSIONES_CSV
        }
        id_col_map = {
            'compra': 'ID_Compra',
            'venta': 'ID_Venta',
            'conversion': 'ID_Conversion' # Asegurar que coincida con el CSV
        }
        prefijo_map = {
            'compra': 'C',
            'venta': 'V',
            'conversion': 'CF'
        }

        archivo_path = archivo_map.get(tipo)
        id_col = id_col_map.get(tipo)
        prefijo = prefijo_map.get(tipo)

        if not archivo_path or not id_col or not prefijo:
            print(f"Error: Tipo '{tipo}' no reconocido para obtener último ID.")
            return 0 # o lanzar excepción

        max_id = 0
        if os.path.exists(archivo_path):
            try:
                df = pd.read_csv(archivo_path)
                if not df.empty and id_col in df.columns:
                    # Extraer la parte numérica del ID
                    ids_numericos = df[id_col].astype(str).str.replace(prefijo, '', regex=False)
                    ids_numericos = pd.to_numeric(ids_numericos, errors='coerce').dropna()
                    if not ids_numericos.empty:
                        max_id = int(ids_numericos.max())
            except Exception as e:
                print(f"Error leyendo {archivo_path} para obtener último ID: {e}")
        return max_id

    def guardar_compra_simple(self, id_compra: str, cantidad: float, moneda: str, precio: float, plataforma: str, comisiones: float, tasa_cambio: float, fuente_fondos: str):
        """Guarda una compra simple en el CSV y actualiza el estado interno."""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_compra = {
            'ID_Compra': id_compra,
            'Fecha_Compra': fecha_actual, 
            'Cantidad_USDT_Comprada': cantidad,
            'Moneda_Pago': moneda,
            'Precio_Unitario_Moneda_Pago': precio,
            'Tasa_Cambio_UYU_USD_Compra': tasa_cambio,
            'Fuente_De_Fondos_Fiat': fuente_fondos,
            'Comisiones_Compra_Moneda_Pago': comisiones,
            'Plataforma': plataforma
        }
        self.datos['compras'].append(nueva_compra)
        
        # Guardar en CSV
        df_compras = pd.DataFrame(self.datos['compras'])
        df_compras.to_csv(COMPRAS_CSV, index=False)
        self.data_loaded = True # Actualizar estado

    def guardar_venta_simple(self, id_venta: str, cantidad: float, moneda: str, precio: float, plataforma: str, comisiones: float, tasa_cambio: float):
        """Guarda una venta simple en el CSV y actualiza el estado interno."""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_venta = {
            'ID_Venta': id_venta,
            'Fecha_Venta': fecha_actual,
            'Cantidad_USDT_Vendida': cantidad,
            'Moneda_Recibida': moneda,
            'Precio_Unitario_Moneda_Recibida': precio,
            'Tasa_Cambio_UYU_USD_Venta': tasa_cambio,
            'Comisiones_Venta_Moneda_Recibida': comisiones,
            'Plataforma': plataforma
        }
        self.datos['ventas'].append(nueva_venta)
        
        # Guardar en CSV
        df_ventas = pd.DataFrame(self.datos['ventas'])
        df_ventas.to_csv(VENTAS_CSV, index=False)
        self.data_loaded = True # Actualizar estado

    def guardar_conversion_simple(self, id_conversion: str, origen: str, cant_origen: float, destino: str, cant_destino: float, id_venta_asociada: str, notas: str):
        """Guarda una conversión simple en el CSV y actualiza el estado interno."""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_conversion = {
            'ID_Conversion': id_conversion,
            'Fecha_Conversion': fecha_actual,
            'Moneda_Origen': origen,
            'Cantidad_Origen': cant_origen,
            'Moneda_Destino': destino,
            'Cantidad_Destino': cant_destino,
            'ID_Venta_Asociada': id_venta_asociada if id_venta_asociada.upper() != 'N/A' else '',
            'Notas': notas
        }
        self.datos['conversiones'].append(nueva_conversion)
        
        # Guardar en CSV
        df_conversiones = pd.DataFrame(self.datos['conversiones'])
        df_conversiones.to_csv(CONVERSIONES_CSV, index=False)
        self.data_loaded = True # Actualizar estado

    def estado_archivos(self):
        """Muestra el estado de los archivos de datos."""
        self.limpiar_pantalla()
        self.mostrar_header()
        print("\n" + "─"*10 + " ESTADO DE ARCHIVOS " + "─"*10)

        archivos = {
            "Compras USDT": COMPRAS_CSV,
            "Ventas USDT": VENTAS_CSV,
            "Conversiones Fiat": CONVERSIONES_CSV,
            "Log de Errores": LOG_ERRORES_TXT
        }

        for nombre, ruta in archivos.items():
            if os.path.exists(ruta):
                print(f"\n🟢 {nombre}: Encontrado")
                print(f"   Ruta: {os.path.abspath(ruta)}")
                try:
                    df = pd.read_csv(ruta)
                    print(f"   Registros: {len(df)}")
                    if not df.empty:
                        print(f"   Columnas: {', '.join(df.columns.tolist())}")
                except pd.errors.EmptyDataError:
                    print("   Archivo vacío.")
                except Exception as e:
                    print(f"   Error al leer: {e}")
            else:
                print(f"\n🔴 {nombre}: No encontrado")
                print(f"   Ruta esperada: {os.path.abspath(ruta)}")
        
        print("\n" + "─"*40)
        input("\nPresiona Enter para volver...")

    def crear_ejemplos(self):
        """Llama a la función de script_p2p_tracker para crear archivos CSV de ejemplo."""
        self.limpiar_pantalla()
        self.mostrar_header()
        print("\n" + "─"*10 + " CREAR DATOS DE EJEMPLO " + "─"*10)
        print("\n🟡 Intentando crear archivos de ejemplo con datos significativos...")
        try:
            crear_ejemplos_desde_tracker() # Llamada a la función importada
            print("\n✅ Proceso de creación de ejemplos finalizado.")
            print("   Verifica la consola del script para más detalles.")
        except Exception as e:
            print(f"\n❌ Error al intentar crear archivos de ejemplo: {e}")
            print("   Asegúrate que el script 'script_p2p_tracker.py' está accesible.")
        
        input("\nPresiona Enter para continuar...")

    def backup(self):
        """Crea un backup de los archivos CSV en la carpeta data/backups."""
        self.limpiar_pantalla()
        self.mostrar_header()
        print("\n" + "─"*10 + " BACKUP DE DATOS " + "─"*10)

        archivos_a_backupear = {
            "compras_usdt.csv": COMPRAS_CSV,
            "ventas_usdt.csv": VENTAS_CSV,
            "conversiones_fiat.csv": CONVERSIONES_CSV
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = os.path.join(BACKUPS_DIR, f"backup_{timestamp}")
        
        try:
            os.makedirs(backup_subdir, exist_ok=True)
            print(f"\n📂 Creando backup en: {backup_subdir}")

            for nombre_base, ruta_original in archivos_a_backupear.items():
                if os.path.exists(ruta_original):
                    ruta_backup = os.path.join(backup_subdir, nombre_base)
                    # Leer el original y escribir en el backup
                    df = pd.read_csv(ruta_original)
                    df.to_csv(ruta_backup, index=False)
                    print(f"  ✅ Copiado: {nombre_base} -> {ruta_backup}")
                else:
                    print(f"  ⚠️ Archivo no encontrado, no se hizo backup: {nombre_base}")
            
            print("\n🎉 Backup completado.")
        
        except Exception as e:
            print(f"\n❌ Error durante el backup: {e}")
            # Considerar loggear este error a LOG_ERRORES_TXT

        input("\nPresiona Enter para continuar...")

def main():
    # Crear directorios si no existen (ya se hace al inicio del script con las nuevas definiciones)
    # os.makedirs('../data', exist_ok=True) 
    # os.makedirs('../data/reports', exist_ok=True)
    # os.makedirs('../data/backups', exist_ok=True)

    # Crear una instancia del dashboard y correrlo
    app = P2PDashboard()
    app.mostrar_menu_principal()

if __name__ == "__main__":
    main() 