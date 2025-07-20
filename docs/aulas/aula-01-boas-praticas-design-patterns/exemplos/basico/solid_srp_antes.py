"""
Exemplo ANTES: Violação do Princípio da Responsabilidade Única (SRP)
Esta classe mistura lógica de cálculo, persistência e apresentação, dificultando manutenção e testes.
"""

class RelatorioFinanceiro:
    def __init__(self, dados):
        self.dados = dados

    def calcular_total(self):
        total = 0
        for item in self.dados:
            total += item['valor']
        return total

    def salvar_em_arquivo(self, caminho):
        with open(caminho, 'w') as f:
            for item in self.dados:
                f.write(f"{item['nome']}: {item['valor']}\n")

    def exibir(self):
        print("Relatório:")
        for item in self.dados:
            print(f"{item['nome']}: {item['valor']}")
        print(f"Total: {self.calcular_total()}")

# ERRO COMUM: Misturar responsabilidades em uma única classe dificulta manutenção, testes e evolução do sistema.
