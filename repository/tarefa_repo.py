import json

from model.tarefa import Tarefa


class TarefaRepo:
    def __init__(self):
        self.arquivo = "tarefa.json"

    def __carregar(self):
        try:
            with open(self.arquivo, "r" ) as arq:
                return json.load(arq)
        except FileNotFoundError:
                return {}

    def __salvar(self, dicionario):
            with open(self.arquivo, "w") as arq:
                json.dump(dicionario, arq)
    def salvar(self, tarefa):
        dados = self.__carregar()
        tarefa_dict = tarefa.to_dict()
        dados[tarefa.id] = tarefa_dict
        self.__salvar(dados)
        return dados
    def buscar_todos(self):
        dados = self.__carregar()
        trfs = []
        for tarefa_dict in dados.values():
            trf = Tarefa.from_dict(tarefa_dict)
            trfs.append(trf)
        return trfs

    def buscar_por_id(self, id_tarefa):
        dados = self.__carregar()
        tarefa_dict = dados.get(id_tarefa)
        if tarefa_dict:
            return Tarefa.from_dict(tarefa_dict)
        else:
            return None

    def atualizar(self, dicionario):
        dados = self.__carregar()
        dados[dicionario.id] = dicionario.to_dict()
        self.__salvar(dados)

    def deletar(self, id_tarefa):
        dados = self.__carregar()
        tarefa_dict = dados.get(id_tarefa)
        if tarefa_dict:
            dados.pop(id_tarefa)
            self.__salvar(dados)
            return True
        else:
            return False