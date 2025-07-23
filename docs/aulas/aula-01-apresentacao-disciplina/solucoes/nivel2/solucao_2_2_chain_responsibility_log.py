#!/usr/bin/env python3
"""
EXERCÍCIO 2.2: CHAIN OF RESPONSIBILITY - SISTEMA DE LOGGING

CONTEXTO: Implementar um sistema de logging robusto que utiliza o padrão 
Chain of Responsibility para processar mensagens através de diferentes 
handlers, cada um com responsabilidades específicas.

OBJETIVOS:
1. Demonstrar o padrão Chain of Responsibility
2. Criar um pipeline de processamento de logs
3. Implementar diferentes níveis de logging
4. Mostrar flexibilidade na configuração de handlers
5. Aplicar princípios SOLID no design

CONCEITOS DEMONSTRADOS:
- Chain of Responsibility Pattern
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP) 
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)
- Strategy Pattern (para formatadores)
- Template Method Pattern (para handlers base)
- Observer Pattern (para notificações)

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Protocol, Any, Callable
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import queue
import time
from pathlib import Path


# =============================================================================
# VALUE OBJECTS E ENUMERAÇÕES
# =============================================================================

class NivelLog(Enum):
    """Níveis de log com valores numéricos para comparação"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class TipoHandler(Enum):
    """Tipos de handlers disponíveis"""
    CONSOLE = auto()
    ARQUIVO = auto()
    EMAIL = auto()
    DATABASE = auto()
    WEBHOOK = auto()
    SYSLOG = auto()


@dataclass(frozen=True)
class MensagemLog:
    """
    Value Object para representar uma mensagem de log
    
    RESPONSABILIDADES:
    - Encapsular dados da mensagem
    - Garantir imutabilidade
    - Fornecer representação consistente
    """
    nivel: NivelLog
    mensagem: str
    timestamp: datetime = field(default_factory=datetime.now)
    contexto: Dict[str, Any] = field(default_factory=dict)
    origem: str = ""
    thread_id: str = field(default_factory=lambda: str(threading.current_thread().ident))
    
    def __post_init__(self):
        """Validações pós-inicialização"""
        if not self.mensagem.strip():
            raise ValueError("Mensagem não pode estar vazia")
        
        if not isinstance(self.nivel, NivelLog):
            raise ValueError("Nível deve ser uma instância de NivelLog")


@dataclass(frozen=True)
class ConfiguracaoHandler:
    """
    Value Object para configuração de handlers
    
    RESPONSABILIDADES:
    - Encapsular configurações específicas do handler
    - Validar parâmetros de configuração
    - Fornecer defaults seguros
    """
    tipo: TipoHandler
    nivel_minimo: NivelLog = NivelLog.INFO
    formatador: str = "padrao"
    parametros: Dict[str, Any] = field(default_factory=dict)
    ativo: bool = True
    
    def __post_init__(self):
        """Validações pós-inicialização"""
        if not isinstance(self.tipo, TipoHandler):
            raise ValueError("Tipo deve ser uma instância de TipoHandler")


# =============================================================================
# INTERFACES E PROTOCOLOS
# =============================================================================

class IFormatadorLog(Protocol):
    """
    Interface para formatadores de log
    
    RESPONSABILIDADES:
    - Definir contrato para formatação de mensagens
    - Permitir diferentes estratégias de formatação
    """
    
    def formatar(self, mensagem: MensagemLog) -> str:
        """Formatar mensagem de log para string"""
        ...


class INotificadorCritico(Protocol):
    """
    Interface para notificação de logs críticos
    
    RESPONSABILIDADES:
    - Definir contrato para notificações críticas
    - Permitir diferentes estratégias de notificação
    """
    
    def notificar_critico(self, mensagem: MensagemLog) -> None:
        """Notificar sobre log crítico"""
        ...


class IRepositorioLog(Protocol):
    """
    Interface para persistência de logs
    
    RESPONSABILIDADES:
    - Definir contrato para armazenamento
    - Abstrair detalhes de persistência
    """
    
    def salvar(self, mensagem: MensagemLog, conteudo_formatado: str) -> None:
        """Salvar log no repositório"""
        ...
    
    def buscar(self, filtros: Dict[str, Any]) -> List[MensagemLog]:
        """Buscar logs com filtros"""
        ...


class IMetricasLog(Protocol):
    """
    Interface para coleta de métricas de logging
    
    RESPONSABILIDADES:
    - Definir contrato para métricas
    - Permitir monitoramento do sistema
    """
    
    def registrar_processamento(self, mensagem: MensagemLog, handler: str) -> None:
        """Registrar que uma mensagem foi processada"""
        ...
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obter estatísticas do sistema de log"""
        ...


# =============================================================================
# HANDLERS BASE - TEMPLATE METHOD PATTERN
# =============================================================================

class HandlerLogBase(ABC):
    """
    Classe base abstrata para handlers de log
    
    RESPONSABILIDADES:
    - Implementar Chain of Responsibility
    - Definir template method para processamento
    - Gerenciar referência ao próximo handler
    - Aplicar filtros básicos
    
    PADRÕES APLICADOS:
    - Template Method Pattern
    - Chain of Responsibility Pattern
    """
    
    def __init__(self, configuracao: ConfiguracaoHandler):
        self._configuracao = configuracao
        self._proximo_handler: Optional['HandlerLogBase'] = None
        self._formatador: IFormatadorLog = FormatadorPadrao()
        self._metricas: Optional[IMetricasLog] = None
    
    def definir_proximo(self, handler: 'HandlerLogBase') -> 'HandlerLogBase':
        """
        Define o próximo handler na cadeia
        
        RETORNA: O handler passado para facilitar encadeamento fluente
        """
        self._proximo_handler = handler
        return handler
    
    def definir_formatador(self, formatador: IFormatadorLog) -> None:
        """Define o formatador para este handler"""
        self._formatador = formatador
    
    def definir_metricas(self, metricas: IMetricasLog) -> None:
        """Define o coletor de métricas"""
        self._metricas = metricas
    
    def processar(self, mensagem: MensagemLog) -> None:
        """
        Template method para processamento de mensagens
        
        RESPONSABILIDADES:
        - Aplicar filtros
        - Delegar processamento específico
        - Passar para próximo handler
        - Registrar métricas
        """
        try:
            # Aplicar filtros básicos
            if self._deve_processar(mensagem):
                # Processar neste handler
                self._processar_interno(mensagem)
                
                # Registrar métricas se disponível
                if self._metricas:
                    self._metricas.registrar_processamento(
                        mensagem, 
                        self.__class__.__name__
                    )
            
            # Continuar a cadeia
            if self._proximo_handler:
                self._proximo_handler.processar(mensagem)
                
        except Exception as e:
            self._tratar_erro(mensagem, e)
            
            # Mesmo com erro, continuar a cadeia se possível
            if self._proximo_handler:
                self._proximo_handler.processar(mensagem)
    
    def _deve_processar(self, mensagem: MensagemLog) -> bool:
        """
        Determina se este handler deve processar a mensagem
        
        RESPONSABILIDADES:
        - Verificar nível mínimo
        - Verificar se handler está ativo
        - Aplicar filtros específicos
        """
        if not self._configuracao.ativo:
            return False
        
        if mensagem.nivel.value < self._configuracao.nivel_minimo.value:
            return False
        
        return self._filtro_especifico(mensagem)
    
    def _filtro_especifico(self, mensagem: MensagemLog) -> bool:
        """Filtro específico do handler - pode ser sobrescrito"""
        return True
    
    @abstractmethod
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Processamento específico do handler - deve ser implementado"""
        pass
    
    def _tratar_erro(self, mensagem: MensagemLog, erro: Exception) -> None:
        """Tratamento padrão de erros - pode ser sobrescrito"""
        print(f"ERRO no handler {self.__class__.__name__}: {erro}")
    
    @property
    def configuracao(self) -> ConfiguracaoHandler:
        """Acesso à configuração do handler"""
        return self._configuracao


# =============================================================================
# FORMATADORES - STRATEGY PATTERN
# =============================================================================

class FormatadorPadrao:
    """
    Formatador padrão para mensagens de log
    
    RESPONSABILIDADES:
    - Formatar mensagens em formato legível
    - Incluir informações essenciais
    """
    
    def formatar(self, mensagem: MensagemLog) -> str:
        """Formato: [TIMESTAMP] [NÍVEL] [THREAD] [ORIGEM] MENSAGEM"""
        timestamp_str = mensagem.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        origem_str = f"[{mensagem.origem}]" if mensagem.origem else ""
        
        return (f"[{timestamp_str}] [{mensagem.nivel.name}] "
                f"[Thread-{mensagem.thread_id}] {origem_str} {mensagem.mensagem}")


class FormatadorJSON:
    """
    Formatador JSON para integração com sistemas externos
    
    RESPONSABILIDADES:
    - Serializar mensagens em JSON
    - Incluir metadados estruturados
    """
    
    def formatar(self, mensagem: MensagemLog) -> str:
        """Formato JSON estruturado"""
        data = {
            "timestamp": mensagem.timestamp.isoformat(),
            "level": mensagem.nivel.name,
            "message": mensagem.mensagem,
            "thread_id": mensagem.thread_id,
            "source": mensagem.origem,
            "context": mensagem.contexto
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


class FormatadorSimples:
    """
    Formatador simplificado para console
    
    RESPONSABILIDADES:
    - Formato mínimo para visualização rápida
    - Reduzir ruído visual
    """
    
    def formatar(self, mensagem: MensagemLog) -> str:
        """Formato simples: NÍVEL: MENSAGEM"""
        return f"{mensagem.nivel.name}: {mensagem.mensagem}"


class FormatadorDetalhado:
    """
    Formatador detalhado para debugging
    
    RESPONSABILIDADES:
    - Incluir todas as informações disponíveis
    - Facilitar debugging e análise
    """
    
    def formatar(self, mensagem: MensagemLog) -> str:
        """Formato detalhado com contexto completo"""
        base = FormatadorPadrao().formatar(mensagem)
        
        if mensagem.contexto:
            contexto_str = json.dumps(mensagem.contexto, ensure_ascii=False)
            base += f" | Contexto: {contexto_str}"
        
        return base


# =============================================================================
# HANDLERS CONCRETOS
# =============================================================================

class HandlerConsole(HandlerLogBase):
    """
    Handler para saída no console
    
    RESPONSABILIDADES:
    - Exibir logs no terminal
    - Aplicar cores por nível (opcional)
    - Suportar diferentes formatos
    """
    
    # Códigos ANSI para cores
    CORES = {
        NivelLog.DEBUG: '\033[36m',    # Ciano
        NivelLog.INFO: '\033[32m',     # Verde
        NivelLog.WARNING: '\033[33m',  # Amarelo
        NivelLog.ERROR: '\033[31m',    # Vermelho
        NivelLog.CRITICAL: '\033[35m'  # Magenta
    }
    RESET = '\033[0m'
    
    def __init__(self, configuracao: ConfiguracaoHandler):
        super().__init__(configuracao)
        self._usar_cores = configuracao.parametros.get('usar_cores', True)
    
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Exibe mensagem no console com cores opcionais"""
        conteudo = self._formatador.formatar(mensagem)
        
        if self._usar_cores and hasattr(os, 'name') and os.name != 'nt':
            cor = self.CORES.get(mensagem.nivel, '')
            conteudo = f"{cor}{conteudo}{self.RESET}"
        
        print(conteudo)


class HandlerArquivo(HandlerLogBase):
    """
    Handler para escrita em arquivo
    
    RESPONSABILIDADES:
    - Persistir logs em arquivo
    - Gerenciar rotação de arquivos
    - Garantir thread-safety
    """
    
    def __init__(self, configuracao: ConfiguracaoHandler):
        super().__init__(configuracao)
        self._caminho_arquivo = configuracao.parametros.get(
            'caminho', 'logs/aplicacao.log'
        )
        self._max_tamanho = configuracao.parametros.get(
            'max_tamanho_mb', 10
        ) * 1024 * 1024  # Converter para bytes
        self._max_arquivos = configuracao.parametros.get('max_arquivos', 5)
        self._lock = threading.Lock()
        
        # Criar diretório se não existir
        Path(self._caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)
    
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Escreve mensagem no arquivo com thread-safety"""
        conteudo = self._formatador.formatar(mensagem)
        
        with self._lock:
            # Verificar se precisa rotacionar
            if self._precisa_rotacionar():
                self._rotacionar_arquivo()
            
            # Escrever no arquivo
            with open(self._caminho_arquivo, 'a', encoding='utf-8') as arquivo:
                arquivo.write(conteudo + '\n')
                arquivo.flush()
    
    def _precisa_rotacionar(self) -> bool:
        """Verifica se o arquivo precisa ser rotacionado"""
        try:
            return os.path.getsize(self._caminho_arquivo) > self._max_tamanho
        except FileNotFoundError:
            return False
    
    def _rotacionar_arquivo(self) -> None:
        """Rotaciona arquivos de log"""
        try:
            # Mover arquivos existentes
            for i in range(self._max_arquivos - 1, 0, -1):
                arquivo_antigo = f"{self._caminho_arquivo}.{i}"
                arquivo_novo = f"{self._caminho_arquivo}.{i + 1}"
                
                if os.path.exists(arquivo_antigo):
                    if i == self._max_arquivos - 1:
                        os.remove(arquivo_antigo)  # Remover o mais antigo
                    else:
                        os.rename(arquivo_antigo, arquivo_novo)
            
            # Renomear arquivo atual
            if os.path.exists(self._caminho_arquivo):
                os.rename(self._caminho_arquivo, f"{self._caminho_arquivo}.1")
                
        except OSError as e:
            print(f"Erro na rotação de arquivo: {e}")


class HandlerEmail(HandlerLogBase):
    """
    Handler para envio de logs por email
    
    RESPONSABILIDADES:
    - Enviar logs críticos por email
    - Gerenciar configurações SMTP
    - Implementar throttling para evitar spam
    """
    
    def __init__(self, configuracao: ConfiguracaoHandler):
        super().__init__(configuracao)
        self._smtp_server = configuracao.parametros.get('smtp_server', 'localhost')
        self._smtp_port = configuracao.parametros.get('smtp_port', 587)
        self._usuario = configuracao.parametros.get('usuario', '')
        self._senha = configuracao.parametros.get('senha', '')
        self._destinatarios = configuracao.parametros.get('destinatarios', [])
        self._remetente = configuracao.parametros.get('remetente', 'system@empresa.com')
        
        # Throttling para evitar spam
        self._ultimo_envio = {}
        self._intervalo_minimo = configuracao.parametros.get('intervalo_minimo_segundos', 300)
    
    def _filtro_especifico(self, mensagem: MensagemLog) -> bool:
        """Só processa logs críticos ou de erro"""
        return mensagem.nivel.value >= NivelLog.ERROR.value
    
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Envia email se não estiver em throttling"""
        if self._em_throttling(mensagem):
            return
        
        try:
            self._enviar_email(mensagem)
            self._registrar_envio(mensagem)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
    def _em_throttling(self, mensagem: MensagemLog) -> bool:
        """Verifica se está em período de throttling"""
        chave = f"{mensagem.nivel.name}:{mensagem.origem}"
        ultimo = self._ultimo_envio.get(chave, 0)
        agora = time.time()
        
        return (agora - ultimo) < self._intervalo_minimo
    
    def _registrar_envio(self, mensagem: MensagemLog) -> None:
        """Registra timestamp do último envio"""
        chave = f"{mensagem.nivel.name}:{mensagem.origem}"
        self._ultimo_envio[chave] = time.time()
    
    def _enviar_email(self, mensagem: MensagemLog) -> None:
        """Envia email usando SMTP"""
        if not self._destinatarios:
            return
        
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = self._remetente
        msg['To'] = ', '.join(self._destinatarios)
        msg['Subject'] = f"[{mensagem.nivel.name}] Log do Sistema"
        
        corpo = self._formatador.formatar(mensagem)
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        # Enviar
        with smtplib.SMTP(self._smtp_server, self._smtp_port) as servidor:
            if self._usuario and self._senha:
                servidor.starttls()
                servidor.login(self._usuario, self._senha)
            
            servidor.send_message(msg)


class HandlerDatabase(HandlerLogBase):
    """
    Handler para persistência em banco de dados
    
    RESPONSABILIDADES:
    - Armazenar logs estruturados
    - Otimizar inserções em lote
    - Gerenciar conexões de forma eficiente
    """
    
    def __init__(self, configuracao: ConfiguracaoHandler):
        super().__init__(configuracao)
        self._repositorio: Optional[IRepositorioLog] = None
        self._buffer: List[MensagemLog] = []
        self._tamanho_lote = configuracao.parametros.get('tamanho_lote', 100)
        self._timeout_lote = configuracao.parametros.get('timeout_lote_segundos', 30)
        self._lock = threading.Lock()
        self._ultimo_flush = time.time()
    
    def definir_repositorio(self, repositorio: IRepositorioLog) -> None:
        """Define o repositório para persistência"""
        self._repositorio = repositorio
    
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Adiciona mensagem ao buffer para processamento em lote"""
        if not self._repositorio:
            return
        
        with self._lock:
            self._buffer.append(mensagem)
            
            # Verificar se deve fazer flush
            if (len(self._buffer) >= self._tamanho_lote or 
                time.time() - self._ultimo_flush > self._timeout_lote):
                self._flush_buffer()
    
    def _flush_buffer(self) -> None:
        """Persiste todas as mensagens do buffer"""
        if not self._buffer or not self._repositorio:
            return
        
        try:
            for mensagem in self._buffer:
                conteudo = self._formatador.formatar(mensagem)
                self._repositorio.salvar(mensagem, conteudo)
            
            self._buffer.clear()
            self._ultimo_flush = time.time()
            
        except Exception as e:
            print(f"Erro ao persistir logs: {e}")
            # Em caso de erro, manter buffer para retry
    
    def finalizar(self) -> None:
        """Força flush do buffer ao finalizar"""
        with self._lock:
            self._flush_buffer()


class HandlerAssincrono(HandlerLogBase):
    """
    Handler que processa logs assincronamente
    
    RESPONSABILIDADES:
    - Processar logs em thread separada
    - Evitar bloqueio da aplicação principal
    - Gerenciar queue de mensagens
    """
    
    def __init__(self, configuracao: ConfiguracaoHandler, handler_destino: HandlerLogBase):
        super().__init__(configuracao)
        self._handler_destino = handler_destino
        self._queue: queue.Queue = queue.Queue(
            maxsize=configuracao.parametros.get('max_queue_size', 1000)
        )
        self._thread_worker: Optional[threading.Thread] = None
        self._executando = False
        self._iniciar_worker()
    
    def _iniciar_worker(self) -> None:
        """Inicia thread worker para processamento assíncrono"""
        self._executando = True
        self._thread_worker = threading.Thread(
            target=self._processar_queue,
            daemon=True
        )
        self._thread_worker.start()
    
    def _processar_interno(self, mensagem: MensagemLog) -> None:
        """Adiciona mensagem à queue para processamento assíncrono"""
        try:
            self._queue.put_nowait(mensagem)
        except queue.Full:
            print("AVISO: Queue de log assíncrono cheia, descartando mensagem")
    
    def _processar_queue(self) -> None:
        """Worker thread que processa mensagens da queue"""
        while self._executando:
            try:
                # Timeout para permitir verificação de _executando
                mensagem = self._queue.get(timeout=1.0)
                self._handler_destino._processar_interno(mensagem)
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no processamento assíncrono: {e}")
    
    def finalizar(self) -> None:
        """Finaliza processamento assíncrono graciosamente"""
        self._executando = False
        
        if self._thread_worker and self._thread_worker.is_alive():
            self._thread_worker.join(timeout=5.0)
        
        # Processar mensagens restantes
        while not self._queue.empty():
            try:
                mensagem = self._queue.get_nowait()
                self._handler_destino._processar_interno(mensagem)
            except queue.Empty:
                break


# =============================================================================
# FACTORIES E BUILDERS
# =============================================================================

class FabricaHandlers:
    """
    Factory para criação de handlers
    
    RESPONSABILIDADES:
    - Centralizar criação de handlers
    - Aplicar configurações padrão
    - Facilitar extensibilidade
    """
    
    @staticmethod
    def criar_console(
        nivel_minimo: NivelLog = NivelLog.INFO,
        usar_cores: bool = True,
        formatador: str = "padrao"
    ) -> HandlerConsole:
        """Cria handler de console com configurações padrão"""
        config = ConfiguracaoHandler(
            tipo=TipoHandler.CONSOLE,
            nivel_minimo=nivel_minimo,
            formatador=formatador,
            parametros={'usar_cores': usar_cores}
        )
        return HandlerConsole(config)
    
    @staticmethod
    def criar_arquivo(
        caminho: str = "logs/aplicacao.log",
        nivel_minimo: NivelLog = NivelLog.DEBUG,
        max_tamanho_mb: int = 10,
        max_arquivos: int = 5,
        formatador: str = "detalhado"
    ) -> HandlerArquivo:
        """Cria handler de arquivo com configurações padrão"""
        config = ConfiguracaoHandler(
            tipo=TipoHandler.ARQUIVO,
            nivel_minimo=nivel_minimo,
            formatador=formatador,
            parametros={
                'caminho': caminho,
                'max_tamanho_mb': max_tamanho_mb,
                'max_arquivos': max_arquivos
            }
        )
        return HandlerArquivo(config)
    
    @staticmethod
    def criar_email(
        destinatarios: List[str],
        smtp_server: str = "localhost",
        smtp_port: int = 587,
        usuario: str = "",
        senha: str = "",
        remetente: str = "system@empresa.com",
        nivel_minimo: NivelLog = NivelLog.ERROR,
        intervalo_minimo_segundos: int = 300
    ) -> HandlerEmail:
        """Cria handler de email com configurações padrão"""
        config = ConfiguracaoHandler(
            tipo=TipoHandler.EMAIL,
            nivel_minimo=nivel_minimo,
            formatador="detalhado",
            parametros={
                'destinatarios': destinatarios,
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'usuario': usuario,
                'senha': senha,
                'remetente': remetente,
                'intervalo_minimo_segundos': intervalo_minimo_segundos
            }
        )
        return HandlerEmail(config)


class ConstrutorCadeiaLog:
    """
    Builder para construção fluente de cadeias de handlers
    
    RESPONSABILIDADES:
    - Facilitar construção de cadeias complexas
    - Prover interface fluente
    - Gerenciar formatadores e configurações
    """
    
    def __init__(self):
        self._handlers: List[HandlerLogBase] = []
        self._formatadores: Dict[str, IFormatadorLog] = {
            'padrao': FormatadorPadrao(),
            'json': FormatadorJSON(),
            'simples': FormatadorSimples(),
            'detalhado': FormatadorDetalhado()
        }
    
    def adicionar_console(
        self, 
        nivel: NivelLog = NivelLog.INFO,
        formatador: str = "simples",
        **kwargs
    ) -> 'ConstrutorCadeiaLog':
        """Adiciona handler de console à cadeia"""
        handler = FabricaHandlers.criar_console(nivel, **kwargs)
        handler.definir_formatador(self._formatadores[formatador])
        self._handlers.append(handler)
        return self
    
    def adicionar_arquivo(
        self,
        caminho: str,
        nivel: NivelLog = NivelLog.DEBUG,
        formatador: str = "detalhado",
        **kwargs
    ) -> 'ConstrutorCadeiaLog':
        """Adiciona handler de arquivo à cadeia"""
        handler = FabricaHandlers.criar_arquivo(caminho, nivel, **kwargs)
        handler.definir_formatador(self._formatadores[formatador])
        self._handlers.append(handler)
        return self
    
    def adicionar_email(
        self,
        destinatarios: List[str],
        nivel: NivelLog = NivelLog.ERROR,
        formatador: str = "detalhado",
        **kwargs
    ) -> 'ConstrutorCadeiaLog':
        """Adiciona handler de email à cadeia"""
        handler = FabricaHandlers.criar_email(destinatarios, nivel, **kwargs)
        handler.definir_formatador(self._formatadores[formatador])
        self._handlers.append(handler)
        return self
    
    def adicionar_customizado(self, handler: HandlerLogBase) -> 'ConstrutorCadeiaLog':
        """Adiciona handler customizado à cadeia"""
        self._handlers.append(handler)
        return self
    
    def construir(self) -> Optional[HandlerLogBase]:
        """Constrói a cadeia de handlers"""
        if not self._handlers:
            return None
        
        # Conectar handlers em cadeia
        for i in range(len(self._handlers) - 1):
            self._handlers[i].definir_proximo(self._handlers[i + 1])
        
        return self._handlers[0]


# =============================================================================
# SISTEMA PRINCIPAL DE LOGGING
# =============================================================================

class SistemaLog:
    """
    Sistema principal de logging
    
    RESPONSABILIDADES:
    - Gerenciar cadeia de handlers
    - Prover interface simples para aplicação
    - Gerenciar métricas e monitoramento
    - Implementar padrão Singleton (opcional)
    """
    
    def __init__(self, cadeia_handlers: Optional[HandlerLogBase] = None):
        self._cadeia_handlers = cadeia_handlers
        self._metricas: Optional[IMetricasLog] = None
        self._notificador_critico: Optional[INotificadorCritico] = None
        
        # Cache de loggers por origem
        self._loggers_cache: Dict[str, 'Logger'] = {}
    
    def definir_cadeia_handlers(self, cadeia: HandlerLogBase) -> None:
        """Define a cadeia de handlers"""
        self._cadeia_handlers = cadeia
    
    def definir_metricas(self, metricas: IMetricasLog) -> None:
        """Define sistema de métricas"""
        self._metricas = metricas
        
        # Propagar para todos os handlers
        handler_atual = self._cadeia_handlers
        while handler_atual:
            handler_atual.definir_metricas(metricas)
            handler_atual = handler_atual._proximo_handler
    
    def definir_notificador_critico(self, notificador: INotificadorCritico) -> None:
        """Define notificador para logs críticos"""
        self._notificador_critico = notificador
    
    def obter_logger(self, origem: str = "") -> 'Logger':
        """
        Obtém logger específico para uma origem
        
        RESPONSABILIDADES:
        - Cache de loggers por origem
        - Prover interface específica
        """
        if origem not in self._loggers_cache:
            self._loggers_cache[origem] = Logger(self, origem)
        
        return self._loggers_cache[origem]
    
    def processar_mensagem(self, mensagem: MensagemLog) -> None:
        """
        Processa mensagem através da cadeia de handlers
        
        RESPONSABILIDADES:
        - Validar mensagem
        - Iniciar processamento na cadeia
        - Notificar sobre logs críticos
        """
        if not self._cadeia_handlers:
            return
        
        try:
            # Processar através da cadeia
            self._cadeia_handlers.processar(mensagem)
            
            # Notificar se crítico
            if (mensagem.nivel == NivelLog.CRITICAL and 
                self._notificador_critico):
                self._notificador_critico.notificar_critico(mensagem)
                
        except Exception as e:
            print(f"Erro no sistema de log: {e}")
    
    def finalizar(self) -> None:
        """Finaliza sistema graciosamente"""
        handler_atual = self._cadeia_handlers
        while handler_atual:
            if hasattr(handler_atual, 'finalizar'):
                handler_atual.finalizar()
            handler_atual = handler_atual._proximo_handler


class Logger:
    """
    Interface específica para logging por origem
    
    RESPONSABILIDADES:
    - Prover métodos convenientes por nível
    - Adicionar contexto automático
    - Facilitar uso da aplicação
    """
    
    def __init__(self, sistema: SistemaLog, origem: str):
        self._sistema = sistema
        self._origem = origem
        self._contexto_base: Dict[str, Any] = {}
    
    def definir_contexto_base(self, contexto: Dict[str, Any]) -> None:
        """Define contexto que será incluído em todas as mensagens"""
        self._contexto_base = contexto.copy()
    
    def debug(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """Log de debug"""
        self._log(NivelLog.DEBUG, mensagem, contexto)
    
    def info(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """Log informativo"""
        self._log(NivelLog.INFO, mensagem, contexto)
    
    def warning(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """Log de aviso"""
        self._log(NivelLog.WARNING, mensagem, contexto)
    
    def error(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """Log de erro"""
        self._log(NivelLog.ERROR, mensagem, contexto)
    
    def critical(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """Log crítico"""
        self._log(NivelLog.CRITICAL, mensagem, contexto)
    
    def _log(self, nivel: NivelLog, mensagem: str, contexto: Optional[Dict[str, Any]]) -> None:
        """Método interno para criação e processamento de mensagens"""
        contexto_final = self._contexto_base.copy()
        if contexto:
            contexto_final.update(contexto)
        
        mensagem_log = MensagemLog(
            nivel=nivel,
            mensagem=mensagem,
            origem=self._origem,
            contexto=contexto_final
        )
        
        self._sistema.processar_mensagem(mensagem_log)


# =============================================================================
# IMPLEMENTAÇÕES DE APOIO
# =============================================================================

class MetricasLogMemoria:
    """
    Implementação em memória para coleta de métricas
    
    RESPONSABILIDADES:
    - Coletar estatísticas de uso
    - Manter contadores por nível e handler
    - Prover relatórios de performance
    """
    
    def __init__(self):
        self._contadores: Dict[str, int] = {}
        self._tempos_processamento: List[float] = []
        self._lock = threading.Lock()
    
    def registrar_processamento(self, mensagem: MensagemLog, handler: str) -> None:
        """Registra que uma mensagem foi processada"""
        with self._lock:
            # Contador por nível
            chave_nivel = f"nivel_{mensagem.nivel.name}"
            self._contadores[chave_nivel] = self._contadores.get(chave_nivel, 0) + 1
            
            # Contador por handler
            chave_handler = f"handler_{handler}"
            self._contadores[chave_handler] = self._contadores.get(chave_handler, 0) + 1
            
            # Contador geral
            self._contadores['total'] = self._contadores.get('total', 0) + 1
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas coletadas"""
        with self._lock:
            stats = self._contadores.copy()
            
            if self._tempos_processamento:
                stats['tempo_medio_ms'] = sum(self._tempos_processamento) / len(self._tempos_processamento) * 1000
                stats['tempo_max_ms'] = max(self._tempos_processamento) * 1000
            
            return stats


class NotificadorCriticoConsole:
    """
    Notificador simples que exibe alertas no console
    
    RESPONSABILIDADES:
    - Notificação visual de logs críticos
    - Alertas imediatos para desenvolvedores
    """
    
    def notificar_critico(self, mensagem: MensagemLog) -> None:
        """Exibe alerta crítico no console"""
        print("\n" + "="*60)
        print("🚨 ALERTA CRÍTICO - SISTEMA DE LOG 🚨")
        print("="*60)
        print(f"Timestamp: {mensagem.timestamp}")
        print(f"Origem: {mensagem.origem}")
        print(f"Mensagem: {mensagem.mensagem}")
        if mensagem.contexto:
            print(f"Contexto: {json.dumps(mensagem.contexto, indent=2)}")
        print("="*60 + "\n")


# =============================================================================
# FUNÇÃO PRINCIPAL E DEMONSTRAÇÕES
# =============================================================================

def demonstrar_sistema_logging():
    """
    Demonstração completa do sistema de logging
    
    OBJETIVOS:
    - Mostrar configuração de cadeia complexa
    - Demonstrar diferentes handlers
    - Exibir flexibilidade do sistema
    - Validar princípios SOLID
    """
    
    print("🔧 SISTEMA DE LOGGING - CHAIN OF RESPONSIBILITY")
    print("=" * 60)
    print("Demonstrando padrão Chain of Responsibility em sistema de logging")
    print("Princípios SOLID aplicados:")
    print("• SRP: Cada handler tem responsabilidade específica")
    print("• OCP: Extensível para novos handlers")
    print("• LSP: Handlers podem ser substituídos")
    print("• ISP: Interfaces segregadas por funcionalidade")
    print("• DIP: Depende de abstrações, não implementações")
    print("=" * 60)
    
    # 1. Construir cadeia de handlers usando Builder Pattern
    print("\n📋 1. CONSTRUINDO CADEIA DE HANDLERS")
    print("-" * 40)
    
    cadeia = (ConstrutorCadeiaLog()
              .adicionar_console(
                  nivel=NivelLog.INFO,
                  formatador="simples",
                  usar_cores=True
              )
              .adicionar_arquivo(
                  caminho="logs/aplicacao.log",
                  nivel=NivelLog.DEBUG,
                  formatador="detalhado",
                  max_tamanho_mb=5
              )
              .adicionar_arquivo(
                  caminho="logs/erros.log",
                  nivel=NivelLog.ERROR,
                  formatador="json",
                  max_tamanho_mb=2
              )
              .construir())
    
    print("✅ Cadeia construída:")
    print("   Console (INFO+) → Arquivo Geral (DEBUG+) → Arquivo Erros (ERROR+)")
    
    # 2. Configurar sistema principal
    print("\n⚙️ 2. CONFIGURANDO SISTEMA PRINCIPAL")
    print("-" * 40)
    
    sistema = SistemaLog(cadeia)
    
    # Adicionar métricas
    metricas = MetricasLogMemoria()
    sistema.definir_metricas(metricas)
    
    # Adicionar notificador crítico
    notificador = NotificadorCriticoConsole()
    sistema.definir_notificador_critico(notificador)
    
    print("✅ Sistema configurado com:")
    print("   • Métricas em memória")
    print("   • Notificador crítico no console")
    
    # 3. Demonstrar uso com diferentes origens
    print("\n📝 3. DEMONSTRANDO LOGGING POR MÓDULOS")
    print("-" * 40)
    
    # Logger para módulo de autenticação
    logger_auth = sistema.obter_logger("auth")
    logger_auth.definir_contexto_base({"modulo": "autenticacao", "versao": "1.0"})
    
    # Logger para módulo de pagamento
    logger_payment = sistema.obter_logger("payment")
    logger_payment.definir_contexto_base({"modulo": "pagamento", "versao": "2.1"})
    
    # Logger para módulo de database
    logger_db = sistema.obter_logger("database")
    logger_db.definir_contexto_base({"modulo": "database", "versao": "1.5"})
    
    print("✅ Loggers criados para diferentes módulos")
    
    # 4. Simular cenários de uso
    print("\n🎬 4. SIMULANDO CENÁRIOS DE USO")
    print("-" * 40)
    
    # Cenário 1: Fluxo normal de autenticação
    print("\n📋 Cenário 1: Fluxo de Autenticação")
    logger_auth.info("Iniciando processo de autenticação", {
        "usuario": "usuario123",
        "ip": "192.168.1.100"
    })
    
    logger_auth.debug("Validando credenciais", {
        "usuario": "usuario123",
        "metodo": "password"
    })
    
    logger_auth.info("Autenticação realizada com sucesso", {
        "usuario": "usuario123",
        "sessao_id": "sess_abc123"
    })
    
    # Cenário 2: Erro no processamento de pagamento
    print("\n💳 Cenário 2: Erro no Pagamento")
    logger_payment.info("Iniciando processamento de pagamento", {
        "pedido_id": "order_456",
        "valor": "R$ 299,90",
        "metodo": "cartao_credito"
    })
    
    logger_payment.warning("Tentativa de pagamento rejeitada", {
        "pedido_id": "order_456",
        "motivo": "cartao_expirado",
        "tentativa": 1
    })
    
    logger_payment.error("Falha no processamento após múltiplas tentativas", {
        "pedido_id": "order_456",
        "tentativas": 3,
        "ultimo_erro": "gateway_timeout"
    })
    
    # Cenário 3: Problema crítico no banco
    print("\n🗄️ Cenário 3: Problema Crítico no Banco")
    logger_db.info("Executando backup noturno", {
        "tipo": "backup_completo",
        "inicio": datetime.now().isoformat()
    })
    
    logger_db.warning("Conexão instável detectada", {
        "host": "db-server-01",
        "tentativas_reconexao": 5
    })
    
    logger_db.critical("FALHA CRÍTICA: Perda de conexão com banco principal", {
        "host": "db-server-01",
        "erro": "connection_timeout",
        "impacto": "sistema_indisponivel",
        "acao_necessaria": "verificar_infraestrutura"
    })
    
    # 5. Demonstrar handlers especiais
    print("\n🔧 5. DEMONSTRANDO HANDLERS ESPECIAIS")
    print("-" * 40)
    
    # Handler assíncrono
    handler_async_console = HandlerAssincrono(
        ConfiguracaoHandler(
            tipo=TipoHandler.CONSOLE,
            parametros={'max_queue_size': 100}
        ),
        FabricaHandlers.criar_console(formatador="simples")
    )
    
    print("✅ Handler assíncrono criado")
    
    # Simular carga alta
    print("📊 Simulando processamento assíncrono...")
    for i in range(5):
        mensagem = MensagemLog(
            nivel=NivelLog.INFO,
            mensagem=f"Processamento assíncrono #{i+1}",
            origem="async_test"
        )
        handler_async_console._processar_interno(mensagem)
    
    # Aguardar processamento
    time.sleep(0.5)
    handler_async_console.finalizar()
    
    # 6. Exibir métricas
    print("\n📊 6. MÉTRICAS DO SISTEMA")
    print("-" * 40)
    
    stats = metricas.obter_estatisticas()
    for chave, valor in stats.items():
        print(f"   {chave}: {valor}")
    
    # 7. Demonstrar flexibilidade - adicionar handler dinamicamente
    print("\n🔌 7. EXTENSIBILIDADE - NOVO HANDLER")
    print("-" * 40)
    
    class HandlerWebhook(HandlerLogBase):
        """Handler customizado para webhook"""
        
        def _processar_interno(self, mensagem: MensagemLog) -> None:
            if mensagem.nivel.value >= NivelLog.ERROR.value:
                print(f"🌐 WEBHOOK: Enviando para endpoint externo: {mensagem.mensagem}")
    
    # Adicionar à cadeia existente
    handler_webhook = HandlerWebhook(
        ConfiguracaoHandler(
            tipo=TipoHandler.WEBHOOK,
            nivel_minimo=NivelLog.ERROR
        )
    )
    
    # Encontrar último handler da cadeia e adicionar webhook
    handler_atual = cadeia
    while handler_atual._proximo_handler:
        handler_atual = handler_atual._proximo_handler
    handler_atual.definir_proximo(handler_webhook)
    
    print("✅ Handler webhook adicionado dinamicamente")
    
    # Testar novo handler
    logger_auth.error("Teste do novo handler webhook", {
        "teste": True,
        "handler": "webhook"
    })
    
    # 8. Finalização
    print("\n🏁 8. FINALIZANDO SISTEMA")
    print("-" * 40)
    
    sistema.finalizar()
    print("✅ Sistema finalizado graciosamente")
    
    # 9. Resumo dos padrões demonstrados
    print("\n📋 PADRÕES E PRINCÍPIOS DEMONSTRADOS")
    print("=" * 60)
    print("🔗 Chain of Responsibility:")
    print("   • Cadeia de handlers processando mensagens")
    print("   • Cada handler decide se processa e passa adiante")
    print("   • Flexibilidade para adicionar/remover handlers")
    
    print("\n📋 Template Method:")
    print("   • HandlerLogBase define algoritmo geral")
    print("   • Subclasses implementam passos específicos")
    print("   • Reutilização de código comum")
    
    print("\n🎯 Strategy Pattern:")
    print("   • Diferentes formatadores intercambiáveis")
    print("   • Algoritmos de formatação encapsulados")
    print("   • Seleção dinâmica de estratégia")
    
    print("\n🏭 Factory Pattern:")
    print("   • FabricaHandlers centraliza criação")
    print("   • Configurações padrão aplicadas")
    print("   • Facilita manutenção e extensão")
    
    print("\n🔨 Builder Pattern:")
    print("   • ConstrutorCadeiaLog para construção fluente")
    print("   • Interface intuitiva para configuração")
    print("   • Flexibilidade na composição")
    
    print("\n📐 Princípios SOLID:")
    print("   • SRP: Cada classe tem responsabilidade única")
    print("   • OCP: Extensível sem modificar código existente")
    print("   • LSP: Handlers substituíveis transparentemente")
    print("   • ISP: Interfaces específicas e focadas")
    print("   • DIP: Dependências invertidas via interfaces")


if __name__ == "__main__":
    demonstrar_sistema_logging()
