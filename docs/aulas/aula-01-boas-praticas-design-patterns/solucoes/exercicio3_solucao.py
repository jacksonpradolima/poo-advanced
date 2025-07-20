"""
Solução do Exercício 3: Refatoração avançada e Observer
"""
from typing import List, Protocol

class EstrategiaCalculo(Protocol):
    def calcular(self, dados: List[float]) -> float:
        ...

class SomaEstrategia:
    def calcular(self, dados: List[float]) -> float:
        return sum(dados)

class SistemaNovo:
    def __init__(self, estrategia: EstrategiaCalculo):
        self.dados: List[float] = []
        self.estrategia = estrategia
        self.observadores = []
    def adicionar(self, valor: float) -> None:
        self.dados.append(valor)
        self.notificar(f"Valor {valor} adicionado.")
    def calcular(self) -> float:
        return self.estrategia.calcular(self.dados)
    def imprimir(self) -> None:
        print("Dados:", self.dados)
        print("Total:", self.calcular())
    def adicionar_observador(self, obs):
        self.observadores.append(obs)
    def notificar(self, mensagem: str) -> None:
        for obs in self.observadores:
            obs.atualizar(mensagem)

class ObservadorLog:
    def atualizar(self, mensagem: str) -> None:
        print(f"LOG: {mensagem}")

# Uso:
sistema = SistemaNovo(SomaEstrategia())
log = ObservadorLog()
sistema.adicionar_observador(log)
sistema.adicionar(10)
sistema.adicionar(20)
sistema.imprimir()
