# 🔵 Exercícios Nível 1 - Básico

## Exercício 1.1: Calculadora de Impostos 📊

### Contexto
Você foi contratado para criar uma biblioteca simples de cálculo de impostos para uma pequena empresa. O sistema deve calcular diferentes tipos de impostos sobre vendas e estar totalmente configurado com ambiente profissional.

### Objetivos Pedagógicos
- Aplicar configuração de ambiente virtual
- Praticar tipagem estática com mypy
- Implementar testes unitários básicos
- Configurar linting com ruff

### Requisitos Funcionais
1. **Função `calcular_icms`**: Calcula ICMS (18%) sobre valor da venda
2. **Função `calcular_iss`**: Calcula ISS (5%) sobre valor do serviço  
3. **Função `calcular_pis_cofins`**: Calcula PIS (1.65%) + COFINS (7.6%)
4. **Função `total_impostos`**: Soma todos os impostos de uma venda

### Requisitos Técnicos
- Python 3.12+
- Tipagem completa com type hints
- Validação de valores negativos
- Tratamento de casos especiais (valor zero)
- Precisão decimal adequada para cálculos financeiros

### Estrutura Esperada
```
calculadora-impostos/
├── pyproject.toml
├── README.md
├── .gitignore
├── .pre-commit-config.yaml
├── calculadora/
│   ├── __init__.py
│   └── impostos.py
└── tests/
    ├── __init__.py
    └── test_impostos.py
```

### Código Base

```python
# calculadora/impostos.py
from decimal import Decimal
from typing import Union

Numero = Union[int, float, Decimal]

def calcular_icms(valor_venda: Numero) -> Decimal:
    """
    Calcula o ICMS (18%) sobre o valor da venda.
    
    Args:
        valor_venda: Valor base para cálculo do ICMS
        
    Returns:
        Valor do ICMS calculado
        
    Raises:
        ValueError: Se valor_venda for negativo
        
    Example:
        >>> calcular_icms(100)
        Decimal('18.00')
    """
    # IMPLEMENTAR: Sua lógica aqui
    pass

# IMPLEMENTAR: As outras funções seguindo o mesmo padrão
```

### Casos de Teste Obrigatórios
```python
# tests/test_impostos.py
import pytest
from decimal import Decimal
from calculadora.impostos import calcular_icms, calcular_iss, calcular_pis_cofins, total_impostos

def test_calcular_icms_valor_positivo():
    """Testa cálculo de ICMS com valor válido."""
    # IMPLEMENTAR: Teste com valor 100, esperado 18.00
    pass

def test_calcular_icms_valor_zero():
    """Testa cálculo de ICMS com valor zero."""
    # IMPLEMENTAR: Teste com valor 0, esperado 0.00
    pass

def test_calcular_icms_valor_negativo():
    """Testa se ValueError é lançada para valor negativo."""
    # IMPLEMENTAR: Teste que verifica se exceção é lançada
    pass

# IMPLEMENTAR: Testes para as outras funções
```

### Critérios de Avaliação
- [ ] Ambiente virtual configurado e documentado
- [ ] pyproject.toml completo com dependências corretas
- [ ] Todas as funções implementadas e tipadas
- [ ] Tratamento adequado de erros
- [ ] Cobertura de testes >= 90%
- [ ] Código passa em ruff check e mypy
- [ ] Pre-commit configurado e funcionando
- [ ] README.md com instruções claras

### Dicas de Implementação
1. Use `Decimal` para cálculos financeiros precisos
2. Valide entradas antes de calcular
3. Documente casos especiais nos docstrings
4. Teste casos limites (zero, valores muito grandes)

### Extensões Opcionais
- Adicionar função para calcular impostos por região
- Implementar formatação monetária brasileira
- Criar CLI simples com typer

---

## Exercício 1.2: Validador de CPF 🆔

### Contexto
Crie uma biblioteca para validação de CPF seguindo as regras oficiais da Receita Federal. Este é um componente comum em sistemas brasileiros e deve ser robusto e bem testado.

### Objetivos Pedagógicos
- Praticar algoritmos de validação
- Implementar testes com dados reais
- Trabalhar com formatação de strings
- Aplicar tratamento de exceções

### Requisitos Funcionais
1. **Função `validar_cpf`**: Valida CPF usando algoritmo oficial
2. **Função `formatar_cpf`**: Formata CPF no padrão XXX.XXX.XXX-XX
3. **Função `limpar_cpf`**: Remove formatação e caracteres especiais
4. **Função `gerar_cpf_valido`**: Gera CPF válido para testes

### Requisitos Técnicos
- Validação do algoritmo de dígito verificador
- Tratamento de CPFs com formatação
- Rejeição de CPFs com todos os dígitos iguais
- Performance adequada para validação em lote

### Estrutura Esperada
```
validador-cpf/
├── pyproject.toml
├── README.md
├── .gitignore
├── .pre-commit-config.yaml
├── validador/
│   ├── __init__.py
│   └── cpf.py
└── tests/
    ├── __init__.py
    └── test_cpf.py
```

### Código Base
```python
# validador/cpf.py
import re
from typing import List

def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo oficial da Receita Federal.
    
    Args:
        cpf: String contendo CPF (com ou sem formatação)
        
    Returns:
        True se CPF é válido, False caso contrário
        
    Example:
        >>> validar_cpf("123.456.789-09")
        True
        >>> validar_cpf("111.111.111-11")
        False
    """
    # IMPLEMENTAR: Sua lógica aqui
    pass

# IMPLEMENTAR: As outras funções
```

### Casos de Teste Obrigatórios
- CPFs válidos conhecidos
- CPFs inválidos (dígito verificador errado)
- CPFs com todos os dígitos iguais
- CPFs com formatação e sem formatação
- Strings vazias e valores None
- CPFs com caracteres especiais inválidos

### Critérios de Avaliação
- [ ] Algoritmo de validação implementado corretamente
- [ ] Todos os formatos de entrada aceitos
- [ ] Tratamento robusto de casos especiais
- [ ] Cobertura de testes >= 95%
- [ ] Performance adequada (< 1ms por validação)
- [ ] Documentação clara com exemplos

### Dicas de Implementação
1. Use regex para limpar a entrada
2. Implemente o algoritmo passo a passo
3. Crie fixtures com CPFs conhecidos válidos/inválidos
4. Teste performance com listas grandes

---

## Exercício 1.3: Conversor de Unidades 📏

### Contexto
Desenvolva uma biblioteca para conversão entre diferentes unidades de medida. O sistema deve ser extensível e preciso, servindo como base para aplicações científicas ou de engenharia.

### Objetivos Pedagógicos
- Trabalhar com classes e enums
- Implementar pattern Strategy implicitamente
- Praticar documentação técnica
- Aplicar testes parametrizados

### Requisitos Funcionais
1. **Conversões de Temperatura**: Celsius, Fahrenheit, Kelvin
2. **Conversões de Distância**: Metro, Quilômetro, Milha, Pé
3. **Conversões de Peso**: Quilograma, Libra, Onça
4. **Função universal `converter`**: Interface única para todas as conversões

### Requisitos Técnicos
- Precisão decimal adequada
- Validação de unidades suportadas
- Tratamento de temperaturas absolutas inválidas (< 0 Kelvin)
- Interface consistente para todas as categorias

### Estrutura Esperada
```
conversor-unidades/
├── pyproject.toml
├── README.md
├── .gitignore
├── .pre-commit-config.yaml
├── conversor/
│   ├── __init__.py
│   ├── temperatura.py
│   ├── distancia.py
│   ├── peso.py
│   └── core.py
└── tests/
    ├── __init__.py
    ├── test_temperatura.py
    ├── test_distancia.py
    ├── test_peso.py
    └── test_core.py
```

### Código Base
```python
# conversor/temperatura.py
from enum import Enum
from decimal import Decimal
from typing import Union

class UnidadeTemperatura(str, Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"

def celsius_para_fahrenheit(celsius: Union[int, float, Decimal]) -> Decimal:
    """
    Converte temperatura de Celsius para Fahrenheit.
    
    Formula: F = C * 9/5 + 32
    
    Args:
        celsius: Temperatura em graus Celsius
        
    Returns:
        Temperatura em graus Fahrenheit
        
    Example:
        >>> celsius_para_fahrenheit(0)
        Decimal('32.0')
    """
    # IMPLEMENTAR: Sua lógica aqui
    pass

# IMPLEMENTAR: Outras funções de conversão
```

### Casos de Teste Obrigatórios
- Conversões conhecidas (0°C = 32°F = 273.15K)
- Casos limites (zero absoluto)
- Precisão decimal em conversões
- Valores negativos onde aplicável
- Tratamento de tipos diferentes (int, float, Decimal)

### Critérios de Avaliação
- [ ] Todas as conversões implementadas corretamente
- [ ] Precisão decimal mantida
- [ ] Validações de entrada adequadas
- [ ] Cobertura de testes >= 90%
- [ ] Interface consistente entre categorias
- [ ] Documentação com fórmulas e exemplos

### Dicas de Implementação
1. Use Decimal para manter precisão
2. Valide limites físicos (ex: temperatura absoluta)
3. Crie testes parametrizados para múltiplas conversões
4. Documente as fórmulas utilizadas

### Extensões Opcionais
- Adicionar conversões de pressão
- Implementar conversões de área e volume
- Criar CLI interativo para conversões
