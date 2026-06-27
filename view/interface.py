import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


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


    def botao_criar_tarefa(self):
        JanelaFormulario(self.root, self.service, self._carregar_tarefas)
    def botao_editar_tarefa(self):
        pass

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
        pass


    def _carregar_tarefas(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        tarefas = self.service.listar_tarefas()

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