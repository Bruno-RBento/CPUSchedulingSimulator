import random
import time
import numpy as np
from operator import neg


def ordem_chegada(lista):
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            if lista[j].tempo_chegada > lista[j + 1].tempo_chegada:
                armazenar_processo = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = armazenar_processo
    return lista


def FCFS(lista_processos):
    i = 0
    tempo_a_mais = 0
    while len(lista_processos) > 0:
        ordem_chegada(lista_processos)
        while lista_processos[i].tempo_execucao > 0:
            if len(lista_processos) > i:
                lista_processos[i].tempo_execucao = round(lista_processos[i].tempo_execucao,2)
                print(lista_processos[i])
                lista_processos[i].tempo_execucao -= 1
                lista_processos[i].tempo_execucao = round(lista_processos[i].tempo_execucao,2)
                time.sleep(1)

        if lista_processos[i].tempo_execucao <= 0.0:
            tempo_a_mais = neg(lista_processos[i].tempo_execucao)
            lista_processos[i + 1].tempo_execucao -= tempo_a_mais
            print("Processo com o id "+str(lista_processos[i].pid)+" concluido com sucesso")
            lista_processos.pop(i)


def roundRobin(lista_processos,intervalo_exe = 5):
    i = 0
    nao_incrementar = 0
    while len(lista_processos) > 0:
        if len(lista_processos) <= i:
            i = 0
            nao_incrementar = 0
        if lista_processos[i].tempo_execucao > intervalo_exe:
            lista_processos[i].tempo_execucao -= intervalo_exe
            print("Processo com o ID "+str(lista_processos[i].pid)+" não eliminado, pois ainda faltam "+str(round(lista_processos[i].tempo_execucao,2))+" segundos para terminar")
            i = i + 1
        else:
            print("Processo com o id "+str(lista_processos[i].pid)+" concluido com sucesso!")
            lista_processos.pop(i)
        time.sleep(1)
        

def ordenarTempoOrdemCrescente(lista):
    var_elemento = lista[0]
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            if lista[j].tempo_execucao > lista[j + 1].tempo_execucao:
                var_elemento = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = var_elemento
    
    return lista

def maiorID(lista):
    maior = 0
    for i in range(len(lista) - 1):
        if lista[i].pid > maior:
            maior = lista[i].pid
    return maior

def imprimir_lista(lista):
    for i in range(len(lista)):
        lista[i].tempo_execucao = round(lista[i].tempo_execucao,2)
        print(lista[i])

def shortestJob(lista_processos):
    contador = 1
    maior = 0
    while len(lista_processos) > 0:
        print("Nova Execução")
        ordenarTempoOrdemCrescente(lista_processos)
        imprimir_lista(lista_processos)
        lista_processos[0].tempo_execucao -= 1
        # Gerar mais um processo em 15% das vezes, ou seja, temos 15% de probabilidades de termos um processo adicionado
        num = random.randint(1, 100)
        if num <= 15:
            config = {
                'chegada': 'exponential',
                'lambda': 0.5,
                'execucao': 'normal',
                'media': 10,
                'desvio': 2,
                'prioridade': 'uniforme'
            }

            maior = maiorID(lista_processos) + 1
            processo = gerar_processos(1,config,maior)
            lista_processos.append(processo[0])
            print("Processo com o id "+str(maior)+" adicionado com sucesso") 

        if lista_processos[0].tempo_execucao <= 0:
            tempo_a_mais = neg(lista_processos[0].tempo_execucao)
            lista_processos[1].tempo_execucao -= tempo_a_mais
            print("Processo com o id "+str(lista_processos[0].pid)+" concluido com sucesso!")
            lista_processos.pop(0)
        
        time.sleep(1)

    
def ordenarPorPrioridade(lista):
    var_elemento = lista[0]
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            if lista[j].prioridade > lista[j + 1].prioridade:
                var_elemento = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = var_elemento
    return lista

# Preemptivo que para um processo se chegar um com nível de prioridade inferior/superior(dependendo da implementação), neste caso é inferior
def Priority_Scheduling_Preemptivo(lista_processos):
    contador = 1
    i = -1
    while len(lista_processos) > 0:
        print("Nova Execução")
        ordenarPorPrioridade(lista_processos)
        imprimir_lista(lista_processos)
        lista_processos[0].tempo_execucao -= 1
        num = random.randint(1, 100)
        if num <= 15:
            config = {
                'chegada': 'exponential',
                'lambda': 0.5,
                'execucao': 'normal',
                'media': 10,
                'desvio': 2,
                'prioridade': 'uniforme'
            }

            maior = maiorID(lista_processos) + 1
            processo = gerar_processos(1,config,maior)
            processo[0].prioridade = 1
            lista_processos.append(processo[0])
            print("Processo com o id "+str(maior)+" adicionado com sucesso") 

        if lista_processos[0].tempo_execucao <= 0:
            tempo_a_mais = neg(lista_processos[0].tempo_execucao)
            lista_processos[1].tempo_execucao -= tempo_a_mais
            print("Processo com o ID "+str(lista_processos[0].pid)+" eliminado com sucesso")
            lista_processos.pop(0)
        time.sleep(1)



def Priority_Scheduling_Non_Preemptivo(lista_processos):
    contador = 1
    guardarElementoAtual = lista_processos[0]
    maior = 0
    i = -1
    ordenarPorPrioridade(lista_processos)
    while len(lista_processos) > 0:
        print("Nova Execução")
        maior = maiorID(lista_processos)
        guardarElementoAtual = lista_processos[0]
        lista_processos.pop(0)
        ordenarPorPrioridade(lista_processos)
        lista_processos.insert(0,guardarElementoAtual)
        imprimir_lista(lista_processos)
        lista_processos[0].tempo_execucao -= 1
        num = random.randint(1, 100)
        if num <= 15:
            config = {
                'chegada': 'exponential',
                'lambda': 0.5,
                'execucao': 'normal',
                'media': 10,
                'desvio': 2,
                'prioridade': 'uniforme'
            }

            maior = maiorID(lista_processos) + 1
            processo = gerar_processos(1,config,maior)
            processo[0].prioridade = 1
            lista_processos.append(processo[0])
            print("Processo com o id "+str(maior)+" adicionado com sucesso")

        if lista_processos[0].tempo_execucao <= 0:
            tempo_a_mais = neg(lista_processos[0].tempo_execucao)
            lista_processos[1].tempo_execucao -= tempo_a_mais
            print("Processo com o ID "+str(lista_processos[0].pid)+" eliminado com sucesso")
            lista_processos.pop(0)
        time.sleep(1)