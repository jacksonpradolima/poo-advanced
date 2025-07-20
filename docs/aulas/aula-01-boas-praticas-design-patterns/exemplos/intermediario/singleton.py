"""
Exemplo do padrão Singleton
Garante que apenas uma instância da classe seja criada.
"""
class Configuracao:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        self.parametro = 'valor'

# USO:
config1 = Configuracao()
config2 = Configuracao()
print(config1 is config2)  # True

# BENEFÍCIO: Útil para gerenciar configurações globais ou recursos compartilhados.
