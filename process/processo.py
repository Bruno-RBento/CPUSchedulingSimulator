class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao, prioridade, prazo=None, periodo=None):
        self.pid = pid  # Identificador único do processo
        self.tempo_chegada = tempo_chegada  # Quando o processo chega
        self.tempo_execucao = tempo_execucao  # Tempo de execução necessário
        self.tempo_restante = tempo_execucao  # Tempo restante para execução
        self.prioridade = prioridade  # Prioridade do processo
        self.prazo = prazo  # Prazo de execução (para algoritmos em tempo real)
        self.periodo = periodo  # Período (para processos periódicos)
        self.tempo_inicio = None  # Quando começou a execução
        self.tempo_conclusao = None  # Quando terminou

"""
Este ficheiro define a classe Processo, que representa cada processo na simulação. 
A classe contém atributos como o ID do processo (PID), tempo de chegada, tempo de execução, 
tempo restante, prioridade, prazo, entre outros. Esta classe ajuda a estruturar os dados de cada processo 
para que possam ser manipulados e simulados no escalonador.
"""
