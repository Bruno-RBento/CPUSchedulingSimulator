from typing import List, Optional
import random
import numpy as np


class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao, prioridade, prazo=None, periodo=None):
        self.pid = pid
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.prioridade = prioridade
        self.prazo = prazo
        self.periodo = periodo
        self.tempo_inicio = None
        self.tempo_conclusao = None

def gerar_processos_R(qtd_processos: int, chegada: str, burst: str) -> List[Processo]:
    processos = []
    tempo_atual = 0

    for i in range(qtd_processos):
        pid = i + 1  # Começa no 1

        # Gerar tempo de chegada
        if chegada == "Poisson":
            lambda_chegada = 1  # Taxa média de chegada
            tempo_incremento = np.random.poisson(lambda_chegada)
            tempo_atual += tempo_incremento
        elif chegada == "Exponential":
            taxa_chegada = 1
            tempo_incremento = np.random.exponential(1 / taxa_chegada)
            tempo_atual += tempo_incremento
        else:
            raise ValueError("Tipo de chegada inválido. Use 'poisson' ou 'exponencial'.")

        # Gerar tempo de execução (burst)
        if burst == "Normal":
            tempo_execucao = max(0.1, np.random.normal(loc=5, scale=2))
        elif burst == "Exponential":
            tempo_execucao = max(0.1, np.random.exponential(scale=3))
        else:
            raise ValueError("Tipo de burst inválido. Use 'normal' ou 'exponencial'.")

        # Gerar prioridade entre 1 e 5
        prioridade = random.randint(1, 5)

        processo = Processo(
            pid=pid,
            tempo_chegada=round(tempo_atual, 2),
            tempo_execucao=round(tempo_execucao, 2),
            prioridade=prioridade
        )
        processos.append(processo)

    return processos


def converter_processos_para_tabela(processos: List[Processo]):
    """
    Converte uma lista de objetos Processo em uma lista de tuplas para inserção na TreeView do Tkinter.
    """
    tabela = []
    for p in processos:
        linha = (
            p.pid,
            p.tempo_chegada,
            p.tempo_execucao,
            p.prioridade if p.prioridade is not None else '-',
            p.periodo if p.periodo is not None else '-'
        )
        tabela.append(linha)
    return tabela


# Exemplo de uso:
exemplo_processos = [
    Processo("P1", 0.0, 5.0, 1),
    Processo("P2", 1.0, 3.0, 2, periodo=10),
    Processo("P3", 2.0, 4.0, 3)
]

converter_processos_para_tabela(exemplo_processos)
