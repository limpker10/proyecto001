import psycopg2
from datetime import datetime

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="SISTRA",
    user="postgres",
    password="postgresadmin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

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
        if len(cadena) <= longitud_maxima:
            return cadena
        else:
            print(f"La entrada no debe exceder {longitud_maxima} caracteres.")

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


    """
    Función para ingresar datos en la base de datos.
    """
    try:
        # Solicitar los datos al usuario
        # serie = validar_cadena("Ingrese la serie: ", 5)
        # numero_guia = validar_cadena("Ingrese el número de guía: ", 10)
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
            INSERT INTO despacho (ser_tra, nro_tra, fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', datos)
        conn.commit()
        print("Datos ingresados correctamente.")
    except Exception as e:
        print("Error al ingresar datos:", e)

def buscar_mostrar_datos(serie, numero_guia):
    """
    Función para buscar y mostrar datos en la base de datos.
    """
    try:
        cursor.execute('SELECT * FROM despacho WHERE serie=%s AND numero_guia=%s', (serie, numero_guia))
        resultado = cursor.fetchone()
        
        if resultado:
            print(" *************************************************** ")
            print("Fecha de transporte:", resultado[3])
            print("Serie de factura:", resultado[4])
            print("Número de factura:", resultado[5])
            print("Fecha de producción:", resultado[6])
            print("Monto:", resultado[7])
            print("Serie de peso:", resultado[8])
            print("Número de peso:", resultado[9])
            print("Fecha de peso:", resultado[10])
            print("Monto de peso:", resultado[11])
            print(" *************************************************** ")
            return True
        else:
            print("No se encontraron datos para la serie y número de guía especificados.")
            return False
    except Exception as e:
        print("Error al buscar datos:", e)
        return False

def actualizar_datos():
    """
    Función para actualizar datos en la base de datos.
    """
    try:
        # Solicitar la serie y el número de guía al usuario
        serie = validar_cadena("Ingrese la serie: ", 5)
        numero_guia = validar_cadena("Ingrese el número de guía: ", 10)
        
        # Verificar si existen datos con la serie y número de guía ingresados
        if buscar_mostrar_datos(serie, numero_guia):
            # Solicitar los nuevos datos al usuario
            fec_tra = solicitar_fecha("Ingrese la nueva fecha de transporte (DD/MM/AAAA): ")
            ser_fac = validar_cadena("Ingrese la nueva serie de la factura: ", 5)
            nro_fac = validar_cadena("Ingrese el nuevo número de la factura: ", 10)
            fec_pro = solicitar_fecha("Ingrese la nueva fecha de producción (DD/MM/AAAA): ")
            monto = validar_flotante("Ingrese el nuevo monto: ")
            ser_peso = validar_cadena("Ingrese la nueva serie del peso: ", 5)
            nro_peso = validar_cadena("Ingrese el nuevo número del peso: ", 10)
            fec_peso = solicitar_fecha("Ingrese la nueva fecha del peso (DD/MM/AAAA): ")
            mon_peso = validar_flotante("Ingrese el nuevo monto del peso: ")

            # Actualizar los datos en la base de datos
            datos = (fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso, serie, numero_guia)
            cursor.execute('''
                UPDATE despacho 
                SET fec_tra=%s, ser_fac=%s, nro_fac=%s, fec_pro=%s, monto=%s, ser_peso=%s, nro_peso=%s, fec_peso=%s, mon_peso=%s
                WHERE serie=%s AND numero_guia=%s
            ''', datos)
            conn.commit()
            print("Datos actualizados correctamente.")
    except Exception as e:
        print("Error al actualizar datos:", e)

# Ejecutar el menú principal
actualizar_datos()

# Cerrar la conexión
conn.close()
