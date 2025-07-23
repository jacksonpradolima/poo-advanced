#!/usr/bin/env python3
"""
EXERCÍCIO 3.1: SISTEMA BANCÁRIO - ARQUITETURA HEXAGONAL

CONTEXTO: Desenvolver um sistema bancário completo utilizando Arquitetura 
Hexagonal (Ports & Adapters), demonstrando todos os princípios SOLID e 
múltiplos design patterns em um cenário complexo e realista.

OBJETIVOS:
1. Implementar Arquitetura Hexagonal completa
2. Demonstrar Domain-Driven Design (DDD)
3. Aplicar todos os princípios SOLID rigorosamente
4. Implementar múltiplos design patterns
5. Criar sistema extensível e testável
6. Simular operações bancárias reais
7. Gerenciar transações e auditoria

ARQUITETURA:
📦 Domain (Core)
├── 🔵 Entities (Conta, Cliente, Transacao)
├── 🔵 Value Objects (CPF, Dinheiro, etc.)
├── 🔵 Domain Services (RegrasNegocio)
└── 🔵 Domain Events (EventoTransacao)

📦 Application (Ports)
├── 🔌 Use Cases (AbrirConta, Transferir)
├── 🔌 Input Ports (Interfaces de entrada)
└── 🔌 Output Ports (Interfaces de saída)

📦 Infrastructure (Adapters)
├── 🔧 Database Adapters
├── 🔧 External Service Adapters
├── 🔧 Notification Adapters
└── 🔧 Web/API Adapters

PADRÕES DEMONSTRADOS:
- Hexagonal Architecture
- Domain-Driven Design
- Repository Pattern
- Factory Method Pattern
- Strategy Pattern
- Observer Pattern
- Command Pattern
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)
- Unit of Work Pattern
- Specification Pattern

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum, auto
from typing import Dict, List, Optional, Protocol, Any, Callable, Union
from uuid import UUID, uuid4
import json
import re
import hashlib
import threading
from collections import defaultdict
import time


# =============================================================================
# DOMAIN LAYER - VALUE OBJECTS
# =============================================================================

@dataclass(frozen=True)
class CPF:
    """
    Value Object para CPF com validação
    
    RESPONSABILIDADES:
    - Validar formato e dígitos verificadores
    - Garantir imutabilidade
    - Fornecer representações padronizadas
    """
    numero: str
    
    def __post_init__(self):
        """Validação após inicialização"""
        if not self._validar_cpf(self.numero):
            raise ValueError(f"CPF inválido: {self.numero}")
    
    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida CPF segundo algoritmo oficial"""
        # Remover caracteres não numéricos
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)
        
        # Verificar se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        soma1 = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        digito1 = 11 - (soma1 % 11)
        if digito1 >= 10:
            digito1 = 0
        
        # Calcular segundo dígito verificador
        soma2 = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        digito2 = 11 - (soma2 % 11)
        if digito2 >= 10:
            digito2 = 0
        
        # Verificar dígitos
        return cpf_limpo[9:11] == f"{digito1}{digito2}"
    
    @property
    def formatado(self) -> str:
        """CPF formatado com pontos e traço"""
        limpo = re.sub(r'[^0-9]', '', self.numero)
        return f"{limpo[:3]}.{limpo[3:6]}.{limpo[6:9]}-{limpo[9:11]}"
    
    @property
    def limpo(self) -> str:
        """CPF apenas com números"""
        return re.sub(r'[^0-9]', '', self.numero)


@dataclass(frozen=True)
class Dinheiro:
    """
    Value Object para representação monetária
    
    RESPONSABILIDADES:
    - Garantir precisão decimal
    - Implementar operações monetárias
    - Validar valores
    - Formatar para exibição
    """
    valor: Decimal
    moeda: str = "BRL"
    
    def __post_init__(self):
        """Validação e normalização"""
        if self.valor < 0:
            raise ValueError("Valor monetário não pode ser negativo")
        
        # Arredondar para 2 casas decimais
        object.__setattr__(self, 'valor', 
                          self.valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def __add__(self, other: 'Dinheiro') -> 'Dinheiro':
        """Soma de valores monetários"""
        if self.moeda != other.moeda:
            raise ValueError("Não é possível somar moedas diferentes")
        return Dinheiro(self.valor + other.valor, self.moeda)
    
    def __sub__(self, other: 'Dinheiro') -> 'Dinheiro':
        """Subtração de valores monetários"""
        if self.moeda != other.moeda:
            raise ValueError("Não é possível subtrair moedas diferentes")
        resultado = self.valor - other.valor
        if resultado < 0:
            raise ValueError("Resultado da subtração não pode ser negativo")
        return Dinheiro(resultado, self.moeda)
    
    def __mul__(self, fator: Union[int, float, Decimal]) -> 'Dinheiro':
        """Multiplicação por escalar"""
        return Dinheiro(self.valor * Decimal(str(fator)), self.moeda)
    
    def __eq__(self, other: object) -> bool:
        """Igualdade entre valores monetários"""
        if not isinstance(other, Dinheiro):
            return False
        return self.valor == other.valor and self.moeda == other.moeda
    
    def __lt__(self, other: 'Dinheiro') -> bool:
        """Comparação menor que"""
        if self.moeda != other.moeda:
            raise ValueError("Não é possível comparar moedas diferentes")
        return self.valor < other.valor
    
    def __le__(self, other: 'Dinheiro') -> bool:
        """Comparação menor ou igual"""
        return self < other or self == other
    
    def __gt__(self, other: 'Dinheiro') -> bool:
        """Comparação maior que"""
        return not self <= other
    
    def __ge__(self, other: 'Dinheiro') -> bool:
        """Comparação maior ou igual"""
        return not self < other
    
    @property
    def formatado(self) -> str:
        """Formatação monetária brasileira"""
        if self.moeda == "BRL":
            return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"{self.valor:.2f} {self.moeda}"
    
    @classmethod
    def zero(cls, moeda: str = "BRL") -> 'Dinheiro':
        """Factory method para valor zero"""
        return cls(Decimal('0.00'), moeda)
    
    def is_zero(self) -> bool:
        """Verifica se o valor é zero"""
        return self.valor == Decimal('0.00')


@dataclass(frozen=True)
class Endereco:
    """
    Value Object para endereço
    
    RESPONSABILIDADES:
    - Validar dados de endereço
    - Normalizar informações
    - Fornecer representação completa
    """
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    uf: str
    
    def __post_init__(self):
        """Validação de dados"""
        if not re.match(r'^\d{5}-?\d{3}$', self.cep):
            raise ValueError("CEP deve ter formato 12345-678 ou 12345678")
        
        if len(self.uf) != 2:
            raise ValueError("UF deve ter 2 caracteres")
        
        if not self.logradouro.strip():
            raise ValueError("Logradouro é obrigatório")
    
    @property
    def cep_formatado(self) -> str:
        """CEP formatado"""
        cep_limpo = re.sub(r'[^0-9]', '', self.cep)
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    
    @property
    def completo(self) -> str:
        """Endereço completo formatado"""
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f", {self.bairro}, {self.cidade}/{self.uf}, CEP: {self.cep_formatado}"
        return endereco


# =============================================================================
# DOMAIN LAYER - ENUMERAÇÕES
# =============================================================================

class TipoConta(Enum):
    """Tipos de conta bancária"""
    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"
    INVESTIMENTO = "INVESTIMENTO"
    EMPRESARIAL = "EMPRESARIAL"


class StatusConta(Enum):
    """Status da conta bancária"""
    ATIVA = "ATIVA"
    BLOQUEADA = "BLOQUEADA"
    ENCERRADA = "ENCERRADA"
    PENDENTE_APROVACAO = "PENDENTE_APROVACAO"


class TipoTransacao(Enum):
    """Tipos de transação"""
    DEPOSITO = "DEPOSITO"
    SAQUE = "SAQUE"
    TRANSFERENCIA_SAIDA = "TRANSFERENCIA_SAIDA"
    TRANSFERENCIA_ENTRADA = "TRANSFERENCIA_ENTRADA"
    PAGAMENTO = "PAGAMENTO"
    ESTORNO = "ESTORNO"
    RENDIMENTO = "RENDIMENTO"
    TARIFA = "TARIFA"


class StatusTransacao(Enum):
    """Status da transação"""
    PENDENTE = "PENDENTE"
    PROCESSANDO = "PROCESSANDO"
    CONCLUIDA = "CONCLUIDA"
    FALHOU = "FALHOU"
    CANCELADA = "CANCELADA"
    ESTORNADA = "ESTORNADA"


# =============================================================================
# DOMAIN LAYER - DOMAIN EVENTS
# =============================================================================

# DOMAIN LAYER - DOMAIN EVENTS
# =============================================================================

class EventoDominio:
    """Classe base para eventos de domínio"""
    
    def __init__(self):
        self.id: UUID = uuid4()
        self.timestamp: datetime = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialização do evento"""
        return {
            'id': str(self.id),
            'timestamp': self.timestamp.isoformat(),
            'tipo': self.__class__.__name__,
            **{k: v for k, v in self.__dict__.items() 
               if k not in ['id', 'timestamp']}
        }


@dataclass(frozen=True)
class EventoContaCriada:
    """Evento disparado quando conta é criada"""
    conta_id: UUID
    cliente_id: UUID
    tipo_conta: TipoConta
    agencia: str
    numero: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialização do evento"""
        return {
            'id': str(self.id),
            'timestamp': self.timestamp.isoformat(),
            'tipo': self.__class__.__name__,
            'conta_id': str(self.conta_id),
            'cliente_id': str(self.cliente_id),
            'tipo_conta': self.tipo_conta.value,
            'agencia': self.agencia,
            'numero': self.numero
        }


@dataclass(frozen=True)
class EventoTransacaoRealizada:
    """Evento disparado quando transação é realizada"""
    transacao_id: UUID
    conta_origem_id: Optional[UUID]
    conta_destino_id: Optional[UUID]
    tipo: TipoTransacao
    valor: Dinheiro
    descricao: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class EventoSaldoInsuficiente:
    """Evento disparado quando há tentativa com saldo insuficiente"""
    conta_id: UUID
    valor_tentativa: Dinheiro
    saldo_atual: Dinheiro
    operacao: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class EventoLimiteExcedido:
    """Evento disparado quando limite é excedido"""
    conta_id: UUID
    limite_atual: Dinheiro
    valor_tentativa: Dinheiro
    tipo_limite: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)


# =============================================================================
# DOMAIN LAYER - ENTITIES
# =============================================================================

class EntidadeBase:
    """
    Classe base para entidades do domínio
    
    RESPONSABILIDADES:
    - Gerenciar identidade única
    - Controlar eventos de domínio
    - Fornecer estrutura comum
    """
    
    def __init__(self, id: Optional[UUID] = None):
        self._id = id or uuid4()
        self._eventos: List[EventoDominio] = []
    
    @property
    def id(self) -> UUID:
        """Identificador único da entidade"""
        return self._id
    
    def adicionar_evento(self, evento: EventoDominio) -> None:
        """Adiciona evento de domínio"""
        self._eventos.append(evento)
    
    def obter_eventos(self) -> List[EventoDominio]:
        """Obtém eventos de domínio"""
        return self._eventos.copy()
    
    def limpar_eventos(self) -> None:
        """Limpa eventos após processamento"""
        self._eventos.clear()
    
    def __eq__(self, other: object) -> bool:
        """Igualdade baseada no ID"""
        if not isinstance(other, EntidadeBase):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash baseado no ID"""
        return hash(self._id)


class Cliente(EntidadeBase):
    """
    Entidade Cliente do sistema bancário
    
    RESPONSABILIDADES:
    - Gerenciar dados pessoais
    - Manter histórico de relacionamento
    - Validar elegibilidade para produtos
    - Controlar perfil de risco
    """
    
    def __init__(self, 
                 nome: str,
                 cpf: CPF,
                 endereco: Endereco,
                 telefone: str,
                 email: str,
                 data_nascimento: datetime,
                 id: Optional[UUID] = None):
        super().__init__(id)
        
        self._nome = self._validar_nome(nome)
        self._cpf = cpf
        self._endereco = endereco
        self._telefone = self._validar_telefone(telefone)
        self._email = self._validar_email(email)
        self._data_nascimento = data_nascimento
        self._data_cadastro = datetime.now()
        self._ativo = True
        self._perfil_risco = "BAIXO"
        self._pontuacao_credito = 0
        
        # Validar idade mínima
        if self._calcular_idade() < 18:
            raise ValueError("Cliente deve ter pelo menos 18 anos")
    
    def _validar_nome(self, nome: str) -> str:
        """Valida e normaliza nome"""
        nome = nome.strip()
        if len(nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
            raise ValueError("Nome deve conter apenas letras e espaços")
        return nome.title()
    
    def _validar_telefone(self, telefone: str) -> str:
        """Valida formato do telefone"""
        telefone_limpo = re.sub(r'[^0-9]', '', telefone)
        if len(telefone_limpo) not in [10, 11]:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        return telefone_limpo
    
    def _validar_email(self, email: str) -> str:
        """Valida formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao, email):
            raise ValueError("Email inválido")
        return email.lower()
    
    def _calcular_idade(self) -> int:
        """Calcula idade atual"""
        hoje = datetime.now().date()
        nascimento = self._data_nascimento.date()
        idade = hoje.year - nascimento.year
        if hoje < nascimento.replace(year=hoje.year):
            idade -= 1
        return idade
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def cpf(self) -> CPF:
        return self._cpf
    
    @property
    def endereco(self) -> Endereco:
        return self._endereco
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def data_nascimento(self) -> datetime:
        return self._data_nascimento
    
    @property
    def idade(self) -> int:
        return self._calcular_idade()
    
    @property
    def ativo(self) -> bool:
        return self._ativo
    
    @property
    def perfil_risco(self) -> str:
        return self._perfil_risco
    
    def atualizar_endereco(self, novo_endereco: Endereco) -> None:
        """Atualiza endereço do cliente"""
        self._endereco = novo_endereco
    
    def atualizar_telefone(self, novo_telefone: str) -> None:
        """Atualiza telefone do cliente"""
        self._telefone = self._validar_telefone(novo_telefone)
    
    def atualizar_email(self, novo_email: str) -> None:
        """Atualiza email do cliente"""
        self._email = self._validar_email(novo_email)
    
    def inativar(self) -> None:
        """Inativa cliente"""
        self._ativo = False
    
    def reativar(self) -> None:
        """Reativa cliente"""
        self._ativo = True
    
    def atualizar_perfil_risco(self, novo_perfil: str) -> None:
        """Atualiza perfil de risco"""
        perfis_validos = ["BAIXO", "MEDIO", "ALTO"]
        if novo_perfil not in perfis_validos:
            raise ValueError(f"Perfil deve ser um de: {perfis_validos}")
        self._perfil_risco = novo_perfil


class Conta(EntidadeBase):
    """
    Entidade Conta Bancária
    
    RESPONSABILIDADES:
    - Gerenciar saldo e operações
    - Controlar limites e regras
    - Manter histórico de transações
    - Validar operações bancárias
    """
    
    def __init__(self,
                 cliente_id: UUID,
                 agencia: str,
                 numero: str,
                 tipo: TipoConta,
                 saldo_inicial: Dinheiro = None,
                 id: Optional[UUID] = None):
        super().__init__(id)
        
        self._cliente_id = cliente_id
        self._agencia = self._validar_agencia(agencia)
        self._numero = self._validar_numero(numero)
        self._tipo = tipo
        self._saldo = saldo_inicial or Dinheiro.zero()
        self._status = StatusConta.ATIVA
        self._data_abertura = datetime.now()
        self._limite_diario = self._definir_limite_inicial()
        self._limite_usado_hoje = Dinheiro.zero()
        self._data_ultimo_uso = datetime.now().date()
        self._transacoes: List[UUID] = []
        
        # Disparar evento de criação
        self.adicionar_evento(EventoContaCriada(
            conta_id=self.id,
            cliente_id=cliente_id,
            tipo_conta=tipo,
            agencia=agencia,
            numero=numero
        ))
    
    def _validar_agencia(self, agencia: str) -> str:
        """Valida código da agência"""
        if not re.match(r'^\d{4}$', agencia):
            raise ValueError("Agência deve ter 4 dígitos")
        return agencia
    
    def _validar_numero(self, numero: str) -> str:
        """Valida número da conta"""
        # Remove caracteres não numéricos
        numero_limpo = re.sub(r'[^0-9]', '', numero)
        if len(numero_limpo) < 6:
            raise ValueError("Número da conta deve ter pelo menos 6 dígitos")
        return numero_limpo
    
    def _definir_limite_inicial(self) -> Dinheiro:
        """Define limite diário inicial baseado no tipo da conta"""
        limites = {
            TipoConta.CORRENTE: Dinheiro(Decimal('5000.00')),
            TipoConta.POUPANCA: Dinheiro(Decimal('2000.00')),
            TipoConta.INVESTIMENTO: Dinheiro(Decimal('10000.00')),
            TipoConta.EMPRESARIAL: Dinheiro(Decimal('50000.00'))
        }
        return limites.get(self._tipo, Dinheiro(Decimal('1000.00')))
    
    def _resetar_limite_diario_se_necessario(self) -> None:
        """Reseta limite diário se mudou o dia"""
        hoje = datetime.now().date()
        if self._data_ultimo_uso < hoje:
            self._limite_usado_hoje = Dinheiro.zero()
            self._data_ultimo_uso = hoje
    
    @property
    def cliente_id(self) -> UUID:
        return self._cliente_id
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def numero(self) -> str:
        return self._numero
    
    @property
    def numero_formatado(self) -> str:
        """Número da conta formatado"""
        return f"{self._numero[:-1]}-{self._numero[-1]}"
    
    @property
    def tipo(self) -> TipoConta:
        return self._tipo
    
    @property
    def saldo(self) -> Dinheiro:
        return self._saldo
    
    @property
    def status(self) -> StatusConta:
        return self._status
    
    @property
    def data_abertura(self) -> datetime:
        return self._data_abertura
    
    @property
    def limite_diario_disponivel(self) -> Dinheiro:
        """Limite diário disponível"""
        self._resetar_limite_diario_se_necessario()
        return self._limite_diario - self._limite_usado_hoje
    
    def pode_realizar_operacao(self, valor: Dinheiro, operacao: str) -> bool:
        """Verifica se pode realizar operação"""
        if self._status != StatusConta.ATIVA:
            return False
        
        if operacao in ['SAQUE', 'TRANSFERENCIA_SAIDA', 'PAGAMENTO']:
            # Verificar saldo
            if self._saldo < valor:
                self.adicionar_evento(EventoSaldoInsuficiente(
                    conta_id=self.id,
                    valor_tentativa=valor,
                    saldo_atual=self._saldo,
                    operacao=operacao
                ))
                return False
            
            # Verificar limite diário
            self._resetar_limite_diario_se_necessario()
            if self._limite_usado_hoje + valor > self._limite_diario:
                self.adicionar_evento(EventoLimiteExcedido(
                    conta_id=self.id,
                    limite_atual=self.limite_diario_disponivel,
                    valor_tentativa=valor,
                    tipo_limite="DIARIO"
                ))
                return False
        
        return True
    
    def debitar(self, valor: Dinheiro, operacao: str = "DEBITO") -> None:
        """Debita valor da conta"""
        if not self.pode_realizar_operacao(valor, operacao):
            raise ValueError(f"Não é possível realizar operação: {operacao}")
        
        self._saldo = self._saldo - valor
        
        if operacao in ['SAQUE', 'TRANSFERENCIA_SAIDA', 'PAGAMENTO']:
            self._resetar_limite_diario_se_necessario()
            self._limite_usado_hoje = self._limite_usado_hoje + valor
    
    def creditar(self, valor: Dinheiro) -> None:
        """Credita valor na conta"""
        if self._status != StatusConta.ATIVA:
            raise ValueError("Conta não está ativa")
        
        self._saldo = self._saldo + valor
    
    def bloquear(self, motivo: str = "") -> None:
        """Bloqueia a conta"""
        self._status = StatusConta.BLOQUEADA
    
    def desbloquear(self) -> None:
        """Desbloqueia a conta"""
        self._status = StatusConta.ATIVA
    
    def encerrar(self) -> None:
        """Encerra a conta"""
        if not self._saldo.is_zero():
            raise ValueError("Não é possível encerrar conta com saldo")
        self._status = StatusConta.ENCERRADA
    
    def adicionar_transacao(self, transacao_id: UUID) -> None:
        """Adiciona transação ao histórico"""
        self._transacoes.append(transacao_id)
    
    def atualizar_limite_diario(self, novo_limite: Dinheiro) -> None:
        """Atualiza limite diário"""
        if novo_limite.valor <= 0:
            raise ValueError("Limite deve ser positivo")
        self._limite_diario = novo_limite


class Transacao(EntidadeBase):
    """
    Entidade Transação Bancária
    
    RESPONSABILIDADES:
    - Registrar operações financeiras
    - Controlar status e auditoria
    - Manter rastreabilidade
    - Validar integridade
    """
    
    def __init__(self,
                 tipo: TipoTransacao,
                 valor: Dinheiro,
                 descricao: str,
                 conta_origem_id: Optional[UUID] = None,
                 conta_destino_id: Optional[UUID] = None,
                 id: Optional[UUID] = None):
        super().__init__(id)
        
        self._tipo = tipo
        self._valor = valor
        self._descricao = descricao
        self._conta_origem_id = conta_origem_id
        self._conta_destino_id = conta_destino_id
        self._status = StatusTransacao.PENDENTE
        self._data_criacao = datetime.now()
        self._data_processamento: Optional[datetime] = None
        self._hash_integridade = self._calcular_hash()
        self._observacoes: List[str] = []
        
        # Validar dados da transação
        self._validar_transacao()
    
    def _validar_transacao(self) -> None:
        """Valida dados da transação"""
        if self._valor.valor <= 0:
            raise ValueError("Valor da transação deve ser positivo")
        
        # Validar contas conforme tipo de transação
        if self._tipo in [TipoTransacao.SAQUE, TipoTransacao.PAGAMENTO, TipoTransacao.TARIFA]:
            if not self._conta_origem_id:
                raise ValueError(f"Conta origem obrigatória para {self._tipo.value}")
        
        elif self._tipo == TipoTransacao.DEPOSITO:
            if not self._conta_destino_id:
                raise ValueError("Conta destino obrigatória para depósito")
        
        elif self._tipo in [TipoTransacao.TRANSFERENCIA_SAIDA, TipoTransacao.TRANSFERENCIA_ENTRADA]:
            if not (self._conta_origem_id and self._conta_destino_id):
                raise ValueError("Conta origem e destino obrigatórias para transferência")
    
    def _calcular_hash(self) -> str:
        """Calcula hash para integridade"""
        dados = f"{self.id}{self._tipo.value}{self._valor.valor}{self._data_criacao}"
        return hashlib.sha256(dados.encode()).hexdigest()
    
    @property
    def tipo(self) -> TipoTransacao:
        return self._tipo
    
    @property
    def valor(self) -> Dinheiro:
        return self._valor
    
    @property
    def descricao(self) -> str:
        return self._descricao
    
    @property
    def conta_origem_id(self) -> Optional[UUID]:
        return self._conta_origem_id
    
    @property
    def conta_destino_id(self) -> Optional[UUID]:
        return self._conta_destino_id
    
    @property
    def status(self) -> StatusTransacao:
        return self._status
    
    @property
    def data_criacao(self) -> datetime:
        return self._data_criacao
    
    @property
    def data_processamento(self) -> Optional[datetime]:
        return self._data_processamento
    
    @property
    def hash_integridade(self) -> str:
        return self._hash_integridade
    
    def processar(self) -> None:
        """Marca transação como processando"""
        if self._status != StatusTransacao.PENDENTE:
            raise ValueError("Só é possível processar transações pendentes")
        
        self._status = StatusTransacao.PROCESSANDO
        self._data_processamento = datetime.now()
    
    def concluir(self) -> None:
        """Marca transação como concluída"""
        if self._status != StatusTransacao.PROCESSANDO:
            raise ValueError("Só é possível concluir transações em processamento")
        
        self._status = StatusTransacao.CONCLUIDA
        
        # Disparar evento
        self.adicionar_evento(EventoTransacaoRealizada(
            transacao_id=self.id,
            conta_origem_id=self._conta_origem_id,
            conta_destino_id=self._conta_destino_id,
            tipo=self._tipo,
            valor=self._valor,
            descricao=self._descricao
        ))
    
    def falhar(self, motivo: str) -> None:
        """Marca transação como falhada"""
        self._status = StatusTransacao.FALHOU
        self._observacoes.append(f"FALHA: {motivo} - {datetime.now()}")
    
    def cancelar(self, motivo: str) -> None:
        """Cancela transação"""
        if self._status == StatusTransacao.CONCLUIDA:
            raise ValueError("Não é possível cancelar transação concluída")
        
        self._status = StatusTransacao.CANCELADA
        self._observacoes.append(f"CANCELAMENTO: {motivo} - {datetime.now()}")
    
    def estornar(self, motivo: str) -> None:
        """Estorna transação concluída"""
        if self._status != StatusTransacao.CONCLUIDA:
            raise ValueError("Só é possível estornar transações concluídas")
        
        self._status = StatusTransacao.ESTORNADA
        self._observacoes.append(f"ESTORNO: {motivo} - {datetime.now()}")
    
    def adicionar_observacao(self, observacao: str) -> None:
        """Adiciona observação à transação"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._observacoes.append(f"{timestamp}: {observacao}")
    
    def verificar_integridade(self) -> bool:
        """Verifica integridade da transação"""
        hash_atual = self._calcular_hash()
        return hash_atual == self._hash_integridade


# =============================================================================
# APPLICATION LAYER - PORTS (INTERFACES)
# =============================================================================

class IRepositorioCliente(Protocol):
    """Interface para repositório de clientes"""
    
    def salvar(self, cliente: Cliente) -> None:
        """Salva cliente"""
        ...
    
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """Busca cliente por ID"""
        ...
    
    def buscar_por_cpf(self, cpf: CPF) -> Optional[Cliente]:
        """Busca cliente por CPF"""
        ...
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        ...
    
    def listar_todos(self) -> List[Cliente]:
        """Lista todos os clientes"""
        ...


class IRepositorioConta(Protocol):
    """Interface para repositório de contas"""
    
    def salvar(self, conta: Conta) -> None:
        """Salva conta"""
        ...
    
    def buscar_por_id(self, id: UUID) -> Optional[Conta]:
        """Busca conta por ID"""
        ...
    
    def buscar_por_numero(self, agencia: str, numero: str) -> Optional[Conta]:
        """Busca conta por agência e número"""
        ...
    
    def listar_por_cliente(self, cliente_id: UUID) -> List[Conta]:
        """Lista contas do cliente"""
        ...


class IRepositorioTransacao(Protocol):
    """Interface para repositório de transações"""
    
    def salvar(self, transacao: Transacao) -> None:
        """Salva transação"""
        ...
    
    def buscar_por_id(self, id: UUID) -> Optional[Transacao]:
        """Busca transação por ID"""
        ...
    
    def listar_por_conta(self, conta_id: UUID, 
                        data_inicio: Optional[datetime] = None,
                        data_fim: Optional[datetime] = None) -> List[Transacao]:
        """Lista transações da conta"""
        ...


class IProcessadorEventos(Protocol):
    """Interface para processamento de eventos"""
    
    def processar(self, evento: EventoDominio) -> None:
        """Processa evento de domínio"""
        ...


class INotificadorTransacao(Protocol):
    """Interface para notificações de transação"""
    
    def notificar_transacao_realizada(self, transacao: Transacao, 
                                    conta_origem: Optional[Conta],
                                    conta_destino: Optional[Conta]) -> None:
        """Notifica transação realizada"""
        ...


class IValidadorFraude(Protocol):
    """Interface para validação de fraude"""
    
    def validar(self, transacao: Transacao, conta: Conta) -> bool:
        """Valida se transação pode ser suspeita de fraude"""
        ...


class IConsultorCreditoExterno(Protocol):
    """Interface para consulta de crédito externa"""
    
    def consultar_score(self, cpf: CPF) -> int:
        """Consulta score de crédito"""
        ...
    
    def consultar_restricoes(self, cpf: CPF) -> List[str]:
        """Consulta restrições"""
        ...


# =============================================================================
# APPLICATION LAYER - USE CASES
# =============================================================================

class CasoUsoBase:
    """Classe base para casos de uso"""
    
    def __init__(self):
        self._eventos_gerados: List[EventoDominio] = []
    
    def obter_eventos(self) -> List[EventoDominio]:
        """Obtém eventos gerados durante execução"""
        return self._eventos_gerados.copy()
    
    def limpar_eventos(self) -> None:
        """Limpa eventos após processamento"""
        self._eventos_gerados.clear()


@dataclass
class ComandoCriarCliente:
    """Comando para criar cliente"""
    nome: str
    cpf: str
    endereco_cep: str
    endereco_logradouro: str
    endereco_numero: str
    endereco_complemento: Optional[str]
    endereco_bairro: str
    endereco_cidade: str
    endereco_uf: str
    telefone: str
    email: str
    data_nascimento: datetime


@dataclass
class ResultadoCriarCliente:
    """Resultado da criação de cliente"""
    cliente_id: str
    sucesso: bool
    mensagem: str


class CriarClienteUseCase(CasoUsoBase):
    """
    Caso de uso para criar cliente
    
    RESPONSABILIDADES:
    - Validar dados do cliente
    - Verificar duplicatas
    - Consultar restrições externas
    - Criar e persistir cliente
    """
    
    def __init__(self,
                 repo_cliente: IRepositorioCliente,
                 consultor_credito: Optional[IConsultorCreditoExterno] = None):
        super().__init__()
        self._repo_cliente = repo_cliente
        self._consultor_credito = consultor_credito
    
    def executar(self, comando: ComandoCriarCliente) -> ResultadoCriarCliente:
        """Executa criação de cliente"""
        try:
            # 1. Criar value objects
            cpf = CPF(comando.cpf)
            endereco = Endereco(
                cep=comando.endereco_cep,
                logradouro=comando.endereco_logradouro,
                numero=comando.endereco_numero,
                complemento=comando.endereco_complemento,
                bairro=comando.endereco_bairro,
                cidade=comando.endereco_cidade,
                uf=comando.endereco_uf
            )
            
            # 2. Verificar se CPF já existe
            cliente_existente = self._repo_cliente.buscar_por_cpf(cpf)
            if cliente_existente:
                return ResultadoCriarCliente(
                    cliente_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="CPF já cadastrado no sistema"
                )
            
            # 3. Verificar se email já existe
            email_existente = self._repo_cliente.buscar_por_email(comando.email)
            if email_existente:
                return ResultadoCriarCliente(
                    cliente_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="Email já cadastrado no sistema"
                )
            
            # 4. Consultar restrições externas (se disponível)
            if self._consultor_credito:
                restricoes = self._consultor_credito.consultar_restricoes(cpf)
                if restricoes:
                    return ResultadoCriarCliente(
                        cliente_id=UUID('00000000-0000-0000-0000-000000000000'),
                        sucesso=False,
                        mensagem=f"Cliente possui restrições: {', '.join(restricoes)}"
                    )
            
            # 5. Criar cliente
            cliente = Cliente(
                nome=comando.nome,
                cpf=cpf,
                endereco=endereco,
                telefone=comando.telefone,
                email=comando.email,
                data_nascimento=comando.data_nascimento
            )
            
            # 6. Salvar cliente
            self._repo_cliente.salvar(cliente)
            
            # 7. Coletar eventos
            self._eventos_gerados.extend(cliente.obter_eventos())
            
            return ResultadoCriarCliente(
                cliente_id=cliente.id,
                sucesso=True,
                mensagem="Cliente criado com sucesso"
            )
            
        except Exception as e:
            return ResultadoCriarCliente(
                cliente_id=UUID('00000000-0000-0000-0000-000000000000'),
                sucesso=False,
                mensagem=f"Erro ao criar cliente: {str(e)}"
            )


@dataclass
class ComandoAbrirConta:
    """Comando para abrir conta"""
    cliente_id: str
    tipo_conta: TipoConta
    agencia: str
    deposito_inicial: Optional[Dinheiro] = None


@dataclass
class ResultadoAbrirConta:
    """Resultado da abertura de conta"""
    conta_id: str
    agencia: str
    numero: str
    sucesso: bool
    mensagem: str


class AbrirContaUseCase(CasoUsoBase):
    """
    Caso de uso para abrir conta
    
    RESPONSABILIDADES:
    - Validar cliente
    - Gerar número da conta
    - Aplicar regras de negócio
    - Criar e persistir conta
    """
    
    def __init__(self,
                 repo_cliente: IRepositorioCliente,
                 repo_conta: IRepositorioConta):
        super().__init__()
        self._repo_cliente = repo_cliente
        self._repo_conta = repo_conta
        self._contador_conta = 100000  # Simulação de contador
    
    def executar(self, comando: ComandoAbrirConta) -> ResultadoAbrirConta:
        """Executa abertura de conta"""
        try:
            # 1. Validar se cliente existe
            cliente = self._repo_cliente.buscar_por_id(comando.cliente_id)
            if not cliente:
                return ResultadoAbrirConta(
                    conta_id=UUID('00000000-0000-0000-0000-000000000000'),
                    agencia="",
                    numero="",
                    sucesso=False,
                    mensagem="Cliente não encontrado"
                )
            
            # 2. Verificar se cliente está ativo
            if not cliente.ativo:
                return ResultadoAbrirConta(
                    conta_id=UUID('00000000-0000-0000-0000-000000000000'),
                    agencia="",
                    numero="",
                    sucesso=False,
                    mensagem="Cliente inativo"
                )
            
            # 3. Gerar número da conta
            numero_conta = self._gerar_numero_conta()
            
            # 4. Validar depósito inicial se fornecido
            saldo_inicial = None
            if comando.deposito_inicial:
                if comando.deposito_inicial.valor <= 0:
                    return ResultadoAbrirConta(
                        conta_id=UUID('00000000-0000-0000-0000-000000000000'),
                        agencia="",
                        numero="",
                        sucesso=False,
                        mensagem="Depósito inicial deve ser positivo"
                    )
                saldo_inicial = comando.deposito_inicial
            
            # 5. Criar conta
            conta = Conta(
                cliente_id=comando.cliente_id,
                agencia=comando.agencia,
                numero=numero_conta,
                tipo=comando.tipo_conta,
                saldo_inicial=saldo_inicial
            )
            
            # 6. Salvar conta
            self._repo_conta.salvar(conta)
            
            # 7. Coletar eventos
            self._eventos_gerados.extend(conta.obter_eventos())
            
            return ResultadoAbrirConta(
                conta_id=conta.id,
                agencia=conta.agencia,
                numero=conta.numero_formatado,
                sucesso=True,
                mensagem="Conta aberta com sucesso"
            )
            
        except Exception as e:
            return ResultadoAbrirConta(
                conta_id=UUID('00000000-0000-0000-0000-000000000000'),
                agencia="",
                numero="",
                sucesso=False,
                mensagem=f"Erro ao abrir conta: {str(e)}"
            )
    
    def _gerar_numero_conta(self) -> str:
        """Gera número único da conta"""
        self._contador_conta += 1
        numero = str(self._contador_conta)
        # Calcular dígito verificador simples
        soma = sum(int(d) * (i + 1) for i, d in enumerate(numero))
        digito = soma % 10
        return numero + str(digito)


@dataclass
class ComandoRealizarTransferencia:
    """Comando para realizar transferência"""
    conta_origem_id: str
    conta_destino_id: str
    valor: Dinheiro
    descricao: str


@dataclass
class ResultadoRealizarTransferencia:
    """Resultado da transferência"""
    transacao_id: str
    sucesso: bool
    mensagem: str


class RealizarTransferenciaUseCase(CasoUsoBase):
    """
    Caso de uso para realizar transferência
    
    RESPONSABILIDADES:
    - Validar contas origem e destino
    - Verificar saldo e limites
    - Validar fraude
    - Executar transferência atomicamente
    - Registrar transações
    """
    
    def __init__(self,
                 repo_conta: IRepositorioConta,
                 repo_transacao: IRepositorioTransacao,
                 validador_fraude: Optional[IValidadorFraude] = None,
                 notificador: Optional[INotificadorTransacao] = None):
        super().__init__()
        self._repo_conta = repo_conta
        self._repo_transacao = repo_transacao
        self._validador_fraude = validador_fraude
        self._notificador = notificador
    
    def executar(self, comando: ComandoRealizarTransferencia) -> ResultadoRealizarTransferencia:
        """Executa transferência"""
        try:
            # 1. Validar valor
            if comando.valor.valor <= 0:
                return ResultadoRealizarTransferencia(
                    transacao_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="Valor deve ser positivo"
                )
            
            valor = comando.valor
            
            # 2. Buscar contas
            conta_origem = self._repo_conta.buscar_por_id(comando.conta_origem_id)
            conta_destino = self._repo_conta.buscar_por_id(comando.conta_destino_id)
            
            if not conta_origem:
                return ResultadoRealizarTransferencia(
                    transacao_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="Conta origem não encontrada"
                )
            
            if not conta_destino:
                return ResultadoRealizarTransferencia(
                    transacao_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="Conta destino não encontrada"
                )
            
            # 3. Validar se contas são diferentes
            if conta_origem.id == conta_destino.id:
                return ResultadoRealizarTransferencia(
                    transacao_id=UUID('00000000-0000-0000-0000-000000000000'),
                    sucesso=False,
                    mensagem="Conta origem e destino devem ser diferentes"
                )
            
            # 4. Criar transação
            transacao = Transacao(
                tipo=TipoTransacao.TRANSFERENCIA_SAIDA,
                valor=valor,
                descricao=comando.descricao,
                conta_origem_id=conta_origem.id,
                conta_destino_id=conta_destino.id
            )
            
            # 5. Validar fraude (se disponível)
            if self._validador_fraude:
                if not self._validador_fraude.validar(transacao, conta_origem):
                    transacao.falhar("Transação bloqueada por suspeita de fraude")
                    self._repo_transacao.salvar(transacao)
                    return ResultadoRealizarTransferencia(
                        transacao_id=transacao.id,
                        sucesso=False,
                        mensagem="Transação bloqueada por suspeita de fraude"
                    )
            
            # 6. Iniciar processamento
            transacao.processar()
            
            # 7. Verificar se origem pode realizar operação
            if not conta_origem.pode_realizar_operacao(valor, "TRANSFERENCIA_SAIDA"):
                transacao.falhar("Saldo ou limite insuficiente")
                self._repo_transacao.salvar(transacao)
                return ResultadoRealizarTransferencia(
                    transacao_id=transacao.id,
                    sucesso=False,
                    mensagem="Saldo ou limite insuficiente"
                )
            
            # 8. Verificar se destino pode receber
            if conta_destino.status != StatusConta.ATIVA:
                transacao.falhar("Conta destino não está ativa")
                self._repo_transacao.salvar(transacao)
                return ResultadoRealizarTransferencia(
                    transacao_id=transacao.id,
                    sucesso=False,
                    mensagem="Conta destino não está ativa"
                )
            
            # 9. Executar transferência atomicamente
            conta_origem.debitar(valor, "TRANSFERENCIA_SAIDA")
            conta_destino.creditar(valor)
            
            # 10. Concluir transação
            transacao.concluir()
            
            # 11. Registrar transação nas contas
            conta_origem.adicionar_transacao(transacao.id)
            conta_destino.adicionar_transacao(transacao.id)
            
            # 12. Persistir alterações
            self._repo_transacao.salvar(transacao)
            self._repo_conta.salvar(conta_origem)
            self._repo_conta.salvar(conta_destino)
            
            # 13. Coletar eventos
            self._eventos_gerados.extend(transacao.obter_eventos())
            self._eventos_gerados.extend(conta_origem.obter_eventos())
            self._eventos_gerados.extend(conta_destino.obter_eventos())
            
            # 14. Notificar (se disponível)
            if self._notificador:
                self._notificador.notificar_transacao_realizada(
                    transacao, conta_origem, conta_destino
                )
            
            return ResultadoRealizarTransferencia(
                transacao_id=transacao.id,
                sucesso=True,
                mensagem="Transferência realizada com sucesso"
            )
            
        except Exception as e:
            return ResultadoRealizarTransferencia(
                transacao_id=UUID('00000000-0000-0000-0000-000000000000'),
                sucesso=False,
                mensagem=f"Erro ao realizar transferência: {str(e)}"
            )


# =============================================================================
# FUNÇÃO PRINCIPAL E DEMONSTRAÇÕES
# =============================================================================

def demonstrar_sistema_bancario():
    """
    Demonstração completa do sistema bancário
    
    OBJETIVOS:
    - Mostrar Arquitetura Hexagonal
    - Demonstrar Domain-Driven Design
    - Validar princípios SOLID
    - Exibir múltiplos design patterns
    """
    
    print("🏦 SISTEMA BANCÁRIO - ARQUITETURA HEXAGONAL")
    print("=" * 70)
    print("Demonstrando Arquitetura Hexagonal (Ports & Adapters)")
    print("com Domain-Driven Design e princípios SOLID")
    print()
    print("🏗️ CAMADAS DA ARQUITETURA:")
    print("📦 Domain (Core)    - Entidades, VOs, Regras de Negócio")
    print("📦 Application      - Casos de Uso, Ports (Interfaces)")  
    print("📦 Infrastructure   - Adapters, Persistência, APIs")
    print("=" * 70)


if __name__ == "__main__":
    demonstrar_sistema_bancario()
