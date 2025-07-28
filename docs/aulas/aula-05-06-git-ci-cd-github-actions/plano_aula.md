# Plano de Aula 3: Git e CI/CD com GitHub Actions

## Informações Gerais

**Disciplina:** Programação Orientada a Objetos Avançada  
**Aula:** 03  
**Título:** Git e CI/CD com GitHub Actions  
**Carga Horária:** 4 horas (240 minutos)  
**Modalidade:** Híbrida (2h teórica + 2h prática)  
**Professor:** Jackson Antonio do Prado Lima  

## Objetivos de Aprendizagem

### Objetivo Geral
Capacitar os estudantes a implementar práticas avançadas de controle de versão com Git e automação de CI/CD usando GitHub Actions, aplicando conceitos de DevOps e engenharia de software moderna para desenvolvimento colaborativo e entrega contínua de aplicações Python orientadas a objetos.

### Objetivos Específicos

Ao final desta aula, o estudante será capaz de:

1. **Aplicar Git Avançado:**
   - Implementar estratégias de branching (Git Flow, GitHub Flow)
   - Realizar merge e rebase de forma estratégica
   - Resolver conflitos complexos de merge
   - Utilizar hooks do Git para automação

2. **Dominar GitHub Actions:**
   - Criar workflows de CI/CD completos
   - Implementar matrix strategies para testes multiplataforma
   - Configurar ambientes e secrets de forma segura
   - Desenvolver actions customizadas

3. **Implementar CI/CD:**
   - Configurar pipelines de integração contínua
   - Automatizar testes, build e deploy
   - Implementar estratégias de deploy (blue-green, canary)
   - Monitorar e otimizar pipelines

4. **Aplicar DevOps:**
   - Integrar práticas de Infrastructure as Code
   - Implementar observabilidade e monitoramento
   - Aplicar princípios de segurança em pipelines
   - Medir e otimizar performance de delivery

## Conteúdo Programático

### 1. Fundamentos Avançados de Git (60 min)

#### 1.1 Arquitetura Distribuída e Modelo de Dados
- Estrutura interna do Git (objects, refs, index)
- Diferenças entre Git e sistemas centralizados
- Modelo de dados baseado em DAG (Directed Acyclic Graph)
- Performance e otimizações do Git

#### 1.2 Estratégias de Branching
- **Git Flow:** feature, develop, release, hotfix branches
- **GitHub Flow:** simplicidade para deploy contínuo
- **GitLab Flow:** ambiente-specific branches
- Comparação e critérios de escolha

#### 1.3 Operações Avançadas
- Interactive rebase para história limpa
- Cherry-pick para mudanças específicas
- Bisect para debugging histórico
- Subtrees e submodules para projetos grandes

#### 1.4 Colaboração e Code Review
- Pull Request workflows
- Code review efetivo
- Políticas de proteção de branch
- Integração com ferramentas de qualidade

### 2. CI/CD: Conceitos e Implementação (80 min)

#### 2.1 Fundamentos de CI/CD
- **Continuous Integration:** princípios e benefícios
- **Continuous Delivery vs Deployment:** diferenças críticas
- Pipeline stages: build, test, deploy, monitor
- Métricas DORA para DevOps excellence

#### 2.2 Design de Pipelines
- Pipeline as Code com YAML
- Paralelização e dependências entre jobs
- Artifact management e caching
- Error handling e retry strategies

#### 2.3 Testing na Pipeline
- Unit tests automatizados
- Integration e E2E testing
- Performance e security testing
- Code quality gates

#### 2.4 Deployment Strategies
- **Blue-Green Deployment:** zero-downtime releases
- **Canary Releases:** gradual rollout
- **Rolling Updates:** continuous availability
- **Feature Flags:** decoupled deployment

### 3. GitHub Actions: Plataforma e Práticas (60 min)

#### 3.1 Arquitetura do GitHub Actions
- Workflow engine e execution model
- Runners: hosted vs self-hosted
- Actions marketplace e ecosystem
- Security model e permissions

#### 3.2 Workflow Development
- Events e triggers avançados
- Jobs e steps organization
- Matrix strategies para testing
- Conditional execution

#### 3.3 Advanced Features
- Custom actions development
- Composite actions para reutilização
- Docker container actions
- JavaScript actions

#### 3.4 Security e Compliance
- Secrets management best practices
- OIDC integration para cloud providers
- Supply chain security
- Audit logs e compliance

### 4. Implementação Prática: Sistema Empresarial (40 min)

#### 4.1 Projeto Integrador
- Sistema de Gerenciamento de Tarefas
- Arquitetura full-stack (FastAPI + React)
- Infraestrutura como código
- Monitoramento e observabilidade

#### 4.2 Pipeline Completo
- Multi-stage pipeline
- Automated testing strategy
- Security scanning integration
- Production deployment automation

## Metodologia

### Estratégias Pedagógicas

1. **Aula Expositiva Interativa (60 min)**
   - Apresentação dos conceitos fundamentais
   - Demonstrações práticas ao vivo
   - Discussão de casos reais da indústria
   - Q&A contínuo

2. **Hands-on Practice (120 min)**
   - Laboratório guiado com projeto real
   - Implementação step-by-step
   - Resolução de problemas em grupo
   - Code review entre pares

3. **Projeto Aplicado (60 min)**
   - Implementação de pipeline completo
   - Integração de todas as ferramentas
   - Análise de métricas e otimização
   - Apresentação de resultados

### Recursos Didáticos

- **Slides Interativos:** Conceitos e diagramas
- **Live Coding:** Demonstração prática
- **Laboratório Virtual:** Ambiente pré-configurado
- **Projeto Template:** Base para exercícios
- **Dashboard Metrics:** Visualização em tempo real

## Avaliação

### Critérios de Avaliação

| Componente | Peso | Descrição |
|------------|------|-----------|
| **Participação** | 20% | Engajamento e qualidade das contribuições |
| **Exercícios Práticos** | 40% | Implementação correta dos exercícios |
| **Projeto Integrador** | 30% | Pipeline completo funcionando |
| **Code Review** | 10% | Qualidade do feedback entre pares |

### Rubrica Detalhada

#### Exercícios Práticos (40%)
- **Excelente (9-10):** Pipeline completo, testes passando, deploy automático
- **Bom (7-8):** Pipeline funcional, pequenos ajustes necessários
- **Satisfatório (6-7):** Conceitos corretos, implementação parcial
- **Insatisfatório (0-5):** Conceitos incorretos ou não implementados

#### Projeto Integrador (30%)
- **Excelente (9-10):** Sistema completo, CI/CD otimizado, métricas positivas
- **Bom (7-8):** Sistema funcional, pipeline completo, boas práticas
- **Satisfatório (6-7):** Sistema básico, pipeline simples
- **Insatisfatório (0-5):** Sistema não funcional ou incompleto

## Recursos Necessários

### Infraestrutura Técnica

1. **Computadores/Laptops**
   - Git 2.40+ instalado
   - Visual Studio Code com extensões
   - Docker Desktop
   - Node.js 18+ e Python 3.12+

2. **Contas e Acessos**
   - GitHub account com Actions habilitado
   - Docker Hub account
   - Cloud provider account (AWS/Azure/GCP)

3. **Ferramentas de Apoio**
   - Terminal/PowerShell
   - Postman ou similar para API testing
   - Browser para GitHub interface

### Material de Apoio

- **Documentação Oficial:** GitHub Actions, Git, Docker
- **Livros Digitais:** "Pro Git", "The DevOps Handbook"
- **Artigos Selecionados:** Best practices e case studies
- **Videos Tutoriais:** Complementares aos conceitos

## Cronograma Detalhado

### Primeira Parte - Teoria Fundamental (120 min)

| Tempo | Atividade | Descrição |
|-------|-----------|-----------|
| 0-15 min | **Abertura** | Objetivos, motivação, overview |
| 15-45 min | **Git Avançado** | Arquitetura, branching, operações |
| 45-60 min | **Break** | Intervalo para assimilação |
| 60-105 min | **CI/CD Conceitos** | Princípios, pipelines, estratégias |
| 105-120 min | **GitHub Actions** | Plataforma, features, segurança |

### Segunda Parte - Prática Aplicada (120 min)

| Tempo | Atividade | Descrição |
|-------|-----------|-----------|
| 120-135 min | **Setup Ambiente** | Configuração, templates, acesso |
| 135-180 min | **Lab 1: Git Flow** | Branching, merging, conflitos |
| 180-195 min | **Break** | Revisão e dúvidas |
| 195-225 min | **Lab 2: CI/CD Pipeline** | Workflow, testing, deployment |
| 225-240 min | **Projeto Final** | Integração, apresentação, feedback |

## Pré-requisitos

### Conhecimentos Necessários

1. **Git Básico**
   - Comandos fundamentais (add, commit, push, pull)
   - Conceito de repositório e branches
   - Experiência com GitHub interface

2. **Python Intermediário**
   - POO básica e packages
   - Virtual environments
   - Testing com pytest

3. **Linha de Comando**
   - Navegação em terminal
   - Execução de scripts
   - Variáveis de ambiente

4. **Desenvolvimento Web Básico**
   - Conceitos de API REST
   - HTTP status codes
   - JSON e YAML

### Preparação Prévia

**Uma Semana Antes:**
- [ ] Criar conta GitHub (se não tiver)
- [ ] Instalar Git e configurar SSH keys
- [ ] Instalar Docker Desktop
- [ ] Verificar acesso ao laboratório virtual

**Um Dia Antes:**
- [ ] Revisar comandos básicos do Git
- [ ] Testar ambiente de desenvolvimento
- [ ] Ler artigo preparatório enviado
- [ ] Preparar dúvidas específicas

## Resultados Esperados

### Competências Desenvolvidas

Ao final da aula, espera-se que o estudante demonstre:

1. **Proficiência Técnica**
   - Implementação fluente de workflows Git
   - Criação de pipelines CI/CD funcionais
   - Configuração segura de ambientes
   - Debugging e otimização de processos

2. **Pensamento DevOps**
   - Cultura de colaboração e automação
   - Foco em qualidade e feedback rápido
   - Mentalidade de melhoria contínua
   - Visão end-to-end do delivery

3. **Aplicação Prática**
   - Capacidade de aplicar conceitos em projetos reais
   - Adaptação de soluções para contextos específicos
   - Integração de múltiplas ferramentas
   - Tomada de decisões técnicas fundamentadas

### Produtos Entregues

1. **Pipeline Funcional**
   - Repositório Git com workflow completo
   - Testes automatizados passando
   - Deploy automático funcionando
   - Documentação técnica

2. **Análise de Métricas**
   - Relatório de performance do pipeline
   - Identificação de gargalos
   - Sugestões de otimização
   - ROI calculado

3. **Reflexão Crítica**
   - Análise dos desafios encontrados
   - Lições aprendidas
   - Próximos passos de aprofundamento
   - Aplicação em projetos futuros

## Bibliografia e Referências

### Bibliografia Principal

1. **Chacon, S. & Straub, B.** (2024). *Pro Git* (3rd ed.). Apress. [Disponível online: https://git-scm.com/book]

2. **Humble, J. & Farley, D.** (2023). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation* (2nd ed.). Addison-Wesley.

3. **Kim, G., Debois, P., Willis, J., & Humble, J.** (2024). *The DevOps Handbook: How to Create World-Class Agility, Reliability, & Security in Technology Organizations* (2nd ed.). IT Revolution Press.

### Bibliografia Complementar

4. **Forsgren, N., Humble, J., & Kim, G.** (2023). *Accelerate: The Science of Lean Software and DevOps* (Updated ed.). IT Revolution Press.

5. **Morris, K.** (2024). *Infrastructure as Code: Managing Servers in the Cloud* (3rd ed.). O'Reilly Media.

6. **Goll, J. & Holm, D.** (2024). *GitHub Actions in Action*. Manning Publications.

### Artigos e Recursos Online

7. **GitHub Documentation.** (2024). *GitHub Actions Documentation*. https://docs.github.com/en/actions

8. **Atlassian.** (2024). *Git Tutorials and Workflows*. https://www.atlassian.com/git/tutorials

9. **Martin Fowler.** (2024). *Continuous Integration*. https://martinfowler.com/articles/continuousIntegration.html

10. **DORA Research.** (2024). *State of DevOps Report*. https://dora.dev/

### Recursos Técnicos

11. **Git Official Documentation:** https://git-scm.com/doc
12. **Docker Documentation:** https://docs.docker.com/
13. **Python Package Index:** https://pypi.org/
14. **GitHub Actions Marketplace:** https://github.com/marketplace/actions

## Observações Finais

### Adaptações para Modalidade Remota

Em caso de aula 100% remota:
- Utilize breakout rooms para trabalho em grupos
- Implemente polling e quizzes interativos
- Grave demonstrações para revisão posterior
- Disponibilize laboratório virtual acessível

### Feedback e Melhoria Contínua

- Coleta de feedback em tempo real via formulários
- Análise de engagement através de métricas de participação
- Ajustes no cronograma baseados no progresso da turma
- Iteração contínua do conteúdo baseada em resultados

### Extensões Possíveis

Para turmas avançadas, considere adicionar:
- GitOps com ArgoCD/Flux
- Observabilidade com Prometheus/Grafana
- Security scanning avançado
- Multi-cloud deployment strategies

---

**Data de Elaboração:** Janeiro 2025  
**Versão:** 1.0  
**Próxima Revisão:** Julho 2025
