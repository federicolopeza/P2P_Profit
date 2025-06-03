Okay, aquí tienes un prompt detallado que puedes usar para guiar a una IA o a un desarrollador en la creación del script en Python. Este prompt se basa en la estrategia que definimos.

---

## Prompt para Desarrollar Script Python de Seguimiento P2P Cripto

**Objetivo Principal del Script:**

Desarrollar un script en Python para realizar un seguimiento de transacciones de compra y venta de USDT (P2P), manejando múltiples monedas fiat (UYU y USD), calculando la rentabilidad (P&L) de las operaciones con USDT utilizando el método de Costo Promedio Ponderado (CPP), y rastreando el flujo de los fondos fiat generados por las ventas, incluyendo su posible conversión y reinversión.

---

**I. Estructuras de Datos (Entrada):**

El script deberá ser capaz de leer y procesar datos desde archivos CSV. Cada CSV representará una tabla lógica. Se recomienda usar la librería Pandas para manejar estos datos.

1.  **`compras_usdt.csv`:**
    * `ID_Compra`: String (Identificador único de la compra)
    * `Fecha_Compra`: String (Formato AAAA-MM-DD)
    * `Cantidad_USDT_Comprada`: Float
    * `Moneda_Pago`: String ("UYU" o "USD")
    * `Precio_Unitario_Moneda_Pago`: Float
    * `Tasa_Cambio_UYU_USD_Compra`: Float (UYU por 1 USD; si `Moneda_Pago` es USD, puede ser 1 o N/A)
    * `Fuente_De_Fondos_Fiat`: String (Ej: "Capital Nuevo", "Venta_ID_XXX", "Conversion_Fiat_ID_YYY")
    * `Comisiones_Compra_Moneda_Pago`: Float (Opcional, comisiones en la `Moneda_Pago`)

2.  **`ventas_usdt.csv`:**
    * `ID_Venta`: String (Identificador único de la venta de USDT y del fiat generado)
    * `Fecha_Venta`: String (Formato AAAA-MM-DD)
    * `Cantidad_USDT_Vendida`: Float
    * `Moneda_Recibida`: String ("UYU" o "USD")
    * `Precio_Unitario_Moneda_Recibida`: Float
    * `Tasa_Cambio_UYU_USD_Venta`: Float (UYU por 1 USD; si `Moneda_Recibida` es USD, puede ser 1 o N/A)
    * `Comisiones_Venta_Moneda_Recibida`: Float (Opcional, comisiones en la `Moneda_Recibida`)

3.  **`conversiones_fiat.csv`:**
    * `ID_Conversion_Fiat`: String (Identificador único de la conversión)
    * `Fecha_Conversion`: String (Formato AAAA-MM-DD)
    * `Moneda_Origen`: String ("UYU" o "USD")
    * `Cantidad_Origen`: Float
    * `Moneda_Destino`: String ("UYU" o "USD")
    * `Cantidad_Destino`: Float
    * `Fuente_Conversion_Fiat`: String (Ej: "Restante_Venta_ID_XXX", "Ahorros_Generales_UYU")

*(Nota: La `Tabla_Tasas_Cambio_Diarias_UYU_USD` es implícita. Si la tasa no está en la transacción, el script podría tener una función para buscarla en un CSV aparte o requerirla como input si falta. Para simplificar, asumimos que la tasa relevante está en las filas de `compras_usdt.csv` y `ventas_usdt.csv` si la moneda es UYU).*

---

**II. Funcionalidades Clave del Script:**

1.  **Carga y Validación de Datos:**
    * Cargar los datos desde los archivos CSV a DataFrames de Pandas.
    * Validar tipos de datos básicos y la presencia de columnas esenciales.
    * Convertir columnas de fecha a objetos datetime.
    * Ordenar las transacciones por fecha.

2.  **Cálculos Preliminares en Compras:**
    * Para cada compra en `compras_usdt.csv`:
        * `Costo_Total_Moneda_Pago = Cantidad_USDT_Comprada * Precio_Unitario_Moneda_Pago + Comisiones_Compra_Moneda_Pago`
        * `Costo_Total_en_USD`:
            * Si `Moneda_Pago` == "USD", es igual a `Costo_Total_Moneda_Pago`.
            * Si `Moneda_Pago` == "UYU", es `Costo_Total_Moneda_Pago / Tasa_Cambio_UYU_USD_Compra`.
        * `Costo_Adquisicion_Unitario_USD = Costo_Total_en_USD / Cantidad_USDT_Comprada`.
        * Añadir estas columnas calculadas al DataFrame de compras.

3.  **Cálculos Preliminares en Ventas:**
    * Para cada venta en `ventas_usdt.csv`:
        * `Ingreso_Total_Moneda_Recibida = Cantidad_USDT_Vendida * Precio_Unitario_Moneda_Recibida - Comisiones_Venta_Moneda_Recibida`
        * `Ingreso_Neto_en_USD`:
            * Si `Moneda_Recibida` == "USD", es igual a `Ingreso_Total_Moneda_Recibida`.
            * Si `Moneda_Recibida` == "UYU", es `Ingreso_Total_Moneda_Recibida / Tasa_Cambio_UYU_USD_Venta`.
        * Añadir estas columnas calculadas al DataFrame de ventas.

4.  **Implementación del Costo Promedio Ponderado (CPP) y P&L:**
    * Inicializar: `inventario_usdt_cantidad = 0`, `inventario_usdt_costo_total_usd = 0`.
    * Procesar todas las transacciones (compras y ventas combinadas y ordenadas por fecha).
    * **Al procesar una Compra:**
        * `inventario_usdt_cantidad += Cantidad_USDT_Comprada` (de la compra actual).
        * `inventario_usdt_costo_total_usd += Costo_Total_en_USD` (de la compra actual).
    * **Al procesar una Venta:**
        * Calcular `cpp_actual_usdt`:
            * Si `inventario_usdt_cantidad > 0`, `cpp_actual_usdt = inventario_usdt_costo_total_usd / inventario_usdt_cantidad`.
            * Manejar caso `inventario_usdt_cantidad == 0` (error o advertencia, no se puede vender sin stock).
        * `Costo_Base_USD_de_USDT_Vendido = Cantidad_USDT_Vendida * cpp_actual_usdt`.
        * `Ganancia_Perdida_USDT_en_USD = Ingreso_Neto_en_USD` (de la venta actual) `- Costo_Base_USD_de_USDT_Vendido`.
        * Guardar `Costo_Base_USD_de_USDT_Vendido` y `Ganancia_Perdida_USDT_en_USD` asociados a la venta.
        * Actualizar inventario:
            * `inventario_usdt_costo_total_usd -= Costo_Base_USD_de_USDT_Vendido`.
            * `inventario_usdt_cantidad -= Cantidad_USDT_Vendida`.

5.  **Seguimiento del Flujo de Fiat (Manejo de "Restantes"):**
    * Crear una estructura (ej. un diccionario o DataFrame) para rastrear el fiat generado por cada venta y su estado.
        * Clave: `ID_Venta`.
        * Valores: `Moneda_Generada`, `Monto_Neto_Generado_Moneda_Original`, `Monto_Fiat_Utilizado_Moneda_Original`, `Monto_Fiat_Disponible_Moneda_Original`, `Estado_Fiat` ("Disponible", "Parcialmente Usado", "Totalmente Usado", "Convertido").
    * **Al procesar una Venta:** Registrar el `Ingreso_Neto_Moneda_Recibida` en esta estructura.
    * **Al procesar una Compra:**
        * Verificar `Fuente_De_Fondos_Fiat`.
        * Si la fuente es "Venta\_ID\_XXX":
            * Identificar la moneda y el monto de la compra (`Costo_Total_Moneda_Pago`).
            * Actualizar el `Monto_Fiat_Utilizado_Moneda_Original` y `Monto_Fiat_Disponible_Moneda_Original` para `ID_Venta_XXX` en la estructura de seguimiento de fiat. Actualizar `Estado_Fiat`.
    * **Al procesar una `Conversion_Fiat`:**
        * Verificar `Fuente_Conversion_Fiat`. Si es "Restante\_Venta\_ID\_XXX":
            * Actualizar el `Monto_Fiat_Utilizado_Moneda_Original` (marcando que se usó para conversión) y `Estado_Fiat` (a "Convertido") para `ID_Venta_XXX`.
        * Registrar el `Cantidad_Destino` y `Moneda_Destino` como un nuevo monto fiat disponible, asociado al `ID_Conversion_Fiat`. (Este monto puede luego ser usado en una compra, referenciando `Fuente_De_Fondos_Fiat` = "Conversion\_Fiat\_ID\_YYY").

6.  **Generación de Reportes (Salida):**
    * **Reporte de Transacciones de Venta:** Un nuevo CSV o DataFrame que incluya, para cada venta:
        * Todos los campos originales de `ventas_usdt.csv`.
        * `Ingreso_Neto_en_USD` (calculado).
        * `Costo_Base_USD_de_USDT_Vendido` (calculado).
        * `Ganancia_Perdida_USDT_en_USD` (calculado).
    * **Reporte de Estado de Inventario USDT:**
        * `Cantidad_USDT_Actual_En_Stock`.
        * `Costo_Total_USD_Del_Stock_Actual`.
        * `CPP_Actual_USDT`.
    * **Reporte de Flujo de Fiat (Opcional Avanzado):**
        * Un resumen de los saldos fiat disponibles (UYU y USD) provenientes de operaciones cripto, detallando su origen (`ID_Venta` o `ID_Conversion_Fiat`) si es posible.
        * Estado de cada `Ingreso_Neto_Moneda_Recibida` de las ventas.
    * Mostrar los reportes en la consola y/o guardarlos como nuevos archivos CSV.

---

**III. Consideraciones Adicionales:**

* **Librerías:** Recomendar `pandas` para la manipulación de datos.
* **Modularidad:** Estructurar el código en funciones claras (ej. `cargar_datos()`, `calcular_cpp_y_pl()`, `rastrear_fiat()`, `generar_reportes()`).
* **Manejo de Errores:** Incluir manejo básico de errores (ej. archivos no encontrados, datos faltantes cruciales, ventas sin stock suficiente).
* **Comentarios en el Código:** El script debe estar bien comentado para explicar la lógica.
* **Suposiciones:** Asumir que los IDs son únicos y que las fechas permiten una ordenación cronológica correcta de las operaciones.

---

Este prompt debería ser lo suficientemente detallado para que una IA o un desarrollador comprenda la tarea y pueda empezar a construir el script. ¡Mucha suerte con ello!