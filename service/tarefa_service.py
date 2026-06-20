import datetime
from model.tarefa import Tarefa, Prioridade
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

        self.repo.salvar(tarefa=Tarefa(titulo, descricao, prioridade, prazo))
