"""
Exemplo do padrão Adapter
Permite que interfaces incompatíveis trabalhem juntas.
"""
class SistemaAntigo:
    def processar(self, dados: str) -> str:
        return dados.upper()

class SistemaNovo:
    def executar(self, dados: str) -> str:
        return dados.lower()

class Adapter:
    def __init__(self, sistema_novo: SistemaNovo) -> None:
        self.sistema_novo = sistema_novo

    def processar(self, dados: str) -> str:
        # Adapta a interface do sistema novo para o antigo
        return self.sistema_novo.executar(dados)

# USO:
sistema_antigo = SistemaAntigo()
sistema_novo = SistemaNovo()
adapter = Adapter(sistema_novo)
print(sistema_antigo.processar("Teste"))  # TESTE
print(adapter.processar("Teste"))         # teste

# BENEFÍCIO: Permite integração de sistemas legados com novos componentes.
