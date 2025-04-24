class Registo:
    def __init__(self):
        self.linhas = []  # Lista de logs

    def registar(self, tempo, mensagem):
        self.linhas.append((tempo, mensagem))  # Registra a mensagem com o tempo

    def mostrar(self):
        for tempo, mensagem in sorted(self.linhas):
            print(f"[{tempo}] {mensagem}")  # Exibe os logs ordenados por tempo

"""
Responsável pelo registo ou acompanhamento do estado dos processos. 
Este ficheiro pode armazenar e processar informações sobre os processos 
enquanto estão a ser executados, 
como tempos de início, 
término, e outros dados relevantes para a simulação.
"""
