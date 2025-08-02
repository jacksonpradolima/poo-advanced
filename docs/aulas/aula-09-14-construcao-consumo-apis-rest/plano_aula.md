---
aula: "9-14"
titulo: "Construção e Consumo de APIs REST"
objetivo: "Capacitar os alunos a projetar, construir e consumir APIs RESTful utilizando o framework FastAPI em Python. A ênfase será no desenvolvimento de APIs robustas, seguras, documentadas automaticamente e com práticas modernas de desenvolvimento orientado a objetos e validação de dados."
conceitos: ["APIs REST", "FastAPI", "Pydantic", "httpx", "OpenAPI", "Tratamento de Erros", "Caching", "Postman"]
prerequisitos: ["Fundamentos de POO", "Python intermediário", "HTTP básico", "JSON"]
dificuldade: "intermediário"
owner: "Jackson Antonio do Prado Lima"
date_created: "2025-08-02"
tempo_estimado: "12h (720min)"
forma_entrega: "projeto prático integrado"
competencias: ["Criação de APIs RESTful", "Validação de dados com Pydantic", "Consumo de APIs externas", "Documentação automática", "Tratamento de erros"]
metodologia: "Aulas práticas com desenvolvimento contínuo, demonstrações ao vivo, exercícios graduados por complexidade"
llm_style: "detailed"
language: "pt-BR"
tone: "profissional e didático"
---

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
