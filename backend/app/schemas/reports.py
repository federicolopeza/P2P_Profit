#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schemas de reportes para P2P Profit API
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field

from .transactions import FiatFlowRecord, SalesPLRecord, CurrencyStats


class PLReportResponse(BaseModel):
    """Respuesta del reporte de P&L"""
    resumen: dict = Field(..., description="Resumen ejecutivo del P&L")
    ventas: List[SalesPLRecord] = Field(..., description="Detalle de todas las ventas")
    metricas: dict = Field(..., description="Métricas calculadas")
    por_moneda: List[CurrencyStats] = Field(..., description="Estadísticas por moneda")
    generado_en: datetime = Field(..., description="Timestamp de generación del reporte")


class FiatFlowReportResponse(BaseModel):
    """Respuesta del reporte de flujo de fiat"""
    resumen: dict = Field(..., description="Resumen del flujo de fiat")
    flujos: List[FiatFlowRecord] = Field(..., description="Detalle de flujos por venta")
    totales: dict = Field(..., description="Totales consolidados")
    disponibilidad: dict = Field(..., description="Fiat disponible por moneda")
    generado_en: datetime = Field(..., description="Timestamp de generación del reporte")


class DataReloadResponse(BaseModel):
    """Respuesta de la recarga de datos"""
    status: str = Field(..., description="Estado de la operación")
    archivos_procesados: List[str] = Field(..., description="Archivos CSV procesados")
    registros_cargados: dict = Field(..., description="Cantidad de registros cargados por archivo")
    tiempo_procesamiento: float = Field(..., description="Tiempo de procesamiento en segundos")
    errores: List[str] = Field(default=[], description="Errores encontrados durante el procesamiento")
    ultima_actualizacion: datetime = Field(..., description="Timestamp de la actualización")


class HealthStatusResponse(BaseModel):
    """Estado de salud del sistema de datos"""
    status: str = Field(..., description="Estado general del sistema")
    archivos_csv: dict = Field(..., description="Estado de archivos CSV")
    datos_cargados: bool = Field(..., description="Si los datos están cargados en memoria")
    ultima_carga: Optional[datetime] = Field(None, description="Última vez que se cargaron los datos")
    estadisticas: dict = Field(..., description="Estadísticas básicas de los datos")


class APIResponse(BaseModel):
    """Respuesta estándar de la API"""
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[dict] = Field(None, description="Datos de la respuesta")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la respuesta") 