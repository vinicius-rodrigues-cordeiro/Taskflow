import tkinter as tk
from enum import Enum
from tkinter import ttk

from model import tarefa
from model.tarefa import Tarefa


class JanelaPrincipal:
    def __init__(self, root, service):
        self.service = service
        self.root = root
        self.root.title('Janela Principal')
        self.root.resizable(width=True, height=True)
        self.root.geometry('550x550')
        self.root.minsize(250, 250)
        self.root.maxsize(750, 750)
        self._construir_layout()


    def _construir_layout(self):

        self.janela = tk.Frame(self.root, bg='white')
        self.janela.pack(fill='both', expand=True)

        self.sidebar = tk.Frame(self.janela, bg='gray', width=150)
        self.sidebar.pack(side='left', fill='y')

        self.conteudo = tk.Frame(self.janela, bg='white', width=500)
        self.conteudo.pack(side='right', fill='both', expand=True)

        self.tabela = ttk.Treeview(self.conteudo, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5'), show='headings')
        self.tabela.heading('Col1', text='Data de criação')
        self.tabela.column('Col1', width=100)
        self.tabela.heading('Col2', text='Titulo')
        self.tabela.column('Col2', width=100)
        self.tabela.heading('Col3', text='Prioridade')
        self.tabela.column('Col3', width=100)
        self.tabela.heading('Col4', text='Prazo')
        self.tabela.column('Col4', width=100)
        self.tabela.heading('Col5', text='Status')
        self.tabela.column('Col5', width=100)
        self._carregar_tarefas()
        self.tabela.pack(fill='both', expand=True)

        self.btn_criar = tk.Button(self.sidebar, text="Criar", command=self.botao_criar_tarefa)
        self.btn_criar.pack(side='top', fill='x')

        self.btn_editar = tk.Button(self.sidebar, text="Editar", command=self.botao_editar_tarefa)
        self.btn_editar.pack(side='top', fill='x')

        self.btn_excluir = tk.Button(self.sidebar, text="Excluir", command=self.botao_excluir_tarefa)
        self.btn_excluir.pack(side='top', fill='x')

        self.btn_ver = tk.Button(self.sidebar, text="Ver", command=self.botao_ver_tarefa)
        self.btn_ver.pack(side='top', fill='x')

        self.rodape = tk.Frame(self.conteudo, bg='white')
        self.rodape.pack(side='bottom', fill='x')

        self.btn_cancelar = tk.Button(self.rodape, text="Cancelar", command=self.botao_cancelar_tarefa)
        self.btn_cancelar.pack(side='left', fill='x')

        self.btn_salvar = tk.Button(self.rodape, text="Salvar", command=self.botao_salvar_tarefa)
        self.btn_salvar.pack(side='right', fill='x')


    def botao_criar_tarefa(self):
        print("Criando tarefa")
    def botao_editar_tarefa(self):
        print("Editar tarefa")
    def botao_excluir_tarefa(self):
        print("Excluir tarefa")
    def botao_ver_tarefa(self):
        print("Ver tarefa")
    def botao_salvar_tarefa(self):
        print("Salvar tarefa")
    def botao_cancelar_tarefa(self):
        print("Cancelar tarefa")

    def _carregar_tarefas(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        tarefas = self.service.listar_tarefas()
        for t in tarefas:
            self.tabela.insert(
                '',
                'end',
                values=(t.criado_em,
                        t.titulo,
                        t.prioridade.value,
                        t.prazo,
                        t.status.value)
            )