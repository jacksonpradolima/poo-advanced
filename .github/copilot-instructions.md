---
mode: 'agent'
description: 'Gerar planos de aula estruturados, objetivos, metodologias e conteúdos por sessão com base no plano de ensino da disciplina'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'githubRepo', 'openSimpleBrowser', 'problems', 'runTasks', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI]
---
# Geração de Plano de Aula para a Disciplina

## Diretriz Primária

Gerar um plano de aula abrangente, detalhado e pedagogicamente estruturado alinhado ao plano de ensino oficial da disciplina. O plano deve permitir que instrutores ou agentes educacionais gerem, adaptem e executem conteúdos instrucionais, exemplos de código, avaliações e atividades, conforme o plano oficial aprovado para a disciplina.

O plano de ensino da disciplina encontra-se em `plano_ensino.md` no diretório principal.

Sempre leia o histórico e arquivos presentes no repositório para garantir consistência antes de sugerir novos conteúdos ou códigos.

## Contexto de Execução

Este guia direciona comunicações AI-to-AI e o planejamento instrucional AI-humano, garantindo geração automatizada e repetível de aulas respeitando a estrutura pedagógica, profundidade e sequência do curso.

## Requisitos Centrais

- Todos os planos de aula devem estar rigorosamente alinhados ao **plano oficial da disciplina** (`plano_ensino.md`).
- Linguagem: **Python** (v3.12+), não utilizar Java ou C++.
- Incluir objetivos estruturados e progressivos: **Objetivo Geral** e **Objetivos Específicos** por aula. Ambos disponíveis no plano de ensino.
- O conteúdo deve detalhar tópicos, exemplos de código, exercícios e referências às ferramentas, bibliotecas e frameworks especificados no plano. O conteúdo programático está disponível no plano de ensino.
- A metodologia deve definir explicitamente as etapas da aula, alocação de tempo, ferramentas e frameworks. A metodologia está disponível no plano de ensino.
- Todos os entregáveis (exercícios, projetos, avaliações) devem estar alinhados com a abordagem baseada em projetos definida no plano.

## Estrutura Obrigatória do Plano de Aula

Cada plano de aula deve conter:

- **Objetivo Geral da Aula**
- **Objetivos Específicos**
- **Conteúdos a Serem Abordados**
- **Metodologia**: com etapas detalhadas, alocação de tempo, ferramentas e frameworks.
- **Métodos de Avaliação**: formativa (ao longo da aula) e somativa (checkpoints).
- **Referências e Materiais de Apoio**: incluindo URLs, documentação oficial e referências acadêmicas.
- **Exemplo de Código em Python**, sempre que aplicável.
- **Entregáveis Esperados dos Estudantes**.

## Objetivos Educacionais Gerais

### Público-Alvo
- **Primário**: Estudantes de graduação em Ciência da Computação, Sistemas de Informação e áreas afins
- **Secundário**: Desenvolvedores iniciantes/intermediários buscando aprimoramento em POO
- **Terciário**: Profissionais em transição de paradigmas procedimentais para orientados a objetos

### Nível de Complexidade
- **Progressivo**: Começar com conceitos fundamentais e evoluir gradualmente
- **Didático**: Priorizar clareza sobre sofisticação técnica
- **Prático**: Cada conceito deve ter aplicação concreta e demonstrável

## Padrões de Implementação Otimizados para IA

- Usar linguagem determinística e não ambígua.
- Formatar o conteúdo em seções estruturadas em Markdown.
- Citar versões exatas das ferramentas (ex: FastAPI 0.110+).
- Incluir boas práticas de codificação Python, com aderência ao **PEP8**.
- Referenciar testes unitários com **pytest**, cobertura com **pytest-cov**, e CI/CD com **GitHub Actions**.

## Especificações de Arquivo de Saída

- Salvar planos de aula gerados em `/docs/aulas/`.
- Convenção de nomeação: `aula-[numero_da_aula]-[topico].md`
- Exemplo: `aula-03-ci-cd-github-actions.md`
- Todos os arquivos devem conter **YAML front matter**.
- Organização de Diretórios
```
docs/aulas/aula-XX-nome_da_aula/
├── README.md                  # Conteúdo principal da aula
├── plano_aula.md              # Plano de Aula relacionado
├── exemplos/                  # Códigos demonstrativos
│   ├── basico/                # Exemplos introdutórios
│   ├── intermediario/         # Exemplos com complexidade média
│   └── avancado/              # Exemplos desafiadores
├── exercicios/                # Atividades práticas
│   ├── README.md              # Instruções dos exercícios
│   ├── nivel1/                # Exercícios básicos
│   ├── nivel2/                # Exercícios intermediários
│   └── nivel3/                # Exercícios avançados
├── recursos/                  # Material de apoio
│   ├── diagramas/             # UML, fluxogramas, etc.
│   ├── referencias/           # Links e bibliografia
│   └── slides/                # Apresentações (se aplicável)
└── solucoes/                  # Gabaritos (pasta privada/opcional)
```

## Template de Plano de Aula

````md
---
aula: XX
titulo: "Nome da Aula"
objetivo: '[Objetivo principal da aula]'
conceitos: ['conceito1', 'conceito2', 'conceito3']
prerequisitos: '['aula-YY', 'conceito-previo']
dificuldade: 'básico|intermediário|avançado'
owner: 'Jackson Antonio do Prado Lima'
date_created: '[AAAA-MM-DD]'

---

# Objetivo Geral
[Descrever claramente o objetivo pedagógico geral da aula.]

## Objetivos Específicos
1. [Objetivo específico 1]
2. [Objetivo específico 2]
3. [Objetivo específico 3]

## Conteúdo Programático
- Tópico 1
- Tópico 2
- Tópico 3

## Metodologia
- **Duração da Exposição:** [minutos]
- **Atividade Prática:** [tarefas de programação, projetos, integrações]
- **Tecnologias e Ferramentas:** [listar versões específicas, ex: FastAPI 0.110+, PostgreSQL 15+, Polars]
- **Avaliação:** [descrição das avaliações: quizzes, desafios de codificação, marcos do projeto]

## Exemplo de Código
```python
# Exemplo em Python relacionado ao tópico da aula
```

## Conexões com Outras Aulas
[Como esta aula se relaciona com o curso]

## Material Complementar
[Recursos adicionais para aprofundamento]

## Perguntas Frequentes
[Dúvidas comuns antecipadas]
````

## Metadados e Organização

### 1. Frontmatter Padrão
```yaml
---
aula: XX
titulo: "Nome da Aula"
objetivo: '[Objetivo principal da aula]'
conceitos: ["conceito1", "conceito2", "conceito3"]
prerequisitos: ["aula-YY", "conceito-previo"]
dificuldade: "básico|intermediário|avançado"
owner: 'Jackson Antonio do Prado Lima'
date_created: '[AAAA-MM-DD]'
---
```

### 2. Tags Semânticas
- `#fundamental`: Conceitos essenciais da POO
- `#aplicado`: Implementações práticas
- `#teoria`: Discussões conceituais profundas
- `#exercicio`: Atividades práticas
- `#exemplo`: Código demonstrativo
- `#antipadrao`: Exemplos de práticas ruins
- `#boapratica`: Demonstrações de código de qualidade


## Estilo de Escrita

### 1. Tom e Linguagem
- **Didático**: Explicativo, mas não condescendente
- **Acessível**: Evitar jargões desnecessários
- **Motivacional**: Destacar aplicações práticas e benefícios
- **Inclusivo**: Usar exemplos diversos e linguagem neutra

### 2. Progressão Pedagógica
- **Scaffolding**: Construir sobre conhecimento anterior
- **Exemplos Concretos**: Preferir casos do mundo real
- **Analogias**: Usar metáforas quando apropriado
- **Repetição Espaçada**: Reforçar conceitos importantes

### 3. Tratamento de Erros
- **Antecipar Dificuldades**: Identificar pontos de confusão comum
- **Debugging Pedagógico**: Mostrar como identificar e corrigir erros
- **Mindset de Crescimento**: Tratar erros como oportunidades de aprendizado

## Padrões de Exercícios

### 1. Classificação por Dificuldade

#### Nível 1 - Básico (🔵)
- **Objetivo**: Aplicação direta de conceitos
- **Complexidade**: Uma única funcionalidade
- **Tempo Estimado**: 15-30 minutos
- **Exemplo**: Implementar uma classe simples com getters/setters

#### Nível 2 - Intermediário (🟡)
- **Objetivo**: Integração de múltiplos conceitos
- **Complexidade**: Sistema pequeno com 2-4 classes
- **Tempo Estimado**: 45-90 minutos
- **Exemplo**: Sistema de biblioteca com livros e usuários

#### Nível 3 - Avançado (🔴)
- **Objetivo**: Design complexo e tomada de decisões arquiteturais
- **Complexidade**: Sistema completo com múltiplas responsabilidades
- **Tempo Estimado**: 2-4 horas
- **Exemplo**: Sistema bancário com diferentes tipos de conta

### 2. Elementos Obrigatórios em Exercícios
- **Contexto**: Cenário realista e motivador
- **Requisitos**: Lista clara e não ambígua
- **Restrições**: Limitações técnicas ou conceituais
- **Critérios de Avaliação**: Como será medido o sucesso
- **Dicas**: Orientações para superar dificuldades comuns
- **Extensões**: Sugestões para ir além do básico

### 3. Template de Exercício
```markdown
## 🏋️ Exercício [N]: [Nome do Exercício] [🔵/🟡/🔴]

### 📋 Contexto
[Descrição do cenário/problema]

### 🎯 Objetivos
- [ ] [Objetivo específico 1]
- [ ] [Objetivo específico 2]
- [ ] [Objetivo específico 3]

### 📋 Requisitos Funcionais
1. [Requisito claro e testável]
2. [Requisito claro e testável]

### ⚙️ Requisitos Técnicos
- [Restrição ou orientação técnica]
- [Conceito específico que deve ser usado]

### 💡 Dicas
- [Orientação para começar]
- [Como superar dificuldade comum]

### 🔍 Critérios de Avaliação
- [ ] [Critério objetivo]
- [ ] [Critério objetivo]

### 🚀 Desafios Extras (Opcional)
- [Extensão avançada]
- [Variação interessante]

### ⏱️ Tempo Estimado: [X] minutos
```

## Diagramas e Visualizações

### 1. Padrões UML
- **Classes**: Sempre mostrar atributos, métodos e visibilidade
- **Relacionamentos**: Usar cardinalidade e rótulos descritivos
- **Sequência**: Para fluxos complexos de interação
- **Estados**: Para objetos com ciclo de vida importante

### 2. Ferramentas Recomendadas
- **PlantUML**: Para diagramas em código
- **Draw.io**: Para diagramas visuais complexos
- **Mermaid**: Para diagramas simples em Markdown

### 3. Convenções Visuais
- **Cores**: Usar esquema consistente (classes = azul, interfaces = verde, etc.)
- **Destaque**: Marcar elementos sendo ensinados na aula atual
- **Simplificação**: Omitir detalhes irrelevantes para o conceito sendo ensinado

## Interconexão Entre Aulas

### 1. Sistema de Referências
- **Backwards**: Sempre mencionar pré-requisitos
- **Forwards**: Antecipar onde conceitos serão expandidos
- **Cross-references**: Conectar com aulas relacionadas

### 2. Continuidade de Exemplos
- **Evolução**: Usar o mesmo domínio em múltiplas aulas
- **Refinamento**: Melhorar implementações anteriores
- **Comparação**: Mostrar "antes e depois" das melhorias

### 3. Mapa Conceitual
- Manter um diagrama geral mostrando dependências entre conceitos
- Atualizar após cada nova aula
- Usar para validar sequência pedagógica

## Métodos de Avaliação

- Quiz sobre [tópico]
- Exercício prático de codificação sobre [tópico]
- Discussão em grupo ou revisão de código

## Convenções de Codificação

### Instruções para Python

* Escreva comentários claros e concisos para cada função.
* Certifique-se de que as funções tenham nomes descritivos e incluam type hints (dicas de tipo).
* Forneça docstrings seguindo as convenções do PEP 257.
* Utilize o módulo `typing` para anotações de tipo (ex.: `List[str]`, `Dict[str, int]`).
* Divida funções complexas em funções menores e mais gerenciáveis.

### Instruções Gerais

* Sempre priorize a legibilidade e a clareza.
* Para códigos relacionados a algoritmos, inclua explicações sobre a abordagem utilizada.
* Escreva códigos que sigam boas práticas de manutenibilidade, incluindo comentários explicando decisões de design.
* Trate casos de borda (edge cases) e implemente tratamento de exceções de forma clara.
* Para bibliotecas ou dependências externas, mencione seu uso e propósito em comentários.
* Use convenções de nomenclatura consistentes e siga as melhores práticas específicas da linguagem.
* Escreva código conciso, eficiente, idiomático e que também seja fácil de entender.

### Estilo e Formatação de Código

* Siga o guia de estilo **PEP 8** para Python.
* Mantenha a indentação correta (use 4 espaços por nível de indentação).
* Garanta que as linhas não ultrapassem 79 caracteres.
* Coloque docstrings de funções e classes imediatamente após o `def` ou `class`.
* Use linhas em branco para separar funções, classes e blocos de código quando apropriado.

### Casos de Borda e Testes

* Sempre inclua casos de teste para os caminhos críticos da aplicação.
* Considere casos de borda comuns, como entradas vazias, tipos de dados inválidos e conjuntos de dados grandes.
* Inclua comentários sobre os casos de borda e o comportamento esperado nestes casos.
* Escreva testes unitários para as funções e documente-os com docstrings explicando os casos de teste.

### Exemplo de Documentação Adequada

```python
def calculate_area(radius: float) -> float:
    """
    Calcula a área de um círculo dado o raio.

    Parameters:
    radius (float): O raio do círculo.

    Returns:
    float: A área do círculo, calculada como π * raio².
    """
    import math
    return math.pi * radius ** 2
```

### Comentários Pedagógicos
- **Propósito**: Cada bloco de código deve explicar "por quê", não apenas "o quê"
- **Progressão**: Comentários devem guiar o raciocínio step-by-step
- **Alternativas**: Mencionar diferentes abordagens quando relevante
- **Armadilhas**: Alertar sobre erros comuns

#### Exemplo de Comentário Pedagógico:
```python
from typing import Optional


# CONCEITO: Encapsulamento
#
# O atributo '_saldo' está protegido por convenção (prefixo underline),
# reforçando o princípio do encapsulamento: o estado interno do objeto
# não deve ser manipulado diretamente, apenas por métodos públicos.
#
# BENEFÍCIO: Impede alterações indevidas, mantendo a integridade do objeto.
#
# ERRO COMUM: Tornar o atributo público, permitindo mudanças diretas
# que podem deixar o objeto em estado inconsistente.

class ContaBancaria:
    """
    Representa uma conta bancária simples com operações de depósito,
    saque e consulta de saldo. Demonstra o conceito de encapsulamento.
    """

    def __init__(self, saldo_inicial: float = 0.0) -> None:
        """
        Inicializa a conta com um saldo inicial opcional.

        Parameters
        ----------
        saldo_inicial : float
            Valor inicial do saldo da conta. Deve ser >= 0.
        """
        if saldo_inicial < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")
        self._saldo: float = saldo_inicial

    def depositar(self, valor: float) -> None:
        """
        Deposita um valor positivo na conta.

        Parameters
        ----------
        valor : float
            Valor a ser depositado. Deve ser maior que zero.

        Raises
        ------
        ValueError
            Se o valor for menor ou igual a zero.
        """
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._saldo += valor

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque se houver saldo suficiente.

        Parameters
        ----------
        valor : float
            Valor a ser sacado. Deve ser positivo e menor ou igual ao saldo.

        Returns
        -------
        bool
            True se o saque foi realizado com sucesso, False caso contrário.
        """
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")

        if valor > self._saldo:
            return False

        self._saldo -= valor
        return True

    def consultar_saldo(self) -> float:
        """
        Retorna o saldo atual da conta.

        Returns
        -------
        float
            Saldo atual da conta.
        """
        return self._saldo


def criar_conta_com_valor_inicial(valor: Optional[float] = 0.0) -> ContaBancaria:
    """
    Função auxiliar para criar uma conta bancária já com validação.

    Parameters
    ----------
    valor : Optional[float]
        Valor inicial para o saldo da conta. Padrão é 0.0.

    Returns
    -------
    ContaBancaria
        Uma nova instância de ContaBancaria.
    """
    return ContaBancaria(saldo_inicial=valor)

```


## Referências e Materiais de Apoio

- [Documentação oficial do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação do pdoc](https://pdoc.dev/docs/pdoc.html)

## Processo de Criação de Conteúdo

### 1. Workflow Padrão
1. **Planejamento**: Definir objetivos e escopo
2. **Pesquisa**: Revisar materiais existentes e referências
3. **Estruturação**: Organizar conteúdo segundo template
4. **Desenvolvimento**: Criar textos, códigos e exercícios
5. **Revisão**: Validar qualidade e consistência
6. **Teste**: Executar códigos e verificar exercícios
7. **Publicação**: Disponibilizar para estudantes

### 2. Checklist de Qualidade
- [ ] Objetivos de aprendizagem claramente definidos
- [ ] Conceitos explicados com clareza e progressão lógica
- [ ] Exemplos práticos funcionais e bem comentados
- [ ] Exercícios variados em dificuldade e abordagem
- [ ] Conexões com outras aulas estabelecidas
- [ ] Material complementar de qualidade
- [ ] Linguagem inclusiva e acessível
- [ ] Formatação consistente com padrões do projeto
- [ ] Metadados completos e atualizados

### 3. Versionamento de Conteúdo
- **Major (X.0.0)**: Reestruturação significativa do conteúdo
- **Minor (X.Y.0)**: Adição de novos exemplos ou exercícios
- **Patch (X.Y.Z)**: Correções de bugs ou melhorias menores


## Boas Práticas Específicas

### 1. Para Conceitos Abstratos
- **Analogias Concretas**: Usar metáforas do mundo real
- **Visualizações**: Diagramas e representações gráficas
- **Progressão Gradual**: Do simples ao complexo
- **Múltiplas Perspectivas**: Diferentes formas de explicar

### 2. Para Código Complexo
- **Decomposição**: Quebrar em partes menores
- **Narrativa**: Contar a "história" do código
- **Alternativas**: Mostrar diferentes implementações
- **Refatoração**: Demonstrar evolução e melhoria

### 3. Para Exercícios Desafiadores
- **Scaffolding**: Fornecer estrutura inicial
- **Marcos Intermediários**: Objetivos parciais
- **Dicas Graduais**: Ajuda progressiva
- **Celebração**: Reconhecer conquistas

---

# Instruções Diretas para o GitHub Copilot e Modelos de Linguagem

- Sempre **verifique os arquivos existentes no repositório antes de sugerir novos conteúdos ou exemplos.**
- **Adote o formato e a estrutura pedagógica descritos neste documento** como padrão absoluto.
- **Nunca crie exemplos puramente teóricos sem aplicação prática.**
- Sempre que criar exemplos ou exercícios:
  - Forneça **comentários explicativos detalhados** em português.
  - Aplique boas práticas de design orientado a objetos.
  - Inclua testes unitários sempre que possível.
- Utilize sempre a linguagem Python, salvo instrução explícita contrária.
- Caso um conteúdo já esteja disponível, foque em **expandir ou complementar**, nunca duplicar.
- Para cada aula ou exemplo criado:
  - Inicie por descrever os **Objetivos de Aprendizagem**.
  - Relacione com conteúdos prévios e indique próximos passos.
  - Utilize a estrutura de diretórios e templates definidos.

> **Importante:** Sempre priorize clareza didática, exemplos incrementais e linguagem acessível ao público-alvo de graduação.

---
