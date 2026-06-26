from view.interface import JanelaPrincipal
from service.tarefa_service import TarefaService
import tkinter as tk

root = tk.Tk()
service = TarefaService()
janela = JanelaPrincipal(root, service)
root.mainloop()
