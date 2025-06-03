#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cálculos y métricas para P2P Profit
Implementa la lógica de negocio para procesar transacciones y generar reportes
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional
import logging
from collections import defaultdict

from ..schemas.transactions import FiatFlowRecord, SalesPLRecord, TransactionSummary, CurrencyStats

logger = logging.getLogger(__name__)


class P2PCalculator:
    """Calculadora de métricas P2P"""
    
    def __init__(self):
        self.last_calculation: Optional[datetime] = None
    
    def calculate_transaction_summary(
        self, 
        fiat_flow_data: List[FiatFlowRecord], 
        sales_pl_data: List[SalesPLRecord]
    ) -> TransactionSummary:
        """Calcular resumen general de transacciones"""
        
        # Calcular totales de ventas
        total_ventas = len(sales_pl_data)
        total_usdt_vendido = sum(record.cantidad_usdt_vendida for record in sales_pl_data)
        ganancia_total_usd = sum(record.ganancia_perdida_usd for record in sales_pl_data)
        
        # Calcular fiat generado en USD
        total_fiat_generado_usd = sum(record.ingreso_neto_usd for record in sales_pl_data)
        
        # Calcular fiat disponible por moneda
        fiat_disponible_usd = Decimal('0')
        fiat_disponible_uyu = Decimal('0')
        
        for record in fiat_flow_data:
            if record.estado_fiat == "Disponible":
                if record.moneda_generada == "USD":
                    fiat_disponible_usd += record.monto_fiat_disponible
                elif record.moneda_generada == "UYU":
                    fiat_disponible_uyu += record.monto_fiat_disponible
        
        # Calcular ROI
        total_costo_base = sum(record.costo_base_usd for record in sales_pl_data)
        roi_porcentaje = (ganancia_total_usd / total_costo_base * 100) if total_costo_base > 0 else Decimal('0')
        
        self.last_calculation = datetime.now()
        
        return TransactionSummary(
            total_ventas=total_ventas,
            total_usdt_vendido=total_usdt_vendido,
            total_fiat_generado_usd=total_fiat_generado_usd,
            fiat_disponible_usd=fiat_disponible_usd,
            fiat_disponible_uyu=fiat_disponible_uyu,
            ganancia_total_usd=ganancia_total_usd,
            roi_porcentaje=roi_porcentaje,
            ultima_actualizacion=self.last_calculation
        )
    
    def calculate_currency_stats(self, sales_pl_data: List[SalesPLRecord]) -> List[CurrencyStats]:
        """Calcular estadísticas por moneda"""
        
        # Agrupar por moneda
        currency_data = defaultdict(lambda: {
            'ventas': 0,
            'volumen_usdt': Decimal('0'),
            'fiat_generado': Decimal('0'),
            'ganancia_total': Decimal('0')
        })
        
        for record in sales_pl_data:
            currency = record.moneda_recibida
            currency_data[currency]['ventas'] += 1
            currency_data[currency]['volumen_usdt'] += record.cantidad_usdt_vendida
            currency_data[currency]['fiat_generado'] += record.ingreso_total
            currency_data[currency]['ganancia_total'] += record.ganancia_perdida_usd
        
        # Crear objetos CurrencyStats
        stats = []
        for currency, data in currency_data.items():
            ganancia_promedio = (
                data['ganancia_total'] / data['ventas'] 
                if data['ventas'] > 0 else Decimal('0')
            )
            
            stats.append(CurrencyStats(
                moneda=currency,
                total_ventas=data['ventas'],
                volumen_usdt=data['volumen_usdt'],
                fiat_generado=data['fiat_generado'],
                fiat_disponible=Decimal('0'),  # Se calculará desde fiat_flow_data
                ganancia_promedio=ganancia_promedio
            ))
        
        return stats
    
    def update_currency_stats_with_flow(
        self, 
        currency_stats: List[CurrencyStats], 
        fiat_flow_data: List[FiatFlowRecord]
    ) -> List[CurrencyStats]:
        """Actualizar estadísticas de moneda con datos de flujo de fiat"""
        
        # Calcular fiat disponible por moneda
        fiat_disponible = defaultdict(Decimal)
        for record in fiat_flow_data:
            if record.estado_fiat == "Disponible":
                fiat_disponible[record.moneda_generada] += record.monto_fiat_disponible
        
        # Actualizar estadísticas
        for stat in currency_stats:
            stat.fiat_disponible = fiat_disponible.get(stat.moneda, Decimal('0'))
        
        return currency_stats
    
    def generate_pl_report_data(
        self, 
        fiat_flow_data: List[FiatFlowRecord], 
        sales_pl_data: List[SalesPLRecord]
    ) -> Dict[str, any]:
        """Generar datos completos para reporte P&L"""
        
        # Resumen ejecutivo
        summary = self.calculate_transaction_summary(fiat_flow_data, sales_pl_data)
        
        # Estadísticas por moneda
        currency_stats = self.calculate_currency_stats(sales_pl_data)
        currency_stats = self.update_currency_stats_with_flow(currency_stats, fiat_flow_data)
        
        # Métricas adicionales
        metricas = self._calculate_additional_metrics(sales_pl_data)
        
        # Resumen ejecutivo como dict
        resumen = {
            "total_ventas": summary.total_ventas,
            "volumen_total_usdt": float(summary.total_usdt_vendido),
            "ganancia_total_usd": float(summary.ganancia_total_usd),
            "roi_porcentaje": float(summary.roi_porcentaje),
            "fiat_disponible": {
                "USD": float(summary.fiat_disponible_usd),
                "UYU": float(summary.fiat_disponible_uyu)
            }
        }
        
        return {
            "resumen": resumen,
            "ventas": sales_pl_data,
            "metricas": metricas,
            "por_moneda": currency_stats,
            "generado_en": datetime.now()
        }
    
    def generate_fiat_flow_report_data(
        self, 
        fiat_flow_data: List[FiatFlowRecord]
    ) -> Dict[str, any]:
        """Generar datos completos para reporte de flujo de fiat"""
        
        # Calcular totales
        totales = self._calculate_fiat_totals(fiat_flow_data)
        
        # Disponibilidad por moneda
        disponibilidad = self._calculate_fiat_availability(fiat_flow_data)
        
        # Resumen
        resumen = {
            "total_registros": len(fiat_flow_data),
            "fiat_total_generado": totales["total_generado"],
            "fiat_total_disponible": totales["total_disponible"],
            "porcentaje_utilizado": totales["porcentaje_utilizado"]
        }
        
        return {
            "resumen": resumen,
            "flujos": fiat_flow_data,
            "totales": totales,
            "disponibilidad": disponibilidad,
            "generado_en": datetime.now()
        }
    
    def _calculate_additional_metrics(self, sales_pl_data: List[SalesPLRecord]) -> Dict[str, any]:
        """Calcular métricas adicionales"""
        if not sales_pl_data:
            return {}
        
        # Ganancia por transacción
        ganancias = [float(record.ganancia_perdida_usd) for record in sales_pl_data]
        ganancia_promedio = sum(ganancias) / len(ganancias)
        ganancia_maxima = max(ganancias)
        ganancia_minima = min(ganancias)
        
        # Volumen por transacción
        volumenes = [float(record.cantidad_usdt_vendida) for record in sales_pl_data]
        volumen_promedio = sum(volumenes) / len(volumenes)
        
        # Fechas
        fechas = [record.fecha_venta for record in sales_pl_data]
        fecha_primera = min(fechas)
        fecha_ultima = max(fechas)
        dias_operando = (fecha_ultima - fecha_primera).days + 1
        
        return {
            "ganancia_promedio_usd": ganancia_promedio,
            "ganancia_maxima_usd": ganancia_maxima,
            "ganancia_minima_usd": ganancia_minima,
            "volumen_promedio_usdt": volumen_promedio,
            "fecha_primera_venta": fecha_primera.isoformat(),
            "fecha_ultima_venta": fecha_ultima.isoformat(),
            "dias_operando": dias_operando,
            "ganancia_por_dia": ganancia_promedio / dias_operando if dias_operando > 0 else 0
        }
    
    def _calculate_fiat_totals(self, fiat_flow_data: List[FiatFlowRecord]) -> Dict[str, any]:
        """Calcular totales de fiat"""
        total_generado = sum(record.monto_neto_generado for record in fiat_flow_data)
        total_utilizado = sum(record.monto_fiat_utilizado for record in fiat_flow_data)
        total_disponible = sum(record.monto_fiat_disponible for record in fiat_flow_data)
        
        porcentaje_utilizado = (
            float(total_utilizado / total_generado * 100) 
            if total_generado > 0 else 0.0
        )
        
        return {
            "total_generado": float(total_generado),
            "total_utilizado": float(total_utilizado),
            "total_disponible": float(total_disponible),
            "porcentaje_utilizado": porcentaje_utilizado
        }
    
    def _calculate_fiat_availability(self, fiat_flow_data: List[FiatFlowRecord]) -> Dict[str, any]:
        """Calcular disponibilidad de fiat por moneda"""
        availability = defaultdict(lambda: {"disponible": Decimal('0'), "utilizado": Decimal('0')})
        
        for record in fiat_flow_data:
            currency = record.moneda_generada
            availability[currency]["disponible"] += record.monto_fiat_disponible
            availability[currency]["utilizado"] += record.monto_fiat_utilizado
        
        # Convertir a dict normal con float
        result = {}
        for currency, data in availability.items():
            result[currency] = {
                "disponible": float(data["disponible"]),
                "utilizado": float(data["utilizado"]),
                "total": float(data["disponible"] + data["utilizado"])
            }
        
        return result


# Instancia global del calculador
calculator = P2PCalculator() 