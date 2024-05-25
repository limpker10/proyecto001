import pandas as pd
from tabulate import tabulate
import psycopg2
from datetime import datetime

# Ruta del archivo Excel
ruta_excel = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS066O5ADAioBZJRARe0SwFAPCjIEWy65W3sqf56ja6gznDkjc6qgUsgykJid_1XCOnbFUUkrsVcdV6/pub?output=xlsx'

def leer_datos_excel(ruta):
    """Lee el archivo Excel y devuelve un DataFrame con las columnas renombradas."""
    df = pd.read_excel(ruta, header=2)
    df.columns = [
        'Numero',
        'fecha_salida',
        'razon_social',
        'RUC',
        'Placa_tracto',
        'Placa_Ramfla',
        'Tipo_de_plataforma',
        'MTC_Dos_placas',
        'Apellidos_y_nombres',
        'Licencia',
        'Celular',
        'Jenrry_Mirio',
        'Serie',
        'Numero_Guia',
        'Cincuenta_soles',
        'Tipo_Mineral',
        'Peso_toneladas'
    ]
    # Convertir la columna 'RUC' a string para evitar notación científica
    df['RUC'] = df['RUC'].apply(lambda x: f'{int(x):011d}' if pd.notnull(x) else x)
    return df

def filtrar_por_fecha(df, fecha_str):
    """Filtra el DataFrame por la fecha de salida proporcionada."""
    fecha_filtro = datetime.strptime(fecha_str, '%Y-%m-%d')
    df_filtrado = df[df['fecha_salida'] == fecha_filtro]
    return df_filtrado

def mostrar_dataframe(df):
    """Muestra el DataFrame utilizando tabulate."""
    columnas_a_mostrar = ['razon_social', 'RUC', 'Serie', 'Numero_Guia']
    print(tabulate(df[columnas_a_mostrar], headers='keys', tablefmt='rounded_outline'))

def insertar_proveedor_si_no_existe(cur, ruc, razon_social):
    """Inserta un proveedor en la tabla Proveedor si no existe."""
    select_query = "SELECT 1 FROM Proveedor WHERE rucp = %s"
    insert_query = """
    INSERT INTO Proveedor (rucp, razon_social) 
    VALUES (%s, %s)
    """
    cur.execute(select_query, (ruc,))
    if not cur.fetchone():
        cur.execute(insert_query, (ruc, razon_social))

def insertar_en_base_de_datos(df, conn_params):
    """Inserta los datos filtrados en la tabla Despacho y verifica/inserta proveedores."""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    for index, row in df.iterrows():
        # Verificar e insertar proveedor si no existe
        insertar_proveedor_si_no_existe(cur, row['RUC'], row['razon_social'])

        # Insertar datos en la tabla Despacho
        insert_query = """
        WITH existing_record AS (
            SELECT 1
            FROM Despacho
            WHERE serie_guia = %s AND numero_guia = %s
        )
        INSERT INTO Despacho (
            fecha_salida, razon_social, ruc, placa_tracto, placa_ramfla, tipo_plataforma, mtc_dos_placas, 
            apellidos_nombres, licencia, celular, serie_guia, numero_guia, tipo_mineral, peso_toneladas,cliente
        )
        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM existing_record)
        """
        cur.execute(insert_query, (
            row['Serie'], row['Numero_Guia'],
            row['fecha_salida'], row['razon_social'], row['RUC'], row['Placa_tracto'], row['Placa_Ramfla'], 
            row['Tipo_de_plataforma'], row['MTC_Dos_placas'], row['Apellidos_y_nombres'], row['Licencia'], 
            row['Celular'], row['Serie'], row['Numero_Guia'], row['Tipo_Mineral'], row['Peso_toneladas'],cliente
        ))

    conn.commit()

    print("╔════════════════════════════════════════════════════════════════════╗")
    print("                 Se ingresaron correctamente los datos                 ")
    print("╚════════════════════════════════════════════════════════════════════╝")

    cur.close()
    conn.close()

def seleccionar_cliente():
    global cliente
    while True:
        cliente = input("Selecciona un cliente (sheco/shogui): ").lower()
        if cliente in ['sheco', 'shogui']:
            return cliente
        else:
            print("Opción inválida. Por favor, selecciona entre 'sheco' y 'shogui'.")

def main():
    global cliente
    # Leer el archivo Excel
    df = leer_datos_excel(ruta_excel)
    
    # Mostrar las primeras filas del DataFrame para verificar que se haya leído correctamente
    # print(df.head())
    
    # Solicitar al usuario una fecha para filtrar
    fecha_input = input("Ingrese una fecha (YYYY-MM-DD) para filtrar: ")
    cliente = seleccionar_cliente()
    # Filtrar el DataFrame por la fecha de salida
    df_filtrado = filtrar_por_fecha(df, fecha_input)
    
    # Mostrar el DataFrame filtrado utilizando tabulate
    mostrar_dataframe(df_filtrado)
    
    # Parámetros de conexión a la base de datos
    conn_params = {
        'dbname': 'SISTRA',
        'user': 'postgres',
        'password': 'postgresadmin',
        'host': 'localhost',
        'port': '5432'
    }
    
    # Insertar los datos filtrados en la base de datos
    insertar_en_base_de_datos(df_filtrado, conn_params)

if __name__ == "__main__":
    main()
