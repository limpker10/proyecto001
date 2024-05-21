import psycopg2
from datetime import datetime

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="transporte",
    user="postgres",
    password="postgresadmin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def solicitar_fecha(mensaje):
    """
    Solicita una fecha al usuario y verifica que sea válida.
    """
    while True:
        fecha_str = input(mensaje)
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto. Por favor, use el formato YYYY-MM-DD.")

def ingresar_datos():
    """
    Función para ingresar datos en la base de datos.
    """
    try:
        # Solicitar los datos al usuario
        serie = input("Ingrese la serie: ")
        numero_guia = int(input("Ingrese el número de guía: "))
        fec_tra = solicitar_fecha("Ingrese la fecha de transporte (YYYY-MM-DD): ")
        ser_fac = input("Ingrese la serie de la factura: ")
        nro_fac = input("Ingrese el número de la factura: ")
        fec_pro = solicitar_fecha("Ingrese la fecha de producción (YYYY-MM-DD): ")
        monto = float(input("Ingrese el monto: "))
        ser_peso = input("Ingrese la serie del peso: ")
        nro_peso = input("Ingrese el número del peso: ")
        fec_peso = solicitar_fecha("Ingrese la fecha del peso (YYYY-MM-DD): ")
        mon_peso = float(input("Ingrese el monto del peso: "))

        # Insertar los datos en la base de datos
        datos = (serie, numero_guia, fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
        cursor.execute('''
            INSERT INTO Despacho3 (serie, numero_guia, fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        cursor.execute('SELECT * FROM Despacho3 WHERE serie=%s AND numero_guia=%s', (serie, numero_guia))
        resultado = cursor.fetchone()
        
        if resultado:
            print("Fecha de salida:", resultado[2])
            print("Razón social:", resultado[3])
            print("RUC:", resultado[4])
            print("Placa de tracto:", resultado[5])
            print("Placa de ramfla:", resultado[6])
            print("Tipo de plataforma:", resultado[7])
            print("MTC dos placas:", resultado[8])
            print("Apellidos y nombres:", resultado[9])
            print("Licencia:", resultado[10])
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
        serie = input("Ingrese la serie: ")
        numero_guia = input("Ingrese el número de guía: ")
        
        # Verificar si existen datos con la serie y número de guía ingresados
        if buscar_mostrar_datos(serie, numero_guia):
            # Solicitar los nuevos datos al usuario
            fec_tra = solicitar_fecha("Ingrese la nueva fecha de transporte (YYYY-MM-DD): ")
            ser_fac = input("Ingrese la nueva serie de la factura: ")
            nro_fac = input("Ingrese el nuevo número de la factura: ")
            fec_pro = solicitar_fecha("Ingrese la nueva fecha de producción (YYYY-MM-DD): ")
            monto = float(input("Ingrese el nuevo monto: "))
            ser_peso = input("Ingrese la nueva serie del peso: ")
            nro_peso = input("Ingrese el nuevo número del peso: ")
            fec_peso = solicitar_fecha("Ingrese la nueva fecha del peso (YYYY-MM-DD): ")
            mon_peso = float(input("Ingrese el nuevo monto del peso: "))

            # Actualizar los datos en la base de datos
            datos = (fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso, serie, numero_guia)
            cursor.execute('''
                UPDATE Despacho3 
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
