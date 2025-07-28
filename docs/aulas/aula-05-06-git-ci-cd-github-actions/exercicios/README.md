# Exercícios Práticos - Aula 03: Git e CI/CD com GitHub Actions

## Visão Geral

Este conjunto de exercícios está estruturado em três níveis progressivos de dificuldade, cada um focado em diferentes aspectos do Git avançado e CI/CD com GitHub Actions. Os exercícios são projetados para serem realizados sequencialmente, construindo conhecimento e habilidades de forma incremental.

## Estrutura dos Exercícios

### 🔵 Nível 1 - Básico (15-30 minutos cada)
**Objetivo:** Aplicação direta de conceitos fundamentais
- **Exercício 1.1:** Git Flow Básico
- **Exercício 1.2:** Primeiro Workflow GitHub Actions
- **Exercício 1.3:** Pipeline de Testes Simples

### 🟡 Nível 2 - Intermediário (45-90 minutos cada)
**Objetivo:** Integração de múltiplos conceitos e ferramentas
- **Exercício 2.1:** Sistema de Branching Empresarial
- **Exercício 2.2:** Pipeline Multi-Ambiente
- **Exercício 2.3:** Workflow com Matrix Strategy

### 🔴 Nível 3 - Avançado (2-4 horas cada)
**Objetivo:** Design complexo e decisões arquiteturais
- **Exercício 3.1:** Pipeline Completo com Microserviços
- **Exercício 3.2:** Sistema de Deploy Automatizado
- **Exercício 3.3:** Observabilidade e Monitoramento

## Pré-requisitos Gerais

### Ferramentas Necessárias
- Git 2.40+
- Docker Desktop
- Visual Studio Code
- Python 3.12+
- Node.js 18+
- Conta GitHub com Actions habilitado

### Conhecimentos Prévios
- Git básico (add, commit, push, pull)
- Python intermediário e POO
- Conceitos básicos de API REST
- Familiaridade com linha de comando

## Configuração do Ambiente

### 1. Clone do Repositório Base
```bash
# Clone o repositório template
git clone https://github.com/seu-usuario/poo-advanced-exercises.git
cd poo-advanced-exercises

# Configure sua identidade Git
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### 2. Configuração Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Verificação Docker
```bash
# Testar instalação Docker
docker --version
docker run hello-world
```

### 4. Configuração GitHub
- Verifique se GitHub Actions está habilitado no seu repositório
- Configure secrets necessários (conforme exercícios específicos)
- Certifique-se de ter permissões de admin no repositório

## Metodologia de Avaliação

### Critérios Gerais
Cada exercício será avaliado com base em:

1. **Funcionalidade (40%)**
   - O código executa sem erros
   - Atende todos os requisitos especificados
   - Comportamento correto em casos normais

2. **Qualidade do Código (25%)**
   - Seguimento das convenções PEP 8
   - Comentários explicativos adequados
   - Estrutura organizada e legível

3. **Implementação Git/CI/CD (25%)**
   - Uso correto de Git (commits, branches, merges)
   - Workflow GitHub Actions funcional
   - Boas práticas de DevOps aplicadas

4. **Documentação (10%)**
   - README explicativo
   - Comentários no código
   - Instruções de uso claras

### Rubrica por Nível

#### Nível 1 - Básico 🔵
- **Excelente (9-10):** Todos os requisitos atendidos, código limpo, workflow funcional
- **Bom (7-8):** Requisitos principais atendidos, pequenos ajustes necessários
- **Satisfatório (6-7):** Conceitos corretos, implementação funcional básica
- **Insatisfatório (0-5):** Requisitos não atendidos ou erros fundamentais

#### Nível 2 - Intermediário 🟡
- **Excelente (9-10):** Sistema integrado completo, boas práticas aplicadas, documentação clara
- **Bom (7-8):** Integração funcional, algumas boas práticas aplicadas
- **Satisfatório (6-7):** Funcionalidade básica, integração parcial
- **Insatisfatório (0-5):** Integração falha ou conceitos incorretos

#### Nível 3 - Avançado 🔴
- **Excelente (9-10):** Arquitetura robusta, otimizações aplicadas, produção-ready
- **Bom (7-8):** Arquitetura sólida, funcionalidade completa
- **Satisfatório (6-7):** Implementação básica dos requisitos avançados
- **Insatisfatório (0-5):** Arquitetura falha ou não implementado

## Submissão e Entrega

### Formato de Entrega
Para cada exercício, submeta:

1. **Código Fonte Completo**
   - Todos os arquivos necessários
   - Estrutura de diretórios organizada
   - Dependências documentadas

2. **Repositório Git**
   - Histórico de commits claro
   - Branches organizadas (quando aplicável)
   - Tags para versões (quando aplicável)

3. **Documentação**
   - README.md explicativo
   - Instruções de instalação/execução
   - Capturas de tela (quando relevante)

4. **Evidências de Funcionamento**
   - Logs de execução
   - Screenshots de workflows GitHub Actions
   - Resultados de testes

### Cronograma de Entregas

| Exercício | Prazo | Observações |
|-----------|-------|-------------|
| **Nível 1 (todos)** | 1 semana após a aula | Pode ser feito durante a aula |
| **Nível 2 (escolher 2)** | 2 semanas após a aula | Priorize exercícios de seu interesse |
| **Nível 3 (escolher 1)** | 3 semanas após a aula | Projeto mais elaborado |

### Submissão
- **Plataforma:** GitHub Classroom ou repositório pessoal
- **Formato:** Link do repositório + arquivo ZIP de backup
- **Deadline:** 23:59 da data especificada
- **Late Policy:** -1 ponto por dia de atraso

## Recursos de Apoio

### Documentação Oficial
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)

### Tutoriais Recomendados
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [GitHub Skills](https://skills.github.com/)
- [Docker Getting Started](https://docs.docker.com/get-started/)

### Ferramentas Úteis
- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [GitHub Actions Marketplace](https://github.com/marketplace/actions)
- [YAML Validator](https://www.yamllint.com/)
- [Markdown Editor](https://stackedit.io/)

## Dicas Gerais de Sucesso

### Para Iniciantes
1. **Comece pelo Básico:** Não pule etapas, construa base sólida
2. **Pratique Comandos Git:** Use linha de comando além de interfaces gráficas
3. **Leia Documentação:** GitHub Actions tem excelente documentação
4. **Teste Localmente:** Sempre teste antes de fazer commit

### Para Intermediários
1. **Foque na Integração:** Como as ferramentas trabalham juntas
2. **Automatize Tudo:** Se você fez manualmente, pode ser automatizado
3. **Monitore Performance:** Acompanhe tempo de execução dos workflows
4. **Implemente Segurança:** Nunca commite credenciais

### Para Avançados
1. **Pense em Escala:** Como sua solução funcionaria com 10x o tamanho
2. **Otimize Recursos:** Cache, paralelização, resource limits
3. **Implemente Observabilidade:** Logs, métricas, alertas
4. **Considere Custos:** GitHub Actions tem limites e custos

## Suporte e Dúvidas

### Canais de Comunicação
- **Fórum da Disciplina:** Para dúvidas gerais e discussões
- **Email Professor:** Para questões específicas ou problemas técnicos
- **Discord/Slack:** Para comunicação rápida e peer support
- **Office Hours:** Segundas e quartas, 14h-16h

### FAQ - Perguntas Frequentes

**Q: Meu workflow GitHub Actions não está executando, o que fazer?**
A: Verifique se está na branch correta, se o arquivo YAML está em `.github/workflows/`, e se não há erros de sintaxe.

**Q: Como debuggar um erro no workflow?**
A: Use o tab "Actions" no GitHub, clique no workflow com erro e examine os logs detalhados de cada step.

**Q: Posso usar ferramentas além das mencionadas?**
A: Sim, mas documente a justificativa e garanta que atende aos objetivos do exercício.

**Q: Como colaborar com colegas nos exercícios de nível 3?**
A: Grupos de até 3 pessoas são permitidos para nível 3. Documente a contribuição de cada membro.

**Q: Onde encontro exemplos de workflows complexos?**
A: Examine repositórios populares no GitHub, muitos têm workflows públicos como referência.

---

**Bom trabalho e que os exercícios fortaleçam seu domínio em Git e CI/CD!** 🚀

**Última Atualização:** Janeiro 2025  
**Versão:** 1.0
