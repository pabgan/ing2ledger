#!/usr/bin/env python3
import sys
from xlrd import open_workbook, xldate_as_tuple
from datetime import datetime

#################################################################
# Auxiliary bits
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

#################################################################
# 1. Check arguments
# TODO: Use argument parser
if len(sys.argv) != 2:
    print("Usage is: ing2ledger input.xls")
    exit(1)

ingfile = sys.argv[1]

#################################################################
# 2. Parse input document
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
                                    datetime(*xldate_as_tuple(sheet.cell(row, col_fechavalor).value, 0)),
                                    sheet.cell(row, col_categoria).value,
                                    sheet.cell(row, col_subcategoria).value,
                                    sheet.cell(row, col_descripcion).value,
                                    sheet.cell(row, col_comentario).value,
                                    sheet.cell(row, col_imagen).value,
                                    sheet.cell(row, col_importe).value,
                                    sheet.cell(row, col_saldo).value))

#################################################################
# TODO: 3. Identify last movement in common, that is, the last movement
#    that was written in the log file
for movement in listofmovements:
    # Separate each movement with a blank line
    print("\n")
    print("%s/%s/%s  %s" % (movement.fechavalor.year, movement.fechavalor.month, movement.fechavalor.day, movement.descripcion))
    if movement.comentario is not None and len(movement.comentario) != 0:
        print("\t;%s" % (movement.comentario))
    if movement.importe < 0:
        print("\tGastos:%s:%s\t\t€%s" %(movement.categoria, movement.subcategoria, movement.importe))
        print("\tAssets:Checking:Pablo")
    else:
        print("\tAssets:Checking:Pablo\t\t€%s" % (movement.importe))
        print("\t???")
