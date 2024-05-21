import xlrd
from xlwt import Workbook
from xlutils.copy import copy

archivo_excel = 'Pagos_a_Proveedores_TBK 09-05-24.xls'
libro = xlrd.open_workbook(archivo_excel, formatting_info=True)
libro_modificable = copy(libro)
hoja = libro_modificable.get_sheet(0)

# Escribir un nuevo valor en una celda específica (por ejemplo, B5)
fila = 7  #  (índice base 0) EQUIVALE EN EXCEL A FILA 8
columna = 6  # columna B (índice base 0) EQUIVALE A COLUMNA 7 
hoja.write(fila, columna, 'rucp Nuevo Valor')
fila = 7  # fila 5 (índice base 0)
columna = 7  # columna B (índice base 0)  EUIVALE A COLUMNAO 8
hoja.write(fila, columna, 'nombre prove')


# Guardar el libro de trabajo modificado
libro_modificable.save(archivo_excel)

print(f"Valor actualizado en la celda B5 del archivo {archivo_excel}")
