import psycopg2
import csv

# Datos de conexión a la base de datos PostgreSQL
db_params = {
    'dbname': 'tu_base_de_datos',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'port': 5432
}

# Ruta al archivo CSV
csv_file_path = 'C:/sampledb/persons.csv'

# Nombre de la tabla en la base de datos donde se insertarán los datos
table_name = 'persons'

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    print("Conexión a la base de datos establecida exitosamente.")

    # Leer el archivo CSV e insertar los datos en la tabla
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Saltar la cabecera del CSV si existe
        
        for row in csv_reader:
            # Construir la consulta SQL de inserción
            insert_query = f"INSERT INTO {table_name} (first_name, last_name, dob, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, row)

    # Confirmar los cambios
    conn.commit()
    print("Datos insertados exitosamente en la tabla.")

except (Exception as error):
    print(f"Ocurrió un error: {error}")

finally:
    # Cerrar la conexión a la base de datos
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Conexión a la base de datos cerrada.")
