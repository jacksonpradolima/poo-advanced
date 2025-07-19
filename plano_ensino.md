# Identificação

Disciplina: Programação Orientada a Objetos II

Carga Horária – 72 horas-aula

# Ementa

* Princípios de boa prática em Orientação a Objetos:
  + Código Limpo
  + SOLID
  + YAGNI
  + DRY.
* Padrões de Projeto (design patterns).
* Refatoração de códigos.
* Integração de Programas Orientados a Objetos com banco de dados.
* Desenvolvimento de Interface de Usuário Gráfica.
* Integração de sistemas via API.

# Objetivo Geral

Capacitar o aluno a desenvolver software modular, testável, documentado e pronto para deploy, utilizando práticas modernas de desenvolvimento orientado a objetos com Python, integração com banco de dados, APIs, CI/CD, containers e visualização de dados.

# Objetivos Específicos

* Revisar princípios fundamentais de POO e boas práticas (Clean Code, SOLID, DRY, YAGNI)
* Implementar e aplicar Design Patterns clássicos em projetos reais
* Integrar sistemas via APIs RESTful.
* Integrar sistemas orientados a objetos com bancos de dados relacionais e analíticos.
* Criar interfaces gráficas desktop ou web.
* Aplicar práticas de DevOps: testes automatizados, integração contínua, containerização e deploy.
* Manipular e visualizar dados utilizando Polars.
* Explorar tópicos avançados como Retrieval-Augmented Generation (RAG) como diferencial.

# Metodologia

* Aulas práticas com desenvolvimento contínuo em laboratório
* Estudo de caso e projetos com aplicação real
* Utilização de ferramentas e fluxos do mercado (CI/CD, Docker, GitHub)
* Revisões e sessões de code review
* Apresentações orais e feedbacks entre equipes

Ferramentas e Tecnologias

* Linguagem: Python 3.12+
* Banco de dados: PostgreSQL e DuckDB
* DataFrames: Polars
* API: FastAPI + httpx/asyncio
* GUI: Tkinter, Streamlit ou Web (opcional)
* Testes: pytest, pytest-mock
* Análise: Postman, OpenAPI
* Extras: pydantic, dataclasses, tqdm, rich

# Avaliação

|  |  |
| --- | --- |
| **Componente** | **Peso** |
| Checkpoint 1: Projeto Pacial | 50% |
| Checkpoint 2: Projeto Final | 50% |

Critérios considerados:

* Qualidade e boas práticas de POO
* Testes automatizados e cobertura
* CI/CD funcional
* Documentação adequada
* Containerização e deploy
* Qualidade da apresentação final

Deve:

* Ter arquitetura orientada a objetos com SOLID
* Persistir dados em banco de dados
* Fazer análise com Polars (quando aplicável)
* Expor ou consumir APIs REST
* Aplicar design patterns
* Testes automatizados com pytest
* Ter logs, manipulação de erros, e documentação

# Conteúdo Programático

|  |  |  |
| --- | --- | --- |
| **Aula** | **Tema** | **Entregas / Observações** |
| **1º Bimestre – De Código Limpo a APIs Profissionais: Fundamentos, Testes e Banco de Dados** | | |
| 1-2 | * Apresentação da Disciplina * Boas Práticas e Design Patterns Clássicos | * SOLID, DRY, YAGNI, KISS, Coesão x Acoplamento * Patterns clássicos (Strategy, Factory, Singleton, etc.) |
| 3-4 | Ambiente profissional de projetos Python | * Projeto inicial no GitHub (empty template) * uv ou poetry para ambientes isolados * Configuração de projeto com pyproject.toml * Documentação com pdoc * Testes com pytest, cobertura com pytest-cov e benchmark com pytest-benchmark |
| 5-6 | Git e CI/CD com GitHub Actions | * Git e commits semânticos (conventional commits) * Introdução   Workflow com:   * Linting (pre-commit) * pre-commit com mypy e ruff * Testes (pytest) * Coverage + Build do pacote |
| 7-8 | Refatoração de Códigos | * Code smells e refatoração incremental * Refatoração de Software (tipos e atores) * Sonarcloud (CI) * Refatoração baseada em TDD |
| 9-14 | Construção e Consumo de APIs REST | * Definição * Criação de APIs com [**FastAPI**](https://github.com/fastapi/full-stack-fastapi-template) (simples) * Criação de rotas, validação com pydantic * Retorno estruturado, tratamento de erros * Consumo com httpx, asyncio, backoff, e testes com responses * Consumo de APIs externas com caching local * Uso do Postman * Geração de OpenAPI |
| 15-20 | Integração com Banco de Dados | * PostgreSQL e DuckDB * ORM básico com dataclasses + SQL * Pyarrow * Uso de testcontainers |
| **2º Bimestre – Pipeline Profissional: Deploy, Orquestração e Visualização de Dados** | | |
| 21-22 | Manipulação de Dados com Polars | * Leitura, transformação, agregações * Integração entre objetos e DataFrames * Dashboards com plotly * ETL básico |
| 23-27 | Interface de Usuário (GUI/Web) | * Construção de GUI com Tkinter ou PySide6 * Alternativa: mini dashboard com Streamlit * Conectar GUI com API Rest e DuckDB |
| 28-32 | Containerização, Orquestração e CI/CD completo com build e push de imagem | * Docker e uvicorn para deploy local * Docker Compose com persistência e testes * Volume persistente + testes em Docker * GitHub Actions com Docker (deploy) * Deploy em Netlify e Render |
| 33-34 | Tópicos Avançados: RAG (Retrieval-Augmented Generation) | * Exemplos com OpenAI/LLM simulados ou locais (ollama) * Fundamentos de RAG (Retrieval-Augmented Generation) * [**Implementando RAG utilizando Vector Search no Azure Cosmos DB**](https://github.com/waltercoan/reactor2025-rag-cosmosdb) |
| 35-36 | Apresentações finais | Slides, live demo, justificativas |
|  | Exame |  |

A seguir, o **detalhamento** dos blocos.

**Detalhamento das Aulas**

## Aula 1 - Apresentação da Disciplina, Boas Práticas e Design Patterns Clássicos

### Objetivo Geral:

* Introduzir a disciplina de Programação Orientada a Objetos II (POOII), contextualizando os objetivos do semestre e as competências a serem desenvolvidas. Revisar e aprofundar os princípios de boas práticas em desenvolvimento orientado a objetos, explorando padrões de design clássicos que favorecem a manutenção, a extensibilidade e a legibilidade do software.

### Objetivos Específicos:

* Apresentar o plano de ensino, a metodologia de avaliação e o cronograma detalhado do curso.
* Reforçar os princípios de boas práticas como SOLID, DRY, YAGNI e KISS.
* Discutir a importância da coesão e do acoplamento baixo na modelagem orientada a objetos.
* Estudar e implementar padrões de design clássicos como Strategy, Factory, Singleton, Observer, Adapter e Command.
* Estimular a compreensão sobre como o uso consciente de padrões contribui para a escalabilidade e manutenção de sistemas complexos.

### Conteúdo Programático:

* Apresentação da disciplina:
  + Objetivos gerais e específicos.
  + Metodologia de ensino e formas de avaliação.
  + Apresentação do projeto integrador que será desenvolvido durante o semestre.
* Revisão dos princípios de boas práticas:
  + SOLID:
    - Single Responsibility Principle.
    - Open/Closed Principle.
    - Liskov Substitution Principle.
    - Interface Segregation Principle.
    - Dependency Inversion Principle.
  + DRY (Don't Repeat Yourself).
  + YAGNI (You Aren't Gonna Need It).
  + KISS (Keep It Simple, Stupid).
  + Coesão e Acoplamento.
* Padrões de Design:
  + Comportamentais: Strategy, Observer, Command.
  + Criacionais: Factory Method, Singleton.
  + Estruturais: Adapter.
  + Exemplos práticos de aplicação.

### Metodologia:

* A aula será dividida em dois momentos principais. No primeiro, será feita a apresentação formal da disciplina, do plano de ensino, do método de avaliação e do projeto integrador que será desenvolvido durante o semestre.
* Em seguida, será feita uma revisão aprofundada dos princípios de boas práticas. O professor utilizará exemplos de código ruins (com smells evidentes) e, gradativamente, refatorará esses exemplos ao vivo para demonstrar como aplicar os princípios de SOLID, DRY, YAGNI e KISS.
* Será feita uma discussão interativa com os alunos sobre experiências prévias com código mal estruturado e como boas práticas poderiam ter evitado problemas de manutenção e evolução.
* Após a revisão dos princípios, o professor introduzirá os padrões de design com exemplos clássicos e cotidianos que justifiquem o seu uso. Cada padrão será exemplificado com problemas reais do desenvolvimento de software e como o padrão proposto resolve ou mitiga esses problemas.
* Os alunos serão organizados em grupos para elaborar pequenos exemplos de aplicação dos padrões discutidos, promovendo um ambiente de aprendizagem colaborativa.
* Para consolidar o conhecimento, cada aluno deverá implementar ao menos dois padrões de design em um repositório pessoal no GitHub, que será utilizado ao longo do semestre para acompanhamento do progresso.
* O encerramento da aula será marcado por uma breve reflexão coletiva sobre a importância dos padrões de design e boas práticas na trajetória de um desenvolvedor profissional, relacionando o conteúdo com o que será abordado nas próximas aulas.

## Aula 2 - Ambiente Profissional de Projetos Python

### Objetivo Geral:

* Capacitar os alunos a configurarem um ambiente de desenvolvimento Python profissional e moderno, alinhado às práticas utilizadas por equipes de engenharia de software no mercado. A aula visa criar uma base sólida de ferramentas e configurações que garantam qualidade de código, segurança, organização de dependências e documentação técnica desde o início do projeto.

### Objetivos Específicos:

* Introduzir o uso de ambientes virtuais para isolar dependências de projetos Python.
* Configurar ambientes com uv e poetry para controle de pacotes e versões.
* Estabelecer fluxos de linting e análise estática de código com ruff e mypy.
* Implementar hooks automáticos de pre-commit para garantir qualidade antes do versionamento.
* Configurar documentação automática com pdoc.
* Criar testes unitários básicos com pytest e medir cobertura com pytest-cov.
* Registrar o projeto inicial no GitHub, configurando um repositório versionado adequadamente.

### Conteúdo Programático:

* Ambientes Virtuais:
  + O que são, importância e criação com uv.
  + Alternativa com poetry e comparativo.
* pyproject.toml:
  + Estrutura e gerenciamento centralizado de dependências.
* Ferramentas de Qualidade de Código:
  + Ruff: configuração e execução.
  + Mypy: introdução à tipagem estática.
* Hooks de pre-commit:
  + Configuração do pre-commit com ruff, mypy e black.
  + Execução automática de qualidade antes de commits.
* Documentação com pdoc:
  + Geração automática de documentação a partir de docstrings.
* Testes e Benchmark:
  + Introdução ao pytest.
  + pytest-cov para medir cobertura de testes.
  + pytest-benchmark para medir performance de funções.
* Registro do projeto no GitHub.

### Metodologia:

* Exposição teórica inicial com apresentação de ferramentas modernas de desenvolvimento Python.
* Demonstração prática do professor criando um ambiente completo desde o zero.
* Atividade prática guiada: cada aluno criará o seu ambiente virtual, instalará dependências e configurará as ferramentas de linting e tipagem.
* Implementação prática de pre-commit configurando as ferramentas de qualidade.
* Exercício prático: desenvolvimento de funções básicas e escrita dos primeiros testes unitários com pytest.
* Geração de documentação com pdoc para o projeto criado.
* Criação e configuração de repositório no GitHub para versionamento do projeto.
* Reflexão em grupo sobre os benefícios do ambiente profissional configurado, especialmente para equipes distribuídas.
* Como tarefa de casa, cada aluno deverá concluir a documentação inicial do projeto e escrever ao menos 3 testes adicionais para funções criadas.

## Aula 3 - Git e CI/CD com GitHub Actions

### Objetivo Geral:

* Capacitar os alunos a utilizar o sistema de controle de versão Git de maneira eficiente e profissional, integrando workflows de integração contínua (CI) com GitHub Actions. O objetivo é que os alunos compreendam como versionar código com qualidade, adotando práticas de commits semânticos e estabelecendo pipelines automáticos para validação, testes e build dos projetos.

### Objetivos Específicos:

* Reforçar o entendimento e prática de versionamento com Git.
* Aplicar boas práticas de commit semântico com Conventional Commits.
* Configurar GitHub Actions para executar workflows automáticos de linting, testes e builds.
* Automatizar verificação de cobertura de testes e benchmarks de performance.
* Integrar pipelines CI/CD para reforçar qualidade e confiabilidade do software.

### Conteúdo Programático:

* Revisão prática de Git:
  + Comandos essenciais: clone, add, commit, push, pull, branch.
  + Gitflow básico e alternativas de branching strategy.
* Commits Semânticos:
  + Padrão Conventional Commits.
  + Ferramentas para padronização de mensagens de commit.
* GitHub Actions:
  + Estrutura de workflows: jobs, steps, runners.
  + Exemplos de automação: linting com pre-commit, testes com pytest, cobertura com pytest-cov.
  + Build do pacote Python.
  + Execução de benchmarks automáticos com pytest-benchmark.
* Configuração de badge de cobertura e build status no README.md.

### Metodologia:

* A aula será iniciada com uma revisão prática dos comandos mais importantes do Git, reforçando conceitos de versionamento distribuído.
* O professor irá demonstrar exemplos práticos de fluxos de commit e merge, destacando a importância dos commits semânticos e como eles facilitam a automação e o controle de mudanças.
* Cada aluno será orientado a configurar o Conventional Commits no repositório pessoal utilizando ferramentas como Commitizen ou commitlint.
* Após a configuração do fluxo de commits, iniciaremos a configuração dos pipelines de CI/CD com GitHub Actions.
* Atividade prática guiada: criação de um workflow básico para executar linting e testes unitários automaticamente a cada push e pull request.
* Em seguida, o workflow será estendido para incluir geração de relatório de cobertura de testes, execução de benchmarks de funções críticas e build do pacote do projeto.
* Os alunos também configurarão o badge de status de build e cobertura no README.md do projeto.
* Durante a prática, o professor destacará problemas comuns em pipelines CI/CD e como diagnosticar e resolver.
* Para consolidar o aprendizado, cada aluno deverá configurar o pipeline completo e demonstrar o funcionamento via push de código no GitHub.
* Como exercício complementar, os alunos deverão explorar a possibilidade de configurar jobs paralelos em workflows e cache de dependências para acelerar builds.
* Finalização com discussão sobre a importância do CI/CD no mercado atual, especialmente em ambientes ágeis e de DevOps, e reflexões sobre como isso impacta a qualidade do software entregue.

## Aula 4 - Refatoração de Códigos, Code Smells e Integração com SonarCloud

### Objetivo Geral:

* Capacitar os alunos a identificar deficiências de qualidade em sistemas orientados a objetos por meio da identificação de code smells e a aplicar técnicas sistemáticas de refatoração. Além disso, introduzir o uso de ferramentas de análise contínua de qualidade de código, com destaque para o SonarCloud, integrado aos pipelines CI/CD estabelecidos anteriormente.

### Objetivos Específicos:

* Compreender o conceito de code smells e sua influência na manutenção e evolução de sistemas.
* Aplicar técnicas de refatoração incremental para eliminação de code smells.
* Revisar conceitos de refatoração de software baseados em tipos e atores.
* Introduzir e configurar o SonarCloud para análise contínua de qualidade do código.
* Integrar o SonarCloud ao pipeline do GitHub Actions para inspeção automatizada.
* Consolidar o uso do TDD (Test-Driven Development) para apoiar a refatoração segura de código.

### Conteúdo Programático:

* Introdução aos Code Smells:
  + Tipos comuns: métodos longos, classes grandes, code duplication, data clumps, long parameter list, feature envy.
  + Exemplos práticos de cada tipo de smell.
* Técnicas de Refatoração:
  + Refatoração incremental.
  + Extração de métodos e classes.
  + Redução de complexidade ciclomática.
  + Aplicação de padrões de design como mecanismo de refatoração.
* TDD e Refatoração:
  + Revisão prática do ciclo Red-Green-Refactor.
  + Exemplos práticos com pytest.
* Ferramentas de Análise Estática:
  + SonarCloud: configuração, integração com GitHub, interpretação de métricas.
  + Outras ferramentas complementares: pylint, flake8.
* Integração do SonarCloud no GitHub Actions.

### Metodologia:

* A aula será iniciada com uma explicação teórica sobre o conceito de code smells, apoiada em exemplos de projetos reais ou legados para ilustrar os impactos negativos na manutenção de código.
* O professor conduzirá uma revisão das técnicas de refatoração incremental, explicando passo a passo como refatorar sem alterar o comportamento externo do software.
* Serão apresentados casos práticos para aplicação de técnicas de refatoração e aplicação de padrões de design como estratégia para resolver problemas estruturais.
* Cada aluno será desafiado a identificar code smells em um projeto de exemplo previamente fornecido.
* Em seguida, os alunos deverão propor e aplicar refatorações no código, guiados por testes automatizados, reforçando a prática de TDD.
* O professor demonstrará a configuração do SonarCloud com integração ao GitHub Actions, mostrando como as análises de qualidade serão executadas automaticamente a cada commit.
* Os alunos replicarão a configuração do SonarCloud em seus próprios repositórios, validando o pipeline e interpretando os relatórios gerados.
* Durante a prática, será estimulada a análise crítica dos relatórios do SonarCloud para compreensão dos principais indicadores de qualidade: cobertura de testes, duplicidade de código, vulnerabilidades, bugs e code smells.
* Atividade de laboratório: cada aluno deverá entregar um relatório das refatorações aplicadas, as melhorias percebidas nas métricas do SonarCloud e o antes/depois das principais funções refatoradas.
* Encerramento com uma roda de conversa sobre o papel contínuo da refatoração no ciclo de vida do software e o impacto da qualidade de código em equipes ágeis.
* Como tarefa complementar, os alunos deverão escolher uma função ou classe do projeto pessoal para aplicar refatorações adicionais, documentando as decisões técnicas e os benefícios percebidos.

## Aula 5 a 7 - Construção e Consumo de APIs REST com FastAPI

### Objetivo Geral:

* Capacitar os alunos a projetar, construir e consumir APIs RESTful utilizando o framework FastAPI em Python. A ênfase será no desenvolvimento de APIs robustas, seguras, documentadas automaticamente e com práticas modernas de desenvolvimento orientado a objetos e validação de dados. Ao final destas aulas, os alunos deverão ser capazes de criar APIs completas e consumir serviços externos de forma eficiente.

### Objetivos Específicos:

* Compreender os princípios fundamentais das APIs REST.
* Aprender a criar rotas RESTful utilizando o framework FastAPI.
* Implementar validação de dados com Pydantic.
* Tratar erros e criar retornos estruturados.
* Implementar consumo de APIs externas com httpx e técnicas de retry/backoff.
* Utilizar Postman para testar e documentar APIs manualmente.
* Integrar práticas de caching para otimizar consumo de APIs externas.
* Gerar documentação automática via OpenAPI.

### Conteúdo Programático:

* Definição e Princípios de APIs REST:
  + Operações CRUD mapeadas em verbos HTTP.
  + Statelessness, Cacheability, Layered System.
* Introdução ao FastAPI:
  + Instalação e configuração inicial.
  + Criação de rotas com path, query e body parameters.
* Pydantic para Validação de Dados:
  + Definição de schemas para requests e responses.
  + Validações complexas e customizadas.
* Tratamento de Erros:
  + Exception Handlers.
  + Formatação de erros consistentes.
* Consumo de APIs Externas:
  + Uso de httpx com suporte assíncrono.
  + Técnicas de retry, backoff e timeout.
* Caching Local de Requisições:
  + Implementação de caching simples para respostas de APIs.
* Testes e Exploração de APIs com Postman.
* Geração e Exploração da Documentação OpenAPI.

### Metodologia:

* As três aulas serão conduzidas de forma prática, com breves exposições teóricas seguidas de exemplos práticos implementados ao vivo pelo professor.
* Iniciaremos com a criação de uma API simples para um domínio de exemplo escolhido coletivamente (ex: sistema de biblioteca, inventário ou gestão de tarefas).
* Cada conceito será introduzido de forma incremental, com aplicação prática imediata pelos alunos em seus projetos.
* Haverá um exercício prático em que cada aluno deverá:
  + Criar rotas GET, POST, PUT, DELETE.
  + Implementar validação com Pydantic.
  + Tratar erros de forma customizada.
* No segundo momento, os alunos implementarão o consumo de uma API externa pública, aplicando técnicas de retry e caching local.
* Será proposta uma atividade prática utilizando o Postman para testar todas as rotas criadas, incluindo testes de diferentes payloads e verificações de status codes.
* Os alunos também deverão explorar a documentação automática do FastAPI gerada via OpenAPI e aprimorá-la com descrições adicionais.
* A prática será consolidada com um exercício integrador: criar uma API que consuma outra API pública (ex.: API de clima, moedas ou localização), armazene os dados localmente e exponha um endpoint para consulta otimizada com caching.
* Os alunos receberão como desafio opcional a implementação de autenticação básica na API com tokens simples.
* Ao final do ciclo de três aulas, haverá uma revisão coletiva com cada aluno apresentando o funcionamento da sua API e os aprendizados adquiridos.
* Checklist de entrega: repositório com a API criada, documentação gerada, exemplos de consumo de APIs externas, scripts de caching e testes realizados no Postman.

## Aula 8 a 10 - Integração com Banco de Dados: PostgreSQL e DuckDB

### Objetivo Geral:

* Capacitar os alunos a integrar as APIs desenvolvidas com bancos de dados relacionais e analíticos, especificamente PostgreSQL e DuckDB. O foco dessas aulas é consolidar os conhecimentos sobre persistência de dados, modelagem de entidades, operações CRUD diretamente no banco, além de análises rápidas com DuckDB, integrando essas ferramentas com as APIs REST criadas anteriormente.

### Objetivos Específicos:

* Configurar conexões entre aplicações Python e bancos de dados PostgreSQL e DuckDB.
* Implementar modelos de dados com SQLAlchemy, ORM mais popular no ecossistema Python.
* Realizar operações CRUD diretamente conectadas ao banco de dados.
* Integrar DuckDB para consultas analíticas rápidas diretamente em arquivos ou dataframes.
* Aprender a escrever consultas SQL complexas integradas com APIs.
* Utilizar Testcontainers para criação de bancos temporários para testes automatizados.

### Conteúdo Programático:

* Introdução ao PostgreSQL:
  + Conceitos básicos e diferenciais do PostgreSQL.
  + Comandos essenciais de SQL: CREATE, SELECT, INSERT, UPDATE, DELETE.
* SQLAlchemy:
  + Criação de modelos ORM.
  + Mapeamento objeto-relacional.
  + Sessões e transações.
* Integração da API com o PostgreSQL:
  + Persistência dos dados recebidos via endpoints.
  + Recuperação de informações diretamente do banco.
* DuckDB:
  + Leitura de dados analíticos direto de arquivos Parquet ou CSV.
  + Consultas SQL integradas com Polars.
  + Casos de uso para análises rápidas.
* Testcontainers para PostgreSQL:
  + Introdução ao conceito.
  + Criação de ambientes temporários para testes.
* Exercícios de integração completa API + Banco.

### Metodologia:

* O professor apresentará inicialmente o papel de um banco de dados relacional no contexto de APIs, destacando vantagens e cenários de uso.
* Em laboratório, será demonstrada a instalação e configuração do PostgreSQL localmente, além da introdução prática ao SQL.
* Atividade prática: cada aluno criará um banco de dados PostgreSQL para seu projeto, modelando as tabelas necessárias com SQLAlchemy.
* Os alunos modificarão suas APIs para persistir os dados em banco de forma transacional.
* No segundo momento, será introduzido o DuckDB, com exemplos práticos de consulta a datasets analíticos, simulando cenários de BI e análises rápidas.
* Exercício prático: implementar um endpoint na API que execute consultas analíticas via DuckDB e devolva insights pré-processados.
* Introdução aos Testcontainers será feita através de um exemplo guiado, permitindo que os alunos criem bancos de dados isolados para testes automatizados.
* Cada aluno realizará testes de integração garantindo que sua API persista, recupere e manipule dados de forma consistente.
* Como atividade de aprofundamento, será proposto um desafio: criar uma pequena rotina ETL (Extract, Transform, Load) utilizando DuckDB e Polars, transformando dados persistidos em insights consumíveis pela API.
* Ao final do ciclo de três aulas, cada aluno deverá entregar:
  + Código da API com persistência em banco.
  + Endpoint analítico com DuckDB.
  + Scripts de criação e migração de banco.
  + Testes automatizados com Testcontainers.
* O ciclo será finalizado com uma apresentação prática dos sistemas persistentes e análises implementadas.

## Aula 11 - Manipulação de Dados com Polars

### Objetivo Geral:

* Desenvolver nos alunos a capacidade de manipulação, transformação e análise de dados em Python utilizando a biblioteca Polars, reconhecida por sua alta performance e concorrência otimizada em relação ao Pandas. Esta aula foca na integração de Polars com DuckDB e PostgreSQL, promovendo uma abordagem prática para construção de pipelines de dados que podem ser consumidos por APIs ou sistemas de visualização.

### Objetivos Específicos:

* Compreender as vantagens do Polars em comparação ao Pandas para manipulação de grandes volumes de dados.
* Aprender a criar DataFrames com Polars a partir de diferentes fontes de dados, incluindo arquivos Parquet, CSV e consultas a bancos.
* Realizar operações de transformação, filtragem, agregações e joins entre DataFrames.
* Integrar Polars com DuckDB para consultas analíticas SQL sobre DataFrames em memória.
* Implementar pipelines ETL simples utilizando Polars e DuckDB.
* Exportar dados processados para formatos otimizados como Parquet.

### Conteúdo Programático:

* Introdução ao Polars:
  + Arquitetura: Lazy vs Eager Evaluation.
  + Comparativo com Pandas.
* Operações com Polars:
  + Criação de DataFrames.
  + Seleção, filtragem, transformação de colunas.
  + GroupBy e Window Functions.
  + Joins entre DataFrames.
* Integração com DuckDB:
  + Execução de queries SQL sobre DataFrames em memória.
  + Composição de análises analíticas via DuckDB + Polars.
* Pipeline de Dados ETL:
  + Extração de dados do PostgreSQL.
  + Transformação dos dados com Polars.
  + Carregamento dos resultados para armazenamento em Parquet.
* Exportação de dados para uso em APIs ou visualização.

### Metodologia:

* A aula iniciará com uma explanação teórica sobre o problema da manipulação eficiente de dados em Python, especialmente quando lidando com grandes volumes.
* O professor demonstrará benchmarks simples que evidenciem a superioridade do Polars em cenários específicos em relação ao Pandas.
* Em seguida, cada aluno criará DataFrames a partir de datasets reais disponibilizados (exemplos: dados meteorológicos, dados de mobilidade urbana ou séries temporais econômicas).
* Os alunos realizarão operações práticas de filtragem, agregação, transformação de colunas e fusão de DataFrames.
* Atividade prática orientada: implementar uma rotina de extração de dados do PostgreSQL, transformar as informações com Polars e salvar o resultado em arquivo Parquet.
* Em seguida, os alunos aprenderão a executar consultas SQL sobre os DataFrames com DuckDB, integrando a linguagem SQL à manipulação funcional com Polars.
* Será proposto um exercício prático desafiador: construir um pipeline completo de ETL que extrai dados brutos, transforma os dados com regras de negócio aplicadas e gera um output otimizado para ser servido via API ou visualizado.
* Reflexão coletiva sobre os benefícios de pipelines de dados performáticos e suas aplicações em sistemas reais.
* Como atividade de extensão, os alunos poderão integrar o pipeline criado diretamente com um endpoint na API desenvolvida previamente, permitindo a geração de relatórios sob demanda.
* Checklist de entrega:
  + Código do pipeline ETL completo.
  + DataFrames intermediários e finais.
  + Arquivos exportados em Parquet.
  + Scripts SQL aplicados via DuckDB.

## Aula 12 e 13 - Interface de Usuário (GUI/Web): Tkinter, PySide6 e Streamlit para Consumo de APIs

### Objetivo Geral:

* Capacitar os alunos no desenvolvimento de interfaces gráficas e aplicações web interativas utilizando Tkinter, PySide6 e Streamlit, integradas às APIs RESTful previamente desenvolvidas. As aulas têm como objetivo oferecer uma compreensão prática de como construir camadas de apresentação para sistemas orientados a objetos, possibilitando a interação intuitiva com dados e funcionalidades disponibilizadas pelas APIs.

### Objetivos Específicos:

* Compreender o papel das interfaces gráficas em sistemas computacionais.
* Diferenciar interfaces desktop de soluções web interativas.
* Construir interfaces utilizando Tkinter e PySide6.
* Desenvolver dashboards e aplicações web com Streamlit.
* Integrar o consumo de APIs REST dentro das interfaces gráficas e web.
* Implementar operações CRUD completas diretamente pela interface.
* Aplicar boas práticas de separação de responsabilidades entre GUI, lógica de negócio e consumo de APIs.

### Conteúdo Programático:

* Fundamentos de UX/UI aplicados ao desenvolvimento de interfaces.
  + Conceitos de UX/UI básicos.
  + Arquitetura MVC para separação de responsabilidades.
* Tkinter:
  + Widgets principais: Label, Button, Entry, Treeview.
  + Criação de janelas e widgets básicos.
  + Layouts, eventos e callbacks.
* PySide6:
  + Introdução ao framework Qt.
  + Criação de janelas modernas e responsivas.
  + Manipulação de eventos, sinais e slots.
  + Customização de estilos e componentes avançados.
* Streamlit:
  + Desenvolvimento rápido de dashboards interativos.
  + Manipulação de inputs, visualização de tabelas e gráficos.
  + Exibição de gráficos com Plotly e visualização de dados.
* Consumo de APIs REST:
  + Integração com httpx para operações CRUD.
  + Exibição e atualização de informações em tempo real.
* Boas práticas de arquitetura para interfaces.
* Estruturação de projetos GUI integrados com back-end.

### Metodologia:

* As aulas serão iniciadas com uma contextualização teórica sobre o papel das interfaces em sistemas, destacando a importância da usabilidade e da experiência do usuário.
* O professor demonstrará exemplos práticos com Tkinter, criando formulários simples que realizam operações CRUD através das APIs desenvolvidas.
* Em seguida, será explorado o PySide6, com foco na criação de interfaces mais modernas e customizadas, incluindo o uso de sinais e slots para comunicação entre componentes.
* Alternativamente, será apresentada a construção de dashboards e aplicações analíticas utilizando Streamlit, enfatizando a simplicidade de desenvolvimento e o potencial para aplicações de visualização de dados.
* Atividades práticas:
  + Cada aluno escolherá ao menos uma tecnologia (Tkinter, PySide6 ou Streamlit) para criar uma interface completa que interaja com sua API.
  + Os alunos deverão implementar funcionalidades de listagem, criação, atualização e exclusão de registros via interface.
  + Implementação de feedback visual para operações realizadas (ex.: confirmações, mensagens de erro).
* O professor orientará sobre organização do código, separando claramente as camadas de interface, lógica de negócio e consumo de APIs.
* Exercício prático avançado: incluir autenticação básica na interface, caso a API a suporte.
* Discussão coletiva sobre as vantagens e desvantagens de cada tecnologia apresentada.
* Finalização com apresentação dos projetos desenvolvidos pelos alunos, permitindo feedbacks dos colegas e professor.
* Checklist de entrega:
  + Código da interface funcional.
  + Integração completa com API.
  + Implementação de operações CRUD.
  + Boas práticas de organização e modularização.

## Aula 14 e 15 - Containerização, Orquestração e CI/CD Completo com Build, Push de Imagem e Deploy Local/Cloud

### Objetivo Geral:

* Ensinar aos alunos como empacotar, orquestrar e automatizar o ciclo completo de desenvolvimento, build, testes, integração e deploy utilizando Docker, Docker Compose e pipelines CI/CD com GitHub Actions. Além disso, capacitar os alunos a realizar o deploy local com Docker e uvicorn, configurar volume persistente para bancos de dados, realizar testes em ambiente containerizado, e explorar alternativas de deploy em nuvem como Netlify e Render.

### Objetivos Específicos:

* Compreender o funcionamento do Docker e sua importância no DevOps.
* Criar Dockerfiles otimizados para APIs, bancos de dados e interfaces.
* Realizar deploy local utilizando Docker e uvicorn.
* Integrar serviços diversos em um ambiente único utilizando Docker Compose.
* Configurar volumes persistentes para bancos de dados e executar testes dentro do ambiente containerizado.
* Configurar pipelines CI/CD no GitHub Actions para build, testes, análise de qualidade e push de imagens para Docker Hub ou GitHub Container Registry.
* Implementar deploy automatizado com GitHub Actions.
* Explorar deploy de aplicações em Netlify (frontend) e Render (backend).
* Implementar boas práticas de segurança e eficiência na construção de imagens.

### Conteúdo Programático:

* Conceitos de Containerização e Orquestração:
  + Benefícios da containerização.
  + Docker vs Máquinas Virtuais.
* Docker:
  + Criação de Dockerfiles otimizados.
  + Multistage Builds.
  + Estratégias para redução de tamanho de imagem.
  + Deploy local com Docker e uvicorn.
* Docker Compose:
  + Orquestração de múltiplos serviços: API, Banco de Dados, Interface.
  + Configuração de redes privadas.
  + Persistência de dados com volumes.
  + Testes em ambiente containerizado.
* CI/CD Completo:
  + Configuração de workflows no GitHub Actions.
  + Stages: lint, testes, build de imagem, push de imagem.
  + Geração de versão semântica.
  + Push automatizado para registries Docker Hub ou GitHub Container Registry.
  + Deploy contínuo com GitHub Actions.
* Deploy em Nuvem:
  + Deploy de frontend no Netlify.
  + Deploy de backend no Render.
* Segurança e Boas Práticas:
  + Minimização de imagens.
  + Uso de usuários não-root em containers.
  + Análise estática de imagens.

### Metodologia:

* A aula será conduzida com abordagem prática e incremental, iniciando com a criação de Dockerfiles para cada serviço desenvolvido pelos alunos.
* O professor demonstrará o deploy local da API utilizando Docker e uvicorn, preparando o ambiente para testes e validações.
* Cada aluno configurará seu docker-compose.yml para orquestrar API, banco de dados com volume persistente e interface gráfica.
* Os alunos realizarão testes funcionais dentro do ambiente containerizado para validar a integração entre os serviços.
* Em paralelo, será configurado o pipeline CI/CD completo no GitHub Actions incluindo linting, testes, build de imagem, push para registry e deploy automatizado.
* Serão exploradas as ferramentas Netlify e Render para deploy em nuvem, com demonstrações práticas de publicação de frontend e backend.
* Discussão orientada sobre práticas de segurança em ambientes Docker e eficiência em builds.
* Checklist de entrega:
  + Dockerfiles otimizados.
  + docker-compose.yml funcional.
  + Pipeline CI/CD funcional no GitHub Actions.
  + Deploy local funcional com Docker e uvicorn.
  + Volume persistente configurado para o banco.
  + Imagem publicada em registry.
  + Deploy realizado em Netlify e/ou Render.
  + Documentação do processo de build, testes, deploy local e em nuvem.

## Aula 16 - Tópicos Avançados: RAG (Retrieval-Augmented Generation) com CosmosDB Vector Search

### Objetivo Geral:

* Proporcionar aos alunos um entendimento aprofundado sobre a técnica de Retrieval-Augmented Generation (RAG), capacitando-os a integrar bases de dados vetoriais com Large Language Models (LLMs) para desenvolver sistemas inteligentes que recuperem informações contextuais e aprimorem a geração de conteúdo. A aula abordará o uso do **Azure Cosmos DB com Vector Search**, técnicas de embeddings, integração com LLMs como OpenAI GPT e desenvolvimento de um pipeline completo para consultas inteligentes.

### Objetivos Específicos:

* Compreender o conceito e a arquitetura de sistemas RAG.
* Explicar o papel dos embeddings na representação semântica de documentos.
* Demonstrar o uso do Cosmos DB com Vector Search para armazenamento e recuperação vetorial.
* Construir uma pipeline RAG completa utilizando embeddings, recuperação vetorial e geração com LLM.
* Integrar o sistema RAG em uma API desenvolvida com .NET e Python via Jupyter Notebook.
* Discutir as implicações éticas, limitações e possibilidades de aplicação do RAG.

### Conteúdo Programático:

* Conceito de Retrieval-Augmented Generation (RAG)
  + Definição e aplicações práticas.
  + Diferença entre geração pura e geração com recuperação.
* Embeddings e Representação Vetorial:
  + O que são embeddings e como são gerados.
  + Modelos de embeddings (ex: OpenAI Ada Embedding).
  + Espaços multidimensionais e similaridade semântica.
* Azure CosmosDB com Vector Search:
  + Configuração do CosmosDB com Vector Search.
  + Criação de containers vetoriais.
  + Inserção de dados com embeddings.
  + Consulta vetorial com função vector\_distance.
* Integração com Large Language Models (LLM):
  + Configuração do acesso à API OpenAI (ChatGPT 3.5 Turbo).
  + Composição de prompts com contexto recuperado.
  + Prevenção de alucinações e aprimoramento de respostas.
* Desenvolvimento Prático:
  + Ambiente de desenvolvimento: .NET, Jupyter Notebook, DNET Interactive.
  + Pipeline completo: geração de embeddings, armazenamento no CosmosDB, consulta vetorial, composição de prompt, geração com GPT.
  + Visualização e interpretação de embeddings.
* Deploy e Acesso ao Sistema:
  + Utilização de CodeSpaces com Dev Containers.
* Aspectos Éticos e Limitações:
  + Limitações da janela de contexto dos LLMs.
  + Estratégias para contornar o limite de tokens.
  + Segurança e privacidade em dados sensíveis.

### Metodologia:

* A aula será iniciada com uma exposição teórica interativa sobre RAG, reforçada por exemplos práticos.

Será realizada uma demonstração passo a passo utilizando o repositório oficial:

1. **Configuração do CosmosDB:** Criação do banco, habilitação de Vector Search.
2. **Geração de Embeddings:** Com arquivos JSON representando receitas culinárias, transformando-os em embeddings vetoriais.
3. **Armazenamento e Indexação:** Inserção dos documentos com embeddings no CosmosDB.
4. **Consulta Vetorial:** Implementação de query utilizando vector\_distance para calcular similaridade.
5. **Integração com ChatGPT:** Envio do contexto recuperado para o GPT 3.5 Turbo via API, gerando respostas com alta precisão contextual.
6. **Exemplos Práticos:** Perguntas como "Quais sobremesas do Oriente Médio vocês oferecem?" ilustrando o retorno de dados precisos baseados nos embeddings.

* **Atividade Prática:**
  Cada aluno deverá replicar a pipeline demonstrada, personalizando com seu próprio conjunto de dados e desenvolvendo uma API FastAPI ou .NET para exposição do endpoint RAG.
* **Desafio Avançado:**
  Alunos que desejarem poderão substituir o CosmosDB por um banco vetorial open source (ex: ChromaDB ou PostgreSQL com pgvector) e configurar Semantic Kernel para simplificar a integração.
* **Checklist de Entrega:**
  + Pipeline completo de RAG funcional.
  + Embeddings gerados e armazenados.
  + Query vetorial implementada.
  + Integração com LLM concluída.
  + API desenvolvida para acesso externo.
  + Documentação do processo.
* **Reflexão Final:**
  Discussão coletiva sobre oportunidades de aplicação do RAG em sistemas corporativos, impactos éticos e limitações tecnológicas.

## Aulas 17 e 18 - Apresentações Finais dos Projetos

### Objetivo Geral

* Consolidar o aprendizado desenvolvido ao longo da disciplina por meio da apresentação prática dos projetos finais. Estas aulas têm como objetivo avaliar não apenas o funcionamento técnico das soluções criadas, mas também a capacidade dos alunos em argumentar tecnicamente sobre suas decisões de arquitetura, ferramentas utilizadas, soluções adotadas para integração de sistemas, práticas de DevOps, segurança e usabilidade.

### Objetivos Específicos:

* Apresentar os projetos finais desenvolvidos, destacando arquitetura, tecnologias e integrações.
* Demonstrar o funcionamento completo do sistema, incluindo API, persistência em banco de dados, interface de usuário e processos de CI/CD.
* Evidenciar o uso de práticas de boas práticas de programação orientada a objetos e design patterns.
* Mostrar a integração com RAG (opcional) ou outras soluções avançadas implementadas.
* Refletir sobre as dificuldades enfrentadas durante o desenvolvimento e como foram superadas.
* Apresentar documentação técnica clara, abrangendo setup do projeto, instruções de uso e detalhes de deploy.
* Realizar autoavaliação e avaliação entre pares.

### Conteúdo Programático:

* Exposição dos Projetos:
  + Apresentação arquitetural: diagrama dos componentes.
  + Demonstração funcional: API, interface gráfica/web, banco de dados.
  + CI/CD: demonstração do pipeline funcionando com build, testes e push de imagem.
  + Deploy: apresentação da aplicação rodando em ambiente local ou na nuvem.
* Discussão Técnica:
  + Justificativa das escolhas tecnológicas.
  + Estratégias de integração entre componentes.
  + Aplicação de princípios SOLID, DRY, YAGNI.
  + Patterns aplicados na solução.
  + Problemas enfrentados e soluções técnicas adotadas.
* Documentação:
  + Guia de instalação e execução.
  + Configurações necessárias.
  + Descrição dos endpoints.
  + Instruções para deploy local e remoto.
* Aspectos de Qualidade:
  + Testes implementados.
  + Resultados do SonarCloud.
  + Cobertura de testes.
  + Performance e segurança.

### Metodologia:

* Cada grupo ou aluno apresentará o projeto desenvolvido, iniciando por um overview do sistema, seguido por demonstração prática do funcionamento.
* O professor e os colegas poderão realizar perguntas técnicas para aprofundar a compreensão sobre as soluções implementadas.
* Será feita uma análise crítica de cada apresentação, destacando pontos fortes e oportunidades de melhoria.
* Todos os alunos devem entregar previamente a documentação técnica completa do projeto, com scripts de setup, configurações, credenciais de ambiente (se for o caso), e instruções detalhadas de uso.
* Atividade avaliativa formativa: cada aluno realizará uma autoavaliação e também avaliará pelo menos dois projetos de colegas, seguindo critérios definidos pelo professor.
* Os projetos serão avaliados com base nos seguintes critérios:
  + Completude funcional.
  + Qualidade do código.
  + Estrutura e modularização.
  + Integração entre os componentes.
  + Automação via CI/CD.
  + Qualidade da documentação.
  + Clareza na apresentação.
  + Uso de soluções avançadas como RAG, se implementado.

### Checklist de Entrega Final:

* Repositório GitHub atualizado com código e documentação.
* Dockerfiles e docker-compose.yml funcionais.
* Pipeline CI/CD documentado e operacional.
* Deploy funcional (local ou em nuvem).
* Slides da apresentação.
* Relatório reflexivo sobre o desenvolvimento do projeto.

**Modelo de Avaliação em Rubrica para os Projetos Finais**

| **Critério** | **Peso** | **Descrição** | **Nota (0-10)** |
| --- | --- | --- | --- |
| **Completude Funcional** | 20% | O projeto entrega todas as funcionalidades previstas, com operações CRUD completas, integração entre componentes e APIs funcionais. |  |
| **Qualidade do Código** | 15% | O código está limpo, seguindo boas práticas de programação orientada a objetos, aplicando princípios como SOLID, DRY e YAGNI. |  |
| **Estrutura e Modularização** | 10% | O projeto está bem organizado em módulos/cohesionados, separando lógica de negócio, apresentação e persistência de dados. |  |
| **Integração entre Componentes** | 10% | A API, banco de dados, interface e demais serviços estão integrados e funcionando corretamente. |  |
| **Automação via CI/CD** | 10% | Pipelines de integração contínua configurados, executando testes, builds e push de imagem para registro. |  |
| **Qualidade da Documentação** | 10% | O projeto possui documentação clara e completa: instalação, configuração, endpoints, testes e instruções de deploy. |  |
| **Performance e Segurança** | 5% | O projeto apresenta preocupações com performance (ex: caching, queries otimizadas) e segurança básica (ex: validação de entrada, autenticação mínima). |  |
| **Clareza na Apresentação** | 10% | O aluno apresenta o projeto de forma objetiva, clara e demonstra domínio sobre as decisões técnicas tomadas. |  |
| **Soluções Avançadas (RAG, etc.)** | 5% | Implementação de soluções diferenciadas como RAG, caching avançado, deploy em cloud, etc. (opcional para ponto extra). |  |

**Nota Final = Soma ponderada dos critérios acima.**

Além da avaliação do professor, cada aluno realizará uma **autoavaliação** e uma **avaliação por pares**, atribuindo nota e feedback para dois projetos apresentados pelos colegas.

**Modelo de Autoavaliação**

**Nome do Aluno:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ **Título do Projeto:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

1. **O que você considera o ponto mais forte do seu projeto?**
2. **Quais foram os principais desafios enfrentados e como foram superados?**
3. **Quais princípios de boas práticas de código e design patterns você aplicou no seu projeto?**
4. **Como foi sua experiência com CI/CD e automação no projeto?**
5. **O que você faria de diferente se tivesse mais tempo ou recursos?**
6. **Autoavaliação Final (0 a 10):** \_\_\_\_\_\_\_
7. **Justifique a nota atribuída:**

**Modelo de Avaliação por Pares**

**Nome do Avaliador:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ **Nome do Avaliado:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ **Título do Projeto Avaliado:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

1. **Completude Funcional:** Nota (0-10): \_\_\_\_\_\_
2. **Qualidade do Código:** Nota (0-10): \_\_\_\_\_\_
3. **Integração entre Componentes:** Nota (0-10): \_\_\_\_\_\_
4. **Interface e Usabilidade:** Nota (0-10): \_\_\_\_\_\_
5. **Documentação:** Nota (0-10): \_\_\_\_\_\_
6. **Apresentação:** Nota (0-10): \_\_\_\_\_\_

**Feedback geral sobre o projeto:**

**Sugestões de melhoria:**

Observação: O feedback será utilizado para aprimoramento e não terá caráter punitivo.

# Justificativa (Importância da disciplina na formação do egresso)

A disciplina de **Programação Orientada a Objetos II (POOII)** constitui um componente curricular essencial para o Curso de Engenharia de Software da UNIVILLE, alinhando-se diretamente à Missão Institucional de formar profissionais éticos, críticos, inovadores e comprometidos com o desenvolvimento regional sustentável. Inserida no contexto do Projeto Pedagógico do Curso (PPC) e do Projeto Pedagógico Institucional (PPI), esta disciplina contribui significativamente para o desenvolvimento de competências técnicas e profissionais que caracterizam o perfil do engenheiro de software formado pela UNIVILLE.

Complementando os conhecimentos adquiridos em Programação Orientada a Objetos I, a disciplina POOII aprofunda o domínio sobre o paradigma de orientação a objetos e suas aplicações práticas na engenharia de software moderna. Enquanto POOI introduz os conceitos essenciais para compreender princípios como encapsulamento, herança, polimorfismo e abstração, bem como as boas práticas de modelagem de sistemas modulares e reutilizáveis, a disciplina POOII avança para o desenvolvimento de soluções complexas, com foco em design patterns, integração com bancos de dados, construção de APIs, desenvolvimento de interfaces de usuário e integração de sistemas.

O conteúdo de POOII prepara o aluno para a realidade do mercado de trabalho, onde o domínio de tecnologias como Docker, GitHub Actions, CI/CD, FastAPI, PostgreSQL, DuckDB e frameworks de interface como Streamlit, Tkinter e PySide6 é fundamental. A disciplina também diferencia o egresso ao introduzir tópicos emergentes como o Retrieval-Augmented Generation (RAG) e a integração com Large Language Models (LLMs), tecnologias essenciais na construção de sistemas inteligentes que utilizam inteligência artificial aplicada.

Essa formação está alinhada ao perfil profissiográfico do egresso de Engenharia de Software, que requer profissionais aptos a especificar, projetar, implementar e gerenciar sistemas complexos e inovadores. A disciplina potencializa o desenvolvimento de habilidades analíticas, de resolução de problemas, pensamento crítico e capacidade de inovação tecnológica, promovendo também uma reflexão ética sobre o impacto social das soluções de software.

Além do aspecto técnico, a disciplina reafirma o compromisso da UNIVILLE com a formação cidadã, ética e crítica, alinhando-se ao PPI e ao PPC. O egresso torna-se um profissional capaz de propor soluções tecnológicas sustentáveis, comprometido com o desenvolvimento social e econômico da região, em consonância com a missão da instituição.

Por meio de metodologias ativas e projetos práticos, POOII consolida a aprendizagem significativa e prepara o aluno para atuar de forma protagonista em equipes multidisciplinares, conduzindo projetos de desenvolvimento de software de forma eficiente, ética e inovadora. Assim, a disciplina contribui de forma decisiva para a formação integral do engenheiro de software, pronto para enfrentar os desafios da transformação digital e da indústria 4.0, fortalecendo sua inserção no mercado de trabalho e sua atuação como agente de transformação social e tecnológica.

# Objetivos

## Objetivo Geral (prever a contribuição da disciplina em termos do conhecimento, habilidade e atitudes para formação do egresso)

* Desenvolver no aluno a capacidade de projetar, implementar e integrar soluções de software complexas utilizando metodologias, técnicas e ferramentas avançadas de Programação Orientada a Objetos (POO), capacitando-o a construir sistemas robustos, escaláveis, seguros e inovadores que incorporem boas práticas de engenharia de software, padrões de projeto, integração com bancos de dados, APIs modernas, interfaces gráficas, pipelines de automação (CI/CD) e tecnologias emergentes como inteligência artificial e Retrieval-Augmented Generation (RAG). Ao final da disciplina, o estudante será capaz de atuar com excelência técnica, senso crítico e responsabilidade ética na concepção e desenvolvimento de soluções computacionais alinhadas às demandas do mercado e aos desafios da transformação digital.

## Objetivos Específicos

1. Revisar os princípios fundamentais da Programação Orientada a Objetos (POO) e aplicar padrões de projeto para construção de sistemas modulares, reutilizáveis e de fácil manutenção.
2. Desenvolver APIs RESTful modernas e seguras utilizando frameworks atualizados como FastAPI e boas práticas de engenharia de software.
3. Implementar integração com bancos de dados relacionais e analíticos, como PostgreSQL e DuckDB, empregando técnicas eficientes de persistência e manipulação de dados.
4. Construir interfaces de usuário gráficas (GUI) e web interativas utilizando Tkinter, PySide6 e Streamlit para consumo e visualização de dados de APIs.
5. Aplicar práticas de automação de desenvolvimento com CI/CD utilizando GitHub Actions para integração contínua, execução de testes, análise de qualidade de código e deploy automatizado.
6. Utilizar técnicas de containerização com Docker e orquestração com Docker Compose para ambientes de desenvolvimento e produção replicáveis e seguros.
7. Explorar o conceito de Retrieval-Augmented Generation (RAG), desenvolvendo pipelines que integram bancos de dados vetoriais com Large Language Models (LLMs) para recuperação inteligente de informações.
8. Realizar testes unitários, de integração e de performance para garantir a robustez e a qualidade das soluções desenvolvidas.
9. Aplicar boas práticas de documentação técnica utilizando ferramentas como pdoc, garantindo a clareza e a manutenção futura dos projetos.
10. Estimular a reflexão ética e crítica sobre o uso de tecnologias emergentes e seu impacto na sociedade e no mercado de trabalho.
11. Elaborar um projeto prático integrador que evidencie a aplicação dos conhecimentos adquiridos na disciplina, culminando na apresentação de uma solução completa, funcional e documentada.

# Descrever proposta(s) de integração curricular

A disciplina de Programação Orientada a Objetos II propicia amplas possibilidades de integração curricular com outras disciplinas do Curso de Engenharia de Software, promovendo a interdisciplinaridade e ampliando a formação prática e teórica dos estudantes. A seguir, destacam-se propostas de integração:

1. Integração com Engenharia de Software e Testes de Software:
   * A disciplina pode ser articulada com Engenharia de Software e Testes de Software, permitindo que os alunos desenvolvam projetos orientados a objetos aplicando práticas de testes unitários, integração, cobertura de código e Test-Driven Development (TDD). Isso fortalece a construção de sistemas com alta qualidade, validando práticas como integração contínua (CI/CD) abordadas em ambas disciplinas.
2. Integração com Desenvolvimento Web e Mobile:
   * A construção de APIs RESTful e interfaces gráficas ou web propostas em POOII podem ser integradas às disciplinas de Desenvolvimento Web e Mobile. Os alunos podem utilizar as APIs desenvolvidas para alimentar aplicações frontend desenvolvidas com frameworks modernos, promovendo a compreensão completa do ciclo de desenvolvimento de sistemas distribuídos.
3. Integração com Inteligência Artificial Aplicada:
   * Com a introdução do conceito de Retrieval-Augmented Generation (RAG) e integração com Large Language Models, POOII complementa o aprendizado em disciplinas de Inteligência Artificial Aplicada. Os alunos podem colaborar na construção de soluções inteligentes que combinem machine learning, processamento de linguagem natural e recuperação de informações.
4. Integração com Banco de Dados e Ciência de Dados:
   * As práticas com PostgreSQL, DuckDB e manipulação de dados com Polars permitem a integração com disciplinas de Banco de Dados e Ciência de Dados. Projetos interdisciplinares podem explorar desde a persistência eficiente de dados até a extração de insights analíticos para alimentar APIs ou sistemas inteligentes.
5. Integração com Projeto Integrador e TCC:
   * As competências adquiridas em POOII servem como base para os Projetos Integradores e Trabalhos de Conclusão de Curso (TCC), oferecendo aos alunos ferramentas e metodologias para propor soluções completas, desde o backend robusto até a entrega de aplicações com interfaces otimizadas e automação de deploy.

Essa abordagem de integração curricular fortalece a formação ampla e prática dos alunos, estimulando o desenvolvimento de projetos multidisciplinares alinhados às demandas reais do mercado e consolidando o papel da Engenharia de Software na transformação digital.

# Procedimentos Didáticos

Aulas teóricas expositivas dialogadas ministradas por professores do Departamento de Informática em salas de aula utilizando-se de quadro e sistemas multimídia (datashow). Aulas práticas em laboratório também fazem parte das atividades.

# Bibliografia Básica

* ARAUJO, Everton Coimbra. Orientação a objetos com Java. São Paulo: Visual Books, 2008.
* FURGERI, Sérgio. Java 7: ensino didático. São Paulo: Érica, 2010.
* PUGA, Sandra; RISSETTI, Gerson. Lógica de programação e estrutura de dados, com aplicações em Java. 2. ed. São Paulo: Pearson Prentice Hall, 2008.

# Bibliografia Complementar

* BARNES, David. Programação orientada a objetos com Java. 4. Ed. São Paulo: Prentice Hall, 2009.
* BORATTI, Isaias Camilo. Programação orientada a objetos em JAVA. São Paulo: Visual Books, 2007
* DEITEL, H. M; DEITEL, P. J. Java, como programar. 8. ed. São Paulo: Prentice Hall, 2010.
* MOTA, Alisson Abreu. Programação orientada a objetos com C++. Florianópolis: Relativa, 2001.
