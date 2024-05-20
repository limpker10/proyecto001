import psycopg2
from datetime import datetime
serie=" "    
numero_guia = 0
    
# Conexión a la base de datos
conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="j2929b",
            host="localhost",
            port="5433"
        )
       
cursor = conn.cursor()

# Función para ingresar datos
def ingresar_datos():
    serie = input("Ingrese la serie: ")
    numero_guia = int(input("Ingrese el número de guía: "))
    fec_tra = input("Ingrese la fecha de transporte (YYYY-MM-DD): ")
    fec_tra = datetime.strptime(fec_tra, "%Y-%m-%d").date()
    ser_fac = input("Ingrese la serie de la factura: ")
    nro_fac = input("Ingrese el número de la factura: ")
    fec_pro = input("Ingrese la fecha de producción (YYYY-MM-DD): ")
    fec_pro = datetime.strptime(fec_pro, "%Y-%m-%d").date()
    monto = float(input("Ingrese el monto: "))
    ser_peso = input("Ingrese la serie del peso: ")
    nro_peso = input("Ingrese el número del peso: ")
    fec_peso = input("Ingrese la fecha del peso (YYYY-MM-DD): ")
    fec_peso = datetime.strptime(fec_peso, "%Y-%m-%d").date()
    mon_peso = float(input("Ingrese el monto del peso: "))
    datos = (serie, numero_guia, fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
    cursor.execute('''INSERT INTO Despacho3 (serie, numero_guia, fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', datos)
    conn.commit()
    print("Datos ingresados correctamente.")

# Función para buscar y mostrar datos
def buscar_mostrar_datos():
    global serie,numero_guia

    serie = input("Ingrese la serie: ")
    numero_guia = int(input("Ingrese el número de guía: "))
    cursor.execute('''SELECT * FROM Despacho3 WHERE serie=%s AND numero_guia=%s''', (serie, numero_guia))
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
        ingresar_datos()
        actualizar_datos()

    else:
        print("No se encontraron datos para la serie y número de guía especificados.")

# Función para actualizar datos
def actualizar_datos():
    global serie,numero_guia
    buscar_mostrar_datos():
    #serie = input("Ingrese la serie: ")
    #numero_guia = int(input("Ingrese el número de guía: "))
    #cursor.execute('''SELECT * FROM Despacho3 WHERE serie=%s AND numero_guia=%s''', (serie, numero_guia))
    #resultado = cursor.fetchone()
    
    fec_tra = input("Ingrese la nueva fecha de transporte (YYYY-MM-DD): ")
    fec_tra = datetime.strptime(fec_tra, "%Y-%m-%d").date()
    ser_fac = input("Ingrese la nueva serie de la factura: ")
    nro_fac = input("Ingrese el nuevo número de la factura: ")
    fec_pro = input("Ingrese la nueva fecha de producción (YYYY-MM-DD): ")
    fec_pro = datetime.strptime(fec_pro, "%Y-%m-%d").date()
    monto = float(input("Ingrese el nuevo monto: "))
    ser_peso = input("Ingrese la nueva serie del peso: ")
    nro_peso = input("Ingrese el nuevo número del peso: ")
    fec_peso = input("Ingrese la nueva fecha del peso (YYYY-MM-DD): ")
    fec_peso = datetime.strptime(fec_peso, "%Y-%m-%d").date()
    mon_peso = float(input("Ingrese el nuevo monto del peso: "))
    datos = (fec_tra, ser_fac, nro_fac, fec_pro, monto, ser_peso, nro_peso, fec_peso, mon_peso, serie, numero_guia)
    cursor.execute('''UPDATE Despacho3 
                      SET fec_tra=%s, ser_fac=%s, nro_fac=%s, fec_pro=%s, monto=%s, ser_peso=%s, nro_peso=%s, fec_peso=%s, mon_peso=%s
                      WHERE serie=%s AND numero_guia=%s''', datos)
    conn.commit()
    print("Datos actualizados correctamente.")

# Menú principal
actualizar_datos()

 Cerrar conexión a la base de datos
conn.close()
