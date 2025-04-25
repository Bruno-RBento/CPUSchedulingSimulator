import random

def maiorID(lista):
    maior = 0
    for i in range(len(lista)):
        if len(lista[i]) == 2:  # Caso a tupla tenha apenas 2 elementos
            id, tempo = lista[i]
        elif len(lista[i]) == 3:  # Caso a tupla tenha 3 elementos
            id, tempo, prioridade = lista[i]
        if id > maior:
            maior = id
    return maior


def RoundRobin2(lista_processos, quantum=5,tempo_max=10):
    tempo_atual = 0
    ordem_execucao = []
    i = 0
    id_atual = maiorID(lista_processos) + 1

    while len(lista_processos) > 0:
        if i >= len(lista_processos):
            i = 0

        pid, burst = lista_processos[i]
        tempo_exec = min(burst, quantum)
        inicio = tempo_atual
        fim = inicio + tempo_exec
        ordem_execucao.append({"id": pid, "start": inicio, "end": fim})
        tempo_atual = fim

        if burst > quantum:
            lista_processos[i] = (pid, burst - quantum)
            i += 1
        else:
            print("Processo com o ID "+str(pid)+" concluído com sucesso")
            lista_processos.pop(i)
        num = random.randint(1, 100)
        if num <= 15:
            novo_burst = round(random.normalvariate(10, 2), 2)
            novo_burst = max(novo_burst, 0.5)  # Garante que o novo_burst não seja menor que 0.5
            novo_burst = min(novo_burst, tempo_max)  # Garante que o novo_burst não ultrapasse o tempo_max
            novo_processo = (id_atual, novo_burst)
            lista_processos.append(novo_processo)
            print("Processo com o ID "+str(id_atual)+" adicionado com sucesso")
            id_atual += 1


    return ordem_execucao

def ordenarTempoOrdemCrescente(lista):
    var_elemento = lista[0]
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            id1,tempo1 = lista[j]
            id2,tempo2 = lista[j + 1]
            if tempo1 > tempo2:
                var_elemento = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = var_elemento
    
    return lista

def ShortestJob2(lista_processos,tempo_max=10):
    tempo_atual = 0
    ordem_execucao = []
    id_atual = maiorID(lista_processos) + 1

    while len(lista_processos) > 0:
        ordenarTempoOrdemCrescente(lista_processos)
        pid, burst = lista_processos[0]
        inicio = tempo_atual
        fim = inicio + burst
        ordem_execucao.append({"id": pid, "start": inicio, "end": fim})
        tempo_atual = fim
        print("Processo com o ID "+str(pid)+" concluído com sucesso")
        lista_processos.pop(0)
        num = random.randint(1, 100)
        if num <= 15:
            novo_burst = round(random.normalvariate(10, 2), 2)
            novo_burst = max(novo_burst, 0.5)  # Garante que o novo_burst não seja menor que 0.5
            novo_burst = min(novo_burst, tempo_max)  # Garante que o novo_burst não ultrapasse o tempo_max
            novo_processo = (id_atual, novo_burst)
            lista_processos.append(novo_processo)
            print("Processo com o ID "+str(id_atual)+" adicionado com sucesso")
            id_atual += 1

    return ordem_execucao



def Priority_Preemptivo2(lista_processos, tempo_max=10):
    tempo_atual = 0
    ordem_execucao = []
    id_atual = maiorID(lista_processos) + 1

    while len(lista_processos) > 0:
        ordenarPorPrioridade(lista_processos)
        pid, burst, prioridade = lista_processos[0]
        inicio = tempo_atual
        fim = inicio + 1
        ordem_execucao.append({"id": pid, "start": inicio, "end": fim})
        tempo_atual = fim
        burst -= 1
        lista_processos[0] = (pid, burst, prioridade)

        if burst <= 0:
            print("Processo com o ID "+str(pid)+" concluído com sucesso")
            lista_processos.pop(0)
        else:
            lista_processos[0] = (pid, burst, prioridade)

        num = random.randint(1, 100)
        if num <= 0:
            novo_burst = round(random.normalvariate(10, 2), 2)
            novo_burst = max(novo_burst, 0.5)
            novo_burst = min(novo_burst, tempo_max)
            nova_prioridade = random.randint(1, 10)
            novo_processo = (id_atual, novo_burst, nova_prioridade)
            lista_processos.append(novo_processo)
            print("Processo com o ID "+str(id_atual)+" adicionado com sucesso")
            id_atual += 1

    return ordem_execucao



def ordenarPorPrioridade(lista):
    var_elemento = lista[0]
    id1 = 0
    tempo1 = 0
    id2 = 0
    tempo2 = 0
    prioridade1 = 0
    prioridade2 = 0
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            id1,tempo1,prioridade1 = lista[j]
            id2,tempo2,prioridade2 = lista[j + 1]
            if prioridade1 > prioridade2:
                var_elemento = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = var_elemento
    
    return lista

def Priority_NaoPreemptivo2(lista_processos, tempo_max=10):
    print("10")
    tempo_atual = 0
    ordem_execucao = []
    id_atual = maiorID(lista_processos) + 1

    while len(lista_processos) > 0:
        ordenarPorPrioridade(lista_processos)
        pid, burst, prioridade = lista_processos[0]
        inicio = tempo_atual
        fim = inicio + burst
        ordem_execucao.append({"id": pid, "start": inicio, "end": fim})
        tempo_atual = fim
        print("Processo com o ID "+str(pid)+" concluído com sucesso")
        lista_processos.pop(0)
        num = random.randint(1, 100)
        if num <= 15:
            novo_burst = round(random.normalvariate(10, 2), 2)
            novo_burst = max(novo_burst, 0.5)  # Garante que o novo_burst não seja menor que 0.5
            novo_burst = min(novo_burst, tempo_max)  # Garante que o novo_burst não ultrapasse o tempo_max
            nova_prioridade = random.randint(1, 10)
            novo_processo = (id_atual, novo_burst, nova_prioridade)
            lista_processos.append(novo_processo)
            print("Processo com o ID "+str(id_atual)+" adicionado com sucesso")
            id_atual += 1

    return ordem_execucao