import datetime
# As importações corretas e limpas estão aqui
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import openpyxl

class ProducaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Produção")

        self.tempos_producao_segundos = []

        main_frame = ttk.Frame(root, padding=(20, 10))
        main_frame.pack(fill=BOTH, expand=True)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Comprimento total do desenho:").pack(pady=(5,2))
        self.entry_desenho = ttk.Entry(input_frame)
        self.entry_desenho.pack(fill=X)

        ttk.Label(input_frame, text="Comprimento de lâmina total para corte:").pack(pady=(10,2))
        self.entry_lamina = ttk.Entry(input_frame)
        self.entry_lamina.pack(fill=X)

        ttk.Label(input_frame, text="Quantidade total de folhas:").pack(pady=(10,2))
        self.entry_folhas = ttk.Entry(input_frame)
        self.entry_folhas.pack(fill=X)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Adicionar Produção", command=self.adicionar_producao, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Finalizar e Calcular Término", command=self.calcular_termino, bootstyle="primary").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Exportar Histórico", command=self.exportar_excel, bootstyle="info").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar Histórico", command=self.limpar_historico, bootstyle="danger").pack(side=LEFT, padx=5)

        self.resultado_label = ttk.Label(main_frame, text="", justify="center", font=("Helvetica", 10))
        self.resultado_label.pack(pady=10)

        self.tree = ttk.Treeview(main_frame, columns=("Desenho", "Lâmina", "Folhas", "Tempo"), show="headings")
        self.tree.heading("Desenho", text="Desenho")
        self.tree.heading("Lâmina", text="Lâmina")
        self.tree.heading("Folhas", text="Folhas")
        self.tree.heading("Tempo", text="Tempo Estimado")
        self.tree.pack(pady=10, fill="both", expand=True, padx=10)

        self.tree.column("Desenho", width=120, anchor="center")
        self.tree.column("Lâmina", width=120, anchor="center")
        self.tree.column("Folhas", width=100, anchor="center")
        self.tree.column("Tempo", width=150, anchor="center")
    
    def calcular_tempo_producao(self, valor_desenho, valor, qtd_fl):
        comprimento_desenho = (valor_desenho * qtd_fl) / 80.6214
        comprimento_corte = (valor * qtd_fl) / 140.3811
        comprimento_total = comprimento_desenho + comprimento_corte
        return int(comprimento_total)

    def adicionar_producao(self):
        try:
            valor_desenho = float(self.entry_desenho.get().replace(",", "."))
            valor = float(self.entry_lamina.get().replace(",", "."))
            qtd_fl = int(self.entry_folhas.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return

        tempo_producao_segundos = self.calcular_tempo_producao(valor_desenho, valor, qtd_fl)
        tempo_setup_segundos = 10 * 60
        tempo_total_item_segundos = tempo_producao_segundos + tempo_setup_segundos
        
        self.tempos_producao_segundos.append(tempo_total_item_segundos)
        tempo_formatado = str(datetime.timedelta(seconds=tempo_total_item_segundos))
        self.resultado_label.config(text=f"Produção adicionada!\nTempo estimado (com setup): {tempo_formatado}")

        self.tree.insert("", "end", values=(valor_desenho, valor, qtd_fl, tempo_formatado))

        self.entry_desenho.delete(0, ttk.END)
        self.entry_lamina.delete(0, ttk.END)
        self.entry_folhas.delete(0, ttk.END)

    def calcular_termino(self):
        if not self.tempos_producao_segundos:
            messagebox.showwarning("Aviso", "Nenhuma produção adicionada.")
            return

        tempo_total_segundos = sum(self.tempos_producao_segundos)
        tempo_restante_seg = tempo_total_segundos

        inicio_turno = datetime.time(8, 0)
        almoco_inicio = datetime.time(12, 0)
        almoco_fim = datetime.time(13, 0)
        cafe_inicio = datetime.time(15, 0)
        cafe_fim = datetime.time(15, 15)
        fim_turno = datetime.time(16, 30)

        cursor_tempo = datetime.datetime.now()
        
        if cursor_tempo.time() < inicio_turno:
            cursor_tempo = cursor_tempo.replace(hour=inicio_turno.hour, minute=inicio_turno.minute, second=0, microsecond=0)
        
        if cursor_tempo.time() >= fim_turno:
            cursor_tempo = (cursor_tempo + datetime.timedelta(days=1)).replace(hour=inicio_turno.hour, minute=inicio_turno.minute, second=0, microsecond=0)
        
        while tempo_restante_seg > 0:
            if cursor_tempo.weekday() >= 5:
                dias_para_segunda = 7 - cursor_tempo.weekday()
                cursor_tempo += datetime.timedelta(days=dias_para_segunda)
                cursor_tempo = cursor_tempo.replace(hour=inicio_turno.hour, minute=inicio_turno.minute, second=0, microsecond=0)
                continue
            
            dia_atual = cursor_tempo.date()
            periodos_trabalho = [
                (datetime.datetime.combine(dia_atual, inicio_turno), datetime.datetime.combine(dia_atual, almoco_inicio)),
                (datetime.datetime.combine(dia_atual, almoco_fim), datetime.datetime.combine(dia_atual, cafe_inicio)),
                (datetime.datetime.combine(dia_atual, cafe_fim), datetime.datetime.combine(dia_atual, fim_turno))
            ]

            for inicio_periodo, fim_periodo in periodos_trabalho:
                inicio_real_do_calculo = max(cursor_tempo, inicio_periodo)

                if inicio_real_do_calculo >= fim_periodo:
                    continue

                segundos_disponiveis_no_periodo = (fim_periodo - inicio_real_do_calculo).total_seconds()

                if tempo_restante_seg <= segundos_disponiveis_no_periodo:
                    cursor_tempo = inicio_real_do_calculo + datetime.timedelta(seconds=tempo_restante_seg)
                    tempo_restante_seg = 0
                    break
                else:
                    tempo_restante_seg -= segundos_disponiveis_no_periodo
                    cursor_tempo = fim_periodo
            
            if tempo_restante_seg > 0:
                proximo_dia = cursor_tempo.date() + datetime.timedelta(days=1)
                cursor_tempo = datetime.datetime.combine(proximo_dia, inicio_turno)

        hora_termino = cursor_tempo
        resumo = (
            f"Tempo total de produção: {str(datetime.timedelta(seconds=tempo_total_segundos))}\n"
            f"Previsão de término: {hora_termino.strftime('%d/%m/%Y às %H:%M:%S')}"
        )
        self.resultado_label.config(text=resumo)
        messagebox.showinfo("Resultado Final", resumo)

    def exportar_excel(self):
        if not self.tree.get_children():
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Arquivo Excel", "*.xlsx")], title="Salvar histórico")
        if not file_path: return
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Histórico Produção"
        sheet.append(["Desenho", "Corte", "Folhas", "Tempo Estimado"])
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            sheet.append(valores)
        workbook.save(file_path)
        messagebox.showinfo("Sucesso", f"Histórico exportado para:\n{file_path}")

    def limpar_historico(self):
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o histórico?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tempos_producao_segundos.clear()
            self.resultado_label.config(text="")
            messagebox.showinfo("Sucesso", "Histórico foi limpo.")

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = ProducaoApp(root)
    root.mainloop()