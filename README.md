# Programação Orientada a Objetos II (POOII) - Python

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📚 Sobre

Este repositório contém os materiais, exemplos e recursos utilizados no avançado de **Programação Orientada a Objetos**. O curso foca em práticas avançadas de desenvolvimento de software com orientação a objetos utilizando Python, incluindo integração com bancos de dados, APIs, CI/CD, testes, containerização, interfaces gráficas e RAG.

### 🎯Objetivo Geral

Capacitar o aluno a desenvolver software modular, testável, documentado e pronto para deploy, utilizando práticas modernas de desenvolvimento orientado a objetos com Python, integração com banco de dados, APIs, CI/CD, containers e visualização de dados.

#### Objetivos Específicos

* Revisar princípios fundamentais de POO e boas práticas (Clean Code, SOLID, DRY, YAGNI)
* Implementar e aplicar Design Patterns clássicos em projetos reais
* Integrar sistemas via APIs RESTful.
* Integrar sistemas orientados a objetos com bancos de dados relacionais e analíticos.
* Criar interfaces gráficas desktop ou web.
* Aplicar práticas de DevOps: testes automatizados, integração contínua, containerização e deploy.
* Manipular e visualizar dados utilizando Polars.
* Explorar tópicos avançados como Retrieval-Augmented Generation (RAG) como diferencial.


## 🗓️ Estrutura do Curso

O curso está organizado conforme o cronograma de 36 aulas:

| **Aula** | **Tema** | **Entregas / Observações** | **Status** |
| --- | --- | --- | --- |
| 1-2 |  Boas Práticas e Design Patterns Clássicos | * SOLID, DRY, YAGNI, KISS, Coesão x Acoplamento * Patterns clássicos (Strategy, Factory, Singleton, etc.) |🔄 Em desenvolvimento |
| 3-4 | Ambiente profissional de projetos Python | * Projeto inicial no GitHub (empty template) * uv ou poetry para ambientes isolados * Configuração de projeto com pyproject.toml * Documentação com pdoc * Testes com pytest, cobertura com pytest-cov e benchmark com pytest-benchmark |🔄 Em desenvolvimento |
| 5-6 | Git e CI/CD com GitHub Actions | * Git e commits semânticos (conventional commits) * Introdução   Workflow com:   * Linting (pre-commit) * pre-commit com mypy e ruff * Testes (pytest) * Coverage + Build do pacote |🔄 Em desenvolvimento |
| 7-8 | Refatoração de Códigos | * Code smells e refatoração incremental * Refatoração de Software (tipos e atores) * Sonarcloud (CI) * Refatoração baseada em TDD |🔄 Em desenvolvimento |
| 9-14 | Construção e Consumo de APIs REST | * Definição * Criação de APIs com FastAPI (simples) * Criação de rotas, validação com pydantic * Retorno estruturado, tratamento de erros * Consumo com httpx, asyncio, backoff, e testes com responses * Consumo de APIs externas com caching local * Uso do Postman * Geração de OpenAPI |🔄 Em desenvolvimento |
| 15-20 | Integração com Banco de Dados | * PostgreSQL e DuckDB * ORM básico com dataclasses + SQL * Pyarrow * Uso de testcontainers |🔄 Em desenvolvimento |
| 21-22 | Manipulação de Dados com Polars | * Leitura, transformação, agregações * Integração entre objetos e DataFrames * Dashboards com plotly * ETL básico |🔄 Em desenvolvimento |
| 23-27 | Interface de Usuário (GUI/Web) | * Construção de GUI com Tkinter ou PySide6 * Alternativa: mini dashboard com Streamlit * Conectar GUI com API Rest e DuckDB |🔄 Em desenvolvimento |
| 28-32 | Containerização, Orquestração e CI/CD completo com build e push de imagem | * Docker e uvicorn para deploy local * Docker Compose com persistência e testes * Volume persistente + testes em Docker * GitHub Actions com Docker (deploy) * Deploy em Netlify e Render |🔄 Em desenvolvimento |
| 33-34 | Tópicos Avançados: RAG (Retrieval-Augmented Generation) | * Exemplos com OpenAI/LLM simulados ou locais (ollama) * Fundamentos de RAG (Retrieval-Augmented Generation) |🔄 Em desenvolvimento |
| 35-36 | Apresentações finais | Slides, live demo, justificativas | - |

## 💻 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**
- **PostgreSQL 15+**
- **DuckDB**
- **Polars**
- **Tkinter, PySide6, Streamlit**
- **Docker, Docker Compose**
- **GitHub Actions**
- **pytest, pytest-cov**
- **pdoc**
- **SonarCloud**

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- Poetry ou uv
- Docker

### Executando Testes

```bash
# Instalar dependências
poetry install

# Executar testes
pytest --cov=./

# Visualizar cobertura
pytest --cov-report html
```

## 📖 Conteúdos em Destaque

* **Princípios SOLID, DRY, YAGNI**
* **Refatoração com SonarCloud**
* **APIs REST com FastAPI**
* **Integração com PostgreSQL e DuckDB**
* **ETL e manipulação de dados com Polars**
* **Interfaces gráficas GUI e web**
* **Pipeline CI/CD completo com GitHub Actions**
* **Containerização com Docker**
* **Deploys em Netlify, Render**
* **Retrieval-Augmented Generation (RAG) com LLMs**
* **Testes unitários, integração e performance**

## 🔮 Trabalhos Futuros

* [ ] Finalizar todos os exemplos práticos por aula
* [ ] Documentar todas as aulas via pdoc
* [ ] Implementar projetos integradores completos

## 🤝 Reúso do Material

O conteúdo deste repositório pode ser reutilizado com devida referência ao repositório. Pull Requests com melhorias e novos exemplos são bem-vindos!

Para dúvidas, comentários ou sugestões, abra uma **issue**.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
