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
from script_p2p_tracker import crear_archivos_ejemplo as crear_ejemplos_desde_tracker

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
        
        header_panel = Panel(
            Align.center(Columns([header_text, subtitle], align="center")),
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
        
        # Crear tabla de estado
        status_table = Table(show_header=False, box=None, padding=(0, 1))
        status_table.add_column("Métrica", style="bold")
        status_table.add_column("Valor", justify="right")
        
        status_table.add_row("🛍️ Compras Registradas:", f"[bold cyan]{num_compras}[/bold cyan]")
        status_table.add_row("💸 Ventas Registradas:", f"[bold green]{num_ventas}[/bold green]")
        status_table.add_row("🔄 Conversiones Fiat:", f"[bold yellow]{num_conversiones}[/bold yellow]")
        
        # Estado general
        if num_compras > 0 or num_ventas > 0 or num_conversiones > 0:
            status_message = Text("🎉 ¡Datos cargados! Listo para análisis.", style="bold green")
        else:
            status_message = Text("⚠️ Sin datos. Usa 'Gestionar Datos' para iniciar.", style="bold yellow")
        
        # Panel principal de estado
        status_content = Columns([
            status_table,
            Padding(status_message, (2, 0, 0, 0))
        ])
        
        status_panel = Panel(
            status_content,
            title="[bold]📊 ESTADO RÁPIDO[/bold]",
            style="bright_blue",
            box=box.ROUNDED
        )
        
        self.console.print(status_panel)
        self.console.print()

    def show_main_menu(self):
        """Muestra el menú principal elegante"""
        menu_items = [
            ("1️⃣", "📝 Gestionar Datos de Transacciones", "primary"),
            ("2️⃣", "📊 Ver Resumen Financiero Global", "info"),
            ("3️⃣", "📈 Análisis Detallado por Categoría", "success"),
            ("4️⃣", "🔧 Herramientas y Utilidades", "warning"),
            ("5️⃣", "❌ Salir del Dashboard", "error")
        ]
        
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Opción", style="bold", width=4)
        menu_table.add_column("Descripción", style="bold")
        
        for option, description, style_name in menu_items:
            menu_table.add_row(option, f"[{self.theme_colors[style_name]}]{description}[/{self.theme_colors[style_name]}]")
        
        menu_panel = Panel(
            menu_table,
            title="[bold]🏠 MENÚ PRINCIPAL[/bold]",
            style="bright_magenta",
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
            breadcrumb_text = Text(f"📍 {breadcrumb}", style="muted")
            self.console.print(breadcrumb_text)
            self.console.print()
        
        section_panel = Panel(
            Align.center(title),
            style="bright_green",
            box=box.DOUBLE_EDGE
        )
        self.console.print(section_panel)
        self.console.print()

    def display_table_with_pagination(self, df: pd.DataFrame, title: str, max_rows: int = 15):
        """Muestra una tabla con paginación usando Rich Table"""
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
                show_lines=True
            )
            
            # Añadir columnas
            for col in df.columns:
                table.add_column(col, style="white")
            
            # Añadir filas con formato
            df_slice = df.iloc[start_row:end_row]
            for _, row in df_slice.iterrows():
                formatted_row = []
                for col, value in row.items():
                    if pd.isna(value):
                        formatted_row.append("[muted]N/A[/muted]")
                    elif isinstance(value, (int, float)):
                        if 'ganancia' in col.lower() or 'perdida' in col.lower() or 'pl' in col.lower():
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
                self.show_success_message("¡Hasta luego! 👋")
                break
            else:
                self.show_error_message("Opción inválida. Intenta de nuevo.")
                Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_gestionar_datos(self):
        """Menú de gestión de datos"""
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
            menu_table.add_column("Opción", style="bold", width=4)
            menu_table.add_column("Descripción", style="bold")
            
            for option, description, style_name in menu_items:
                menu_table.add_row(option, f"[{self.theme_colors[style_name]}]{description}[/{self.theme_colors[style_name]}]")
            
            menu_panel = Panel(
                menu_table,
                title="[bold]📝 OPCIONES DE GESTIÓN[/bold]",
                style="bright_green",
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
        """Formulario de compra con Rich"""
        self.show_section_header("📈 REGISTRAR NUEVA COMPRA", "Inicio > Gestión > Nueva Compra")
        
        try:
            # ID automático
            ultimo_id = self.obtener_ultimo_id('compra')
            nuevo_id = f"C{ultimo_id + 1:03d}"
            
            self.show_info_message(f"ID de Compra Asignado: {nuevo_id}")
            
            # Formulario paso a paso
            cantidad = self._get_validated_float("🪙 Cantidad de USDT comprados", min_val=0.01)
            moneda = self._get_validated_choice("💰 Moneda utilizada", ["USD", "UYU"])
            precio = self._get_validated_float(f"💵 Precio por USDT en {moneda}", min_val=0.01)
            plataforma = Prompt.ask("🏦 [bold]Plataforma[/bold] (ej: Binance, KuCoin, Bybit)")
            
            tasa_cambio = 1.0
            if moneda == "UYU":
                tasa_cambio = self._get_validated_float("💱 Tasa de Cambio (1 USD = X UYU)", min_val=0.01)
            
            fuente_fondos = Prompt.ask("📊 [bold]Fuente de Fondos Fiat[/bold]", default="Capital Nuevo")
            comisiones = self._get_validated_float("💸 Comisiones en USDT", min_val=0.0, default=0.0)
            
            # Mostrar resumen
            self._show_transaction_summary("COMPRA", {
                "ID": nuevo_id,
                "Cantidad USDT": f"{cantidad:.2f}",
                "Moneda": moneda,
                "Precio por USDT": f"{precio:.2f} {moneda}",
                "Plataforma": plataforma.capitalize(),
                "Tasa Cambio": f"{tasa_cambio:.2f}" if moneda == "UYU" else "N/A",
                "Comisiones": f"{comisiones:.4f} USDT",
                "Fuente de Fondos": fuente_fondos,
                "Costo Total": f"{cantidad * precio:.2f} {moneda}"
            })
            
            if Confirm.ask("[bold green]¿Confirmas guardar esta compra?[/bold green]"):
                self.guardar_compra_simple(nuevo_id, cantidad, moneda, precio, plataforma.lower(), comisiones, tasa_cambio, fuente_fondos)
                self.show_success_message("¡Compra guardada exitosamente!")
            else:
                self.show_info_message("Compra cancelada por el usuario.")
                
        except KeyboardInterrupt:
            self.show_info_message("Operación cancelada por el usuario.")
        except Exception as e:
            self.show_error_message(f"Error inesperado: {e}")
        
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def _get_validated_float(self, prompt: str, min_val: float = None, max_val: float = None, default: float = None) -> float:
        """Obtiene un número flotante validado del usuario"""
        while True:
            try:
                if default is not None:
                    value = Prompt.ask(f"[bold]{prompt}[/bold]", default=str(default))
                else:
                    value = Prompt.ask(f"[bold]{prompt}[/bold]")
                
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
        return Prompt.ask(f"[bold]{prompt}[/bold]", choices=choices)

    def _show_transaction_summary(self, transaction_type: str, data: Dict[str, str]):
        """Muestra un resumen de la transacción antes de guardar"""
        summary_table = Table(show_header=False, box=None, padding=(0, 1))
        summary_table.add_column("Campo", style="bold cyan", width=20)
        summary_table.add_column("Valor", style="white")
        
        for key, value in data.items():
            summary_table.add_row(f"{key}:", value)
        
        summary_panel = Panel(
            summary_table,
            title=f"[bold]📝 RESUMEN DE LA {transaction_type}[/bold]",
            style="bright_yellow",
            box=box.ROUNDED
        )
        
        self.console.print(summary_panel)

    # Métodos de utilidad (simplificados para el espacio)
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

    def guardar_compra_simple(self, id_compra: str, cantidad: float, moneda: str, precio: float, plataforma: str, comisiones: float, tasa_cambio: float, fuente_fondos: str):
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
        self.datos['compras'].append(nueva_compra)
        
        df_compras = pd.DataFrame(self.datos['compras'])
        df_compras.to_csv(COMPRAS_CSV, index=False)
        self.data_loaded = True

    # Placeholders para otros métodos que se implementarían siguiendo el mismo patrón
    def form_venta_rich(self):
        """Formulario de venta con Rich (placeholder)"""
        self.show_info_message("Formulario de venta - En desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def form_conversion_rich(self):
        """Formulario de conversión con Rich (placeholder)"""
        self.show_info_message("Formulario de conversión - En desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def ver_datos_actuales_rich(self):
        """Ver datos actuales con Rich (placeholder)"""
        self.show_info_message("Visualización de datos - En desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_resumen(self):
        """Menú de resumen (placeholder)"""
        self.show_info_message("Menú de resumen - En desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_analisis(self):
        """Menú de análisis (placeholder)"""
        self.show_info_message("Menú de análisis - En desarrollo")
        Prompt.ask("\n[bold]Presiona Enter para continuar[/bold]")

    def menu_herramientas(self):
        """Menú de herramientas (placeholder)"""
        self.show_info_message("Menú de herramientas - En desarrollo")
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