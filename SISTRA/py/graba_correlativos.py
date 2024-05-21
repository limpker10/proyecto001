import psycopg2
from datetime import date

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="transporte",
    user="postgres",
    password="postgresadmin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Consulta para obtener los montos y las fechas de transporte de la tabla Despacho para clientes 'sheco'
cur.execute("SELECT monto, fec_tra, ruc FROM Despacho WHERE cliente = 'sheco'")
despachos = cur.fetchall()

# Asegurarse de que hay registros de despachos para clientes 'sheco'
if not despachos:
    raise ValueError("No se encontraron despachos para clientes 'sheco'")

# Mostrar resumen de los datos obtenidos
print("Resumen de datos obtenidos:")
for despacho in despachos:
    print(f"Monto: {despacho[0]}, Fecha de transporte: {despacho[1]}, RUC: {despacho[2]}")

# Cerrar la conexión
cur.close()
conn.close()
