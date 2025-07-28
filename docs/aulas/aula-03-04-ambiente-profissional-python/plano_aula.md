---
aula: 02
titulo: "Ambiente Profissional de Projetos Python"
objetivo: "Capacitar os alunos a configurarem um ambiente de desenvolvimento Python profissional e moderno"
carga_horaria: "3h"
modalidade: "Prática com demonstração"
prerequisitos: ['Python 3.12+', 'Git básico', 'conceitos de POO']
---

# Plano de Aula 02 - Ambiente Profissional de Projetos Python

## Identificação

- **Disciplina**: Programação Orientada a Objetos II
- **Aula**: 02
- **Tema**: Ambiente Profissional de Projetos Python
- **Duração**: 180 minutos (3 horas)
- **Modalidade**: Aula prática com demonstração e laboratório

## Objetivo Geral

Capacitar os alunos a configurarem um ambiente de desenvolvimento Python profissional e moderno, alinhado às práticas utilizadas por equipes de engenharia de software no mercado. A aula visa criar uma base sólida de ferramentas e configurações que garantam qualidade de código, segurança, organização de dependências e documentação técnica desde o início do projeto.

## Objetivos Específicos

- [ ] Introduzir o uso de ambientes virtuais para isolar dependências de projetos Python
- [ ] Configurar ambientes com uv e poetry para controle de pacotes e versões
- [ ] Estabelecer fluxos de linting e análise estática de código com ruff e mypy
- [ ] Implementar hooks automáticos de pre-commit para garantir qualidade antes do versionamento
- [ ] Configurar documentação automática com pdoc
- [ ] Criar testes unitários básicos com pytest e medir cobertura com pytest-cov
- [ ] Registrar o projeto inicial no GitHub, configurando um repositório versionado adequadamente

## Conteúdo Programático

### Bloco 1: Fundamentos (45 min)
- **Ambientes Virtuais**
  - O que são, importância e criação com uv
  - Alternativa com poetry e comparativo
- **pyproject.toml**
  - Estrutura e gerenciamento centralizado de dependências

### Bloco 2: Qualidade de Código (60 min)
- **Ferramentas de Qualidade de Código**
  - Ruff: configuração e execução
  - Mypy: introdução à tipagem estática
- **Hooks de pre-commit**
  - Configuração do pre-commit com ruff, mypy e black
  - Execução automática de qualidade antes de commits

### Bloco 3: Documentação e Testes (45 min)
- **Documentação com pdoc**
  - Geração automática de documentação a partir de docstrings
- **Testes e Benchmark**
  - Introdução ao pytest
  - pytest-cov para medir cobertura de testes
  - pytest-benchmark para medir performance de funções

### Bloco 4: Versionamento (30 min)
- **Registro do projeto no GitHub**
  - Criação de repositório
  - Configuração inicial
  - Primeiro commit com estrutura completa

## Metodologia

### Estratégias Didáticas
1. **Exposição Teórica** (30 min): Apresentação de conceitos e ferramentas modernas
2. **Demonstração Prática** (60 min): Professor criando ambiente completo ao vivo
3. **Laboratório Guiado** (80 min): Alunos replicando e configurando seus próprios ambientes
4. **Síntese e Avaliação** (10 min): Validação dos ambientes criados

### Recursos Necessários
- Laboratório de informática com acesso à internet
- Python 3.12+ instalado em todas as máquinas
- Git configurado
- Acesso ao GitHub
- Editor de código (VS Code recomendado)

### Sequência de Atividades

#### Abertura (10 min)
- Apresentação dos objetivos da aula
- Contextualização da importância de ambientes profissionais
- Demonstração de problemas comuns sem configuração adequada

#### Demonstração do Professor (60 min)
- Criação passo-a-passo de um projeto exemplo
- Configuração de todas as ferramentas
- Explicação de cada etapa e suas justificativas

#### Laboratório Prático (80 min)
- Alunos replicam o processo demonstrado
- Apoio individualizado para resolução de problemas
- Validação da configuração de cada aluno

#### Exercícios Adicionais (20 min)
- Criação de funções adicionais no projeto
- Escrita de testes unitários
- Geração de documentação

#### Fechamento (10 min)
- Verificação dos ambientes configurados
- Esclarecimento de dúvidas
- Orientações para próxima aula

## Avaliação

### Critérios de Avaliação
- [ ] Ambiente virtual configurado corretamente
- [ ] pyproject.toml completo e funcional
- [ ] Ferramentas de qualidade operacionais (ruff, mypy)
- [ ] Pre-commit funcionando
- [ ] Testes executando com cobertura mínima
- [ ] Documentação sendo gerada
- [ ] Repositório GitHub configurado

### Entregáveis
1. **Repositório GitHub** com estrutura completa do projeto
2. **Relatório de Configuração** documentando o processo e ferramentas
3. **Demonstração** do ambiente funcionando (testes, linting, documentação)

### Peso na Avaliação
- Configuração técnica correta: 60%
- Qualidade da documentação: 20%
- Organização do código: 20%

## Recursos Adicionais

### Leituras Complementares
- [Documentação oficial do UV](https://docs.astral.sh/uv/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ruff Configuration](https://docs.astral.sh/ruff/)
- [Mypy Documentation](https://mypy.readthedocs.io/)

### Ferramentas Online
- [GitHub](https://github.com)
- [PyPI](https://pypi.org)
- [Python Package Index](https://pypi.org)

## Preparação Prévia

### Para o Professor
- [ ] Ambiente de demonstração preparado
- [ ] Slides com conceitos teóricos
- [ ] Projeto exemplo completo para demonstração
- [ ] Checklist de verificação para cada aluno

### Para os Alunos
- [ ] Python 3.12+ instalado e funcionando
- [ ] Git configurado com nome e email
- [ ] Conta GitHub criada
- [ ] Editor de código instalado

## Possíveis Dificuldades e Soluções

### Problemas Técnicos Comuns
1. **Problemas de instalação do UV**
   - Solução: Fallback para venv + pip
   - Documentação de troubleshooting preparada

2. **Conflitos de PATH/ambiente**
   - Solução: Verificação step-by-step das variáveis
   - Reset completo do ambiente se necessário

3. **Problemas de rede/proxy**
   - Solução: Configuração de proxy para ferramentas
   - Packages offline como backup

### Adaptações para Diferentes Níveis
- **Iniciantes**: Mais tempo na explicação de conceitos básicos
- **Avançados**: Exercícios extras com configurações avançadas
- **Grupos mistos**: Peer programming entre níveis diferentes

## Extensões e Exercícios Extras

### Para Casa
1. Configurar o mesmo ambiente em máquina pessoal
2. Adicionar 3 novas funções ao projeto com testes
3. Configurar GitHub Actions básico (preparação para próxima aula)

### Desafios Avançados
1. Configurar ambiente com Poetry e comparar com UV
2. Implementar custom pre-commit hooks
3. Configurar multiple Python versions com pyenv

## Conexões com Outras Aulas

### Pré-requisitos Importantes
- Aula 01: Conceitos de POO e boas práticas
- Conhecimento básico de Git

### Preparação para Próximas Aulas
- Aula 03: CI/CD com GitHub Actions (baseado neste ambiente)
- Aula 04: Refatoração (utilizará as ferramentas de qualidade)
- Projetos futuros: Base para todos os desenvolvimentos do semestre
