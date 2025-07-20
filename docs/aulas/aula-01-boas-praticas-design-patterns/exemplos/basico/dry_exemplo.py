"""
Exemplo de aplicação do princípio DRY (Don't Repeat Yourself)
Evite duplicação de lógica, centralizando o cálculo em uma função reutilizável.
"""
from typing import List, Dict

def calcular_total(dados: List[Dict]) -> float:
    """
    Calcula o total dos valores presentes na lista de dados.
    """
    return sum(item['valor'] for item in dados)

# Uso correto:
dados = [
    {'nome': 'Produto A', 'valor': 10.0},
    {'nome': 'Produto B', 'valor': 20.0}
]
print(f"Total: {calcular_total(dados)}")

# ERRO COMUM: Repetir o cálculo em vários lugares do código, dificultando manutenção.
