"""
Exemplo DEPOIS: Aplicação do Princípio da Responsabilidade Única (SRP)
Cada classe tem uma responsabilidade clara: cálculo, persistência ou apresentação.
Facilita manutenção, testes e evolução.
"""
from typing import List, Dict

class CalculadoraRelatorio:
    """
    Responsável apenas pelo cálculo do total.
    """
    def calcular_total(self, dados: List[Dict]) -> float:
        return sum(item['valor'] for item in dados)

class PersistenciaRelatorio:
    """
    Responsável apenas por salvar os dados em arquivo.
    """
    def salvar_em_arquivo(self, dados: List[Dict], caminho: str) -> None:
        with open(caminho, 'w') as f:
            for item in dados:
                f.write(f"{item['nome']}: {item['valor']}\n")

class ApresentacaoRelatorio:
    """
    Responsável apenas por exibir os dados.
    """
    def exibir(self, dados: List[Dict], total: float) -> None:
        print("Relatório:")
        for item in dados:
            print(f"{item['nome']}: {item['valor']}")
        print(f"Total: {total}")

# BENEFÍCIO: Cada classe pode ser testada e evoluída separadamente, facilitando manutenção e extensão.
