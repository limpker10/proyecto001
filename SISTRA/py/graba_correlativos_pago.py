import psycopg2
from decimal import Decimal
from datetime import date
from tabulate import tabulate

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="SISTRA",
    user="postgres",
    password="postgresadmin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Consulta para obtener los datos de la tabla Despacho para clientes 'sheco'
# Supongamos que tienes la fecha en una variable
fecha_especifica = '2024-08-05'  # Formato YYYY-MM-DD

# Ejecución de la consulta SQL con la fecha específica
query = """
    SELECT razon_social, serie, numero_guia, monto, fecha_salida, ruc
    FROM despacho
    WHERE cliente = 'sheco' AND fecha_salida = %s;
"""

# Ejecutar la consulta con la fecha específica como parámetro
cur.execute(query, (fecha_especifica,))
despachos = cur.fetchall()

# Asegurarse de que hay registros de despachos para clientes 'sheco'
if not despachos:
    raise ValueError("No se encontraron despachos para clientes 'sheco'")

# Preparar datos para la previsualización con detracción del 4% aplicada
datos_previsualizacion = []
total_monto_con_detraccion = Decimal('0.00')
for despacho in despachos:
    razon_social, serie, numero_guia, monto, fecha_salida, ruc = despacho
    if monto is not None:
        monto_con_detraccion = monto * Decimal('0.96')  # Aplicar detracción del 4% usando Decimal
        monto_str = f"{monto:.2f}"
        monto_con_detraccion_str = f"{monto_con_detraccion:.2f}"
        total_monto_con_detraccion += monto_con_detraccion
    else:
        monto_str = "N/A"  # Si el monto es None, mostrar 'N/A'
        monto_con_detraccion_str = "N/A"

    datos_previsualizacion.append([
        razon_social, ruc, serie, numero_guia, fecha_salida, monto_str, monto_con_detraccion_str
    ])

# Mostrar previsualización de los datos en formato de tabla
print("Previsualización de datos con detracción del 4% aplicada:")
print(tabulate(datos_previsualizacion, headers=["Razon Social", "RUC", "Serie", "Numero Guia", "Fecha de Salida", "Monto", "Monto con Detracción"], tablefmt="outline"))

# Imprimir el total del monto con detracción
print("╔════════════════════════════════════════════════════════════════════╗")
print(f" Total del Monto con Detracción: {total_monto_con_detraccion:.2f}  ")
print("╚════════════════════════════════════════════════════════════════════╝")

# Solicitar autorización para proceder
autorizacion = input("¿Desea proceder con la verificación de cuentas bancarias de los proveedores? (s/n): ")

if autorizacion.lower() == 's':
    # Obtener los RUCs de los despachos
    rucs = tuple(despacho[5] for despacho in despachos)

    print("Proveedores sin cuenta bancaria encontrados (RUC):")
    
    query = """
        SELECT rucp, razon_social, celular
        FROM Proveedor
        WHERE cuentabanco IS NULL AND rucp IN %s;
        """
    cur.execute(query, (rucs,))
    proveedores = cur.fetchall()

    if proveedores:
        headers = ["RUC", "Razón Social", "Celular"]

        print(tabulate(proveedores, headers=headers, tablefmt="outline"))
    else:
        print("No se encontraron proveedores sin cuenta bancaria. Pasando a la siguiente acción.")
        

# Cerrar la conexión
cur.close()
conn.close()
