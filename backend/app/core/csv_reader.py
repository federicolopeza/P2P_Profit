#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lector de archivos CSV para P2P Profit
Procesa los archivos de flujo de fiat y ventas P&L
"""

import pandas as pd
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import logging
from typing import List, Dict, Optional, Tuple
import os

from ..schemas.transactions import FiatFlowRecord, SalesPLRecord

logger = logging.getLogger(__name__)


class CSVDataManager:
    """Gestor de datos CSV para P2P Profit"""
    
    def __init__(self, data_dir: str = "../data"):
        """
        Inicializar el gestor de datos CSV
        
        Args:
            data_dir: Directorio donde están los archivos CSV
        """
        self.data_dir = Path(data_dir)
        self.fiat_flow_data: List[FiatFlowRecord] = []
        self.sales_pl_data: List[SalesPLRecord] = []
        self.last_update: Optional[datetime] = None
        
        # Nombres de archivos por defecto
        self.fiat_flow_file = "reporte_flujo_fiat.csv"
        self.sales_pl_file = "reporte_ventas_pl.csv"
    
    def get_csv_paths(self) -> Dict[str, Path]:
        """Obtener rutas de archivos CSV"""
        # Buscar archivos en el directorio raíz del proyecto
        project_root = Path(__file__).parent.parent.parent.parent
        
        paths = {
            "fiat_flow": project_root / self.fiat_flow_file,
            "sales_pl": project_root / self.sales_pl_file
        }
        
        return paths
    
    def check_csv_files(self) -> Dict[str, bool]:
        """Verificar existencia de archivos CSV"""
        paths = self.get_csv_paths()
        status = {}
        
        for name, path in paths.items():
            exists = path.exists()
            status[name] = exists
            if not exists:
                logger.warning(f"Archivo CSV no encontrado: {path}")
            else:
                logger.info(f"Archivo CSV encontrado: {path}")
        
        return status
    
    def load_fiat_flow_data(self) -> List[FiatFlowRecord]:
        """Cargar datos de flujo de fiat desde CSV"""
        try:
            paths = self.get_csv_paths()
            fiat_flow_path = paths["fiat_flow"]
            
            if not fiat_flow_path.exists():
                logger.error(f"Archivo de flujo de fiat no encontrado: {fiat_flow_path}")
                return []
            
            # Leer CSV
            df = pd.read_csv(fiat_flow_path)
            logger.info(f"Cargando {len(df)} registros de flujo de fiat")
            
            # Convertir a objetos Pydantic
            records = []
            for _, row in df.iterrows():
                try:
                    record = FiatFlowRecord(
                        id_venta=str(row['ID_Venta']),
                        moneda_generada=str(row['Moneda_Generada']),
                        monto_neto_generado=Decimal(str(row['Monto_Neto_Generado_Moneda_Original'])),
                        monto_fiat_utilizado=Decimal(str(row['Monto_Fiat_Utilizado_Moneda_Original'])),
                        monto_fiat_disponible=Decimal(str(row['Monto_Fiat_Disponible_Moneda_Original'])),
                        estado_fiat=str(row['Estado_Fiat']),
                        fecha_venta=pd.to_datetime(row['Fecha_Venta']).to_pydatetime()
                    )
                    records.append(record)
                except Exception as e:
                    logger.error(f"Error procesando registro de flujo: {e}")
                    continue
            
            self.fiat_flow_data = records
            logger.info(f"✅ Cargados {len(records)} registros de flujo de fiat")
            return records
            
        except Exception as e:
            logger.error(f"Error cargando datos de flujo de fiat: {e}")
            return []
    
    def load_sales_pl_data(self) -> List[SalesPLRecord]:
        """Cargar datos de P&L de ventas desde CSV"""
        try:
            paths = self.get_csv_paths()
            sales_pl_path = paths["sales_pl"]
            
            if not sales_pl_path.exists():
                logger.error(f"Archivo de P&L de ventas no encontrado: {sales_pl_path}")
                return []
            
            # Leer CSV
            df = pd.read_csv(sales_pl_path)
            logger.info(f"Cargando {len(df)} registros de P&L de ventas")
            
            # Convertir a objetos Pydantic
            records = []
            for _, row in df.iterrows():
                try:
                    record = SalesPLRecord(
                        id_venta=str(row['ID_Venta']),
                        fecha_venta=pd.to_datetime(row['Fecha_Venta']).to_pydatetime(),
                        cantidad_usdt_vendida=Decimal(str(row['Cantidad_USDT_Vendida'])),
                        moneda_recibida=str(row['Moneda_Recibida']),
                        ingreso_total=Decimal(str(row['Ingreso_Total_Moneda_Recibida'])),
                        ingreso_neto_usd=Decimal(str(row['Ingreso_Neto_en_USD'])),
                        costo_base_usd=Decimal(str(row['Costo_Base_USD_de_USDT_Vendido'])),
                        ganancia_perdida_usd=Decimal(str(row['Ganancia_Perdida_USDT_en_USD']))
                    )
                    records.append(record)
                except Exception as e:
                    logger.error(f"Error procesando registro de P&L: {e}")
                    continue
            
            self.sales_pl_data = records
            logger.info(f"✅ Cargados {len(records)} registros de P&L de ventas")
            return records
            
        except Exception as e:
            logger.error(f"Error cargando datos de P&L de ventas: {e}")
            return []
    
    def reload_all_data(self) -> Dict[str, any]:
        """Recargar todos los datos CSV"""
        start_time = datetime.now()
        results = {
            "archivos_procesados": [],
            "registros_cargados": {},
            "errores": []
        }
        
        try:
            # Verificar archivos
            file_status = self.check_csv_files()
            
            # Cargar flujo de fiat
            if file_status.get("fiat_flow", False):
                fiat_records = self.load_fiat_flow_data()
                results["archivos_procesados"].append("reporte_flujo_fiat.csv")
                results["registros_cargados"]["fiat_flow"] = len(fiat_records)
            else:
                results["errores"].append("Archivo de flujo de fiat no encontrado")
            
            # Cargar P&L de ventas
            if file_status.get("sales_pl", False):
                pl_records = self.load_sales_pl_data()
                results["archivos_procesados"].append("reporte_ventas_pl.csv")
                results["registros_cargados"]["sales_pl"] = len(pl_records)
            else:
                results["errores"].append("Archivo de P&L de ventas no encontrado")
            
            self.last_update = datetime.now()
            
        except Exception as e:
            error_msg = f"Error durante la recarga de datos: {e}"
            logger.error(error_msg)
            results["errores"].append(error_msg)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        results["tiempo_procesamiento"] = processing_time
        
        return results
    
    def get_data(self) -> Tuple[List[FiatFlowRecord], List[SalesPLRecord]]:
        """Obtener datos cargados (cargar si es necesario)"""
        if not self.fiat_flow_data or not self.sales_pl_data:
            logger.info("Datos no cargados, iniciando carga automática...")
            self.reload_all_data()
        
        return self.fiat_flow_data, self.sales_pl_data
    
    def get_stats(self) -> Dict[str, any]:
        """Obtener estadísticas de los datos cargados"""
        return {
            "fiat_flow_records": len(self.fiat_flow_data),
            "sales_pl_records": len(self.sales_pl_data),
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "data_loaded": bool(self.fiat_flow_data and self.sales_pl_data)
        }


# Instancia global del gestor de datos
csv_manager = CSVDataManager() 