# 🚀 P2P Profit - Sistema de Seguimiento Cripto Profesional

<div align="center">

![P2P Profit Logo](https://img.shields.io/badge/P2P-Profit-blue?style=for-the-badge&logo=bitcoin&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Version](https://img.shields.io/badge/Version-1.0.0-red?style=flat-square)](https://github.com/user/p2p-profit)

**Sistema avanzado de seguimiento y análisis P2P para transacciones de criptomonedas con cálculo automático de P&L usando metodología CPP (Costo Promedio Ponderado)**

[🚀 Inicio Rápido](#-inicio-rápido) • 
[📖 Documentación](#-documentación) • 
[🎯 Características](#-características) • 
[📊 Demo](#-demo-y-ejemplos)

</div>

---

## 📋 Tabla de Contenidos

- [🎯 Características](#-características)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [💼 Casos de Uso](#-casos-de-uso)
- [🛠️ Instalación](#️-instalación)
- [📊 Demo y Ejemplos](#-demo-y-ejemplos)
- [🔧 Uso Detallado](#-uso-detallado)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🧮 Metodología CPP](#-metodología-cpp)
- [📈 Reportes y Analytics](#-reportes-y-analytics)
- [🔒 Seguridad y Privacidad](#-seguridad-y-privacidad)
- [🤝 Contribución](#-contribución)
- [📞 Soporte](#-soporte)
- [📜 Licencia](#-licencia)

---

## 🎯 Características

### 🏆 **Funcionalidades Principales**

| Característica | Descripción | Estado |
|----------------|-------------|---------|
| 🧮 **Cálculo CPP Preciso** | Metodología de Costo Promedio Ponderado para cálculo exacto de P&L | ✅ |
| 💱 **Soporte Multi-Moneda** | Manejo de USD y UYU con tasas de cambio dinámicas | ✅ |
| 📊 **Dashboard Interactivo** | Interfaz de consola completa para gestión y análisis | ✅ |
| 🤖 **Procesamiento Automático** | Script batch para procesamiento masivo de datos | ✅ |
| 📈 **Reportes Avanzados** | Generación automática de CSV con métricas detalladas | ✅ |
| 🔄 **Seguimiento de Flujo Fiat** | Rastreo completo del dinero generado por ventas | ✅ |
| 🏦 **Integración Binance** | Cálculo automático de comisiones de Binance | ✅ |
| 💾 **Backup Automático** | Sistema de respaldo de datos integrado | ✅ |
| 🛡️ **Validación de Datos** | Verificación y limpieza automática de información | ✅ |
| 📱 **Cross-Platform** | Compatible con Windows, macOS y Linux | ✅ |

### 🎨 **Herramientas Incluidas**

🎛️ Dashboard Interactivo Rich (`src/dashboard_p2p.py`)
├── 🌈 Interfaz CLI moderna con la biblioteca Rich
├── 📊 Tablas elegantes con colores y formato profesional
├── 🎯 Menús intuitivos con paneles redondeados
├── ✅ Validación en tiempo real con feedback visual
├── 📝 Gestión de datos con formularios guiados
├── 📊 Visualización de datos avanzada con paginación
├── 🔧 Herramientas de administración integradas
└── 📱 Experiencia de usuario optimizada para consola

🤖 Script Automático (`src/script_p2p_tracker.py`)
├── ⚡ Procesamiento batch ultra-rápido
├── 📈 Cálculos CPP automatizados
├── 📊 Generación automática de reportes
└── 🔄 Integración con otros sistemas

**Características destacadas de Rich:**
- ✨ **Diseño Visual Moderno**: Paneles redondeados, colores profesionales y layout elegante
- 🎯 **Navegación Intuitiva**: Menús claramente organizados con feedback visual
- 📊 **Tablas Elegantes**: Formato automático con colores para P&L positivo/negativo
- ✅ **Validación Visual**: Mensajes de error y éxito con paneles coloridos
- 🔄 **Paginación Inteligente**: Navegación fluida en datasets grandes
- 🎨 **Tema Consistente**: Paleta de colores unificada en toda la aplicación

**Navegación del Dashboard:**
```
1️⃣ Gestionar Datos de Transacciones
   ├── 📝 Nueva Compra USDT
   ├── 💸 Nueva Venta USDT  
   ├── 🔄 Nueva Conversión Fiat
   └── 👀 Ver Datos Existentes

2️⃣ Ver Resumen Financiero Global
   ├── 💰 P&L Total (Ganancias/Pérdidas)
   ├── 📊 Estado del Inventario
   ├── 📈 ROI y Métricas Principales
   └── 🏢 Desglose por Plataforma

3️⃣ Análisis Detallado por Categoría
   ├── 🏪 Análisis por Plataforma
   ├── 💱 Análisis por Moneda
   ├── 📅 Análisis Temporal
   └── 📋 Historial de Transacciones

4️⃣ Herramientas y Utilidades
   ├── 💾 Crear Backup de Datos
   ├── 📄 Estado de Archivos
   ├── ✅ Validar Integridad de Datos
   └── 🔧 Configuración del Sistema
```

### 🚀 **Scripts y Automatización**

#### Dashboard Principal Rich
```bash
python src/dashboard_p2p.py
```
- 🌈 **Interfaz Rich moderna** con paneles elegantes
- 📝 **Gestión completa** de transacciones con validación visual
- 📊 **Análisis en tiempo real** de P&L y ROI con tablas coloridas
- 🔧 **Herramientas administrativas** con feedback profesional

#### Script Automático
```bash
python src/script_p2p_tracker.py
```
- 🤖 **Procesamiento batch** de datos
- 📈 **Reportes automáticos** en CSV
- 🔍 **Validación de integridad** de datos
- ⚡ **Cálculos optimizados** de CPP y P&L

---

## 🚀 Inicio Rápido

### ⚡ **Instalación en 3 pasos**

```bash
# 1. Clonar el repositorio
git clone https://github.com/user/p2p-profit.git
cd p2p-profit

# 2. Instalar dependencias (incluye Rich para interfaz moderna)
pip install -r requirements.txt

# 3. ¡Ejecutar!
python src/dashboard_p2p.py       # Dashboard interactivo
# o
python src/script_p2p_tracker.py  # Procesamiento automático
```

### 🎯 **Primer uso en 30 segundos**

```bash
# Ejecutar dashboard moderno con Rich
python src/dashboard_p2p.py
```

**Salida esperada - Interfaz Rich:**
```
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                          ║
║  ✨ P2P CRYPTO TRACKER ✨ Dashboard Interactivo Profesional                                              ║
║                                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝

╭──────────────────────────── 📊 ESTADO RÁPIDO ────────────────────────────────╮
│ 🛍️ Compras Registradas:              0                                        │
│ 💸 Ventas Registradas:               0                                         │
│ 🔄 Conversiones Fiat:                0                                         │
│                                                                               │
│            ⚠️ Sin datos. Usa 'Gestionar Datos' para iniciar.                │
╰───────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────── 🏠 MENÚ PRINCIPAL ─────────────────────────────╮
│   1️⃣         📝 Gestionar Datos de Transacciones                           │
│   2️⃣         📊 Ver Resumen Financiero Global                              │
│   3️⃣         📈 Análisis Detallado por Categoría                           │
│   4️⃣         🔧 Herramientas y Utilidades                                  │
│   5️⃣         ❌ Salir del Dashboard                                         │
╰─────────────────────────────────────────────────────────────────────────────╯

✨ Selecciona una opción: 
```

---

## 💼 Casos de Uso

### 🎯 **¿Para quién es este sistema?**

| Perfil | Beneficios |
|--------|------------|
| 🏪 **Traders P2P** | Seguimiento preciso de ganancias/pérdidas en operaciones USDT |
| 📊 **Contadores/Asesores** | Cálculos fiscales precisos con metodología CPP |
| 🏢 **Pequeñas Empresas** | Control financiero de operaciones cripto |
| 🔬 **Analistas** | Data analytics de rendimiento de trading |
| 💰 **Inversores** | ROI tracking y optimización de estrategias |

### 🌟 **Escenarios Reales**

```
📈 Caso 1: Trader Activo
- 50+ transacciones mensuales
- Múltiples plataformas (Binance, WhatsApp, etc.)
- Necesita P&L preciso para declaraciones fiscales

📊 Caso 2: Empresa de Remesas
- Conversiones USD ↔ UYU frecuentes
- Seguimiento de comisiones y spreads
- Reportes para auditorías

🔄 Caso 3: Arbitrajista
- Compra/venta en diferentes exchanges
- Seguimiento de oportunidades de arbitraje
- Análisis de rentabilidad por plataforma
```

---

## 🛠️ Instalación

### 📋 **Requisitos del Sistema**

| Componente | Versión Mínima | Recomendada |
|------------|----------------|-------------|
| **Python** | 3.7+ | 3.9+ |
| **Pandas** | 1.5.0+ | 2.0+ |
| **NumPy** | 1.21.0+ | 1.24+ |
| **Rich** | 13.0.0+ | 14.0+ |
| **OS** | Windows 10, macOS 10.14, Ubuntu 18.04 | Cualquier versión reciente |
| **RAM** | 4GB | 8GB+ |
| **Almacenamiento** | 100MB | 1GB+ |

### 🔧 **Instalación Detallada**

#### Opción 1: Instalación Estándar
```bash
# Clonar repositorio
git clone https://github.com/user/p2p-profit.git
cd p2p-profit

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Instalar dependencias (incluye Rich para interfaz moderna)
pip install -r requirements.txt

# Verificar instalación con el dashboard moderno
python src/dashboard_p2p.py
```

#### Opción 2: Instalación de Desarrollo
```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest black flake8  # Herramientas de desarrollo

# Configurar pre-commit hooks
pre-commit install

# Ejecutar tests
pytest tests/
```

#### Opción 3: Docker (Próximamente)
```bash
# Pull imagen
docker pull p2p-profit:latest

# Ejecutar
docker run -v $(pwd)/data:/app/data p2p-profit:latest
```

---

## 📊 Demo y Ejemplos

### 🎬 **Demo Interactivo**

```bash
# Ejecutar dashboard interactivo
python src/dashboard_p2p.py
```

**Salida esperada:**
```
✨────────────────────────────────────────────────────────────✨
│               📊 P2P CRYPTO TRACKER 📊                     │
│                 📈 Dashboard Interactivo                   │
✨────────────────────────────────────────────────────────────✨

╔════════════════════════════════════════════════════════╗
║                    ESTADO RÁPIDO                       ║
╠════════════════════════════════════════════════════════╣
║ 🛍️ Compras Registradas: 0                            ║
║ 💸 Ventas Registradas:  0                            ║
║ 🔄 Conversiones Fiat: 0                            ║
║                                                        ║
║ ⚠️ Sin datos. Usa 'Gestionar Datos' para iniciar.  ║
╚════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════╗
║                    MENÚ PRINCIPAL                      ║
╠════════════════════════════════════════════════════════╣
║  1️⃣  📝 Gestionar Datos de Transacciones              ║
║  2️⃣  📊 Ver Resumen Financiero Global                 ║
║  3️⃣  📈 Análisis Detallado por Categoría              ║
║  4️⃣  🔧 Herramientas y Utilidades                     ║
║  5️⃣  ❌ Salir del Dashboard                           ║
╚════════════════════════════════════════════════════════╝

✨ Selecciona una opción y presiona Enter: 
```

### 📈 **Ejemplo de Datos Procesados**

**Entrada (compras_usdt.csv):**
```csv
ID_Compra,Fecha_Compra,Cantidad_USDT_Comprada,Moneda_Pago,Precio_Unitario_Moneda_Pago,Plataforma
C001,2025-06-01,621.95,USD,0.989,binance
C002,2025-06-02,119.95,USD,0.997,binance
C003,2025-06-02,7210.0,USD,1.0,whatsapp
```

**Salida (reporte_ventas_pl.csv):**
```csv
ID_Venta,Cantidad_USDT_Vendida,Ingreso_Neto_en_USD,Costo_Base_USD,Ganancia_Perdida_USD
V001,202.74,212.76,201.07,11.69
V002,4000.06,4073.91,3992.91,81.00
V003,1089.88,1146.56,1087.93,58.63
```

### 🧮 **Cálculo CPP en Acción**

```python
# Ejemplo de cálculo automático
Compra 1: 621.95 USDT a $0.989 = $615.05
Compra 2: 119.95 USDT a $0.997 = $119.59
CPP Actual: ($615.05 + $119.59) / (621.95 + 119.95) = $0.9917

Venta 1: 202.74 USDT a $1.05 = $212.76
Costo Base: 202.74 * $0.9917 = $201.07
P&L: $212.76 - $201.07 = $11.69 ✅
```

---

## 🔧 Uso Detallado

### 🎨 **Dashboard Moderno con Rich**

**Comandos principales:**
```bash
# Iniciar dashboard interactivo moderno
python src/dashboard_p2p.py

# Procesamiento automático en batch
python src/script_p2p_tracker.py
```

**Características destacadas de Rich:**
- ✨ **Diseño Visual Moderno**: Paneles redondeados, colores profesionales y layout elegante
- 🎯 **Navegación Intuitiva**: Menús claramente organizados con feedback visual
- 📊 **Tablas Elegantes**: Formato automático con colores para P&L positivo/negativo
- ✅ **Validación Visual**: Mensajes de error y éxito con paneles coloridos
- 🔄 **Paginación Inteligente**: Navegación fluida en datasets grandes
- 🎨 **Tema Consistente**: Paleta de colores unificada en toda la aplicación

**Navegación del Dashboard:**
```
1️⃣ Gestionar Datos de Transacciones
   ├── 📝 Nueva Compra USDT
   ├── 💸 Nueva Venta USDT  
   ├── 🔄 Nueva Conversión Fiat
   └── 👀 Ver Datos Existentes

2️⃣ Ver Resumen Financiero Global
   ├── 💰 P&L Total (Ganancias/Pérdidas)
   ├── 📊 Estado del Inventario
   ├── 📈 ROI y Métricas Principales
   └── 🏢 Desglose por Plataforma

3️⃣ Análisis Detallado por Categoría
   ├── 🏪 Análisis por Plataforma
   ├── 💱 Análisis por Moneda
   ├── 📅 Análisis Temporal
   └── 📋 Historial de Transacciones

4️⃣ Herramientas y Utilidades
   ├── 💾 Crear Backup de Datos
   ├── 📄 Estado de Archivos
   ├── ✅ Validar Integridad de Datos
   └── 🔧 Configuración del Sistema
```

### 🚀 **Scripts y Automatización**

#### Dashboard Principal Rich
```bash
python src/dashboard_p2p.py
```
- 🌈 **Interfaz Rich moderna** con paneles elegantes
- 📝 **Gestión completa** de transacciones con validación visual
- 📊 **Análisis en tiempo real** de P&L y ROI con tablas coloridas
- 🔧 **Herramientas administrativas** con feedback profesional

#### Script Automático
```bash
python src/script_p2p_tracker.py
```
- 🤖 **Procesamiento batch** de datos
- 📈 **Reportes automáticos** en CSV
- 🔍 **Validación de integridad** de datos
- ⚡ **Cálculos optimizados** de CPP y P&L

---

## 📁 Estructura del Proyecto

```
P2P_Profit/
├── 📊 src/                          # Código fuente principal
│   ├── dashboard_p2p.py            # 🎛️ Dashboard interactivo
│   └── script_p2p_tracker.py       # 🤖 Script de procesamiento
├── 📁 data/                         # Datos y archivos CSV
│   ├── compras_usdt.csv            # 📈 Registro de compras
│   ├── ventas_usdt.csv             # 📉 Registro de ventas
│   ├── conversiones_fiat.csv       # 🔄 Conversiones de moneda
│   ├── 📊 reports/                  # Reportes generados
│   │   ├── reporte_ventas_pl.csv   # 💰 P&L por venta
│   │   └── reporte_flujo_fiat.csv  # 💱 Seguimiento de fiat
│   └── 🗄️ backups/                 # Respaldos automáticos
├── 📚 docs/                         # Documentación
│   ├── README.md                   # 📋 Documentación principal (Este archivo)
│   ├── prompt.md                   # 🔧 Guía de desarrollo histórica
│   └── prompt_01.md                # 📖 Especificaciones históricas detalladas
├── 🔧 requirements.txt              # Dependencias Python
├── 📜 LICENSE                       # Licencia del Proyecto
├── 🚫 .gitignore                    # Configuración Git
└── README.md                       # Enlace simbólico o copia del README principal del proyecto
```

### 🗂️ **Descripción de Archivos**

| Archivo/Carpeta | Propósito | Importancia |
|-----------------|-----------|-------------|
| `src/dashboard_p2p.py` | Interfaz interactiva principal | 🔴 Crítico |
| `src/script_p2p_tracker.py` | Motor de cálculos y reportes | 🔴 Crítico |
| `data/compras_usdt.csv` | Base de datos de compras | 🔴 Crítico |
| `data/ventas_usdt.csv` | Base de datos de ventas | 🔴 Crítico |
| `data/reports/` | Reportes y análisis | 🟡 Importante |
| `docs/` | Documentación técnica | 🟢 Opcional |

---

## 🧮 Metodología CPP

### 📊 **¿Qué es el Costo Promedio Ponderado?**

El **CPP (Weighted Average Cost)** es la metodología estándar para calcular el costo real de activos cuando se realizan múltiples compras a diferentes precios.

```
CPP = (Suma de todos los costos en USD) / (Suma de todas las cantidades)
```

### 🔢 **Ejemplo Práctico**

```python
# Compras secuenciales
Compra 1: 100 USDT a $0.98 = $98.00
Compra 2: 200 USDT a $1.02 = $204.00
Compra 3: 150 USDT a $0.99 = $148.50

# Cálculo CPP
Total invertido: $98.00 + $204.00 + $148.50 = $450.50
Total USDT: 100 + 200 + 150 = 450 USDT
CPP = $450.50 / 450 = $1.0011 por USDT

# Al vender 100 USDT a $1.05
Ingreso: 100 * $1.05 = $105.00
Costo base: 100 * $1.0011 = $100.11
P&L = $105.00 - $100.11 = $4.89 ✅
```

### ⚡ **Ventajas del Sistema CPP**

| Ventaja | Descripción |
|---------|-------------|
| 🎯 **Precisión** | Cálculo exacto sin importar la cantidad de transacciones |
| 📊 **Transparencia** | Cada venta muestra su CPP utilizado |
| 🔄 **Actualización continua** | CPP se recalcula automáticamente |
| 📈 **Compliance** | Cumple estándares contables internacionales |
| 🧮 **Auditable** | Trazabilidad completa de cálculos |

---

## 📈 Reportes y Analytics

### 📊 **Reporte de P&L de Ventas**

**Archivo:** `data/reports/reporte_ventas_pl.csv`

```csv
ID_Venta,Fecha_Venta,Cantidad_USDT_Vendida,Ingreso_Neto_en_USD,Costo_Base_USD,Ganancia_Perdida_USD,CPP_Utilizado
V001,2025-06-01,202.74,212.76,201.07,11.69,0.9917
V002,2025-06-02,4000.06,4073.91,3992.91,81.00,0.9982
V003,2025-06-02,1089.88,1146.56,1087.93,58.63,0.9982
```

**Métricas incluidas:**
- 💰 **P&L individual**: Ganancia/pérdida por transacción
- 📊 **CPP utilizado**: Costo promedio al momento de la venta
- 💱 **Conversiones automáticas**: UYU → USD usando tasas reales
- 🏦 **Comisiones incluidas**: Cálculo neto de ganancias

### 💱 **Reporte de Flujo de Fiat**

**Archivo:** `data/reports/reporte_flujo_fiat.csv`

```csv
ID_Venta,Moneda_Generada,Monto_Neto_Generado,Monto_Disponible,Estado_Fiat
V001,UYU,8999.63,8999.63,Disponible
V002,UYU,172326.42,172326.42,Disponible
V003,UYU,48499.66,48499.66,Disponible
```

**Control de flujo:**
- 🔄 **Seguimiento de origen**: Cada peso/dólar rastreado a su venta origen
- 📈 **Estado actualizado**: Disponible, Parcialmente Usado, Totalmente Usado
- 💰 **Saldos en tiempo real**: UYU y USD disponibles para reinversión

### 📊 **Métricas Avanzadas**

#### Dashboard en Consola
```
💰 P&L Total: $151.31 USD
📊 ROI: 5.37%
🪙 Stock USDT: 2,971.72 USDT
💵 Inversión total: $2,966.35 USD
💱 Fiat disponible: 229,825.73 UYU
📈 Operaciones rentables: 3/3 (100%)
```

#### Análisis por Plataforma
```
🏦 Binance: 2 operaciones, P&L: $92.69
💬 WhatsApp: 1 operación, P&L: $58.63
🔄 Otros: 1 operación, P&L: $11.69
```

---

## 🔒 Seguridad y Privacidad

### 🛡️ **Características de Seguridad**

| Aspecto | Implementación |
|---------|----------------|
| 🔐 **Datos locales** | Todo se almacena localmente, sin cloud |
| 📁 **Backup automático** | Respaldos con timestamp en `data/backups/` |
| 🔍 **Validación de entrada** | Verificación de tipos y rangos |
| 📊 **Logs detallados** | Trazabilidad completa de operaciones |
| 🚫 **Sin APIs externas** | No se conecta a internet para cálculos |

### 🔐 **Mejores Prácticas**

```bash
# Backup regular recomendado
# Desde dashboard: 4️⃣ Herramientas → 3️⃣ Exportar Backup

# Gitignore configurado para proteger datos sensibles
echo "data/*.csv" >> .gitignore  # Opcional: excluir datos del repo

# Encriptación adicional (opcional)
gpg --symmetric data/backups/backup_20250603_143000.tar.gz
```

### ⚠️ **Consideraciones Importantes**

- 📊 **Datos financieros**: Este sistema maneja información financiera sensible
- 🔒 **Responsabilidad del usuario**: Mantener backups y seguridad de archivos
- 📈 **Uso fiscal**: Verificar con contador antes de usar para declaraciones
- 🔍 **Auditoría**: Guardar evidencia de transacciones originales

---

## 🤝 Contribución

### 🚀 **¿Cómo contribuir?**

¡Las contribuciones son bienvenidas! Este proyecto sigue las mejores prácticas de desarrollo open source.

#### 🔧 **Setup de Desarrollo**

```bash
# Fork y clone
git clone https://github.com/tu-usuario/p2p-profit.git
cd p2p-profit

# Crear branch para tu feature
git checkout -b feature/nueva-funcionalidad

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Hacer cambios y test
pytest tests/
black src/
flake8 src/

# Commit y push
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

#### 📋 **Guías de Contribución**

| Tipo | Descripción | Proceso |
|------|-------------|---------|
| 🐛 **Bug fix** | Corrección de errores | Issue → Branch → PR |
| ✨ **Feature** | Nueva funcionalidad | Discussion → Issue → PR |
| 📚 **Docs** | Documentación | Direct PR |
| 🔧 **Refactor** | Mejoras de código | Issue → PR |

#### 🎯 **Áreas de Mejora**

- 📱 **GUI Desktop**: Interfaz gráfica con Tkinter/PyQt
- 🌐 **Web Interface**: Dashboard web con Flask/FastAPI
- 📊 **Más exchanges**: Integración con Kraken, Coinbase, etc.
- 🔄 **API REST**: Endpoints para integración externa
- 📈 **Charts avanzados**: Visualizaciones con matplotlib
- 🧪 **Testing**: Cobertura completa de tests

### 🏷️ **Roadmap**

```
📅 v1.1.0 (Q2 2025)
├── 📱 GUI Desktop con Tkinter
├── 📊 Gráficos avanzados
└── 🔄 Integración con más exchanges

📅 v1.2.0 (Q3 2025)
├── 🌐 Dashboard web
├── 📱 App móvil
└── ☁️ Sincronización cloud opcional

📅 v2.0.0 (Q4 2025)
├── 🤖 Machine Learning para predicciones
├── 📊 Analytics avanzados
└── 🔗 API pública
```

---

## 📞 Soporte

### 🆘 **¿Necesitas ayuda?**

| Tipo de consulta | Canal | Tiempo de respuesta |
|------------------|--------|-------------------|
| 🐛 **Bugs** | [GitHub Issues](https://github.com/user/p2p-profit/issues) | 24-48h |
| ❓ **Preguntas** | [Discussions](https://github.com/user/p2p-profit/discussions) | 1-3 días |
| 💡 **Features** | [Feature Requests](https://github.com/user/p2p-profit/issues/new?template=feature_request.md) | 1 semana |
| 🔒 **Seguridad** | security@p2p-profit.com | 24h |

### 📚 **Recursos Adicionales**

- 📖 **Documentación completa**: [Wiki del proyecto](https://github.com/user/p2p-profit/wiki)
- 🎥 **Video tutoriales**: [YouTube Channel](https://youtube.com/p2p-profit)
- 💬 **Comunidad**: [Discord Server](https://discord.gg/p2p-profit)
- 📰 **Blog**: [Actualizaciones y tips](https://blog.p2p-profit.com)

## ❓ FAQ y Troubleshooting

### 🔧 **Problemas Comunes**

**⚠️ Error: ModuleNotFoundError**
```bash
# Solución:
pip install -r requirements.txt
```

**⚠️ Error: FileNotFoundError**
```bash
# Verificar que existan los archivos CSV:
python src/dashboard_p2p.py
# → Seleccionar 4️⃣ Herramientas → 1️⃣ Estado de Archivos
```

**⚠️ Dashboard no muestra datos**
```bash
# 1. Verificar datos existentes
python src/dashboard_p2p.py
# → Seleccionar 1️⃣ Gestionar Datos → 4️⃣ Ver Datos

# 2. Agregar datos de prueba
# → Seleccionar 1️⃣ Gestionar Datos → 1️⃣ Nueva Compra
```

**⚠️ Cálculos incorrectos de P&L**
```bash
# Validar integridad de datos
python src/dashboard_p2p.py
# → Seleccionar 4️⃣ Herramientas → 3️⃣ Validar Datos
```

---

<div align="center">

**[⬆️ Volver al inicio](#-p2p-profit---sistema-de-seguimiento-cripto-profesional)**

---

[![Hecho con ❤️](https://img.shields.io/badge/Hecho%20con-❤️-red?style=flat-square)](https://github.com/user/p2p-profit)
[![Python](https://img.shields.io/badge/Powered%20by-Python-blue?style=flat-square&logo=python)](https://python.org)

**¿Te gustó el proyecto? ¡Dale una ⭐ en GitHub!**

</div>