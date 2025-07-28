# 🏦 Sistema Bancário - Arquitetura Hexagonal

Este projeto demonstra um sistema bancário completo implementado com **Arquitetura Hexagonal** (Ports & Adapters), **Domain-Driven Design** e todos os **princípios SOLID**.

## 🎯 Objetivos Educacionais

Este sistema foi desenvolvido para demonstrar:

- **Arquitetura Hexagonal** (Ports & Adapters)
- **Domain-Driven Design** (DDD)
- **Princípios SOLID** em aplicação prática
- **Design Patterns** essenciais
- **Clean Architecture** com separação clara de responsabilidades
- **Testabilidade** e **extensibilidade**

## 🏗️ Arquitetura

### Camadas da Aplicação

```
📦 Domain (Core Business)
├── 🧩 Entities: Cliente, Conta, Transacao
├── 💎 Value Objects: CPF, Dinheiro, Endereco
├── 📋 Use Cases: CriarCliente, AbrirConta, RealizarTransferencia
├── 🔌 Ports: RepositorioCliente, ValidadorFraude, etc.
└── 📢 Domain Events: EventoContaCriada, EventoTransacaoRealizada

📦 Infrastructure (External World)
├── 🗄️ Adapters de Persistência: RepositorioMemoria, RepositorioSQLite
├── 🌐 Adapters de Serviços: ConsultorCreditoSerasa, ValidadorFraude
├── 📧 Adapters de Notificação: NotificadorEmail, NotificadorSMS
├── 📊 Adapters de Métricas: ColetorMetricas, Auditoria
└── ⚡ Adapters de Eventos: ProcessadorEventosAssincrono
```

### Fluxo de Dados

```
🖥️ Interface/API → 📋 Use Cases → 🏛️ Domain → 🔌 Ports → 🔧 Adapters
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- Bibliotecas: dataclasses, typing, decimal, uuid, datetime

### Execução

```bash
# Navegar para o diretório
cd solucao_3_1_banco_hexagonal

# Executar demonstração completa
python main.py
```

## 📁 Estrutura do Projeto

```
solucao_3_1_banco_hexagonal/
├── 📄 domain.py           # Camada de domínio (Core)
├── 📄 infrastructure.py   # Camada de infraestrutura (Adapters)
├── 📄 main.py            # Demonstração completa
└── 📄 README.md          # Esta documentação
```

## 🎯 Funcionalidades Demonstradas

### 1. Gestão de Clientes
- ✅ Criação de clientes com validação de CPF
- ✅ Consulta externa de score de crédito (Serasa)
- ✅ Validação de dados pessoais e endereço

### 2. Gestão de Contas
- ✅ Abertura de contas corrente e poupança
- ✅ Controle de limites diários
- ✅ Geração automática de números de conta

### 3. Operações Bancárias
- ✅ Transferências entre contas
- ✅ Validação de saldo e limites
- ✅ Controle de fraude inteligente
- ✅ Notificações automáticas

### 4. Recursos Avançados
- ✅ Processamento assíncrono de eventos
- ✅ Auditoria completa de transações
- ✅ Métricas de performance
- ✅ Relatórios de compliance
- ✅ Integração com serviços externos

## 🏛️ Camada de Domínio (domain.py)

### Entities (Entidades)

#### 👤 Cliente
```python
@dataclass
class Cliente:
    id: str
    nome: str
    cpf: CPF
    endereco: Endereco
    telefone: str
    email: str
    data_nascimento: datetime
    data_criacao: datetime
    ativo: bool = True
```

#### 🏦 Conta
```python
@dataclass
class Conta:
    id: str
    cliente_id: str
    agencia: str
    numero: str
    tipo: TipoConta
    saldo: Dinheiro
    limite_diario: Dinheiro
    data_criacao: datetime
    ativa: bool = True
```

#### 💰 Transacao
```python
@dataclass
class Transacao:
    id: str
    conta_id: str
    tipo: TipoTransacao
    valor: Dinheiro
    descricao: str
    status: StatusTransacao
    data_criacao: datetime
```

### Value Objects (Objetos de Valor)

#### 📋 CPF
- Validação automática de dígitos verificadores
- Formatação padronizada (xxx.xxx.xxx-xx)
- Imutabilidade garantida

#### 💵 Dinheiro
- Precisão decimal para operações financeiras
- Validação de valores negativos
- Formatação monetária brasileira

#### 🏠 Endereco
- Validação de CEP brasileiro
- Estrutura completa de endereço
- Normalização de dados

### Use Cases (Casos de Uso)

#### 👥 CriarClienteUseCase
- Validação de dados do cliente
- Consulta externa de crédito
- Prevenção de duplicação por CPF
- Geração de eventos de domínio

#### 🏦 AbrirContaUseCase
- Validação de cliente existente
- Geração de número de conta único
- Configuração de limites por tipo
- Depósito inicial obrigatório

#### 💸 RealizarTransferenciaUseCase
- Validação de saldo e limites
- Detecção de fraude inteligente
- Processamento atômico
- Notificações automáticas

## 🔧 Camada de Infraestrutura (infrastructure.py)

### Adapters de Persistência

#### 🗄️ RepositorioClienteMemoria
- Implementação em memória para testes
- Interface padronizada para futuras implementações
- Busca por CPF e ID

#### 🗄️ RepositorioContaMemoria
- Controle de numeração sequencial
- Busca por cliente e agência
- Listagem com filtros

#### 🗄️ RepositorioTransacaoMemoria
- Histórico completo de transações
- Filtros por conta e período
- Suporte a paginação

### Adapters de Serviços Externos

#### 🔍 ConsultorCreditoSerasa
- Simulação de consulta ao Serasa
- Score de crédito dinâmico
- Verificação de restrições

#### 🛡️ ValidadorFraudeInteligente
- Detecção de padrões suspeitos
- Análise de valor e frequência
- Machine Learning simulado

### Adapters de Notificação

#### 📧 NotificadorEmailSMTP
- Simulação de envio de emails
- Templates personalizados
- Configuração por cliente

### Adapters de Observabilidade

#### 📊 ColetorMetricasBanco
- Métricas de performance
- Estatísticas de operações
- Relatórios de uso

#### 📋 AuditoriaTransacoes
- Log completo de eventos
- Relatórios de compliance
- Detecção de transações suspeitas

#### ⚡ ProcessadorEventosAssincrono
- Processamento não-bloqueante
- Sistema de handlers flexível
- Tolerância a falhas

## 🎨 Princípios SOLID Aplicados

### 🔹 Single Responsibility Principle (SRP)
- **Cliente**: Apenas dados e comportamentos de cliente
- **Conta**: Apenas operações bancárias básicas
- **CriarClienteUseCase**: Apenas criação de clientes
- **ValidadorFraude**: Apenas validação de fraude

### 🔹 Open/Closed Principle (OCP)
```python
# Extensível sem modificação
class NovoNotificadorSMS(INotificador):
    def notificar_transacao_realizada(self, transacao, conta_origem, conta_destino):
        # Nova implementação
        pass

# Uso sem alterar código existente
transferencia_uc = RealizarTransferenciaUseCase(
    repo_conta, repo_transacao, validador_fraude, novo_notificador_sms
)
```

### 🔹 Liskov Substitution Principle (LSP)
```python
# Qualquer implementação de IRepositorioCliente é substituível
repo_memoria = RepositorioClienteMemoria()
repo_sqlite = RepositorioClienteSQLite()
repo_postgres = RepositorioClientePostgres()

# Todos funcionam no mesmo contexto
criar_cliente_uc = CriarClienteUseCase(repo_memoria, consultor_credito)
```

### 🔹 Interface Segregation Principle (ISP)
```python
# Interfaces específicas e focadas
class IRepositorioCliente(Protocol):
    def salvar(self, cliente: Cliente) -> None: ...
    def buscar_por_id(self, cliente_id: str) -> Optional[Cliente]: ...
    def buscar_por_cpf(self, cpf: CPF) -> Optional[Cliente]: ...

class IValidadorFraude(Protocol):
    def validar_transacao(self, conta_origem: Conta, valor: Dinheiro) -> bool: ...

# Sem métodos desnecessários
```

### 🔹 Dependency Inversion Principle (DIP)
```python
# Casos de uso dependem de abstrações, não implementações
class RealizarTransferenciaUseCase:
    def __init__(self, 
                 repo_conta: IRepositorioConta,        # Abstração
                 repo_transacao: IRepositorioTransacao, # Abstração
                 validador_fraude: IValidadorFraude,    # Abstração
                 notificador: INotificador):            # Abstração
        # Dependências invertidas
```

## 🎨 Design Patterns Implementados

### 🏭 Repository Pattern
- Abstração da camada de persistência
- Interfaces padronizadas para acesso a dados
- Implementações intercambiáveis

### 📋 Command Pattern
- Encapsulamento de operações complexas
- Comandos reutilizáveis e testáveis
- Separação entre requisição e execução

### 👀 Observer Pattern
- Sistema de eventos desacoplado
- Processamento assíncrono
- Extensibilidade para novos handlers

### 🔧 Adapter Pattern
- Integração com sistemas externos
- Conversão de interfaces incompatíveis
- Isolamento de dependências externas

### 🏭 Factory Pattern
- Criação de objetos complexos
- Encapsulamento da lógica de criação
- Flexibilidade na instanciação

### 🎯 Strategy Pattern
- Algoritmos intercambiáveis
- Validação de fraude configurável
- Políticas de negócio flexíveis

## 🧪 Testabilidade

### Vantagens da Arquitetura

```python
# Teste unitário do domínio (sem dependências externas)
def test_transferencia_saldo_insuficiente():
    conta = Conta.criar(cliente_id="123", tipo=TipoConta.CORRENTE, 
                       agencia="0001", deposito_inicial=Decimal("100"))
    
    with pytest.raises(SaldoInsuficienteError):
        conta.debitar(Dinheiro(Decimal("200")))

# Teste de integração com mocks
def test_transferencia_use_case():
    repo_conta_mock = Mock(spec=IRepositorioConta)
    validador_mock = Mock(spec=IValidadorFraude)
    
    use_case = RealizarTransferenciaUseCase(
        repo_conta_mock, repo_transacao_mock, 
        validador_mock, notificador_mock
    )
    
    # Teste isolado do caso de uso
```

### Isolamento de Dependências
- **Domínio**: Testável sem infraestrutura
- **Casos de Uso**: Testáveis com mocks
- **Adapters**: Testáveis individualmente
- **Integração**: Testável de ponta a ponta

## 📈 Extensibilidade

### Adicionando Novos Adapters

```python
# Novo adapter para blockchain
class RepositorioContaBlockchain(IRepositorioConta):
    def salvar(self, conta: Conta) -> None:
        # Implementação blockchain
        pass

# Novo adapter para IA de fraude
class ValidadorFraudeIA(IValidadorFraude):
    def validar_transacao(self, conta_origem: Conta, valor: Dinheiro) -> bool:
        # Machine Learning real
        pass

# Uso sem alterar código existente
transferencia_uc = RealizarTransferenciaUseCase(
    RepositorioContaBlockchain(),
    repo_transacao,
    ValidadorFraudeIA(),
    notificador
)
```

### Adicionando Novos Casos de Uso

```python
class EmprestimoUseCase:
    def __init__(self, 
                 repo_conta: IRepositorioConta,
                 consultor_credito: IConsultorCredito,
                 motor_riscos: IMotorRiscos):
        # Novo caso de uso usando infraestrutura existente
        pass
```

## 🔐 Segurança e Compliance

### Validação de Fraude
- Análise de padrões de transação
- Limites dinâmicos por conta
- Bloqueio automático de operações suspeitas
- Machine Learning para detecção

### Auditoria
- Log completo de todas as operações
- Rastreabilidade de eventos
- Relatórios de compliance
- Detecção de anomalias

### Dados Sensíveis
- Validação rigorosa de CPF
- Encriptação de dados pessoais (simulada)
- Controle de acesso granular
- Política de retenção de dados

## 📊 Métricas e Monitoramento

### Performance
- Tempo de resposta por operação
- Throughput de transações
- Uso de recursos
- Latência de APIs externas

### Negócio
- Volume de transações
- Valores movimentados
- Taxa de fraude detectada
- Score médio de clientes

### Operacional
- Disponibilidade do sistema
- Taxa de erro por operação
- Tempo de processamento de eventos
- Saúde das integrações

## 🎓 Conceitos Avançados Demonstrados

### Domain-Driven Design
- **Ubiquitous Language**: Linguagem do domínio bancário
- **Bounded Contexts**: Contexto bem definido
- **Entities vs Value Objects**: Distinção clara
- **Domain Events**: Comunicação entre agregados
- **Rich Domain Model**: Comportamentos no domínio

### Arquitetura Hexagonal
- **Isolation**: Domínio isolado de infraestrutura
- **Dependency Inversion**: Dependências apontam para dentro
- **Ports**: Contratos bem definidos
- **Adapters**: Implementações específicas
- **Testability**: Testável em isolamento

### Clean Architecture
- **Independence**: Camadas independentes
- **Testability**: Testável sem UI/DB/Web
- **Flexibility**: Mudanças de infraestrutura fáceis
- **Business Rules**: Regras de negócio centralizadas

## 🚀 Próximos Passos

### Melhorias Possíveis
1. **Persistência Real**: Implementar adapters para PostgreSQL/MongoDB
2. **API REST**: Adicionar camada de apresentação HTTP
3. **Testes Automatizados**: Suite completa de testes
4. **Cache**: Sistema de cache para performance
5. **Configuração**: Sistema de configuração flexível
6. **Logging**: Sistema de logging estruturado
7. **Métricas**: Integração com Prometheus/Grafana
8. **Segurança**: Autenticação e autorização

### Padrões Adicionais
- **Event Sourcing**: Histórico completo de eventos
- **CQRS**: Separação de comando e consulta
- **Saga Pattern**: Transações distribuídas
- **Circuit Breaker**: Resiliência a falhas
- **Retry Pattern**: Tentativas automáticas

## 📚 Referências e Estudos

### Livros Recomendados
- "Clean Architecture" - Robert C. Martin
- "Domain-Driven Design" - Eric Evans
- "Implementing Domain-Driven Design" - Vaughn Vernon
- "Building Microservices" - Sam Newman
- "Patterns of Enterprise Application Architecture" - Martin Fowler

### Conceitos Relacionados
- **Microservices Architecture**
- **Event-Driven Architecture**
- **SOLID Principles**
- **Design Patterns**
- **Clean Code**

---

## 👨‍🏫 Sobre o Autor

**Prof. Jackson Antonio do Prado Lima**  
Especialista em Arquitetura de Software e Programação Orientada a Objetos

Este projeto foi desenvolvido para fins educacionais, demonstrando na prática os conceitos mais importantes da arquitetura de software moderna.

---

**🎯 Objetivo**: Demonstrar arquitetura de software de qualidade empresarial aplicando princípios fundamentais de forma prática e educativa.
