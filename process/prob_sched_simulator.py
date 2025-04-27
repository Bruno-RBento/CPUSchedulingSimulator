# Função para calcular o tempo de espera médio
def calculate_avg_waiting_time(processes):
    total_waiting_time = sum([p.waiting_time for p in processes])
    return total_waiting_time / len(processes)

# Função para calcular o tempo de turnaround médio
def calculate_avg_turnaround_time(processes):
    total_turnaround_time = sum([p.turnaround_time for p in processes])
    return total_turnaround_time / len(processes)

# Função para calcular a utilização da CPU
def calculate_cpu_utilization(cpu_time, total_time):
    return cpu_time / total_time

# Função para calcular o throughput
def calculate_throughput(processes, total_time):
    return len(processes) / total_time

# Rate Monotonic (RMS) Scheduling
def rate_monotonic_scheduler(processes):
    # Ordenar os processos por período (menor período = maior prioridade)
    processes.sort(key=lambda p: p.period)
    # Implementação do escalonamento e coleta de estatísticas

# EDF Scheduling
def edf_scheduler(processes):
    # Ordenar os processos por deadline (menor deadline = maior prioridade)
    processes.sort(key=lambda p: p.deadline)
    # Implementação do escalonamento e coleta de estatísticas

# Detecção de Deadline Misses
def detect_deadline_misses(processes):
    misses = []
    for p in processes:
        if p.completion_time > p.deadline:
            misses.append(p)
    return misses
