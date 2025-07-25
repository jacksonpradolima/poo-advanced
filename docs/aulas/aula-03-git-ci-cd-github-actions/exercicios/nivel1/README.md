# Exercícios Nível 1 - Básico 🔵

## Visão Geral

Os exercícios do Nível 1 focam na aplicação direta dos conceitos fundamentais de Git avançado e GitHub Actions. Cada exercício deve ser completado em 15-30 minutos e serve como base para os níveis mais avançados.

---

## Exercício 1.1: Git Flow Básico 🔵

### Contexto
Você trabalha em uma pequena startup e precisa implementar um workflow Git organizado para o desenvolvimento de uma aplicação Python simples. A equipe decidiu adotar o Git Flow para manter o código organizado e facilitar releases.

### Objetivos Pedagógicos
- Compreender e aplicar o modelo Git Flow
- Praticar operações de branching e merging
- Desenvolver boas práticas de commit
- Entender o ciclo de vida de features

### Cenário
Sua equipe está desenvolvendo um sistema de calculadora científica em Python. Você foi designado para implementar duas novas funcionalidades: operações trigonométricas e conversão de unidades.

### Requisitos Funcionais

1. **Estrutura Inicial**
   - Criar repositório com branch `main` e `develop`
   - Implementar calculadora básica (soma, subtração, multiplicação, divisão)
   - Configurar arquivo `.gitignore` apropriado para Python

2. **Feature 1: Operações Trigonométricas**
   - Criar feature branch `feature/trigonometric-operations`
   - Implementar métodos: `sin()`, `cos()`, `tan()`
   - Adicionar validação de entrada
   - Incluir tratamento de exceções

3. **Feature 2: Conversão de Unidades**
   - Criar feature branch `feature/unit-conversion`
   - Implementar conversões: temperatura, comprimento, peso
   - Adicionar interface de usuário simples
   - Incluir documentação das funções

4. **Integração e Release**
   - Merge das features para `develop`
   - Resolver conflitos se existirem
   - Criar release branch `release/v1.0.0`
   - Finalizar release e merge para `main`

### Requisitos Técnicos

1. **Estrutura do Projeto**
```
calculadora-cientifica/
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── calculadora.py
│   ├── trigonometria.py
│   └── conversoes.py
├── tests/
│   ├── __init__.py
│   ├── test_calculadora.py
│   ├── test_trigonometria.py
│   └── test_conversoes.py
└── docs/
    └── manual_usuario.md
```

2. **Padrão de Commits**
   - Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`
   - Commits atômicos (uma mudança por commit)
   - Mensagens descritivas em português

3. **Branches Requeridas**
   - `main`: versão de produção
   - `develop`: desenvolvimento ativo
   - `feature/trigonometric-operations`
   - `feature/unit-conversion`
   - `release/v1.0.0`

### Código Base Fornecido

**src/calculadora.py** (implementar)
```python
"""
Calculadora Científica Básica
Sistema de calculadora com operações básicas e avançadas.
"""

class Calculadora:
    """Classe principal da calculadora científica."""
    
    def __init__(self):
        """Inicializa a calculadora."""
        self.historico = []
    
    def somar(self, a: float, b: float) -> float:
        """Realiza soma de dois números."""
        # TODO: Implementar
        pass
    
    def subtrair(self, a: float, b: float) -> float:
        """Realiza subtração de dois números."""
        # TODO: Implementar
        pass
    
    def multiplicar(self, a: float, b: float) -> float:
        """Realiza multiplicação de dois números."""
        # TODO: Implementar
        pass
    
    def dividir(self, a: float, b: float) -> float:
        """Realiza divisão de dois números."""
        # TODO: Implementar (tratar divisão por zero)
        pass
    
    def limpar_historico(self) -> None:
        """Limpa o histórico de operações."""
        # TODO: Implementar
        pass
```

### Passo a Passo Sugerido

#### Fase 1: Configuração Inicial (5 min)
1. Criar repositório local e remoto
2. Configurar `.gitignore` para Python
3. Implementar calculadora básica
4. Commit inicial na branch `main`
5. Criar branch `develop`

#### Fase 2: Feature Trigonométrica (10 min)
1. Criar branch `feature/trigonometric-operations` a partir de `develop`
2. Implementar `src/trigonometria.py`
3. Adicionar testes unitários
4. Commits incrementais
5. Merge para `develop`

#### Fase 3: Feature Conversões (10 min)
1. Criar branch `feature/unit-conversion` a partir de `develop`
2. Implementar `src/conversoes.py`
3. Adicionar interface de usuário
4. Documentar funcionalidades
5. Merge para `develop`

#### Fase 4: Release (5 min)
1. Criar branch `release/v1.0.0` a partir de `develop`
2. Ajustar versão e documentação
3. Merge para `main` e `develop`
4. Criar tag `v1.0.0`

### Restrições e Limitações

1. **Git Flow Estrito**
   - Não é permitido commit direto em `main`
   - Features devem partir de `develop`
   - Release deve ser criada antes do merge final

2. **Qualidade do Código**
   - Todos os métodos devem ter docstrings
   - Tratamento adequado de exceções
   - Testes unitários obrigatórios

3. **Documentação**
   - README.md explicativo
   - Manual do usuário básico
   - Comentários no código

### Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Git Flow Correto** | 30% | Branches, merges e workflow adequados |
| **Funcionalidade** | 25% | Calculadora funcionando conforme especificado |
| **Qualidade Código** | 20% | PEP 8, docstrings, tratamento de erros |
| **Testes** | 15% | Cobertura e qualidade dos testes |
| **Documentação** | 10% | README e comentários explicativos |

### Dicas de Implementação

1. **Git Flow Commands**
```bash
# Inicializar Git Flow
git flow init

# Criar feature
git flow feature start trigonometric-operations

# Finalizar feature
git flow feature finish trigonometric-operations

# Criar release
git flow release start v1.0.0

# Finalizar release
git flow release finish v1.0.0
```

2. **Estrutura de Testes**
```python
import unittest
from src.trigonometria import OperacoesTrigonometricas

class TestTrigonometria(unittest.TestCase):
    def setUp(self):
        self.trig = OperacoesTrigonometricas()
    
    def test_seno_zero(self):
        resultado = self.trig.sin(0)
        self.assertAlmostEqual(resultado, 0, places=7)
```

### Extensões Opcionais

Para quem terminar rapidamente:
- Implementar logaritmos e exponenciais
- Adicionar histórico persistente (arquivo)
- Criar interface gráfica simples com tkinter
- Implementar calculadora de matrizes

### Entrega

**Formato:** Repositório GitHub com histórico Git completo
**Prazo:** 1 semana após a aula
**Arquivos Required:**
- Código fonte completo
- Testes funcionando
- README.md detalhado
- Screenshot do histórico Git (`git log --oneline --graph`)

---

## Exercício 1.2: Primeiro Workflow GitHub Actions 🔵

### Contexto
Sua startup decidiu implementar CI (Continuous Integration) para automatizar testes e garantir qualidade do código. Como desenvolvedor junior, você foi encarregado de criar o primeiro workflow GitHub Actions para o projeto da calculadora científica.

### Objetivos Pedagógicos
- Compreender a estrutura de workflows GitHub Actions
- Implementar pipeline básico de CI
- Configurar testes automatizados
- Entender triggers e eventos

### Cenário
O projeto da calculadora científica do exercício anterior precisa de um sistema de CI que execute automaticamente os testes toda vez que código novo for enviado para o repositório, garantindo que nenhuma mudança quebra funcionalidades existentes.

### Requisitos Funcionais

1. **Trigger Automático**
   - Executar em push para `main` e `develop`
   - Executar em Pull Requests
   - Executar em schedule (daily às 9h UTC)

2. **Ambiente de Teste**
   - Python 3.12
   - Instalar dependências automaticamente
   - Configurar ambiente virtual

3. **Pipeline de Qualidade**
   - Executar testes unitários
   - Verificar cobertura de código
   - Validar estilo de código (flake8)
   - Gerar relatório de qualidade

4. **Notificações**
   - Status badges no README
   - Notificação em caso de falha

### Requisitos Técnicos

1. **Arquivo Workflow**
   - Localização: `.github/workflows/ci.yml`
   - Nome descritivo: "Continuous Integration"
   - Documentação inline com comentários

2. **Jobs e Steps**
   - Job único: `test`
   - Steps organizados e nomeados
   - Uso de actions oficiais do marketplace

3. **Dependências**
```text
# requirements.txt
pytest>=7.4.0
pytest-cov>=4.1.0
flake8>=6.0.0
black>=23.0.0

# requirements-dev.txt
pytest-html>=3.2.0
coverage[toml]>=7.3.0
```

### Código Base - Workflow Template

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

# TODO: Configurar triggers apropriados
on:
  # Adicionar eventos apropriados

# TODO: Definir variáveis de ambiente globais
env:
  PYTHON_VERSION: "3.12"

jobs:
  test:
    # TODO: Configurar runner
    runs-on: 
    
    # TODO: Adicionar strategy matrix para testar múltiplas versões Python
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    # TODO: Implementar checkout do código
    
    # TODO: Configurar Python
    
    # TODO: Cache para dependências
    
    # TODO: Instalar dependências
    
    # TODO: Executar linter (flake8)
    
    # TODO: Executar testes com cobertura
    
    # TODO: Upload dos resultados
```

### Passo a Passo Detalhado

#### Fase 1: Configuração Básica (5 min)
1. Criar diretório `.github/workflows/`
2. Criar arquivo `ci.yml`
3. Definir nome e triggers básicos
4. Configurar job de teste

#### Fase 2: Setup do Ambiente (8 min)
1. Checkout do código fonte
2. Configurar Python com versões múltiplas
3. Configurar cache para pip
4. Instalar dependências de desenvolvimento

#### Fase 3: Pipeline de Qualidade (10 min)
1. Executar flake8 para style check
2. Executar pytest com cobertura
3. Gerar relatórios HTML
4. Upload de artifacts

#### Fase 4: Configurações Avançadas (7 min)
1. Adicionar badges ao README
2. Configurar falha em baixa cobertura
3. Testar workflow completo
4. Documentar processo

### Exemplo de Implementação

**Step 1: Checkout e Python Setup**
```yaml
- name: Checkout do código
  uses: actions/checkout@v4

- name: Configurar Python ${{ matrix.python-version }}
  uses: actions/setup-python@v4
  with:
    python-version: ${{ matrix.python-version }}
```

**Step 2: Cache e Dependências**
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Instalar dependências
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
```

### Arquivo de Testes Exemplo

**tests/test_integration.py**
```python
"""
Testes de integração para workflow CI/CD.
Valida que o ambiente está configurado corretamente.
"""

import sys
import subprocess
import importlib.util


def test_python_version():
    """Verifica se a versão Python está correta."""
    assert sys.version_info >= (3, 11), "Python 3.11+ é obrigatório"


def test_required_packages():
    """Verifica se pacotes obrigatórios estão instalados."""
    required_packages = ['pytest', 'coverage', 'flake8']
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        assert spec is not None, f"Pacote {package} não encontrado"


def test_code_style():
    """Executa verificação de estilo durante os testes."""
    result = subprocess.run(
        ['flake8', 'src/', '--max-line-length=88'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Erros de estilo: {result.stdout}"


def test_calculator_imports():
    """Verifica se os módulos da calculadora podem ser importados."""
    try:
        from src.calculadora import Calculadora
        from src.trigonometria import OperacoesTrigonometricas
        from src.conversoes import ConversaoUnidades
        
        # Teste básico de instanciação
        calc = Calculadora()
        assert calc is not None
        
    except ImportError as e:
        assert False, f"Erro ao importar módulos: {e}"
```

### Configuração de Badges

**README.md** (adicionar no topo)
```markdown
# Calculadora Científica

![CI Status](https://github.com/seu-usuario/calculadora-cientifica/workflows/Continuous%20Integration/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Code Coverage](https://img.shields.io/badge/coverage-95%25-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema de calculadora científica com operações básicas e avançadas.

## Status do Build

| Branch | Status | Cobertura |
|--------|--------|-----------|
| main   | ![main](https://github.com/seu-usuario/repo/workflows/CI/badge.svg?branch=main) | ![cov](coverage-badge.svg) |
| develop| ![dev](https://github.com/seu-usuario/repo/workflows/CI/badge.svg?branch=develop) | ![cov](coverage-badge.svg) |
```

### Restrições e Limitações

1. **Workflow Constraints**
   - Máximo 5 minutes de execução
   - Usar apenas actions oficiais ou verificadas
   - Matrix strategy obrigatória para Python versions

2. **Qualidade Gates**
   - Cobertura mínima: 80%
   - Zero warnings no flake8
   - Todos os testes devem passar

3. **Documentação**
   - Comentários explicativos no YAML
   - README atualizado com badges
   - Documentação do processo de CI

### Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Workflow Funcional** | 35% | Pipeline executa sem erros |
| **Configuração Correta** | 25% | Triggers, matrix, environment corretos |
| **Qualidade Gates** | 20% | Testes, cobertura, linting funcionando |
| **Documentação** | 15% | Comentários no YAML, README atualizado |
| **Best Practices** | 5% | Cache, artifacts, naming conventions |

### Dicas de Troubleshooting

1. **Workflow não executa**
   - Verificar se arquivo está em `.github/workflows/`
   - Validar sintaxe YAML (usar yamllint)
   - Checar permissões do repositório

2. **Falhas de Dependências**
   - Usar cache para pip packages
   - Especificar versões exatas
   - Verificar requirements.txt

3. **Testes Falhando**
   - Executar localmente primeiro
   - Verificar path imports
   - Checar environment variables

### Extensões Avançadas

Para estudantes que finalizarem rapidamente:
- Adicionar job de build para múltiplos OS (Ubuntu, Windows, macOS)
- Implementar deploy automático para GitHub Pages
- Configurar Slack/Discord notifications
- Adicionar security scanning com CodeQL

### Recursos de Apoio

**GitHub Actions Marketplace:**
- [Setup Python](https://github.com/marketplace/actions/setup-python)
- [Cache](https://github.com/marketplace/actions/cache)
- [Upload Artifact](https://github.com/marketplace/actions/upload-a-build-artifact)

**Validadores:**
- [YAML Lint](https://www.yamllint.com/)
- [GitHub Actions Validator](https://rhysd.github.io/actionlint/)

### Entrega

**Formato:** Repositório GitHub com workflow funcionando
**Evidências Required:**
- Screenshot do workflow executando com sucesso
- Badge no README funcionando
- Log completo de uma execução
- Documentação do processo

---

## Exercício 1.3: Pipeline de Testes Simples 🔵

### Contexto
Após implementar o workflow básico, sua equipe percebeu a necessidade de um pipeline de testes mais robusto. O líder técnico solicitou a criação de um sistema que execute diferentes tipos de teste e forneça feedback detalhado sobre a qualidade do código.

### Objetivos Pedagógicos
- Implementar diferentes tipos de teste (unit, integration, E2E)
- Compreender test runners e coverage tools
- Configurar relatórios de qualidade
- Entender test artifacts e reporting

### Cenário
A calculadora científica agora precisa de um pipeline de testes abrangente que inclua testes unitários, de integração e end-to-end, além de análise de código estática e geração de relatórios detalhados para o time de QA.

### Requisitos Funcionais

1. **Múltiplos Tipos de Teste**
   - **Unit Tests:** Testam funções individuais
   - **Integration Tests:** Testam interação entre módulos
   - **End-to-End Tests:** Testam fluxo completo do usuário
   - **Performance Tests:** Verificam performance básica

2. **Análise de Código**
   - **Static Analysis:** flake8, pylint, mypy
   - **Security Scan:** bandit para vulnerabilidades
   - **Complexity Analysis:** radon para complexidade
   - **Documentation:** pydocstyle para docstrings

3. **Relatórios e Artifacts**
   - HTML coverage report
   - JUnit XML para integração
   - Performance benchmarks
   - Code quality metrics

4. **Conditional Execution**
   - Diferentes pipelines para branches
   - Testes opcionais para draft PRs
   - Skip testes em mudanças de documentação

### Requisitos Técnicos

1. **Estrutura de Testes Expandida**
```
tests/
├── unit/
│   ├── test_calculadora_basic.py
│   ├── test_trigonometria.py
│   └── test_conversoes.py
├── integration/
│   ├── test_calculadora_integration.py
│   └── test_workflow_completo.py
├── e2e/
│   ├── test_interface_usuario.py
│   └── test_scenarios_completos.py
├── performance/
│   ├── test_benchmarks.py
│   └── test_memory_usage.py
└── conftest.py
```

2. **Configuração de Ferramentas**
```ini
# setup.cfg
[flake8]
max-line-length = 88
exclude = venv,__pycache__,.git,build,dist
ignore = E203,W503

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=xml
    --junitxml=pytest-report.xml

[mypy]
python_version = 3.12
strict = True
disallow_untyped_defs = True
```

3. **Dependências Expandidas**
```text
# requirements-test.txt
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-html>=3.2.0
pytest-xdist>=3.3.0
pytest-benchmark>=4.0.0
pytest-mock>=3.11.0
flake8>=6.0.0
pylint>=2.17.0
mypy>=1.5.0
bandit>=1.7.0
radon>=6.0.0
pydocstyle>=6.3.0
coverage[toml]>=7.3.0
```

### Código Base - Pipeline Expandido

```yaml
# .github/workflows/testing-pipeline.yml
name: Testing Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC

env:
  PYTHON_VERSION: "3.12"
  COVERAGE_THRESHOLD: "80"

jobs:
  # TODO: Job para análise estática
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      # Implementar steps para flake8, pylint, mypy, bandit
    
  # TODO: Job para testes unitários
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      # Implementar steps para testes unitários com coverage
    
  # TODO: Job para testes de integração
  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      # Implementar steps para testes de integração
    
  # TODO: Job para testes E2E
  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      # Implementar steps para testes end-to-end
    
  # TODO: Job para performance tests
  performance-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      # Implementar steps para benchmarks
    
  # TODO: Job final para agregar resultados
  quality-gate:
    needs: [static-analysis, unit-tests, integration-tests, e2e-tests, performance-tests]
    runs-on: ubuntu-latest
    steps:
      # Implementar quality gate final
```

### Implementação dos Testes

#### 1. Testes Unitários Avançados

**tests/unit/test_calculadora_advanced.py**
```python
"""
Testes unitários avançados para calculadora científica.
Inclui parametrized tests, fixtures e mocking.
"""

import pytest
import math
from unittest.mock import Mock, patch
from src.calculadora import Calculadora


class TestCalculadoraAdvanced:
    """Suite de testes avançados para calculadora."""
    
    @pytest.fixture
    def calculadora(self):
        """Fixture para instância limpa da calculadora."""
        return Calculadora()
    
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
        (float('inf'), 1, float('inf')),
    ])
    def test_soma_parametrizada(self, calculadora, a, b, expected):
        """Testa soma com múltiplos casos usando parametrize."""
        resultado = calculadora.somar(a, b)
        if math.isinf(expected):
            assert math.isinf(resultado)
        else:
            assert resultado == expected
    
    @pytest.mark.parametrize("a,b", [
        (1, 0),
        (float('inf'), 0),
        (-5, 0),
    ])
    def test_divisao_por_zero(self, calculadora, a, b):
        """Testa se divisão por zero lança exceção apropriada."""
        with pytest.raises(ZeroDivisionError):
            calculadora.dividir(a, b)
    
    def test_historico_operacoes(self, calculadora):
        """Testa se histórico de operações é mantido corretamente."""
        calculadora.somar(2, 3)
        calculadora.multiplicar(4, 5)
        
        assert len(calculadora.historico) == 2
        assert calculadora.historico[0]['operacao'] == 'soma'
        assert calculadora.historico[0]['resultado'] == 5
    
    @patch('src.calculadora.datetime')
    def test_timestamp_operacoes(self, mock_datetime, calculadora):
        """Testa se timestamp é adicionado às operações."""
        mock_datetime.now.return_value = "2024-01-01 10:00:00"
        
        calculadora.somar(1, 1)
        
        assert calculadora.historico[0]['timestamp'] == "2024-01-01 10:00:00"
        mock_datetime.now.assert_called_once()


@pytest.mark.slow
class TestCalculadoraPerformance:
    """Testes de performance para operações pesadas."""
    
    def test_operacoes_em_lote_performance(self, benchmark):
        """Benchmark para múltiplas operações."""
        calc = Calculadora()
        
        def operacoes_lote():
            for i in range(1000):
                calc.somar(i, i+1)
                calc.multiplicar(i, 2)
        
        result = benchmark(operacoes_lote)
        assert len(calc.historico) == 2000
```

#### 2. Testes de Integração

**tests/integration/test_calculadora_integration.py**
```python
"""
Testes de integração para calculadora científica.
Testa interação entre módulos diferentes.
"""

import pytest
from src.calculadora import Calculadora
from src.trigonometria import OperacoesTrigonometricas
from src.conversoes import ConversaoUnidades


class TestIntegracaoCompleta:
    """Testes de integração entre todos os módulos."""
    
    @pytest.fixture
    def sistema_completo(self):
        """Setup do sistema completo integrado."""
        return {
            'calculadora': Calculadora(),
            'trigonometria': OperacoesTrigonometricas(),
            'conversoes': ConversaoUnidades()
        }
    
    def test_workflow_calculo_trigonometrico_completo(self, sistema_completo):
        """
        Testa workflow completo:
        1. Converter graus para radianos
        2. Calcular seno
        3. Elevar ao quadrado
        4. Converter resultado para percentual
        """
        calc = sistema_completo['calculadora']
        trig = sistema_completo['trigonometria']
        conv = sistema_completo['conversoes']
        
        # Workflow: sin²(30°) em percentual
        angulo_graus = 30
        angulo_rad = conv.graus_para_radianos(angulo_graus)
        seno_valor = trig.sin(angulo_rad)
        seno_quadrado = calc.multiplicar(seno_valor, seno_valor)
        percentual = conv.decimal_para_percentual(seno_quadrado)
        
        # sin(30°) = 0.5, sin²(30°) = 0.25 = 25%
        assert abs(percentual - 25.0) < 0.01
    
    def test_cadeia_conversoes_unidades(self, sistema_completo):
        """
        Testa cadeia de conversões:
        Celsius → Fahrenheit → Kelvin → Celsius
        """
        conv = sistema_completo['conversoes']
        
        temp_inicial = 25.0  # Celsius
        temp_f = conv.celsius_para_fahrenheit(temp_inicial)
        temp_k = conv.fahrenheit_para_kelvin(temp_f)
        temp_final = conv.kelvin_para_celsius(temp_k)
        
        # Deve retornar ao valor original
        assert abs(temp_final - temp_inicial) < 0.01
    
    def test_persistencia_estado_entre_operacoes(self, sistema_completo):
        """Testa se estado é mantido corretamente entre operações."""
        calc = sistema_completo['calculadora']
        
        # Múltiplas operações sequenciais
        resultado1 = calc.somar(10, 5)
        resultado2 = calc.multiplicar(resultado1, 2)
        resultado3 = calc.dividir(resultado2, 3)
        
        # Verificar histórico completo
        assert len(calc.historico) == 3
        assert calc.historico[-1]['resultado'] == resultado3
        assert resultado3 == 10.0  # ((10+5)*2)/3 = 30/3 = 10
```

#### 3. Testes End-to-End

**tests/e2e/test_interface_usuario.py**
```python
"""
Testes end-to-end simulando interação do usuário.
Testa fluxos completos da aplicação.
"""

import pytest
import io
import sys
from contextlib import redirect_stdout, redirect_stdin
from src.main import AplicacaoCalculadora


class TestFluxoUsuario:
    """Testes de fluxo end-to-end do usuário."""
    
    @pytest.fixture
    def app(self):
        """Fixture para aplicação completa."""
        return AplicacaoCalculadora()
    
    def test_fluxo_calculadora_basica_completo(self, app):
        """
        Simula usuário fazendo cálculos básicos completos:
        1. Abre aplicação
        2. Faz algumas operações
        3. Consulta histórico
        4. Limpa histórico
        5. Sai da aplicação
        """
        entradas = [
            "1",  # Menu calculadora básica
            "2", "3", "+",  # 2 + 3
            "5", "2", "*",  # 5 * 2
            "h",  # Histórico
            "c",  # Limpar
            "q"   # Quit
        ]
        
        entrada_simulada = "\n".join(entradas)
        saida = io.StringIO()
        
        with redirect_stdin(io.StringIO(entrada_simulada)):
            with redirect_stdout(saida):
                app.executar()
        
        output = saida.getvalue()
        
        # Verificações das saídas esperadas
        assert "Resultado: 5" in output  # 2 + 3
        assert "Resultado: 10" in output  # 5 * 2
        assert "Histórico limpo" in output
        assert "Obrigado por usar" in output
    
    def test_fluxo_trigonometria_avancado(self, app):
        """
        Testa fluxo completo de cálculos trigonométricos:
        1. Acessa menu trigonometria
        2. Calcula sin, cos, tan de ângulos específicos
        3. Verifica resultados conhecidos
        """
        entradas = [
            "2",  # Menu trigonometria
            "30", "sin",  # sin(30°) = 0.5
            "60", "cos",  # cos(60°) = 0.5
            "45", "tan",  # tan(45°) = 1.0
            "h",  # Histórico
            "q"   # Quit
        ]
        
        entrada_simulada = "\n".join(entradas)
        saida = io.StringIO()
        
        with redirect_stdin(io.StringIO(entrada_simulada)):
            with redirect_stdout(saida):
                app.executar()
        
        output = saida.getvalue()
        
        # Verificar resultados trigonométricos esperados
        assert "0.5" in output  # sin(30°) e cos(60°)
        assert "1.0" in output  # tan(45°)
    
    def test_tratamento_erros_usuario(self, app):
        """
        Testa como aplicação lida com erros de usuário:
        1. Entrada inválida no menu
        2. Divisão por zero
        3. Valores não numéricos
        """
        entradas = [
            "99",  # Opção inválida
            "1",   # Calculadora básica
            "5", "0", "/",  # Divisão por zero
            "abc", "2", "+",  # Entrada não numérica
            "q"    # Quit
        ]
        
        entrada_simulada = "\n".join(entradas)
        saida = io.StringIO()
        
        with redirect_stdin(io.StringIO(entrada_simulada)):
            with redirect_stdout(saida):
                try:
                    app.executar()
                except Exception:
                    pass  # Esperado em caso de erro
        
        output = saida.getvalue()
        
        # Verificar mensagens de erro apropriadas
        assert "Opção inválida" in output or "Erro" in output
        assert "Divisão por zero" in output or "Erro" in output
```

### Pipeline Workflow Completo

```yaml
name: Comprehensive Testing Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    
    - name: Install analysis tools
      run: |
        pip install flake8 pylint mypy bandit radon pydocstyle
    
    - name: Run flake8
      run: flake8 src/ tests/ --statistics
    
    - name: Run pylint
      run: pylint src/ --output-format=json > pylint-report.json
      continue-on-error: true
    
    - name: Run mypy
      run: mypy src/
    
    - name: Run bandit security scan
      run: bandit -r src/ -f json -o bandit-report.json
      continue-on-error: true
    
    - name: Run radon complexity
      run: radon cc src/ --json > radon-report.json
    
    - name: Upload analysis reports
      uses: actions/upload-artifact@v3
      with:
        name: static-analysis-reports
        path: "*-report.json"

  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ \
          --cov=src \
          --cov-report=html \
          --cov-report=xml \
          --junitxml=junit-unit.xml \
          -v
    
    - name: Check coverage threshold
      run: |
        coverage report --fail-under=80
    
    - name: Upload unit test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: unit-test-results-${{ matrix.python-version }}
        path: |
          htmlcov/
          coverage.xml
          junit-unit.xml

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ \
          --junitxml=junit-integration.xml \
          -v
    
    - name: Upload integration results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: integration-test-results
        path: junit-integration.xml

  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run E2E tests
      run: |
        pytest tests/e2e/ \
          --junitxml=junit-e2e.xml \
          -v --tb=short
    
    - name: Upload E2E results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: e2e-test-results
        path: junit-e2e.xml

  performance-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
        pip install pytest-benchmark
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ \
          --benchmark-json=benchmark-results.json \
          -v
    
    - name: Upload benchmark results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: benchmark-results.json

  quality-gate:
    needs: [static-analysis, unit-tests, integration-tests, e2e-tests, performance-tests]
    runs-on: ubuntu-latest
    
    steps:
    - name: Download all artifacts
      uses: actions/download-artifact@v3
    
    - name: Generate quality report
      run: |
        echo "# Quality Gate Report" > quality-report.md
        echo "## Test Results Summary" >> quality-report.md
        echo "- ✅ Static Analysis: Completed" >> quality-report.md
        echo "- ✅ Unit Tests: Completed" >> quality-report.md
        echo "- ✅ Integration Tests: Completed" >> quality-report.md
        echo "- ✅ E2E Tests: Completed" >> quality-report.md
        echo "- ✅ Performance Tests: Completed" >> quality-report.md
    
    - name: Upload quality report
      uses: actions/upload-artifact@v3
      with:
        name: quality-gate-report
        path: quality-report.md
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '🎉 All quality gates passed! ✅'
          })
```

### Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Pipeline Completo** | 30% | Todos os jobs executam sem erro |
| **Cobertura de Testes** | 25% | Unit, integration, E2E implementados |
| **Quality Gates** | 20% | Static analysis, coverage threshold |
| **Artifacts e Reports** | 15% | Relatórios gerados e uploadados |
| **Configuração Avançada** | 10% | Matrix, cache, conditional execution |

### Entrega

**Evidências Required:**
- Workflow executando com sucesso (screenshot)
- Relatórios de cobertura (HTML)
- Artifacts baixados do GitHub
- Quality gate report gerado
- Documentação do pipeline no README

### Recursos de Apoio

**Pytest Plugins Úteis:**
- pytest-xdist: Execução paralela
- pytest-benchmark: Performance testing
- pytest-mock: Mocking avançado
- pytest-html: Relatórios HTML

**GitHub Actions:**
- [Test Reporter](https://github.com/marketplace/actions/test-reporter)
- [Coverage Comment](https://github.com/marketplace/actions/coverage-comment)
- [Benchmark Action](https://github.com/marketplace/actions/continuous-benchmark)

---

**Parabéns! Você completou todos os exercícios do Nível 1! 🎉**

Estes exercícios básicos estabeleceram uma base sólida em:
- Git Flow e branching strategies
- GitHub Actions workflows
- Comprehensive testing pipelines
- Quality gates e CI/CD practices

**Próximo Passo:** Avance para os [Exercícios Nível 2](../nivel2/README.md) para integração avançada e workflows complexos! 🚀
