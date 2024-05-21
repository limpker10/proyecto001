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
cur.execute("SELECT razon_social, serie, numero_guia, monto, fec_tra, ruc FROM despacho WHERE cliente = 'sheco'")
despachos = cur.fetchall()

# Asegurarse de que hay registros de despachos para clientes 'sheco'
if not despachos:
    raise ValueError("No se encontraron despachos para clientes 'sheco'")

# Preparar datos para la previsualización con detracción del 4% aplicada
datos_previsualizacion = []
total_monto_con_detraccion = Decimal('0.00')
for despacho in despachos:
    razon_social, serie, numero_guia, monto, fec_tra, ruc = despacho
    if monto is not None:
        monto_con_detraccion = monto * Decimal('0.96')  # Aplicar detracción del 4% usando Decimal
        monto_str = f"{monto:.2f}"
        monto_con_detraccion_str = f"{monto_con_detraccion:.2f}"
        total_monto_con_detraccion += monto_con_detraccion
    else:
        monto_str = "N/A"  # Si el monto es None, mostrar 'N/A'
        monto_con_detraccion_str = "N/A"

    datos_previsualizacion.append([
        razon_social, ruc, serie, numero_guia, fec_tra, monto_str,monto_con_detraccion_str 
    ])

# Mostrar previsualización de los datos en formato de tabla
print("Previsualización de datos con detracción del 4% aplicada:")
print(tabulate(datos_previsualizacion, headers=["Razon Social", "RUC", "Serie", "Numero Guia", "Fecha de Transporte","Monto", "Monto con Detracción"], tablefmt="grid"))
# Imprimir el total del monto con detracción
print(f"\nTotal del Monto con Detracción: {total_monto_con_detraccion:.2f}")
# Solicitar autorización para proceder
autorizacion = input("¿Desea proceder con la verificación de cuentas bancarias de los proveedores? (s/n): ")

if autorizacion.lower() == 's':
    # Obtener los RUCs de los despachos
    rucs = tuple(despacho[5] for despacho in despachos)

    # Consulta para verificar que todos los proveedores tengan cuenta bancaria
    cur.execute("SELECT ruc, banco FROM Proveedor WHERE ruc IN %s", (rucs,))
    proveedores = cur.fetchall()

    # Crear un diccionario para mapear RUC a banco
    ruc_to_banco = {proveedor[0]: proveedor[1] for proveedor in proveedores}

    # Verificar si hay proveedores sin cuenta bancaria
    proveedores_sin_cuenta = [proveedor[0] for proveedor in proveedores if not proveedor[1]]
    if proveedores_sin_cuenta:
        print("Proveedores sin cuenta bancaria encontrados (RUC):")
        for ruc in proveedores_sin_cuenta:
            print(ruc)
    else:
        print("Todos los proveedores tienen cuenta bancaria.")

# Cerrar la conexión
cur.close()
conn.close()
