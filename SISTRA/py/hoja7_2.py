import pandas as pd
import re
from datetime import datetime
import os

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
    global filtradas_fecha
    
    # Obtener los títulos de la fila 3 (índice 2)
    titulos = datos_hoja.iloc[1]
    
    for i in range(num_filas):
        for j in range(num_columnas):
            valor = datos_hoja.iloc[i, j]  # Obtener el valor de la celda actual
            cvalor = str(valor) if isinstance(valor, str) else ""
            
            # Validar si el valor es una fecha según el patrón o si es de tipo datetime
            if isinstance(valor, pd.Timestamp) or pattern.match(cvalor):
                if (isinstance(valor, pd.Timestamp) and valor.strftime('%d/%m/%Y') == fecha_a_buscar) or cvalor == fecha_a_buscar:
                    # Agregar la fila al DataFrame filtrado si la fecha coincide con la fecha a buscar
                    filtradas_fecha = pd.concat([filtradas_fecha, datos_hoja.iloc[[i]]], ignore_index=True)

def leerExcel(nhoja):
    for nombre_hoja, datos_hoja in hojas_excel.items():
        if nombre_hoja == nhoja:
            # Obtener la cantidad de filas y columnas de la hoja
            num_filas, num_columnas = datos_hoja.shape
            leerHoja(num_filas, num_columnas, datos_hoja)

# Llamada a la función para leer la hoja específica "Registro"
leerExcel("Registro")

# Nombre del archivo a guardar
nombre_archivo = f"fechas_filtradas_{fecha_a_buscar.replace('/', '-')}.xlsx"

# Verificar si el archivo ya existe y eliminarlo si es necesario
if os.path.exists(nombre_archivo):
    os.remove(nombre_archivo)

# Guardar el DataFrame filtrado en un archivo Excel
filtradas_fecha.to_excel(nombre_archivo, index=False)

print(f"Archivo '{nombre_archivo}' creado con las filas que contienen la fecha especificada.")
