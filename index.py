import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import plotly.express as px
import pandas as pd
import threading
from PIL import Image, ImageTk


from gannt import gerar_grafico_png

from importcsv  import importar_csv
from algoritmos import (
    FCFS,
    FCFS2,
    FCFS3_lista_objetos,
    roundRobin,
    shortestJob,
    Priority_Scheduling_Preemptivo,
    Priority_Scheduling_Non_Preemptivo
)


root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("800x700")

algorithm_var = tk.StringVar()
simulation_mode = tk.StringVar()
quantum_var = tk.StringVar()
max_time_var = tk.StringVar()
process_count_var = tk.StringVar()
arrival_dist_var = tk.StringVar()
burst_dist_var = tk.StringVar()


modo_entrada_var = tk.StringVar(value="importar")
tipo_processo_var = tk.StringVar(value="aperiodico")

processos = []

main_frame = ttk.Frame(root)
main_frame.pack(pady=10)


def alternar_modo(modo):
    tipo_frame.pack_forget()
    import_frame.pack_forget()
    gerar_frame.pack_forget()

    if modo == "importar":
        tipo_frame.pack(pady=5)
        import_frame.pack(pady=5)
    else:
        gerar_frame.pack(pady=5, fill='x', padx=10)

def gerar_processos(tipo):
    messagebox.showinfo("Gerar", f"Gerar processos {tipo} com distribuições selecionadas.")


def converter_processos_para_tabela(processos):
    """
    Converte objetos Processo em tuplas legíveis para a TreeView.
    """
    return [
        (
            p.pid,
            p.tempo_chegada,
            p.tempo_execucao,
            p.prioridade if p.prioridade is not None else '-',
            p.periodo if p.periodo is not None else '-'
        )
        for p in processos
    ]


def update_process_queue():
    queue_box.delete(*queue_box.get_children())
    for linha in converter_processos_para_tabela(processos):
        queue_box.insert('', 'end', values=linha)
        
def on_algorithm_selected(event=None):
    algoritmo = algorithm_var.get()
    if "Round Robin" in algoritmo:
        quantum_entry.config(state='normal')
    else:
        quantum_entry.config(state='disabled')


def mostrar_gantt(dados):
    for widget in frame_gantt.winfo_children():
        widget.destroy()

    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para mostrar!")
        return

    processos_convertidos = [
        {
            "Processo": f"P{p['id']}",
            "Inicio": p["start"],
            "Duracao": p["end"] - p["start"]
        }
        for p in dados
    ]

    imagem_path = gerar_grafico_png(processos_convertidos)
    imagem = Image.open(imagem_path)
    imagem_tk = ImageTk.PhotoImage(imagem)

    label = tk.Label(frame_gantt, image=imagem_tk)
    label.image = imagem_tk
    label.pack(padx=10, pady=10)


def iniciar_simulacao():
    modo = modo_entrada_var.get()
    tipo = tipo_processo_var.get()
    algoritmo = algorithm_var.get()

    if not processos:
        messagebox.showwarning("Aviso", "Nenhum processo carregado ou gerado!")
        return

    if tipo == "aperiodico":
        if algoritmo.startswith("First-Come"):
            gantt_data = FCFS3_lista_objetos(processos)
            mostrar_gantt(gantt_data)

        elif algoritmo.startswith("Shortest Job"):
            processos_ordenados = sorted(processos, key=lambda p: p.tempo_execucao)
            gantt_data = FCFS2(processos_ordenados)  # ou um algoritmo próprio
            mostrar_gantt(gantt_data)

        # Exemplo para Round Robin:
        elif algoritmo.startswith("Round Robin"):
            try:
                quantum = int(quantum_var.get())
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insere um valor válido para o quantum.")
                return

            gantt_data = roundRobin(processos, quantum)
            mostrar_gantt(gantt_data)

        # Outros algoritmos podem seguir a mesma lógica...

    elif tipo == "periodico":
        messagebox.showinfo("Aviso", f"O algoritmo '{algoritmo}' será aplicado a processos periódicos — a simulação ainda não está implementada aqui.")


# Scheduling Algorithm
ttk.Label(main_frame, text="Scheduling Algorithm").pack(pady=5)
algorithm_menu = ttk.Combobox(main_frame, textvariable=algorithm_var, state="readonly")
algorithm_menu['values'] = ["First-Come, First-Served (FCFS)", "Shortest Job (SJ)", "Priority Preemptive","Priority  Non-Preemptive", "Round Robin (RR)", "RT Rate Monotonic", "EDF (Earliest Deadline First)", "Multilevel Queue Scheduling"]
algorithm_menu.pack()
algorithm_menu.bind("<<ComboboxSelected>>", on_algorithm_selected)

# Time controls
time_frame = ttk.Frame(main_frame)
time_frame.pack(pady=10)

ttk.Label(time_frame, text="Tempo Máximo").grid(row=0, column=0, padx=5, sticky='w')
max_time_entry = ttk.Entry(time_frame, textvariable=max_time_var, width=20)
max_time_entry.grid(row=1, column=0, padx=5)

ttk.Label(time_frame, text="Nº de Processos").grid(row=0, column=1, padx=5, sticky='w')
process_count_entry = ttk.Entry(time_frame, textvariable=process_count_var, width=20)
process_count_entry.grid(row=1, column=1, padx=5)

# Quantum
quantum_frame = ttk.Frame(main_frame)
quantum_frame.pack(pady=10)
ttk.Label(quantum_frame, text="Time Quantum (for Round Robin scheduling)").grid(row=0, column=0, sticky="w")
quantum_entry = ttk.Entry(quantum_frame, textvariable=quantum_var, width=20, state='disabled')
quantum_entry.grid(row=1, column=0, pady=5)

# Modo de Entrada
entrada_frame = ttk.LabelFrame(main_frame, text="Modo de Entrada de Processos")
entrada_frame.pack(pady=10, fill='x', padx=10)

ttk.Radiobutton(entrada_frame, text="Importar de CSV", variable=modo_entrada_var, value="importar", command=lambda: alternar_modo("importar")).pack(anchor='w', padx=10)
ttk.Radiobutton(entrada_frame, text="Gerar Aleatoriamente", variable=modo_entrada_var, value="gerar", command=lambda: alternar_modo("gerar")).pack(anchor='w', padx=10)

# Tipo de processo
tipo_frame = ttk.LabelFrame(main_frame, text="Tipo de Processo")
ttk.Radiobutton(tipo_frame, text="Geral/Aperiódico", variable=tipo_processo_var, value="aperiodico").pack(anchor='w', padx=10)
ttk.Radiobutton(tipo_frame, text="Periódico (Tempo Real)", variable=tipo_processo_var, value="periodico").pack(anchor='w', padx=10)

# Frame de importação
import_frame = ttk.Frame(main_frame)
import_button = ttk.Button(import_frame, text="Importar CSV", command=lambda: importar_csv(processos, tipo_processo_var, update_process_queue))
import_button.pack()

# Frame de geração
gerar_frame = ttk.LabelFrame(main_frame, text="Parâmetros de Geração Aleatória")

ttk.Label(gerar_frame, text="Distribuição de Chegada").grid(row=0, column=0, sticky='w')
ttk.Combobox(gerar_frame, textvariable=arrival_dist_var, values=["Poisson", "Exponential"], state='readonly').grid(row=0, column=1, padx=5)

ttk.Label(gerar_frame, text="Distribuição de Burst").grid(row=1, column=0, sticky='w')
ttk.Combobox(gerar_frame, textvariable=burst_dist_var, values=["Normal", "Exponential"], state='readonly').grid(row=1, column=1, padx=5)

ttk.Button(gerar_frame, text="Gerar Processos Aleatórios", command=lambda: gerar_processos(tipo_processo_var.get())).grid(row=2, column=0, columnspan=6, pady=10)

# Botão para iniciar simulação (fora do main_frame para ficar sempre no fim)
start_button = ttk.Button(root, text="Iniciar Simulação", command=lambda: iniciar_simulacao())
start_button.pack(pady=20)


queue_label = ttk.Label(main_frame, text="Fila de Processos")
queue_label.pack()

queue_box = ttk.Treeview(main_frame, columns=("ID", "Chegada", "Burst", "Prioridade", "Período"), show='headings')
for col in ("ID", "Chegada", "Burst", "Prioridade", "Período"):
    queue_box.heading(col, text=col)
    queue_box.column(col, anchor='center', width=100)  # define largura e alinhamento


queue_box.pack(pady=10, fill='x')

frame_gantt = ttk.LabelFrame(root, text="Gráfico Gantt")
frame_gantt.pack(fill='both', expand=True, padx=10, pady=10)


# Inicia no modo de importação
alternar_modo("importar")

# Loop principal
root.mainloop()
