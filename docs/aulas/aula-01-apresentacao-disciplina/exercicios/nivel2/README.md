# 🟡 Exercícios Nível 2 - Intermediário

## Exercício 2.1: Sistema de E-commerce com SOLID (60 min)

### 📋 Descrição
Desenvolva um sistema de e-commerce aplicando **todos os cinco princípios SOLID** de forma integrada. Este exercício combina múltiplos conceitos em um cenário realista.

### 🎯 Cenário de Negócio
Você deve criar um sistema para uma loja online que:
- Gerencia produtos com diferentes tipos (físicos, digitais, serviços)
- Processa pedidos com diferentes métodos de pagamento
- Calcula fretes baseado em estratégias específicas
- Envia notificações por diferentes canais
- Aplica descontos conforme regras de negócio

### 📋 Requisitos Funcionais

#### **Gestão de Produtos:**
- Produtos físicos têm peso e dimensões
- Produtos digitais têm tamanho de arquivo e licença
- Serviços têm duração e categoria

#### **Processamento de Pedidos:**
- Calcular valor total com impostos
- Aplicar descontos baseados em regras
- Validar disponibilidade de estoque
- Processar pagamento através de diferentes gateways

#### **Cálculo de Frete:**
- Frete grátis para pedidos acima de R$ 100
- Cálculo por peso para produtos físicos
- Produtos digitais não têm frete
- Serviços têm taxa fixa opcional

#### **Sistema de Notificações:**
- Email para confirmação de pedido
- SMS para mudanças de status
- Push notification para ofertas

### 📋 Requisitos Técnicos

#### **Aplicação dos Princípios SOLID:**

1. **SRP**: Cada classe tem uma responsabilidade específica
2. **OCP**: Sistema extensível para novos tipos sem modificação
3. **LSP**: Substituição correta de implementações
4. **ISP**: Interfaces específicas para diferentes necessidades
5. **DIP**: Dependência de abstrações, não implementações

#### **Padrões de Design Requeridos:**
- **Strategy**: Para cálculo de frete e desconto
- **Factory Method**: Para criação de produtos
- **Observer**: Para notificações de mudança de status
- **Adapter**: Para diferentes gateways de pagamento

### 💻 Estrutura Base

```python
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Protocol
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# =============================================================================
# MODELOS DE DOMÍNIO
# =============================================================================

class TipoProduto(Enum):
    FISICO = "fisico"
    DIGITAL = "digital" 
    SERVICO = "servico"

class StatusPedido(Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

@dataclass
class DimensoesProduto:
    altura: float  # cm
    largura: float  # cm
    profundidade: float  # cm
    peso: float  # kg

# =============================================================================
# INTERFACES E ABSTRAÇÕES (ISP + DIP)
# =============================================================================

class Produto(ABC):
    """Classe base para todos os produtos (SRP)"""
    
    def __init__(self, id: str, nome: str, preco: Decimal, categoria: str):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
    
    @abstractmethod
    def get_tipo(self) -> TipoProduto:
        pass
    
    @abstractmethod
    def validar_disponibilidade(self) -> bool:
        pass

class CalculadoraFrete(Protocol):
    """Interface para estratégias de cálculo de frete (ISP)"""
    
    def calcular(self, produtos: List[Produto], destino: str) -> Decimal:
        pass

class ProcessadorPagamento(Protocol):
    """Interface para gateways de pagamento (ISP + DIP)"""
    
    def processar(self, valor: Decimal, dados_pagamento: dict) -> bool:
        pass

class ServicoNotificacao(Protocol):
    """Interface para notificações (ISP)"""
    
    def enviar(self, destinatario: str, mensagem: str) -> bool:
        pass

class ObservadorPedido(Protocol):
    """Interface para observadores de pedido (Observer Pattern)"""
    
    def notificar_mudanca_status(self, pedido_id: str, status: StatusPedido) -> None:
        pass

# =============================================================================
# SEU TRABALHO COMEÇA AQUI
# =============================================================================

# TODO 1: Implementar classes concretas de produtos (SRP + LSP)
class ProdutoFisico(Produto):
    """Produto físico com dimensões e peso"""
    # Implementar: dimensoes, peso, estoque
    pass

class ProdutoDigital(Produto):
    """Produto digital com tamanho de arquivo e licença"""
    # Implementar: tamanho_arquivo, tipo_licenca, url_download
    pass

class ProdutoServico(Produto):
    """Serviço com duração e categoria"""
    # Implementar: duracao_horas, categoria_servico
    pass

# TODO 2: Implementar Factory para criação de produtos (Factory Method + OCP)
class FabricaProdutos:
    """Factory para criação de diferentes tipos de produto"""
    
    @staticmethod
    def criar_produto(tipo: TipoProduto, **kwargs) -> Produto:
        # Implementar factory method
        pass

# TODO 3: Implementar estratégias de frete (Strategy Pattern)
class FreteGratis:
    """Estratégia de frete grátis para pedidos acima de valor mínimo"""
    pass

class FretePorPeso:
    """Estratégia de frete baseada no peso total"""
    pass

class FreteTaxaFixa:
    """Estratégia de frete com taxa fixa"""
    pass

# TODO 4: Implementar adaptadores para pagamento (Adapter Pattern)
class AdaptadorPayPal:
    """Adaptador para gateway PayPal"""
    pass

class AdaptadorStripe:
    """Adaptador para gateway Stripe"""
    pass

# TODO 5: Implementar serviços de notificação (Strategy + Observer)
class NotificacaoEmail:
    """Serviço de notificação por email"""
    pass

class NotificacaoSMS:
    """Serviço de notificação por SMS"""
    pass

# TODO 6: Implementar classe principal Pedido (SRP + Observer)
class Pedido:
    """Classe principal que coordena o processo de pedido"""
    
    def __init__(self, id: str, cliente_email: str):
        self.id = id
        self.cliente_email = cliente_email
        self.produtos: List[Produto] = []
        self.status = StatusPedido.PENDENTE
        self.observadores: List[ObservadorPedido] = []
        self.data_criacao = datetime.now()
        
        # Injeção de dependências (DIP)
        self._calculadora_frete: CalculadoraFrete = None
        self._processador_pagamento: ProcessadorPagamento = None
    
    def configurar_dependencias(self, 
                               calculadora_frete: CalculadoraFrete,
                               processador_pagamento: ProcessadorPagamento):
        """Configuração de dependências (DIP)"""
        self._calculadora_frete = calculadora_frete
        self._processador_pagamento = processador_pagamento
    
    def adicionar_produto(self, produto: Produto) -> None:
        """Adiciona produto ao pedido"""
        # TODO: Implementar validação e adição
        pass
    
    def calcular_total(self) -> Decimal:
        """Calcula valor total incluindo frete"""
        # TODO: Implementar cálculo
        pass
    
    def processar_pedido(self, dados_pagamento: dict, endereco_entrega: str) -> bool:
        """Processa o pedido completo"""
        # TODO: Implementar fluxo completo:
        # 1. Validar produtos
        # 2. Calcular total com frete
        # 3. Processar pagamento
        # 4. Atualizar status
        # 5. Notificar observadores
        pass
    
    def adicionar_observador(self, observador: ObservadorPedido) -> None:
        """Adiciona observador para mudanças de status"""
        pass
    
    def _notificar_observadores(self) -> None:
        """Notifica todos os observadores sobre mudança de status"""
        pass

# TODO 7: Implementar observador para notificações automáticas
class GerenciadorNotificacoes:
    """Observador que gerencia notificações automáticas"""
    
    def __init__(self, servico_email: ServicoNotificacao, servico_sms: ServicoNotificacao):
        self._servico_email = servico_email
        self._servico_sms = servico_sms
    
    def notificar_mudanca_status(self, pedido_id: str, status: StatusPedido) -> None:
        """Implementar lógica de notificação baseada no status"""
        pass
```

### 🧪 Cenários de Teste Obrigatórios

```python
def test_criacao_produtos_diferentes_tipos():
    """Testa factory e polimorfismo de produtos"""
    pass

def test_calculo_frete_estrategias_diferentes():
    """Testa strategy pattern para frete"""
    pass

def test_processamento_pedido_completo():
    """Testa fluxo completo de pedido"""
    pass

def test_notificacoes_automaticas():
    """Testa observer pattern para notificações"""
    pass

def test_substituicao_gateways_pagamento():
    """Testa adapter pattern e DIP"""
    pass

def test_extensibilidade_novos_produtos():
    """Testa OCP - adicionar novo tipo sem modificar código"""
    pass
```

### 📝 Exemplo de Uso Esperado

```python
# Configuração do sistema
fabrica = FabricaProdutos()
frete_strategy = FretePorPeso(taxa_por_kg=5.00)
pagamento_adapter = AdaptadorPayPal()
notificacao_email = NotificacaoEmail()
notificacao_sms = NotificacaoSMS()

# Criar produtos
produto1 = fabrica.criar_produto(
    TipoProduto.FISICO,
    id="001", nome="Notebook", preco=Decimal("2500.00"),
    peso=2.5, altura=30, largura=40, profundidade=3
)

produto2 = fabrica.criar_produto(
    TipoProduto.DIGITAL,
    id="002", nome="Software", preco=Decimal("99.00"),
    tamanho_arquivo=150, tipo_licenca="single_user"
)

# Criar e processar pedido
pedido = Pedido("PED001", "cliente@email.com")
pedido.configurar_dependencias(frete_strategy, pagamento_adapter)

# Adicionar observador de notificações
gerenciador_notif = GerenciadorNotificacoes(notificacao_email, notificacao_sms)
pedido.adicionar_observador(gerenciador_notif)

# Processar
pedido.adicionar_produto(produto1)
pedido.adicionar_produto(produto2)

sucesso = pedido.processar_pedido(
    dados_pagamento={"token": "xyz123"},
    endereco_entrega="Rua A, 123"
)

print(f"Pedido processado: {sucesso}")
print(f"Total: R$ {pedido.calcular_total()}")
```

---

## Exercício 2.2: Sistema de Logger com Chain of Responsibility (45 min)

### 📋 Descrição
Implemente um sistema de logging aplicando o **Chain of Responsibility Pattern** integrado com **Strategy Pattern** para diferentes formatadores.

### 🎯 Objetivo
Criar um sistema flexível de logging onde diferentes handlers processam mensagens baseados em níveis de severidade, com formatação personalizada.

### 📋 Requisitos

#### **Níveis de Log:**
- **DEBUG**: Informações detalhadas para desenvolvimento
- **INFO**: Informações gerais do sistema  
- **WARNING**: Avisos que não impedem execução
- **ERROR**: Erros que impedem operação específica
- **CRITICAL**: Erros críticos que podem parar o sistema

#### **Handlers Requeridos:**
- **ConsoleHandler**: Exibe logs no console (DEBUG e acima)
- **FileHandler**: Salva logs em arquivo (INFO e acima)
- **EmailHandler**: Envia logs críticos por email (ERROR e acima)
- **DatabaseHandler**: Persiste logs importantes (WARNING e acima)

#### **Formatadores:**
- **SimpleFormatter**: Apenas a mensagem
- **DetailedFormatter**: Timestamp + nível + mensagem
- **JSONFormatter**: Formato JSON estruturado

### 💻 Código Base

```python
from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum
from typing import Optional, Protocol
import json

class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class LogRecord:
    def __init__(self, level: LogLevel, message: str, timestamp: datetime = None):
        self.level = level
        self.message = message
        self.timestamp = timestamp or datetime.now()
        self.level_name = level.name

# TODO: Implementar Strategy Pattern para formatadores
class LogFormatter(Protocol):
    def format(self, record: LogRecord) -> str:
        pass

class SimpleFormatter:
    """Formatador simples - apenas mensagem"""
    pass

class DetailedFormatter:
    """Formatador detalhado com timestamp e nível"""
    pass

class JSONFormatter:
    """Formatador JSON estruturado"""
    pass

# TODO: Implementar Chain of Responsibility
class LogHandler(ABC):
    """Handler base para Chain of Responsibility"""
    
    def __init__(self, level: LogLevel, formatter: LogFormatter):
        self._level = level
        self._formatter = formatter
        self._next_handler: Optional[LogHandler] = None
    
    def set_next(self, handler: 'LogHandler') -> 'LogHandler':
        """Define próximo handler na chain"""
        self._next_handler = handler
        return handler
    
    def handle(self, record: LogRecord) -> None:
        """Processa log record na chain"""
        if self._can_handle(record):
            self._do_handle(record)
        
        if self._next_handler:
            self._next_handler.handle(record)
    
    def _can_handle(self, record: LogRecord) -> bool:
        """Verifica se handler deve processar este record"""
        return record.level >= self._level
    
    @abstractmethod
    def _do_handle(self, record: LogRecord) -> None:
        """Implementação específica do handler"""
        pass

# TODO: Implementar handlers concretos
class ConsoleHandler(LogHandler):
    """Handler para output no console"""
    pass

class FileHandler(LogHandler):
    """Handler para salvamento em arquivo"""
    
    def __init__(self, level: LogLevel, formatter: LogFormatter, filename: str):
        super().__init__(level, formatter)
        self._filename = filename
    
    # TODO: Implementar _do_handle
    pass

class EmailHandler(LogHandler):
    """Handler para envio de logs críticos por email"""
    
    def __init__(self, level: LogLevel, formatter: LogFormatter, 
                 email_to: str, email_subject: str = "Sistema - Log Crítico"):
        super().__init__(level, formatter)
        self._email_to = email_to
        self._email_subject = email_subject
    
    # TODO: Implementar _do_handle (simulação)
    pass

class DatabaseHandler(LogHandler):
    """Handler para persistência em banco de dados"""
    
    def __init__(self, level: LogLevel, formatter: LogFormatter, connection_string: str):
        super().__init__(level, formatter)
        self._connection = connection_string
    
    # TODO: Implementar _do_handle (simulação)
    pass

# TODO: Implementar Logger principal
class Logger:
    """Logger principal que usa Chain of Responsibility"""
    
    def __init__(self, name: str):
        self.name = name
        self._handler_chain: Optional[LogHandler] = None
    
    def add_handler(self, handler: LogHandler) -> None:
        """Adiciona handler à chain"""
        if self._handler_chain is None:
            self._handler_chain = handler
        else:
            # TODO: Adicionar ao final da chain
            pass
    
    def _log(self, level: LogLevel, message: str) -> None:
        """Método interno para logging"""
        if self._handler_chain:
            record = LogRecord(level, message)
            self._handler_chain.handle(record)
    
    def debug(self, message: str) -> None:
        self._log(LogLevel.DEBUG, message)
    
    def info(self, message: str) -> None:
        self._log(LogLevel.INFO, message)
    
    def warning(self, message: str) -> None:
        self._log(LogLevel.WARNING, message)
    
    def error(self, message: str) -> None:
        self._log(LogLevel.ERROR, message)
    
    def critical(self, message: str) -> None:
        self._log(LogLevel.CRITICAL, message)
```

### 📝 Exemplo de Uso Esperado

```python
# Configurar formatadores
simple_fmt = SimpleFormatter()
detailed_fmt = DetailedFormatter()
json_fmt = JSONFormatter()

# Configurar handlers
console_handler = ConsoleHandler(LogLevel.DEBUG, detailed_fmt)
file_handler = FileHandler(LogLevel.INFO, detailed_fmt, "app.log")
email_handler = EmailHandler(LogLevel.ERROR, simple_fmt, "admin@empresa.com")
db_handler = DatabaseHandler(LogLevel.WARNING, json_fmt, "sqlite:///logs.db")

# Montar chain
console_handler.set_next(file_handler).set_next(db_handler).set_next(email_handler)

# Configurar logger
logger = Logger("MyApp")
logger.add_handler(console_handler)

# Usar logger
logger.debug("Iniciando aplicação")           # Só console
logger.info("Usuário fez login")              # Console + arquivo
logger.warning("Cache quase cheio")           # Console + arquivo + DB
logger.error("Falha na conexão")              # Todos os handlers
logger.critical("Sistema indisponível")       # Todos os handlers
```

### 🧪 Casos de Teste

```python
def test_chain_processa_niveis_corretos():
    """Verifica se cada handler processa apenas níveis apropriados"""
    pass

def test_formatadores_diferentes():
    """Testa se formatadores produzem outputs esperados"""
    pass

def test_chain_completa():
    """Verifica se chain processa em sequência correta"""
    pass

def test_handler_unico():
    """Testa logger com apenas um handler"""
    pass
```

---

## 📊 Resumo do Nível 2

Ao completar estes exercícios, você terá integrado:

✅ **Todos os 5 Princípios SOLID**
✅ **Strategy + Factory + Observer + Adapter**
✅ **Chain of Responsibility**
✅ **Dependency Injection Avançada**
✅ **Arquitetura em Camadas**

### 🎯 Próximos Passos
Com domínio destes padrões integrados, você está pronto para o **[Nível 3](../nivel3/README.md)** - arquiteturas complexas e patterns empresariais.

---

**⏱️ Tempo estimado total: 105 minutos**
**🎖️ Nível de dificuldade: Intermediário**
**📚 Conceitos integrados: SOLID completo, múltiplos Design Patterns**
