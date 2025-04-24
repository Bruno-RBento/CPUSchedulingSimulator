from process.pcb import Processo
from process.registo import Registo

def exemplo_estatico():
    registo = Registo()
    lista_processos = [(1, 2), (2, 3), (3, 2), (4, 2)]
    processos = []

    tempo_chegada = 0
    for pid, tempo_execucao in lista_processos:
        processo = Processo(pid, tempo_chegada, tempo_execucao, prioridade=1)  # prioridade fixa
        processos.append(processo)
        registo.registar(tempo_chegada, f"Processo {pid} criado com burst {tempo_execucao}")
        tempo_chegada += 1  # Pode ajustar se quiser todos no mesmo instante

    registo.mostrar()

if __name__ == "__main__":
    exemplo_estatico()

