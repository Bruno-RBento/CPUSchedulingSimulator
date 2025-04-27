from tkinter import filedialog, messagebox
import csv
from processo import Processo

def importar_csv(processos, tipo_processo_var, update_process_queue):
    tipo = tipo_processo_var.get()
    filepath = filedialog.askopenfilename(
        title="Selecionar Ficheiro CSV",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        return

    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            leitor = csv.reader(csvfile)
            header = next(leitor)
            processos.clear()

            if tipo == "aperiodico":
                for row in leitor:
                    if len(row) >= 4:
                        pid = row[0]
                        start = float(row[1])
                        burst = float(row[2])
                        priority = int(row[3])
                        proc = Processo(pid, start, burst, priority)
                        processos.append(proc)

            elif tipo == "periodico":
                for row in leitor:
                    if len(row) >= 4:
                        pid = row[0]
                        start = float(row[1])
                        burst = float(row[2])
                        period = float(row[3])
                        proc = Processo(pid, start, burst, prioridade=0, periodo=period)
                        processos.append(proc)

            messagebox.showinfo("Importado", f"{len(processos)} processos {tipo} importados com sucesso.")
            update_process_queue()

    except Exception as e:
        messagebox.showerror("Erro ao importar", f"Ocorreu um erro: {e}")
