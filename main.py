from model.tarefa import Prioridade
from service.tarefa_service import TarefaService

service = TarefaService()

resultado = service.criar_tarefa(
    titulo="Estudar Python",
    descricao="Revisar o projeto TaskFlow",
    prioridade=Prioridade.ALTA,
    prazo="2026-12-31"
)

print(resultado)
