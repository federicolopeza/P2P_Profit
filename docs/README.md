# Sistema de Seguimiento P2P de USDT

Este sistema permite el seguimiento y análisis completo de transacciones P2P de USDT con cálculo de Profit & Loss (P&L) usando Costo Promedio Ponderado (CPP).

## 🎯 Características Principales

- **Cálculo P&L preciso** usando metodología CPP
- **Soporte multi-moneda** (UYU y USD)
- **Seguimiento de flujo de fiat** generado por ventas
- **Manejo de conversiones** de fiat
- **Rastreo de "restantes"** para reinversión
- **Base de datos en archivos CSV** (texto plano, ubicados en `data/`)
- **Cálculo automático de comisiones** para transacciones en Binance (opcional)
- **Dos herramientas complementarias** para diferentes necesidades (ubicadas en `src/`)

## 📊 Datos de Ejemplo (y Reales)

El sistema puede trabajar con tus datos reales. Si los archivos de datos (`data/compras_usdt.csv`, `data/ventas_usdt.csv`, `data/conversiones_fiat.csv`) no existen al ejecutar los scripts por primera vez, se crearán con **datos de ejemplo** para demostración dentro del directorio `data/`.

### 📈 Compras
- **Archivo**: `data/compras_usdt.csv`

### 📉 Ventas
- **Archivo**: `data/ventas_usdt.csv`

> **Nota**: Los scripts crearán estos archivos en `data/` con datos de ejemplo si no los encuentran. Puedes reemplazarlos o llenarlos con tus transacciones reales.

## 🛠️ Herramientas Disponibles

### 1. 📋 Dashboard Interactivo (`src/dashboard_p2p.py`)
```bash
python src/dashboard_p2p.py
```
- **Análisis profundo** con todos los cálculos
- **Visualización detallada** de toda la información
- **Datos cargados desde `data/`** y gestionados en el script
- **Ingreso de datos interactivo** mediante formularios (guarda en `data/`)
- **Exportación opcional** manual de reportes (a `data/reports/`)
- **Ideal para análisis detallado y gestión interactiva de datos**

### 2. ⚙️ Script Principal (`src/script_p2p_tracker.py`)
```bash
python src/script_p2p_tracker.py
```
- **Procesamiento batch** automático (lee desde `data/`)
- **Generación de reportes** en CSV (a `data/reports/`)
- **Automatización** y cálculos complejos
- **Ideal para procesamiento masivo y generación automática de reportes**

## 📋 Descripción

Este proyecto incluye **dos herramientas** complementarias (ubicadas en la carpeta `src/`) para el seguimiento completo de transacciones de compra y venta de USDT en operaciones P2P:

### 1. **Script Principal (`src/script_p2p_tracker.py`)**
- Cálculo de P&L usando Costo Promedio Ponderado (CPP)
- Seguimiento del flujo de fiat (UYU y USD)
- Manejo de conversiones de fiat
- Rastreo de "restantes" de ventas
- Exportación automática a CSV a la carpeta `data/reports/`

### 2. **Dashboard Interactivo (`src/dashboard_p2p.py`)**
- Ingreso de datos con formularios detallados (guarda en `data/`)
- Visualización completa de cálculos y estados.
- Gestión de archivos CSV (ver estado, crear ejemplos en `data/`, backup en `data/backups/`).
- IDs automáticos y validaciones exhaustivas.
- Dashboard completo con todos los cálculos presentados en consola.
- Opción para exportar los reportes a CSV manualmente (a `data/reports/`).

## 🚀 Instalación y Uso

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Elegir tu herramienta (ambos scripts están en la carpeta `src/`)

#### **📊 Dashboard Interactivo** (Análisis profundo e Interactivo)
```bash
python src/dashboard_p2p.py
```
**Perfecto para**: Análisis detallado, gestión avanzada de datos y archivos, ingreso interactivo de transacciones.

#### **🤖 Script Principal** (Procesamiento batch y reportes automáticos)
```bash
python src/script_p2p_tracker.py
```
**Perfecto para**: Exportación automática de reportes, integración con otros sistemas, procesamiento masivo.

## 📊 Comparación de Herramientas

| Característica      | Dashboard Interactivo (`src/`)     | Script Principal (`src/`)            |
|---------------------|------------------------------------|--------------------------------------|
| **Interfaz**        | 📊 Consola Interactiva (Menús)   | 📄 Terminal (Ejecución directa)    |
| **Entrada datos**   | ✅ Detallada (Formularios, a `data/`) | ❌ Manual (Editando CSV en `data/`)   |
| **Cálculos**        | 🔄 Automáticos (Al visualizar)   | 🔄 Automáticos (Al ejecutar)       |
| **Análisis Profundo**| ⭐ Perfecto                        | ⭐ Perfecto (Datos en `data/reports/`) |
| **Gestión Datos**   | ✅ Avanzada (Menús, en `data/`)    | ❌ Limitada (Directo en `data/`)     |
| **Exportación CSV** | ✅ Opcional (Desde menú, a `data/reports/`) | ⭐ Automática (Al ejecutar, a `data/reports/`) |

## 💡 Cuándo Usar Cada Herramienta

### 📊 **Dashboard Interactivo (`src/dashboard_p2p.py`)** - Análisis Profundo y Gestión Interactiva
```bash
python src/dashboard_p2p.py
```
**Usa cuando:**
- ✅ Necesitas análisis P&L detallado y visualización en consola.
- ✅ Quieres ver flujo de fiat completo.
- ✅ Necesitas ingresar datos de forma interactiva (se guardan en `data/`).
- ✅ Necesitas gestión avanzada de archivos CSV (crear en `data/`, borrar, backup a `data/backups/`).
- ✅ Requieres formularios con todas las opciones para el ingreso de datos.

### 🤖 **Script Principal (`src/script_p2p_tracker.py`)** - Automatización y Reportes
```bash
python src/script_p2p_tracker.py
```
**Usa cuando:**
- ✅ Necesitas exportar reportes (`data/reports/reporte_ventas_pl.csv`, `data/reports/reporte_flujo_fiat.csv`) automáticamente a archivos CSV.
- ✅ Quieres procesamiento batch de los datos (desde `data/`).
- ✅ Podrías integrar la salida con otros sistemas o flujos de trabajo.

## 📁 Archivos de Entrada (ubicados en `data/`)

El sistema espera tres archivos CSV en el directorio `data/`:

### 1. `data/compras_usdt.csv`
```csv
ID_Compra,Fecha_Compra,Cantidad_USDT_Comprada,Moneda_Pago,Precio_Unitario_Moneda_Pago,Tasa_Cambio_UYU_USD_Compra,Fuente_De_Fondos_Fiat,Comisiones_Compra_Moneda_Pago,Plataforma
C001,2024-01-15,100.0,USD,1.0,1.0,Capital Nuevo,0.0,Binance
C002,2024-02-10,200.0,UYU,41.0,41.0,Capital Nuevo,50.0,WhatsApp
```

### 2. `data/ventas_usdt.csv`
```csv
ID_Venta,Fecha_Venta,Cantidad_USDT_Vendida,Moneda_Recibida,Precio_Unitario_Moneda_Recibida,Tasa_Cambio_UYU_USD_Venta,Comisiones_Venta_Moneda_Recibida,Plataforma
V001,2024-02-20,80.0,USD,1.03,1.0,0.5,Otro
V002,2024-03-15,120.0,UYU,42.5,42.5,100.0,WhatsApp
```

### 3. `data/conversiones_fiat.csv` (Opcional)
```csv
ID_Conversion,Fecha_Conversion,Moneda_Origen,Cantidad_Origen,Moneda_Destino,Cantidad_Destino,ID_Venta_Asociada,Notas
CF001,2024-03-20,UYU,5000.0,USD,120.0,N/A,Dashboard Input
```
(Nótese que `ID_Conversion_Fiat` y `Fuente_Conversion_Fiat` fueron actualizados a `ID_Conversion`, `ID_Venta_Asociada` y `Notas` respectivamente en los scripts más recientes para el archivo de conversiones).

## 🔄 Cómo Funciona (Lógica Principal en `src/script_p2p_tracker.py`, utilizada también por el Dashboard)

### 1. Carga de Datos
- Lee los archivos CSV desde `data/` y valida los datos.
- Convierte fechas y ordena transacciones cronológicamente.

### 2. Cálculos Preliminares
- **Compras**: Calcula costo total en USD usando tasas de cambio.
- **Ventas**: Calcula ingresos netos en USD.

### 3. Procesamiento CPP
- Mantiene inventario USDT con costo promedio ponderado.
- Calcula P&L real de cada venta usando CPP.

### 4. Seguimiento de Fiat
- Rastrea el fiat generado por cada venta.
- Controla cómo se reutiliza en nuevas compras.
- Maneja conversiones UYU ↔ USD.

### 5. Reportes
Genera (o permite generar) reportes principales que se guardan en `data/reports/`:
- **Ventas con P&L**: Ganancia/pérdida de cada operación.
- **Inventario USDT**: Stock actual y CPP (principalmente en consola).
- **Flujo de Fiat**: Saldos disponibles por moneda.

## 📊 Reportes de Salida

### Archivos CSV generados (en `data/reports/` por `src/script_p2p_tracker.py` o vía `src/dashboard_p2p.py`):
- `data/reports/reporte_ventas_pl.csv`: Detalle de P&L por venta.
- `data/reports/reporte_flujo_fiat.csv`: Estado del fiat generado.

### Reportes en consola (ambos scripts muestran información, el Dashboard de forma más interactiva):
- Resumen de P&L total.
- ROI aproximado.
- Saldos fiat disponibles.
- Inventario USDT actual.

## 🎯 Características Clave

### ✅ Implementadas:
- Cálculo CPP preciso.
- Manejo multi-moneda (UYU/USD).
- Seguimiento de conversiones fiat.
- Rastreo de origen de fondos.
- Validación de datos.
- Reportes detallados.
- Archivos de ejemplo automáticos (si los principales no existen, a través de las funciones de los scripts).

### 🔧 Características Técnicas:
- Código modular y bien documentado.
- Manejo de errores.
- Interfaz de consola interactiva en `src/dashboard_p2p.py`.
- Compatible con pandas estándar.
- Cálculo automático opcional de comisiones de Binance.

## 💡 Tips de Uso

### Formato de Fuente de Fondos:
- `"Capital Nuevo"`: Dinero nuevo aportado.
- `"Venta_ID_V001"`: Proviene de la venta V001.
- `"Conversion_Fiat_ID_CF001"`: Proviene de conversión CF001.

### Formato de Conversiones:
- `"Restante_Venta_ID_V002"`: Conversión del restante de venta V002.
- `"Ahorros_Generales_UYU"`: Conversión de ahorros acumulados.

## 🚨 Importante

1.  **Orden cronológico**: Las fechas deben permitir ordenación correcta.
2.  **IDs únicos**: Cada transacción debe tener ID único.
3.  **Plataforma**: Indicar la plataforma (ej. Binance, WhatsApp, Otro) para cada compra/venta.
4.  **Tasas de cambio**: Siempre en formato UYU/USD cuando aplique.
5.  **Consistencia**: Mantener formato de moneda ("USD" o "UYU").

## 🛠️ Personalización

El código está diseñado para ser fácilmente modificable:
- **Formularios (`src/dashboard_p2p.py`)**: Agregar campos o validaciones.
- **Cálculos (`src/script_p2p_tracker.py`)**: Modificar lógica o añadir nuevas métricas.
- **Integración**: Conectar con APIs o bases de datos.

## 📞 Soporte

Si necesitas modificaciones o encuentras algún problema, el código está bien comentado y estructurado para facilitar las adaptaciones.

**Recomendación de uso:**
1. **Análisis y Gestión Interactiva**: `src/dashboard_p2p.py` 📊  
2. **Reportes Automáticos y Procesamiento Batch**: `src/script_p2p_tracker.py` 🤖 

## 📁 Estructura del Proyecto Propuesta

```
P2P_Profit/
├── .gitignore
├── LICENSE
├── requirements.txt
├── docs/
│   ├── README.md
│   ├── prompt.md
│   └── prompt_01.md
├── src/
│   ├── script_p2p_tracker.py
│   └── dashboard_p2p.py
└── data/
    ├── compras_usdt.csv
    ├── ventas_usdt.csv
    ├── conversiones_fiat.csv
    ├── reports/
    │   ├── reporte_ventas_pl.csv
    │   └── reporte_flujo_fiat.csv
    └── backups/
        └── (aquí se guardarán los backups, ej: backup_compras_20240325_103000.csv)
```

Esta estructura organiza el código fuente en `src/`, los datos de entrada y salida en `data/` (con subcarpetas para reportes y backups), y la documentación en `docs/`.

**Archivos de Datos y Ejemplo:**
- Los archivos `compras_usdt.csv`, `ventas_usdt.csv`, y `conversiones_fiat.csv` deben residir en la carpeta `data/`.
- Si alguno de estos archivos no se encuentra al ejecutar los scripts, se crearán automáticamente con datos de ejemplo en la carpeta `data/`. Puedes luego modificar estos archivos con tus datos reales.

**Reportes:**
- Los reportes generados, como `reporte_ventas_pl.csv` y `reporte_flujo_fiat.csv`, se guardarán en `data/reports/`.

**Backups:**
- La función de backup del dashboard interactivo guardará copias de seguridad de tus archivos de datos en `data/backups/`. 