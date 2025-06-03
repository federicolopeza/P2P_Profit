# 🚀 P2P Profit Backend API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?style=for-the-badge&logo=postgresql)

**Backend API REST para el sistema de seguimiento P2P de criptomonedas**

</div>

---

## 📋 Descripción

Backend API construido con **FastAPI** que proporciona todos los endpoints necesarios para el sistema P2P Profit. Incluye funcionalidades para:

- 🧮 **Cálculo CPP automático** con metodología de Costo Promedio Ponderado
- 💱 **Gestión multi-moneda** (USD/UYU) con tasas de cambio
- 📊 **Generación de reportes** y métricas en tiempo real
- 🔄 **Seguimiento de flujo de fiat** desde ventas hasta reinversión
- 🏦 **Integración con exchanges** (Binance y otros)
- 🛡️ **Autenticación JWT** y manejo de usuarios

## 🏗️ Arquitectura

```
backend/
├── main.py                 # 🚀 Punto de entrada de la aplicación
├── requirements.txt        # 📦 Dependencias Python
├── env.example            # 🔧 Variables de entorno de ejemplo
├── app/
│   ├── __init__.py
│   ├── config.py          # ⚙️ Configuración de la aplicación
│   ├── models/           # 🗄️ Modelos de SQLAlchemy
│   ├── schemas/          # 📝 Esquemas de Pydantic
│   ├── api/              # 🌐 Endpoints de la API
│   ├── core/             # 🔧 Lógica de negocio central
│   ├── db/               # 🗃️ Configuración de base de datos
│   └── utils/            # 🛠️ Utilidades y helpers
├── tests/                # 🧪 Tests automatizados
├── alembic/              # 📊 Migraciones de base de datos
└── docker/               # 🐳 Configuración Docker
```

## 🚀 Inicio Rápido

### 1. **Requisitos Previos**

```bash
# Python 3.9+
python --version

# PostgreSQL 15+
psql --version

# Git
git --version
```

### 2. **Instalación**

```bash
# Clonar repositorio (si no está clonado)
git clone <repo-url>
cd P2P_Profit/backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. **Configuración**

```bash
# Copiar configuración de ejemplo
cp env.example .env

# Editar variables de entorno
nano .env  # o tu editor preferido
```

**Variables clave a configurar:**
```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/p2p_profit

# Seguridad (IMPORTANTE: cambiar en producción)
SECRET_KEY=tu-clave-super-secreta-aqui

# CORS para tu frontend
CORS_ORIGINS=http://localhost:3000
```

### 4. **Base de Datos**

```bash
# Crear base de datos PostgreSQL
createdb p2p_profit

# Ejecutar migraciones (próximamente)
# alembic upgrade head
```

### 5. **Ejecutar**

```bash
# Desarrollo con auto-reload
python main.py

# O usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. **Verificar**

Abrir en el navegador:
- 🌐 **API**: http://localhost:8000
- 📚 **Documentación**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

## 📊 Endpoints Principales

### 🔍 **Información de la API**
```http
GET /                    # Info básica de la API
GET /health             # Health check
GET /api/v1/info        # Información detallada
```

### 💱 **Transacciones** (próximamente)
```http
GET    /api/v1/transactions/       # Listar transacciones
POST   /api/v1/transactions/       # Crear transacción
GET    /api/v1/transactions/{id}   # Obtener transacción
PUT    /api/v1/transactions/{id}   # Actualizar transacción
DELETE /api/v1/transactions/{id}   # Eliminar transacción
```

### 📈 **Reportes** (próximamente)
```http
GET /api/v1/reports/pl             # Reporte P&L
GET /api/v1/reports/flow           # Flujo de fiat
GET /api/v1/reports/metrics        # Métricas generales
```

### 👤 **Usuarios** (próximamente)
```http
POST /api/v1/auth/login            # Login
POST /api/v1/auth/register         # Registro
GET  /api/v1/users/me              # Perfil del usuario
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_api.py -v
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t p2p-profit-api .

# Ejecutar contenedor
docker run -p 8000:8000 p2p-profit-api

# Docker Compose (con PostgreSQL)
docker-compose up -d
```

## 🔧 Desarrollo

### **Estructura de Código**

```python
# Ejemplo de endpoint
from fastapi import APIRouter, Depends
from app.schemas import TransactionCreate, TransactionResponse
from app.core.transactions import create_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
async def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva transacción"""
    return await create_transaction(db, transaction)
```

### **Configuración de Entorno**

La aplicación soporta múltiples entornos:

```bash
# Desarrollo (por defecto)
ENVIRONMENT=development

# Producción
ENVIRONMENT=production

# Testing
ENVIRONMENT=testing
```

### **Logging**

```python
import logging
logger = logging.getLogger(__name__)

logger.info("🚀 Iniciando proceso...")
logger.error("❌ Error en el proceso")
```

## 📈 Características Técnicas

### **FastAPI Features Utilizados**
- ✅ **Async/Await** para operaciones no bloqueantes
- ✅ **Pydantic Models** para validación automática
- ✅ **OpenAPI/Swagger** documentación automática
- ✅ **Dependency Injection** para componentes reutilizables
- ✅ **Middleware** para CORS, logging y autenticación
- ✅ **Exception Handlers** personalizados

### **Base de Datos**
- 🗄️ **SQLAlchemy 2.0** con async support
- 📊 **Alembic** para migraciones
- 🔄 **Connection pooling** para performance
- 📈 **Índices optimizados** para consultas rápidas

### **Seguridad**
- 🔐 **JWT Authentication** con refresh tokens
- 🛡️ **Password hashing** con bcrypt
- 🌐 **CORS** configurado para frontend
- 📝 **Request validation** automática

## 🚨 Troubleshooting

### **Problemas Comunes**

#### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Verificar conexión
psql -h localhost -U postgres -d p2p_profit
```

#### Puerto ya en uso
```bash
# Cambiar puerto en .env
PORT=8001

# O matar proceso en puerto 8000
sudo lsof -t -i:8000 | xargs kill -9
```

#### Problemas de dependencias
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt

# Limpiar cache de pip
pip cache purge
```

## 📚 Documentación Adicional

- 📖 **FastAPI Docs**: https://fastapi.tiangolo.com/
- 🗄️ **SQLAlchemy**: https://docs.sqlalchemy.org/
- 📊 **Alembic**: https://alembic.sqlalchemy.org/
- 🔐 **JWT**: https://pyjwt.readthedocs.io/

## 🤝 Contribución

1. **Fork** el repositorio
2. **Crear** branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. **Push** a branch (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

### **Estándares de Código**

```bash
# Formatear código
black app/
isort app/

# Linting
flake8 app/
mypy app/
```

---

<div align="center">

**[🚀 Volver al Roadmap](../docs/ROADMAP.md)** • 
**[📊 Ver Frontend](../frontend/README.md)** • 
**[📖 Documentación Principal](../README.md)**

---

[![FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-green?style=for-the-badge)](https://fastapi.tiangolo.com/)

</div> 