"""
Exemplo do padrão Observer
Permite que objetos sejam notificados sobre mudanças em outros objetos.
"""
from typing import List, Protocol

class Observador(Protocol):
    def atualizar(self, mensagem: str) -> None:
        ...

class Sujeito:
    def __init__(self) -> None:
        self.observadores: List[Observador] = []

    def adicionar(self, observador: Observador) -> None:
        self.observadores.append(observador)

    def notificar(self, mensagem: str) -> None:
        for obs in self.observadores:
            obs.atualizar(mensagem)

class ObservadorConcreto:
    def atualizar(self, mensagem: str) -> None:
        print(f"Recebido: {mensagem}")

# USO:
sujeito = Sujeito()
obs1 = ObservadorConcreto()
sujeito.adicionar(obs1)
sujeito.notificar("Mudança de estado!")

# BENEFÍCIO: Facilita comunicação entre objetos sem acoplamento direto.
