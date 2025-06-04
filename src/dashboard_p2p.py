#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard P2P Cripto - USDT (Dashboard P2P Interactivo con Rich)
Autor: AI Assistant
Fecha: 2024

Dashboard interactivo profesional para seguimiento P2P USDT usando Rich
"""

import pandas as pd
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Rich components para UI moderna
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.padding import Padding
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.style import Style

# Importar la función para crear ejemplos desde el script tracker
try:
    from script_p2p_tracker import crear_archivos_ejemplo as crear_ejemplos_desde_tracker
except ImportError:
    def crear_ejemplos_desde_tracker():
        pass

# --- Definición de rutas ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports')
BACKUPS_DIR = os.path.join(DATA_DIR, 'backups')

# Rutas a los archivos de datos principales
COMPRAS_CSV = os.path.join(DATA_DIR, 'compras_usdt.csv')
VENTAS_CSV = os.path.join(DATA_DIR, 'ventas_usdt.csv')
CONVERSIONES_CSV = os.path.join(DATA_DIR, 'conversiones_fiat.csv')
LOG_ERRORES_TXT = os.path.join(BASE_DIR, 'log_errores_dashboard.txt')

# Rutas para reportes
REPORTE_FLUJO_FIAT_CSV = os.path.join(REPORTS_DIR, 'reporte_flujo_fiat.csv')
REPORTE_VENTAS_PL_CSV = os.path.join(REPORTS_DIR, 'reporte_ventas_pl.csv')

# Asegurar que los directorios existan
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)

class P2PDashboardRich:
    def __init__(self):
        # Console principal con tema personalizado
        self.console = Console(theme=self._create_theme())
        
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
        
        # Paleta de colores del tema
        self.theme_colors = {
            'primary': 'bold cyan',
            'secondary': 'bold magenta',
            'success': 'bold green',
            'warning': 'bold yellow',
            'error': 'bold red',
            'info': 'bold blue',
            'accent': 'bright_yellow',
            'neutral': 'white',
            'muted': 'bright_black'
        }

    def _create_theme(self):
        """Crea el tema personalizado para el dashboard"""
        from rich.theme import Theme
        return Theme({
            "primary": "bold cyan",
            "secondary": "bold magenta", 
            "success": "bold green",
            "warning": "bold yellow",
            "error": "bold red",
            "info": "bold blue",
            "accent": "bright_yellow",
            "neutral": "white",
            "muted": "bright_black",
            "positive": "bold green",
            "negative": "bold red"
        })

    def clear_screen(self):
        """Limpia la pantalla de forma elegante"""
        self.console.clear()

    def show_header(self):
        """Muestra el encabezado principal del dashboard"""
        header_text = Text()
        header_text.append("✨ ", style="bright_yellow")
        header_text.append("P2P CRYPTO TRACKER", style="bold cyan")
        header_text.append(" ✨", style="bright_yellow")
        
        subtitle = Text("Dashboard Interactivo Profesional", style="italic bright_blue")
        
        header_content = Columns([
            Align.center(header_text),
            Align.center(subtitle)
        ], align="center")
        
        header_panel = Panel(
            header_content,
            style="bright_cyan",
            box=box.DOUBLE_EDGE,
            padding=(1, 2)
        )
        
        self.console.print(header_panel)
        self.console.print()

    def show_status_panel(self):
        """Muestra el panel de estado rápido"""
        self.cargar_datos_rapido()
        
        # Calcular métricas básicas
        num_compras = len(self.datos.get('compras', []))
        num_ventas = len(self.datos.get('ventas', []))
        num_conversiones = len(self.datos.get('conversiones', []))
        
        # Crear tabla de estado básico
        basic_stats = Table(show_header=False, box=None, padding=(0, 1))
        basic_stats.add_column("Métrica", style="bold white", width=25)
        basic_stats.add_column("Valor", justify="right", style="bold")
        
        basic_stats.add_row("🛍️ Compras Registradas:", f"[cyan]{num_compras}[/cyan]")
        basic_stats.add_row("💸 Ventas Registradas:", f"[green]{num_ventas}[/green]")
        basic_stats.add_row("🔄 Conversiones Fiat:", f"[yellow]{num_conversiones}[/yellow]")
        
        # Estado general
        if num_compras > 0 or num_ventas > 0 or num_conversiones > 0:
            status_msg = Text("🎉 ¡Datos cargados! Listo para análisis.", style="bold green")
        else:
            status_msg = Text("⚠️ Sin datos. Usa 'Gestionar Datos' para iniciar.", style="bold yellow")
        
        # Layout del panel de estado
        status_content = Columns([
            basic_stats,
            Padding(Align.center(status_msg), (1, 2))
        ])
        
        status_panel = Panel(
            status_content,
            title="[bold bright_blue]📊 ESTADO RÁPIDO[/bold bright_blue]",
            style="blue",
            box=box.ROUNDED
        )
        
        self.console.print(status_panel)
        self.console.print()

    def show_main_menu(self):
        """Muestra el menú principal elegante"""
        menu_items = [
            ("1️⃣", "📝 Gestionar Datos de Transacciones"),
            ("2️⃣", "📊 Ver Resumen Financiero Global"),
            ("3️⃣", "📈 Análisis Detallado por Categoría"),
            ("4️⃣", "🔧 Herramientas y Utilidades"),
            ("5️⃣", "❌ Salir del Dashboard")
        ]
        
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Opción", style="bold bright_yellow", width=6)
        menu_table.add_column("Descripción", style="bold white")
        
        colors = ["cyan", "blue", "green", "yellow", "red"]
        for i, (option, description) in enumerate(menu_items):
            color = colors[i]
            menu_table.add_row(option, f"[{color}]{description}[/{color}]")
        
        menu_panel = Panel(
            menu_table,
            title="[bold bright_magenta]🏠 MENÚ PRINCIPAL[/bold bright_magenta]",
            style="magenta",
            box=box.ROUNDED
        )
        
        self.console.print(menu_panel)

    def get_user_choice(self, prompt_text: str = "✨ Selecciona una opción") -> str:
        """Obtiene la selección del usuario con estilo"""
        return Prompt.ask(f"[bold bright_yellow]{prompt_text}[/bold bright_yellow]")

    def show_success_message(self, message: str):
        """Muestra un mensaje de éxito"""
        success_panel = Panel(
            f"[bold green]✅ {message}[/bold green]",
            style="green",
            box=box.ROUNDED
        )
        self.console.print(success_panel)

    def show_error_message(self, message: str):
        """Muestra un mensaje de error"""
        error_panel = Panel(
            f"[bold red]❌ {message}[/bold red]",
            style="red",
            box=box.ROUNDED
        )
        self.console.print(error_panel)

    def show_info_message(self, message: str):
        """Muestra un mensaje informativo"""
        info_panel = Panel(
            f"[bold blue]ℹ️ {message}[/bold blue]",
            style="blue",
            box=box.ROUNDED
        )
        self.console.print(info_panel)

    def show_section_header(self, title: str, breadcrumb: str = ""):
        """Muestra el encabezado de una sección"""
        self.clear_screen()
        self.show_header()
        
        if breadcrumb:
            breadcrumb_text = Text(f"📍 {breadcrumb}", style="dim white")
            self.console.print(Align.center(breadcrumb_text))
            self.console.print()
        
        section_panel = Panel(
            Align.center(Text(title, style="bold")),
            style="bright_green",
            box=box.DOUBLE_EDGE
        )
        self.console.print(section_panel)
        self.console.print()

    def display_dataframe_table(self, df: pd.DataFrame, title: str, max_rows: int = 15):
        """Muestra una tabla de DataFrame con paginación usando Rich Table"""
        if df.empty:
            self.show_info_message(f"No hay datos para mostrar en {title}")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return

        total_rows = len(df)
        start_row = 0

        while start_row < total_rows:
            self.clear_screen()
            self.show_header()
            
            end_row = min(start_row + max_rows, total_rows)
            
            # Crear tabla Rich
            table = Table(
                title=f"[bold]{title}[/bold] - Filas {start_row + 1} a {end_row} de {total_rows}",
                box=box.ROUNDED,
                header_style="bold magenta",
                show_lines=True,
                expand=True
            )
            
            # Añadir columnas con anchos dinámicos
            for col in df.columns:
                if 'ID' in col:
                    table.add_column(col, style="cyan", width=8)
                elif 'Fecha' in col:
                    table.add_column(col, style="blue", width=12)
                elif any(word in col.lower() for word in ['cantidad', 'precio', 'ganancia', 'perdida', 'costo']):
                    table.add_column(col, style="green", justify="right", width=12)
                else:
                    table.add_column(col, style="white", width=15)
            
            # Añadir filas con formato
            df_slice = df.iloc[start_row:end_row]
            for _, row in df_slice.iterrows():
                formatted_row = []
                for col, value in row.items():
                    if pd.isna(value):
                        formatted_row.append("[dim]N/A[/dim]")
                    elif isinstance(value, (int, float)):
                        if any(word in col.lower() for word in ['ganancia', 'perdida', 'pl']):
                            color = "green" if value >= 0 else "red"
                            formatted_row.append(f"[{color}]{value:,.2f}[/{color}]")
                        else:
                            formatted_row.append(f"{value:,.2f}" if isinstance(value, float) else str(value))
                    else:
                        formatted_row.append(str(value))
                table.add_row(*formatted_row)
            
            self.console.print(table)
            
            # Controles de paginación
            if end_row < total_rows:
                self.console.print(f"\n[bold]Mostrando {end_row} de {total_rows} registros[/bold]")
                action = Prompt.ask(
                    "[bold bright_yellow]Siguiente página (s) / Ver todas (t) / Volver (v)[/bold bright_yellow]",
                    choices=["s", "t", "v"],
                    default="s"
                )
                
                if action == "s":
                    start_row = end_row
                elif action == "t":
                    max_rows = total_rows
                else:
                    break
            else:
                Prompt.ask("\n[bold]Presiona Enter para volver[/bold]")
                break

    def _get_validated_float(self, prompt: str, min_val: float = None, max_val: float = None, default: float = None) -> float:
        """Obtiene un número flotante validado del usuario"""
        while True:
            try:
                full_prompt = f"[bold cyan]{prompt}[/bold cyan]"
                if default is not None:
                    value = Prompt.ask(full_prompt, default=str(default))
                else:
                    value = Prompt.ask(full_prompt)
                
                float_val = float(value)
                
                if min_val is not None and float_val < min_val:
                    self.show_error_message(f"El valor debe ser mayor o igual a {min_val}")
                    continue
                    
                if max_val is not None and float_val > max_val:
                    self.show_error_message(f"El valor debe ser menor o igual a {max_val}")
                    continue
                    
                return float_val
                
            except ValueError:
                self.show_error_message("Por favor, ingresa un número válido.")
            except KeyboardInterrupt:
                raise

    def _get_validated_choice(self, prompt: str, choices: List[str]) -> str:
        """Obtiene una opción validada del usuario"""
        return Prompt.ask(f"[bold cyan]{prompt}[/bold cyan]", choices=choices)

    def _show_transaction_summary(self, transaction_type: str, data: Dict[str, str]):
        """Muestra un resumen de la transacción antes de guardar"""
        summary_table = Table(show_header=False, box=None, padding=(0, 1))
        summary_table.add_column("Campo", style="bold cyan", width=20)
        summary_table.add_column("Valor", style="white")
        
        for key, value in data.items():
            summary_table.add_row(f"{key}:", value)
        
        summary_panel = Panel(
            summary_table,
            title=f"[bold bright_yellow]📝 RESUMEN DE LA {transaction_type}[/bold bright_yellow]",
            style="yellow",
            box=box.ROUNDED
        )
        
        self.console.print(summary_panel)

    def cargar_datos_rapido(self):
        """Carga rápida de datos"""
        try:
            if os.path.exists(COMPRAS_CSV):
                df = pd.read_csv(COMPRAS_CSV)
                self.datos['compras'] = df.to_dict('records')
            else:
                self.datos['compras'] = []
            
            if os.path.exists(VENTAS_CSV):
                df = pd.read_csv(VENTAS_CSV)
                self.datos['ventas'] = df.to_dict('records')
            else:
                self.datos['ventas'] = []
                
            if os.path.exists(CONVERSIONES_CSV):
                df = pd.read_csv(CONVERSIONES_CSV)
                self.datos['conversiones'] = df.to_dict('records')
            else:
                self.datos['conversiones'] = []
            
            self.data_loaded = True
        except Exception as e:
            self.show_error_message(f"Error al cargar datos: {e}")
            self.data_loaded = False

    def obtener_ultimo_id(self, tipo: str) -> int:
        """Obtiene el último ID numérico"""
        archivo_map = {
            'compra': COMPRAS_CSV,
            'venta': VENTAS_CSV,
            'conversion': CONVERSIONES_CSV
        }
        
        id_col_map = {
            'compra': 'ID_Compra',
            'venta': 'ID_Venta',
            'conversion': 'ID_Conversion'
        }
        
        prefijo_map = {
            'compra': 'C',
            'venta': 'V',
            'conversion': 'CF'
        }

        archivo_path = archivo_map.get(tipo)
        id_col = id_col_map.get(tipo)
        prefijo = prefijo_map.get(tipo)

        max_id = 0
        if os.path.exists(archivo_path):
            try:
                df = pd.read_csv(archivo_path)
                if not df.empty and id_col in df.columns:
                    ids_numericos = df[id_col].astype(str).str.replace(prefijo, '', regex=False)
                    ids_numericos = pd.to_numeric(ids_numericos, errors='coerce').dropna()
                    if not ids_numericos.empty:
                        max_id = int(ids_numericos.max())
            except Exception:
                pass
        return max_id

    def guardar_compra_simple(self, id_compra: str, cantidad: float, moneda: str, precio: float, 
                             plataforma: str, comisiones: float, tasa_cambio: float, fuente_fondos: str):
        """Guarda una compra simple"""
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
        
        # Cargar datos existentes o crear nuevo DataFrame
        if os.path.exists(COMPRAS_CSV):
            df_compras = pd.read_csv(COMPRAS_CSV)
            df_compras = pd.concat([df_compras, pd.DataFrame([nueva_compra])], ignore_index=True)
        else:
            df_compras = pd.DataFrame([nueva_compra])
        
        df_compras.to_csv(COMPRAS_CSV, index=False)
        self.datos['compras'].append(nueva_compra)
        self.data_loaded = True

    def guardar_venta_simple(self, id_venta: str, cantidad: float, moneda: str, precio: float, 
                           plataforma: str, comisiones: float, tasa_cambio: float):
        """Guarda una venta simple"""
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
        
        # Cargar datos existentes o crear nuevo DataFrame
        if os.path.exists(VENTAS_CSV):
            df_ventas = pd.read_csv(VENTAS_CSV)
            df_ventas = pd.concat([df_ventas, pd.DataFrame([nueva_venta])], ignore_index=True)
        else:
            df_ventas = pd.DataFrame([nueva_venta])
        
        df_ventas.to_csv(VENTAS_CSV, index=False)
        self.datos['ventas'].append(nueva_venta)
        self.data_loaded = True

    def run_main_loop(self):
        """Bucle principal del dashboard"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_status_panel()
            self.show_main_menu()
            
            choice = self.get_user_choice()
            
            if choice == "1":
                self.menu_gestionar_datos()
            elif choice == "2":
                self.menu_resumen()
            elif choice == "3":
                self.menu_analisis()
            elif choice == "4":
                self.menu_herramientas()
            elif choice == "5":
                self.console.print("\n[bold green]¡Hasta luego! 👋[/bold green]")
                break
            else:
                self.show_error_message("Opción inválida. Intenta de nuevo.")
                Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_gestionar_datos(self):
        """Menú de gestión de datos mejorado"""
        while True:
            self.show_section_header("📝 GESTIONAR DATOS DE TRANSACCIONES", "Inicio > Gestión de Datos")
            
            menu_items = [
                ("1️⃣", "➕ Registrar Nueva Compra de USDT", "success"),
                ("2️⃣", "➖ Registrar Nueva Venta de USDT", "warning"),
                ("3️⃣", "🔄 Registrar Nueva Conversión Fiat", "info"),
                ("4️⃣", "📋 Ver Todos los Datos Actuales", "primary"),
                ("5️⃣", "⬅️ Volver al Menú Principal", "muted")
            ]
            
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Opción", style="bold bright_yellow", width=6)
            menu_table.add_column("Descripción", style="bold")
            
            for option, description, style_type in menu_items:
                color = self.theme_colors.get(style_type, "white")
                menu_table.add_row(option, f"[{color}]{description}[/{color}]")
            
            menu_panel = Panel(
                menu_table,
                title="[bold bright_green]📝 OPCIONES DE GESTIÓN[/bold bright_green]",
                style="green",
                box=box.ROUNDED
            )
            
            self.console.print(menu_panel)
            
            choice = self.get_user_choice()
            
            if choice == "1":
                self.form_compra_rich()
            elif choice == "2":
                self.form_venta_rich()
            elif choice == "3":
                self.form_conversion_rich() 
            elif choice == "4":
                self.ver_datos_actuales_rich()
            elif choice == "5":
                break
            else:
                self.show_error_message("Opción inválida. Intenta de nuevo.")
                Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def form_compra_rich(self):
        """Formulario de compra con Rich mejorado"""
        self.show_section_header("📈 REGISTRAR NUEVA COMPRA", "Inicio > Gestión > Nueva Compra")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('compra')
            nuevo_id = f"C{ultimo_id + 1:03d}"
            
            id_panel = Panel(
                f"[bold cyan]ID de Compra Asignado: {nuevo_id}[/bold cyan]",
                style="cyan",
                box=box.ROUNDED
            )
            self.console.print(id_panel)
            self.console.print()
            
            # Formulario paso a paso con validaciones
            cantidad = self._get_validated_float("🪙 Cantidad de USDT comprados", min_val=0.01)
            moneda = self._get_validated_choice("💰 Moneda utilizada para el pago", ["USD", "UYU"])
            precio = self._get_validated_float(f"💵 Precio por USDT en {moneda}", min_val=0.01)
            plataforma = Prompt.ask("[bold cyan]🏦 Plataforma[/bold cyan] (ej: Binance, KuCoin, Bybit)", default="Binance")
            
            tasa_cambio = 1.0
            if moneda == "UYU":
                tasa_cambio = self._get_validated_float("💱 Tasa de Cambio (1 USD = X UYU)", min_val=0.01)
            
            fuente_fondos = Prompt.ask("[bold cyan]📊 Fuente de Fondos Fiat[/bold cyan]", default="Capital Nuevo")
            comisiones = self._get_validated_float("💸 Comisiones pagadas (en la moneda de pago)", min_val=0.0, default=0.0)
            
            # Cálculo del costo total
            costo_total = cantidad * precio + comisiones
            
            # Mostrar resumen
            self._show_transaction_summary("COMPRA", {
                "ID": nuevo_id,
                "Cantidad USDT": f"{cantidad:.2f}",
                "Moneda": moneda,
                "Precio por USDT": f"{precio:.4f} {moneda}",
                "Plataforma": plataforma.capitalize(),
                "Tasa Cambio": f"{tasa_cambio:.2f}" if moneda == "UYU" else "N/A",
                "Comisiones": f"{comisiones:.2f} {moneda}",
                "Fuente de Fondos": fuente_fondos,
                "Costo Total": f"{costo_total:.2f} {moneda}"
            })
            
            if Confirm.ask("[bold green]¿Confirmas guardar esta compra?[/bold green]"):
                self.guardar_compra_simple(nuevo_id, cantidad, moneda, precio, plataforma.lower(), 
                                         comisiones, tasa_cambio, fuente_fondos)
                self.show_success_message("¡Compra guardada exitosamente!")
            else:
                self.show_info_message("Compra cancelada por el usuario.")
                
        except KeyboardInterrupt:
            self.show_info_message("Operación cancelada por el usuario.")
        except Exception as e:
            self.show_error_message(f"Error inesperado: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def form_venta_rich(self):
        """Formulario de venta con Rich completo"""
        self.show_section_header("📉 REGISTRAR NUEVA VENTA", "Inicio > Gestión > Nueva Venta")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('venta')
            nuevo_id = f"V{ultimo_id + 1:03d}"
            
            id_panel = Panel(
                f"[bold red]ID de Venta Asignado: {nuevo_id}[/bold red]",
                style="red",
                box=box.ROUNDED
            )
            self.console.print(id_panel)
            self.console.print()
            
            # Formulario paso a paso con validaciones
            cantidad = self._get_validated_float("💰 Cantidad de USDT vendidos", min_val=0.01)
            moneda = self._get_validated_choice("💵 Moneda recibida", ["USD", "UYU"])
            precio = self._get_validated_float(f"💸 Precio por USDT en {moneda}", min_val=0.01)
            plataforma = Prompt.ask("[bold cyan]🏦 Plataforma[/bold cyan] (ej: Binance, P2P, WhatsApp)", default="P2P")
            
            tasa_cambio = 1.0
            if moneda == "UYU":
                tasa_cambio = self._get_validated_float("💱 Tasa de Cambio (1 USD = X UYU)", min_val=0.01)
            
            comisiones = self._get_validated_float("💸 Comisiones pagadas (en la moneda recibida)", min_val=0.0, default=0.0)
            
            # Cálculo del ingreso neto
            ingreso_bruto = cantidad * precio
            ingreso_neto = ingreso_bruto - comisiones
            
            # Mostrar resumen
            self._show_transaction_summary("VENTA", {
                "ID": nuevo_id,
                "Cantidad USDT": f"{cantidad:.2f}",
                "Moneda Recibida": moneda,
                "Precio por USDT": f"{precio:.4f} {moneda}",
                "Plataforma": plataforma.capitalize(),
                "Tasa Cambio": f"{tasa_cambio:.2f}" if moneda == "UYU" else "N/A",
                "Comisiones": f"{comisiones:.2f} {moneda}",
                "Ingreso Bruto": f"{ingreso_bruto:.2f} {moneda}",
                "Ingreso Neto": f"{ingreso_neto:.2f} {moneda}"
            })
            
            if Confirm.ask("[bold green]¿Confirmas guardar esta venta?[/bold green]"):
                self.guardar_venta_simple(nuevo_id, cantidad, moneda, precio, plataforma.lower(), 
                                        comisiones, tasa_cambio)
                self.show_success_message("¡Venta guardada exitosamente!")
            else:
                self.show_info_message("Venta cancelada por el usuario.")
                
        except KeyboardInterrupt:
            self.show_info_message("Operación cancelada por el usuario.")
        except Exception as e:
            self.show_error_message(f"Error inesperado: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def form_conversion_rich(self):
        """Formulario de conversión fiat con Rich completo"""
        self.show_section_header("🔄 REGISTRAR NUEVA CONVERSIÓN FIAT", "Inicio > Gestión > Nueva Conversión")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('conversion')
            nuevo_id = f"CF{ultimo_id + 1:03d}"
            
            id_panel = Panel(
                f"[bold yellow]ID de Conversión Asignado: {nuevo_id}[/bold yellow]",
                style="yellow",
                box=box.ROUNDED
            )
            self.console.print(id_panel)
            self.console.print()
            
            # Formulario paso a paso con validaciones
            moneda_origen = self._get_validated_choice("💱 Moneda de origen", ["UYU", "USD"])
            cantidad_origen = self._get_validated_float(f"💰 Cantidad en {moneda_origen}", min_val=0.01)
            
            moneda_destino = "USD" if moneda_origen == "UYU" else "UYU"
            self.show_info_message(f"Moneda de destino: {moneda_destino}")
            
            cantidad_destino = self._get_validated_float(f"💵 Cantidad recibida en {moneda_destino}", min_val=0.01)
            
            # Calcular tasa de conversión implícita
            if moneda_origen == "UYU":
                tasa_conversion = cantidad_origen / cantidad_destino
            else:
                tasa_conversion = cantidad_destino / cantidad_origen
            
            # ID de venta asociada (opcional)
            id_venta_asociada = Prompt.ask("[bold cyan]🔗 ID de Venta Asociada[/bold cyan] (opcional, ej: V001)", default="")
            
            notas = Prompt.ask("[bold cyan]📝 Notas[/bold cyan] (opcional)", default="Conversión manual")
            
            # Mostrar resumen
            self._show_transaction_summary("CONVERSIÓN", {
                "ID": nuevo_id,
                "Moneda Origen": moneda_origen,
                "Cantidad Origen": f"{cantidad_origen:.2f} {moneda_origen}",
                "Moneda Destino": moneda_destino,
                "Cantidad Destino": f"{cantidad_destino:.2f} {moneda_destino}",
                "Tasa Conversión": f"{tasa_conversion:.4f}",
                "Venta Asociada": id_venta_asociada if id_venta_asociada else "N/A",
                "Notas": notas
            })
            
            if Confirm.ask("[bold green]¿Confirmas guardar esta conversión?[/bold green]"):
                self.guardar_conversion_simple(nuevo_id, moneda_origen, cantidad_origen, 
                                             moneda_destino, cantidad_destino, tasa_conversion,
                                             id_venta_asociada, notas)
                self.show_success_message("¡Conversión guardada exitosamente!")
            else:
                self.show_info_message("Conversión cancelada por el usuario.")
                
        except KeyboardInterrupt:
            self.show_info_message("Operación cancelada por el usuario.")
        except Exception as e:
            self.show_error_message(f"Error inesperado: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def guardar_conversion_simple(self, id_conversion: str, moneda_origen: str, cantidad_origen: float,
                                moneda_destino: str, cantidad_destino: float, tasa_conversion: float,
                                id_venta_asociada: str, notas: str):
        """Guarda una conversión simple"""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_conversion = {
            'ID_Conversion': id_conversion,
            'Fecha_Conversion': fecha_actual,
            'Moneda_Origen': moneda_origen,
            'Cantidad_Origen': cantidad_origen,
            'Moneda_Destino': moneda_destino,
            'Cantidad_Destino': cantidad_destino,
            'Tasa_Conversion_Implicita': tasa_conversion,
            'ID_Venta_Asociada': id_venta_asociada if id_venta_asociada else "",
            'Notas': notas
        }
        
        # Cargar datos existentes o crear nuevo DataFrame
        if os.path.exists(CONVERSIONES_CSV):
            df_conversiones = pd.read_csv(CONVERSIONES_CSV)
            df_conversiones = pd.concat([df_conversiones, pd.DataFrame([nueva_conversion])], ignore_index=True)
        else:
            df_conversiones = pd.DataFrame([nueva_conversion])
        
        df_conversiones.to_csv(CONVERSIONES_CSV, index=False)
        self.datos['conversiones'].append(nueva_conversion)
        self.data_loaded = True

    def ver_datos_actuales_rich(self):
        """Ver datos actuales con Rich"""
        self.show_section_header("📋 TODOS LOS DATOS ACTUALES", "Inicio > Gestión > Ver Datos")
        
        self.cargar_datos_rapido()
        
        if not self.data_loaded:
            self.show_error_message("No se pudieron cargar los datos")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return
        
        # Mostrar compras
        if self.datos['compras']:
            df_compras = pd.DataFrame(self.datos['compras'])
            self.display_dataframe_table(df_compras, "📈 COMPRAS DE USDT")
        
        # Mostrar ventas
        if self.datos['ventas']:
            df_ventas = pd.DataFrame(self.datos['ventas'])
            self.display_dataframe_table(df_ventas, "📉 VENTAS DE USDT")
        
        # Mostrar conversiones
        if self.datos['conversiones']:
            df_conversiones = pd.DataFrame(self.datos['conversiones'])
            self.display_dataframe_table(df_conversiones, "🔄 CONVERSIONES FIAT")
        
        if not any([self.datos['compras'], self.datos['ventas'], self.datos['conversiones']]):
            self.show_info_message("No hay datos para mostrar. Registra algunas transacciones primero.")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_resumen(self):
        """Menú de resumen financiero completo"""
        self.show_section_header("📊 RESUMEN FINANCIERO GLOBAL", "Inicio > Resumen")
        
        self.cargar_datos_rapido()
        
        if not self.data_loaded:
            self.show_error_message("No se pudieron cargar los datos")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return
        
        # Calcular métricas básicas
        metricas = self._calcular_metricas_financieras()
        
        if not metricas:
            self.show_info_message("No hay datos suficientes para calcular métricas financieras")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return
        
        # Mostrar métricas principales
        self._mostrar_panel_metricas_principales(metricas)
        
        # Mostrar resumen por plataforma
        self._mostrar_resumen_por_plataforma()
        
        # Mostrar últimas transacciones
        self._mostrar_ultimas_transacciones()
        
        Prompt.ask("\n[bold bright_yellow]Presiona Enter para volver al menú principal[/bold bright_yellow]")

    def _calcular_metricas_financieras(self):
        """Calcula métricas financieras básicas"""
        try:
            compras = self.datos.get('compras', [])
            ventas = self.datos.get('ventas', [])
            conversiones = self.datos.get('conversiones', [])
            
            if not compras and not ventas:
                return None
            
            # Cálculos básicos de compras
            total_usdt_comprado = sum(float(c.get('Cantidad_USDT_Comprada', 0)) for c in compras)
            inversion_total_usd = 0
            
            for compra in compras:
                cantidad = float(compra.get('Cantidad_USDT_Comprada', 0))
                precio = float(compra.get('Precio_Unitario_Moneda_Pago', 0))
                moneda = compra.get('Moneda_Pago', 'USD')
                tasa = float(compra.get('Tasa_Cambio_UYU_USD_Compra', 1))
                comisiones = float(compra.get('Comisiones_Compra_Moneda_Pago', 0))
                
                costo_total = (cantidad * precio) + comisiones
                if moneda == 'UYU':
                    costo_total = costo_total / tasa
                inversion_total_usd += costo_total
            
            # Cálculos básicos de ventas
            total_usdt_vendido = sum(float(v.get('Cantidad_USDT_Vendida', 0)) for v in ventas)
            ingresos_total_usd = 0
            
            for venta in ventas:
                cantidad = float(venta.get('Cantidad_USDT_Vendida', 0))
                precio = float(venta.get('Precio_Unitario_Moneda_Recibida', 0))
                moneda = venta.get('Moneda_Recibida', 'USD')
                tasa = float(venta.get('Tasa_Cambio_UYU_USD_Venta', 1))
                comisiones = float(venta.get('Comisiones_Venta_Moneda_Recibida', 0))
                
                ingreso_neto = (cantidad * precio) - comisiones
                if moneda == 'UYU':
                    ingreso_neto = ingreso_neto / tasa
                ingresos_total_usd += ingreso_neto
            
            # Cálculo de métricas
            usdt_en_inventario = total_usdt_comprado - total_usdt_vendido
            cpp_promedio = inversion_total_usd / total_usdt_comprado if total_usdt_comprado > 0 else 0
            pl_realizado = ingresos_total_usd - (total_usdt_vendido * cpp_promedio) if total_usdt_vendido > 0 else 0
            roi_porcentaje = (pl_realizado / inversion_total_usd * 100) if inversion_total_usd > 0 else 0
            
            return {
                'total_compras': len(compras),
                'total_ventas': len(ventas),
                'total_conversiones': len(conversiones),
                'total_usdt_comprado': total_usdt_comprado,
                'total_usdt_vendido': total_usdt_vendido,
                'usdt_en_inventario': usdt_en_inventario,
                'inversion_total_usd': inversion_total_usd,
                'ingresos_total_usd': ingresos_total_usd,
                'cpp_promedio': cpp_promedio,
                'pl_realizado': pl_realizado,
                'roi_porcentaje': roi_porcentaje
            }
        except Exception as e:
            self.show_error_message(f"Error al calcular métricas: {e}")
            return None

    def _mostrar_panel_metricas_principales(self, metricas):
        """Muestra el panel principal de métricas"""
        # Crear tabla de métricas principales
        metricas_table = Table(show_header=False, box=None, padding=(0, 2))
        metricas_table.add_column("Métrica", style="bold white", width=25)
        metricas_table.add_column("Valor", style="bold", justify="right", width=20)
        metricas_table.add_column("Métrica", style="bold white", width=25)
        metricas_table.add_column("Valor", style="bold", justify="right", width=20)
        
        # Fila 1
        metricas_table.add_row(
            "💰 P&L Realizado:",
            f"[{'green' if metricas['pl_realizado'] >= 0 else 'red'}]${metricas['pl_realizado']:,.2f} USD[/{'green' if metricas['pl_realizado'] >= 0 else 'red'}]",
            "📈 ROI:",
            f"[{'green' if metricas['roi_porcentaje'] >= 0 else 'red'}]{metricas['roi_porcentaje']:,.2f}%[/{'green' if metricas['roi_porcentaje'] >= 0 else 'red'}]"
        )
        
        # Fila 2
        metricas_table.add_row(
            "🪙 USDT en Inventario:",
            f"[cyan]{metricas['usdt_en_inventario']:,.2f} USDT[/cyan]",
            "💵 CPP Promedio:",
            f"[yellow]${metricas['cpp_promedio']:,.4f} USD[/yellow]"
        )
        
        # Fila 3
        metricas_table.add_row(
            "📊 Inversión Total:",
            f"[blue]${metricas['inversion_total_usd']:,.2f} USD[/blue]",
            "💸 Ingresos Totales:",
            f"[green]${metricas['ingresos_total_usd']:,.2f} USD[/green]"
        )
        
        # Fila 4
        metricas_table.add_row(
            "🛍️ Total Compras:",
            f"[cyan]{metricas['total_compras']}[/cyan]",
            "💸 Total Ventas:",
            f"[magenta]{metricas['total_ventas']}[/magenta]"
        )
        
        panel_metricas = Panel(
            metricas_table,
            title="[bold bright_green]💰 MÉTRICAS FINANCIERAS PRINCIPALES[/bold bright_green]",
            style="green",
            box=box.ROUNDED
        )
        
        self.console.print(panel_metricas)
        self.console.print()

    def _mostrar_resumen_por_plataforma(self):
        """Muestra resumen agrupado por plataforma"""
        try:
            # Agrupar compras por plataforma
            compras_por_plataforma = {}
            for compra in self.datos.get('compras', []):
                plataforma = compra.get('Plataforma', 'Desconocida').title()
                if plataforma not in compras_por_plataforma:
                    compras_por_plataforma[plataforma] = {'cantidad': 0, 'costo': 0}
                
                cantidad = float(compra.get('Cantidad_USDT_Comprada', 0))
                precio = float(compra.get('Precio_Unitario_Moneda_Pago', 0))
                moneda = compra.get('Moneda_Pago', 'USD')
                tasa = float(compra.get('Tasa_Cambio_UYU_USD_Compra', 1))
                
                costo = cantidad * precio
                if moneda == 'UYU':
                    costo = costo / tasa
                
                compras_por_plataforma[plataforma]['cantidad'] += cantidad
                compras_por_plataforma[plataforma]['costo'] += costo
            
            # Agrupar ventas por plataforma
            ventas_por_plataforma = {}
            for venta in self.datos.get('ventas', []):
                plataforma = venta.get('Plataforma', 'Desconocida').title()
                if plataforma not in ventas_por_plataforma:
                    ventas_por_plataforma[plataforma] = {'cantidad': 0, 'ingreso': 0}
                
                cantidad = float(venta.get('Cantidad_USDT_Vendida', 0))
                precio = float(venta.get('Precio_Unitario_Moneda_Recibida', 0))
                moneda = venta.get('Moneda_Recibida', 'USD')
                tasa = float(venta.get('Tasa_Cambio_UYU_USD_Venta', 1))
                
                ingreso = cantidad * precio
                if moneda == 'UYU':
                    ingreso = ingreso / tasa
                
                ventas_por_plataforma[plataforma]['cantidad'] += cantidad
                ventas_por_plataforma[plataforma]['ingreso'] += ingreso
            
            # Crear tabla de resumen por plataforma
            plataforma_table = Table(
                title="[bold]📊 RESUMEN POR PLATAFORMA[/bold]",
                box=box.ROUNDED,
                header_style="bold magenta"
            )
            
            plataforma_table.add_column("Plataforma", style="cyan", width=15)
            plataforma_table.add_column("Compras USDT", style="blue", justify="right", width=15)
            plataforma_table.add_column("Ventas USDT", style="green", justify="right", width=15)
            plataforma_table.add_column("Costo USD", style="yellow", justify="right", width=15)
            plataforma_table.add_column("Ingreso USD", style="green", justify="right", width=15)
            
            # Obtener todas las plataformas únicas
            todas_plataformas = set(compras_por_plataforma.keys()) | set(ventas_por_plataforma.keys())
            
            for plataforma in sorted(todas_plataformas):
                compras_data = compras_por_plataforma.get(plataforma, {'cantidad': 0, 'costo': 0})
                ventas_data = ventas_por_plataforma.get(plataforma, {'cantidad': 0, 'ingreso': 0})
                
                plataforma_table.add_row(
                    plataforma,
                    f"{compras_data['cantidad']:,.2f}" if compras_data['cantidad'] > 0 else "[dim]0.00[/dim]",
                    f"{ventas_data['cantidad']:,.2f}" if ventas_data['cantidad'] > 0 else "[dim]0.00[/dim]",
                    f"${compras_data['costo']:,.2f}" if compras_data['costo'] > 0 else "[dim]$0.00[/dim]",
                    f"${ventas_data['ingreso']:,.2f}" if ventas_data['ingreso'] > 0 else "[dim]$0.00[/dim]"
                )
            
            self.console.print(plataforma_table)
            self.console.print()
            
        except Exception as e:
            self.show_error_message(f"Error al calcular resumen por plataforma: {e}")

    def _mostrar_ultimas_transacciones(self):
        """Muestra las últimas transacciones"""
        try:
            # Combinar y ordenar todas las transacciones por fecha
            todas_transacciones = []
            
            for compra in self.datos.get('compras', []):
                todas_transacciones.append({
                    'tipo': 'Compra',
                    'id': compra.get('ID_Compra', ''),
                    'fecha': compra.get('Fecha_Compra', ''),
                    'cantidad': float(compra.get('Cantidad_USDT_Comprada', 0)),
                    'plataforma': compra.get('Plataforma', '').title()
                })
            
            for venta in self.datos.get('ventas', []):
                todas_transacciones.append({
                    'tipo': 'Venta',
                    'id': venta.get('ID_Venta', ''),
                    'fecha': venta.get('Fecha_Venta', ''),
                    'cantidad': float(venta.get('Cantidad_USDT_Vendida', 0)),
                    'plataforma': venta.get('Plataforma', '').title()
                })
            
            # Ordenar por fecha (más recientes primero)
            todas_transacciones.sort(key=lambda x: x['fecha'], reverse=True)
            
            # Mostrar últimas 10 transacciones
            ultimas_table = Table(
                title="[bold]🕒 ÚLTIMAS TRANSACCIONES[/bold]",
                box=box.ROUNDED,
                header_style="bold blue"
            )
            
            ultimas_table.add_column("Tipo", style="white", width=8)
            ultimas_table.add_column("ID", style="cyan", width=8)
            ultimas_table.add_column("Fecha", style="blue", width=20)
            ultimas_table.add_column("Cantidad USDT", style="green", justify="right", width=15)
            ultimas_table.add_column("Plataforma", style="yellow", width=12)
            
            for transaccion in todas_transacciones[:10]:
                tipo_color = "green" if transaccion['tipo'] == 'Compra' else "red"
                tipo_icon = "📈" if transaccion['tipo'] == 'Compra' else "📉"
                
                ultimas_table.add_row(
                    f"[{tipo_color}]{tipo_icon} {transaccion['tipo']}[/{tipo_color}]",
                    transaccion['id'],
                    transaccion['fecha'][:16] if len(transaccion['fecha']) > 16 else transaccion['fecha'],
                    f"{transaccion['cantidad']:,.2f}",
                    transaccion['plataforma']
                )
            
            self.console.print(ultimas_table)
            
        except Exception as e:
            self.show_error_message(f"Error al mostrar últimas transacciones: {e}")

    def menu_analisis(self):
        """Menú de análisis detallado"""
        while True:
            self.show_section_header("📈 ANÁLISIS DETALLADO POR CATEGORÍA", "Inicio > Análisis")
            
            menu_items = [
                ("1️⃣", "📊 Análisis por Plataforma Detallado", "info"),
                ("2️⃣", "📈 Análisis Temporal (por Mes)", "success"),
                ("3️⃣", "💰 Análisis de Rentabilidad", "warning"),
                ("4️⃣", "🔄 Análisis de Conversiones Fiat", "primary"),
                ("5️⃣", "⬅️ Volver al Menú Principal", "muted")
            ]
            
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Opción", style="bold bright_yellow", width=6)
            menu_table.add_column("Descripción", style="bold")
            
            for option, description, style_type in menu_items:
                color = self.theme_colors.get(style_type, "white")
                menu_table.add_row(option, f"[{color}]{description}[/{color}]")
            
            menu_panel = Panel(
                menu_table,
                title="[bold bright_blue]📈 OPCIONES DE ANÁLISIS[/bold bright_blue]",
                style="blue",
                box=box.ROUNDED
            )
            
            self.console.print(menu_panel)
            
            choice = self.get_user_choice()
            
            if choice == "1":
                self._analisis_por_plataforma_detallado()
            elif choice == "2":
                self._analisis_temporal()
            elif choice == "3":
                self._analisis_rentabilidad()
            elif choice == "4":
                self._analisis_conversiones()
            elif choice == "5":
                break
            else:
                self.show_error_message("Opción inválida. Intenta de nuevo.")
                Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _analisis_por_plataforma_detallado(self):
        """Análisis detallado por plataforma"""
        self.show_section_header("📊 ANÁLISIS POR PLATAFORMA DETALLADO", "Inicio > Análisis > Por Plataforma")
        
        self.cargar_datos_rapido()
        
        if not self.data_loaded or (not self.datos.get('compras') and not self.datos.get('ventas')):
            self.show_info_message("No hay datos suficientes para el análisis por plataforma")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return
        
        try:
            # Análisis detallado por plataforma
            analisis_plataforma = {}
            
            # Procesar compras
            for compra in self.datos.get('compras', []):
                plataforma = compra.get('Plataforma', 'Desconocida').title()
                if plataforma not in analisis_plataforma:
                    analisis_plataforma[plataforma] = {
                        'compras_count': 0, 'ventas_count': 0,
                        'usdt_comprado': 0, 'usdt_vendido': 0,
                        'costo_total': 0, 'ingreso_total': 0,
                        'cpp_promedio': 0, 'precio_venta_promedio': 0
                    }
                
                cantidad = float(compra.get('Cantidad_USDT_Comprada', 0))
                precio = float(compra.get('Precio_Unitario_Moneda_Pago', 0))
                moneda = compra.get('Moneda_Pago', 'USD')
                tasa = float(compra.get('Tasa_Cambio_UYU_USD_Compra', 1))
                comisiones = float(compra.get('Comisiones_Compra_Moneda_Pago', 0))
                
                costo_total = (cantidad * precio) + comisiones
                if moneda == 'UYU':
                    costo_total = costo_total / tasa
                
                analisis_plataforma[plataforma]['compras_count'] += 1
                analisis_plataforma[plataforma]['usdt_comprado'] += cantidad
                analisis_plataforma[plataforma]['costo_total'] += costo_total
            
            # Procesar ventas
            for venta in self.datos.get('ventas', []):
                plataforma = venta.get('Plataforma', 'Desconocida').title()
                if plataforma not in analisis_plataforma:
                    analisis_plataforma[plataforma] = {
                        'compras_count': 0, 'ventas_count': 0,
                        'usdt_comprado': 0, 'usdt_vendido': 0,
                        'costo_total': 0, 'ingreso_total': 0,
                        'cpp_promedio': 0, 'precio_venta_promedio': 0
                    }
                
                cantidad = float(venta.get('Cantidad_USDT_Vendida', 0))
                precio = float(venta.get('Precio_Unitario_Moneda_Recibida', 0))
                moneda = venta.get('Moneda_Recibida', 'USD')
                tasa = float(venta.get('Tasa_Cambio_UYU_USD_Venta', 1))
                comisiones = float(venta.get('Comisiones_Venta_Moneda_Recibida', 0))
                
                ingreso_neto = (cantidad * precio) - comisiones
                if moneda == 'UYU':
                    ingreso_neto = ingreso_neto / tasa
                
                analisis_plataforma[plataforma]['ventas_count'] += 1
                analisis_plataforma[plataforma]['usdt_vendido'] += cantidad
                analisis_plataforma[plataforma]['ingreso_total'] += ingreso_neto
            
            # Calcular promedios y métricas
            for plataforma, data in analisis_plataforma.items():
                if data['usdt_comprado'] > 0:
                    data['cpp_promedio'] = data['costo_total'] / data['usdt_comprado']
                if data['usdt_vendido'] > 0:
                    data['precio_venta_promedio'] = data['ingreso_total'] / data['usdt_vendido']
            
            # Crear tabla de análisis detallado
            analisis_table = Table(
                title="[bold]📊 ANÁLISIS DETALLADO POR PLATAFORMA[/bold]",
                box=box.ROUNDED,
                header_style="bold magenta",
                show_lines=True
            )
            
            analisis_table.add_column("Plataforma", style="cyan", width=12)
            analisis_table.add_column("Compras", style="blue", justify="center", width=8)
            analisis_table.add_column("Ventas", style="green", justify="center", width=8)
            analisis_table.add_column("USDT Comprado", style="yellow", justify="right", width=15)
            analisis_table.add_column("USDT Vendido", style="red", justify="right", width=15)
            analisis_table.add_column("CPP Promedio", style="blue", justify="right", width=12)
            analisis_table.add_column("Precio Venta Prom.", style="green", justify="right", width=16)
            
            for plataforma in sorted(analisis_plataforma.keys()):
                data = analisis_plataforma[plataforma]
                analisis_table.add_row(
                    plataforma,
                    str(data['compras_count']),
                    str(data['ventas_count']),
                    f"{data['usdt_comprado']:,.2f}",
                    f"{data['usdt_vendido']:,.2f}",
                    f"${data['cpp_promedio']:,.4f}" if data['cpp_promedio'] > 0 else "[dim]N/A[/dim]",
                    f"${data['precio_venta_promedio']:,.4f}" if data['precio_venta_promedio'] > 0 else "[dim]N/A[/dim]"
                )
            
            self.console.print(analisis_table)
            
        except Exception as e:
            self.show_error_message(f"Error en análisis por plataforma: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _analisis_temporal(self):
        """Análisis temporal por mes"""
        self.show_section_header("📈 ANÁLISIS TEMPORAL (POR MES)", "Inicio > Análisis > Temporal")
        self.show_info_message("Análisis temporal por mes - Funcionalidad avanzada en desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _analisis_rentabilidad(self):
        """Análisis de rentabilidad"""
        self.show_section_header("💰 ANÁLISIS DE RENTABILIDAD", "Inicio > Análisis > Rentabilidad")
        self.show_info_message("Análisis de rentabilidad detallado - Funcionalidad avanzada en desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _analisis_conversiones(self):
        """Análisis de conversiones fiat"""
        self.show_section_header("🔄 ANÁLISIS DE CONVERSIONES FIAT", "Inicio > Análisis > Conversiones")
        
        self.cargar_datos_rapido()
        
        if not self.datos.get('conversiones'):
            self.show_info_message("No hay conversiones registradas para analizar")
            Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")
            return
        
        df_conversiones = pd.DataFrame(self.datos['conversiones'])
        self.display_dataframe_table(df_conversiones, "🔄 CONVERSIONES FIAT REGISTRADAS")

    def menu_herramientas(self):
        """Menú de herramientas y utilidades"""
        while True:
            self.show_section_header("🔧 HERRAMIENTAS Y UTILIDADES", "Inicio > Herramientas")
            
            menu_items = [
                ("1️⃣", "📁 Estado de Archivos de Datos", "info"),
                ("2️⃣", "🗂️ Crear Backup de Datos", "warning"),
                ("3️⃣", "📊 Ejecutar Script Principal (Cálculos CPP)", "success"),
                ("4️⃣", "🧹 Validar y Limpiar Datos", "primary"),
                ("5️⃣", "⬅️ Volver al Menú Principal", "muted")
            ]
            
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Opción", style="bold bright_yellow", width=6)
            menu_table.add_column("Descripción", style="bold")
            
            for option, description, style_type in menu_items:
                color = self.theme_colors.get(style_type, "white")
                menu_table.add_row(option, f"[{color}]{description}[/{color}]")
            
            menu_panel = Panel(
                menu_table,
                title="[bold bright_yellow]🔧 HERRAMIENTAS DISPONIBLES[/bold bright_yellow]",
                style="yellow",
                box=box.ROUNDED
            )
            
            self.console.print(menu_panel)
            
            choice = self.get_user_choice()
            
            if choice == "1":
                self._mostrar_estado_archivos()
            elif choice == "2":
                self._crear_backup()
            elif choice == "3":
                self._ejecutar_script_principal()
            elif choice == "4":
                self._validar_datos()
            elif choice == "5":
                break
            else:
                self.show_error_message("Opción inválida. Intenta de nuevo.")
                Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _mostrar_estado_archivos(self):
        """Muestra el estado de los archivos de datos"""
        self.show_section_header("📁 ESTADO DE ARCHIVOS DE DATOS", "Inicio > Herramientas > Estado Archivos")
        
        archivos_estado = [
            ("compras_usdt.csv", COMPRAS_CSV),
            ("ventas_usdt.csv", VENTAS_CSV),
            ("conversiones_fiat.csv", CONVERSIONES_CSV)
        ]
        
        estado_table = Table(
            title="[bold]📁 ESTADO DE ARCHIVOS[/bold]",
            box=box.ROUNDED,
            header_style="bold blue"
        )
        
        estado_table.add_column("Archivo", style="cyan", width=20)
        estado_table.add_column("Estado", style="white", width=10)
        estado_table.add_column("Registros", style="green", justify="right", width=12)
        estado_table.add_column("Tamaño", style="yellow", justify="right", width=12)
        estado_table.add_column("Última Modificación", style="blue", width=20)
        
        for nombre, ruta in archivos_estado:
            if os.path.exists(ruta):
                try:
                    df = pd.read_csv(ruta)
                    registros = len(df)
                    tamaño = os.path.getsize(ruta)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(ruta)).strftime("%Y-%m-%d %H:%M")
                    
                    estado_table.add_row(
                        nombre,
                        "[green]✅ Existe[/green]",
                        str(registros),
                        f"{tamaño} bytes",
                        mod_time
                    )
                except Exception as e:
                    estado_table.add_row(
                        nombre,
                        "[yellow]⚠️ Error[/yellow]",
                        "N/A",
                        "N/A",
                        str(e)[:20]
                    )
            else:
                estado_table.add_row(
                    nombre,
                    "[red]❌ No existe[/red]",
                    "0",
                    "0 bytes",
                    "N/A"
                )
        
        self.console.print(estado_table)
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _crear_backup(self):
        """Crea un backup de los datos"""
        self.show_section_header("🗂️ CREAR BACKUP DE DATOS", "Inicio > Herramientas > Backup")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(BACKUPS_DIR, f"backup_{timestamp}")
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            archivos_backup = [
                ("compras_usdt.csv", COMPRAS_CSV),
                ("ventas_usdt.csv", VENTAS_CSV),
                ("conversiones_fiat.csv", CONVERSIONES_CSV)
            ]
            
            archivos_copiados = 0
            for nombre, origen in archivos_backup:
                if os.path.exists(origen):
                    destino = os.path.join(backup_dir, nombre)
                    import shutil
                    shutil.copy2(origen, destino)
                    archivos_copiados += 1
            
            if archivos_copiados > 0:
                self.show_success_message(f"Backup creado exitosamente en: {backup_dir}")
                self.show_info_message(f"Archivos respaldados: {archivos_copiados}")
            else:
                self.show_info_message("No hay archivos para respaldar")
                
        except Exception as e:
            self.show_error_message(f"Error al crear backup: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _ejecutar_script_principal(self):
        """Ejecuta el script principal para cálculos CPP"""
        self.show_section_header("📊 EJECUTAR SCRIPT PRINCIPAL", "Inicio > Herramientas > Script Principal")
        self.show_info_message("Funcionalidad para ejecutar script_p2p_tracker.py - En desarrollo")
        self.show_info_message("Esta función ejecutará los cálculos CPP completos y generará reportes")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _validar_datos(self):
        """Valida y limpia los datos"""
        self.show_section_header("🧹 VALIDAR Y LIMPIAR DATOS", "Inicio > Herramientas > Validar")
        self.show_info_message("Funcionalidad de validación y limpieza de datos - En desarrollo")
        self.show_info_message("Esta función verificará la integridad de los datos y corregirá errores comunes")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

def main():
    """Función principal"""
    try:
        dashboard = P2PDashboardRich()
        dashboard.run_main_loop()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold red]👋 ¡Hasta luego![/bold red]")
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]❌ Error inesperado: {e}[/bold red]")

if __name__ == "__main__":
    main() 