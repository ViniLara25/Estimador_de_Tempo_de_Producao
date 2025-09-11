#Comprimento de lâmina da peça de amostra 98.353,319mm. Tempo gasto: 23 minutos e 56 segundos.

import math

while True:
    try:
        valor_texto = input('Digite o comprimento de lâmina total para o corte: ');
        valor_correto = valor_texto.replace(',','.');
        valor = float(valor_correto);
        break;
    except ValueError: print('Valor inválido, por favor, digite novamente: ');

while True:
    try:
        qtd_fl_texto = input("Digite a quantidade total de folhas: ")
        qtd_fl_correto = qtd_fl_texto.replace(',','.')
        qtd_fl = int(qtd_fl_correto)
        break;
    except ValueError: print('Valor inválido, por favor, digite novaente: ');

comprimento = (valor*qtd_fl)/68.63

hora = comprimento/3600
hora_inteiro = math.floor(hora)

minuto = (hora-hora_inteiro)*60
minuto_inteiro = math.floor(minuto)

segundo = (minuto-minuto_inteiro)*60
segundo_inteiro = math.floor(segundo)

print (f'O tempo de produção será: \n {hora_inteiro}:{minuto_inteiro}:{segundo_inteiro}')