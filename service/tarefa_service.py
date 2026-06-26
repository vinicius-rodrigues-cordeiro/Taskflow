import datetime

from model.tarefa import Tarefa, Prioridade, Status
from repository.tarefa_repo import TarefaRepo

class TarefaService:
    def __init__(self):
        self.repo = TarefaRepo()

    def criar_tarefa(self, titulo, prioridade, prazo, descricao):
        if titulo is None or titulo.strip() == "":
            raise ValueError("Titulo não pode ficar vazio")

        if prioridade is None:
            prioridade = Prioridade.MEDIA

        try:
            prazo = datetime.datetime.fromisoformat(prazo)
        except ValueError:
            raise ValueError("Formato de prazo invalido. Use AAAA-MM-DD")

        if prazo is None or prazo <= datetime.datetime.now():
                raise ValueError("Prazo deve ser uma data futura")

        return self.repo.salvar(tarefa=Tarefa(titulo, descricao, prioridade, prazo))

    def atualizar_tarefa(self, id_tarefa, titulo, prioridade, prazo, descricao):
        t = self.repo.buscar_por_id(id_tarefa)

        if t is None:
            raise Exception("Não existe uma tarefa com esse ID")
        else:
            if titulo is not None:
                t.titulo = titulo
            if prioridade is not None:
                t.prioridade = Prioridade(prioridade)

            if prazo is not None:
                try:
                    t.prazo = datetime.datetime.fromisoformat(prazo)
                except ValueError:
                    raise ValueError("Formato de prazo invalido. Use AAAA-MM-DD")

                if t.prazo <= datetime.datetime.now():
                    raise ValueError("Prazo deve ser uma data futura")

            if descricao is not None:
                t.descricao = descricao

            self.repo.atualizar(t)

    def atualizar_status(self, id_tarefa, novo_status, confirmacao=False):
        s = self.repo.buscar_por_id(id_tarefa)
        if s is None:
            raise Exception("Esse ID não existe")
        elif novo_status == Status.EM_ANDAMENTO and s.status == Status.CONCLUIDA:
            if confirmacao:
                s.status = novo_status
                self.repo.atualizar(s)
            else:
                raise Exception("O status não foi atualizado!")
        else:
            s.status = novo_status
            self.repo.atualizar(s)

    def listar_tarefas(self):
        tarefas = self.repo.buscar_todos()
        t = []
        for tarefa in tarefas:
            if tarefa.status != Status.CANCELADA:
                t.append(tarefa)
        return t




    def listar_canceladas(self):
        tarefas = self.repo.buscar_todos()
        t = []
        for tarefa in tarefas:
            if tarefa.status == Status.CANCELADA:
                t.append(tarefa)
        return t


    def deletar_tarefa(self, id_tarefa, confirmacao=False):
        d = self.repo.buscar_por_id(id_tarefa)
        if d is None:
            raise Exception("O ID não existe")
        elif d.status == Status.EM_ANDAMENTO:
            if confirmacao:
                self.repo.deletar(id_tarefa)
            else:
                raise Exception("A tarefa não foi deletada")
        else:
            self.repo.deletar(id_tarefa)

