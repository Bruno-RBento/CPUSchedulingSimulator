# Makefile para Simulador de Escalonamento de Processos

# Comando para o Python (caso uses 'python3' em vez de 'python', muda aqui)
PYTHON = python

# Nome do ficheiro principal da aplicação
MAIN = index.py

# Instalar dependências
install:
	pip install pillow plotly numpy

# Executar o simulador
run:
	$(PYTHON) $(MAIN)

# Limpar ficheiros temporários (opcional)
clean:
	rm -f *.png
	rm -f __pycache__/*
	rm -rf __pycache__

# Atalhos
all: install run
