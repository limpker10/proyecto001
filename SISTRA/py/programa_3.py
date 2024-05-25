import psycopg2
from decimal import Decimal
from datetime import date
from tabulate import tabulate
import datetime
import os
import pandas as pd
import subprocess

from xlutils.copy import copy

def obtener_conexion_bd():
    """Establece y retorna la conexión a la base de datos."""
    try:
        return psycopg2.connect(
            dbname="SISTRA",
            user="postgres",
            password="postgresadmin",
            host="localhost",
            port="5432"
        )
    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        exit(1)

def validar_fecha(fecha_str):
    """Valida que la fecha tenga el formato YYYY-MM-DD."""
    try:
        return date.fromisoformat(fecha_str)
    except ValueError:
        raise ValueError("La fecha ingresada no tiene el formato correcto. Por favor, use el formato YYYY-MM-DD.")

def obtener_despachos(cur, fecha):
    """Obtiene los datos de despachos para un cliente específico en una fecha dada."""
    query = """
        SELECT razon_social, serie_guia, numero_guia, monto_factura, fecha_salida, ruc
        FROM despacho
        WHERE cliente = 'sheco' AND fecha_salida = %s;
    """
    cur.execute(query, (fecha,))
    return cur.fetchall()

def preparar_datos_previsualizacion(despachos):
    """Prepara los datos para la previsualización, aplicando una detracción del 4%."""
    datos_previsualizacion = []
    total_monto_con_detraccion = Decimal('0.00')

    for despacho in despachos:
        razon_social, serie, numero_guia, monto, fecha_salida, ruc = despacho
        if monto is not None:
            detraccion = monto * Decimal('0.04')  # Calcular detracción del 4%
            monto_con_detraccion = monto * Decimal('0.96')  # Aplicar detracción del 4%
            monto_str = f"{monto:.2f}"
            detraccion_str = f"{detraccion:.2f}"
            monto_con_detraccion_str = f"{monto_con_detraccion:.2f}"
            total_monto_con_detraccion += monto_con_detraccion
        else:
            monto_str = "N/A"  # Si el monto es None, mostrar 'N/A'
            detraccion_str = "N/A"
            monto_con_detraccion_str = "N/A"

        datos_previsualizacion.append([
            razon_social, ruc, serie, numero_guia, fecha_salida, monto_str, detraccion_str, monto_con_detraccion_str
        ])

    return datos_previsualizacion, total_monto_con_detraccion

def mostrar_previsualizacion(datos_previsualizacion, total_monto_con_detraccion):
    """Muestra la previsualización de los datos en formato de tabla."""
    print("Previsualización de datos con detracción del 4% aplicada:")
    print(tabulate(datos_previsualizacion, headers=["Razon Social", "RUC", "Serie", "Numero Guia", "Fecha de Salida", "Monto", "Detracción", "Monto con Detracción"], tablefmt="rounded_outline"))
    print("╔════════════════════════════════════════════════════════════════════╗")
    print(f" Total del Monto con Detracción: {total_monto_con_detraccion:.2f}  ")
    print("╚════════════════════════════════════════════════════════════════════╝")

def verificar_cuentas_bancarias(cur, rucs,total_monto_con_detraccion):
    """Verifica las cuentas bancarias de los proveedores y muestra los que no tienen cuenta."""
    query = """
        SELECT rucp, razon_social, celular
        FROM Proveedor
        WHERE cuentabanco IS NULL AND rucp IN %s;
    """
    cur.execute(query, (rucs,))
    proveedores = cur.fetchall()

    if proveedores:
        headers = ["RUC", "Razón Social", "Celular"]
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("         Proveedores sin cuenta bancaria encontrados :                ")
        print("         Ponerse en contacto o llenar la cuenta bancaria              ")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(tabulate(proveedores, headers=headers, tablefmt="rounded_outline"))
        

        # Bucle para editar proveedores hasta que el usuario decida terminar
        while True:
            continuar = input("¿Desea modificar algún proveedor? (s/n): ").lower()
            if continuar != 's':
                break
            editar_proveedor(cur, proveedores)

    else:
        print("No se encontraron proveedores sin cuenta bancaria. Pasando a la siguiente acción.")
        llenar_db_correlativos_pago_y_actualizar_despacho(cur, rucs,total_monto_con_detraccion)
        return True
    
    return False

def editar_proveedor(cur, proveedores):
    # Mostrar lista de proveedores 
    print("Seleccione el proveedor a modificar:")
    headers = ["#", "RUC", "Razón Social", "Celular"]
    proveedores_con_indices = [(i+1, proveedor[0], proveedor[1], proveedor[2]) for i, proveedor in enumerate(proveedores)]
    print(tabulate(proveedores_con_indices, headers=headers, tablefmt="rounded_outline"))

    # Solicitar selección de proveedor
    proveedor_seleccionado = int(input("Número de opción: ")) - 1
    proveedor_id = proveedores[proveedor_seleccionado][0]

    # Obtener los datos actuales del proveedor
    print("Selecciona el tipo de cuenta:")
    opciones_tipo_cuenta = [
        "CTA. CORRIENTE SOLES SCOTIABANK",
        "CTA. INTERBANCARIA SOLES"
    ]
    for i, opcion in enumerate(opciones_tipo_cuenta, start=1):
        print(f"{i}. {opcion}")

    # Solicitar tipo de cuenta seleccionado
    tipo_cuenta_seleccionada = int(input("Número de opción: "))
    nuevo_tipo_cuenta = opciones_tipo_cuenta[tipo_cuenta_seleccionada - 1]

    # Solicitar nueva cuenta bancaria según tipo de cuenta seleccionado
    nueva_cuenta_banco = " "
    nueva_cuenta_inter = " "

    if nuevo_tipo_cuenta == "CTA. CORRIENTE SOLES SCOTIABANK":
        nueva_cuenta_banco = input("Nueva cuenta banco: ")
    elif nuevo_tipo_cuenta == "CTA. INTERBANCARIA SOLES":
        nueva_cuenta_inter = input("Nueva cuenta interbancaria: ")

    # Mostrar previsualización de los cambios
    proveedor_previsualizado = [
        nuevo_tipo_cuenta,    # tipocuenta
        nueva_cuenta_banco,   # cuentabanco
        nueva_cuenta_inter    # cuentainter
    ]
    print("Previsualización de los cambios:")
    print(tabulate([proveedor_previsualizado], headers=["Tipo Cuenta", "Cuenta Banco", "Cuenta Interbancaria"], tablefmt="rounded_outline"))
    # Confirmar actualización
    confirmacion = input("¿Desea actualizar este proveedor con los nuevos datos? (s/n): ").lower()
    if confirmacion == 's':
        # Actualizar datos del proveedor en la base de datos
        cur.execute("""
            UPDATE Proveedor
            SET tipocuenta = %s, cuentabanco = %s, cuentainter = %s
            WHERE rucp = %s
        """, (nuevo_tipo_cuenta, nueva_cuenta_banco, nueva_cuenta_inter, proveedor_id))
        cur.connection.commit()
        print("Proveedor actualizado exitosamente.")
        
    else:
        print("Actualización cancelada.")


def generar_excel_pagos(cur, datos_previsualizacion):
    """
    Llena una tabla de correlativos de pago y actualiza la información de despacho en un archivo Excel.

    :param cur: Cursor de la base de datos para ejecutar consultas.
    :param datos_previsualizacion: Datos de previsualización que contienen información de los proveedores.
    """
    # Definir consulta para obtener información de proveedores
    select_query_proveedor = """
        SELECT tipocuenta AS "FORMA DE PAGO", 
               cuentabanco AS "CUENTA SCOTIABANK", 
               cuentainter AS "CUENTA INTERBANCARIA",  
               correo AS "CORREO ELECTRÓNICO"
        FROM Proveedor
        WHERE rucp = %s;
    """
    
    # Lista para almacenar nuevos datos a agregar al DataFrame
    datos = []

    # Iterar sobre los datos de previsualización para completar el DataFrame
    for datos_prev in datos_previsualizacion:
        ruc_proveedor = datos_prev[1]
        
        # Ejecutar la consulta de selección para cada proveedor
        cur.execute(select_query_proveedor, (ruc_proveedor,))
        result = cur.fetchone()
        print("Resultado de la consulta para el proveedor:", result)
        
        if result:
            # Convertir explícitamente los valores a texto
            cuenta_scotiabank = str(result[1])
            cuenta_interbancaria = str(result[2])
            
            # Agregar los datos a la lista de nuevos datos
            datos.append({
                " ": " ",
                'RUC DEL PROVEEDOR': ruc_proveedor,
                'RAZÓN SOCIAL': datos_prev[0],  # Suponiendo que este índice es correcto para RAZÓN SOCIAL
                'FORMA DE PAGO': result[0],
                'IMPORTE': datos_prev[7],  # Suponiendo que este índice es correcto para IMPORTE
                'CUENTA SCOTIABANK': cuenta_scotiabank,
                'CUENTA INTERBANCARIA': cuenta_interbancaria,
                'PAGO ÚNICO / SINGLE PAY': " ",
                'TIPO DE DOCUMENTO DE PAGO': "FACTURA",
                'N° DOCUMENTO': " ",
                'FECHA EMISIÓN DOCUMENTO': " ",
                'CORREO ELECTRÓNICO': result[3],
                'ERRORES Y DUPLICADOS': " "
            })

   
    # Obtener la fecha actual en formato YYYY-MM-DD
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    source_file_path = "E:\\EPIS_UNSA\\PROYECTO\\tutorial-env\\proyecto\\SISTRA\\molde\\Pagos_a_Proveedores_TBK.xls"
    destination_file_path = f"E:\\EPIS_UNSA\\PROYECTO\\tutorial-env\\proyecto\\SISTRA\\pagos\\Pagos_a_Proveedores_TBK_{current_date}.xls"
    
    # Convertir la lista de diccionarios a una cadena de texto en formato CSV
    data_string = ";".join([",".join(map(str, row.values())) for row in datos])

    # Ejecutar el programa Java con los argumentos
    jar_path = "ExcelEditor.jar"
    subprocess.run(["java", "-jar", jar_path, source_file_path, destination_file_path, data_string])

    print(f"Archivo guardado en {destination_file_path}")  # Confirmar la ubicación donde se guardó el archivo

    


def llenar_db_correlativos_pago_y_actualizar_despacho(cur, rucs, total_monto_con_detraccion):
    # Generar datos simulados para correlativos_pago
    print(rucs)
    datos = []
    correlativos_generados = []

    for ruc in rucs:
        fecha_pago = datetime.date.today()
        monto = total_monto_con_detraccion  # Monto simulado
        documento_banco = "N/A"  # Documento simulado usando los últimos 4 dígitos del RUC
        nro_documentos = 1  # Número de documentos simulado
        tipo_pago = "FACTURA"  # Tipo de pago simulado
        estado = 'P'  # Estado simulado

        datos.append((fecha_pago, monto, documento_banco, nro_documentos, tipo_pago, estado))

    # Insertar datos en la tabla correlativos_pago y obtener los códigos correlativos generados
    query_insert = """
    INSERT INTO correlativos_pago (fecha_pago, monto, documento_banco, nro_documentos, tipo_pago, estado)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING codigo_correlativo;
    """
    for data in datos:
        cur.execute(query_insert, data)
        codigo_correlativo = cur.fetchone()[0]
        correlativos_generados.append(codigo_correlativo)

    cur.connection.commit()

    # Actualizar la tabla despacho con los códigos correlativos generados
    query_update = """
    UPDATE despacho
    SET codigo_correlativo = %s
    WHERE ruc = %s;
    """
    for ruc, codigo_correlativo in zip(rucs, correlativos_generados):
        cur.execute(query_update, (codigo_correlativo, ruc))

    cur.connection.commit()
    print("Datos insertados en la tabla 'correlativos_pago' y actualizados en la tabla 'despacho' exitosamente.")



def main():
    # Establecer conexión a la base de datos
    conn = obtener_conexion_bd()
    cur = conn.cursor()
    generar_correlativo_pago = False;
    try:
        # Solicitar al usuario que ingrese la fecha específica
        fecha_especifica = input("Ingrese la fecha específica (formato YYYY-MM-DD): ")
        validar_fecha(fecha_especifica)

        # Obtener datos de despachos
        despachos = obtener_despachos(cur, fecha_especifica)

        # Asegurarse de que hay registros de despachos para clientes 'sheco'
        if not despachos:
            raise ValueError("No se encontraron despachos para clientes 'sheco'") 

        # Preparar datos para la previsualización
        datos_previsualizacion, total_monto_con_detraccion = preparar_datos_previsualizacion(despachos)

        # Mostrar previsualización de los datos
        mostrar_previsualizacion(datos_previsualizacion, total_monto_con_detraccion)

        # Solicitar autorización para proceder
        autorizacion = input("¿Desea proceder con la verificación de cuentas bancarias de los proveedores? (s/n): ")

        if autorizacion.lower() == 's':
            # Obtener los RUCs de los despachos
            rucs = tuple(despacho[5] for despacho in despachos)
            generar_correlativo_pago = verificar_cuentas_bancarias(cur, rucs,total_monto_con_detraccion)
        
        if generar_correlativo_pago:
            generar_excel_pagos(cur,datos_previsualizacion)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
