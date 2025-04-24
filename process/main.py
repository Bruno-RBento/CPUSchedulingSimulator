import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from process.gerador import gerar_processos
from process.registo import Registo

config = {
    'chegada': 'exponential',  # Tipo de distribuição para os tempos de chegada
    'lambda': 0.5,  # Taxa de chegada
    'execucao': 'normal',  # Tipo de distribuição para os tempos de execução
    'media': 10,  # Média dos tempos de execução
    'desvio': 2,  # Desvio padrão para a distribuição normal
    'prioridade': 'uniforme'  # Distribuição para a prioridade dos processos
}

def exemplo():
    registo = Registo()
    processos = gerar_processos(5, config)  # Gerar 5 processos

    for p in processos:
        registo.registar(p.tempo_chegada, f"Gerado Processo {p.pid} com tempo de execução {p.tempo_execucao}")
    registo.mostrar()  # Exibir os logs registrados

if __name__ == "__main__":
    exemplo()


"""
Este ficheiro é geralmente o ponto de entrada para a execução do programa. 
Ele pode organizar a simulação, importar os módulos necessários e
orquestrar o processo de geração, execução e registo dos processos.
"""
