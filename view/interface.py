import tkinter as tk
from enum import Enum
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from model import tarefa
from model.tarefa import Status, Tarefa


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

        self.sidebar = tk.Frame(self.janela, bg='white', width=150)
        self.sidebar.pack(side='left', fill='y')

        self.area_direita = tk.Frame(self.janela, bg='white', width=150)
        self.area_direita.pack(side='right', fill='both', expand=True)

        self.header = tk.Frame(self.area_direita, bg='white', width=150)
        self.header.pack(side='top', fill='x')

        self.conteudo = tk.Frame(self.area_direita, bg='white', width=500)
        self.conteudo.pack(side='right', fill='both', expand=True)

        # Label e Combobox de Status
        tk.Label(self.header, text="Status:").pack(side='left', padx=5)
        self.combo_status = ttk.Combobox(self.header,
                                         values=["Todos",
                                                 "Pendente",
                                                 "Em andamento",
                                                 "Concluida",
                                                 "Cancelada"],
                                         width=15)
        self.combo_status.current(0)
        self.combo_status.pack(side='left', padx=5)
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self._filtrar_tarefas())

        # Label e Combobox de Prioridade
        tk.Label(self.header, text="Prioridade:").pack(side='left', padx=5)
        self.combo_prioridade = ttk.Combobox(self.header,
                                             values=["Todas",
                                                     "Baixa",
                                                     "Media",
                                                     "Alta"],
                                             width=15)
        self.combo_prioridade.current(0)
        self.combo_prioridade.pack(side='left', padx=5)
        self.combo_prioridade.bind("<<ComboboxSelected>>", lambda e: self._filtrar_tarefas())

        self.tabela = ttk.Treeview(self.conteudo, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5'), show='headings')
        self.tabela.heading('Col1', text='Data de criação', command= lambda: self._ordenar_colunas('Col1'))
        self.tabela.column('Col1', width=100)
        self.tabela.heading('Col2', text='Titulo', command= lambda: self._ordenar_colunas('Col2'))
        self.tabela.column('Col2', width=100)
        self.tabela.heading('Col3', text='Prioridade', command= lambda: self._ordenar_colunas('Col3'))
        self.tabela.column('Col3', width=100)
        self.tabela.heading('Col4', text='Prazo', command= lambda: self._ordenar_colunas('Col4'))
        self.tabela.column('Col4', width=100)
        self.tabela.heading('Col5', text='Status', command= lambda: self._ordenar_colunas('Col5'))
        self.tabela.column('Col5', width=100)
        self._carregar_tarefas()
        self.tabela.pack(fill='both', expand=True)

        self.btn_criar = tk.Button(self.sidebar, text="Criar", command=self.botao_criar_tarefa)
        self.btn_criar.pack(side='top', fill='x')

        self.btn_editar = tk.Button(self.sidebar, text="Editar", command=self.botao_editar_tarefa)
        self.btn_editar.pack(side='top', fill='x')

        self.btn_excluir = tk.Button(self.sidebar, text="Excluir", command=self.botao_excluir_tarefa)
        self.btn_excluir.pack(side='top', fill='x')

        self.btn_ver_detalhes = tk.Button(self.sidebar, text="Ver", command=self.botao_ver_tarefa)
        self.btn_ver_detalhes.pack(side='top', fill='x')

        self.btn_ver_canceladas = tk.Button(self.sidebar, text="Canceladas", command=self.botao_ver_tarefas_canceladas)
        self.btn_ver_canceladas.pack(side='top', fill='x')


    def _filtrar_tarefas(self):
        status = self.combo_status.get()
        status = None if status == "Todos" else status
        prioridade = self.combo_prioridade.get()
        prioridade = None if prioridade == "Todas" else prioridade
        tarefas = self.service.listar_com_filtro(status, prioridade)
        self._carregar_tarefas(tarefas)

    def _ordenar_colunas(self, coluna):
        ids_tarefas = self.tabela.get_children()
        tarefas = [self.service.buscar_por_id(id_tarefa) for id_tarefa in ids_tarefas]
        ordem_de_prioridade = {"Alta": 1, "Media": 2, "Baixa": 3}
        ordem_de_status = {"Pendente": 1, "Em andamento": 2, "Cancelada": 3, "Concluida": 4}

        if coluna == "Col1":
            tarefas.sort(key=lambda t: t.criado_em)
        elif coluna == "Col2":
            tarefas.sort(key=lambda t: t.titulo)
        elif coluna == "Col3":
            tarefas.sort(key=lambda t: ordem_de_prioridade[t.prioridade.value])
        elif coluna == 'Col4':
            tarefas.sort(key=lambda t: (t.prazo, ordem_de_prioridade[t.prioridade.value]))
        elif coluna == 'Col5':
            tarefas.sort(key=lambda t: ordem_de_status[t.status.value])

        self._carregar_tarefas(tarefas)


    def botao_criar_tarefa(self):
        JanelaFormulario(self.root, self.service, self._carregar_tarefas)

    def botao_editar_tarefa(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa primeiro.")
            return None

        self.id_tarefa = selecionado[0]
        tarefa = self.service.buscar_por_id(self.id_tarefa)
        JanelaEdicao(self.root, self.service, self._carregar_tarefas, tarefa)

    def botao_excluir_tarefa(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa primeiro.")
            return None

        self.id_tarefa = selecionado[0]
        self.confirmado = messagebox.askyesno("Confirmar", "Deseja excluir esta tarefa?")
        if self.confirmado:
            self.service.deletar_tarefa(self.id_tarefa, confirmacao=True)
            self._carregar_tarefas()
        return None

    def botao_ver_tarefa(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa primeiro.")
            return None
        self.id_tarefa = selecionado[0]
        tarefa = self.service.buscar_por_id(self.id_tarefa)
        JanelaDetalhes(self.root, self.service, tarefa)


    def botao_ver_tarefas_canceladas(self):
        JanelaCanceladas(self.root, self.service)

    def _carregar_tarefas(self, tarefas=None):
        if tarefas is None:
            tarefas = self.service.listar_tarefas()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for t in tarefas:
            self.tabela.insert(
                '',
                'end', iid=str(t.id),
                values=(t.criado_em,
                        t.titulo,
                        t.prioridade.value,
                        t.prazo,
                        t.status.value)
            )

class JanelaFormulario(tk.Toplevel):
    def __init__(self, parent, service, tarefas):
        super().__init__(parent)
        self.service = service
        self.ao_salvar = tarefas
        self.janela = tk.Frame(self, bg='white')
        self.title('Formulario para criação de tarefas')
        self.resizable(False, False)
        self.geometry('300x300')
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Titulo: ").pack(pady=5)
        self.entry_titulo = tk.Entry(self)
        self.entry_titulo.pack(pady=5)

        tk.Label(self, text="Descrição: ").pack(pady=5)
        self.entry_descricao = tk.Entry(self)
        self.entry_descricao.pack(pady=5)

        tk.Label(self, text="Prioridade: ").pack(pady=5)
        self.combo_box_prioridade = ttk.Combobox(self, values=["Baixa", "Media", "Alta"])
        self.combo_box_prioridade.current(1)
        self.combo_box_prioridade.pack(pady=5)

        tk.Label(self, text="Status: ").pack(pady=5)
        self.combo_box_status = ttk.Combobox(self, values=["Pendente"])
        self.combo_box_status.current(0)
        self.combo_box_status.pack(pady=5)

        self.prazo = DateEntry(
            self,
            width=25,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            locale="pt_BR",
            date_pattern="dd/mm/yyyy",
        )
        self.prazo.pack(pady=5)

        self.rodape = tk.Frame(self, bg='white')
        self.rodape.pack(side='bottom', fill='x')

        self.btn_cancelar = tk.Button(self.rodape, text="Cancelar", command=self.botao_cancelar_tarefa)
        self.btn_cancelar.pack(side='left', fill='x')

        self.btn_salvar = tk.Button(self.rodape, text="Salvar", command=self.botao_salvar_tarefa)
        self.btn_salvar.pack(side='right', fill='x')

    def botao_salvar_tarefa(self):
        titulo = self.entry_titulo.get()
        descricao = self.entry_descricao.get()
        prioridade = self.combo_box_prioridade.get()
        prazo = self.prazo.get_date().strftime("%Y-%m-%d")
        self.combo_box_status.get()
        self.service.criar_tarefa(titulo, prioridade, prazo, descricao)
        self.ao_salvar()
        self.destroy()



    def botao_cancelar_tarefa(self):
        self.destroy()

class JanelaEdicao(JanelaFormulario):
    def __init__(self, parent, service, ao_salvar, tarefa):
        super().__init__(parent, service, ao_salvar)
        self.tarefa = tarefa
        self.title('Formulario para edição de tarefas')
        self.service = service
        self.ao_salvar = ao_salvar

        self.entry_titulo.delete(0, tk.END)  # limpa
        self.entry_titulo.insert(0,self.tarefa.titulo)

        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0,self.tarefa.descricao)

        self.combo_box_prioridade.set(self.tarefa.prioridade.value)
        self.combo_box_status.set(self.tarefa.status.value)
        self.combo_box_status['values'] = ["Pendente", "Em andamento", "Concluida", "Cancelada"]

        self.prazo.set_date(self.tarefa.prazo)

        self.btn_salvar.config(command=self.botao_atualizar_tarefa)

    def botao_atualizar_tarefa(self):
        titulo = self.entry_titulo.get()
        descricao = self.entry_descricao.get()
        prioridade = self.combo_box_prioridade.get()
        prazo = self.prazo.get_date().strftime("%Y-%m-%d")
        novo_status = Status(self.combo_box_status.get())
        if self.tarefa.status == Status.CONCLUIDA and novo_status == Status.EM_ANDAMENTO:
            confirmado = messagebox.askyesno("Atenção!", "Você deseja reverter uma tarefa concluída para Em andamento?")
            if not confirmado:
                return None
            self.service.atualizar_status(str(self.tarefa.id), Status(novo_status), confirmacao=True)

        else:
            self.service.atualizar_status(str(self.tarefa.id), Status(novo_status))

        self.service.atualizar_tarefa(str(self.tarefa.id), titulo, prioridade, prazo, descricao)
        self.ao_salvar()
        self.destroy()

class JanelaDetalhes(tk.Toplevel):
    def __init__(self, parent, service, tarefa):
        super().__init__(parent)

        tk.Label(self, text=f'ID: {tarefa.id},').pack(pady=5)
        tk.Label(self, text=f'Data de criação: {tarefa.criado_em}').pack(pady=5)
        tk.Label(self, text=f'Titulo: {tarefa.titulo}').pack(pady=5)
        tk.Label(self, text=f'Descrição: {tarefa.descricao}').pack(pady=5)
        tk.Label(self, text=f'Prioridade: {tarefa.prioridade.value}').pack(pady=5)
        tk.Label(self, text=f'Status: {tarefa.status.value}').pack(pady=5)
        tk.Label(self, text=f'Prazo: {tarefa.prazo}').pack(pady=5)

        self.btn_fechar = tk.Button(self, text="Fechar", command=self.destroy)
        self.btn_fechar.pack(pady=10)

class JanelaCanceladas(tk.Toplevel):
    def __init__(self, parent, service):
        super().__init__(parent)

        self.service = service
        self.title('Tarefas Canceladas')
        self.geometry('600x400')
        self.transient(parent)
        self.grab_set()

        self.tabela = ttk.Treeview(self, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5'), show='headings')
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
        self._carregar_canceladas()
        self.tabela.pack(fill='both', expand=True)

        self.btn_ver_tarefa = tk.Button(self, text="Ver tarefa", command=self._botao_ver_tarefa)
        self.btn_ver_tarefa.pack(side='bottom', fill='x')

        self.btn_fechar = tk.Button(self, text="Fechar", command=self.destroy)
        self.btn_fechar.pack(pady=10)

    def _carregar_canceladas(self):
        tarefas = self.service.listar_canceladas()
        for t in tarefas:
            self.tabela.insert('', 'end', iid=str(t.id),
            values=(t.criado_em, t.titulo, t.prioridade.value, t.prazo, t.status.value))

    def _botao_ver_tarefa(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa primeiro.")
            return
        id_tarefa = selecionado[0]
        tarefa = self.service.buscar_por_id(id_tarefa)
        JanelaDetalhes(self, self.service, tarefa)
