"""
Estudo de caso: Refatoração de sistema legado com code smells
Antes: Classe monolítica, acoplamento alto, duplicação de código
Depois: Aplicação de SOLID, DRY, padrões Strategy e Observer
"""
# ANTES
class SistemaLegado:
    def __init__(self):
        self.dados = []
    def adicionar(self, valor):
        self.dados.append(valor)
    def calcular(self):
        total = 0
        for v in self.dados:
            total += v
        return total
    def imprimir(self):
        print("Dados:", self.dados)
        print("Total:", self.calcular())

# DEPOIS
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

# USO:
sistema = SistemaNovo(SomaEstrategia())
log = ObservadorLog()
sistema.adicionar_observador(log)
sistema.adicionar(10)
sistema.adicionar(20)
sistema.imprimir()

# BENEFÍCIO: Código modular, testável, extensível e com baixo acoplamento.
