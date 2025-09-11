#pip install pyinstaller (Instalar no terminal do codespace.)
#pyinstaller --onefile aplicacao.py
#pyinstaller --onefile --noconsole aplicacao.py
#O arquivo xecutavél estará na pasta dist.

import math
import tkinter as tk
from tkinter import messagebox

def calcular_produtividade():
    """
    Função para calcular a produtividade e exibir o resultado.
    """
    try:
        # Pega os valores dos campos de entrada
        valor_str = entrada_comprimento.get().replace(',', '.')
        qtd_fl_str = entrada_folhas.get().replace(',', '.')

        # Converte para float e int
        valor = float(valor_str)
        qtd_fl = int(qtd_fl_str)

        # Lógica de cálculo
        comprimento = (valor * qtd_fl) / 140.3811
        hora = comprimento / 3600
        hora_inteiro = math.floor(hora)

        minuto = (hora - hora_inteiro) * 60
        minuto_inteiro = math.floor(minuto)

        segundo = (minuto - minuto_inteiro) * 60
        segundo_inteiro = math.floor(segundo)

        # Formata o tempo e exibe na label de resultado
        tempo_producao = f"{hora_inteiro:02}:{minuto_inteiro:02}:{segundo_inteiro:02}"
        resultado_label.config(text=f"Tempo de produção: {tempo_producao} (Horas:Minutos:Segundos)")

    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos. Por favor, digite números.")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Calculadora de Produtividade")
janela.geometry("400x200")

# Widgets (elementos da interface)
frame = tk.Frame(janela, padx=10, pady=10)
frame.pack(expand=True)

# Comprimento da lâmina
tk.Label(frame, text="Comprimento de lâmina total:").grid(row=0, column=0, pady=5)
entrada_comprimento = tk.Entry(frame)
entrada_comprimento.grid(row=0, column=1, pady=5)

# Quantidade de folhas
tk.Label(frame, text="Quantidade total de folhas:").grid(row=1, column=0, pady=5)
entrada_folhas = tk.Entry(frame)
entrada_folhas.grid(row=1, column=1, pady=5)

# Botão de cálculo
botao_calcular = tk.Button(frame, text="Calcular", command=calcular_produtividade)
botao_calcular.grid(row=2, columnspan=2, pady=10)

# Label para exibir o resultado
resultado_label = tk.Label(frame, text="Tempo de produção: ")
resultado_label.grid(row=3, columnspan=2, pady=5)

# Iniciar o loop principal da interface
janela.mainloop()