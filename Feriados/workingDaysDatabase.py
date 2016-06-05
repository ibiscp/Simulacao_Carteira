__author__ = 'Ibis'

import xlrd
from datetime import datetime
import sqlite3

def createDatabase():
    conn = sqlite3.connect('Feriados.db')
    c = conn.cursor()

    str = '''CREATE TABLE Feriados (
    'Date'	TEXT NOT NULL UNIQUE,
    'Descrição' STRING,
    PRIMARY KEY(Date))'''

    # Create table
    c.execute(str)

    # Save (commit) the changes
    conn.commit()
    conn.close()

    return

def insertMany(data):

    conn = sqlite3.connect('Feriados.db')
    c = conn.cursor()

    str = 'INSERT INTO Feriados VALUES (?,?)'
    c.executemany(str, data)

    conn.commit()
    conn.close()

    return

TeamPointWorkbook = xlrd.open_workbook('feriados_nacionais.xls')
sheet = TeamPointWorkbook.sheet_by_index(0)

feriados = list(list())

for row in range(1,sheet.nrows-9):

    date = xlrd.xldate_as_tuple(sheet.cell_value(row,0), TeamPointWorkbook.datemode)
    date = datetime(*date)
    date = date.strftime("%Y/%m/%d")
    descricao = sheet.cell_value(row,2)

    feriados.append((date,descricao))

createDatabase()
insertMany(feriados)

'''if (date.isoweekday() in range(1, 6)):
    print('É')
else:
    print('Não')'''
#date = datetime(*dateT)
#date = sheet.cell_value(row,0)
#date = datetime.strptime(date,'%d/%m/%Y')