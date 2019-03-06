#!/usr/bin/env python3
import sys
from xlrd import open_workbook

class movement(object):
    fechavalor = None
    categoria = None
    subcategoria = None
    descripcion = None
    comentario = None
    imagen = None
    importe = None
    saldo = None
    
    def __init__(self,fechavalor,categoria,subcategoria,descripcion,comentario,imagen,importe,saldo):
        self.fechavalor = fechavalor
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.descripcion = descripcion
        self.comentario = comentario
        self.imagen = imagen
        self.importe = importe
        self.saldo = saldo


if len(sys.argv) != 2:
    print("Usage is: ing2ledger input.xls")
    exit(1)

ingfile = sys.argv[1]

# Constants referring where specific information is inside the xls file
coord_numerocuenta = (1,3)
coord_fechaexportacion = (3,3)

row_firstmovement = 6
col_fechavalor = 0
col_categoria = 1
col_subcategoria = 2
col_descripcion = 3
col_comentario = 4
col_imagen = 5
col_importe = 6
col_saldo = 7

# Open the file
book = open_workbook(ingfile)
sheet = book.sheet_by_index(0)

numerocuenta = sheet.cell(*coord_numerocuenta).value

listofmovements = list()
for row in range(row_firstmovement, sheet.nrows):
    listofmovements.append(movement(
                                    sheet.cell(row, col_fechavalor).value,
                                    sheet.cell(row, col_categoria).value,
                                    sheet.cell(row, col_subcategoria).value,
                                    sheet.cell(row, col_descripcion).value,
                                    sheet.cell(row, col_comentario).value,
                                    sheet.cell(row, col_imagen).value,
                                    sheet.cell(row, col_importe).value,
                                    sheet.cell(row, col_saldo).value))

for movement in listofmovements:
    print(movement.importe)
