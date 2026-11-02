# -----------------------------------------------------------------------------#
#                                                                              #
#                                  FINANZAS I                                  #
#                                                                              #
# PROFESOR/AUXILIAR: LUISA RODRIGUEZ FAJARDO           UNIVERSIDAD DE CHILE    #
#                                                                              #
# ---------------------------------------------------------------------------- #

# -----------------------------------------------------------------------------#
# LIBRERÍAS EN R: ¿QUÉ SON Y PARA QUÉ SE USAN?--------------------------------
# -----------------------------------------------------------------------------#
# ¿Qué es una librería (o paquete) en R?
# Una librería es una colección de funciones, datos y documentación que extiende
# las capacidades básicas de R. Permiten realizar tareas específicas como:
# - Leer archivos Excel o CSV
# - Manipular datos (dplyr, tidyr)
# - Crear gráficos (ggplot2)
# - Descargar datos financieros (quantmod)
# - Trabajar con fechas (lubridate)
# - Y mucho más...

# -----------------------------------------------------------------------------#
# ¿Cómo se INSTALA una librería?
# Esto se hace UNA sola vez por equipo (no se repite cada vez que corras el script)

# Sintaxis:
# install.packages("nombre_del_paquete")

# Ejemplos:
# install.packages("dplyr")      # Manipulación de datos
# install.packages("readxl")     # Leer archivos .xlsx
# install.packages("ggplot2")    # Visualización de datos
# install.packages("lubridate")  # Manejo de fechas
# install.packages("quantmod")   # Finanzas

# -----------------------------------------------------------------------------#
# ¿Cómo se CARGA una librería?
# Esto SÍ debe hacerse cada vez que inicias un script o reinicias R.

# Sintaxis:
# library(nombre_del_paquete)

# Ejemplos:
library(dplyr)
library(readxl)
library(ggplot2)

# Nota: Si la librería no está instalada, R mostrará un error.
# Solución: instalarla primero con install.packages("nombre")

# -----------------------------------------------------------------------------#
# Recomendación:
# Al inicio de tus scripts, carga todas las librerías que vas a usar.
# Si estás trabajando en un equipo, puedes usar condicionales para evitar errores:

# if (!require("readxl")) install.packages("readxl")
# library(readxl)

# Esto verifica si el paquete ya está instalado y, si no lo está, lo instala automáticamente.


# =============================================================================#
# Instalación y carga de librerías esenciales para análisis financiero
# =============================================================================#

# Instalar paquetes (solo una vez)
# install.packages(c(
#  "tidyverse",          # Manipulación de datos, gráficos, lectura de archivos
#  "lubridate",          # Manejo de fechas y tiempos
#  "xts",                # Estructuras para series temporales
#  "zoo",                # Manipulación de series temporales
#  "quantmod",           # Descarga y análisis de datos financieros
#  "PerformanceAnalytics", # Métricas de desempeño financiero
#  "tseries",            # Análisis de series temporales y pruebas estadísticas
#  "forecast",           # Modelado y predicción de series temporales
#  "readxl",             # Lectura de archivos Excel (.xlsx)
#  "writexl",            # Escritura de archivos Excel (.xlsx)
#  "data.table",         # Manipulación rápida de grandes volúmenes de datos
#  "car",                # Herramientas de regresión y ANOVA
#  "psych",              # Estadísticas descriptivas, análisis factorial
#  "corrplot",           # Visualización de matrices de correlación
#  "scales"              # Formato de escalas en gráficos (%, moneda, etc.)
# ))

# Cargar los paquetes (se debe hacer cada vez que se use R)
library(tidyverse)
library(lubridate)
library(xts)
library(zoo)
library(quantmod)
library(PerformanceAnalytics)
library(tseries)
library(forecast)
library(writexl)
library(data.table)
library(car)
library(psych)
library(corrplot)
library(scales)

# Mensaje informativo
cat("¡Librerías cargadas con éxito! Ya puedes trabajar con datos financieros en R.\n")

# Eb ocaciónes se puden encontrar estos tipos de operadores:

# "%>%" se llama pipe operator (operador de tubería) y proviene del paquete 
# magrittr (heredado por todo el tidyverse).
# Su función es encadenar varias operaciones de manera legible, “pasando” el 
# resultado del paso anterior como primer argumento del siguiente paso

# "%in%" Devuelve un vector lógico del mismo largo que x; cada posición es TRUE 
# si el elemento correspondiente de x aparece al menos una vez en y, 
# FALSE en caso contrario

# Ejemplo: Piensa en %in% como la pregunta «¿está esto dentro de aquello?».
# c("manzana", "pera", "uva") %in% c("pera", "mango", "kiwi")
# Resultado en consola:  FALSE  TRUE FALSE




# (Opcional) Muestra el directorio de trabajo actual (donde se guardarán archivos)
getwd()
# Si quieres cambiarlo, descomenta y ajusta la ruta:
# setwd("C:/Users/TuUsuario/Documentos/R")

rm(list = ls())
gc()


# =============================================================================#
#                      DESCARGA DE DATOS DESDE YAHOO FINANCE-------------------
# =============================================================================#

# Cargar paquetes necesarios
library(quantmod)   # Para descargar y manipular datos financieros
library(dplyr)      # Para manipular datos de forma moderna
library(lubridate)  # Para trabajar con fechas
library(tidyquant)  # Simplifica todo con sintaxis tidyverse

# Nota: pedir la ayuda para que vean la librería de tidyquant
help("tidyquant")

tq_get_options() # para que vean las opciones de descarga

# -----------------------------------------------------------------------------#
# Descargar y ver datos de Apple y Microsoft
# -----------------------------------------------------------------------------#
datos_tidy <- tq_get(
  c("AAPL", "MSFT"),       #  vector con los símbolos bursátiles
  from = "2023-01-01",     #  fecha inicial de la serie
  to   = "2024-01-01",     #  fecha final (no incluida)
  get  = "stock.prices",   #  indica que queremos precios
  periodicity = "monthly") #  periodicidad: mensual

# Mostrar los primeros datos
head(datos_tidy)

# Vista rápida por empresa
datos_tidy %>% 
  group_by(symbol) %>% 
  summarise(Primera_fecha = min(date),
            Última_fecha  = max(date),
            Registros     = n())

# Nota: Cuando no se especifica periodicidad se descrga automaticamente con 
# frecuencia diaria


# --------- OPCIONAL: datos ANUALES (demostración de error intencional) --------
# Hacer esta opción para que vean el error que arroja

datos_tidy <- tq_get(
  c("AAPL", "MSFT"),       
  from = "2023-01-01",     
  to   = "2024-01-01",     
  get  = "stock.prices",   
  periodicity = "yearly") # <-- ESTO DARÁ ERROR (a propósito)



# =============================================================================#
#                       GUÍA: CÁLCULO DE RETORNOS EN R ------------
# =============================================================================#
#
# Objetivo:
#   Calcular retornos financieros con distintos niveles de dificultad:
#
#   1. Cambio absoluto del precio.
#   2. Retorno simple o aritmético.
#   3. Retorno logarítmico.
#   4. Retornos de varios períodos.
#   5. Retornos acumulados.
#   6. Retornos mensuales.
#   7. Retornos y volatilidad anualizados.
#   8. Medidas móviles.
#   9. Retorno total, retorno de una cartera y retorno en exceso.
#
# ==============================================================================#

# ------------------------------------------------------------------------------#
# 2. CAMBIO DE PRECIO, RETORNO SIMPLE Y RETORNO LOGARÍTMICO---------------
# ------------------------------------------------------------------------------#

# Sea P_t el precio actual y P_(t-1) el precio del período anterior.
#
# Cambio absoluto:
#
#     Delta P_t = P_t - P_(t-1)
#
# Retorno simple en forma decimal:
#
#     R_t = (P_t - P_(t-1)) / P_(t-1)
#         = P_t / P_(t-1) - 1
#
# Retorno logarítmico en forma decimal:
#
#     r_t = ln(P_t / P_(t-1))
#         = ln(1 + R_t)
#
# Para expresar un retorno decimal como porcentaje, se multiplica por 100.

datos_tidy <- datos_tidy |>
  group_by(symbol) |>                                # Separa cada empresa
  arrange(date, .by_group = TRUE) |>                 # Orden temporal interno
  mutate(
    precio_t_1 = lag(close, n = 1),                  # Precio del período previo
    
    cambio_precio = close - precio_t_1,              # Cambio en unidades monetarias
    factor_crecimiento = close / precio_t_1,         # P_t / P_(t-1)
    
    retorno_simple_dec = factor_crecimiento - 1,     # Retorno simple decimal
    retorno_simple_pct = 100 * retorno_simple_dec,   # Retorno simple porcentual
    
    retorno_log_dec = log(factor_crecimiento),       # Retorno log decimal
    retorno_log_pct = 100 * retorno_log_dec          # Retorno log porcentual
  ) |>
  ungroup()


# La primera observación de cada empresa tendrá NA porque no existe un precio
# anterior con el cual compararla. Esto es normal y no representa un error.


# ============================================================#
# Estadísticas básicas sobre precios y retornos----------------
# ============================================================#

# Filtrar AAPL y ver resumen de los precios ajustados
datos_tidy |> 
  filter(symbol == "AAPL") |>          # ⬅ solo Apple
  pull(adjusted) |>                    # extrae vector → summary() necesita un vector numérico
  summary()
# Mín, 1er cuartil, mediana, media, 3er cuartil y máximo

summary(datos_tidy) # de esta manera se obtiene el resumen de toda la base

summary(datos_tidy$adjusted[datos_tidy$symbol == "AAPL"]) #alternativa más sencilla

summary(subset(datos_tidy, symbol == "AAPL")$adjusted) # otra alterantiva

# Si quiero especificar cada metrica:

datos_tidy |>
  filter(symbol == "AAPL") |>
  summarise(
    Min.   = min(adjusted),
    Q1     = quantile(adjusted, 0.25),
    Median = median(adjusted),
    Mean   = mean(adjusted),
    Q3     = quantile(adjusted, 0.75),
    Max.   = max(adjusted)
  )

# Media del precio ajustado
datos_tidy |> 
  filter(symbol == "AAPL") |> 
  summarise(mean_adj = mean(adjusted, na.rm = TRUE))


# Desviación estándar del Close (volatilidad)
datos_tidy |> 
  filter(symbol == "AAPL") |> 
  summarise(sd_close = sd(close, na.rm = TRUE))


# a) Base R
sd(datos_tidy$close[datos_tidy$symbol == "AAPL"], na.rm = TRUE)

# b) subset() + with()
with(subset(datos_tidy, symbol == "AAPL"), sd(close, na.rm = TRUE))


# Estadistica para ambas acciones agrupadas
datos_tidy |> 
  group_by(symbol) |>                        # agrupa por ticker
  summarise(
    mean_adj   = mean(adjusted, na.rm = TRUE),
    sd_close   = sd(close,    na.rm = TRUE),
    mean_rt    = mean(Rt,  na.rm = TRUE),
    .groups = "drop"                         # evita que el resultado siga “agrupado”
  )

# | Columna    | Qué significa                                      |
# | ---------- | -------------------------------------------------- |
# | `mean_adj` | Precio ajustado promedio en el periodo.            |
# | `sd_close` | Volatilidad (desv. estándar) del precio de cierre. |
# | `mean_rt`  | Rentabilidad logarítmica media mensual.            |
  

# Estadísticas para un subconjunto dinámico
library(data.table)

setDT(datos_tidy)[symbol %in% c("AAPL","MSFT"),
                  .( mean_adj = mean(adjusted, na.rm = TRUE),
                     sd_adj   = sd(adjusted,   na.rm = TRUE),
                     mean_clo = mean(close,    na.rm = TRUE),
                     sd_clo   = sd(close,      na.rm = TRUE),
                     mean_ret = mean(Rt,  na.rm = TRUE),
                     sd_ret   = sd(Rt,    na.rm = TRUE)
                  ), by = symbol]
