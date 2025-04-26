import time
import random
import copy



def FCFS4(lista_processos, tempo_max=100, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0

    lista = copy.deepcopy(lista_processos)  # <- COPIA antes de mexer

    lista.sort(key=lambda p: p.tempo_chegada)  # Ordena pela chegada

    for proc in lista:
        if processos_escalonados >= processos_max:
            break

        if proc.tempo_chegada > tempo_atual:
            tempo_atual = proc.tempo_chegada

        if tempo_atual + proc.tempo_execucao <= tempo_max:
            inicio = tempo_atual
            fim = inicio + proc.tempo_execucao
            proc.tempo_inicio = inicio
            proc.tempo_conclusao = fim

            ordem_execucao.append({
                "id": proc.pid,
                "start": inicio,
                "end": fim
            })

            tempo_atual = fim
            processos_escalonados += 1

        elif tempo_atual < tempo_max:
            inicio = tempo_atual
            fim = tempo_max
            tempo_execucao_parcial = fim - inicio

            proc.tempo_inicio = inicio
            proc.tempo_conclusao = fim

            ordem_execucao.append({
                "id": proc.pid,
                "start": inicio,
                "end": fim
            })

            tempo_atual = fim
            processos_escalonados += 1
            break

    return ordem_execucao




def ShortestJob3(lista_processos, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0

    # FAZER CÓPIA para não modificar a lista original:
    lista = copy.deepcopy(lista_processos)   # ← copia completa, objetos independentes

    lista.sort(key=lambda p: p.tempo_chegada)  # Primeiro ordena por chegada

    while lista and tempo_atual < tempo_max and processos_escalonados < processos_max:
        disponiveis = [p for p in lista if p.tempo_chegada <= tempo_atual]

        if not disponiveis:
            tempo_atual = lista[0].tempo_chegada
            continue

        disponiveis.sort(key=lambda p: p.tempo_execucao)
        proc = disponiveis[0]

        if tempo_atual + proc.tempo_execucao <= tempo_max:
            inicio = tempo_atual
            fim = inicio + proc.tempo_execucao
            proc.tempo_inicio = inicio
            proc.tempo_conclusao = fim

            ordem_execucao.append({
                "id": proc.pid,
                "start": inicio,
                "end": fim
            })

            tempo_atual = fim
            processos_escalonados += 1
            lista.remove(proc)

        else:
            inicio = tempo_atual
            fim = tempo_max

            proc.tempo_inicio = inicio
            proc.tempo_conclusao = fim

            ordem_execucao.append({
                "id": proc.pid,
                "start": inicio,
                "end": fim
            })

            tempo_atual = fim
            processos_escalonados += 1
            break

    return ordem_execucao



def RoundRobin2(lista_processos, quantum=5, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0
    fila = []

    lista = copy.deepcopy(lista_processos)  # ← copia completa, objetos independentes
    lista.sort(key=lambda p: p.tempo_chegada)

    while (lista or fila) and tempo_atual < tempo_max and processos_escalonados < processos_max:
        # Primeiro: adiciona processos que chegaram
        while lista and lista[0].tempo_chegada <= tempo_atual:
            fila.append(lista.pop(0))

        if not fila:
            if lista:
                tempo_atual = lista[0].tempo_chegada
            continue

        proc = fila.pop(0)

        # *** ANTES DE EXECUTAR, RE-CHECAR processos que chegaram ***
        while lista and lista[0].tempo_chegada <= tempo_atual:
            fila.append(lista.pop(0))

        if tempo_atual < tempo_max:
            inicio = tempo_atual
            tempo_executado = min(quantum, proc.tempo_execucao, tempo_max - tempo_atual)
            fim = inicio + tempo_executado

            if not hasattr(proc, 'tempo_inicio') or proc.tempo_inicio is None:
                proc.tempo_inicio = inicio

            proc.tempo_execucao -= tempo_executado
            proc.tempo_conclusao = fim

            ordem_execucao.append({
                "id": proc.pid,
                "start": inicio,
                "end": fim
            })

            tempo_atual = fim

            # *** Depois de avançar o tempo, RE-CHECAR de novo! ***
            while lista and lista[0].tempo_chegada <= tempo_atual:
                fila.append(lista.pop(0))

            if proc.tempo_execucao > 0:
                fila.append(proc)  # volta para o fim
            else:
                processos_escalonados += 1

    return ordem_execucao




def Priority_Preemptive(lista_processos, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0
    lista = copy.deepcopy(lista_processos)  # ← copia completa, objetos independentes

    lista.sort(key=lambda p: p.tempo_chegada)
    fila = []

    processo_atual = None

    while (lista or fila or processo_atual) and tempo_atual < tempo_max and processos_escalonados < processos_max:
        # Adiciona processos que chegaram até agora
        while lista and lista[0].tempo_chegada <= tempo_atual:
            fila.append(lista.pop(0))

        if processo_atual:
            fila.append(processo_atual)  # Se o processo atual ainda não acabou, volta pra fila

        if fila:
            fila.sort(key=lambda p: (p.prioridade, p.tempo_chegada))
            processo_atual = fila.pop(0)
        else:
            if lista:
                tempo_atual = lista[0].tempo_chegada
            processo_atual = None
            continue

        # Executa 1 unidade de tempo
        inicio = tempo_atual
        fim = inicio + 1

        if not hasattr(processo_atual, 'tempo_inicio') or processo_atual.tempo_inicio is None:
            processo_atual.tempo_inicio = inicio

        processo_atual.tempo_execucao -= 1
        processo_atual.tempo_conclusao = fim

        ordem_execucao.append({
            "id": processo_atual.pid,
            "start": inicio,
            "end": fim
        })

        tempo_atual = fim

        if processo_atual.tempo_execucao <= 0:
            processos_escalonados += 1
            processo_atual = None

    return ordem_execucao




def Priority_Non_Preemptive(lista_processos, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0
    lista = copy.deepcopy(lista_processos)
    lista.sort(key=lambda p: p.tempo_chegada)
    fila = []
    processo_atual = None
    
    while tempo_atual < tempo_max and (lista or fila or processo_atual) and processos_escalonados < processos_max:
        # Adiciona processos que chegaram até agora
        while lista and lista[0].tempo_chegada <= tempo_atual:
            fila.append(lista.pop(0))
            
        if processo_atual is None:
            if fila:
                # Pega o processo com maior prioridade (menor valor = maior prioridade)
                fila.sort(key=lambda p: (p.prioridade, p.tempo_chegada))
                processo_atual = fila.pop(0)
            else:
                # Se não há processos prontos, avança o tempo para a próxima chegada
                if lista:
                    tempo_atual = lista[0].tempo_chegada
                continue
        
        # Executa o processo até terminar
        inicio = tempo_atual
        fim = inicio + processo_atual.tempo_execucao
        
        if fim > tempo_max:
            fim = tempo_max
            processo_atual.tempo_execucao -= (fim - inicio)
        else:
            processo_atual.tempo_execucao = 0
        
        # Registra o tempo de início se for a primeira execução deste processo
        if not hasattr(processo_atual, 'tempo_inicio') or processo_atual.tempo_inicio is None:
            processo_atual.tempo_inicio = inicio
            
        processo_atual.tempo_conclusao = fim
        
        ordem_execucao.append({
            "id": processo_atual.pid,
            "start": inicio,
            "end": fim
        })
        
        tempo_atual = fim
        
        # Se o processo terminou completamente
        if processo_atual.tempo_execucao <= 0:
            processos_escalonados += 1
            processo_atual = None
    
    return ordem_execucao

