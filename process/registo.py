class Registo:
    def __init__(self):
        self.linhas = []  # Lista de logs

    def registar(self, tempo, mensagem):
        self.linhas.append((tempo, mensagem))  # Registra a mensagem com o tempo

    def mostrar(self):
        for tempo, mensagem in sorted(self.linhas):
            print(f"[{tempo}] {mensagem}")  # Exibe os logs ordenados por tempo

