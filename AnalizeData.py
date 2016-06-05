#import analyzeAll

__author__ = 'Ibis'

import database2
import xlrd
from _datetime import datetime
import xlsxwriter
from operator import itemgetter
from math import floor
import matplotlib.pyplot as plt
import numpy as np

#analyzeAll.updateBD()

# Le os títulos salvos no arquivo Ativos, junto com as datas que foram comprados e a quantidade
def readCSV(name):

    data = list(())

    TeamPointWorkbook = xlrd.open_workbook(name)
    sheet = TeamPointWorkbook.sheet_by_index(0)

    for row in range(0,sheet.nrows):
        date = sheet.cell_value(row,1)
        dateT = xlrd.xldate_as_tuple(sheet.cell_value(row,1), TeamPointWorkbook.datemode)
        date = datetime(*dateT)
        date = date.strftime("%Y/%m/%d")
        data.append([sheet.cell_value(row,0), date, sheet.cell_value(row,2)])

    return data

data = readCSV('Ativos.xlsx')

# Pega a maior data entre os ativos
maiorData = ''
for i in data:
    if i[1]>maiorData:
        maiorData = i[1]

# Ordena lista por nome dos títulos
data = sorted(data, key=itemgetter(0))

# Agrupa os títulos que são iguais, somando suas quantidades
newData = list(())
nome = data[0][0]
quantidade = float(data[0][2])
for i in range(1,len(data)):
    if data[i][0] == nome:
        quantidade = quantidade + float(data[i][2])
    else:
        newData.append([nome, quantidade])
        nome = data[i][0]
        quantidade = float(data[i][2])
    if i == len(data)-1:
        newData.append([nome, quantidade])

# Create an new Excel file and add a worksheet.
# workbook = xlsxwriter.Workbook('Alocacao.xlsx')
# worksheet = workbook.add_worksheet()

# Para cada título salvo em ativos pega o histórico de preço daquela data em diante
# for i in newData:
#
#     coluna = newData.index(i)+1
#
#     bdData = database2.getPreçoVenda(i[0], maiorData)
#
#     # Write some numbers, with row/column notation.
#     if newData.index(i) == 0:
#         worksheet.write(0, 0, 'Date')
#     worksheet.write(0, coluna, str(i[0]))
#
#     for j in bdData:
#         linha = bdData.index(j)+1
#         if newData.index(i) == 0:
#             worksheet.write(linha, 0, j[0])
#         a = floor(float(j[1])*float(i[1])*100)/100
#         worksheet.write(linha, coluna, a)
#
# workbook.close()

## Plota a quantia em R$ investido em cada título
# bla = list(())
#
# for i in newData:
#
#     bdData = database2.getPreçoVenda(i[0], maiorData)
#
#     datas = list()
#     valores = list()
#
#     for j in bdData:
#
#         date_object = datetime.strptime(j[0], '%Y/%m/%d')
#         datas.append(date_object)
#         a = floor(float(j[1])*float(i[1])*100)/100
#         valores.append(a)
#
#     bla.append([datas,valores])
#
# for i in bla:
#     plt.plot(i[0], i[1], '.-')
#     plt.hold(True)
#
# plt.show()

# Plota as percentagem investidas em cada título
titulos = list(())

for i in newData:

    bdData = database2.getPreçoVenda(i[0], maiorData)

    # Multiplica o preço de venda do título pelo número total de títulos em posse
    multiplicado = [[x[0], floor(float(x[1])*float(i[1])*100)/100] for x in bdData]

    titulos.append(multiplicado)

percentagens = list(())

for i in range(0,len(titulos[0])):

    # Calcula o total investido
    total = 0
    for j in titulos:
        total = total + j[i][1]

    percentagem = list()

    for j in titulos:
        percentagem.append(floor(j[i][1]/total*100*100)/100)

    percentagens.append([titulos[0][i][0],percentagem])

titulos = list()
for i in range(0,len(percentagens[0][1])):

    datas = list()
    valores = list()

    for j in percentagens:

        date_object = datetime.strptime(j[0], '%Y/%m/%d')
        datas.append(date_object)
        valores.append(j[1][i])

    titulos.append([datas, valores])

for i in titulos:
    plt.plot(i[0], i[1], '.-')
    plt.hold(True)

plt.show()