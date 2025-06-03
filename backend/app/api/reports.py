#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Endpoints de reportes para P2P Profit API
Genera reportes basados en datos CSV existentes
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from ..core.csv_reader import csv_manager
from ..core.calculations import calculator
from ..schemas.reports import (
    PLReportResponse, 
    FiatFlowReportResponse, 
    DataReloadResponse,
    HealthStatusResponse,
    APIResponse
)

logger = logging.getLogger(__name__)

# Router de reportes
router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

@router.get("/pl", response_model=PLReportResponse)
async def get_pl_report():
    """
    📊 Generar reporte de P&L (Profit & Loss)
    
    Analiza las ventas y calcula:
    - Ganancia/pérdida total
    - ROI por moneda
    - Métricas de performance
    - Estadísticas por moneda
    """
    try:
        logger.info("🔄 Generando reporte P&L...")
        
        # Obtener datos
        fiat_flow_data, sales_pl_data = csv_manager.get_data()
        
        if not sales_pl_data:
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron datos de ventas. Verifique los archivos CSV."
            )
        
        # Generar reporte
        report_data = calculator.generate_pl_report_data(fiat_flow_data, sales_pl_data)
        
        logger.info(f"✅ Reporte P&L generado con {len(sales_pl_data)} ventas")
        
        return PLReportResponse(**report_data)
        
    except Exception as e:
        logger.error(f"❌ Error generando reporte P&L: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando reporte P&L: {str(e)}")


@router.get("/flow", response_model=FiatFlowReportResponse)
async def get_fiat_flow_report():
    """
    💰 Generar reporte de flujo de fiat
    
    Analiza el flujo de dinero fiat:
    - Fiat generado por ventas
    - Fiat disponible vs utilizado
    - Distribución por moneda
    - Estado de liquidez
    """
    try:
        logger.info("🔄 Generando reporte de flujo de fiat...")
        
        # Obtener datos
        fiat_flow_data, _ = csv_manager.get_data()
        
        if not fiat_flow_data:
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron datos de flujo de fiat. Verifique los archivos CSV."
            )
        
        # Generar reporte
        report_data = calculator.generate_fiat_flow_report_data(fiat_flow_data)
        
        logger.info(f"✅ Reporte de flujo generado con {len(fiat_flow_data)} registros")
        
        return FiatFlowReportResponse(**report_data)
        
    except Exception as e:
        logger.error(f"❌ Error generando reporte de flujo: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando reporte de flujo: {str(e)}")


@router.get("/summary")
async def get_summary_report():
    """
    📈 Resumen ejecutivo consolidado
    
    Combina métricas clave de P&L y flujo de fiat:
    - KPIs principales
    - Estado financiero actual
    - Tendencias de performance
    """
    try:
        logger.info("🔄 Generando resumen ejecutivo...")
        
        # Obtener datos
        fiat_flow_data, sales_pl_data = csv_manager.get_data()
        
        if not fiat_flow_data and not sales_pl_data:
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron datos. Verifique los archivos CSV."
            )
        
        # Calcular resumen
        summary = calculator.calculate_transaction_summary(fiat_flow_data, sales_pl_data)
        
        # Métricas adicionales
        metricas_adicionales = {}
        if sales_pl_data:
            metricas_adicionales = calculator._calculate_additional_metrics(sales_pl_data)
        
        response_data = {
            "resumen_transacciones": summary.dict(),
            "metricas_adicionales": metricas_adicionales,
            "estado_datos": {
                "registros_fiat": len(fiat_flow_data),
                "registros_ventas": len(sales_pl_data),
                "ultima_actualizacion": csv_manager.last_update.isoformat() if csv_manager.last_update else None
            },
            "generado_en": datetime.now().isoformat()
        }
        
        logger.info("✅ Resumen ejecutivo generado")
        
        return APIResponse(
            success=True,
            message="Resumen ejecutivo generado exitosamente",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error generando resumen: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando resumen: {str(e)}")


# Router de datos
data_router = APIRouter(prefix="/api/v1/data", tags=["data"])

@data_router.post("/reload", response_model=DataReloadResponse)
async def reload_csv_data():
    """
    🔄 Recargar datos desde archivos CSV
    
    Vuelve a leer los archivos CSV y actualiza los datos en memoria:
    - reporte_flujo_fiat.csv
    - reporte_ventas_pl.csv
    """
    try:
        logger.info("🔄 Iniciando recarga de datos CSV...")
        
        # Recargar datos
        results = csv_manager.reload_all_data()
        
        response = DataReloadResponse(
            status="✅ Recarga completada" if not results["errores"] else "⚠️ Recarga con errores",
            archivos_procesados=results["archivos_procesados"],
            registros_cargados=results["registros_cargados"],
            tiempo_procesamiento=results["tiempo_procesamiento"],
            errores=results["errores"],
            ultima_actualizacion=datetime.now()
        )
        
        if results["errores"]:
            logger.warning(f"Recarga completada con errores: {results['errores']}")
        else:
            logger.info("✅ Recarga de datos completada exitosamente")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error durante la recarga: {e}")
        raise HTTPException(status_code=500, detail=f"Error durante la recarga: {str(e)}")


@data_router.get("/health", response_model=HealthStatusResponse)
async def get_data_health():
    """
    🏥 Estado de salud de los datos
    
    Verifica el estado de los archivos CSV y datos cargados:
    - Existencia de archivos
    - Última actualización
    - Estadísticas básicas
    """
    try:
        # Verificar archivos
        file_status = csv_manager.check_csv_files()
        
        # Estadísticas de datos
        stats = csv_manager.get_stats()
        
        # Determinar estado general
        all_files_exist = all(file_status.values())
        data_is_loaded = stats["data_loaded"]
        
        if all_files_exist and data_is_loaded:
            status = "🟢 Saludable"
        elif all_files_exist:
            status = "🟡 Archivos OK, datos no cargados"
        else:
            status = "🔴 Archivos faltantes"
        
        return HealthStatusResponse(
            status=status,
            archivos_csv=file_status,
            datos_cargados=data_is_loaded,
            ultima_carga=csv_manager.last_update,
            estadisticas=stats
        )
        
    except Exception as e:
        logger.error(f"❌ Error verificando salud de datos: {e}")
        raise HTTPException(status_code=500, detail=f"Error verificando salud: {str(e)}")


# Incluir routers en el main router
def get_routers():
    """Obtener todos los routers de la API"""
    return [router, data_router]