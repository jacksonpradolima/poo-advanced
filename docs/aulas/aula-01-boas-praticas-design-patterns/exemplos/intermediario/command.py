"""
Exemplo do padrão Command
Encapsula uma solicitação como um objeto, permitindo parametrização e histórico de comandos.
"""
from typing import Protocol

class Comando(Protocol):
    def executar(self) -> None:
        ...

class ComandoImprimir:
    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
    def executar(self) -> None:
        print(self.mensagem)

class Invocador:
    def __init__(self) -> None:
        self.historico = []
    def executar_comando(self, comando: Comando) -> None:
        comando.executar()
        self.historico.append(comando)

# USO:
cmd = ComandoImprimir("Olá, mundo!")
invocador = Invocador()
invocador.executar_comando(cmd)

# BENEFÍCIO: Permite desfazer/refazer operações e implementar filas de comandos.
