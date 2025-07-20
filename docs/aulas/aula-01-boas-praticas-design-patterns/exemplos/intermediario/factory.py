"""
Exemplo do padrão Factory
Centraliza a criação de objetos, facilitando manutenção e extensão.
"""
from typing import Any

class Produto:
    def __init__(self, nome: str) -> None:
        self.nome = nome

class ProdutoFactory:
    def criar_produto(self, tipo: str) -> Produto:
        if tipo == 'A':
            return Produto('Produto A')
        elif tipo == 'B':
            return Produto('Produto B')
        else:
            raise ValueError('Tipo desconhecido')

# USO:
factory = ProdutoFactory()
produto = factory.criar_produto('A')
print(produto.nome)

# BENEFÍCIO: Facilita a adição de novos tipos de produto sem alterar o código cliente.
