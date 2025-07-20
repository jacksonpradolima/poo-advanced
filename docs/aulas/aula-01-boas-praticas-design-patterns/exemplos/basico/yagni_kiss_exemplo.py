"""
Exemplo de aplicação dos princípios YAGNI e KISS
Evite implementar funcionalidades desnecessárias e prefira soluções simples.
"""
from typing import List

def soma_lista(valores: List[float]) -> float:
    """
    Retorna a soma dos valores da lista.
    Simples, direto e suficiente para o objetivo.
    """
    return sum(valores)

# ERRO COMUM: Criar funções genéricas e complexas sem necessidade (YAGNI)
def soma_lista_com_opcoes(valores: List[float], modo: str = 'normal', arredondar: bool = False) -> float:
    # Função desnecessariamente complexa para o contexto
    resultado = sum(valores)
    if arredondar:
        resultado = round(resultado)
    # ... mais lógica desnecessária ...
    return resultado

# Prefira soluções simples e diretas (KISS):
print(soma_lista([1.5, 2.5, 3.0]))
