#!/usr/bin/env python3
"""
Entidades do Sistema de E-commerce

RESPONSABILIDADE: Entidades com identidade própria e lógica de negócio.
Cada entidade encapsula comportamentos relacionados ao seu ciclo de vida.

PRINCÍPIOS SOLID APLICADOS:
- SRP: Cada entidade tem responsabilidade específica e bem definida
- OCP: Extensível através de herança e composição
- LSP: Subtipos podem substituir tipos base
- ISP: Interfaces segregadas por responsabilidade
- DIP: Depende de abstrações, não de concretizações

PADRÕES DE DESIGN:
- Domain-Driven Design: Entidades ricos em comportamento
- Strategy: Diferentes tipos de produto
- Observer: Eventos de domínio
- State: Estados do pedido

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Dict, Optional, Set, Protocol, Any
from uuid import UUID, uuid4
from datetime import datetime, timedelta
import logging

from .value_objects import (
    Dinheiro, DimensoesProduto, Endereco, InformacaoDigital,
    InformacaoServico, TipoProduto, StatusPedido, TipoNotificacao,
    ResultadoCalculoFrete, DadosPagamento
)


# =============================================================================
# EVENTOS DE DOMÍNIO (Observer Pattern)
# =============================================================================

class EventoDominio(ABC):
    """Base para todos os eventos de domínio"""
    def __init__(self):
        self.timestamp = datetime.now()
        self.id_evento = uuid4()


@dataclass
class ProdutoAdicionado(EventoDominio):
    produto_id: UUID
    nome_produto: str
    preco: Dinheiro


@dataclass
class PedidoCriado(EventoDominio):
    pedido_id: UUID
    cliente_id: UUID
    valor_total: Dinheiro


@dataclass
class StatusPedidoAlterado(EventoDominio):
    pedido_id: UUID
    status_anterior: StatusPedido
    status_novo: StatusPedido
    observacoes: str = ""


@dataclass
class PagamentoProcessado(EventoDominio):
    pedido_id: UUID
    valor: Dinheiro
    metodo_pagamento: str
    sucesso: bool
    detalhes: str = ""


# =============================================================================
# INTERFACES (ISP - Interface Segregation Principle)
# =============================================================================

class PodeCalcularFrete(Protocol):
    """Interface para entidades que podem calcular frete"""
    def calcular_frete(self, endereco_destino: Endereco) -> ResultadoCalculoFrete:
        ...


class PodeSerVendido(Protocol):
    """Interface para itens vendáveis"""
    def obter_preco_venda(self) -> Dinheiro:
        ...
    
    def esta_disponivel(self) -> bool:
        ...


class PodeNotificar(Protocol):
    """Interface para entidades que podem enviar notificações"""
    def obter_preferencias_notificacao(self) -> Set[TipoNotificacao]:
        ...


class PodeTerDesconto(Protocol):
    """Interface para itens que podem receber desconto"""
    def aplicar_desconto(self, percentual: Decimal) -> Dinheiro:
        ...


# =============================================================================
# ENTIDADE BASE
# =============================================================================

class EntidadeDominio(ABC):
    """
    ✅ Classe base para todas as entidades de domínio
    
    PRINCÍPIOS APLICADOS:
    - SRP: Responsável apenas pela identidade e eventos
    - Template Method: Define estrutura para validação
    """
    
    def __init__(self, id: Optional[UUID] = None):
        self._id: UUID = id or uuid4()
        self._eventos: List[EventoDominio] = []
        self._criado_em: datetime = datetime.now()
        self._atualizado_em: datetime = datetime.now()
        self._versao: int = 1
        
        # Executar validação inicial
        self._validar()
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def criado_em(self) -> datetime:
        return self._criado_em
    
    @property
    def atualizado_em(self) -> datetime:
        return self._atualizado_em
    
    @property
    def versao(self) -> int:
        return self._versao
    
    def adicionar_evento(self, evento: EventoDominio) -> None:
        """Adiciona evento de domínio à lista"""
        self._eventos.append(evento)
        logging.info(f"Evento adicionado: {type(evento).__name__} para entidade {self._id}")
    
    def limpar_eventos(self) -> List[EventoDominio]:
        """Remove e retorna todos os eventos pendentes"""
        eventos = self._eventos.copy()
        self._eventos.clear()
        return eventos
    
    def marcar_como_modificado(self) -> None:
        """Marca entidade como modificada"""
        self._atualizado_em = datetime.now()
        self._versao += 1
    
    @abstractmethod
    def _validar(self) -> None:
        """Validação específica da entidade (Template Method)"""
        pass
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self._id})"


# =============================================================================
# ENTIDADE PRODUTO E HIERARQUIA
# =============================================================================

class Produto(EntidadeDominio, PodeSerVendido, PodeTerDesconto):
    """
    ✅ Entidade Produto - Classe base para todos os tipos de produto
    
    PRINCÍPIOS APLICADOS:
    - SRP: Responsável por dados e comportamentos comuns a todos os produtos
    - OCP: Extensível através de subclasses especializadas
    - LSP: Subclasses mantêm contrato da classe base
    """
    
    def __init__(self, nome: str, descricao: str, preco: Dinheiro,
                 categoria: str, fabricante: str, id: Optional[UUID] = None):
        self._nome = nome
        self._descricao = descricao
        self._preco = preco
        self._categoria = categoria
        self._fabricante = fabricante
        self._ativo = True
        self._estoque_minimo = 0
        self._tags: Set[str] = set()
        
        super().__init__(id)
        
        # Evento de criação
        self.adicionar_evento(ProdutoAdicionado(self.id, self._nome, self._preco))
    
    # Propriedades (Encapsulamento)
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def descricao(self) -> str:
        return self._descricao
    
    @property
    def preco(self) -> Dinheiro:
        return self._preco
    
    @property
    def categoria(self) -> str:
        return self._categoria
    
    @property
    def fabricante(self) -> str:
        return self._fabricante
    
    @property
    def ativo(self) -> bool:
        return self._ativo
    
    @property
    def tags(self) -> Set[str]:
        return self._tags.copy()
    
    # Implementação das interfaces
    def obter_preco_venda(self) -> Dinheiro:
        """Implementa PodeSerVendido"""
        return self._preco
    
    def esta_disponivel(self) -> bool:
        """Implementa PodeSerVendido"""
        return self._ativo
    
    def aplicar_desconto(self, percentual: Decimal) -> Dinheiro:
        """Implementa PodeTerDesconto"""
        if percentual < Decimal('0') or percentual > Decimal('100'):
            raise ValueError("Percentual deve estar entre 0 e 100")
        
        desconto = self._preco.aplicar_percentual(percentual)
        return self._preco.subtrair(desconto)
    
    # Métodos de negócio
    def atualizar_preco(self, novo_preco: Dinheiro) -> None:
        """Atualiza preço do produto"""
        if novo_preco.eh_menor_que(Dinheiro(Decimal('0.01'))):
            raise ValueError("Preço deve ser maior que R$ 0,01")
        
        preco_anterior = self._preco
        self._preco = novo_preco
        self.marcar_como_modificado()
        
        logging.info(f"Preço alterado de {preco_anterior} para {novo_preco}")
    
    def adicionar_tag(self, tag: str) -> None:
        """Adiciona tag ao produto"""
        if tag and tag.strip():
            self._tags.add(tag.strip().lower())
            self.marcar_como_modificado()
    
    def remover_tag(self, tag: str) -> None:
        """Remove tag do produto"""
        self._tags.discard(tag.lower())
        self.marcar_como_modificado()
    
    def ativar(self) -> None:
        """Ativa produto para venda"""
        if not self._ativo:
            self._ativo = True
            self.marcar_como_modificado()
            logging.info(f"Produto {self.nome} ativado")
    
    def desativar(self) -> None:
        """Desativa produto para venda"""
        if self._ativo:
            self._ativo = False
            self.marcar_como_modificado()
            logging.info(f"Produto {self.nome} desativado")
    
    def possui_tag(self, tag: str) -> bool:
        """Verifica se produto possui tag específica"""
        return tag.lower() in self._tags
    
    @abstractmethod
    def obter_tipo_produto(self) -> TipoProduto:
        """Método abstrato para obter tipo específico"""
        pass
    
    def _validar(self) -> None:
        """Validações específicas do produto"""
        if not self._nome or len(self._nome.strip()) < 2:
            raise ValueError("Nome do produto deve ter pelo menos 2 caracteres")
        
        if not self._descricao or len(self._descricao.strip()) < 10:
            raise ValueError("Descrição deve ter pelo menos 10 caracteres")
        
        if self._preco.eh_menor_que(Dinheiro(Decimal('0.01'))):
            raise ValueError("Preço deve ser maior que R$ 0,01")
        
        if not self._categoria or len(self._categoria.strip()) < 2:
            raise ValueError("Categoria é obrigatória")
    
    def __str__(self) -> str:
        status = "Ativo" if self._ativo else "Inativo"
        return f"{self._nome} - {self._preco} ({status})"


class ProdutoFisico(Produto, PodeCalcularFrete):
    """
    ✅ Produto Físico - Requer envio postal
    
    RESPONSABILIDADES:
    - Gerenciar dimensões e peso
    - Calcular frete baseado em localização
    - Controlar estoque físico
    """
    
    def __init__(self, nome: str, descricao: str, preco: Dinheiro,
                 categoria: str, fabricante: str, dimensoes: DimensoesProduto,
                 quantidade_estoque: int = 0, id: Optional[UUID] = None):
        
        self._dimensoes = dimensoes
        self._quantidade_estoque = quantidade_estoque
        self._estoque_minimo = 5
        self._localizacao_estoque = "Depósito Principal"
        
        super().__init__(nome, descricao, preco, categoria, fabricante, id)
    
    @property
    def dimensoes(self) -> DimensoesProduto:
        return self._dimensoes
    
    @property
    def quantidade_estoque(self) -> int:
        return self._quantidade_estoque
    
    @property
    def estoque_minimo(self) -> int:
        return self._estoque_minimo
    
    def obter_tipo_produto(self) -> TipoProduto:
        return TipoProduto.FISICO
    
    def esta_disponivel(self) -> bool:
        """Sobrescreve para considerar estoque"""
        return super().esta_disponivel() and self._quantidade_estoque > 0
    
    def calcular_frete(self, endereco_destino: Endereco) -> ResultadoCalculoFrete:
        """
        Implementa cálculo de frete (Strategy Pattern aplicado externamente)
        
        NOTA: Em sistema real, seria injetada uma estratégia de cálculo
        """
        # Simulação simples baseada em peso e distância
        peso_total = max(self._dimensoes.peso, self._dimensoes.calcular_peso_volumetrico())
        
        # Distância aproximada (simulada)
        endereco_origem = Endereco("01310-100", "Av. Paulista", "1000", None,
                                 "Bela Vista", "São Paulo", "SP")
        distancia_km = endereco_origem.calcular_distancia_aproximada(endereco_destino)
        
        # Cálculo simplificado
        valor_base = Decimal('10.00')
        valor_peso = peso_total * Decimal('2.00')
        valor_distancia = Decimal(str(distancia_km)) * Decimal('0.05')
        
        valor_total = valor_base + valor_peso + valor_distancia
        prazo_dias = min(3 + (distancia_km // 200), 30)
        
        return ResultadoCalculoFrete(
            valor=Dinheiro(valor_total),
            prazo_dias=prazo_dias,
            transportadora="Correios",
            servico="PAC",
            detalhes=f"Peso: {peso_total}kg, Distância: {distancia_km}km"
        )
    
    def adicionar_estoque(self, quantidade: int) -> None:
        """Adiciona itens ao estoque"""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        self._quantidade_estoque += quantidade
        self.marcar_como_modificado()
        logging.info(f"Adicionado {quantidade} unidades ao estoque de {self.nome}")
    
    def remover_estoque(self, quantidade: int) -> bool:
        """
        Remove itens do estoque
        
        Returns:
            True se conseguiu remover, False se estoque insuficiente
        """
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        if self._quantidade_estoque >= quantidade:
            self._quantidade_estoque -= quantidade
            self.marcar_como_modificado()
            logging.info(f"Removido {quantidade} unidades do estoque de {self.nome}")
            return True
        
        return False
    
    def esta_em_falta(self) -> bool:
        """Verifica se estoque está abaixo do mínimo"""
        return self._quantidade_estoque <= self._estoque_minimo
    
    def definir_estoque_minimo(self, quantidade: int) -> None:
        """Define quantidade mínima de estoque"""
        if quantidade < 0:
            raise ValueError("Estoque mínimo não pode ser negativo")
        
        self._estoque_minimo = quantidade
        self.marcar_como_modificado()
    
    def __str__(self) -> str:
        base_str = super().__str__()
        estoque_info = f"Estoque: {self._quantidade_estoque}"
        return f"{base_str} - {estoque_info}"


class ProdutoDigital(Produto):
    """
    ✅ Produto Digital - Download imediato
    
    RESPONSABILIDADES:
    - Gerenciar informações de download
    - Controlar licenças e acessos
    - Sem necessidade de estoque físico
    """
    
    def __init__(self, nome: str, descricao: str, preco: Dinheiro,
                 categoria: str, fabricante: str, info_digital: InformacaoDigital,
                 licencas_disponiveis: int = -1, id: Optional[UUID] = None):
        
        self._info_digital = info_digital
        self._licencas_disponiveis = licencas_disponiveis  # -1 = ilimitado
        self._licencas_vendidas = 0
        self._requer_ativacao = bool(info_digital.chave_licenca)
        
        super().__init__(nome, descricao, preco, categoria, fabricante, id)
    
    @property
    def info_digital(self) -> InformacaoDigital:
        return self._info_digital
    
    @property
    def licencas_disponiveis(self) -> int:
        return self._licencas_disponiveis
    
    @property
    def licencas_vendidas(self) -> int:
        return self._licencas_vendidas
    
    def obter_tipo_produto(self) -> TipoProduto:
        return TipoProduto.DIGITAL
    
    def esta_disponivel(self) -> bool:
        """Considera licenças disponíveis"""
        disponivel_base = super().esta_disponivel()
        
        if self._licencas_disponiveis == -1:  # Ilimitado
            return disponivel_base
        
        return disponivel_base and self._licencas_vendidas < self._licencas_disponiveis
    
    def consumir_licenca(self) -> bool:
        """
        Consome uma licença na venda
        
        Returns:
            True se conseguiu consumir, False se não há licenças
        """
        if not self.esta_disponivel():
            return False
        
        if self._licencas_disponiveis != -1:
            self._licencas_vendidas += 1
            self.marcar_como_modificado()
        
        return True
    
    def adicionar_licencas(self, quantidade: int) -> None:
        """Adiciona licenças disponíveis"""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        if self._licencas_disponiveis == -1:
            raise ValueError("Produto tem licenças ilimitadas")
        
        self._licencas_disponiveis += quantidade
        self.marcar_como_modificado()
        logging.info(f"Adicionadas {quantidade} licenças para {self.nome}")
    
    def obter_tempo_download(self, velocidade_mbps: Decimal = Decimal('10')) -> int:
        """Retorna tempo estimado de download"""
        return self._info_digital.tempo_download_estimado(velocidade_mbps)
    
    def eh_arquivo_grande(self) -> bool:
        """Verifica se arquivo é considerado grande"""
        return self._info_digital.eh_arquivo_grande()
    
    def __str__(self) -> str:
        base_str = super().__str__()
        licencas_info = ("Licenças: Ilimitadas" if self._licencas_disponiveis == -1 
                        else f"Licenças: {self._licencas_disponiveis - self._licencas_vendidas}")
        return f"{base_str} - {licencas_info}"


class ProdutoServico(Produto):
    """
    ✅ Produto de Serviço - Mão de obra especializada
    
    RESPONSABILIDADES:
    - Gerenciar informações de execução
    - Controlar agenda e disponibilidade
    - Calcular custos baseados em tempo
    """
    
    def __init__(self, nome: str, descricao: str, preco: Dinheiro,
                 categoria: str, fabricante: str, info_servico: InformacaoServico,
                 profissionais_disponiveis: int = 1, id: Optional[UUID] = None):
        
        self._info_servico = info_servico
        self._profissionais_disponiveis = profissionais_disponiveis
        self._agendamentos_ativos = 0
        self._requer_agendamento = True
        
        super().__init__(nome, descricao, preco, categoria, fabricante, id)
    
    @property
    def info_servico(self) -> InformacaoServico:
        return self._info_servico
    
    @property
    def profissionais_disponiveis(self) -> int:
        return self._profissionais_disponiveis
    
    @property
    def agendamentos_ativos(self) -> int:
        return self._agendamentos_ativos
    
    def obter_tipo_produto(self) -> TipoProduto:
        return TipoProduto.SERVICO
    
    def esta_disponivel(self) -> bool:
        """Considera profissionais disponíveis"""
        disponivel_base = super().esta_disponivel()
        return (disponivel_base and 
                self._agendamentos_ativos < self._profissionais_disponiveis)
    
    def agendar_servico(self) -> bool:
        """
        Agenda execução do serviço
        
        Returns:
            True se conseguiu agendar, False se não há disponibilidade
        """
        if not self.esta_disponivel():
            return False
        
        self._agendamentos_ativos += 1
        self.marcar_como_modificado()
        logging.info(f"Serviço {self.nome} agendado")
        return True
    
    def finalizar_servico(self) -> None:
        """Finaliza execução do serviço"""
        if self._agendamentos_ativos > 0:
            self._agendamentos_ativos -= 1
            self.marcar_como_modificado()
            logging.info(f"Serviço {self.nome} finalizado")
    
    def adicionar_profissional(self) -> None:
        """Adiciona profissional à equipe"""
        self._profissionais_disponiveis += 1
        self.marcar_como_modificado()
    
    def remover_profissional(self) -> bool:
        """Remove profissional da equipe se possível"""
        if self._profissionais_disponiveis > 1:
            self._profissionais_disponiveis -= 1
            self.marcar_como_modificado()
            return True
        return False
    
    def calcular_dias_trabalho(self, horas_por_dia: Decimal = Decimal('8')) -> Decimal:
        """Calcula dias necessários para executar serviço"""
        return self._info_servico.calcular_dias_trabalho(horas_por_dia)
    
    def obter_preco_por_hora(self) -> Dinheiro:
        """Calcula preço por hora do serviço"""
        valor_por_hora = self._preco.valor / self._info_servico.duracao_horas
        return Dinheiro(valor_por_hora)
    
    def __str__(self) -> str:
        base_str = super().__str__()
        disponibilidade = f"Profissionais: {self._profissionais_disponiveis - self._agendamentos_ativos}/{self._profissionais_disponiveis}"
        return f"{base_str} - {disponibilidade}"


# =============================================================================
# ENTIDADE CLIENTE
# =============================================================================

class Cliente(EntidadeDominio, PodeNotificar):
    """
    ✅ Entidade Cliente
    
    RESPONSABILIDADES:
    - Gerenciar dados pessoais e preferências
    - Histórico de compras e fidelidade
    - Preferências de notificação
    """
    
    def __init__(self, nome: str, email: str, telefone: str,
                 endereco_principal: Endereco, id: Optional[UUID] = None):
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._endereco_principal = endereco_principal
        self._enderecos_adicionais: List[Endereco] = []
        self._ativo = True
        self._data_ultima_compra: Optional[datetime] = None
        self._valor_total_compras = Dinheiro(Decimal('0'))
        self._numero_pedidos = 0
        self._preferencias_notificacao: Set[TipoNotificacao] = {TipoNotificacao.EMAIL}
        
        super().__init__(id)
    
    # Propriedades
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    @property
    def endereco_principal(self) -> Endereco:
        return self._endereco_principal
    
    @property
    def enderecos_adicionais(self) -> List[Endereco]:
        return self._enderecos_adicionais.copy()
    
    @property
    def ativo(self) -> bool:
        return self._ativo
    
    @property
    def valor_total_compras(self) -> Dinheiro:
        return self._valor_total_compras
    
    @property
    def numero_pedidos(self) -> int:
        return self._numero_pedidos
    
    # Implementação da interface PodeNotificar
    def obter_preferencias_notificacao(self) -> Set[TipoNotificacao]:
        return self._preferencias_notificacao.copy()
    
    # Métodos de negócio
    def adicionar_endereco(self, endereco: Endereco) -> None:
        """Adiciona endereço adicional"""
        if endereco not in self._enderecos_adicionais:
            self._enderecos_adicionais.append(endereco)
            self.marcar_como_modificado()
    
    def remover_endereco(self, endereco: Endereco) -> bool:
        """Remove endereço adicional"""
        if endereco in self._enderecos_adicionais:
            self._enderecos_adicionais.remove(endereco)
            self.marcar_como_modificado()
            return True
        return False
    
    def obter_todos_enderecos(self) -> List[Endereco]:
        """Retorna todos os endereços (principal + adicionais)"""
        return [self._endereco_principal] + self._enderecos_adicionais
    
    def atualizar_email(self, novo_email: str) -> None:
        """Atualiza email com validação"""
        if '@' not in novo_email or '.' not in novo_email:
            raise ValueError("Email inválido")
        
        self._email = novo_email.lower().strip()
        self.marcar_como_modificado()
    
    def atualizar_telefone(self, novo_telefone: str) -> None:
        """Atualiza telefone com formatação"""
        # Limpar formatação
        telefone_limpo = ''.join(filter(str.isdigit, novo_telefone))
        
        if len(telefone_limpo) not in [10, 11]:  # Fixo ou móvel
            raise ValueError("Telefone inválido")
        
        # Formatar (11) 99999-9999
        if len(telefone_limpo) == 11:
            telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
        else:
            telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        self._telefone = telefone_formatado
        self.marcar_como_modificado()
    
    def configurar_notificacoes(self, tipos: Set[TipoNotificacao]) -> None:
        """Configura preferências de notificação"""
        if not tipos:
            raise ValueError("Pelo menos um tipo de notificação deve ser selecionado")
        
        self._preferencias_notificacao = tipos.copy()
        self.marcar_como_modificado()
    
    def registrar_compra(self, valor: Dinheiro) -> None:
        """Registra nova compra no histórico"""
        self._data_ultima_compra = datetime.now()
        self._valor_total_compras = self._valor_total_compras.somar(valor)
        self._numero_pedidos += 1
        self.marcar_como_modificado()
    
    def eh_cliente_vip(self, valor_minimo: Dinheiro = None) -> bool:
        """Verifica se cliente é VIP baseado em histórico"""
        if valor_minimo is None:
            valor_minimo = Dinheiro(Decimal('1000'))
        
        return (self._numero_pedidos >= 5 and 
                self._valor_total_compras.eh_maior_que(valor_minimo))
    
    def obter_ticket_medio(self) -> Dinheiro:
        """Calcula ticket médio das compras"""
        if self._numero_pedidos == 0:
            return Dinheiro(Decimal('0'))
        
        return Dinheiro(self._valor_total_compras.valor / Decimal(str(self._numero_pedidos)))
    
    def dias_desde_ultima_compra(self) -> Optional[int]:
        """Retorna dias desde última compra"""
        if not self._data_ultima_compra:
            return None
        
        delta = datetime.now() - self._data_ultima_compra
        return delta.days
    
    def ativar(self) -> None:
        """Ativa cliente"""
        self._ativo = True
        self.marcar_como_modificado()
    
    def desativar(self) -> None:
        """Desativa cliente"""
        self._ativo = False
        self.marcar_como_modificado()
    
    def _validar(self) -> None:
        """Validações específicas do cliente"""
        if not self._nome or len(self._nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if '@' not in self._email or '.' not in self._email:
            raise ValueError("Email inválido")
        
        telefone_numeros = ''.join(filter(str.isdigit, self._telefone))
        if len(telefone_numeros) not in [10, 11]:
            raise ValueError("Telefone inválido")
    
    def __str__(self) -> str:
        status = "Ativo" if self._ativo else "Inativo"
        return f"{self._nome} ({self._email}) - {status}"


# =============================================================================
# ENTIDADE PEDIDO (Agregado Raiz)
# =============================================================================

@dataclass
class ItemPedido:
    """Value Object para itens do pedido"""
    produto_id: UUID
    nome_produto: str
    preco_unitario: Dinheiro
    quantidade: int
    desconto_aplicado: Dinheiro = field(default_factory=lambda: Dinheiro(Decimal('0')))
    
    def __post_init__(self):
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
    
    def calcular_subtotal(self) -> Dinheiro:
        """Calcula subtotal do item"""
        subtotal = self.preco_unitario.multiplicar(Decimal(str(self.quantidade)))
        return subtotal.subtrair(self.desconto_aplicado)
    
    def __str__(self) -> str:
        return f"{self.nome_produto} x{self.quantidade} = {self.calcular_subtotal()}"


class Pedido(EntidadeDominio):
    """
    ✅ Entidade Pedido - Agregado Raiz
    
    RESPONSABILIDADES:
    - Gerenciar ciclo de vida do pedido
    - Coordenar itens e pagamento
    - Controlar status e transições
    - Calcular valores totais
    """
    
    def __init__(self, cliente_id: UUID, endereco_entrega: Endereco,
                 id: Optional[UUID] = None):
        self._cliente_id = cliente_id
        self._endereco_entrega = endereco_entrega
        self._itens: List[ItemPedido] = []
        self._status = StatusPedido.CRIADO
        self._data_pedido = datetime.now()
        self._data_confirmacao: Optional[datetime] = None
        self._data_pagamento: Optional[datetime] = None
        self._data_envio: Optional[datetime] = None
        self._data_entrega: Optional[datetime] = None
        self._observacoes = ""
        self._numero_rastreamento: Optional[str] = None
        self._valor_frete = Dinheiro(Decimal('0'))
        self._desconto_total = Dinheiro(Decimal('0'))
        
        super().__init__(id)
        
        # Evento de criação
        self.adicionar_evento(PedidoCriado(self.id, cliente_id, Dinheiro(Decimal('0'))))
    
    # Propriedades
    @property
    def cliente_id(self) -> UUID:
        return self._cliente_id
    
    @property
    def endereco_entrega(self) -> Endereco:
        return self._endereco_entrega
    
    @property
    def itens(self) -> List[ItemPedido]:
        return self._itens.copy()
    
    @property
    def status(self) -> StatusPedido:
        return self._status
    
    @property
    def data_pedido(self) -> datetime:
        return self._data_pedido
    
    @property
    def numero_rastreamento(self) -> Optional[str]:
        return self._numero_rastreamento
    
    @property
    def valor_frete(self) -> Dinheiro:
        return self._valor_frete
    
    # Métodos de negócio - Gerenciamento de Itens
    def adicionar_item(self, produto: Produto, quantidade: int) -> None:
        """Adiciona item ao pedido"""
        if self._status != StatusPedido.CRIADO:
            raise ValueError("Não é possível adicionar itens a pedido já confirmado")
        
        if not produto.esta_disponivel():
            raise ValueError(f"Produto {produto.nome} não está disponível")
        
        # Verificar se item já existe
        for item in self._itens:
            if item.produto_id == produto.id:
                item.quantidade += quantidade
                self.marcar_como_modificado()
                return
        
        # Criar novo item
        novo_item = ItemPedido(
            produto_id=produto.id,
            nome_produto=produto.nome,
            preco_unitario=produto.obter_preco_venda(),
            quantidade=quantidade
        )
        
        self._itens.append(novo_item)
        self.marcar_como_modificado()
    
    def remover_item(self, produto_id: UUID) -> bool:
        """Remove item do pedido"""
        if self._status != StatusPedido.CRIADO:
            raise ValueError("Não é possível remover itens de pedido já confirmado")
        
        for i, item in enumerate(self._itens):
            if item.produto_id == produto_id:
                del self._itens[i]
                self.marcar_como_modificado()
                return True
        
        return False
    
    def atualizar_quantidade_item(self, produto_id: UUID, nova_quantidade: int) -> bool:
        """Atualiza quantidade de um item"""
        if self._status != StatusPedido.CRIADO:
            raise ValueError("Não é possível alterar itens de pedido já confirmado")
        
        if nova_quantidade <= 0:
            return self.remover_item(produto_id)
        
        for item in self._itens:
            if item.produto_id == produto_id:
                item.quantidade = nova_quantidade
                self.marcar_como_modificado()
                return True
        
        return False
    
    def aplicar_desconto_item(self, produto_id: UUID, desconto: Dinheiro) -> bool:
        """Aplica desconto a um item específico"""
        for item in self._itens:
            if item.produto_id == produto_id:
                if desconto.eh_maior_que(item.calcular_subtotal()):
                    raise ValueError("Desconto não pode ser maior que o valor do item")
                
                item.desconto_aplicado = desconto
                self.marcar_como_modificado()
                return True
        
        return False
    
    # Métodos de cálculo
    def calcular_subtotal(self) -> Dinheiro:
        """Calcula subtotal dos itens"""
        if not self._itens:
            return Dinheiro(Decimal('0'))
        
        total = self._itens[0].calcular_subtotal()
        for item in self._itens[1:]:
            total = total.somar(item.calcular_subtotal())
        
        return total
    
    def calcular_total(self) -> Dinheiro:
        """Calcula total do pedido (subtotal + frete - desconto)"""
        subtotal = self.calcular_subtotal()
        total = subtotal.somar(self._valor_frete)
        return total.subtrair(self._desconto_total)
    
    def definir_frete(self, valor_frete: Dinheiro) -> None:
        """Define valor do frete"""
        self._valor_frete = valor_frete
        self.marcar_como_modificado()
    
    def aplicar_desconto_geral(self, desconto: Dinheiro) -> None:
        """Aplica desconto geral ao pedido"""
        subtotal = self.calcular_subtotal()
        if desconto.eh_maior_que(subtotal):
            raise ValueError("Desconto não pode ser maior que o subtotal")
        
        self._desconto_total = desconto
        self.marcar_como_modificado()
    
    # Métodos de status (State Pattern conceitual)
    def confirmar(self, observacoes: str = "") -> None:
        """Confirma o pedido"""
        if self._status != StatusPedido.CRIADO:
            raise ValueError(f"Pedido não pode ser confirmado no status {self._status.value}")
        
        if not self._itens:
            raise ValueError("Pedido deve ter pelo menos um item")
        
        status_anterior = self._status
        self._status = StatusPedido.CONFIRMADO
        self._data_confirmacao = datetime.now()
        self._observacoes = observacoes
        self.marcar_como_modificado()
        
        # Evento de mudança de status
        self.adicionar_evento(StatusPedidoAlterado(
            self.id, status_anterior, self._status, observacoes
        ))
    
    def processar_pagamento(self, dados_pagamento: DadosPagamento, valor: Dinheiro) -> None:
        """Processa pagamento do pedido"""
        if self._status != StatusPedido.CONFIRMADO:
            raise ValueError(f"Pagamento não pode ser processado no status {self._status.value}")
        
        valor_esperado = self.calcular_total()
        if not valor.valor == valor_esperado.valor:
            raise ValueError(f"Valor pago {valor} diferente do esperado {valor_esperado}")
        
        status_anterior = self._status
        self._status = StatusPedido.PAGO
        self._data_pagamento = datetime.now()
        self.marcar_como_modificado()
        
        # Eventos
        self.adicionar_evento(StatusPedidoAlterado(
            self.id, status_anterior, self._status
        ))
        self.adicionar_evento(PagamentoProcessado(
            self.id, valor, str(dados_pagamento), True
        ))
    
    def enviar(self, numero_rastreamento: str) -> None:
        """Marca pedido como enviado"""
        if self._status != StatusPedido.PAGO:
            raise ValueError(f"Pedido não pode ser enviado no status {self._status.value}")
        
        status_anterior = self._status
        self._status = StatusPedido.ENVIADO
        self._data_envio = datetime.now()
        self._numero_rastreamento = numero_rastreamento
        self.marcar_como_modificado()
        
        self.adicionar_evento(StatusPedidoAlterado(
            self.id, status_anterior, self._status, f"Rastreamento: {numero_rastreamento}"
        ))
    
    def entregar(self) -> None:
        """Marca pedido como entregue"""
        if self._status != StatusPedido.ENVIADO:
            raise ValueError(f"Pedido não pode ser entregue no status {self._status.value}")
        
        status_anterior = self._status
        self._status = StatusPedido.ENTREGUE
        self._data_entrega = datetime.now()
        self.marcar_como_modificado()
        
        self.adicionar_evento(StatusPedidoAlterado(
            self.id, status_anterior, self._status
        ))
    
    def cancelar(self, motivo: str) -> None:
        """Cancela o pedido"""
        if self._status in [StatusPedido.ENTREGUE]:
            raise ValueError("Pedido entregue não pode ser cancelado")
        
        status_anterior = self._status
        self._status = StatusPedido.CANCELADO
        self.marcar_como_modificado()
        
        self.adicionar_evento(StatusPedidoAlterado(
            self.id, status_anterior, self._status, motivo
        ))
    
    # Métodos auxiliares
    def obter_quantidade_total_itens(self) -> int:
        """Retorna quantidade total de itens"""
        return sum(item.quantidade for item in self._itens)
    
    def contem_produto(self, produto_id: UUID) -> bool:
        """Verifica se pedido contém produto específico"""
        return any(item.produto_id == produto_id for item in self._itens)
    
    def eh_pedido_fisico(self) -> bool:
        """Verifica se pedido contém apenas produtos físicos"""
        # Em sistema real, consultaria repositório de produtos
        return True  # Simplificação
    
    def tempo_processamento(self) -> Optional[timedelta]:
        """Calcula tempo de processamento do pedido"""
        if self._data_entrega and self._data_pedido:
            return self._data_entrega - self._data_pedido
        return None
    
    def _validar(self) -> None:
        """Validações específicas do pedido"""
        # Validação básica - pedido pode ser criado vazio e ter itens adicionados depois
        pass
    
    def __str__(self) -> str:
        total = self.calcular_total()
        qtd_itens = self.obter_quantidade_total_itens()
        return f"Pedido {self.id} - {self._status.value} - {qtd_itens} itens - {total}"


# =============================================================================
# EXPORTAÇÕES
# =============================================================================

__all__ = [
    # Eventos
    'EventoDominio', 'ProdutoAdicionado', 'PedidoCriado',
    'StatusPedidoAlterado', 'PagamentoProcessado',
    
    # Interfaces
    'PodeCalcularFrete', 'PodeSerVendido', 'PodeNotificar', 'PodeTerDesconto',
    
    # Entidade Base
    'EntidadeDominio',
    
    # Produtos
    'Produto', 'ProdutoFisico', 'ProdutoDigital', 'ProdutoServico',
    
    # Cliente
    'Cliente',
    
    # Pedido
    'ItemPedido', 'Pedido'
]
