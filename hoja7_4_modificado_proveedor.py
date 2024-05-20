import pandas as pd
import re
import datetime
import psycopg2
from psycopg2 import sql

# Variables globales
fecha_str = ""
cliente = ""
fecha = datetime.date.today()

# Función para ingresar y validar una fecha
def ingresar_fecha():
    global fecha_str
    while True:
        fecha_str = input("Ingresa una fecha en formato dd/mm/yyyy: ")
        print("Fecha ingresada:", fecha_str)
        try:
            # Validar si la fecha tiene el formato correcto
            fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto. Por favor, ingresa la fecha en formato dd/mm/yyyy.")

# Función para seleccionar un cliente entre 'sheco' y 'shogui'
def seleccionar_cliente():
    global cliente
    while True:
        cliente = input("Selecciona un cliente (sheco/shogui): ").lower()
        if cliente in ['sheco', 'shogui']:
            return cliente
        else:
            print("Opción inválida. Por favor, selecciona entre 'sheco' y 'shogui'.")

# Función para verificar la conexión a la base de datos
def verificar_conexion():
    try:
        conexion = psycopg2.connect(
            dbname="transporte",
            user="postgres",
            password="postgresadmin",
            host="localhost",
            port="5432"
        )
        conexion.close()
        return True
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return False

# Función para verificar la existencia de la base de datos
def verificar_bd(conexion, nombre_bd):
    with conexion.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nombre_bd,))
        existe = cursor.fetchone()
    return existe is not None

# Función para verificar la existencia de una tabla
def verificar_tabla(conexion, nombre_tabla):
    with conexion.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name=%s)", (nombre_tabla,))
        existe = cursor.fetchone()[0]
    return existe


# Función para verificar la existencia de un proveedor
def verificar_proveedor(conexion, ruc):
    with conexion.cursor() as cursor:
        cursor.execute("SELECT 1 FROM Proveedor WHERE ruc = %s", (ruc,))
        existe = cursor.fetchone()
    return existe is not None

# Función para grabar una fila en la base de datos PostgreSQL
def grabarpos(fila):
    if not verificar_conexion():
        return

    try:
        with psycopg2.connect(
            dbname="transporte",
            user="postgres",
            password="postgresadmin",
            host="localhost",
            port="5432"
        ) as conexion:
            if not verificar_bd(conexion, "transporte"):
                print("La base de datos 'transporte' no existe.")
                return
            
            if not verificar_tabla(conexion, "despacho"):
                print("La tabla 'despacho' no existe.")
                return

            with conexion.cursor() as cursor:
                
                ruc = fila[2]
                if not verificar_proveedor(conexion, ruc):
                    proveedor = (fila[1], ruc, fila[9])
                    cursor.execute("""
                        INSERT INTO proveedor (razon_social, ruc, celular)
                        VALUES (%s, %s, %s)
                    """, proveedor)
                    print("proveedor creado")

                conexion.commit()

            with conexion.cursor() as cursor:
                # Convertir el valor de cincuenta_soles a booleano
                if pd.isna(fila[13]):  # Si el valor es NaN, convertir a False
                    fila[13] = False
                else:
                    fila[13] = bool(fila[13])  # Convertir a booleano
                
                 # Agregar el cliente al final de la fila
                fila.append(cliente)

                insert_query = """
                INSERT INTO despacho3 (
                    fecha_salida, razon_social, ruc, placa_tracto, placa_ramfla,
                    tipo_plataforma, mtc_dos_placas, apellidos_nombres, licencia, celular, usuario, serie, numero_guia, cincuenta_soles, tipo_mineral, cliente
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, fila)
                conexion.commit()
    except Exception as e:
        print("Error al conectar o insertar en la base de datos:", e)

# Función para leer y procesar las filas de la hoja de Excel
def leerHoja(num_filas, num_columnas, datos_hoja):
    global fecha_str
    print("Iterando sobre todas las filas y columnas:")
    for i in range(num_filas):
        fila = datos_hoja.iloc[i, 1:16].values.tolist()
        cvalor = fila[0].strftime("%d/%m/%Y") if isinstance(fila[0], datetime.datetime) else fila[0]
        if cvalor == fecha_str:
            print(fila)
            grabarpos(fila)

# Función para leer el archivo Excel y la hoja específica
def leerExcel(nhoja):
    url_excel = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0je619Hmb2K6G9ExAL4H1oLo-IL_HAS9l0uB__zIv6Jq0aoEtMxtjJXjwEPvtnJvs5vvjM2-L5Ka4/pub?output=xlsx"
    hojas_excel = pd.read_excel(url_excel, sheet_name=None)
    for nombre_hoja, datos_hoja in hojas_excel.items():
        if nombre_hoja == nhoja:
            num_filas, num_columnas = datos_hoja.shape
            leerHoja(num_filas, num_columnas, datos_hoja)

# Main
def main():
    global fecha_str, fecha, cliente
    fecha = ingresar_fecha()
    cliente = seleccionar_cliente()
    fecha_str = fecha.strftime('%d/%m/%Y')
    print(f"Fecha ingresada: {fecha_str}")
    print(f"Cliente seleccionado: {cliente}")

if __name__ == "__main__":
    main()
    leerExcel("Registro")
