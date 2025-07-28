#!/usr/bin/env python3
"""
INFRASTRUCTURE LAYER - ADAPTERS
Sistema Bancário - Arquitetura Hexagonal

Este módulo implementa os adapters (implementações concretas) para as 
interfaces definidas na camada de aplicação, seguindo o padrão Hexagonal.

RESPONSABILIDADES:
- Implementar repositórios em memória e persistentes
- Adapters para serviços externos
- Notificadores e validadores
- Métricas e auditoria

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

import json
import sqlite3
import smtplib
import time
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Callable
from uuid import UUID
from email.mime.text import MIMEText
from pathlib import Path
import threading
from collections import defaultdict

# Imports do domínio
from domain import (
    Cliente, Conta, Transacao, CPF, Dinheiro, EventoDominio,
    IRepositorioCliente, IRepositorioConta, IRepositorioTransacao,
    IProcessadorEventos, INotificadorTransacao, IValidadorFraude,
    IConsultorCreditoExterno, TipoTransacao, StatusTransacao
)


# =============================================================================
# REPOSITÓRIOS EM MEMÓRIA (Para desenvolvimento/testes)
# =============================================================================

class RepositorioClienteMemoria:
    """
    Repositório em memória para clientes
    
    RESPONSABILIDADES:
    - Armazenar clientes em memória
    - Implementar buscas eficientes
    - Simular persistência para testes
    """
    
    def __init__(self):
        self._clientes: Dict[UUID, Cliente] = {}
        self._indice_cpf: Dict[str, UUID] = {}
        self._indice_email: Dict[str, UUID] = {}
        self._lock = threading.RLock()
    
    def salvar(self, cliente: Cliente) -> None:
        """Salva cliente em memória"""
        with self._lock:
            self._clientes[cliente.id] = cliente
            self._indice_cpf[cliente.cpf.limpo] = cliente.id
            self._indice_email[cliente.email] = cliente.id
    
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """Busca cliente por ID"""
        with self._lock:
            return self._clientes.get(id)
    
    def buscar_por_cpf(self, cpf: CPF) -> Optional[Cliente]:
        """Busca cliente por CPF"""
        with self._lock:
            cliente_id = self._indice_cpf.get(cpf.limpo)
            return self._clientes.get(cliente_id) if cliente_id else None
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        with self._lock:
            cliente_id = self._indice_email.get(email.lower())
            return self._clientes.get(cliente_id) if cliente_id else None
    
    def listar_todos(self) -> List[Cliente]:
        """Lista todos os clientes"""
        with self._lock:
            return list(self._clientes.values())


class RepositorioContaMemoria:
    """
    Repositório em memória para contas
    
    RESPONSABILIDADES:
    - Armazenar contas em memória
    - Implementar buscas por diferentes critérios
    - Manter índices para performance
    """
    
    def __init__(self):
        self._contas: Dict[UUID, Conta] = {}
        self._indice_agencia_numero: Dict[str, UUID] = {}
        self._indice_cliente: Dict[UUID, List[UUID]] = defaultdict(list)
        self._lock = threading.RLock()
    
    def salvar(self, conta: Conta) -> None:
        """Salva conta em memória"""
        with self._lock:
            self._contas[conta.id] = conta
            chave_agencia_numero = f"{conta.agencia}-{conta.numero}"
            self._indice_agencia_numero[chave_agencia_numero] = conta.id
            
            if conta.id not in self._indice_cliente[conta.cliente_id]:
                self._indice_cliente[conta.cliente_id].append(conta.id)
    
    def buscar_por_id(self, id: UUID) -> Optional[Conta]:
        """Busca conta por ID"""
        with self._lock:
            return self._contas.get(id)
    
    def buscar_por_numero(self, agencia: str, numero: str) -> Optional[Conta]:
        """Busca conta por agência e número"""
        with self._lock:
            chave = f"{agencia}-{numero}"
            conta_id = self._indice_agencia_numero.get(chave)
            return self._contas.get(conta_id) if conta_id else None
    
    def listar_por_cliente(self, cliente_id: UUID) -> List[Conta]:
        """Lista contas do cliente"""
        with self._lock:
            conta_ids = self._indice_cliente.get(cliente_id, [])
            return [self._contas[id] for id in conta_ids if id in self._contas]


class RepositorioTransacaoMemoria:
    """
    Repositório em memória para transações
    
    RESPONSABILIDADES:
    - Armazenar transações em memória
    - Implementar buscas por conta e período
    - Manter histórico organizado
    """
    
    def __init__(self):
        self._transacoes: Dict[UUID, Transacao] = {}
        self._indice_conta: Dict[UUID, List[UUID]] = defaultdict(list)
        self._lock = threading.RLock()
    
    def salvar(self, transacao: Transacao) -> None:
        """Salva transação em memória"""
        with self._lock:
            self._transacoes[transacao.id] = transacao
            
            # Indexar por conta origem
            if transacao.conta_origem_id:
                if transacao.id not in self._indice_conta[transacao.conta_origem_id]:
                    self._indice_conta[transacao.conta_origem_id].append(transacao.id)
            
            # Indexar por conta destino
            if transacao.conta_destino_id:
                if transacao.id not in self._indice_conta[transacao.conta_destino_id]:
                    self._indice_conta[transacao.conta_destino_id].append(transacao.id)
    
    def buscar_por_id(self, id: UUID) -> Optional[Transacao]:
        """Busca transação por ID"""
        with self._lock:
            return self._transacoes.get(id)
    
    def listar_por_conta(self, conta_id: UUID, 
                        data_inicio: Optional[datetime] = None,
                        data_fim: Optional[datetime] = None) -> List[Transacao]:
        """Lista transações da conta com filtro de período"""
        with self._lock:
            transacao_ids = self._indice_conta.get(conta_id, [])
            transacoes = [self._transacoes[id] for id in transacao_ids 
                         if id in self._transacoes]
            
            # Aplicar filtros de data
            if data_inicio or data_fim:
                transacoes_filtradas = []
                for t in transacoes:
                    if data_inicio and t.data_criacao < data_inicio:
                        continue
                    if data_fim and t.data_criacao > data_fim:
                        continue
                    transacoes_filtradas.append(t)
                return transacoes_filtradas
            
            return transacoes


# =============================================================================
# REPOSITÓRIOS PERSISTENTES (SQLite)
# =============================================================================

class RepositorioClienteSQLite:
    """
    Repositório SQLite para clientes
    
    RESPONSABILIDADES:
    - Persistir clientes em banco SQLite
    - Implementar mapeamento objeto-relacional
    - Garantir integridade referencial
    """
    
    def __init__(self, caminho_db: str = "banco.db"):
        self._caminho_db = caminho_db
        self._inicializar_db()
    
    def _inicializar_db(self) -> None:
        """Inicializa estrutura do banco"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    endereco_cep TEXT NOT NULL,
                    endereco_logradouro TEXT NOT NULL,
                    endereco_numero TEXT NOT NULL,
                    endereco_complemento TEXT,
                    endereco_bairro TEXT NOT NULL,
                    endereco_cidade TEXT NOT NULL,
                    endereco_uf TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    data_cadastro TEXT NOT NULL,
                    ativo INTEGER NOT NULL DEFAULT 1,
                    perfil_risco TEXT NOT NULL DEFAULT 'BAIXO',
                    pontuacao_credito INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()
    
    def salvar(self, cliente: Cliente) -> None:
        """Salva cliente no banco"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO clientes 
                (id, nome, cpf, endereco_cep, endereco_logradouro, endereco_numero,
                 endereco_complemento, endereco_bairro, endereco_cidade, endereco_uf,
                 telefone, email, data_nascimento, data_cadastro, ativo, 
                 perfil_risco, pontuacao_credito)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(cliente.id), cliente.nome, cliente.cpf.limpo,
                cliente.endereco.cep, cliente.endereco.logradouro, 
                cliente.endereco.numero, cliente.endereco.complemento,
                cliente.endereco.bairro, cliente.endereco.cidade, 
                cliente.endereco.uf, cliente.telefone, cliente.email,
                cliente.data_nascimento.isoformat(),
                datetime.now().isoformat(),  # data_cadastro
                1 if cliente.ativo else 0, cliente.perfil_risco, 0
            ))
            conn.commit()
    
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """Busca cliente por ID"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM clientes WHERE id = ?", (str(id),)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_para_cliente(row)
            return None
    
    def buscar_por_cpf(self, cpf: CPF) -> Optional[Cliente]:
        """Busca cliente por CPF"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM clientes WHERE cpf = ?", (cpf.limpo,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_para_cliente(row)
            return None
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM clientes WHERE email = ?", (email.lower(),)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_para_cliente(row)
            return None
    
    def listar_todos(self) -> List[Cliente]:
        """Lista todos os clientes"""
        with sqlite3.connect(self._caminho_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM clientes ORDER BY nome")
            
            return [self._row_para_cliente(row) for row in cursor.fetchall()]
    
    def _row_para_cliente(self, row: sqlite3.Row) -> Cliente:
        """Converte row do banco para objeto Cliente"""
        from domain import Endereco
        
        endereco = Endereco(
            cep=row['endereco_cep'],
            logradouro=row['endereco_logradouro'],
            numero=row['endereco_numero'],
            complemento=row['endereco_complemento'],
            bairro=row['endereco_bairro'],
            cidade=row['endereco_cidade'],
            uf=row['endereco_uf']
        )
        
        cliente = Cliente(
            nome=row['nome'],
            cpf=CPF(row['cpf']),
            endereco=endereco,
            telefone=row['telefone'],
            email=row['email'],
            data_nascimento=datetime.fromisoformat(row['data_nascimento']),
            id=UUID(row['id'])
        )
        
        # Definir estado interno
        if not row['ativo']:
            cliente.inativar()
        
        cliente.atualizar_perfil_risco(row['perfil_risco'])
        
        return cliente


# =============================================================================
# ADAPTERS PARA SERVIÇOS EXTERNOS
# =============================================================================

class ConsultorCreditoSerasa:
    """
    Adapter para consulta de crédito no Serasa
    
    RESPONSABILIDADES:
    - Simular consultas ao Serasa
    - Mapear respostas para formato interno
    - Tratar timeouts e erros
    """
    
    def __init__(self, timeout_segundos: int = 5):
        self._timeout = timeout_segundos
        # Simulação de base de dados externa
        self._scores_simulados = {}
        self._restricoes_simuladas = {}
    
    def consultar_score(self, cpf: CPF) -> int:
        """Consulta score de crédito simulado"""
        # Simular latência da rede
        time.sleep(0.1)
        
        # Retornar score simulado ou gerar baseado no CPF
        if cpf.limpo in self._scores_simulados:
            return self._scores_simulados[cpf.limpo]
        
        # Gerar score baseado no hash do CPF (determinístico)
        hash_cpf = hash(cpf.limpo)
        score = 300 + (abs(hash_cpf) % 601)  # Entre 300 e 900
        self._scores_simulados[cpf.limpo] = score
        return score
    
    def consultar_restricoes(self, cpf: CPF) -> List[str]:
        """Consulta restrições simuladas"""
        # Simular latência da rede
        time.sleep(0.1)
        
        if cpf.limpo in self._restricoes_simuladas:
            return self._restricoes_simuladas[cpf.limpo]
        
        # Simular algumas restrições baseadas no CPF
        restricoes = []
        if int(cpf.limpo[-1]) % 10 == 0:  # 10% dos CPFs
            restricoes.append("SPC")
        if int(cpf.limpo[-2:]) % 15 == 0:  # ~6% dos CPFs
            restricoes.append("SERASA")
        if int(cpf.limpo[-3:]) % 100 == 0:  # 1% dos CPFs
            restricoes.append("BACEN")
        
        self._restricoes_simuladas[cpf.limpo] = restricoes
        return restricoes
    
    def adicionar_score_customizado(self, cpf: str, score: int) -> None:
        """Adiciona score customizado para testes"""
        self._scores_simulados[cpf] = score
    
    def adicionar_restricao_customizada(self, cpf: str, restricoes: List[str]) -> None:
        """Adiciona restrição customizada para testes"""
        self._restricoes_simuladas[cpf] = restricoes


class ValidadorFraudeInteligente:
    """
    Validador de fraude com algoritmos de detecção
    
    RESPONSABILIDADES:
    - Analisar padrões suspeitos
    - Verificar velocidade de transações
    - Detectar comportamentos anômalos
    - Aplicar machine learning (simulado)
    """
    
    def __init__(self):
        self._historico_transacoes: Dict[UUID, List[datetime]] = defaultdict(list)
        self._valores_suspeitos = [
            Dinheiro(Decimal(str(valor))) for valor in [
                1000.00, 2000.00, 5000.00, 10000.00, 15000.00
            ]
        ]
        self._lock = threading.RLock()
    
    def validar(self, transacao: Transacao, conta: Conta) -> bool:
        """Valida se transação pode ser suspeita de fraude"""
        with self._lock:
            # Regra 1: Valores suspeitos exatos
            if any(transacao.valor == valor for valor in self._valores_suspeitos):
                if random.random() < 0.3:  # 30% de chance de bloquear
                    return False
            
            # Regra 2: Múltiplas transações em pouco tempo
            agora = datetime.now()
            conta_id = conta.id
            
            # Limpar transações antigas (mais de 1 hora)
            self._historico_transacoes[conta_id] = [
                t for t in self._historico_transacoes[conta_id]
                if (agora - t).total_seconds() < 3600
            ]
            
            # Verificar frequência
            transacoes_ultima_hora = len(self._historico_transacoes[conta_id])
            if transacoes_ultima_hora >= 5:  # Mais de 5 transações/hora
                return False
            
            # Regra 3: Transações em horário suspeito (madrugada)
            if 2 <= agora.hour <= 5:  # Entre 2h e 5h da manhã
                if transacao.valor > Dinheiro(1000.00):
                    if random.random() < 0.5:  # 50% de chance de bloquear
                        return False
            
            # Regra 4: Valor muito alto comparado ao histórico
            if transacao.valor > conta.saldo * 0.9:  # Mais de 90% do saldo
                if transacao.valor > Dinheiro(5000.00):
                    return False
            
            # Registrar transação para análise futura
            self._historico_transacoes[conta_id].append(agora)
            
            return True


class NotificadorEmailSMTP:
    """
    Notificador via email usando SMTP
    
    RESPONSABILIDADES:
    - Enviar notificações por email
    - Formatar mensagens de transação
    - Tratar erros de envio
    - Implementar retry logic
    """
    
    def __init__(self, servidor_smtp: str = "localhost", 
                 porta: int = 587,
                 usuario: str = "", 
                 senha: str = ""):
        self._servidor_smtp = servidor_smtp
        self._porta = porta
        self._usuario = usuario
        self._senha = senha
        self._emails_clientes: Dict[UUID, str] = {}
    
    def definir_email_cliente(self, cliente_id: UUID, email: str) -> None:
        """Define email do cliente para notificações"""
        self._emails_clientes[cliente_id] = email
    
    def notificar_transacao_realizada(self, transacao: Transacao, 
                                    conta_origem: Optional[Conta],
                                    conta_destino: Optional[Conta]) -> None:
        """Notifica transação realizada por email"""
        try:
            # Notificar conta origem
            if conta_origem and conta_origem.cliente_id in self._emails_clientes:
                self._enviar_notificacao_origem(transacao, conta_origem)
            
            # Notificar conta destino
            if conta_destino and conta_destino.cliente_id in self._emails_clientes:
                self._enviar_notificacao_destino(transacao, conta_destino)
                
        except Exception as e:
            print(f"Erro ao enviar notificação por email: {e}")
    
    def _enviar_notificacao_origem(self, transacao: Transacao, conta: Conta) -> None:
        """Envia notificação para conta origem"""
        email_destino = self._emails_clientes[conta.cliente_id]
        
        assunto = f"Transação Realizada - {transacao.tipo.value}"
        corpo = f"""
        Prezado cliente,
        
        Uma transação foi realizada em sua conta:
        
        Tipo: {transacao.tipo.value}
        Valor: {transacao.valor.formatado}
        Data: {transacao.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}
        Descrição: {transacao.descricao}
        
        Saldo atual: {conta.saldo.formatado}
        
        Se você não reconhece esta transação, entre em contato conosco imediatamente.
        
        Atenciosamente,
        Banco Digital
        """
        
        self._enviar_email(email_destino, assunto, corpo)
    
    def _enviar_notificacao_destino(self, transacao: Transacao, conta: Conta) -> None:
        """Envia notificação para conta destino"""
        email_destino = self._emails_clientes[conta.cliente_id]
        
        assunto = "Depósito Recebido"
        corpo = f"""
        Prezado cliente,
        
        Você recebeu um depósito em sua conta:
        
        Valor: {transacao.valor.formatado}
        Data: {transacao.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}
        Descrição: {transacao.descricao}
        
        Saldo atual: {conta.saldo.formatado}
        
        Atenciosamente,
        Banco Digital
        """
        
        self._enviar_email(email_destino, assunto, corpo)
    
    def _enviar_email(self, destino: str, assunto: str, corpo: str) -> None:
        """Envia email usando SMTP"""
        # Em ambiente de produção, usaria SMTP real
        # Para demonstração, apenas log
        print(f"📧 EMAIL ENVIADO:")
        print(f"   Para: {destino}")
        print(f"   Assunto: {assunto}")
        print(f"   Corpo: {corpo[:100]}...")


class ProcessadorEventosAssincrono:
    """
    Processador de eventos de domínio assíncrono
    
    RESPONSABILIDADES:
    - Processar eventos em background
    - Implementar retry para falhas
    - Manter log de processamento
    - Garantir entrega eventual
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)
        self._fila_eventos: List[EventoDominio] = []
        self._eventos_processados: List[UUID] = []
        self._eventos_falhou: Dict[UUID, int] = defaultdict(int)
        self._executando = False
        self._thread_worker: Optional[threading.Thread] = None
        self._lock = threading.RLock()
    
    def registrar_handler(self, tipo_evento: str, handler: Callable) -> None:
        """Registra handler para tipo de evento"""
        self._handlers[tipo_evento].append(handler)
    
    def processar(self, evento: EventoDominio) -> None:
        """Adiciona evento à fila de processamento"""
        with self._lock:
            self._fila_eventos.append(evento)
            
            if not self._executando:
                self._iniciar_worker()
    
    def _iniciar_worker(self) -> None:
        """Inicia thread worker para processamento"""
        self._executando = True
        self._thread_worker = threading.Thread(
            target=self._processar_eventos,
            daemon=True
        )
        self._thread_worker.start()
    
    def _processar_eventos(self) -> None:
        """Worker que processa eventos da fila"""
        while self._executando or self._fila_eventos:
            with self._lock:
                if not self._fila_eventos:
                    time.sleep(0.1)
                    continue
                
                evento = self._fila_eventos.pop(0)
            
            try:
                # Verificar se já foi processado
                if evento.id in self._eventos_processados:
                    continue
                
                # Verificar se falhou muitas vezes
                if self._eventos_falhou[evento.id] >= 3:
                    print(f"⚠️ Evento {evento.id} falhou 3 vezes, descartando")
                    continue
                
                # Processar evento
                tipo_evento = evento.__class__.__name__
                handlers = self._handlers.get(tipo_evento, [])
                
                for handler in handlers:
                    handler(evento)
                
                # Marcar como processado
                self._eventos_processados.append(evento.id)
                print(f"✅ Evento processado: {tipo_evento}")
                
            except Exception as e:
                print(f"❌ Erro ao processar evento {evento.id}: {e}")
                self._eventos_falhou[evento.id] += 1
                
                # Recolocar na fila para retry
                with self._lock:
                    self._fila_eventos.append(evento)
    
    def parar(self) -> None:
        """Para o processamento de eventos"""
        self._executando = False
        if self._thread_worker:
            self._thread_worker.join(timeout=5)


# =============================================================================
# MÉTRICAS E AUDITORIA
# =============================================================================

class ColetorMetricasBanco:
    """
    Coletor de métricas do sistema bancário
    
    RESPONSABILIDADES:
    - Coletar métricas de performance
    - Manter estatísticas de uso
    - Gerar relatórios
    - Monitorar SLAs
    """
    
    def __init__(self):
        self._metricas: Dict[str, Any] = defaultdict(int)
        self._tempos_operacao: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.RLock()
        self._inicio_coleta = datetime.now()
    
    def registrar_operacao(self, operacao: str, tempo_ms: float, sucesso: bool = True) -> None:
        """Registra métricas de operação"""
        with self._lock:
            self._metricas[f"{operacao}_total"] += 1
            if sucesso:
                self._metricas[f"{operacao}_sucesso"] += 1
            else:
                self._metricas[f"{operacao}_erro"] += 1
            
            self._tempos_operacao[operacao].append(tempo_ms)
    
    def registrar_transacao(self, tipo: TipoTransacao, valor: Dinheiro) -> None:
        """Registra métricas de transação"""
        with self._lock:
            self._metricas[f"transacao_{tipo.value.lower()}_count"] += 1
            self._metricas[f"transacao_{tipo.value.lower()}_valor"] += float(valor.valor)
    
    def obter_relatorio(self) -> Dict[str, Any]:
        """Gera relatório de métricas"""
        with self._lock:
            relatorio = {
                "periodo_coleta": {
                    "inicio": self._inicio_coleta.isoformat(),
                    "duracao_horas": (datetime.now() - self._inicio_coleta).total_seconds() / 3600
                },
                "metricas_gerais": dict(self._metricas),
                "tempos_operacao": {}
            }
            
            # Calcular estatísticas de tempo
            for operacao, tempos in self._tempos_operacao.items():
                if tempos:
                    relatorio["tempos_operacao"][operacao] = {
                        "media_ms": sum(tempos) / len(tempos),
                        "min_ms": min(tempos),
                        "max_ms": max(tempos),
                        "p95_ms": sorted(tempos)[int(len(tempos) * 0.95)] if len(tempos) > 20 else max(tempos)
                    }
            
            return relatorio
    
    def resetar(self) -> None:
        """Reseta todas as métricas"""
        with self._lock:
            self._metricas.clear()
            self._tempos_operacao.clear()
            self._inicio_coleta = datetime.now()


class AuditoriaTransacoes:
    """
    Sistema de auditoria para transações
    
    RESPONSABILIDADES:
    - Registrar trilha de auditoria
    - Detectar anomalias
    - Gerar relatórios de compliance
    - Manter logs imutáveis
    """
    
    def __init__(self, arquivo_auditoria: str = "auditoria.log"):
        self._arquivo = arquivo_auditoria
        self._lock = threading.RLock()
        
        # Criar arquivo se não existir
        Path(self._arquivo).touch(exist_ok=True)
    
    def registrar_evento(self, evento: EventoDominio, contexto: Dict[str, Any] = None) -> None:
        """Registra evento na trilha de auditoria"""
        with self._lock:
            registro = {
                "timestamp": datetime.now().isoformat(),
                "evento_id": str(evento.id),
                "evento_tipo": evento.__class__.__name__,
                "evento_timestamp": evento.timestamp.isoformat(),
                "contexto": contexto or {},
                "dados_evento": evento.to_dict()
            }
            
            # Escrever no arquivo
            with open(self._arquivo, 'a', encoding='utf-8') as f:
                f.write(json.dumps(registro, ensure_ascii=False) + '\n')
    
    def buscar_eventos(self, data_inicio: datetime, data_fim: datetime) -> List[Dict[str, Any]]:
        """Busca eventos por período"""
        eventos = []
        
        try:
            with open(self._arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    registro = json.loads(linha.strip())
                    timestamp = datetime.fromisoformat(registro['timestamp'])
                    
                    if data_inicio <= timestamp <= data_fim:
                        eventos.append(registro)
        
        except FileNotFoundError:
            pass
        
        return eventos
    
    def gerar_relatorio_compliance(self, data_inicio: datetime, data_fim: datetime) -> Dict[str, Any]:
        """Gera relatório de compliance"""
        eventos = self.buscar_eventos(data_inicio, data_fim)
        
        relatorio = {
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            },
            "total_eventos": len(eventos),
            "tipos_evento": defaultdict(int),
            "transacoes_suspeitas": [],
            "valores_movimentados": defaultdict(float)
        }
        
        for evento in eventos:
            tipo = evento['evento_tipo']
            relatorio["tipos_evento"][tipo] += 1
            
            # Analisar transações suspeitas
            if tipo == "EventoTransacaoRealizada":
                dados = evento['dados_evento']
                valor = float(dados.get('valor', {}).get('valor', 0))
                
                # Transação suspeita se > R$ 10.000
                if valor > 10000:
                    relatorio["transacoes_suspeitas"].append({
                        "transacao_id": dados.get('transacao_id'),
                        "valor": valor,
                        "timestamp": evento['timestamp']
                    })
                
                # Acumular valores por tipo
                tipo_transacao = dados.get('tipo', 'DESCONHECIDO')
                relatorio["valores_movimentados"][tipo_transacao] += valor
        
        return relatorio
