from enum import Enum
import datetime
import uuid


class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA= "Media"
    ALTA = "Alta"


class Status(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluida"
    CANCELADA = "Cancelada"

class Tarefa:
    def __init__(self, titulo, descricao, prioridade, prazo, status=None, id_tarefa=None, criado_em=None):
        self.__id_tarefa = id_tarefa if id_tarefa is not None else uuid.uuid4()
        self.__titulo = titulo
        self.__descricao = descricao
        self.__prioridade = prioridade
        self.__status = status if status is not None else Status.PENDENTE
        self.__prazo = prazo
        self.__criado_em = criado_em if criado_em is not None else datetime.datetime.now()

    @property
    def id(self):
        return self.__id_tarefa

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

    @prioridade.setter
    def prioridade(self, nova_prioridade):
        self.__prioridade = nova_prioridade

    @property
    def tarefa_concluida(self):
        return self.__status == Status.CONCLUIDA

    def to_dict(self):
        return {
            "id_tarefa": str(self.__id_tarefa),
            "titulo": self.__titulo,
            "descricao": self.__descricao,
            "prioridade": self.__prioridade.value,
            "status": self.__status.value,
            "prazo": self.__prazo.isoformat(),
            "criado_em": self.__criado_em.isoformat(),

        }


    @classmethod
    def from_dict(cls, dicionario):
        return cls(
            id_tarefa=dicionario["id_tarefa"],
            titulo=dicionario["titulo"],
            descricao=dicionario["descricao"],
            prioridade=Prioridade(dicionario["prioridade"]),
            status=Status(dicionario["status"]),
            prazo=datetime.datetime.fromisoformat(dicionario["prazo"]),
            criado_em=datetime.datetime.fromisoformat(dicionario["criado_em"]),
        )