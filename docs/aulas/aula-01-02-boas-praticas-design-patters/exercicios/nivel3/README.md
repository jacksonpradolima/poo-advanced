# 🔴 Exercícios Nível 3 - Avançado

## Exercício 3.1: Sistema Bancário com Arquitetura Hexagonal (3-4 horas)

### 📋 Descrição
Desenvolva um sistema bancário completo aplicando **Arquitetura Hexagonal (Ports & Adapters)**, **Domain-Driven Design (DDD)**, e múltiplos **Design Patterns** em uma solução empresarial robusta.

### 🎯 Cenário de Negócio
Implemente um sistema bancário que suporte:
- Gestão de contas (Corrente, Poupança, Investimento)
- Transações complexas (Transferências, PIX, TED, DOC)
- Processamento de empréstimos com análise de risco
- Notificações multicanal em tempo real
- Auditoria completa de operações
- Integração com serviços externos (Bacen, SPC, Serasa)

### 🏗️ Arquitetura Hexagonal Requerida

```
┌─────────────────────────────────────────────────────────────┐
│                        ADAPTERS (Infrastructure)             │
├─────────────────────────────────────────────────────────────┤
│  Web API    │  CLI    │  Database  │  External APIs  │ Queue │
│  (FastAPI)  │ (Click) │ (SQLAlch.) │ (HTTP/gRPC)    │(Redis)│
└─────────────┬───────────────────────────────────────┬───────┘
              │                PORTS                   │
┌─────────────▼───────────────────────────────────────▼───────┐
│                     APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│     Use Cases    │   Command/Query Handlers  │   Events     │
│   (Services)     │      (CQRS Pattern)       │ (Observers)  │
└─────────────┬───────────────────────────────────────┬───────┘
              │              DOMAIN               │
┌─────────────▼───────────────────────────────────────▼───────┐
│                      DOMAIN LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  Entities  │ Value Objects │ Domain Services │ Repositories │
│ (Agregates)│   (Immutable) │   (Pure Logic)  │ (Interfaces) │
└─────────────────────────────────────────────────────────────┘
```

### 📋 Requisitos Funcionais Complexos

#### **RF001 - Gestão de Contas**
- Criar conta com validação de documentos
- Aplicar regras específicas por tipo de conta
- Controlar limites e saldos em tempo real
- Histórico completo de alterações

#### **RF002 - Transações Avançadas**
- Transferências com validação de fundos
- PIX instantâneo com chave e QR Code
- TED/DOC com agendamento
- Estorno automático em caso de falha

#### **RF003 - Sistema de Empréstimos**
- Análise de risco baseada em score
- Simulação de parcelas com diferentes taxas
- Aprovação automática/manual baseada em regras
- Controle de inadimplência

#### **RF004 - Auditoria e Compliance**
- Log de todas as operações
- Rastreabilidade completa
- Relatórios regulatórios
- Detecção de fraudes

### 📋 Requisitos Técnicos

#### **Padrões de Design Obrigatórios:**
- **Command Pattern**: Para operações transacionais
- **Strategy Pattern**: Para cálculo de juros e taxas
- **Factory Pattern**: Para criação de diferentes tipos de conta
- **Observer Pattern**: Para notificações e auditoria
- **State Pattern**: Para status de transações
- **Specification Pattern**: Para regras de negócio complexas
- **Repository Pattern**: Para persistência
- **Unit of Work**: Para controle transacional

#### **Princípios Arquiteturais:**
- **Domain-Driven Design**: Linguagem ubíqua e bounded contexts
- **CQRS**: Separação de comandos e consultas
- **Event Sourcing**: Para auditoria (opcional avançado)
- **Dependency Injection**: Inversão de controle completa

### 💻 Estrutura Base da Solução

```python
# =============================================================================
# DOMAIN LAYER - Núcleo da aplicação, independente de frameworks
# =============================================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Protocol
from enum import Enum
import uuid

# Value Objects (Imutáveis, sem identidade)
@dataclass(frozen=True)
class CPF:
    """Value Object para CPF com validação"""
    numero: str
    
    def __post_init__(self):
        if not self._validar_cpf(self.numero):
            raise ValueError(f"CPF inválido: {self.numero}")
    
    def _validar_cpf(self, cpf: str) -> bool:
        # TODO: Implementar validação real de CPF
        return len(cpf) == 11 and cpf.isdigit()

@dataclass(frozen=True)
class Dinheiro:
    """Value Object para representar valores monetários"""
    valor: Decimal
    moeda: str = "BRL"
    
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Valor não pode ser negativo")
    
    def somar(self, outro: 'Dinheiro') -> 'Dinheiro':
        if self.moeda != outro.moeda:
            raise ValueError("Moedas diferentes")
        return Dinheiro(self.valor + outro.valor, self.moeda)
    
    def subtrair(self, outro: 'Dinheiro') -> 'Dinheiro':
        if self.moeda != outro.moeda:
            raise ValueError("Moedas diferentes")
        resultado = self.valor - outro.valor
        return Dinheiro(resultado, self.moeda)

# Enums para o domínio
class TipoConta(Enum):
    CORRENTE = "corrente"
    POUPANCA = "poupanca"
    INVESTIMENTO = "investimento"

class StatusTransacao(Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    CONCLUIDA = "concluida"
    FALHADA = "falhada"
    ESTORNADA = "estornada"

class TipoTransacao(Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"
    TRANSFERENCIA = "transferencia"
    PIX = "pix"
    TED = "ted"
    DOC = "doc"

# Domain Events
@dataclass(frozen=True)
class EventoDominio:
    """Evento base do domínio"""
    id: str
    timestamp: datetime
    agregado_id: str

@dataclass(frozen=True)
class ContaCriada(EventoDominio):
    cpf_titular: str
    tipo_conta: TipoConta
    saldo_inicial: Decimal

@dataclass(frozen=True)
class TransacaoRealizada(EventoDominio):
    conta_origem: str
    conta_destino: Optional[str]
    tipo: TipoTransacao
    valor: Decimal
    status: StatusTransacao

# Especificações para regras de negócio complexas
class EspecificacaoNegocio(ABC):
    """Base para Specification Pattern"""
    
    @abstractmethod
    def satisfeita_por(self, candidate) -> bool:
        pass
    
    def e(self, other: 'EspecificacaoNegocio') -> 'EspecificacaoE':
        return EspecificacaoE(self, other)
    
    def ou(self, other: 'EspecificacaoNegocio') -> 'EspecificacaoOu':
        return EspecificacaoOu(self, other)

class EspecificacaoE(EspecificacaoNegocio):
    def __init__(self, left: EspecificacaoNegocio, right: EspecificacaoNegocio):
        self.left = left
        self.right = right
    
    def satisfeita_por(self, candidate) -> bool:
        return self.left.satisfeita_por(candidate) and self.right.satisfeita_por(candidate)

class EspecificacaoOu(EspecificacaoNegocio):
    def __init__(self, left: EspecificacaoNegocio, right: EspecificacaoNegocio):
        self.left = left
        self.right = right
    
    def satisfeita_por(self, candidate) -> bool:
        return self.left.satisfeita_por(candidate) or self.right.satisfeita_por(candidate)

# TODO: Implementar especificações específicas
class ContaTemSaldoSuficiente(EspecificacaoNegocio):
    """Especificação para verificar saldo suficiente"""
    def __init__(self, valor_minimo: Dinheiro):
        self.valor_minimo = valor_minimo
    
    def satisfeita_por(self, conta) -> bool:
        # TODO: Implementar lógica
        pass

class ClienteElegiveEmprestimo(EspecificacaoNegocio):
    """Especificação complexa para elegibilidade de empréstimo"""
    def __init__(self, score_minimo: int, renda_minima: Dinheiro):
        self.score_minimo = score_minimo
        self.renda_minima = renda_minima
    
    def satisfeita_por(self, cliente) -> bool:
        # TODO: Implementar regras complexas
        pass

# Entidades e Agregados
class Conta:
    """Agregado raiz para operações bancárias"""
    
    def __init__(self, numero: str, cpf_titular: CPF, tipo: TipoConta, 
                 saldo_inicial: Dinheiro = Dinheiro(Decimal("0"))):
        self.numero = numero
        self.cpf_titular = cpf_titular
        self.tipo = tipo
        self._saldo = saldo_inicial
        self._ativa = True
        self._limite = self._calcular_limite_inicial()
        self._historico: List[TransacaoRealizada] = []
        self._eventos: List[EventoDominio] = []
        
        # Registrar evento de criação
        self._registrar_evento(ContaCriada(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            agregado_id=self.numero,
            cpf_titular=cpf_titular.numero,
            tipo_conta=tipo,
            saldo_inicial=saldo_inicial.valor
        ))
    
    @property
    def saldo(self) -> Dinheiro:
        return self._saldo
    
    @property
    def ativa(self) -> bool:
        return self._ativa
    
    def debitar(self, valor: Dinheiro, especificacao: EspecificacaoNegocio = None) -> bool:
        """Debita valor da conta aplicando regras de negócio"""
        if not self._ativa:
            raise ValueError("Conta inativa")
        
        if especificacao and not especificacao.satisfeita_por(self):
            return False
        
        if self._saldo.valor < valor.valor:
            return False
        
        self._saldo = self._saldo.subtrair(valor)
        return True
    
    def creditar(self, valor: Dinheiro) -> None:
        """Credita valor na conta"""
        if not self._ativa:
            raise ValueError("Conta inativa")
        
        self._saldo = self._saldo.somar(valor)
    
    def _calcular_limite_inicial(self) -> Dinheiro:
        """Calcula limite baseado no tipo de conta"""
        limites = {
            TipoConta.CORRENTE: Dinheiro(Decimal("1000")),
            TipoConta.POUPANCA: Dinheiro(Decimal("0")),
            TipoConta.INVESTIMENTO: Dinheiro(Decimal("5000"))
        }
        return limites.get(self.tipo, Dinheiro(Decimal("0")))
    
    def _registrar_evento(self, evento: EventoDominio) -> None:
        """Registra evento para posterior publicação"""
        self._eventos.append(evento)
    
    def obter_eventos_nao_publicados(self) -> List[EventoDominio]:
        """Retorna eventos não publicados"""
        return self._eventos.copy()
    
    def marcar_eventos_como_publicados(self) -> None:
        """Marca eventos como publicados"""
        self._eventos.clear()

# TODO: Implementar Transacao como entidade
class Transacao:
    """Entidade que representa uma transação bancária"""
    
    def __init__(self, tipo: TipoTransacao, valor: Dinheiro, 
                 conta_origem: str, conta_destino: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.tipo = tipo
        self.valor = valor
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.status = StatusTransacao.PENDENTE
        self.timestamp_criacao = datetime.now()
        self.timestamp_conclusao: Optional[datetime] = None
        self._historico_status: List[tuple] = []
    
    def alterar_status(self, novo_status: StatusTransacao) -> None:
        """Altera status da transação (State Pattern)"""
        # TODO: Implementar State Pattern para transições válidas
        pass
    
    def pode_ser_estornada(self) -> bool:
        """Verifica se transação pode ser estornada"""
        # TODO: Implementar regras de estorno
        pass

# =============================================================================
# APPLICATION LAYER - Casos de uso e orquestração
# =============================================================================

# Ports (Interfaces)
class RepositorioConta(Protocol):
    """Port para persistência de contas"""
    
    def salvar(self, conta: Conta) -> None: ...
    def buscar_por_numero(self, numero: str) -> Optional[Conta]: ...
    def buscar_por_cpf(self, cpf: CPF) -> List[Conta]: ...

class RepositorioTransacao(Protocol):
    """Port para persistência de transações"""
    
    def salvar(self, transacao: Transacao) -> None: ...
    def buscar_por_id(self, id: str) -> Optional[Transacao]: ...
    def buscar_por_conta(self, numero_conta: str) -> List[Transacao]: ...

class ServicoNotificacao(Protocol):
    """Port para serviço de notificações"""
    
    def enviar_notificacao(self, destinatario: str, mensagem: str, canal: str) -> bool: ...

class ServicoAntifrude(Protocol):
    """Port para serviço de detecção de fraudes"""
    
    def analisar_transacao(self, transacao: Transacao) -> bool: ...

class UnidadeTrabalho(Protocol):
    """Port para Unit of Work pattern"""
    
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

# Commands (CQRS)
@dataclass
class ComandoCriarConta:
    cpf: str
    tipo: TipoConta
    saldo_inicial: Decimal

@dataclass
class ComandoRealizarTransferencia:
    conta_origem: str
    conta_destino: str
    valor: Decimal
    tipo: TipoTransacao = TipoTransacao.TRANSFERENCIA

# Command Handlers
class ManipuladorComandoCriarConta:
    """Handler para criação de conta (Command Pattern)"""
    
    def __init__(self, repo_conta: RepositorioConta, 
                 servico_notificacao: ServicoNotificacao,
                 unidade_trabalho: UnidadeTrabalho):
        self._repo_conta = repo_conta
        self._servico_notificacao = servico_notificacao
        self._unidade_trabalho = unidade_trabalho
    
    def handle(self, comando: ComandoCriarConta) -> str:
        """Processa comando de criação de conta"""
        with self._unidade_trabalho:
            # Validar CPF
            cpf = CPF(comando.cpf)
            
            # Verificar se já existe conta
            contas_existentes = self._repo_conta.buscar_por_cpf(cpf)
            if len(contas_existentes) >= 3:  # Regra de negócio: máx 3 contas
                raise ValueError("Cliente já possui número máximo de contas")
            
            # Criar conta
            numero_conta = self._gerar_numero_conta()
            saldo_inicial = Dinheiro(comando.saldo_inicial)
            conta = Conta(numero_conta, cpf, comando.tipo, saldo_inicial)
            
            # Salvar
            self._repo_conta.salvar(conta)
            
            # Publicar eventos
            self._publicar_eventos(conta)
            
            self._unidade_trabalho.commit()
            return numero_conta
    
    def _gerar_numero_conta(self) -> str:
        """Gera número único de conta"""
        # TODO: Implementar geração de número único
        return str(uuid.uuid4())[:8]
    
    def _publicar_eventos(self, conta: Conta) -> None:
        """Publica eventos do agregado"""
        eventos = conta.obter_eventos_nao_publicados()
        for evento in eventos:
            # TODO: Publicar evento (Observer Pattern)
            pass
        conta.marcar_eventos_como_publicados()

# TODO: Implementar outros handlers
class ManipuladorComandoTransferencia:
    """Handler para transferências (Command Pattern + Strategy)"""
    
    def __init__(self, repo_conta: RepositorioConta, 
                 repo_transacao: RepositorioTransacao,
                 servico_antifrude: ServicoAntifrude,
                 unidade_trabalho: UnidadeTrabalho):
        self._repo_conta = repo_conta
        self._repo_transacao = repo_transacao
        self._servico_antifrude = servico_antifrude
        self._unidade_trabalho = unidade_trabalho
    
    def handle(self, comando: ComandoRealizarTransferencia) -> str:
        """Processa transferência entre contas"""
        # TODO: Implementar lógica completa de transferência
        # 1. Validar contas origem e destino
        # 2. Verificar saldo suficiente
        # 3. Análise antifraude
        # 4. Executar débito e crédito
        # 5. Registrar transação
        # 6. Publicar eventos
        pass

# =============================================================================
# INFRASTRUCTURE LAYER - Adapters para mundo externo
# =============================================================================

# Adaptadores de Persistência
class RepositorioContaMemoria:
    """Adapter: Repositório em memória para testes"""
    
    def __init__(self):
        self._contas: dict[str, Conta] = {}
    
    def salvar(self, conta: Conta) -> None:
        self._contas[conta.numero] = conta
    
    def buscar_por_numero(self, numero: str) -> Optional[Conta]:
        return self._contas.get(numero)
    
    def buscar_por_cpf(self, cpf: CPF) -> List[Conta]:
        return [conta for conta in self._contas.values() 
                if conta.cpf_titular == cpf]

# TODO: Implementar adaptadores SQL
class RepositorioContaSQL:
    """Adapter: Repositório SQL com SQLAlchemy"""
    
    def __init__(self, session):
        self._session = session
    
    def salvar(self, conta: Conta) -> None:
        # TODO: Mapear domínio para SQL
        pass
    
    def buscar_por_numero(self, numero: str) -> Optional[Conta]:
        # TODO: Buscar no banco e reconstruir agregado
        pass

# Adaptadores de Notificação
class AdaptadorNotificacaoEmail:
    """Adapter: Notificações por email"""
    
    def enviar_notificacao(self, destinatario: str, mensagem: str, canal: str) -> bool:
        if canal != "email":
            return False
        
        print(f"📧 Email para {destinatario}: {mensagem}")
        # TODO: Integração real com provedor de email
        return True

class AdaptadorNotificacaoSMS:
    """Adapter: Notificações por SMS"""
    
    def enviar_notificacao(self, destinatario: str, mensagem: str, canal: str) -> bool:
        if canal != "sms":
            return False
        
        print(f"📱 SMS para {destinatario}: {mensagem}")
        # TODO: Integração real com provedor de SMS
        return True

# Composite para múltiplos canais
class AdaptadorNotificacaoMulticanal:
    """Adapter: Composite para múltiplos canais"""
    
    def __init__(self):
        self._adaptadores = []
    
    def adicionar_adaptador(self, adaptador: ServicoNotificacao) -> None:
        self._adaptadores.append(adaptador)
    
    def enviar_notificacao(self, destinatario: str, mensagem: str, canal: str) -> bool:
        sucesso = False
        for adaptador in self._adaptadores:
            if adaptador.enviar_notificacao(destinatario, mensagem, canal):
                sucesso = True
        return sucesso

# Unit of Work
class UnidadeTrabalhoMemoria:
    """Unit of Work para repositórios em memória"""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
    
    def commit(self) -> None:
        # Para memória, commit é no-op
        pass
    
    def rollback(self) -> None:
        # Para memória, rollback seria complexo
        pass

# =============================================================================
# CONFIGURAÇÃO E COMPOSIÇÃO (Dependency Injection)
# =============================================================================

class ContainerDependencias:
    """Container de injeção de dependências"""
    
    def __init__(self):
        self._servicos = {}
    
    def registrar(self, interface, implementacao):
        self._servicos[interface] = implementacao
    
    def resolver(self, interface):
        return self._servicos.get(interface)
    
    def configurar_para_desenvolvimento(self):
        """Configuração para ambiente de desenvolvimento"""
        # Repositórios em memória
        self.registrar(RepositorioConta, RepositorioContaMemoria())
        self.registrar(RepositorioTransacao, None)  # TODO
        
        # Serviços
        self.registrar(ServicoNotificacao, AdaptadorNotificacaoEmail())
        self.registrar(UnidadeTrabalho, UnidadeTrabalhoMemoria())
        
        # Handlers
        self.registrar(ManipuladorComandoCriarConta, 
                      ManipuladorComandoCriarConta(
                          self.resolver(RepositorioConta),
                          self.resolver(ServicoNotificacao),
                          self.resolver(UnidadeTrabalho)
                      ))

# =============================================================================
# INTERFACE DE USUÁRIO (Adapter para API/CLI)
# =============================================================================

class FachadeSistemaBancario:
    """Facade para simplificar uso do sistema"""
    
    def __init__(self, container: ContainerDependencias):
        self._container = container
    
    def criar_conta(self, cpf: str, tipo: str, saldo_inicial: float = 0.0) -> str:
        """API simplificada para criação de conta"""
        handler = self._container.resolver(ManipuladorComandoCriarConta)
        comando = ComandoCriarConta(
            cpf=cpf,
            tipo=TipoConta(tipo),
            saldo_inicial=Decimal(str(saldo_inicial))
        )
        return handler.handle(comando)
    
    def realizar_transferencia(self, origem: str, destino: str, valor: float) -> str:
        """API simplificada para transferência"""
        # TODO: Implementar usando handler de transferência
        pass
    
    def consultar_saldo(self, numero_conta: str) -> dict:
        """Consulta saldo da conta"""
        repo = self._container.resolver(RepositorioConta)
        conta = repo.buscar_por_numero(numero_conta)
        
        if not conta:
            raise ValueError("Conta não encontrada")
        
        return {
            "numero": conta.numero,
            "saldo": float(conta.saldo.valor),
            "moeda": conta.saldo.moeda,
            "tipo": conta.tipo.value,
            "ativa": conta.ativa
        }
```

### 🧪 Cenários de Teste Avançados

```python
# TODO: Implementar suíte completa de testes
import pytest
from decimal import Decimal

class TestSistemaBancarioCompleto:
    """Testes de integração do sistema completo"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.container = ContainerDependencias()
        self.container.configurar_para_desenvolvimento()
        self.facade = FachadeSistemaBancario(self.container)
    
    def test_fluxo_completo_criacao_conta_e_transferencia(self):
        """Teste do fluxo principal do sistema"""
        # Criar contas
        conta1 = self.facade.criar_conta("12345678901", "corrente", 1000.0)
        conta2 = self.facade.criar_conta("10987654321", "poupanca", 0.0)
        
        # Consultar saldos iniciais
        saldo1 = self.facade.consultar_saldo(conta1)
        saldo2 = self.facade.consultar_saldo(conta2)
        
        assert saldo1["saldo"] == 1000.0
        assert saldo2["saldo"] == 0.0
        
        # Realizar transferência
        # TODO: Implementar quando handler estiver pronto
        
    def test_especificacoes_negocio_complexas(self):
        """Testa Specification Pattern com regras complexas"""
        # TODO: Implementar testes de especificações
        pass
    
    def test_eventos_dominio_publicados(self):
        """Testa se eventos são publicados corretamente"""
        # TODO: Implementar verificação de eventos
        pass
    
    def test_transacao_com_rollback(self):
        """Testa rollback em caso de falha"""
        # TODO: Simular falha e verificar rollback
        pass
```

### 📝 Exemplo de Uso do Sistema

```python
def exemplo_uso_sistema():
    """Demonstração do sistema bancário completo"""
    
    # Configurar container de dependências
    container = ContainerDependencias()
    container.configurar_para_desenvolvimento()
    
    # Inicializar facade
    sistema = FachadeSistemaBancario(container)
    
    try:
        # Criar contas
        print("🏦 Criando contas...")
        conta_joao = sistema.criar_conta("12345678901", "corrente", 5000.0)
        conta_maria = sistema.criar_conta("10987654321", "poupanca", 1000.0)
        
        print(f"✅ Conta do João: {conta_joao}")
        print(f"✅ Conta da Maria: {conta_maria}")
        
        # Consultar saldos
        print("\n💰 Consultando saldos...")
        saldo_joao = sistema.consultar_saldo(conta_joao)
        saldo_maria = sistema.consultar_saldo(conta_maria)
        
        print(f"João: R$ {saldo_joao['saldo']}")
        print(f"Maria: R$ {saldo_maria['saldo']}")
        
        # Realizar transferência
        print("\n💸 Realizando transferência...")
        # sistema.realizar_transferencia(conta_joao, conta_maria, 500.0)
        
        print("✅ Sistema bancário funcionando!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    exemplo_uso_sistema()
```

---

## Exercício 3.2: Sistema de Monitoramento Distribuído (2-3 horas)

### 📋 Descrição
Implemente um sistema de monitoramento distribuído aplicando **Event Sourcing**, **CQRS**, **Publish-Subscribe Pattern** e **Microservices Communication Patterns**.

### 🎯 Cenário
Sistema que monitora múltiplos serviços em tempo real:
- Coleta métricas de CPU, memória, rede
- Detecta anomalias usando machine learning
- Envia alertas automáticos
- Mantém histórico completo para análise
- Dashboard em tempo real

### 📋 Requisitos Técnicos Avançados

#### **Event Sourcing:**
- Todos os eventos são persistidos
- Estado reconstruído a partir de eventos
- Snapshots para performance
- Replay de eventos para debugging

#### **CQRS Completo:**
- Commands para escrita
- Queries para leitura
- Projeções específicas por use case
- Event handlers assíncronos

#### **Patterns de Comunicação:**
- Message Queue para eventos
- Circuit Breaker para resiliência
- Retry Pattern com backoff
- Saga Pattern para transações distribuídas

### 💻 Estrutura Avançada

```python
# TODO: Implementar sistema completo
# Base fornecida - expandir conforme necessário

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import uuid

class TipoEvento(Enum):
    METRICA_COLETADA = "metrica_coletada"
    ANOMALIA_DETECTADA = "anomalia_detectada"
    ALERTA_ENVIADO = "alerta_enviado"
    SERVICO_INDISPONIVEL = "servico_indisponivel"

@dataclass
class EventoSistema:
    """Event Sourcing - Evento base"""
    id: str
    tipo: TipoEvento
    agregado_id: str
    dados: Dict[str, Any]
    timestamp: datetime
    versao: int
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EventoSistema':
        return cls(**data)

# TODO: Implementar Event Store
class EventStore(ABC):
    """Interface para persistência de eventos"""
    
    @abstractmethod
    async def salvar_evento(self, evento: EventoSistema) -> None:
        pass
    
    @abstractmethod
    async def obter_eventos(self, agregado_id: str, 
                           desde_versao: int = 0) -> AsyncIterator[EventoSistema]:
        pass
    
    @abstractmethod
    async def obter_eventos_por_tipo(self, tipo: TipoEvento,
                                   desde: datetime) -> AsyncIterator[EventoSistema]:
        pass

# TODO: Implementar Message Bus
class MessageBus(ABC):
    """Interface para comunicação assíncrona"""
    
    @abstractmethod
    async def publicar(self, evento: EventoSistema) -> None:
        pass
    
    @abstractmethod
    async def subscrever(self, tipo: TipoEvento, handler) -> None:
        pass

# TODO: Implementar Agregados com Event Sourcing
class ServicoMonitorado:
    """Agregado que reconstrói estado a partir de eventos"""
    
    def __init__(self, id: str):
        self.id = id
        self.nome: Optional[str] = None
        self.ativo: bool = True
        self.ultima_metrica: Optional[datetime] = None
        self.alertas_ativos: List[str] = []
        self._versao = 0
        self._eventos_nao_salvos: List[EventoSistema] = []
    
    @classmethod
    async def reconstruir_de_eventos(cls, id: str, 
                                   event_store: EventStore) -> 'ServicoMonitorado':
        """Reconstrói agregado a partir do Event Store"""
        servico = cls(id)
        
        async for evento in event_store.obter_eventos(id):
            servico._aplicar_evento(evento)
        
        return servico
    
    def _aplicar_evento(self, evento: EventoSistema) -> None:
        """Aplica evento ao estado interno"""
        self._versao = evento.versao
        
        if evento.tipo == TipoEvento.METRICA_COLETADA:
            self.ultima_metrica = evento.timestamp
            # TODO: Processar métricas
        
        elif evento.tipo == TipoEvento.ANOMALIA_DETECTADA:
            # TODO: Processar anomalia
            pass
    
    def coletar_metrica(self, cpu: float, memoria: float, rede: float) -> None:
        """Command: Coletar nova métrica"""
        evento = EventoSistema(
            id=str(uuid.uuid4()),
            tipo=TipoEvento.METRICA_COLETADA,
            agregado_id=self.id,
            dados={"cpu": cpu, "memoria": memoria, "rede": rede},
            timestamp=datetime.now(),
            versao=self._versao + 1
        )
        
        self._aplicar_evento(evento)
        self._eventos_nao_salvos.append(evento)

# TODO: Implementar handlers CQRS
class HandlerComandoColetarMetrica:
    """Command Handler para coleta de métricas"""
    
    def __init__(self, event_store: EventStore, message_bus: MessageBus):
        self._event_store = event_store
        self._message_bus = message_bus
    
    async def handle(self, comando) -> None:
        """Processa comando de coleta"""
        # TODO: Implementar lógica completa
        pass

# TODO: Implementar projeções para queries
class ProjecaoMetricasTempoReal:
    """Projeção otimizada para dashboard em tempo real"""
    
    def __init__(self):
        self._metricas_atuais: Dict[str, Dict] = {}
    
    async def processar_evento(self, evento: EventoSistema) -> None:
        """Atualiza projeção baseada em evento"""
        if evento.tipo == TipoEvento.METRICA_COLETADA:
            self._metricas_atuais[evento.agregado_id] = evento.dados

class ProjecaoHistoricoCompleto:
    """Projeção para análise histórica"""
    # TODO: Implementar
    pass

# TODO: Implementar Circuit Breaker
class CircuitBreaker:
    """Pattern para resiliência em chamadas externas"""
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Executa função com circuit breaker"""
        # TODO: Implementar lógica completa
        pass
```

### 🧪 Casos de Teste para Sistema Distribuído

```python
class TestSistemaMonitoramento:
    
    @pytest.mark.asyncio
    async def test_event_sourcing_reconstroi_estado(self):
        """Testa reconstrução de agregado via eventos"""
        # TODO: Implementar
        pass
    
    @pytest.mark.asyncio
    async def test_cqrs_separacao_comando_query(self):
        """Testa separação entre comandos e queries"""
        # TODO: Implementar
        pass
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_resiliencia(self):
        """Testa circuit breaker em falhas"""
        # TODO: Implementar
        pass
```

---

## 📊 Resumo do Nível 3

Ao completar estes exercícios avançados, você terá dominado:

✅ **Arquitetura Hexagonal completa**
✅ **Domain-Driven Design (DDD)**
✅ **Event Sourcing & CQRS**
✅ **Microservices Patterns**
✅ **Specification Pattern**
✅ **Unit of Work & Repository**
✅ **Command Pattern avançado**
✅ **Circuit Breaker & Resilience**

### 🎯 Competências Desenvolvidas

- **Arquitetura Empresarial**: Design de sistemas complexos
- **Patterns Avançados**: Aplicação de patterns em cenários reais
- **Resiliência**: Sistemas tolerantes a falhas
- **Performance**: Otimização e escalabilidade
- **Manutenibilidade**: Código limpo e testável

---

**⏱️ Tempo estimado total: 5-7 horas**
**🎖️ Nível de dificuldade: Avançado**
**🎓 Nível: Arquiteto de Software**
**📚 Conceitos: Arquitetura empresarial, DDD, Event Sourcing, Microservices**
