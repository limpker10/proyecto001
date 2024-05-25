import psycopg2
from datetime import datetime
from tabulate import tabulate
import os

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="SISTRA",
    user="postgres",
    password="postgresadmin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def limpiar_consola():
    """
    Limpia la consola según el sistema operativo.
    """
    if os.name == 'nt':
        os.system('cls')  # Comando para Windows
    else:
        os.system('clear')  # Comando para Unix/Linux/MacOS

def solicitar_fecha(mensaje):
    """
    Solicita una fecha al usuario y verifica que sea válida en formato DD/MM/AAAA.
    """
    while True:
        fecha_str = input(mensaje)
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto. Por favor, use el formato DD/MM/AAAA.")

def validar_cadena(mensaje, longitud_maxima):
    """
    Solicita una cadena al usuario y verifica que no exceda la longitud máxima.
    """
    while True:
        cadena = input(mensaje).strip()
        if 0 < len(cadena) <= longitud_maxima:
            return cadena
        else:
            print(f"La entrada no debe estar vacía y no debe exceder {longitud_maxima} caracteres.")

def validar_entero(mensaje):
    """
    Solicita un número entero al usuario y verifica que sea válido.
    """
    while True:
        try:
            numero = int(input(mensaje))
            return numero
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

def validar_flotante(mensaje):
    """
    Solicita un número flotante al usuario y verifica que sea válido.
    """
    while True:
        try:
            numero = float(input(mensaje))
            return numero
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número válido.")

def ingresar_datos():
    """
    Función para ingresar datos en la base de datos.
    """
    try:
        # Solicitar los datos al usuario
        fec_tra = solicitar_fecha("Ingrese la fecha de transporte (DD/MM/AAAA): ")
        ser_fac = validar_cadena("Ingrese la serie de la factura: ", 5)
        nro_fac = validar_cadena("Ingrese el número de la factura: ", 10)
        fec_pro = solicitar_fecha("Ingrese la fecha de producción (DD/MM/AAAA): ")
        monto = validar_flotante("Ingrese el monto: ")
        ser_peso = validar_cadena("Ingrese la serie del peso: ", 5)
        nro_peso = validar_cadena("Ingrese el número del peso: ", 10)
        fec_peso = solicitar_fecha("Ingrese la fecha del peso (DD/MM/AAAA): ")
        mon_peso = validar_flotante("Ingrese el monto del peso: ")

        # Insertar los datos en la base de datos
        datos = (fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
        cursor.execute('''
            INSERT INTO despacho (fecha_transporte, serie_factura, numero_factura, fecha_produccion, monto_factura, serie_peso, numero_peso, fecha_peso, monto_peso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', datos)
        conn.commit()
        print("Datos ingresados correctamente.")
    except Exception as e:
        print("Error al ingresar datos:", e)

def buscar_mostrar_datos(serie, numero_guia):
    """
    Función para buscar y mostrar todos los campos, incluyendo los vacíos o nulos, en la base de datos.
    """
    try:
        cursor.execute('SELECT * FROM despacho WHERE serie_guia=%s AND numero_guia=%s', (serie, numero_guia))
        resultado = cursor.fetchone()
        
        if resultado:
            # Convertir la tupla resultado a una lista
            resultado = list(resultado)
            
            # Obtener nombres de columnas desde la base de datos
            column_names = [desc[0] for desc in cursor.description]
            
            headers = ["Campo", "Valor"]
            data = []

            # Agregar todos los campos y sus valores a la tabla
            for campo, valor in zip(column_names, resultado):
                if valor is None or valor == '':
                    data.append([campo, "Vacío"])
                else:
                    data.append([campo, valor])

            print(tabulate(data, headers=headers, tablefmt="rounded_outline"))
            
            # Preguntar si se requiere modificación
            modificar = input("¿Desea modificar algún campo? (s/n): ").strip().lower()

            if modificar == 'n':
                limpiar_consola()
                return

            if modificar == 's':
                # Iterar sobre los campos vacíos y permitir edición
                for i, (campo, valor) in enumerate(zip(column_names, resultado)):
                    if valor is None or valor == 'Vacío':
                        ayuda = mostrar_ayuda(campo)
                        nuevo_valor = input(f"El campo '{campo}' está vacío. Ingrese un nuevo valor ({ayuda}): ").strip()
                        if nuevo_valor:  # Verificar que no sea una cadena vacía
                            resultado[i] = nuevo_valor
                            # Actualizar la base de datos con el nuevo valor
                            cursor.execute(f'UPDATE despacho SET {campo}=%s WHERE serie_guia=%s AND numero_guia=%s', (nuevo_valor, serie, numero_guia))
                            conn.commit()
                            print(f"El campo '{campo}' ha sido actualizado a '{nuevo_valor}'")
                            
            print("Todos los campos vacíos han sido actualizados.")

        else:
            print("No se encontraron datos para la serie y número de guía especificados.")
            return
        
    except Exception as e:
        print("Error al buscar datos:", e)
        return

def actualizar_datos(serie, numero_guia):
    """
    Función para actualizar datos específicos en la base de datos.
    """
    try:
        # Solicitar al usuario el campo que desea modificar
        campo = validar_cadena("Ingrese el nombre del campo que desea modificar: ", 50)
        nuevo_valor = input(f"Ingrese el nuevo valor para el campo '{campo}': ").strip()
        
        # Actualizar el campo en la base de datos
        cursor.execute(f'UPDATE despacho SET {campo}=%s WHERE serie_guia=%s AND numero_guia=%s', (nuevo_valor, serie, numero_guia))
        conn.commit()
        print(f"El campo '{campo}' ha sido actualizado correctamente a '{nuevo_valor}'.")
        
    except Exception as e:
        print("Error al actualizar datos:", e)

def mostrar_ayuda(campo):
    """
    Muestra ayuda sobre el formato y los límites de los valores para un campo específico.
    """
    ayuda = {
        "fecha_salida": "Formato: DD/MM/AAAA",
        "razon_social": "Máximo 75 caracteres",
        "ruc": "11 dígitos",
        "placa_tracto": "Máximo 10 caracteres",
        "placa_ramfla": "Máximo 10 caracteres",
        "tipo_plataforma": "Máximo 12 caracteres",
        "mtc_dos_placas": "Máximo 25 caracteres",
        "apellidos_nombres": "Máximo 100 caracteres",
        "licencia": "Máximo 20 caracteres",
        "celular": "9 dígitos",
        "usuario": "Máximo 20 caracteres",
        "serie_guia": "Máximo 5 caracteres",
        "numero_guia": "Número entero",
        "cincuenta_soles": "TRUE o FALSE",
        "tipo_mineral": "Máximo 12 caracteres",
        "peso_toneladas": "Hasta 10 dígitos, 2 decimales",
        "monto_adelanto": "Hasta 10 dígitos, 2 decimales",
        "cliente": "Máximo 10 caracteres",
        "fecha_entrega": "Formato: DD/MM/AAAA",
        "serie_transporte": "Máximo 5 caracteres",
        "numero_transporte": "Máximo 10 caracteres",
        "fecha_transporte": "Formato: DD/MM/AAAA",
        "serie_factura": "Máximo 5 caracteres",
        "numero_factura": "Máximo 10 caracteres",
        "fecha_factura": "Formato: DD/MM/AAAA",
        "monto_factura": "Hasta 10 dígitos, 2 decimales",
        "serie_peso": "Máximo 5 caracteres",
        "numero_peso": "Máximo 10 caracteres",
        "fecha_peso": "Formato: DD/MM/AAAA",
        "monto_peso": "Hasta 10 dígitos, 2 decimales",
        "fecha_pago": "Formato: DD/MM/AAAA",
        "codigo_correlativo": "Máximo 30 caracteres",
        "fecha_detra": "Formato: DD/MM/AAAA",
        "correlativo_detra": "Hasta 10 dígitos"
    }
    return ayuda.get(campo, "No se ha definido un formato para este campo")

def main():
    """
    Función principal del programa.
    """
    while True:
        print("\nOpciones:")
        print("1. Buscar y mostrar datos")
        print("2. Salir")
        
        opcion = validar_entero("Seleccione una opción: ")
        
        if opcion == 1:
            serie = validar_cadena("Ingrese la serie: ", 5)
            numero_guia = validar_cadena("Ingrese el número de guía: ", 10)
            buscar_mostrar_datos(serie, numero_guia)
        elif opcion == 2:
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

    # Cerrar la conexión
    cursor.close()
    conn.close()

# Ejecutar el programa
if __name__ == "__main__":
    main()
