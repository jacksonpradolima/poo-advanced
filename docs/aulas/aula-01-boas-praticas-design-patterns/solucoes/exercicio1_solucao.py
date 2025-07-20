"""
Solução do Exercício 1: Refatoração para SRP
"""
from typing import List, Dict

class CalculadoraRelatorio:
    def calcular_total(self, dados: List[Dict]) -> float:
        return sum(item['valor'] for item in dados)

class PersistenciaRelatorio:
    def salvar_em_arquivo(self, dados: List[Dict], caminho: str) -> None:
        with open(caminho, 'w') as f:
            for item in dados:
                f.write(f"{item['nome']}: {item['valor']}\n")

class ApresentacaoRelatorio:
    def exibir(self, dados: List[Dict], total: float) -> None:
        print("Relatório:")
        for item in dados:
            print(f"{item['nome']}: {item['valor']}")
        print(f"Total: {total}")

# Cada classe tem uma responsabilidade única, facilitando manutenção e testes.
