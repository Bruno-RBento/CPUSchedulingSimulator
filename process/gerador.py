import numpy as np
from .processo import Processo

def gerar_processos(qtd_processos, configuracao_distribuicao, primeiro_pid=1):
    processos = []  # Lista que irá armazenar os processos gerados
    tempo_atual = 0  # Tempo de chegada do primeiro processo é 0

    for i in range(qtd_processos):
        # Tempo de chegada (Poisson ou Exponencial)
        if configuracao_distribuicao['chegada'] == 'poisson':
            intervalo = np.random.poisson(lam=configuracao_distribuicao['lambda'])
        else:
            intervalo = np.random.exponential(scale=1.0 / configuracao_distribuicao['lambda'])
        tempo_atual += intervalo  # Atualiza o tempo de chegada com o intervalo gerado

        # Tempo de execução (burst) (Normal ou Exponencial)
        if configuracao_distribuicao['execucao'] == 'normal':
            tempo_execucao = max(1, np.random.normal(loc=configuracao_distribuicao['media'], scale=configuracao_distribuicao['desvio']))
        else:
            tempo_execucao = np.random.exponential(scale=configuracao_distribuicao['media'])

        # Prioridade (uniforme ou ponderada)
        if configuracao_distribuicao['prioridade'] == 'uniforme':
            prioridade = np.random.randint(1, 6)  # De 1 a 5
        else:
            prioridade = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])

        # Se a configuração de distribuição tiver um 'periodo', cria-se um processo periódico
        if 'periodo' in configuracao_distribuicao:
            periodo = configuracao_distribuicao['periodo']
        else:
            periodo = None  # Não é um processo periódico

        pid = primeiro_pid + i  # Gerar o PID sequencial

        # Criação do processo com os parâmetros
        processo = Processo(
            pid=pid,
            tempo_chegada=round(tempo_atual),
            tempo_execucao=round(tempo_execucao, 2),
            prioridade=prioridade,
            prazo=None,  # Pode ser adicionado um prazo, se necessário
            periodo=periodo  # Passa o periodo para o processo
        )

        processos.append(processo)  # Adiciona o processo à lista de processos

    return processos  # Retorna a lista de processos gerados


"""
Este ficheiro tem a função de gerar os processos. 
Através de configurações e distribuições probabilísticas (como Poisson, Exponencial, Normal), 
ele cria processos com tempos de chegada, tempos de execução, prioridades, entre outros atributos.
O objetivo é simular a chegada de processos que o escalonador irá gerenciar.
"""

