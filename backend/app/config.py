#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de la aplicación P2P Profit
Variables de entorno y configuración general
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings"""
    
    # Información de la aplicación
    app_name: str = "P2P Profit API"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Modo debug")
    
    # Configuración del servidor
    host: str = Field(default="0.0.0.0", description="Host del servidor")
    port: int = Field(default=8000, description="Puerto del servidor")
    reload: bool = Field(default=True, description="Auto-reload en desarrollo")
    
    # Base de datos
    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/p2p_profit",
        description="URL de conexión a PostgreSQL"
    )
    database_echo: bool = Field(default=False, description="Echo SQL queries")
    
    # Seguridad
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Clave secreta para JWT"
    )
    algorithm: str = Field(default="HS256", description="Algoritmo para JWT")
    access_token_expire_minutes: int = Field(
        default=30, 
        description="Minutos de expiración del token"
    )
    
    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Orígenes permitidos para CORS"
    )
    
    # Configuración de logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato de logging"
    )
    
    # Configuración específica P2P
    default_currency: str = Field(default="USD", description="Moneda por defecto")
    supported_currencies: list[str] = Field(
        default=["USD", "UYU"], 
        description="Monedas soportadas"
    )
    
    # Comisiones de exchanges (para cálculos automáticos)
    binance_fee_usd: float = Field(default=0.0028, description="Comisión Binance USD")
    binance_fee_uyu: float = Field(default=0.0016, description="Comisión Binance UYU")
    
    # Configuración de backup
    backup_enabled: bool = Field(default=True, description="Habilitar backups automáticos")
    backup_interval_hours: int = Field(default=24, description="Intervalo de backup en horas")
    backup_retention_days: int = Field(default=30, description="Días de retención de backups")
    
    # Configuración de reportes
    max_transactions_per_report: int = Field(
        default=10000, 
        description="Máximo de transacciones por reporte"
    )
    report_cache_minutes: int = Field(
        default=15, 
        description="Minutos de cache para reportes"
    )
    
    # Configuración de desarrollo
    api_prefix: str = Field(default="/api/v1", description="Prefijo de la API")
    docs_url: Optional[str] = Field(default="/docs", description="URL de documentación")
    redoc_url: Optional[str] = Field(default="/redoc", description="URL de ReDoc")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Configuración específica por entorno
class DevelopmentSettings(Settings):
    """Configuración para desarrollo"""
    debug: bool = True
    reload: bool = True
    database_echo: bool = True
    log_level: str = "DEBUG"


class ProductionSettings(Settings):
    """Configuración para producción"""
    debug: bool = False
    reload: bool = False
    database_echo: bool = False
    log_level: str = "INFO"
    docs_url: Optional[str] = None  # Deshabilitar docs en producción
    redoc_url: Optional[str] = None


class TestingSettings(Settings):
    """Configuración para testing"""
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    log_level: str = "WARNING"


def get_settings() -> Settings:
    """
    Factory para obtener la configuración según el entorno
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Instancia global de configuración
settings = get_settings()


# Función para validar configuración
def validate_settings():
    """Valida que la configuración sea correcta"""
    errors = []
    
    # Validar URL de base de datos
    if not settings.database_url:
        errors.append("DATABASE_URL es requerida")
    
    # Validar secret key en producción
    if not settings.debug and settings.secret_key == "your-secret-key-change-in-production":
        errors.append("SECRET_KEY debe cambiarse en producción")
    
    # Validar monedas soportadas
    if settings.default_currency not in settings.supported_currencies:
        errors.append(f"Default currency {settings.default_currency} no está en supported_currencies")
    
    if errors:
        raise ValueError(f"Errores de configuración: {', '.join(errors)}")
    
    return True


# Configuración de logging
import logging

def configure_logging():
    """Configura el logging de la aplicación"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log") if not settings.debug else logging.NullHandler()
        ]
    )
    
    # Configurar loggers específicos
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.database_echo else logging.WARNING
    )


if __name__ == "__main__":
    # Test de configuración
    configure_logging()
    validate_settings()
    print(f"✅ Configuración válida para entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔧 Debug: {settings.debug}")
    print(f"🗄️ Database: {settings.database_url}")
    print(f"🌐 CORS Origins: {settings.cors_origins}") 