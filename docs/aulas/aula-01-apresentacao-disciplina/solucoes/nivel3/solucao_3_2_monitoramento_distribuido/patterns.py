 #!/usr/bin/env python3
"""
SISTEMA DE MONITORAMENTO DISTRIBUÍDO
Demonstração de Padrões Arquiteturais Avançados

Este sistema demonstra padrões avançados para sistemas distribuídos:
- Event Sourcing e CQRS
- Circuit Breaker Pattern
- Saga Pattern para transações distribuídas
- Observer Pattern para métricas
- Publish-Subscribe para comunicação
- Retry Pattern com backoff exponencial
- Bulkhead Pattern para isolamento

EXECUTAR: python main.py

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

import json
import time
import uuid
import threading
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Union
from collections import defaultdict, deque
import concurrent.futures
import asyncio
from functools import wraps


# =============================================================================
# DOMAIN LAYER - EVENTOS E AGREGADOS
# =============================================================================

class TipoEvento(Enum):
    """Tipos de eventos no sistema"""
    SERVICO_INICIADO = "servico_iniciado"
    SERVICO_PARADO = "servico_parado"
    METRICA_COLETADA = "metrica_coletada"
    ALERTA_GERADO = "alerta_gerado"
    SISTEMA_INDISPONIVEL = "sistema_indisponivel"
    SISTEMA_RECUPERADO = "sistema_recuperado"
    TRANSACAO_INICIADA = "transacao_iniciada"
    TRANSACAO_COMPLETADA = "transacao_completada"
    TRANSACAO_FALHADA = "transacao_falhada"


class SeveridadeAlerta(Enum):
    """Níveis de severidade de alertas"""
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class StatusServico(Enum):
    """Status possíveis de um serviço"""
    INICIANDO = auto()
    ATIVO = auto()
    DEGRADADO = auto()
    INDISPONIVEL = auto()
    MANUTENCAO = auto()


@dataclass(frozen=True)
class EventoSistema:
    """Evento base do sistema"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    tipo: TipoEvento = TipoEvento.METRICA_COLETADA
    origem: str = ""
    dados: Dict[str, Any] = field(default_factory=dict)
    versao: int = 1


@dataclass
class Metrica:
    """Value Object para métricas"""
    nome: str
    valor: Union[int, float, str]
    unidade: str
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.valor, (int, float)) and self.valor < 0:
            raise ValueError("Métricas numéricas não podem ser negativas")


@dataclass
class Alerta:
    """Entidade de alerta"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    titulo: str = ""
    descricao: str = ""
    severidade: SeveridadeAlerta = SeveridadeAlerta.INFO
    origem: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    resolvido: bool = False
    timestamp_resolucao: Optional[datetime] = None
    metadados: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Servico:
    """Entidade de serviço monitorado"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nome: str = ""
    url: str = ""
    status: StatusServico = StatusServico.INICIANDO
    ultima_verificacao: datetime = field(default_factory=datetime.now)
    tempo_resposta_ms: float = 0.0
    taxa_erro: float = 0.0
    metricas: List[Metrica] = field(default_factory=list)
    alertas_ativos: List[str] = field(default_factory=list)  # IDs dos alertas
    configuracao: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# PADRÃO EVENT SOURCING E CQRS
# =============================================================================

class EventStore:
    """
    Event Store para Event Sourcing
    
    RESPONSABILIDADES:
    - Armazenar eventos de forma imutável
    - Permitir consulta de eventos por agregado
    - Suportar snapshots para performance
    - Garantir ordenação temporal
    """
    
    def __init__(self):
        self._eventos: List[EventoSistema] = []
        self._indices_por_origem: Dict[str, List[int]] = defaultdict(list)
        self._snapshots: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def adicionar_evento(self, evento: EventoSistema) -> None:
        """Adiciona evento ao store"""
        with self._lock:
            posicao = len(self._eventos)
            self._eventos.append(evento)
            self._indices_por_origem[evento.origem].append(posicao)
    
    def obter_eventos_por_origem(self, origem: str, 
                                desde: Optional[datetime] = None) -> List[EventoSistema]:
        """Obtém todos os eventos de uma origem"""
        with self._lock:
            indices = self._indices_por_origem.get(origem, [])
            eventos = [self._eventos[i] for i in indices]
            
            if desde:
                eventos = [e for e in eventos if e.timestamp >= desde]
            
            return sorted(eventos, key=lambda e: e.timestamp)
    
    def obter_todos_eventos(self, desde: Optional[datetime] = None,
                           ate: Optional[datetime] = None) -> List[EventoSistema]:
        """Obtém todos os eventos do sistema"""
        with self._lock:
            eventos = list(self._eventos)
            
            if desde:
                eventos = [e for e in eventos if e.timestamp >= desde]
            if ate:
                eventos = [e for e in eventos if e.timestamp <= ate]
            
            return sorted(eventos, key=lambda e: e.timestamp)


class QueryModel:
    """
    Modelo de consulta para CQRS
    
    Projetado a partir dos eventos para consultas otimizadas
    """
    
    def __init__(self, event_store: EventStore):
        self._event_store = event_store
        self._servicos: Dict[str, Servico] = {}
        self._alertas: Dict[str, Alerta] = {}
        self._metricas_agregadas: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._lock = threading.RLock()
        self._ultimo_evento_processado = 0
    
    def atualizar_projecoes(self) -> None:
        """Atualiza as projeções baseadas nos novos eventos"""
        with self._lock:
            todos_eventos = self._event_store.obter_todos_eventos()
            
            # Processar apenas eventos novos
            novos_eventos = todos_eventos[self._ultimo_evento_processado:]
            
            for evento in novos_eventos:
                self._processar_evento(evento)
            
            self._ultimo_evento_processado = len(todos_eventos)
    
    def _processar_evento(self, evento: EventoSistema) -> None:
        """Processa um evento para atualizar as projeções"""
        if evento.tipo == TipoEvento.SERVICO_INICIADO:
            self._processar_servico_iniciado(evento)
        elif evento.tipo == TipoEvento.METRICA_COLETADA:
            self._processar_metrica_coletada(evento)
        elif evento.tipo == TipoEvento.ALERTA_GERADO:
            self._processar_alerta_gerado(evento)
        elif evento.tipo == TipoEvento.SISTEMA_INDISPONIVEL:
            self._processar_sistema_indisponivel(evento)
        elif evento.tipo == TipoEvento.SISTEMA_RECUPERADO:
            self._processar_sistema_recuperado(evento)
    
    def _processar_servico_iniciado(self, evento: EventoSistema) -> None:
        """Processa evento de serviço iniciado"""
        dados = evento.dados
        servico = Servico(
            id=evento.origem,
            nome=dados.get('nome', ''),
            url=dados.get('url', ''),
            status=StatusServico.ATIVO,
            ultima_verificacao=evento.timestamp,
            configuracao=dados.get('configuracao', {})
        )
        self._servicos[evento.origem] = servico
    
    def _processar_metrica_coletada(self, evento: EventoSistema) -> None:
        """Processa evento de métrica coletada"""
        dados = evento.dados
        
        # Atualizar métricas do serviço
        if evento.origem in self._servicos:
            servico = self._servicos[evento.origem]
            metrica = Metrica(
                nome=dados.get('nome', ''),
                valor=dados.get('valor', 0),
                unidade=dados.get('unidade', ''),
                timestamp=evento.timestamp,
                tags=dados.get('tags', {})
            )
            servico.metricas.append(metrica)
            
            # Manter apenas últimas 100 métricas por performance
            if len(servico.metricas) > 100:
                servico.metricas = servico.metricas[-100:]
        
        # Agregações para consultas rápidas
        nome_metrica = dados.get('nome', '')
        valor = dados.get('valor', 0)
        
        if nome_metrica not in self._metricas_agregadas:
            self._metricas_agregadas[nome_metrica] = {
                'total': 0,
                'count': 0,
                'min': float('inf'),
                'max': float('-inf'),
                'ultima_atualizacao': evento.timestamp
            }
        
        agg = self._metricas_agregadas[nome_metrica]
        if isinstance(valor, (int, float)):
            agg['total'] += valor
            agg['count'] += 1
            agg['min'] = min(agg['min'], valor)
            agg['max'] = max(agg['max'], valor)
            agg['media'] = agg['total'] / agg['count']
        agg['ultima_atualizacao'] = evento.timestamp
    
    def _processar_alerta_gerado(self, evento: EventoSistema) -> None:
        """Processa evento de alerta gerado"""
        dados = evento.dados
        alerta = Alerta(
            id=dados.get('id', str(uuid.uuid4())),
            titulo=dados.get('titulo', ''),
            descricao=dados.get('descricao', ''),
            severidade=SeveridadeAlerta(dados.get('severidade', 1)),
            origem=evento.origem,
            timestamp=evento.timestamp,
            metadados=dados.get('metadados', {})
        )
        self._alertas[alerta.id] = alerta
        
        # Adicionar à lista de alertas ativos do serviço
        if evento.origem in self._servicos:
            self._servicos[evento.origem].alertas_ativos.append(alerta.id)
    
    def _processar_sistema_indisponivel(self, evento: EventoSistema) -> None:
        """Processa evento de sistema indisponível"""
        if evento.origem in self._servicos:
            self._servicos[evento.origem].status = StatusServico.INDISPONIVEL
            self._servicos[evento.origem].ultima_verificacao = evento.timestamp
    
    def _processar_sistema_recuperado(self, evento: EventoSistema) -> None:
        """Processa evento de sistema recuperado"""
        if evento.origem in self._servicos:
            self._servicos[evento.origem].status = StatusServico.ATIVO
            self._servicos[evento.origem].ultima_verificacao = evento.timestamp
    
    def obter_servicos(self) -> List[Servico]:
        """Obtém todos os serviços"""
        self.atualizar_projecoes()
        with self._lock:
            return list(self._servicos.values())
    
    def obter_servico(self, servico_id: str) -> Optional[Servico]:
        """Obtém um serviço específico"""
        self.atualizar_projecoes()
        with self._lock:
            return self._servicos.get(servico_id)
    
    def obter_alertas_ativos(self) -> List[Alerta]:
        """Obtém todos os alertas ativos"""
        self.atualizar_projecoes()
        with self._lock:
            return [a for a in self._alertas.values() if not a.resolvido]
    
    def obter_metricas_agregadas(self, nome_metrica: str) -> Optional[Dict[str, Any]]:
        """Obtém agregações de uma métrica"""
        self.atualizar_projecoes()
        with self._lock:
            return self._metricas_agregadas.get(nome_metrica)


# =============================================================================
# CIRCUIT BREAKER PATTERN
# =============================================================================

class EstadoCircuitBreaker(Enum):
    """Estados do Circuit Breaker"""
    FECHADO = "fechado"      # Funcionando normalmente
    ABERTO = "aberto"        # Bloqueando chamadas
    MEIO_ABERTO = "meio_aberto"  # Testando recuperação


class CircuitBreaker:
    """
    Implementação do Circuit Breaker Pattern
    
    RESPONSABILIDADES:
    - Detectar falhas em cascata
    - Falhar rapidamente quando sistema está indisponível
    - Permitir recuperação automática
    - Coletar métricas de falhas
    """
    
    def __init__(self, 
                 threshold_falhas: int = 5,
                 timeout_segundos: int = 60,
                 nome: str = "CircuitBreaker"):
        self.threshold_falhas = threshold_falhas
        self.timeout_segundos = timeout_segundos
        self.nome = nome
        
        self._estado = EstadoCircuitBreaker.FECHADO
        self._contador_falhas = 0
        self._timestamp_ultimo_erro = None
        self._timestamp_ultima_tentativa = None
        self._lock = threading.RLock()
        
        # Métricas
        self._total_chamadas = 0
        self._total_sucessos = 0
        self._total_falhas = 0
        self._historico_estados = []
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator para aplicar circuit breaker"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.executar(func, *args, **kwargs)
        return wrapper
    
    def executar(self, func: Callable, *args, **kwargs) -> Any:
        """Executa função com proteção do circuit breaker"""
        with self._lock:
            self._total_chamadas += 1
            self._timestamp_ultima_tentativa = datetime.now()
            
            # Verificar estado antes de executar
            if self._estado == EstadoCircuitBreaker.ABERTO:
                if self._deve_tentar_recuperacao():
                    self._transicionar_para_meio_aberto()
                else:
                    raise CircuitBreakerAbertoException(
                        f"Circuit breaker {self.nome} está aberto"
                    )
            
            try:
                resultado = func(*args, **kwargs)
                self._registrar_sucesso()
                return resultado
                
            except Exception as e:
                self._registrar_falha()
                raise e
    
    def _deve_tentar_recuperacao(self) -> bool:
        """Verifica se é hora de tentar recuperação"""
        if not self._timestamp_ultimo_erro:
            return True
        
        tempo_desde_ultimo_erro = datetime.now() - self._timestamp_ultimo_erro
        return tempo_desde_ultimo_erro.total_seconds() >= self.timeout_segundos
    
    def _transicionar_para_meio_aberto(self) -> None:
        """Transiciona para estado meio-aberto"""
        self._estado = EstadoCircuitBreaker.MEIO_ABERTO
        self._historico_estados.append({
            'estado': self._estado,
            'timestamp': datetime.now(),
            'motivo': 'tentativa_recuperacao'
        })
    
    def _registrar_sucesso(self) -> None:
        """Registra execução bem-sucedida"""
        self._total_sucessos += 1
        
        if self._estado == EstadoCircuitBreaker.MEIO_ABERTO:
            # Sucesso no meio-aberto: volta para fechado
            self._estado = EstadoCircuitBreaker.FECHADO
            self._contador_falhas = 0
            self._historico_estados.append({
                'estado': self._estado,
                'timestamp': datetime.now(),
                'motivo': 'recuperacao_bem_sucedida'
            })
        elif self._estado == EstadoCircuitBreaker.FECHADO:
            # Reduzir contador de falhas gradualmente
            self._contador_falhas = max(0, self._contador_falhas - 1)
    
    def _registrar_falha(self) -> None:
        """Registra execução falhada"""
        self._total_falhas += 1
        self._contador_falhas += 1
        self._timestamp_ultimo_erro = datetime.now()
        
        if self._contador_falhas >= self.threshold_falhas:
            if self._estado != EstadoCircuitBreaker.ABERTO:
                self._estado = EstadoCircuitBreaker.ABERTO
                self._historico_estados.append({
                    'estado': self._estado,
                    'timestamp': datetime.now(),
                    'motivo': f'threshold_atingido_{self._contador_falhas}'
                })
    
    def obter_metricas(self) -> Dict[str, Any]:
        """Obtém métricas do circuit breaker"""
        with self._lock:
            taxa_sucesso = (self._total_sucessos / self._total_chamadas * 100 
                           if self._total_chamadas > 0 else 0)
            
            return {
                'nome': self.nome,
                'estado': self._estado.value,
                'total_chamadas': self._total_chamadas,
                'total_sucessos': self._total_sucessos,
                'total_falhas': self._total_falhas,
                'contador_falhas_atual': self._contador_falhas,
                'taxa_sucesso_pct': round(taxa_sucesso, 2),
                'timestamp_ultimo_erro': self._timestamp_ultimo_erro,
                'timestamp_ultima_tentativa': self._timestamp_ultima_tentativa,
                'historico_estados': self._historico_estados[-10:]  # Últimos 10
            }
    
    def reset(self) -> None:
        """Reset manual do circuit breaker"""
        with self._lock:
            self._estado = EstadoCircuitBreaker.FECHADO
            self._contador_falhas = 0
            self._historico_estados.append({
                'estado': self._estado,
                'timestamp': datetime.now(),
                'motivo': 'reset_manual'
            })


class CircuitBreakerAbertoException(Exception):
    """Exceção lançada quando circuit breaker está aberto"""
    pass


# =============================================================================
# RETRY PATTERN COM BACKOFF EXPONENCIAL
# =============================================================================

class RetryStrategy:
    """
    Estratégia de retry com backoff exponencial
    
    RESPONSABILIDADES:
    - Implementar diferentes estratégias de retry
    - Calcular intervalos de espera
    - Definir condições de parada
    """
    
    def __init__(self,
                 max_tentativas: int = 3,
                 delay_inicial_ms: int = 100,
                 multiplicador: float = 2.0,
                 delay_maximo_ms: int = 30000,
                 jitter: bool = True):
        self.max_tentativas = max_tentativas
        self.delay_inicial_ms = delay_inicial_ms
        self.multiplicador = multiplicador
        self.delay_maximo_ms = delay_maximo_ms
        self.jitter = jitter
    
    def calcular_delay(self, tentativa: int) -> int:
        """Calcula delay para uma tentativa específica"""
        if tentativa <= 0:
            return 0
        
        # Backoff exponencial
        delay = self.delay_inicial_ms * (self.multiplicador ** (tentativa - 1))
        delay = min(delay, self.delay_maximo_ms)
        
        # Adicionar jitter para evitar thundering herd
        if self.jitter:
            jitter_amount = delay * 0.1  # 10% de jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        return max(0, int(delay))
    
    def deve_tentar_novamente(self, tentativa: int, exception: Exception) -> bool:
        """Verifica se deve tentar novamente"""
        if tentativa >= self.max_tentativas:
            return False
        
        # Algumas exceções não devem ser retriadas
        if isinstance(exception, (ValueError, TypeError)):
            return False
        
        return True


class RetryExecutor:
    """
    Executor de operações com retry
    """
    
    def __init__(self, strategy: RetryStrategy, nome: str = "RetryExecutor"):
        self.strategy = strategy
        self.nome = nome
        self._metricas = {
            'total_execucoes': 0,
            'total_sucessos': 0,
            'total_falhas': 0,
            'tentativas_por_execucao': [],
            'ultima_execucao': None
        }
    
    def executar(self, func: Callable, *args, **kwargs) -> Any:
        """Executa função com retry"""
        self._metricas['total_execucoes'] += 1
        self._metricas['ultima_execucao'] = datetime.now()
        
        ultima_exception = None
        
        for tentativa in range(1, self.strategy.max_tentativas + 1):
            try:
                resultado = func(*args, **kwargs)
                self._metricas['total_sucessos'] += 1
                self._metricas['tentativas_por_execucao'].append(tentativa)
                return resultado
                
            except Exception as e:
                ultima_exception = e
                
                if not self.strategy.deve_tentar_novamente(tentativa, e):
                    break
                
                if tentativa < self.strategy.max_tentativas:
                    delay_ms = self.strategy.calcular_delay(tentativa)
                    if delay_ms > 0:
                        time.sleep(delay_ms / 1000)  # Converter para segundos
        
        # Se chegou aqui, todas as tentativas falharam
        self._metricas['total_falhas'] += 1
        self._metricas['tentativas_por_execucao'].append(self.strategy.max_tentativas)
        
        raise RetryExhaustedException(
            f"Todas as {self.strategy.max_tentativas} tentativas falharam",
            ultima_exception
        )
    
    def obter_metricas(self) -> Dict[str, Any]:
        """Obtém métricas do retry executor"""
        tentativas = self._metricas['tentativas_por_execucao']
        
        return {
            'nome': self.nome,
            'total_execucoes': self._metricas['total_execucoes'],
            'total_sucessos': self._metricas['total_sucessos'],
            'total_falhas': self._metricas['total_falhas'],
            'taxa_sucesso_pct': (
                self._metricas['total_sucessos'] / 
                max(1, self._metricas['total_execucoes']) * 100
            ),
            'media_tentativas': sum(tentativas) / max(1, len(tentativas)),
            'ultima_execucao': self._metricas['ultima_execucao']
        }


class RetryExhaustedException(Exception):
    """Exceção lançada quando todas as tentativas de retry falham"""
    
    def __init__(self, message: str, causa_original: Exception):
        super().__init__(message)
        self.causa_original = causa_original


# =============================================================================
# PUBLISH-SUBSCRIBE PATTERN
# =============================================================================

class EventBus:
    """
    Event Bus para comunicação desacoplada
    
    RESPONSABILIDADES:
    - Gerenciar inscrições de handlers
    - Distribuir eventos para subscribers
    - Suportar filtragem de eventos
    - Processamento assíncrono opcional
    """
    
    def __init__(self, nome: str = "EventBus"):
        self.nome = nome
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._global_subscribers: List[Callable] = []
        self._filtros: Dict[str, Callable] = {}
        self._metricas = {
            'eventos_publicados': 0,
            'eventos_processados': 0,
            'eventos_falhados': 0,
            'subscribers_ativos': 0
        }
        self._lock = threading.RLock()
        
        # Pool de threads para processamento assíncrono
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=5, thread_name_prefix=f"EventBus-{nome}"
        )
    
    def subscrever(self, tipo_evento: str, handler: Callable, 
                   filtro: Optional[Callable] = None) -> str:
        """Subscreve um handler para um tipo de evento"""
        with self._lock:
            subscription_id = str(uuid.uuid4())
            
            # Wrapper que inclui ID da subscription
            def wrapper_handler(evento):
                try:
                    # Aplicar filtro se fornecido
                    if filtro and not filtro(evento):
                        return
                    
                    handler(evento)
                    self._metricas['eventos_processados'] += 1
                    
                except Exception as e:
                    self._metricas['eventos_falhados'] += 1
                    print(f"Erro em handler {subscription_id}: {e}")
            
            wrapper_handler.subscription_id = subscription_id
            wrapper_handler.original_handler = handler
            
            self._subscribers[tipo_evento].append(wrapper_handler)
            self._metricas['subscribers_ativos'] += 1
            
            return subscription_id
    
    def subscrever_global(self, handler: Callable) -> str:
        """Subscreve um handler para todos os eventos"""
        with self._lock:
            subscription_id = str(uuid.uuid4())
            
            def wrapper_handler(evento):
                try:
                    handler(evento)
                    self._metricas['eventos_processados'] += 1
                except Exception as e:
                    self._metricas['eventos_falhados'] += 1
                    print(f"Erro em handler global {subscription_id}: {e}")
            
            wrapper_handler.subscription_id = subscription_id
            wrapper_handler.original_handler = handler
            
            self._global_subscribers.append(wrapper_handler)
            self._metricas['subscribers_ativos'] += 1
            
            return subscription_id
    
    def desinscrever(self, subscription_id: str) -> bool:
        """Remove uma subscription"""
        with self._lock:
            # Procurar em subscribers por tipo
            for tipo, handlers in self._subscribers.items():
                handlers_removidos = [
                    h for h in handlers 
                    if getattr(h, 'subscription_id', None) == subscription_id
                ]
                if handlers_removidos:
                    for handler in handlers_removidos:
                        handlers.remove(handler)
                        self._metricas['subscribers_ativos'] -= 1
                    return True
            
            # Procurar em subscribers globais
            handlers_removidos = [
                h for h in self._global_subscribers
                if getattr(h, 'subscription_id', None) == subscription_id
            ]
            if handlers_removidos:
                for handler in handlers_removidos:
                    self._global_subscribers.remove(handler)
                    self._metricas['subscribers_ativos'] -= 1
                return True
            
            return False
    
    def publicar(self, evento: EventoSistema, assincrono: bool = True) -> None:
        """Publica um evento para todos os subscribers"""
        with self._lock:
            self._metricas['eventos_publicados'] += 1
            
            # Coletar handlers relevantes
            handlers_tipo = self._subscribers.get(evento.tipo.value, [])
            handlers_global = self._global_subscribers
            todos_handlers = handlers_tipo + handlers_global
            
            if not todos_handlers:
                return
            
            if assincrono:
                # Processar assincronamente
                for handler in todos_handlers:
                    self._executor.submit(handler, evento)
            else:
                # Processar sincronamente
                for handler in todos_handlers:
                    try:
                        handler(evento)
                    except Exception as e:
                        print(f"Erro ao processar evento {evento.id}: {e}")
    
    def obter_metricas(self) -> Dict[str, Any]:
        """Obtém métricas do event bus"""
        with self._lock:
            return {
                'nome': self.nome,
                'subscribers_por_tipo': {
                    tipo: len(handlers) 
                    for tipo, handlers in self._subscribers.items()
                },
                'subscribers_globais': len(self._global_subscribers),
                'total_subscribers': self._metricas['subscribers_ativos'],
                'eventos_publicados': self._metricas['eventos_publicados'],
                'eventos_processados': self._metricas['eventos_processados'],
                'eventos_falhados': self._metricas['eventos_falhados']
            }
    
    def shutdown(self) -> None:
        """Finaliza o event bus"""
        self._executor.shutdown(wait=True)


# =============================================================================
# BULKHEAD PATTERN
# =============================================================================

class RecursoBulkhead:
    """
    Implementação do Bulkhead Pattern para isolamento de recursos
    
    RESPONSABILIDADES:
    - Isolar pools de recursos
    - Prevenir que falhas em um pool afetem outros
    - Monitorar utilização de recursos
    - Aplicar throttling quando necessário
    """
    
    def __init__(self, nome: str, tamanho_pool: int = 10):
        self.nome = nome
        self.tamanho_pool = tamanho_pool
        self._semaforo = threading.Semaphore(tamanho_pool)
        self._recursos_em_uso = 0
        self._max_recursos_utilizados = 0
        self._total_aquisicoes = 0
        self._total_timeouts = 0
        self._lock = threading.RLock()
        self._historico_utilizacao = deque(maxlen=100)
    
    def adquirir_recurso(self, timeout_segundos: float = 5.0) -> 'RecursoContext':
        """Adquire um recurso do pool"""
        acquired = self._semaforo.acquire(timeout=timeout_segundos)
        
        with self._lock:
            self._total_aquisicoes += 1
            
            if not acquired:
                self._total_timeouts += 1
                raise BulkheadTimeoutException(
                    f"Timeout ao adquirir recurso do pool {self.nome}"
                )
            
            self._recursos_em_uso += 1
            self._max_recursos_utilizados = max(
                self._max_recursos_utilizados, 
                self._recursos_em_uso
            )
            
            timestamp = datetime.now()
            self._historico_utilizacao.append({
                'timestamp': timestamp,
                'recursos_em_uso': self._recursos_em_uso,
                'utilizacao_pct': (self._recursos_em_uso / self.tamanho_pool) * 100
            })
            
            return RecursoContext(self, timestamp)
    
    def liberar_recurso(self) -> None:
        """Libera um recurso do pool"""
        with self._lock:
            if self._recursos_em_uso > 0:
                self._recursos_em_uso -= 1
        
        self._semaforo.release()
    
    def obter_metricas(self) -> Dict[str, Any]:
        """Obtém métricas do bulkhead"""
        with self._lock:
            utilizacao_atual = (self._recursos_em_uso / self.tamanho_pool) * 100
            
            # Calcular utilização média nas últimas medições
            utilizacoes_recentes = [
                h['utilizacao_pct'] for h in list(self._historico_utilizacao)[-10:]
            ]
            utilizacao_media = (
                sum(utilizacoes_recentes) / len(utilizacoes_recentes)
                if utilizacoes_recentes else 0
            )
            
            return {
                'nome': self.nome,
                'tamanho_pool': self.tamanho_pool,
                'recursos_em_uso': self._recursos_em_uso,
                'recursos_disponiveis': self.tamanho_pool - self._recursos_em_uso,
                'utilizacao_atual_pct': round(utilizacao_atual, 2),
                'utilizacao_media_pct': round(utilizacao_media, 2),
                'max_recursos_utilizados': self._max_recursos_utilizados,
                'total_aquisicoes': self._total_aquisicoes,
                'total_timeouts': self._total_timeouts,
                'taxa_timeout_pct': (
                    self._total_timeouts / max(1, self._total_aquisicoes) * 100
                )
            }


class RecursoContext:
    """Context manager para recursos do bulkhead"""
    
    def __init__(self, bulkhead: RecursoBulkhead, timestamp_aquisicao: datetime):
        self.bulkhead = bulkhead
        self.timestamp_aquisicao = timestamp_aquisicao
        self._liberado = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._liberado:
            self.bulkhead.liberar_recurso()
            self._liberado = True
    
    def tempo_uso(self) -> timedelta:
        """Retorna tempo de uso do recurso"""
        return datetime.now() - self.timestamp_aquisicao


class BulkheadTimeoutException(Exception):
    """Exceção lançada quando há timeout na aquisição de recurso"""
    pass


# =============================================================================
# SIMULADOR DE SERVIÇOS
# =============================================================================

class SimuladorServico:
    """
    Simula um serviço externo para demonstração
    """
    
    def __init__(self, nome: str, taxa_falha: float = 0.1, 
                 latencia_base_ms: int = 100):
        self.nome = nome
        self.taxa_falha = taxa_falha
        self.latencia_base_ms = latencia_base_ms
        self._ativo = True
    
    def fazer_requisicao(self) -> Dict[str, Any]:
        """Simula uma requisição ao serviço"""
        # Simular latência
        latencia = self.latencia_base_ms + random.randint(0, 50)
        time.sleep(latencia / 1000)
        
        # Simular falhas
        if not self._ativo or random.random() < self.taxa_falha:
            raise Exception(f"Falha simulada no serviço {self.nome}")
        
        return {
            'status': 'success',
            'data': f'Resposta do {self.nome}',
            'timestamp': datetime.now().isoformat(),
            'latencia_ms': latencia
        }
    
    def definir_ativo(self, ativo: bool) -> None:
        """Define se o serviço está ativo"""
        self._ativo = ativo
    
    def definir_taxa_falha(self, taxa: float) -> None:
        """Define taxa de falha do serviço"""
        self.taxa_falha = max(0.0, min(1.0, taxa))


if __name__ == "__main__":
    print("🏗️ SISTEMA DE MONITORAMENTO DISTRIBUÍDO")
    print("Demonstração de Padrões Arquiteturais Avançados")
    print()
    print("Execute 'python main.py' para ver a demonstração completa")
