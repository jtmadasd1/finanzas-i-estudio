# -----------------------------------------------------------------------------#
#                                                                              #
#                                 FINANZAS I                                   #
#                                                                              #
# PROFESOR/AUXILIAR: LUISA RODRIGUEZ FAJARDO          UNIVERSIDAD DE CHILE     #
#                                                                              #
# ---------------------------------------------------------------------------- #

# -----------------------------------------------------------------------------#
# CREACIÓN DE VARIABLES EN R------------------------------------------------
# -----------------------------------------------------------------------------#

# Una operación simple se puede realizar directamente:
5 + 5
20

# También se puede mostrar texto directamente:
"Ayudantía Finanzas I!"
print("Ayudantía Finanzas I!")  # Imprime texto en la consola

# DESVENTAJA: los resultados no se almacenan, por lo tanto no se pueden reutilizar después.
# Es mejor guardar los resultados en una variable si se necesitarán más adelante.

# -----------------------------------------------------------------------------#
# ¿Por qué crear variables?
# - Permite guardar valores para su uso posterior.
# - Facilita el análisis, evita repetir cálculos y mejora la organización del código.

# VENTAJAS DE CREAR VARIABLES:
# - Permite guardar y reutilizar información.
# - Facilita el trabajo con datos más adelante.
# - Mejora la legibilidad y mantenibilidad del código.
# -----------------------------------------------------------------------------#

# En R se pueden usar "=" o "<-" para asignar valores a una variable. Ambas formas son equivalentes.

# Ejemplos de nombres válidos para variables:
myvar  = "Finance"
my_var = "Finance"
myVar  = "Finance"
MYVAR  = "Finance"
myvar2 = "Finance"

# Nombres válidos deben comenzar con una letra y solo pueden contener letras, números y guiones bajos (_).

# Ejemplos de nombres inválidos (no se deben usar, generan error si se descomentan):
# 2myvar = "Finance"
# my-var = "Finance"
# my var = "Finance"
# _my_var = "Finance"
# my_v@ar = "Finance"
# TRUE = "Finance"     # 'TRUE' es una palabra reservada
# .myvar = "Finance"   # los nombres que comienzan con punto tienen usos especiales


# -----------------------------------------------------------------------------#
# TIPOS DE VARIABLES EN R------------------------------------------------
# -----------------------------------------------------------------------------#

name      = "John"      # character: cadena de texto
age       = 40          # numeric: número entero
range     = 1:50        # integer sequence: del 1 al 50, con incremento de 1
nume      = 2.855       # numeric: número decimal
complejo  = 3i          # complex: parte real = 0, parte imaginaria = 3
logic     = age == 30   # logical: comparación (FALSE)
boolean   = TRUE        # logical: valor lógico verdadero


# ¿Qué es una secuencia?
# Una secuencia es una serie ordenada de números, como 1, 2, 3, ..., 50.
# En R, las secuencias permiten trabajar fácilmente con rangos de valores.

# ¿Qué es un vector?
# Un vector es un conjunto de elementos del mismo tipo, como una lista ordenada de valores.
# Es la estructura más básica y fundamental en R.



# Visualizar valores guardados:
name
age

print(name)
print(age)

# -----------------------------------------------------------------------------#
# CREACIÓN DE VECTORES Y DATA FRAMES-----------------------------------------
# -----------------------------------------------------------------------------#
# Crear un vector de texto:
names = c("Ana", "Luis", "María")

# Crear un vector numérico:
ages = c(25, 30, 28)

# La función c() significa "combine" y se usa para crear vectores.

# Crear un Data Frame con dos columnas:
datos = data.frame(name, ages)

# ¿Qué es un Data Frame?
# Es una tabla de datos (similar a una hoja de Excel), con columnas que pueden tener distintos tipos.
# Es una de las estructuras más utilizadas para análisis de datos en R.

# Visualizar los datos en una pestaña tipo Excel (solo en RStudio):
View(datos)                        # abre vista tipo Excel (solo en RStudio)


# -----------------------------------------------------------------------------#
# ASIGNAR MISMO VALOR A VARIAS VARIABLES----------------------------------------
# -----------------------------------------------------------------------------#

var1 = var2 = var3 = "Orange"
var1
var2
var3

# Eliminar una variable del entorno (rm=remove):
rm(var1)         # elimina una sola variable
# rm(list = "age") # también se puede eliminar usando el nombre en una lista

# -----------------------------------------------------------------------------#
# VERIFICACIÓN Y CONVERSIÓN DE CLASES---------------------------------------
# -----------------------------------------------------------------------------#

# La clase de un objeto define el tipo de datos que contiene y cómo se debe 
#tratar ese objeto dentro de funciones o cálculos

# Ver tipo de variable con class():
class(name)
class(age)
class(range)
class(nume)
class(complejo)
class(logic)

# Convertir tipo de variable:
as.integer(nume)    # convierte a entero

x = "8"
class(x)            # character
z = as.numeric(x)
class(z)            # numeric

# ----------------------------------------------------------------------------------#
# CLASES COMUNES DE OBJETOS EN R ------------
# ----------------------------------------------------------------------------------#
# Clase         | Descripción                                      | Ejemplo
# ------------- | ------------------------------------------------ | -------------------------------#
# "numeric"     | Números reales o decimales                       | x = 3.14
# "integer"     | Números enteros                                  | y = as.integer(10)
# "character"   | Texto o cadenas de caracteres                    | z = "Hola"
# "logical"     | Valores TRUE o FALSE                             | a = 5 > 2
# "complex"     | Números complejos (parte real + imaginaria)      | b = 3 + 2i
# "factor"      | Variables categóricas con niveles definidos      | f = factor(c("alto", "bajo"))
# "data.frame"  | Tabla de datos con columnas de distintos tipos   | df = data.frame(x = 1:3)
# "list"        | Conjunto de elementos de diferentes clases       | lista = list(1, "texto", TRUE)
# ----------------------------------------------------------------------------------#
# Ver la clase de un objeto con la función class():
# class(x)

# -----------------------------------------------------------------------------#
# CONCATENACIÓN DE VARIABLES-------------------------------------------------
# -----------------------------------------------------------------------------#

# paste(): une elementos como texto (los convierte en strings)
# paste(): une valores como texto, separados por espacio

text = "awesome"
paste("R is", text)

text1 = "R is"
text2 = "awesome"
paste(text1, text2)
paste(text, age)

m = 56
n = 80
paste(m, n)

# Concatenación simple con c(): combina elementos en un vector
c(text1, text2)

# Concatenar secuencias:
range2 = 50:100
c(range, range2)

# OJO: combinar números y texto con c() convierte todo a texto.
c(range, text)

# -----------------------------------------------------------------------------#
# MANEJO DE VALORES NA Y FILTRADO DE VECTORES----------------------------------
# -----------------------------------------------------------------------------#

con = c(2, 5, 6, NA, 10, "Finance")  # vector mixto con texto y NA
con

# na.remove() no existe como función base en R, se recomienda usar:
# con[!is.na(con)] # para eliminar NA
# Pero si tienes definida una función llamada na.remove, asegúrate que esté cargada antes.

# Alternativas seguras:
con_sin_na = con[!is.na(con)]  # elimina NA
vector_sin_finance = con_sin_na[con_sin_na != "Finance"]  # quita el texto

# Todo en una sola línea:
vector_limpio = con[!is.na(con) & con != "Finance"]


# Otro Ejemplo
x = c(1, 2, NA, 4, NA)

# Opción 1: eliminar NAs con indexación lógica
x_limpio <- x[!is.na(x)]

# Opción 2: eliminar con na.omit()
x_sin_na <- na.omit(x)


# -----------------------------------------------------------------------------#
# CREACIÓN DE SECUENCIAS-----------------------------------------------------
# -----------------------------------------------------------------------------#
# Una secuencia en R es una serie de números ordenados que siguen una lógica determinada 
#(por ejemplo, de 1 en 1, de 2 en 2, etc.).

# seq(): genera una secuencia desde 1 hasta 20, incrementando de 2 en 2
seq = seq(1, 20, by = 2)
seq

# Ejemplos con el operador ":"
1:5       # Resultado: 1 2 3 4 5
10:1      # Resultado: 10 9 8 ... 1

# Ejemplos con la función seq()
seq(1, 10)                # Secuencia del 1 al 10 (incremento de 1)
seq(1, 10, by = 2)        # Incrementa de 2 en 2: 1 3 5 7 9
seq(0, 1, length.out = 5) # 5 valores espaciados equitativamente entre 0 y 1


# -----------------------------------------------------------------------------#
# OPERACIONES MATEMÁTICAS BÁSICAS EN R------------------------------------------
# -----------------------------------------------------------------------------#

#  Redondeo:
ceiling(1.4)   # Redondea hacia arriba al entero más cercano → 2
floor(1.4)     # Redondea hacia abajo al entero más cercano → 1
round(2.855, 2) # Redondea a 2 decimales → 2.86

# Valor absoluto:
abs(-4.7)      # Convierte un número negativo en positivo → 4.7

# Raíz cuadrada (dos formas equivalentes):
sqrt(16)       # Raíz cuadrada de 16 → 4
16^(1/2)       # También da 4 (exponente fraccionario)

# Máximo y mínimo:
max(5, 10, 15)     # Valor máximo → 15
max(range)        # Máximo de la secuencia 1:50 → 50
min(5, 10, 15)     # Valor mínimo → 5
min(range)        # Mínimo de 1:50 → 1

# ➤ Suma total de una secuencia:
sum(seq)                  # Suma todos los elementos de 'seq'
sum(seq(2, 20, by = 2))   # Suma de los pares del 2 al 20

# Operaciones aritméticas básicas:
67 - 42       # Resta → 25
67 + 42       # Suma → 109
6 * 4         # Multiplicación → 24
10 / 5        # División → 2

# Medidas de dispersión:
sd(seq)       # Desviación estándar (variabilidad respecto al promedio)
var(seq)      # Varianza (cuadrado de la desviación estándar)

# -----------------------------------------------------------------------------#
# CONDICIONES Y FILTROS EN VECTORES--------------------------------------------
# -----------------------------------------------------------------------------#

# Crear una secuencia de números impares del 1 al 99:
datos <- seq(1, 100, by = 2)

# Operadores lógicos permiten crear condiciones sobre los datos

# Comparación lógica:
datos_1 <- datos < 50     # Devuelve TRUE o FALSE para cada elemento
datos_1                   # Ej: [1] TRUE TRUE TRUE ... FALSE FALSE

# Filtrar elementos que cumplen una condición:
datos_2 <- datos[datos < 50]  # Selecciona solo los valores < 50
datos_2

# Filtrar con múltiples condiciones:
# Selecciona los valores entre 30 (inclusive) y 60 (exclusive)
datos_3 <- datos[datos >= 30 & datos < 60]
datos_3


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


