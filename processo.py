from typing import List, Optional


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
