"""
Exemplo do padrão Strategy
Permite selecionar algoritmos em tempo de execução, promovendo flexibilidade e baixo acoplamento.
"""
from typing import Protocol, List

class EstrategiaCalculo(Protocol):
    def calcular(self, valores: List[float]) -> float:
        ...

class SomaEstrategia:
    def calcular(self, valores: List[float]) -> float:
        return sum(valores)

class MediaEstrategia:
    def calcular(self, valores: List[float]) -> float:
        return sum(valores) / len(valores) if valores else 0.0

class ContextoCalculo:
    def __init__(self, estrategia: EstrategiaCalculo) -> None:
        self.estrategia = estrategia

    def executar(self, valores: List[float]) -> float:
        return self.estrategia.calcular(valores)

# USO:
valores = [10, 20, 30]
contexto = ContextoCalculo(SomaEstrategia())
print(f"Soma: {contexto.executar(valores)}")
contexto.estrategia = MediaEstrategia()
print(f"Média: {contexto.executar(valores)}")

# BENEFÍCIO: Permite trocar algoritmos sem alterar o contexto, facilitando extensão e testes.
