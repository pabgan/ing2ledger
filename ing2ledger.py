#!/usr/bin/env python3
import sys
import csv
from datetime import datetime

#################################################################
# Auxiliary bits
fechavalor = 'fechavalor'
categoria = 'categoria'
subcategoria = 'subcategoria'
descripcion = 'descripcion'
comentario = 'comentario'
importe = 'importe'
fieldnames=(fechavalor, categoria, subcategoria, descripcion, comentario, importe)

#class movement(object):
#    fechavalor = None
#    categoria = None
#    subcategoria = None
#    descripcion = None
#    comentario = None
#    imagen = None
#    importe = None
#    saldo = None
#    
#    def __init__(self,fechavalor,categoria,subcategoria,descripcion,comentario,imagen,importe,saldo):
#        self.fechavalor = fechavalor
#        self.categoria = categoria
#        self.subcategoria = subcategoria
#        self.descripcion = descripcion
#        self.comentario = comentario
#        self.imagen = imagen
#        self.importe = importe
#        self.saldo = saldo

#################################################################
# 1. Check arguments
# TODO: Use argument parser
if len(sys.argv) != 2:
    print("Usage is: ing2ledger input.csv")
    exit(1)

ingfile = sys.argv[1]

#################################################################
# 2. Parse input document
with open(ingfile) as csvfile:
    # First we extract metadata
    ingfile_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
    print('; Fichero importado: ' + ingfile)
    numero_de_cuenta = next(ingfile_reader)[3]
    print('; Número de cuenta: ' + numero_de_cuenta)
    titular = next(ingfile_reader)[3]
    print('; Titular: ' + titular)
    fecha_exportación = next(ingfile_reader)[3]
    print('; Fecha de exportación: ' + fecha_exportación)

    # Then we go with the data
    ingfile_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames)
    # Dismiss empty line
    next(ingfile_reader)
    # Dismiss column names
    next(ingfile_reader)

##################################################################
## 3. Translate every line in a ledger transaction
    for movement in ingfile_reader:
        if movement[fechavalor] is None or len(movement[fechavalor]) == 0 or movement[importe] is None or len(movement[importe]) == 0:
            # unuseful line
            continue
        # Separate each movement with a blank line
        print("")
        #print("%s/%s/%s  %s" % (movement.fechavalor.year, movement.fechavalor.month, movement.fechavalor.day, movement.descripcion))
        fecha = movement[fechavalor].split('/')
        print("%s/%s/%s %s" % (fecha[2], fecha[1], fecha[0], movement[descripcion]))
        if movement[comentario] is not None and len(movement[comentario]) != 0:
            print("\t;%s" % (movement[comentario]))
        movement[importe] = movement[importe].replace(',','.')
        if float(movement[importe]) < 0:
            print("\tGastos:%s:%s\t\t€%s" %(movement[categoria], movement[subcategoria], abs(float(movement[importe]))))
            print("\tActivos:Cuentas:Pablo")
        else:
            print("\tActivos:Cuentas:Pablo\t\t€%s" % (movement[importe]))
    
            if movement[descripcion] == "Nomina recibida Assia Ela, S.L.U.":
                print("\tIngresos:Nómina")
            elif movement[descripcion].find("Incentivo por compra TWYP") >= 0 or movement[descripcion].find("Abono por campaña Abono Shopping") >= 0:
                print("\tIngresos:ING")
            else:
                print("\t???")
