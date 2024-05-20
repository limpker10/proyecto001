import pandas as pd
import re
from datetime import datetime

# URL del archivo Excel en Google Sheets
url_excel = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0je619Hmb2K6G9ExAL4H1oLo-IL_HAS9l0uB__zIv6Jq0aoEtMxtjJXjwEPvtnJvs5vvjM2-L5Ka4/pub?output=xlsx"

# Leer todas las hojas del archivo Excel desde la URL
hojas_excel = pd.read_excel(url_excel, sheet_name=None)

# Expresión regular para validar el formato de fecha dd/mm/yyyy
pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')

# Fecha a buscar
fecha_a_buscar = "13/05/2024"

# DataFrame para almacenar las filas filtradas
filtradas_fecha = pd.DataFrame()

def leerHoja(num_filas, num_columnas, datos_hoja):
    """
    Función para iterar sobre todas las filas y columnas de una hoja de Excel y
    filtrar las filas que contienen la fecha especificada.

    Args:
    num_filas (int): Número de filas en la hoja.
    num_columnas (int): Número de columnas en la hoja.
    datos_hoja (DataFrame): Datos de la hoja en forma de DataFrame.
    """
    global filtradas_fecha
    for i in range(num_filas):
        for j in range(num_columnas):
            valor = datos_hoja.iloc[i, j]  # Obtener el valor de la celda actual
            cvalor = "jjjiiii"
            if isinstance(valor, str):
                cvalor = valor

            # Validar si el valor es una fecha según el patrón o si es de tipo datetime
            if isinstance(valor, pd.Timestamp) or pattern.match(cvalor):
                if (isinstance(valor, pd.Timestamp) and valor.strftime('%d/%m/%Y') == fecha_a_buscar) or cvalor == fecha_a_buscar:
                    # Agregar la fila al DataFrame filtrado si la fecha coincide con la fecha a buscar
                    filtradas_fecha = pd.concat([filtradas_fecha, datos_hoja.iloc[[i]]], ignore_index=True)

def leerExcel(nhoja):
    """
    Función para iterar sobre cada hoja del archivo Excel y, si el nombre de la hoja
    coincide con el proporcionado, leer sus datos.

    Args:
    nhoja (str): Nombre de la hoja a buscar y leer.
    """
    for nombre_hoja, datos_hoja in hojas_excel.items():
        if nombre_hoja == nhoja:
            # Obtener la cantidad de filas y columnas de la hoja
            num_filas, num_columnas = datos_hoja.shape
            leerHoja(num_filas, num_columnas, datos_hoja)

# Llamada a la función para leer la hoja específica "Registro"
leerExcel("Registro")

# Guardar el DataFrame filtrado en un archivo Excel
filtradas_fecha.to_excel("fechas_filtradas_fecha.xlsx", index=False)

print("Archivo 'fechas_filtradas_fecha.xlsx' creado con las filas que contienen la fecha especificada.")
