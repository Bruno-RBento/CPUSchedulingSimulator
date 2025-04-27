import time
import random
import copy



def FCFS(lista_processos, tempo_max=100, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0

    lista = lista_processos.copy()  # <- COPIA antes de mexer

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




def ShortestJob(lista_processos, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0

    # FAZER CÓPIA para não modificar a lista original:
    lista = lista_processos.copy()

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



def RoundRobin(lista_processos, quantum=5, tempo_max=10, processos_max=100):
    tempo_atual = 0
    ordem_execucao = []
    processos_escalonados = 0
    fila = []

    lista = lista_processos.copy()
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
    
    # Faz uma cópia segura da lista
    lista_filtrada = [p for p in lista_processos if p.tempo_chegada <= tempo_max]
    lista_filtrada = lista_filtrada[:processos_max]  # Limitar o número de processos
    lista = copy.deepcopy(lista_filtrada)
    
    # Ordena inicialmente por tempo de chegada
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

def Rate_monotonic(lista_processos, tempo_max=10, processos_max=100):
    # Filtrar os processos antes de copiar
    lista_filtrada = [p for p in lista_processos if p.tempo_chegada <= tempo_max]
    lista_filtrada = lista_filtrada[:processos_max]  # Limitar ao máximo de processos

    lista = copy.deepcopy(lista_filtrada)  # Cópia da lista filtrada
    tempo = 0
    ordem_execucao = []
    
    for p in lista:
        if not hasattr(p, 'tempo_restante') or p.tempo_restante is None:
            p.tempo_restante = p.tempo_execucao
        if hasattr(p, 'periodo') and p.periodo is not None:
            p.proxima_chegada = p.tempo_chegada + p.periodo
        else:
            p.proxima_chegada = float('inf')
    
    while tempo < tempo_max:
        for p in lista:
            if hasattr(p, 'periodo') and p.proxima_chegada <= tempo and p.tempo_restante <= 0:
                p.tempo_restante = p.tempo_execucao
                p.proxima_chegada += p.periodo
        
        prontos = [p for p in lista if p.tempo_chegada <= tempo and p.tempo_restante > 0]
        
        prontos.sort(key=lambda p: (p.periodo if hasattr(p, 'periodo') else float('inf'), p.tempo_chegada))
        
        if prontos:
            p = prontos[0]
            inicio = tempo
            tempo_exec = min(1, p.tempo_restante, tempo_max - tempo)
            fim = inicio + tempo_exec
            p.tempo_restante -= tempo_exec
            
            ordem_execucao.append({
                "id": p.pid,
                "start": inicio,
                "end": fim
            })
            
            tempo = fim
        else:
            tempo += 1
    
    return ordem_execucao

def Edf(lista_processos, tempo_max=30, processos_max=100):
    # Filtrar primeiro os processos que chegaram até tempo_max
    lista_filtrada = [p for p in lista_processos if p.tempo_chegada <= tempo_max]
    
    # Limitar o número máximo de processos
    lista_filtrada = lista_filtrada[:processos_max]
    
    # Fazer uma cópia segura da lista filtrada
    lista = copy.deepcopy(lista_filtrada)
    
    tempo = 0
    ordem_execucao = []
    
    for p in lista:
        if not hasattr(p, 'tempo_restante') or p.tempo_restante is None:
            p.tempo_restante = p.tempo_execucao
        if hasattr(p, 'periodo') and p.periodo is not None:
            p.proxima_chegada = p.tempo_chegada + p.periodo
            p.deadline = p.proxima_chegada
        else:
            p.proxima_chegada = float('inf')
            p.deadline = float('inf')
    
    while tempo < tempo_max:
        # Atualizar deadlines para processos que chegam novamente
        for p in lista:
            if hasattr(p, 'periodo') and p.proxima_chegada <= tempo and p.tempo_restante <= 0:
                p.tempo_restante = p.tempo_execucao
                p.proxima_chegada += p.periodo
                p.deadline = p.proxima_chegada
        
        # Processos prontos para executar
        prontos = [p for p in lista if p.tempo_chegada <= tempo and p.tempo_restante > 0]
        
        # Escolher processo com deadline mais próximo
        prontos.sort(key=lambda p: (p.deadline if hasattr(p, 'deadline') else float('inf'), p.tempo_chegada))
        
        if prontos:
            p = prontos[0]
            inicio = tempo
            tempo_exec = min(1, p.tempo_restante, tempo_max - tempo)
            fim = inicio + tempo_exec
            p.tempo_restante -= tempo_exec
            
            ordem_execucao.append({
                "id": p.pid,
                "start": inicio,
                "end": fim
            })
            
            tempo = fim
        else:
            tempo += 1
    
    return ordem_execucao

def Multilevel_Queue_Scheduling(lista_processos, tempo_max=30, processos_max=100):
    # Filtrar apenas processos de tempo real (com período definido)
    lista_filtrada = [p for p in lista_processos if p.tempo_chegada <= tempo_max and p.periodo is not None]
    
    # Limitar o número máximo de processos
    lista_filtrada = lista_filtrada[:processos_max]
    
    # Deepcopy seguro
    lista = copy.deepcopy(lista_filtrada)
    
    tempo = 0
    ordem_execucao = []
    
    # Inicializar estados
    for p in lista:
        if not hasattr(p, 'tempo_restante') or p.tempo_restante is None:
            p.tempo_restante = p.tempo_execucao
        if p.periodo is not None:
            p.proxima_chegada = p.tempo_chegada + p.periodo
            p.deadline = p.proxima_chegada
        else:
            p.proxima_chegada = float('inf')
            p.deadline = float('inf')
    
    while tempo < tempo_max:
        for p in lista:
            if p.periodo is not None and p.proxima_chegada <= tempo and p.tempo_restante <= 0:
                p.tempo_restante = p.tempo_execucao
                p.proxima_chegada += p.periodo
                p.deadline = p.proxima_chegada
        
        prontos = [p for p in lista if p.tempo_chegada <= tempo and p.tempo_restante > 0]
        
        if prontos:
            prontos.sort(key=lambda p: (p.deadline, p.tempo_chegada))
            p = prontos[0]
            
            inicio = tempo
            tempo_exec = min(1, p.tempo_restante, tempo_max - tempo)
            fim = inicio + tempo_exec
            p.tempo_restante -= tempo_exec
            
            ordem_execucao.append({
                "id": p.pid,
                "start": inicio,
                "end": fim
            })
            
            tempo = fim
        else:
            tempo += 1
    
    return ordem_execucao