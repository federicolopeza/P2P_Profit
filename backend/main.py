#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2P Profit Backend API
FastAPI backend para el sistema de seguimiento P2P cripto

Autor: P2P Profit Team
Versión: 1.0.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuración de la aplicación
APP_NAME = "P2P Profit API"
VERSION = "1.0.0"
DESCRIPTION = """
🚀 **P2P Profit API** - Sistema de seguimiento profesional para operaciones P2P de criptomonedas.

## Características principales

* 🧮 **Cálculo CPP**: Metodología de Costo Promedio Ponderado
* 💱 **Multi-moneda**: Soporte para USD y UYU
* 📊 **Reportes avanzados**: Métricas y analytics detallados
* 🔄 **Seguimiento de flujo**: Rastreo completo de fiat
* 🏦 **Integración exchanges**: Binance y otros
* 📱 **API REST**: Endpoints completos para frontend

## Endpoints disponibles

* `/transactions/` - Gestión de transacciones
* `/reports/` - Generación de reportes
* `/metrics/` - Métricas y KPIs
* `/users/` - Gestión de usuarios (próximamente)
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando P2P Profit API...")
    logger.info("📊 Cargando configuración inicial...")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando P2P Profit API...")

# Crear aplicación FastAPI
app = FastAPI(
    title=APP_NAME,
    description=DESCRIPTION,
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response

# Rutas básicas
@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "🎯 P2P Profit API",
        "version": VERSION,
        "status": "🟢 Activo",
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "🟢 Healthy",
        "timestamp": datetime.now().isoformat(),
        "service": APP_NAME,
        "version": VERSION
    }

@app.get("/api/v1/info")
async def api_info():
    """Información detallada de la API"""
    return {
        "api_name": APP_NAME,
        "version": VERSION,
        "description": "API REST para seguimiento P2P cripto",
        "endpoints": {
            "transactions": "/api/v1/transactions/",
            "reports": "/api/v1/reports/", 
            "metrics": "/api/v1/metrics/",
            "health": "/health"
        },
        "features": [
            "🧮 Cálculo CPP automático",
            "💱 Soporte multi-moneda",
            "📊 Reportes en tiempo real",
            "🔄 Seguimiento de flujo fiat",
            "🏦 Integración con exchanges"
        ],
        "timestamp": datetime.now().isoformat()
    }

# Manejo global de errores
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint no encontrado",
            "message": f"La ruta '{request.url.path}' no existe",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Error interno en {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": "Ocurrió un error inesperado",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 