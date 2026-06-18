from enum import Enum
import datetime
import uuid

class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"


class Status(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluida"
    CANCELADA = "Cancelada"

class Tarefa:
    def __init__(self, titulo, descricao, prioridade, prazo):
        self.__id = uuid.uuid4()
        self.__titulo = titulo
        self.__descricao = descricao
        self.__prioridade = prioridade
        self.__status = Status.PENDENTE
        self.__prazo = prazo
        self.__criado_em = datetime.datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        self.__titulo = novo_titulo

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, nova_descricao):
        self.__descricao = nova_descricao

    @property
    def prazo(self):
        return self.__prazo

    @prazo.setter
    def prazo(self, novo_prazo):
        self.__prazo = novo_prazo

    @property
    def criado_em(self):
        return self.__criado_em

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        self.__status = novo_status

    @property
    def prioridade(self):
        return self.__prioridade

    @property
    def tarefa_concluida(self):
        return self.__status == Status.CONCLUIDA
