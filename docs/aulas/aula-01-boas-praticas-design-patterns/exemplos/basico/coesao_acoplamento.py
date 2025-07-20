"""
Exemplo de alta coesão e baixo acoplamento
Cada classe tem uma única responsabilidade e depende de abstrações.
"""
from typing import List

class Calculadora:
    def somar(self, valores: List[float]) -> float:
        return sum(valores)

class Impressora:
    def imprimir(self, mensagem: str) -> None:
        print(mensagem)

class Relatorio:
    def __init__(self, calculadora: Calculadora, impressora: Impressora) -> None:
        self.calculadora = calculadora
        self.impressora = impressora

    def gerar(self, valores: List[float]) -> None:
        total = self.calculadora.somar(valores)
        self.impressora.imprimir(f"Total: {total}")

# BENEFÍCIO: Classes podem ser reutilizadas e testadas separadamente, facilitando manutenção e evolução.
