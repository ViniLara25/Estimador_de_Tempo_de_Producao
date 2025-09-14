#Comprimento de lâmina da peça de amostra 98.353,319mm. Tempo gasto: 23 minutos e 56 segundos.

import math

while True:
    try:
        valor_desenho_texto = input('Digite o comprimento total do desenho: ')
        valor_desenho_correto = valor_desenho_texto.replace(',','.')
        valor_desenho = float(valor_desenho_correto)
        break;
    except ValueError: print("Valor inválido, digite novamente: ")

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

comprimento_desenho = (valor_desenho*qtd_fl)/80.6214
comprimento_corte = (valor*qtd_fl)/140.3811

hora_corte = comprimento_corte/3600
hora_corte_int = math.floor(hora_corte)

minuto_corte = (hora_corte-hora_corte_int)*60
minuto_corte_int = math.floor(minuto_corte)

segundo_corte = (minuto_corte-minuto_corte_int)*60
segundo_corte_int = math.floor(segundo_corte)

hora_draw = comprimento_desenho/3600
hora_draw_int = math.floor(hora_draw)

minuto_draw = (hora_draw-hora_draw_int)*60
minuto_draw_int = math.floor(minuto_draw)

segundo_draw = (minuto_draw-minuto_draw_int)*60
segundo_draw_int = math.floor(segundo_draw)


comprimento_total = comprimento_desenho+comprimento_corte

hora = comprimento_total/3600
hora_inteiro = math.floor(hora)

minuto = (hora-hora_inteiro)*60
minuto_inteiro = math.floor(minuto)

segundo = (minuto-minuto_inteiro)*60
segundo_inteiro = math.floor(segundo)

print(f"Tempo gasto para traçado é de: {hora_draw_int}:{minuto_draw_int}:{segundo_draw_int}\nTempo gasto para corte é de: {hora_corte_int}:{minuto_corte_int}:{segundo_corte_int}\nTempo total de produção: {hora_inteiro}:{minuto_inteiro}:{segundo_inteiro} \n(Horas:Minutos:Segundos)")