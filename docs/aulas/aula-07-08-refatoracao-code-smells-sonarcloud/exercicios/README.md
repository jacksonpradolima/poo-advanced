# Exercícios Práticos - Refatoração de Códigos e Code Smells

## Visão Geral

Este conjunto de exercícios foi cuidadosamente elaborado para consolidar os conceitos de refatoração apresentados na aula. Os exercícios estão organizados em três níveis de dificuldade progressiva, permitindo aplicação prática das técnicas aprendidas.

## Organização dos Exercícios

### 🔵 Nível 1 - Básico (15-30 minutos)
- **Objetivo:** Aplicação direta de conceitos de refatoração
- **Foco:** Identificação e correção de code smells simples
- **Complexidade:** Uma única funcionalidade por exercício

### 🟡 Nível 2 - Intermediário (45-90 minutos)  
- **Objetivo:** Integração de múltiplos conceitos de refatoração
- **Foco:** Sistemas pequenos com 2-4 classes
- **Complexidade:** Aplicação de múltiplas técnicas de refatoração

### 🔴 Nível 3 - Avançado (2-4 horas)
- **Objetivo:** Design complexo e decisões arquiteturais
- **Foco:** Sistemas completos com múltiplas responsabilidades
- **Complexidade:** Refatoração abrangente com integração de ferramentas

## Critérios de Avaliação

Para todos os exercícios, considere:

### Critérios Técnicos
- ✅ **Funcionalidade Preservada:** Comportamento original mantido
- ✅ **Code Smells Eliminados:** Problemas identificados corrigidos
- ✅ **Métricas Melhoradas:** Complexidade ciclomática reduzida
- ✅ **Testabilidade:** Código mais fácil de testar
- ✅ **Legibilidade:** Código mais claro e expressivo

### Critérios de Processo
- ✅ **TDD Aplicado:** Testes escritos antes da refatoração
- ✅ **Incrementalidade:** Mudanças pequenas e frequentes
- ✅ **Documentação:** Justificativas das decisões de refatoração
- ✅ **Ferramentas:** Uso adequado de linters e análise estática

## Estrutura dos Exercícios

Cada exercício contém:

1. **Contexto e Motivação:** Cenário realista que justifica a refatoração
2. **Código Inicial:** Sistema com code smells intencionais
3. **Requisitos:** Lista clara e específica do que deve ser alcançado
4. **Restrições:** Limitações técnicas ou conceituais
5. **Dicas:** Orientações para superar dificuldades comuns
6. **Extensões:** Sugestões para aprofundamento

## Como Trabalhar com os Exercícios

### Passo 1: Análise Inicial
- Leia o código fornecido
- Identifique todos os code smells presentes
- Priorize quais problemas resolver primeiro

### Passo 2: Criação da Rede de Segurança
- Escreva testes que caracterizam o comportamento atual
- Garanta cobertura de pelo menos 80% do código crítico
- Valide que todos os testes passam

### Passo 3: Refatoração Incremental
- Aplique uma técnica de refatoração por vez
- Execute os testes após cada mudança
- Faça commits pequenos e frequentes

### Passo 4: Validação Final
- Execute análise estática (pylint, flake8)
- Compare métricas antes/depois
- Documente as melhorias alcançadas

## Recursos de Apoio

### Ferramentas Recomendadas
```bash
# Instalar dependências para os exercícios
pip install pytest pytest-cov pylint flake8 black isort mypy
```

### Comandos Úteis
```bash
# Executar testes com cobertura
pytest --cov=src --cov-report=html

# Análise de qualidade
pylint src/
flake8 src/
mypy src/

# Formatação automática
black src/
isort src/
```

### Template de Documentação
Para cada refatoração realizada, documente:

```markdown
## Refatoração: [Nome da Técnica]

### Code Smell Identificado
- **Tipo:** [Ex: Long Method, God Class]
- **Localização:** [Arquivo e linha]
- **Impacto:** [Descrição do problema]

### Solução Aplicada
- **Técnica:** [Ex: Extract Method, Replace Conditional with Polymorphism]
- **Justificativa:** [Por que esta técnica foi escolhida]

### Métricas Antes/Depois
- **Complexidade Ciclomática:** [X → Y]
- **Linhas de Código:** [X → Y]  
- **Número de Métodos:** [X → Y]

### Benefícios Alcançados
- [Lista de melhorias observadas]
```

---

**Próximo:** Comece pelo [Nível 1 - Exercícios Básicos](nivel1/) para aplicar conceitos fundamentais de refatoração.
