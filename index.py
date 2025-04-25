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

def update_process_queue():
    queue_box.delete(*queue_box.get_children())
    for p in processos:
        queue_box.insert('', 'end', values=(
            p.get('id', '-'),
            p.get('start', '-'),
            p.get('burst', '-'),
            p.get('priority', '-'),
            p.get('period', '-')  # só terá valor se for periódico
        ))
        
def on_algorithm_selected(event=None):
    algoritmo = algorithm_var.get()
    if "Round Robin" in algoritmo:
        quantum_entry.config(state='normal')
    else:
        quantum_entry.config(state='disabled')


def mostrar_gantt(dados):
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para mostrar!")
        return

    # Converter os dados da simulação para o formato necessário
    processos_convertidos = [
        {
            "Processo": f"P{p['id']}",
            "Inicio": p["start"],
            "Duracao": p["end"] - p["start"]
        }
        for p in dados
    ]

    # Gerar imagem do gráfico
    imagem_path = gerar_grafico_png(processos_convertidos)

    # Mostrar imagem em nova janela Tkinter
    janela = tk.Toplevel()
    janela.title("Gantt Chart")

    imagem = Image.open(imagem_path)
    imagem_tk = ImageTk.PhotoImage(imagem)

    label = tk.Label(janela, image=imagem_tk)
    label.image = imagem_tk  # evitar garbage collection
    label.pack(padx=10, pady=10)

def iniciar_simulacao():
    modo = modo_entrada_var.get()
    tipo = tipo_processo_var.get()
    algoritmo = algorithm_var.get()

    if not processos:
        messagebox.showwarning("Aviso", "Nenhum processo carregado ou gerado!")
        return

    gantt_data = []
    current_time = 0

    if tipo == "aperiodico":
        if algoritmo.startswith("First-Come"):
            dados = [(i + 1, p["burst"]) for i, p in enumerate(processos)]
            FCFS2(dados)

            for p in processos:
                start = current_time
                end = current_time + p["burst"]
                gantt_data.append({"id": p["id"], "start": start, "end": end})
                current_time = end
            mostrar_gantt(gantt_data)

        elif algoritmo.startswith("Shortest Job"):
            dados = sorted(processos, key=lambda p: p["burst"])
            for p in dados:
                start = current_time
                end = current_time + p["burst"]
                gantt_data.append({"id": p["id"], "start": start, "end": end})
                current_time = end
            shortestJob([(i+1, p["burst"]) for i, p in enumerate(dados)])
            mostrar_gantt(gantt_data)

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


# Inicia no modo de importação
alternar_modo("importar")

# Loop principal
root.mainloop()
