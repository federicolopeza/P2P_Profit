#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schemas de transacciones para P2P Profit
Basados en la estructura de CSV existente
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class FiatFlowRecord(BaseModel):
    """Registro de flujo de fiat"""
    id_venta: str = Field(..., description="ID único de la venta")
    moneda_generada: str = Field(..., description="Moneda generada (USD/UYU)")
    monto_neto_generado: Decimal = Field(..., description="Monto neto generado")
    monto_fiat_utilizado: Decimal = Field(..., description="Monto fiat ya utilizado")
    monto_fiat_disponible: Decimal = Field(..., description="Monto fiat disponible")
    estado_fiat: str = Field(..., description="Estado del fiat (Disponible/Utilizado)")
    fecha_venta: datetime = Field(..., description="Fecha de la venta")


class SalesPLRecord(BaseModel):
    """Registro de P&L de ventas"""
    id_venta: str = Field(..., description="ID único de la venta")
    fecha_venta: datetime = Field(..., description="Fecha de la venta")
    cantidad_usdt_vendida: Decimal = Field(..., description="Cantidad de USDT vendida")
    moneda_recibida: str = Field(..., description="Moneda recibida (USD/UYU)")
    ingreso_total: Decimal = Field(..., description="Ingreso total en moneda recibida")
    ingreso_neto_usd: Decimal = Field(..., description="Ingreso neto convertido a USD")
    costo_base_usd: Decimal = Field(..., description="Costo base USD de USDT vendido")
    ganancia_perdida_usd: Decimal = Field(..., description="Ganancia/Pérdida en USD")


class TransactionSummary(BaseModel):
    """Resumen de transacciones"""
    total_ventas: int = Field(..., description="Total de ventas procesadas")
    total_usdt_vendido: Decimal = Field(..., description="Total USDT vendido")
    total_fiat_generado_usd: Decimal = Field(..., description="Total fiat generado en USD")
    fiat_disponible_usd: Decimal = Field(..., description="Fiat disponible en USD")
    fiat_disponible_uyu: Decimal = Field(..., description="Fiat disponible en UYU")
    ganancia_total_usd: Decimal = Field(..., description="Ganancia total acumulada en USD")
    roi_porcentaje: Decimal = Field(..., description="ROI en porcentaje")
    ultima_actualizacion: datetime = Field(..., description="Última vez que se procesaron los datos")


class CurrencyStats(BaseModel):
    """Estadísticas por moneda"""
    moneda: str = Field(..., description="Código de moneda")
    total_ventas: int = Field(..., description="Número de ventas")
    volumen_usdt: Decimal = Field(..., description="Volumen total en USDT")
    fiat_generado: Decimal = Field(..., description="Fiat generado en esta moneda")
    fiat_disponible: Decimal = Field(..., description="Fiat disponible en esta moneda")
    ganancia_promedio: Decimal = Field(..., description="Ganancia promedio por transacción") 