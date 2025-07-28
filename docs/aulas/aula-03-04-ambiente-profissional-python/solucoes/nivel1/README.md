# Soluções dos Exercícios - Nível 1

Esta pasta contém as soluções comentadas dos exercícios de nível básico. As soluções são apresentadas com explicações detalhadas das decisões de implementação e boas práticas aplicadas.

## 🔵 Soluções Disponíveis

### Exercício 1.1: Calculadora de Impostos
- **Arquivo**: `calculadora_impostos_solucao.py`
- **Testes**: `test_calculadora_impostos_solucao.py`
- **Configuração**: `pyproject.toml`

### Exercício 1.2: Validador de CPF
- **Arquivo**: `validador_cpf_solucao.py`
- **Testes**: `test_validador_cpf_solucao.py`
- **Configuração**: `pyproject.toml`

### Exercício 1.3: Conversor de Unidades
- **Arquivo**: `conversor_unidades_solucao.py`
- **Testes**: `test_conversor_unidades_solucao.py`
- **Configuração**: `pyproject.toml`

## Critérios Aplicados

Todas as soluções seguem rigorosamente:

✅ **Tipagem Completa**: Type hints em todas as funções
✅ **Documentação**: Docstrings no formato Google/Sphinx
✅ **Validação**: Tratamento adequado de casos especiais
✅ **Testes**: Cobertura >= 90% com casos limites
✅ **Qualidade**: Código passa em ruff check e mypy
✅ **Configuração**: pyproject.toml completo e funcional

## Como Usar as Soluções

1. **Compare** sua implementação com a solução
2. **Identifique** diferenças nas abordagens
3. **Entenda** as justificativas das decisões técnicas
4. **Aplique** as boas práticas em seus projetos

## Notas Importantes

- As soluções são **uma das possíveis implementações** corretas
- Outras abordagens válidas podem existir
- O foco está em **boas práticas** e **qualidade de código**
- Priorize **legibilidade** e **manutenibilidade** sobre otimização prematura

---

## 🎯 Como Executar as Soluções

### Executar Calculadora de Impostos
```bash
# Execução direta
python calculadora_impostos_solucao.py

# Executar testes
pytest test_calculadora_impostos_solucao.py -v --cov
```

### Executar Gerenciador de Tarefas
```bash
# Execução direta
python gerenciador_tarefas_solucao.py

# Ver ajuda
python gerenciador_tarefas_solucao.py --help

# Executar testes
pytest test_gerenciador_tarefas_solucao.py -v --cov
```

### Executar Todos os Testes
```bash
# Testes com cobertura e relatório detalhado
pytest -v --cov=. --cov-report=html --cov-report=term-missing

# Testes com benchmark (se pytest-benchmark estiver instalado)
pytest --benchmark-only
```

---

## 🔍 Análise de Qualidade

### Verificação de Tipos
```bash
# Verificar tipagem com mypy
mypy calculadora_impostos_solucao.py
mypy gerenciador_tarefas_solucao.py
```

### Formatação e Linting
```bash
# Verificar estilo com ruff
ruff check *.py

# Auto-formatar código
ruff format *.py
```

### Cobertura de Testes
As soluções foram desenvolvidas com foco em alta cobertura de testes:

- **Calculadora**: 100% de cobertura de linhas e branches
- **Gerenciador**: 95%+ de cobertura incluindo casos extremos

---

## 📚 Lições Aprendidas

### 1. Precisão em Cálculos Financeiros
❌ **Problemático**:
```python
def calcular_imposto(valor):
    return valor * 0.18  # Float pode gerar imprecisão!
```

✅ **Correto**:
```python
def calcular_imposto(valor: Union[int, float, Decimal]) -> Decimal:
    valor_decimal = Decimal(str(valor))
    return (valor_decimal * Decimal('0.18')).quantize(Decimal('0.01'))
```

### 2. Tratamento Robusto de Arquivo
❌ **Problemático**:
```python
with open('dados.json') as f:
    dados = json.load(f)  # Pode falhar de várias formas!
```

✅ **Correto**:
```python
try:
    if self.arquivo_dados.exists():
        with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
            dados = json.load(f)
except (json.JSONDecodeError, KeyError, TypeError) as e:
    # Backup e recuperação elegante
    self._criar_backup_e_reiniciar()
```

### 3. Interface de Usuário Intuitiva
❌ **Problemático**:
```python
print("Digite: 1-Add 2-List 3-Exit")  # Pouco amigável
opcao = input(">>")
```

✅ **Correto**:
```python
print("🚀 GERENCIADOR DE TAREFAS")
print("1. ➕ Adicionar tarefa")
print("2. 📋 Listar todas as tarefas")
opcao = input("👉 Escolha uma opção: ")
```

---

## 🎓 Próximos Passos

Após dominar essas soluções básicas, o estudante estará preparado para:

1. **Nível 2 (Intermediário)**: Sistema de biblioteca com múltiplas classes
2. **Nível 3 (Avançado)**: Plataforma de e-commerce com arquitetura complexa
3. **Aplicação em Projetos Reais**: Uso desses padrões em sistemas profissionais

---

## 🤝 Contribuições e Dúvidas

### Para Estudantes
- Analise cada linha dos comentários pedagógicos
- Execute os testes para entender o comportamento esperado
- Modifique o código e observe como os testes falham/passam
- Compare sua solução original com estas implementações

### Para Instrutores
- Use estas soluções como referência para correção
- Adapte os comentários pedagógicos conforme necessário
- Sugira variações dos exercícios baseadas nesta estrutura
- Utilice os testes como base para avaliação automatizada

---

*Desenvolvido com foco em qualidade, clareza e aprendizado prático. Cada linha de código é uma oportunidade de ensino.* 🚀
