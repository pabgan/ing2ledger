#!/usr/bin/env python3
import sys, argparse
import csv
from datetime import datetime

debugging = False

if debugging:
    print()
    print()
    print()
    print('=======================================')
    print('======= EMPEZAMOS =====================')
    print('=======================================')

#################################################################
# Auxiliary bits
date = 'fechavalor'
category = 'categoria'
subcategory = 'subcategoria'
description = 'descripcion'
comment = 'comentario'
amount = 'importe'
fieldnames=(date, category, subcategory, description, comment, amount)

#class transaction(object):
#    date = None
#    category = None
#    subcategory = None
#    description = None
#    comment = None
#    imagen = None
#    amount = None
#    saldo = None
#    
#    def __init__(self,date,category,subcategory,description,comment,imagen,amount,saldo):
#        self.date = date
#        self.category = category
#        self.subcategory = subcategory
#        self.description = description
#        self.comment = comment
#        self.imagen = imagen
#        self.amount = amount
#        self.saldo = saldo

#################################################################
# 1. Check arguments
if __name__ == "__main__":
    # TODO: Better description
    desc='''
Oh yeah
'''

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--accountscfg", help="Config file associating transaction descriptions with accounts.", type=str, default='Accounts.csv', required=False)
    args = parser.parse_args(sys.argv[1:-1])
    ingfile = sys.argv[-1]
    

#################################################################
# 2. Parse accounts config into a dictionary
accounts_dict = dict()
with open(args.accountscfg) as acf:
    acf_reader = csv.reader(acf, delimiter=';', quotechar='"')
    
    # Dismiss title line
    next(acf_reader)
    for row in acf_reader:
        # description;debit_account;credit_account;tag
        accounts_dict[row[0]] = (row[1], row[2], row[3])

if debugging:
    print(accounts_dict)

#################################################################
# 3. Parse input document
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
## 4. Translate every line in a ledger transaction
    for transaction in ingfile_reader:
        if debugging:
            print()
            print('---------------------------------------')
            print('Processing line \'%s\'' % transaction)
            print('---------------------------------------')

        if transaction[date] is None or len(transaction[date]) == 0 or transaction[amount] is None or len(transaction[amount]) == 0:
            # unuseful line
            print()
            print('WARNING - Ignoring line: %s' % (transaction))
            continue

        # 4.1 Separate each transaction with a blank line
        print("")

        # 4.2 Print date and description
        fecha = transaction[date].split('/')
        print("%s/%s/%s %s" % (fecha[2], fecha[1], fecha[0], transaction[description]))

        # 4.3 Print comment if there was any for this transaction
        if transaction[comment] is not None and len(transaction[comment]) != 0:
            print("\t;%s" % (transaction[comment]))

        # 4.4 Print credit account and ammount
        if transaction[description] in accounts_dict:
            if  accounts_dict[transaction[description]][2] != '':
                print ("\t%s\t\t%s ; %s" % (accounts_dict[transaction[description]][1], transaction[amount], accounts_dict[transaction[description]][2]))
            else:
                print ("\t%s\t\t%s" % (accounts_dict[transaction[description]][1], transaction[amount]))
            print("\t%s" % accounts_dict[transaction[description]][0])
        else:
            print("\t; This transaction is not configured")
            print("\tGastos:%s:%s\t\t€%s" %(transaction[category], transaction[subcategory], transaction[amount]))
            print("\tActivos:Cuentas:Pablo")
