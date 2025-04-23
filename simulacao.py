
import random

# --------------------------
# Classe do processo
# --------------------------
class Processo:
    def __init__(self, pid, chegada, burst, prioridade=0, deadline=None):
        self.pid = pid
        self.chegada = chegada
        self.burst = burst
        self.prioridade = prioridade
        self.deadline = deadline

        self.restante = burst
        self.inicio = None
        self.fim = None
        self.estado = "novo"

# --------------------------
# Função de log
# --------------------------
def log(mensagem):
    print(mensagem)
    with open("logs.txt", "a") as f:
        f.write(mensagem + "\n")

# --------------------------
# Gerar processo aleatório
# --------------------------
def gerar_processo(pid):
    chegada = int(random.expovariate(1/3))
    burst = max(1, int(random.expovariate(1/4)))
    deadline = chegada + burst + random.randint(0, 3)  # ajusta la tolerancia
    return Processo(pid, chegada, burst, deadline=deadline)

# --------------------------
# Função para calcular estatísticas
# --------------------------
def calcular_estatisticas(processos, tempo_total, tempo_ocupado_cpu):
    tempos_espera = []
    tempos_retorno = []
    erros_deadline = 0 

    for p in processos:
        if p.inicio is not None and p.fim is not None:
            espera = p.inicio - p.chegada
            retorno = p.fim - p.chegada
            tempos_espera.append(espera)
            tempos_retorno.append(retorno)

            # Verificação de deadline (apenas se houver)
            if p.deadline is not None and p.fim > p.deadline:
                erros_deadline += 1

    # Cálculo das métricas
    media_espera = sum(tempos_espera) / len(tempos_espera) if tempos_espera else 0
    media_retorno = sum(tempos_retorno) / len(tempos_retorno) if tempos_retorno else 0
    utilizacao_cpu = tempo_ocupado_cpu / tempo_total if tempo_total > 0 else 0
    throughput = len(tempos_retorno) / tempo_total if tempo_total > 0 else 0

    # Impressão
    print("\nEstatísticas:")
    print(f"Tempo médio de espera: {media_espera:.2f}")
    print(f"Tempo médio de retorno: {media_retorno:.2f}")
    print(f"Utilização da CPU: {utilizacao_cpu:.2%}")
    print(f"Throughput: {throughput:.2f} processos/unidade de tempo")
    print(f"Erros de deadline: {erros_deadline}")
    print(f"Tempo total simulado: {tempo_total}")
    print(f"Tempo ocupado pela CPU: {tempo_ocupado_cpu}")

    print("\nDetalhes por processo:")
    for p in processos:
        print(f"Processo {p.pid} - Chegada: {p.chegada}, Início: {p.inicio}, Fim: {p.fim}, Burst: {p.burst}, Deadline: {p.deadline}")



# --------------------------
# Simulação FCFS
# --------------------------
def simulacao_fcfs(processos):
    tempo = 0
    fila_prontos = []
    processos_ativos = processos.copy()
    processo_atual = None
    tempo_ocupado_cpu = 0

    # Limpa o arquivo de logs
    with open("logs.txt", "w") as f:
        f.write("")

    while fila_prontos or processo_atual or processos_ativos:
        for p in processos:
            if p.chegada == tempo:
                p.estado = "pronto"
                fila_prontos.append(p)
                log(f"Tempo {tempo}: Processo {p.pid} chegou (burst={p.burst})")

        if not processo_atual and fila_prontos:
            processo_atual = fila_prontos.pop(0)
            processo_atual.estado = "executando"
            if processo_atual.inicio is None:
                processo_atual.inicio = tempo
            log(f"Tempo {tempo}: Processo {processo_atual.pid} começou a executar")

        if processo_atual:
            processo_atual.restante -= 1
            tempo_ocupado_cpu += 1
            if processo_atual.restante == 0:
                processo_atual.estado = "terminado"
                processo_atual.fim = tempo + 1
                log(f"Tempo {tempo + 1}: Processo {processo_atual.pid} terminou")
                processos_ativos.remove(processo_atual)
                processo_atual = None

        tempo += 1

    return tempo, tempo_ocupado_cpu

# --------------------------
# MAIN - Execução do simulador
# --------------------------
if __name__ == "__main__":
    random.seed(42)  # Para reprodutibilidade

    # Gerar lista de processos aleatórios
    processos = [gerar_processo(i + 1) for i in range(5)]
    processos.sort(key=lambda p: p.chegada)

    # Simular FCFS
    tempo_total, tempo_ocupado_cpu = simulacao_fcfs(processos)

    # Calcular estatísticas
    calcular_estatisticas(processos, tempo_total, tempo_ocupado_cpu)