import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


from gannt import gerar_grafico_png

from importcsv  import importar_csv

from algoritmos import (
    FCFS,
    ShortestJob,
    RoundRobin,
    Priority_Preemptive,
    Priority_Non_Preemptive,
    Rate_monotonic,
    Edf,
    Multilevel_Queue_Scheduling
)

from processo import (
    gerar_processos_R
)

root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1200x1000")

algorithm_var = tk.StringVar()
simulation_mode = tk.StringVar()
quantum_var = tk.StringVar()
max_time_var = tk.StringVar()
process_count_var = tk.StringVar()
arrival_dist_var = tk.StringVar()
burst_dist_var = tk.StringVar()

media_espera_var = tk.StringVar()
media_retorno_var = tk.StringVar()
media_resposta_var = tk.StringVar()
utilizacao_var = tk.StringVar()
throughput_var = tk.StringVar()
min_espera_var = tk.StringVar()
max_espera_var = tk.StringVar()
min_resposta_var = tk.StringVar()
max_resposta_var = tk.StringVar()
min_retorno_var = tk.StringVar()
max_retorno_var = tk.StringVar()
ociosidade_var = tk.StringVar()
processos_concluidos_var = tk.StringVar()


modo_entrada_var = tk.StringVar(value="importar")
tipo_processo_var = tk.StringVar(value="aperiodico")

processos = []

columns_frame = ttk.Frame(root)
columns_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Coluna Esquerda
left_frame = ttk.Frame(columns_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

# Coluna Direita
right_frame = ttk.Frame(columns_frame)
right_frame.grid(row=0, column=1, sticky="nsew")

columns_frame.columnconfigure(0, weight=1)
columns_frame.columnconfigure(1, weight=2)
columns_frame.rowconfigure(0, weight=1)


def alternar_modo(modo):
    tipo_frame.pack_forget()
    import_frame.pack_forget()
    gerar_frame.pack_forget()

    if modo == "importar":
        tipo_frame.pack(pady=5)
        import_frame.pack(pady=5)
    else:
        gerar_frame.pack(pady=5, fill='x', padx=10)

def gerar_processos():
    global processos
    num_processos = int(process_count_var.get())
    chegada = arrival_dist_var.get()
    burst = burst_dist_var.get()
    
    processos = gerar_processos_R(num_processos, chegada, burst)
    update_process_queue()

def converter_processos_para_tabela(processos):
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


def calcular_e_mostrar_estatisticas(processos, gantt_data):
    tempos_espera = []
    tempos_retorno = []
    tempos_resposta = []
    
    tempo_cpu = 0
    tempo_total = 0
    
    primeiro_start = {}
    fim_processo = {}
    
    for evento in gantt_data:
        pid = evento['id']
        start = evento['start']
        end = evento['end']
        
        if pid not in primeiro_start:
            primeiro_start[pid] = start
        
        fim_processo[pid] = end
        tempo_cpu += (end - start)

    if fim_processo:
        tempo_total = max(fim_processo.values())

    for p in processos:
        pid = p.pid
        chegada = p.tempo_chegada
        burst = p.tempo_execucao
        
        start = primeiro_start.get(pid, chegada)
        end = fim_processo.get(pid, chegada + burst)
        
        espera = (start - chegada)
        retorno = (end - chegada)
        resposta = (start - chegada)
        
        tempos_espera.append(espera)
        tempos_retorno.append(retorno)
        tempos_resposta.append(resposta)

    # Médias
    media_espera = sum(tempos_espera) / len(tempos_espera) if tempos_espera else 0
    media_retorno = sum(tempos_retorno) / len(tempos_retorno) if tempos_retorno else 0
    media_resposta = sum(tempos_resposta) / len(tempos_resposta) if tempos_resposta else 0
    throughput = (len(processos) / tempo_total) if tempo_total > 0 else 0


    # Mínimos e máximos
    min_espera = min(tempos_espera) if tempos_espera else 0
    max_espera = max(tempos_espera) if tempos_espera else 0
    min_resposta = min(tempos_resposta) if tempos_resposta else 0
    max_resposta = max(tempos_resposta) if tempos_resposta else 0
    min_retorno = min(tempos_retorno) if tempos_retorno else 0
    max_retorno = max(tempos_retorno) if tempos_retorno else 0

    # Atualizar variáveis
    media_espera_var.set(f"{media_espera:.2f} segundos")
    media_retorno_var.set(f"{media_retorno:.2f} segundos")
    media_resposta_var.set(f"{media_resposta:.2f} segundos")

    throughput_var.set(f"{throughput:.2f} processos/segundos")

    # Variáveis novas (que podes usar nos novos campos)
    min_espera_var.set(f"{min_espera:.2f} segundos")
    max_espera_var.set(f"{max_espera:.2f} segundos")
    min_resposta_var.set(f"{min_resposta:.2f} segundos")
    max_resposta_var.set(f"{max_resposta:.2f} segundos")
    min_retorno_var.set(f"{min_retorno:.2f} segundos")
    max_retorno_var.set(f"{max_retorno:.2f} segundos")
    processos_concluidos_var.set(str(len(processos)))


def iniciar_simulacao():
    modo = modo_entrada_var.get()
    tipo = tipo_processo_var.get()
    algoritmo = algorithm_var.get()

    if not processos:
        messagebox.showwarning("Aviso", "Nenhum processo carregado ou gerado!")
        return

    if tipo == "aperiodico":
        if algoritmo.startswith("First-Come"):
            gantt_data = FCFS(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)


        elif algoritmo.startswith("Shortest Job"):
            gantt_data = ShortestJob(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)
            
        elif algoritmo.startswith("Round Robin (RR)"):
                gantt_data = RoundRobin(processos, quantum=int(quantum_var.get()), tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
                calcular_e_mostrar_estatisticas(processos, gantt_data)
                mostrar_gantt(gantt_data)
            
        elif algoritmo.startswith("Priority Preemptive"):
            gantt_data = Priority_Preemptive(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)
            
        
        elif algoritmo.startswith("Priority Non-Preemptive"):
            gantt_data = Priority_Non_Preemptive(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)
            

    elif tipo == "periodico":
        if algoritmo.startswith("RT Rate Monotonic"):
            gantt_data = Rate_monotonic(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)

        elif algoritmo.startswith("EDF (Earliest Deadline First)"):
            gantt_data = Edf(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)

        elif algoritmo.startswith("Multilevel Queue Scheduling"):
            gantt_data = Multilevel_Queue_Scheduling(processos, tempo_max=int(max_time_var.get()), processos_max=int(process_count_var.get()))
            calcular_e_mostrar_estatisticas(processos, gantt_data)
            mostrar_gantt(gantt_data)



    elif tipo == "periodico":
        messagebox.showinfo("Aviso", f"O algoritmo '{algoritmo}' será aplicado a processos periódicos — a simulação ainda não está implementada aqui.")


# Scheduling Algorithm
ttk.Label(left_frame, text="Scheduling Algorithm").pack(pady=5)
algorithm_menu = ttk.Combobox(left_frame, textvariable=algorithm_var, state="readonly")
algorithm_menu['values'] = ["First-Come, First-Served (FCFS)", "Shortest Job (SJ)", "Priority Preemptive","Priority Non-Preemptive", "Round Robin (RR)", "RT Rate Monotonic", "EDF (Earliest Deadline First)", "Multilevel Queue Scheduling"]
algorithm_menu.pack()
algorithm_menu.bind("<<ComboboxSelected>>", on_algorithm_selected)

# Time controls
time_frame = ttk.Frame(left_frame)
time_frame.pack(pady=10)

ttk.Label(time_frame, text="Tempo Máximo").grid(row=0, column=0, padx=5, sticky='w')
max_time_entry = ttk.Entry(time_frame, textvariable=max_time_var, width=20)
max_time_entry.grid(row=1, column=0, padx=5)

ttk.Label(time_frame, text="Nº de Processos").grid(row=0, column=1, padx=5, sticky='w')
process_count_entry = ttk.Entry(time_frame, textvariable=process_count_var, width=20)
process_count_entry.grid(row=1, column=1, padx=5)

# Quantum
quantum_frame = ttk.Frame(left_frame)
quantum_frame.pack(pady=10)
ttk.Label(quantum_frame, text="Time Quantum (for Round Robin scheduling)").grid(row=0, column=0, sticky="w")
quantum_entry = ttk.Entry(quantum_frame, textvariable=quantum_var, width=20, state='disabled')
quantum_entry.grid(row=1, column=0, pady=5)

# Modo de Entrada
entrada_frame = ttk.LabelFrame(left_frame, text="Modo de Entrada de Processos")
entrada_frame.pack(pady=10, fill='x', padx=10)

ttk.Radiobutton(entrada_frame, text="Importar de CSV", variable=modo_entrada_var, value="importar", command=lambda: alternar_modo("importar")).pack(anchor='w', padx=10)
ttk.Radiobutton(entrada_frame, text="Gerar Aleatoriamente", variable=modo_entrada_var, value="gerar", command=lambda: alternar_modo("gerar")).pack(anchor='w', padx=10)

# Tipo de processo
tipo_frame = ttk.LabelFrame(left_frame, text="Tipo de Processo")
ttk.Radiobutton(tipo_frame, text="Geral/Aperiódico", variable=tipo_processo_var, value="aperiodico").pack(anchor='w', padx=10)
ttk.Radiobutton(tipo_frame, text="Periódico (Tempo Real)", variable=tipo_processo_var, value="periodico").pack(anchor='w', padx=10)

# Frame de importação
import_frame = ttk.Frame(left_frame)
import_button = ttk.Button(import_frame, text="Importar CSV", command=lambda: importar_csv(processos, tipo_processo_var, update_process_queue))
import_button.pack()

# Frame de geração
gerar_frame = ttk.LabelFrame(left_frame, text="Parâmetros de Geração Aleatória")

ttk.Label(gerar_frame, text="Numero de Processos").grid(row=0, column=0, sticky='w')
ttk.Entry(gerar_frame, textvariable=process_count_var, width=20).grid(row=0, column=1, padx=5)

ttk.Label(gerar_frame, text="Distribuição de Chegada").grid(row=1, column=0, sticky='w')
ttk.Combobox(gerar_frame, textvariable=arrival_dist_var, values=["Poisson", "Exponential"], state='readonly').grid(row=1, column=1, padx=5)

ttk.Label(gerar_frame, text="Distribuição de Burst").grid(row=2, column=0, sticky='w')
ttk.Combobox(gerar_frame, textvariable=burst_dist_var, values=["Normal", "Exponential"], state='readonly').grid(row=2, column=1, padx=5)

ttk.Button(gerar_frame, text="Gerar Processos Aleatórios", command=gerar_processos).grid(row=3, column=0, columnspan=6, pady=10)


start_button = ttk.Button(left_frame, text="Iniciar Simulação", command=lambda: iniciar_simulacao())
start_button.pack(pady=20)


queue_label = ttk.Label(left_frame, text="Fila de Processos")
queue_label.pack()

queue_box = ttk.Treeview(left_frame, columns=("ID", "Chegada", "Burst", "Prioridade", "Período"), show='headings')
for col in ("ID", "Chegada", "Burst", "Prioridade", "Período"):
    queue_box.heading(col, text=col)
    queue_box.column(col, anchor='center', width=100)  # define largura e alinhamento

queue_box.pack(pady=10, fill='x')

"""
exec_label = ttk.Label(right_frame, text="Lista de Execução (Durante Simulação)")
exec_label.pack()

exec_box = ttk.Treeview(right_frame, columns=("Tempo", "PID", "Ação"), show='headings')
for col in ("Tempo", "PID", "Ação"):
    exec_box.heading(col, text=col)
    exec_box.column(col, anchor='center', width=120) 


exec_box.pack(pady=10, fill='x')

    """
    
frame_resultados = ttk.Frame(right_frame)
frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)


frame_gantt = ttk.LabelFrame(frame_resultados, text="Gráfico Gantt")
frame_gantt.pack(fill='both', expand=True, padx=10, pady=10)


frame_estatisticas = ttk.LabelFrame(frame_resultados, text="Estatísticas da Simulação")
frame_estatisticas.pack(fill='x', padx=10, pady=10)

ttk.Label(frame_estatisticas, text="Tempo médio de espera:").grid(row=0, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=media_espera_var, state='readonly').grid(row=0, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo médio de retorno:").grid(row=1, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=media_retorno_var, state='readonly').grid(row=1, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo médio de resposta:").grid(row=2, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=media_resposta_var, state='readonly').grid(row=2, column=1, sticky='ew', pady=2)


ttk.Label(frame_estatisticas, text="Throughput:").grid(row=4, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=throughput_var, state='readonly').grid(row=4, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo mínimo de espera:").grid(row=5, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=min_espera_var, state='readonly').grid(row=5, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo máximo de espera:").grid(row=6, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=max_espera_var, state='readonly').grid(row=6, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo mínimo de resposta:").grid(row=7, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=min_resposta_var, state='readonly').grid(row=7, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo máximo de resposta:").grid(row=8, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=max_resposta_var, state='readonly').grid(row=8, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo mínimo de retorno:").grid(row=9, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=min_retorno_var, state='readonly').grid(row=9, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Tempo máximo de retorno:").grid(row=10, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=max_retorno_var, state='readonly').grid(row=10, column=1, sticky='ew', pady=2)

ttk.Label(frame_estatisticas, text="Processos Concluídos:").grid(row=12, column=0, sticky='w', pady=2)
tk.Entry(frame_estatisticas, textvariable=processos_concluidos_var, state='readonly').grid(row=12, column=1, sticky='ew', pady=2)


frame_estatisticas.columnconfigure(1, weight=1)

alternar_modo("importar")

root.mainloop()