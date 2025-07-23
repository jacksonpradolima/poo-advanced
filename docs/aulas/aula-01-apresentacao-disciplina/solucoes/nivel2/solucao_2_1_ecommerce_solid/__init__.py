#!/usr/bin/env python3
"""
Sistema de E-commerce SOLID - Solução Completa do Exercício 2.1

CONTEXTO EDUCACIONAL: Este sistema demonstra a implementação prática de todos
os princípios SOLID em um projeto real de e-commerce, servindo como exemplo
abrangente de arquitetura de software bem estruturada.

PRINCÍPIOS SOLID DEMONSTRADOS:
✅ SRP (Single Responsibility Principle)
   - Cada classe tem uma responsabilidade específica e bem definida
   - Entidades, Value Objects, Serviços e Repositórios focados

✅ OCP (Open/Closed Principle)  
   - Sistema extensível através de interfaces e herança
   - Novas estratégias e tipos podem ser adicionados sem modificação

✅ LSP (Liskov Substitution Principle)
   - Subtipos respeitam contratos dos tipos base
   - Produtos, estratégias e implementações são substituíveis

✅ ISP (Interface Segregation Principle)
   - Interfaces pequenas e focadas em responsabilidades específicas
   - Clientes dependem apenas do que realmente usam

✅ DIP (Dependency Inversion Principle)
   - Módulos de alto nível não dependem de detalhes de implementação
   - Dependências injetadas através de abstrações

ARQUITETURA:
- Domain Layer: Entidades e Value Objects com regras de negócio
- Service Layer: Casos de uso e coordenação de operações
- Infrastructure Layer: Implementações concretas e adaptadores

PADRÕES DE DESIGN:
- Strategy: Descontos, pagamentos, frete
- Factory: Criação de produtos e infraestrutura  
- Observer: Eventos de domínio
- Repository: Abstração de persistência
- Adapter: Integração com sistemas externos

TECNOLOGIAS:
- Python 3.12+ com type hints
- Decimal para precisão monetária
- UUID para identificadores únicos
- Logging para rastreabilidade
- Unittest para testes abrangentes

ESTRUTURA DO PROJETO:
domain/
├── entities.py      # Entidades de negócio
└── value_objects.py # Objetos de valor

services/
└── __init__.py      # Serviços de aplicação

infrastructure/
└── __init__.py      # Implementações concretas

main.py              # Demonstração completa
test_sistema.py      # Suite de testes

INSTRUÇÕES DE USO:
1. Execute main.py para ver demonstração completa
2. Execute test_sistema.py para rodar testes
3. Analise o código para entender implementação dos princípios

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
VERSÃO: 1.0
LICENÇA: Educacional - Uso acadêmico
"""

# Metadados do pacote
__version__ = "1.0.0"
__author__ = "Prof. Jackson Antonio do Prado Lima"
__email__ = "jackson.lima@professor.edu.br"
__status__ = "Educational"

def obter_info_sistema() -> dict:
    """
    Retorna informações sobre o sistema e sua arquitetura.
    
    Returns:
        Dict com metadados do sistema, princípios implementados
        e estatísticas de componentes.
    """
    return {
        'nome': 'Sistema E-commerce SOLID',
        'versao': __version__,
        'autor': __author__,
        'descricao': 'Implementação educacional demonstrando princípios SOLID',
        
        'principios_solid': {
            'srp': 'Cada classe tem responsabilidade única',
            'ocp': 'Extensível sem modificação de código existente', 
            'lsp': 'Subtipos substituem tipos base corretamente',
            'isp': 'Interfaces segregadas por responsabilidade',
            'dip': 'Dependências invertidas via abstrações'
        },
        
        'padroes_design': [
            'Strategy (descontos, pagamentos)', 
            'Factory (criação de objetos)',
            'Observer (eventos de domínio)',
            'Repository (abstração de dados)',
            'Adapter (integração externa)',
            'Domain-Driven Design'
        ],
        
        'componentes': {
            'entidades': 6,  # Produto+subtipos, Cliente, Pedido, etc
            'value_objects': 8,  # Dinheiro, Endereco, etc
            'servicos': 4,  # Gestão produtos/clientes/pedidos/notificações
            'repositorios': 3,  # Produto, Cliente, Pedido
            'gateways': 3,  # Pagamento, Notificação, Frete
            'estrategias': 3  # Tipos de desconto
        },
        
        'arquitetura': {
            'camadas': ['Domain', 'Service', 'Infrastructure'],
            'padrao': 'Hexagonal Architecture',
            'inversao_dependencias': True,
            'testabilidade': 'Alta',
            'extensibilidade': 'Alta'
        }
    }


# Exemplo de uso rápido (para testes)
if __name__ == "__main__":
    import pprint
    
    print("🏪 SISTEMA E-COMMERCE SOLID")
    print("=" * 50)
    
    info = obter_info_sistema()
    pprint.pprint(info, width=70)
    
    print("
✅ Sistema carregado com sucesso!")
    print("   Execute main.py para demonstração completa")
    print("   Execute test_sistema.py para rodar testes")

# Importações para facilitar uso do pacote
from .domain.entities import *
from .domain.value_objects import *
from .services.interfaces import *
from .services.implementations import *
from .infrastructure.adapters import *
from .main import demonstrar_ecommerce_solid

__all__ = [
    # Domain
    'Produto', 'ProdutoFisico', 'ProdutoDigital', 'ProdutoServico',
    'Pedido', 'Cliente',
    
    # Value Objects
    'Dinheiro', 'Endereco', 'DimensoesProduto',
    
    # Services
    'CalculadoraFrete', 'ProcessadorPagamento', 'ServicoNotificacao',
    'FabricaProdutos', 'GerenciadorPedidos',
    
    # Infrastructure
    'AdaptadorPayPal', 'AdaptadorStripe', 'NotificacaoEmail', 'NotificacaoSMS',
    
    # Demo
    'demonstrar_ecommerce_solid'
]
