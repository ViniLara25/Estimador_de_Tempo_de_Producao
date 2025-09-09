#Comprimento de lâmina da peça de amostra 98.353,319mm. Tempo gasto: 23 minutos e 56 segundos.

while True:
    try:
        valor_texto = input('Digite o comprimento de lâmina total para o corte: ');
        valor_correto = valor_texto.replce(',','.');
        valor = float(valor_correto);
        break;
    except ValueError: print('Valor inválido, por favor, digite novamente: ');