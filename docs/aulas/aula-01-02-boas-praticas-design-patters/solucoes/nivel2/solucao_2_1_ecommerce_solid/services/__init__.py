#!/usr/bin/env python3
"""
Serviços de Aplicação - Sistema de E-commerce

RESPONSABILIDADE: Camada de serviços que coordena operações de negócio
complexas, implementando casos de uso da aplicação.

PRINCÍPIOS SOLID APLICADOS:
- SRP: Cada serviço tem responsabilidade específica
- OCP: Extensível através de novas implementações de interface
- LSP: Implementações podem ser substituídas
- ISP: Interfaces segregadas por área de responsabilidade
- DIP: Depende de abstrações (repositories, gateways)

PADRÕES DE DESIGN:
- Strategy: Diferentes estratégias de cálculo e processamento
- Factory: Criação de objetos complexos
- Observer: Eventos e notificações
- Command: Encapsulamento de operações

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional, Dict, Any, Set
from uuid import UUID
from datetime import datetime, timedelta
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import (
    Produto, ProdutoFisico, ProdutoDigital, ProdutoServico,
    Cliente, Pedido, ItemPedido, EventoDominio
)
from domain.value_objects import (
    Dinheiro, Endereco, ResultadoCalculoFrete, DadosPagamento,
    TipoNotificacao, StatusPedido, TipoProduto
)


# =============================================================================
# INTERFACES DE REPOSITÓRIO (DIP)
# =============================================================================

class RepositorioProduto(ABC):
    """Interface para repositório de produtos"""
    
    @abstractmethod
    def salvar(self, produto: Produto) -> None:
        pass
    
    @abstractmethod
    def buscar_por_id(self, produto_id: UUID) -> Optional[Produto]:
        pass
    
    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> List[Produto]:
        pass
    
    @abstractmethod
    def buscar_disponiveis(self) -> List[Produto]:
        pass
    
    @abstractmethod
    def excluir(self, produto_id: UUID) -> bool:
        pass


class RepositorioCliente(ABC):
    """Interface para repositório de clientes"""
    
    @abstractmethod
    def salvar(self, cliente: Cliente) -> None:
        pass
    
    @abstractmethod
    def buscar_por_id(self, cliente_id: UUID) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def buscar_ativos(self) -> List[Cliente]:
        pass


class RepositorioPedido(ABC):
    """Interface para repositório de pedidos"""
    
    @abstractmethod
    def salvar(self, pedido: Pedido) -> None:
        pass
    
    @abstractmethod
    def buscar_por_id(self, pedido_id: UUID) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    def buscar_por_cliente(self, cliente_id: UUID) -> List[Pedido]:
        pass
    
    @abstractmethod
    def buscar_por_status(self, status: StatusPedido) -> List[Pedido]:
        pass


# =============================================================================
# INTERFACES DE GATEWAY (DIP)
# =============================================================================

class GatewayPagamento(ABC):
    """Interface para processamento de pagamentos"""
    
    @abstractmethod
    def processar_pagamento(self, dados: DadosPagamento, valor: Dinheiro) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def estornar_pagamento(self, transacao_id: str, valor: Dinheiro) -> Dict[str, Any]:
        pass


class GatewayNotificacao(ABC):
    """Interface para envio de notificações"""
    
    @abstractmethod
    def enviar_notificacao(self, destinatario: str, tipo: TipoNotificacao,
                          assunto: str, mensagem: str) -> bool:
        pass


class ServicoFrete(ABC):
    """Interface para cálculo de frete"""
    
    @abstractmethod
    def calcular_frete(self, produto: ProdutoFisico, endereco_destino: Endereco) -> ResultadoCalculoFrete:
        pass


# =============================================================================
# ESTRATÉGIAS DE DESCONTO (Strategy Pattern)
# =============================================================================

class EstrategiaDesconto(ABC):
    """Interface para estratégias de desconto"""
    
    @abstractmethod
    def calcular_desconto(self, pedido: Pedido, cliente: Cliente) -> Dinheiro:
        pass
    
    @abstractmethod
    def eh_aplicavel(self, pedido: Pedido, cliente: Cliente) -> bool:
        pass


class DescontoClienteVIP(EstrategiaDesconto):
    """Desconto para clientes VIP"""
    
    def __init__(self, percentual: Decimal = Decimal('10')):
        self._percentual = percentual
    
    def calcular_desconto(self, pedido: Pedido, cliente: Cliente) -> Dinheiro:
        if not self.eh_aplicavel(pedido, cliente):
            return Dinheiro(Decimal('0'))
        
        subtotal = pedido.calcular_subtotal()
        return subtotal.aplicar_percentual(self._percentual)
    
    def eh_aplicavel(self, pedido: Pedido, cliente: Cliente) -> bool:
        return cliente.eh_cliente_vip()


class DescontoPrimeiraCompra(EstrategiaDesconto):
    """Desconto para primeira compra"""
    
    def __init__(self, valor_fixo: Dinheiro = None):
        self._valor_fixo = valor_fixo or Dinheiro(Decimal('20'))
    
    def calcular_desconto(self, pedido: Pedido, cliente: Cliente) -> Dinheiro:
        if not self.eh_aplicavel(pedido, cliente):
            return Dinheiro(Decimal('0'))
        
        return self._valor_fixo
    
    def eh_aplicavel(self, pedido: Pedido, cliente: Cliente) -> bool:
        return cliente.numero_pedidos == 0


class DescontoCompraAcima(EstrategiaDesconto):
    """Desconto para compras acima de valor mínimo"""
    
    def __init__(self, valor_minimo: Dinheiro, percentual: Decimal):
        self._valor_minimo = valor_minimo
        self._percentual = percentual
    
    def calcular_desconto(self, pedido: Pedido, cliente: Cliente) -> Dinheiro:
        if not self.eh_aplicavel(pedido, cliente):
            return Dinheiro(Decimal('0'))
        
        subtotal = pedido.calcular_subtotal()
        return subtotal.aplicar_percentual(self._percentual)
    
    def eh_aplicavel(self, pedido: Pedido, cliente: Cliente) -> bool:
        subtotal = pedido.calcular_subtotal()
        return subtotal.eh_maior_que(self._valor_minimo)


# =============================================================================
# FÁBRICA DE PRODUTOS (Factory Pattern)
# =============================================================================

class FabricaProdutos:
    """
    ✅ Factory para criação de produtos
    
    BENEFÍCIOS:
    - Centraliza lógica de criação
    - Valida dados antes da criação
    - Facilita extensão de novos tipos
    """
    
    @staticmethod
    def criar_produto_fisico(nome: str, descricao: str, preco: Dinheiro,
                           categoria: str, fabricante: str, dimensoes: dict,
                           estoque: int = 0) -> ProdutoFisico:
        """Cria produto físico com validações"""
        from domain.value_objects import DimensoesProduto
        
        # Criar dimensões
        dims = DimensoesProduto(
            altura=Decimal(str(dimensoes['altura'])),
            largura=Decimal(str(dimensoes['largura'])),
            profundidade=Decimal(str(dimensoes['profundidade'])),
            peso=Decimal(str(dimensoes['peso']))
        )
        
        produto = ProdutoFisico(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            fabricante=fabricante,
            dimensoes=dims,
            quantidade_estoque=estoque
        )
        
        logging.info(f"Produto físico criado: {produto.nome}")
        return produto
    
    @staticmethod
    def criar_produto_digital(nome: str, descricao: str, preco: Dinheiro,
                            categoria: str, fabricante: str, info_digital: dict,
                            licencas: int = -1) -> ProdutoDigital:
        """Cria produto digital com validações"""
        from domain.value_objects import InformacaoDigital
        
        # Criar informações digitais
        info = InformacaoDigital(
            tamanho_arquivo_mb=Decimal(str(info_digital['tamanho_mb'])),
            formato=info_digital['formato'],
            url_download=info_digital['url_download'],
            chave_licenca=info_digital.get('chave_licenca')
        )
        
        produto = ProdutoDigital(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            fabricante=fabricante,
            info_digital=info,
            licencas_disponiveis=licencas
        )
        
        logging.info(f"Produto digital criado: {produto.nome}")
        return produto
    
    @staticmethod
    def criar_produto_servico(nome: str, descricao: str, preco: Dinheiro,
                            categoria: str, fabricante: str, info_servico: dict,
                            profissionais: int = 1) -> ProdutoServico:
        """Cria produto de serviço com validações"""
        from domain.value_objects import InformacaoServico
        
        # Criar informações do serviço
        info = InformacaoServico(
            duracao_horas=Decimal(str(info_servico['duracao_horas'])),
            categoria=info_servico['categoria'],
            requer_presenca=info_servico.get('requer_presenca', False)
        )
        
        produto = ProdutoServico(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            fabricante=fabricante,
            info_servico=info,
            profissionais_disponiveis=profissionais
        )
        
        logging.info(f"Produto de serviço criado: {produto.nome}")
        return produto


# =============================================================================
# SERVIÇOS DE APLICAÇÃO
# =============================================================================

class ServicoGestãoProdutos:
    """
    ✅ Serviço para gestão de produtos
    
    RESPONSABILIDADES:
    - CRUD de produtos
    - Validações de negócio
    - Gestão de estoque
    """
    
    def __init__(self, repositorio: RepositorioProduto):
        self._repositorio = repositorio
        self._fabrica = FabricaProdutos()
    
    def criar_produto(self, tipo: TipoProduto, dados: Dict[str, Any]) -> Produto:
        """Cria produto baseado no tipo"""
        if tipo == TipoProduto.FISICO:
            produto = self._fabrica.criar_produto_fisico(**dados)
        elif tipo == TipoProduto.DIGITAL:
            produto = self._fabrica.criar_produto_digital(**dados)
        elif tipo == TipoProduto.SERVICO:
            produto = self._fabrica.criar_produto_servico(**dados)
        else:
            raise ValueError(f"Tipo de produto não suportado: {tipo}")
        
        self._repositorio.salvar(produto)
        return produto
    
    def atualizar_preco(self, produto_id: UUID, novo_preco: Dinheiro) -> bool:
        """Atualiza preço de um produto"""
        produto = self._repositorio.buscar_por_id(produto_id)
        if not produto:
            return False
        
        produto.atualizar_preco(novo_preco)
        self._repositorio.salvar(produto)
        
        logging.info(f"Preço do produto {produto.nome} atualizado para {novo_preco}")
        return True
    
    def adicionar_estoque(self, produto_id: UUID, quantidade: int) -> bool:
        """Adiciona estoque a produto físico"""
        produto = self._repositorio.buscar_por_id(produto_id)
        if not produto or not isinstance(produto, ProdutoFisico):
            return False
        
        produto.adicionar_estoque(quantidade)
        self._repositorio.salvar(produto)
        
        logging.info(f"Adicionado estoque: {quantidade} unidades de {produto.nome}")
        return True
    
    def buscar_produtos_disponiveis(self, categoria: Optional[str] = None) -> List[Produto]:
        """Busca produtos disponíveis, opcionalmente por categoria"""
        if categoria:
            produtos = self._repositorio.buscar_por_categoria(categoria)
            return [p for p in produtos if p.esta_disponivel()]
        
        return self._repositorio.buscar_disponiveis()
    
    def verificar_estoque_baixo(self) -> List[ProdutoFisico]:
        """Verifica produtos com estoque baixo"""
        produtos = self._repositorio.buscar_disponiveis()
        produtos_baixo_estoque = []
        
        for produto in produtos:
            if isinstance(produto, ProdutoFisico) and produto.esta_em_falta():
                produtos_baixo_estoque.append(produto)
        
        return produtos_baixo_estoque


class ServicoGestãoClientes:
    """
    ✅ Serviço para gestão de clientes
    
    RESPONSABILIDADES:
    - CRUD de clientes
    - Análise de comportamento
    - Segmentação de clientes
    """
    
    def __init__(self, repositorio: RepositorioCliente):
        self._repositorio = repositorio
    
    def criar_cliente(self, nome: str, email: str, telefone: str,
                     endereco: Endereco) -> Cliente:
        """Cria novo cliente"""
        # Verificar se email já existe
        cliente_existente = self._repositorio.buscar_por_email(email)
        if cliente_existente:
            raise ValueError(f"Cliente com email {email} já existe")
        
        cliente = Cliente(nome, email, telefone, endereco)
        self._repositorio.salvar(cliente)
        
        logging.info(f"Cliente criado: {cliente.nome} ({cliente.email})")
        return cliente
    
    def atualizar_dados_cliente(self, cliente_id: UUID, dados: Dict[str, Any]) -> bool:
        """Atualiza dados do cliente"""
        cliente = self._repositorio.buscar_por_id(cliente_id)
        if not cliente:
            return False
        
        if 'email' in dados:
            cliente.atualizar_email(dados['email'])
        
        if 'telefone' in dados:
            cliente.atualizar_telefone(dados['telefone'])
        
        if 'endereco' in dados:
            cliente.adicionar_endereco(dados['endereco'])
        
        if 'notificacoes' in dados:
            cliente.configurar_notificacoes(dados['notificacoes'])
        
        self._repositorio.salvar(cliente)
        return True
    
    def obter_clientes_vip(self) -> List[Cliente]:
        """Retorna lista de clientes VIP"""
        clientes = self._repositorio.buscar_ativos()
        return [c for c in clientes if c.eh_cliente_vip()]
    
    def obter_clientes_inativos(self, dias_limite: int = 90) -> List[Cliente]:
        """Retorna clientes sem compra recente"""
        clientes = self._repositorio.buscar_ativos()
        clientes_inativos = []
        
        for cliente in clientes:
            dias_ultima_compra = cliente.dias_desde_ultima_compra()
            if dias_ultima_compra and dias_ultima_compra > dias_limite:
                clientes_inativos.append(cliente)
        
        return clientes_inativos
    
    def calcular_segmentacao(self) -> Dict[str, List[Cliente]]:
        """Segmenta clientes por comportamento"""
        clientes = self._repositorio.buscar_ativos()
        
        segmentacao = {
            'vip': [],
            'ativos': [],
            'novos': [],
            'inativos': []
        }
        
        for cliente in clientes:
            if cliente.eh_cliente_vip():
                segmentacao['vip'].append(cliente)
            elif cliente.numero_pedidos == 0:
                segmentacao['novos'].append(cliente)
            elif cliente.dias_desde_ultima_compra() and cliente.dias_desde_ultima_compra() > 90:
                segmentacao['inativos'].append(cliente)
            else:
                segmentacao['ativos'].append(cliente)
        
        return segmentacao


class ServicoProcessamentoPedidos:
    """
    ✅ Serviço para processamento de pedidos
    
    RESPONSABILIDADES:
    - Criação e gestão de pedidos
    - Aplicação de descontos
    - Coordenação de pagamento e entrega
    """
    
    def __init__(self, repositorio_pedido: RepositorioPedido,
                 repositorio_produto: RepositorioProduto,
                 repositorio_cliente: RepositorioCliente,
                 gateway_pagamento: GatewayPagamento,
                 servico_frete: ServicoFrete):
        self._repo_pedido = repositorio_pedido
        self._repo_produto = repositorio_produto
        self._repo_cliente = repositorio_cliente
        self._gateway_pagamento = gateway_pagamento
        self._servico_frete = servico_frete
        
        # Estratégias de desconto
        self._estrategias_desconto: List[EstrategiaDesconto] = [
            DescontoClienteVIP(),
            DescontoPrimeiraCompra(),
            DescontoCompraAcima(Dinheiro(Decimal('200')), Decimal('5'))
        ]
    
    def criar_pedido(self, cliente_id: UUID, endereco_entrega: Endereco) -> Pedido:
        """Cria novo pedido"""
        cliente = self._repo_cliente.buscar_por_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        if not cliente.ativo:
            raise ValueError("Cliente inativo não pode fazer pedidos")
        
        pedido = Pedido(cliente_id, endereco_entrega)
        self._repo_pedido.salvar(pedido)
        
        logging.info(f"Pedido criado: {pedido.id} para cliente {cliente.nome}")
        return pedido
    
    def adicionar_item_pedido(self, pedido_id: UUID, produto_id: UUID, quantidade: int) -> bool:
        """Adiciona item ao pedido"""
        pedido = self._repo_pedido.buscar_por_id(pedido_id)
        produto = self._repo_produto.buscar_por_id(produto_id)
        
        if not pedido or not produto:
            return False
        
        if not produto.esta_disponivel():
            raise ValueError(f"Produto {produto.nome} não está disponível")
        
        # Verificar estoque para produtos físicos
        if isinstance(produto, ProdutoFisico):
            if produto.quantidade_estoque < quantidade:
                raise ValueError(f"Estoque insuficiente. Disponível: {produto.quantidade_estoque}")
        
        pedido.adicionar_item(produto, quantidade)
        self._repo_pedido.salvar(pedido)
        
        return True
    
    def calcular_frete(self, pedido_id: UUID) -> Optional[ResultadoCalculoFrete]:
        """Calcula frete para pedido"""
        pedido = self._repo_pedido.buscar_por_id(pedido_id)
        if not pedido:
            return None
        
        # Para produtos físicos, calcular frete
        for item in pedido.itens:
            produto = self._repo_produto.buscar_por_id(item.produto_id)
            if isinstance(produto, ProdutoFisico):
                resultado_frete = self._servico_frete.calcular_frete(produto, pedido.endereco_entrega)
                pedido.definir_frete(resultado_frete.valor)
                self._repo_pedido.salvar(pedido)
                return resultado_frete
        
        # Sem produtos físicos = frete grátis
        return ResultadoCalculoFrete(
            valor=Dinheiro(Decimal('0')),
            prazo_dias=0,
            transportadora="Digital",
            servico="Download",
            detalhes="Produtos digitais - sem frete"
        )
    
    def aplicar_melhor_desconto(self, pedido_id: UUID) -> Dinheiro:
        """Aplica melhor desconto disponível"""
        pedido = self._repo_pedido.buscar_por_id(pedido_id)
        cliente = self._repo_cliente.buscar_por_id(pedido.cliente_id)
        
        if not pedido or not cliente:
            return Dinheiro(Decimal('0'))
        
        melhor_desconto = Dinheiro(Decimal('0'))
        
        for estrategia in self._estrategias_desconto:
            if estrategia.eh_aplicavel(pedido, cliente):
                desconto = estrategia.calcular_desconto(pedido, cliente)
                if desconto.eh_maior_que(melhor_desconto):
                    melhor_desconto = desconto
        
        if not melhor_desconto.eh_zero():
            pedido.aplicar_desconto_geral(melhor_desconto)
            self._repo_pedido.salvar(pedido)
            logging.info(f"Desconto aplicado: {melhor_desconto} no pedido {pedido_id}")
        
        return melhor_desconto
    
    def processar_pagamento(self, pedido_id: UUID, dados_pagamento: DadosPagamento) -> bool:
        """Processa pagamento do pedido"""
        pedido = self._repo_pedido.buscar_por_id(pedido_id)
        if not pedido:
            return False
        
        if pedido.status != StatusPedido.CONFIRMADO:
            raise ValueError("Pedido deve estar confirmado para processar pagamento")
        
        valor_total = pedido.calcular_total()
        
        try:
            # Processar pagamento via gateway
            resultado = self._gateway_pagamento.processar_pagamento(dados_pagamento, valor_total)
            
            if resultado.get('sucesso'):
                pedido.processar_pagamento(dados_pagamento, valor_total)
                
                # Consumir estoque/licenças
                self._consumir_recursos_pedido(pedido)
                
                # Atualizar histórico do cliente
                cliente = self._repo_cliente.buscar_por_id(pedido.cliente_id)
                if cliente:
                    cliente.registrar_compra(valor_total)
                    self._repo_cliente.salvar(cliente)
                
                self._repo_pedido.salvar(pedido)
                logging.info(f"Pagamento processado com sucesso para pedido {pedido_id}")
                return True
            
        except Exception as e:
            logging.error(f"Erro no processamento de pagamento: {e}")
        
        return False
    
    def _consumir_recursos_pedido(self, pedido: Pedido) -> None:
        """Consome estoque/licenças dos produtos do pedido"""
        for item in pedido.itens:
            produto = self._repo_produto.buscar_por_id(item.produto_id)
            
            if isinstance(produto, ProdutoFisico):
                produto.remover_estoque(item.quantidade)
            elif isinstance(produto, ProdutoDigital):
                for _ in range(item.quantidade):
                    produto.consumir_licenca()
            elif isinstance(produto, ProdutoServico):
                produto.agendar_servico()
            
            self._repo_produto.salvar(produto)
    
    def obter_pedidos_pendentes(self) -> List[Pedido]:
        """Retorna pedidos pendentes de processamento"""
        return self._repo_pedido.buscar_por_status(StatusPedido.CONFIRMADO)
    
    def obter_relatorio_vendas(self, data_inicio: datetime, data_fim: datetime) -> Dict[str, Any]:
        """Gera relatório de vendas do período"""
        # Implementação simplificada
        pedidos_entregues = self._repo_pedido.buscar_por_status(StatusPedido.ENTREGUE)
        
        valor_total = Dinheiro(Decimal('0'))
        quantidade_pedidos = 0
        
        for pedido in pedidos_entregues:
            if data_inicio <= pedido.data_pedido <= data_fim:
                valor_total = valor_total.somar(pedido.calcular_total())
                quantidade_pedidos += 1
        
        ticket_medio = (valor_total.valor / Decimal(str(quantidade_pedidos)) 
                       if quantidade_pedidos > 0 else Decimal('0'))
        
        return {
            'periodo': f"{data_inicio.date()} a {data_fim.date()}",
            'valor_total': valor_total,
            'quantidade_pedidos': quantidade_pedidos,
            'ticket_medio': Dinheiro(ticket_medio)
        }


class ServicoNotificacoes:
    """
    ✅ Serviço de notificações (Observer Pattern)
    
    RESPONSABILIDADES:
    - Escutar eventos de domínio
    - Enviar notificações apropriadas
    - Gerenciar preferências de cliente
    """
    
    def __init__(self, gateway_notificacao: GatewayNotificacao,
                 repositorio_cliente: RepositorioCliente):
        self._gateway = gateway_notificacao
        self._repo_cliente = repositorio_cliente
    
    def processar_evento(self, evento: EventoDominio) -> None:
        """Processa evento de domínio e envia notificações"""
        from domain.entities import PedidoCriado, StatusPedidoAlterado, PagamentoProcessado
        
        if isinstance(evento, PedidoCriado):
            self._notificar_pedido_criado(evento)
        elif isinstance(evento, StatusPedidoAlterado):
            self._notificar_status_alterado(evento)
        elif isinstance(evento, PagamentoProcessado):
            self._notificar_pagamento_processado(evento)
    
    def _notificar_pedido_criado(self, evento) -> None:
        """Notifica criação de pedido"""
        cliente = self._repo_cliente.buscar_por_id(evento.cliente_id)
        if not cliente:
            return
        
        preferencias = cliente.obter_preferencias_notificacao()
        
        assunto = "Pedido Criado com Sucesso"
        mensagem = f"Olá {cliente.nome}, seu pedido {evento.pedido_id} foi criado e está sendo processado."
        
        for tipo in preferencias:
            destinatario = cliente.email if tipo == TipoNotificacao.EMAIL else cliente.telefone
            self._gateway.enviar_notificacao(destinatario, tipo, assunto, mensagem)
    
    def _notificar_status_alterado(self, evento) -> None:
        """Notifica mudança de status"""
        # Implementação similar aos outros métodos
        logging.info(f"Status do pedido {evento.pedido_id} alterado para {evento.status_novo.value}")
    
    def _notificar_pagamento_processado(self, evento) -> None:
        """Notifica processamento de pagamento"""
        logging.info(f"Pagamento de {evento.valor} processado para pedido {evento.pedido_id}")


# =============================================================================
# EXPORTAÇÕES
# =============================================================================

__all__ = [
    # Interfaces de repositório
    'RepositorioProduto', 'RepositorioCliente', 'RepositorioPedido',
    
    # Interfaces de gateway
    'GatewayPagamento', 'GatewayNotificacao', 'ServicoFrete',
    
    # Estratégias
    'EstrategiaDesconto', 'DescontoClienteVIP', 'DescontoPrimeiraCompra', 'DescontoCompraAcima',
    
    # Factory
    'FabricaProdutos',
    
    # Serviços
    'ServicoGestãoProdutos', 'ServicoGestãoClientes', 'ServicoProcessamentoPedidos', 'ServicoNotificacoes'
]
