import random
import time


def gerar_processos():
    tamanho = random.randint(1, 10)  # gera o número da lista de processos(entre 1 e 5)
    lista_processos = []

    for i in range(1, tamanho + 1):
        tempo = random.randint(0, 10)  # tempo de execução aleatório entre 1 e 10
        lista_processos.append((i, tempo))

    return lista_processos

def gerar_processos3():
    tamanho = random.randint(1, 10)  # gera o número da lista de processos(entre 1 e 5)
    lista_processos = []

    for i in range(1, tamanho + 1):
        tempo = random.randint(0, 10)  # tempo de execução aleatório entre 1 e 10
        prioridade = random.randint(1,5)
        lista_processos.append((i, tempo,prioridade))

    return lista_processos

def FCFS(lista_processos):
    duration = 0
    i = -1
    while len(lista_processos) > 0:
        i = i + 1
        tempo = 2
        while tempo > 1:
            if len(lista_processos) > i:
                id,tempo = lista_processos[i]
                duration += 1
                print(lista_processos[i])
                lista_processos[i] = (id, tempo - 1)
                time.sleep(1)

        id,tempo = lista_processos[i]
        if tempo == 0:
            print("Processo com o id "+str(id)+" concluido com sucesso")

# O i é o indice do array e o id = i + 1
def roundRobin(lista_processos):
    intervalo_exe = 5
    i = 0
    nao_incrementar = 0
    while len(lista_processos) > 0:
        if len(lista_processos) <= i:
            i = 0
            nao_incrementar = 0
        id,tempo = lista_processos[i]
        if tempo > intervalo_exe:
            lista_processos[i] = (id,tempo - intervalo_exe)
            i = i + 1
        else:
            print("Processo com o id "+str(id)+" concluido com sucesso!")
            lista_processos.pop(i)
        time.sleep(1)
        
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

def imprimir_lista(lista):
    new_lista = []
    for i in range(len(lista)):
        new_lista.append(lista[i])
    print("Lista Atual: "+str(new_lista))


def shortestJob(lista_processos):
    contador = 1
    id = 0
    tempo = 0
    id2 = 0
    tempo2 = 0
    # Executa até não haver mais "processos" a executar
    while len(lista_processos) > 0:
        ordenarTempoOrdemCrescente(lista_processos)
        imprimir_lista(lista_processos)
        id,tempo = lista_processos[0]
        lista_processos[0] = (id,tempo - 1)
        # Gerar mais um processo em 15% das vezes, ou seja, temos 15% de probabilidades de termos um processo adicionado
        num = random.randint(1, 100)
        if num <= 15:
            while contador >= 1:
                if contador >= 1:
                    var_id = random.randint(1,100)
                    var_tempo = random.randint(1,10)
                    contador = 0
                for j in range(len(lista_processos)):
                    id2,tempo2 = lista_processos[j] 
                    if id2 == var_id:
                        contador += 1
            lista_processos.append((var_id,var_tempo))
            print("Processo com o id "+str(var_id)+" adicionado com sucesso")    
        id3,tempo3 = lista_processos[0]
        if tempo3 < 0:
            print("Processo com o id "+str(id3)+" concluido com sucesso!")
            lista_processos.pop(0)
        
        time.sleep(1)


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

# Preemptivo que para um processo se chegar um com nível de prioridade superior
def Priority_Scheduling_Preemptivo(lista_processos):
    contador = 1
    id = 0
    tempo = 0
    id2 = 0
    tempo2 = 0
    prioridade = 0
    prioridade2 = 0
    i = -1
    # Executa até não haver mais "processos" a executar
    while len(lista_processos) > 0:
        i = i + 1
        ordenarPorPrioridade(lista_processos)
        imprimir_lista(lista_processos)
        id,tempo,prioridade = lista_processos[0]
        lista_processos[0] = (id,tempo - 1,prioridade)
        num = random.randint(1, 100)
        if num <= 15:
            id2,tempo2,prioridade2 = lista_processos[len(lista_processos) - 1]
            var_id = id2 + 1
            lista_processos.append((var_id,random.randint(1,5),random.randint(1,5)))
            print("Processo com o ID "+str(var_id)+" adicionado com sucesso")

        if tempo <= 0:
            print("Processo com o ID "+str(id)+" eliminado com sucesso")
            lista_processos.pop(0)
        time.sleep(1)

def maiorID(lista):
    maior = 0
    for i in range(len(lista) - 1):
        id,tempo,prioridade = lista[i]
        if id > maior:
            maior = id
    return maior
        


def Priority_Scheduling_Non_Preemptivo(lista_processos):
    contador = 1
    id = 0
    tempo = 0
    guardarElementoAtual = lista_processos[0]
    id2 = 0
    tempo2 = 0
    prioridade = 0
    var_maiorID = 0
    prioridade2 = 0
    i = -1
    # Executa até não haver mais "processos" a executar
    while len(lista_processos) > 0:
        i = i + 1
        var_maiorID = maiorID(lista_processos)
        guardarElementoAtual = lista_processos[0]
        lista_processos.pop(0)
        ordenarPorPrioridade(lista_processos)
        # O insert está a inserir no inicio da lista(posição 0)
        lista_processos.insert(0,guardarElementoAtual)
        imprimir_lista(lista_processos)
        id,tempo,prioridade = lista_processos[0]
        tempo = tempo - 1
        lista_processos[0] = (id,tempo,prioridade)
        num = random.randint(1, 100)
        if num <= 15:
            var_tempo = random.randint(1,10)
            var_prioridade = random.randint(1,5)
            contador = 0
            var_id = var_maiorID + 1
            lista_processos.append((var_id,var_tempo,var_prioridade))
            print("Processo com o id "+str(var_id)+" adicionado com sucesso")   

        if tempo <= 0:
            print("Processo com o ID "+str(id)+" eliminado com sucesso")
            lista_processos.pop(0)
        time.sleep(1)


    



# Exemplo de uso
if __name__ == "__main__":
    #processos = gerar_processos()
    #processos3 = gerar_processos3()
    #print("Lista de processos:", processos)
    #FCFS(processos)
    #roundRobin(processos)
    #lista = ordenarTempoOrdemCrescente(processos)
    #for i in range(len(lista)):
    #    print(lista[i])
    #Priority_Scheduling_Non_Preemptivo(processos3)
    print("PROCESSOS ALEATORIAMENTE USANDO A BIBLIOTECA RANDOM!!!")
    print("Menu:")
    print(" 1 - FCFS (First-Come, First-Served)")
    print(" 2 - SJ (Shortest Job)")
    print(" 3 - Round Robin")
    print(" 4 - Priority Scheduling (preemptivo)")
    print(" 5 - Priority Scheduling (não-preemptivo)")
    print(" 6 - Sair")
    res_utilizador = int(input("Introduza um número: "))
    while res_utilizador != 6:
        if res_utilizador == 1:
                processos = gerar_processos()
                print("Lista de processos:", processos)
                FCFS(processos)

        elif res_utilizador == 2:
            processos = gerar_processos()
            print("Lista de processos:", processos)
            shortestJob(processos)

        elif res_utilizador == 3:
            processos = gerar_processos()
            print("Lista de processos:", processos)
            roundRobin(processos)
        
        elif res_utilizador == 4:
            processos = gerar_processos3()
            print("Lista de processos:", processos)
            Priority_Scheduling_Preemptivo(processos)

        elif res_utilizador == 5:
            processos = gerar_processos3()
            print("Lista de processos:", processos)
            Priority_Scheduling_Non_Preemptivo(processos)
        else:
            break

        print("PROCESSOS ALEATORIAMENTE USANDO A BIBLIOTECA RANDOM!!!")
        print("Menu:")
        print(" 1 - FCFS (First-Come, First-Served)")
        print(" 2 - SJ (Shortest Job)")
        print(" 3 - Round Robin")
        print(" 4 - Priority Scheduling (preemptivo)")
        print(" 5 - Priority Scheduling (não-preemptivo)")
        print(" 6 - Sair")
        res_utilizador = int(input("Introduza um número: "))
        