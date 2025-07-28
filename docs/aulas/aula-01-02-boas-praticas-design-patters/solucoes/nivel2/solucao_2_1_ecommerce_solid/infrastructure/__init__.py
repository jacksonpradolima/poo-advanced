#!/usr/bin/env python3
"""
Infraestrutura - Implementações Concretas

RESPONSABILIDADE: Implementações concretas de interfaces de infraestrutura,
incluindo repositórios, gateways e adaptadores externos.

PRINCÍPIOS SOLID APLICADOS:
- SRP: Cada implementação tem responsabilidade específica
- OCP: Novas implementações podem ser adicionadas
- LSP: Implementações respeitam contratos das interfaces
- ISP: Interfaces pequenas e focadas
- DIP: Implementa abstrações definidas na camada de serviços

PADRÕES DE DESIGN:
- Adapter: Adaptação de APIs externas
- Repository: Persistência de dados
- Factory: Criação de objetos de infraestrutura

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
import logging
import json
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import Produto, Cliente, Pedido
from domain.value_objects import (
    Dinheiro, Endereco, ResultadoCalculoFrete, DadosPagamento,
    TipoNotificacao, StatusPedido
)
from services import (
    RepositorioProduto, RepositorioCliente, RepositorioPedido,
    GatewayPagamento, GatewayNotificacao, ServicoFrete
)


# =============================================================================
# REPOSITÓRIOS EM MEMÓRIA (Adapter Pattern)
# =============================================================================

class RepositorioProdutoMemoria(RepositorioProduto):
    """
    ✅ Implementação em memória do repositório de produtos
    
    BENEFÍCIOS:
    - Simples para testes e demonstrações
    - Implementa completamente a interface
    - Permite validação da arquitetura
    """
    
    def __init__(self):
        self._produtos: Dict[UUID, Produto] = {}
        logging.info("Repositório de produtos em memória inicializado")
    
    def salvar(self, produto: Produto) -> None:
        """Salva produto na 'base de dados' em memória"""
        self._produtos[produto.id] = produto
        logging.debug(f"Produto salvo: {produto.nome} (ID: {produto.id})")
    
    def buscar_por_id(self, produto_id: UUID) -> Optional[Produto]:
        """Busca produto por ID"""
        produto = self._produtos.get(produto_id)
        if produto:
            logging.debug(f"Produto encontrado: {produto.nome}")
        else:
            logging.debug(f"Produto não encontrado: {produto_id}")
        return produto
    
    def buscar_por_categoria(self, categoria: str) -> List[Produto]:
        """Busca produtos por categoria"""
        produtos_categoria = [
            produto for produto in self._produtos.values()
            if produto.categoria.lower() == categoria.lower()
        ]
        logging.debug(f"Encontrados {len(produtos_categoria)} produtos na categoria '{categoria}'")
        return produtos_categoria
    
    def buscar_disponiveis(self) -> List[Produto]:
        """Busca produtos disponíveis para venda"""
        produtos_disponiveis = [
            produto for produto in self._produtos.values()
            if produto.esta_disponivel()
        ]
        logging.debug(f"Encontrados {len(produtos_disponiveis)} produtos disponíveis")
        return produtos_disponiveis
    
    def excluir(self, produto_id: UUID) -> bool:
        """Exclui produto por ID"""
        if produto_id in self._produtos:
            produto = self._produtos.pop(produto_id)
            logging.info(f"Produto excluído: {produto.nome}")
            return True
        
        logging.warning(f"Tentativa de excluir produto inexistente: {produto_id}")
        return False
    
    def obter_todos(self) -> List[Produto]:
        """Método auxiliar para testes - retorna todos os produtos"""
        return list(self._produtos.values())
    
    def limpar(self) -> None:
        """Método auxiliar para testes - limpa repositório"""
        self._produtos.clear()
        logging.info("Repositório de produtos limpo")


class RepositorioClienteMemoria(RepositorioCliente):
    """
    ✅ Implementação em memória do repositório de clientes
    """
    
    def __init__(self):
        self._clientes: Dict[UUID, Cliente] = {}
        self._indice_email: Dict[str, UUID] = {}  # Índice para busca por email
        logging.info("Repositório de clientes em memória inicializado")
    
    def salvar(self, cliente: Cliente) -> None:
        """Salva cliente e atualiza índices"""
        self._clientes[cliente.id] = cliente
        self._indice_email[cliente.email.lower()] = cliente.id
        logging.debug(f"Cliente salvo: {cliente.nome} ({cliente.email})")
    
    def buscar_por_id(self, cliente_id: UUID) -> Optional[Cliente]:
        """Busca cliente por ID"""
        cliente = self._clientes.get(cliente_id)
        if cliente:
            logging.debug(f"Cliente encontrado: {cliente.nome}")
        else:
            logging.debug(f"Cliente não encontrado: {cliente_id}")
        return cliente
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        cliente_id = self._indice_email.get(email.lower())
        if cliente_id:
            return self._clientes.get(cliente_id)
        
        logging.debug(f"Cliente não encontrado com email: {email}")
        return None
    
    def buscar_ativos(self) -> List[Cliente]:
        """Busca clientes ativos"""
        clientes_ativos = [
            cliente for cliente in self._clientes.values()
            if cliente.ativo
        ]
        logging.debug(f"Encontrados {len(clientes_ativos)} clientes ativos")
        return clientes_ativos
    
    def obter_todos(self) -> List[Cliente]:
        """Método auxiliar para testes"""
        return list(self._clientes.values())
    
    def limpar(self) -> None:
        """Método auxiliar para testes"""
        self._clientes.clear()
        self._indice_email.clear()
        logging.info("Repositório de clientes limpo")


class RepositorioPedidoMemoria(RepositorioPedido):
    """
    ✅ Implementação em memória do repositório de pedidos
    """
    
    def __init__(self):
        self._pedidos: Dict[UUID, Pedido] = {}
        self._indice_cliente: Dict[UUID, List[UUID]] = {}  # Cliente -> Lista de Pedidos
        self._indice_status: Dict[StatusPedido, List[UUID]] = {}  # Status -> Lista de Pedidos
        logging.info("Repositório de pedidos em memória inicializado")
    
    def salvar(self, pedido: Pedido) -> None:
        """Salva pedido e atualiza índices"""
        self._pedidos[pedido.id] = pedido
        
        # Atualizar índice por cliente
        if pedido.cliente_id not in self._indice_cliente:
            self._indice_cliente[pedido.cliente_id] = []
        
        if pedido.id not in self._indice_cliente[pedido.cliente_id]:
            self._indice_cliente[pedido.cliente_id].append(pedido.id)
        
        # Atualizar índice por status
        if pedido.status not in self._indice_status:
            self._indice_status[pedido.status] = []
        
        # Remover de status antigo se necessário
        for status, pedidos_status in self._indice_status.items():
            if status != pedido.status and pedido.id in pedidos_status:
                pedidos_status.remove(pedido.id)
        
        if pedido.id not in self._indice_status[pedido.status]:
            self._indice_status[pedido.status].append(pedido.id)
        
        logging.debug(f"Pedido salvo: {pedido.id} (Status: {pedido.status.value})")
    
    def buscar_por_id(self, pedido_id: UUID) -> Optional[Pedido]:
        """Busca pedido por ID"""
        pedido = self._pedidos.get(pedido_id)
        if pedido:
            logging.debug(f"Pedido encontrado: {pedido.id}")
        else:
            logging.debug(f"Pedido não encontrado: {pedido_id}")
        return pedido
    
    def buscar_por_cliente(self, cliente_id: UUID) -> List[Pedido]:
        """Busca pedidos de um cliente"""
        pedidos_ids = self._indice_cliente.get(cliente_id, [])
        pedidos = [self._pedidos[pid] for pid in pedidos_ids if pid in self._pedidos]
        logging.debug(f"Encontrados {len(pedidos)} pedidos para cliente {cliente_id}")
        return pedidos
    
    def buscar_por_status(self, status: StatusPedido) -> List[Pedido]:
        """Busca pedidos por status"""
        pedidos_ids = self._indice_status.get(status, [])
        pedidos = [self._pedidos[pid] for pid in pedidos_ids if pid in self._pedidos]
        logging.debug(f"Encontrados {len(pedidos)} pedidos com status {status.value}")
        return pedidos
    
    def obter_todos(self) -> List[Pedido]:
        """Método auxiliar para testes"""
        return list(self._pedidos.values())
    
    def limpar(self) -> None:
        """Método auxiliar para testes"""
        self._pedidos.clear()
        self._indice_cliente.clear()
        self._indice_status.clear()
        logging.info("Repositório de pedidos limpo")


# =============================================================================
# GATEWAYS SIMULADOS (Adapter Pattern)
# =============================================================================

class GatewayPagamentoSimulado(GatewayPagamento):
    """
    ✅ Gateway de pagamento simulado para demonstração
    
    COMPORTAMENTO:
    - Simula processamento de pagamento
    - Pode simular falhas baseado em regras
    - Registra tentativas para auditoria
    """
    
    def __init__(self, taxa_sucesso: float = 0.95):
        self._taxa_sucesso = taxa_sucesso
        self._transacoes: Dict[str, Dict[str, Any]] = {}
        self._contador_transacao = 1
        logging.info(f"Gateway de pagamento simulado inicializado (Taxa sucesso: {taxa_sucesso})")
    
    def processar_pagamento(self, dados: DadosPagamento, valor: Dinheiro) -> Dict[str, Any]:
        """
        Simula processamento de pagamento
        
        REGRAS DE SIMULAÇÃO:
        - Cartões terminados em 0000: sempre falham
        - Valores acima de R$ 10.000: falham (limite)
        - Demais casos: sucesso baseado na taxa configurada
        """
        transacao_id = f"TXN{self._contador_transacao:06d}"
        self._contador_transacao += 1
        
        # Simular validações
        numero_cartao = dados.numero_cartao.replace(' ', '')
        
        # Regras de falha
        if numero_cartao.endswith('0000'):
            resultado = {
                'sucesso': False,
                'transacao_id': transacao_id,
                'motivo': 'Cartão bloqueado',
                'timestamp': datetime.now().isoformat()
            }
        elif valor.eh_maior_que(Dinheiro(Decimal('10000'))):
            resultado = {
                'sucesso': False,
                'transacao_id': transacao_id,
                'motivo': 'Valor acima do limite',
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Simular sucesso baseado na taxa
            import random
            sucesso = random.random() < self._taxa_sucesso
            
            resultado = {
                'sucesso': sucesso,
                'transacao_id': transacao_id,
                'motivo': 'Processado com sucesso' if sucesso else 'Falha na comunicação',
                'timestamp': datetime.now().isoformat(),
                'valor': str(valor.valor),
                'moeda': valor.moeda
            }
        
        # Registrar transação
        self._transacoes[transacao_id] = {
            **resultado,
            'dados_cartao_mascarado': dados.obter_numero_mascarado()
        }
        
        if resultado['sucesso']:
            logging.info(f"Pagamento processado: {transacao_id} - {valor}")
        else:
            logging.warning(f"Falha no pagamento: {transacao_id} - {resultado['motivo']}")
        
        return resultado
    
    def estornar_pagamento(self, transacao_id: str, valor: Dinheiro) -> Dict[str, Any]:
        """Simula estorno de pagamento"""
        if transacao_id not in self._transacoes:
            return {
                'sucesso': False,
                'motivo': 'Transação não encontrada'
            }
        
        transacao_original = self._transacoes[transacao_id]
        if not transacao_original['sucesso']:
            return {
                'sucesso': False,
                'motivo': 'Não é possível estornar transação falhada'
            }
        
        estorno_id = f"EST{self._contador_transacao:06d}"
        self._contador_transacao += 1
        
        resultado = {
            'sucesso': True,
            'estorno_id': estorno_id,
            'transacao_original': transacao_id,
            'valor_estornado': str(valor.valor),
            'timestamp': datetime.now().isoformat()
        }
        
        self._transacoes[estorno_id] = resultado
        logging.info(f"Estorno processado: {estorno_id} para transação {transacao_id}")
        
        return resultado
    
    def obter_historico_transacoes(self) -> List[Dict[str, Any]]:
        """Retorna histórico de transações (para auditoria)"""
        return list(self._transacoes.values())


class GatewayNotificacaoSimulado(GatewayNotificacao):
    """
    ✅ Gateway de notificação simulado
    
    COMPORTAMENTO:
    - Simula envio de notificações
    - Registra todas as tentativas
    - Diferentes comportamentos por tipo de notificação
    """
    
    def __init__(self):
        self._notificacoes_enviadas: List[Dict[str, Any]] = []
        self._falhas_simuladas = {
            TipoNotificacao.SMS: 0.1,  # 10% de falha
            TipoNotificacao.EMAIL: 0.05,  # 5% de falha
            TipoNotificacao.PUSH: 0.15   # 15% de falha
        }
        logging.info("Gateway de notificação simulado inicializado")
    
    def enviar_notificacao(self, destinatario: str, tipo: TipoNotificacao,
                          assunto: str, mensagem: str) -> bool:
        """Simula envio de notificação"""
        import random
        
        # Simular falha baseada no tipo
        taxa_falha = self._falhas_simuladas.get(tipo, 0.05)
        sucesso = random.random() > taxa_falha
        
        notificacao = {
            'destinatario': destinatario,
            'tipo': tipo.value,
            'assunto': assunto,
            'mensagem': mensagem,
            'sucesso': sucesso,
            'timestamp': datetime.now().isoformat(),
            'tentativas': 1
        }
        
        # Se falhou, simular nova tentativa
        if not sucesso:
            sucesso_retry = random.random() > (taxa_falha / 2)  # Menor chance de falha
            notificacao['sucesso'] = sucesso_retry
            notificacao['tentativas'] = 2
            
            if sucesso_retry:
                logging.info(f"Notificação enviada na 2ª tentativa: {tipo.value} para {destinatario}")
            else:
                logging.error(f"Falha ao enviar notificação: {tipo.value} para {destinatario}")
        else:
            logging.info(f"Notificação enviada: {tipo.value} para {destinatario}")
        
        self._notificacoes_enviadas.append(notificacao)
        return notificacao['sucesso']
    
    def obter_historico_notificacoes(self) -> List[Dict[str, Any]]:
        """Retorna histórico de notificações"""
        return self._notificacoes_enviadas.copy()
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Calcula estatísticas de envio"""
        if not self._notificacoes_enviadas:
            return {'total': 0, 'sucesso': 0, 'falha': 0, 'taxa_sucesso': 0.0}
        
        total = len(self._notificacoes_enviadas)
        sucessos = sum(1 for n in self._notificacoes_enviadas if n['sucesso'])
        falhas = total - sucessos
        taxa_sucesso = (sucessos / total) * 100
        
        return {
            'total': total,
            'sucesso': sucessos,
            'falha': falhas,
            'taxa_sucesso': round(taxa_sucesso, 2)
        }


class ServicoFreteSimulado(ServicoFrete):
    """
    ✅ Serviço de cálculo de frete simulado
    
    COMPORTAMENTO:
    - Calcula frete baseado em regras simplificadas
    - Simula diferentes transportadoras
    - Considera peso, dimensões e distância
    """
    
    def __init__(self):
        self._transportadoras = {
            'correios_pac': {
                'nome': 'Correios',
                'servico': 'PAC',
                'valor_base': Decimal('15.00'),
                'valor_por_kg': Decimal('3.50'),
                'prazo_base': 7,
                'limite_peso': Decimal('30')
            },
            'correios_sedex': {
                'nome': 'Correios',
                'servico': 'SEDEX',
                'valor_base': Decimal('25.00'),
                'valor_por_kg': Decimal('5.00'),
                'prazo_base': 3,
                'limite_peso': Decimal('30')
            },
            'transportadora_expressa': {
                'nome': 'Expressa Ltda',
                'servico': 'Entrega Rápida',
                'valor_base': Decimal('35.00'),
                'valor_por_kg': Decimal('4.00'),
                'prazo_base': 2,
                'limite_peso': Decimal('50')
            }
        }
        logging.info("Serviço de frete simulado inicializado")
    
    def calcular_frete(self, produto: 'ProdutoFisico', endereco_destino: Endereco) -> ResultadoCalculoFrete:
        """
        Calcula frete usando regras simplificadas
        
        ALGORITMO:
        1. Calcula peso volumétrico
        2. Usa maior peso (real ou volumétrico)
        3. Determina distância por região
        4. Aplica regras da transportadora
        """
        from domain.entities import ProdutoFisico
        
        # Calcular peso efetivo (maior entre real e volumétrico)
        peso_real = produto.dimensoes.peso
        peso_volumetrico = produto.dimensoes.calcular_peso_volumetrico()
        peso_efetivo = max(peso_real, peso_volumetrico)
        
        # Determinar região para cálculo de distância
        regiao_destino = endereco_destino.obter_regiao()
        fator_distancia = self._obter_fator_distancia(regiao_destino)
        
        # Escolher melhor transportadora baseada no peso
        melhor_opcao = None
        melhor_custo = None
        
        for codigo, transportadora in self._transportadoras.items():
            if peso_efetivo <= transportadora['limite_peso']:
                custo = self._calcular_custo_transportadora(
                    transportadora, peso_efetivo, fator_distancia
                )
                
                if melhor_custo is None or custo['valor'].eh_menor_que(melhor_custo['valor']):
                    melhor_custo = custo
                    melhor_opcao = transportadora
        
        if not melhor_opcao:
            # Produto muito pesado - usar transportadora especializada
            melhor_opcao = self._transportadoras['transportadora_expressa']
            melhor_custo = {
                'valor': Dinheiro(peso_efetivo * Decimal('8.00')),  # Valor especial
                'prazo': 5
            }
        
        resultado = ResultadoCalculoFrete(
            valor=melhor_custo['valor'],
            prazo_dias=melhor_custo['prazo'],
            transportadora=melhor_opcao['nome'],
            servico=melhor_opcao['servico'],
            detalhes=f"Peso: {peso_efetivo}kg, Região: {regiao_destino}"
        )
        
        logging.info(f"Frete calculado: {resultado}")
        return resultado
    
    def _obter_fator_distancia(self, regiao: str) -> Decimal:
        """Calcula fator de distância baseado na região"""
        fatores = {
            'Sudeste': Decimal('1.0'),
            'Sul': Decimal('1.2'),
            'Centro-Oeste': Decimal('1.4'),
            'Nordeste': Decimal('1.6'),
            'Norte': Decimal('2.0')
        }
        return fatores.get(regiao, Decimal('1.5'))
    
    def _calcular_custo_transportadora(self, transportadora: Dict[str, Any],
                                     peso: Decimal, fator_distancia: Decimal) -> Dict[str, Any]:
        """Calcula custo específico da transportadora"""
        valor_base = transportadora['valor_base']
        valor_peso = peso * transportadora['valor_por_kg']
        valor_distancia = valor_base * (fator_distancia - Decimal('1.0'))
        
        valor_total = valor_base + valor_peso + valor_distancia
        prazo_total = int(transportadora['prazo_base'] * float(fator_distancia))
        
        return {
            'valor': Dinheiro(valor_total),
            'prazo': prazo_total
        }
    
    def obter_opcoes_frete(self, produto: 'ProdutoFisico', endereco_destino: Endereco) -> List[ResultadoCalculoFrete]:
        """Retorna todas as opções de frete disponíveis"""
        peso_efetivo = max(produto.dimensoes.peso, produto.dimensoes.calcular_peso_volumetrico())
        fator_distancia = self._obter_fator_distancia(endereco_destino.obter_regiao())
        
        opcoes = []
        
        for transportadora in self._transportadoras.values():
            if peso_efetivo <= transportadora['limite_peso']:
                custo = self._calcular_custo_transportadora(transportadora, peso_efetivo, fator_distancia)
                
                opcao = ResultadoCalculoFrete(
                    valor=custo['valor'],
                    prazo_dias=custo['prazo'],
                    transportadora=transportadora['nome'],
                    servico=transportadora['servico'],
                    detalhes=f"Peso: {peso_efetivo}kg"
                )
                opcoes.append(opcao)
        
        # Ordenar por preço
        opcoes.sort(key=lambda x: x.valor.valor)
        return opcoes


# =============================================================================
# FACTORY DE INFRAESTRUTURA
# =============================================================================

class FabricaInfraestrutura:
    """
    ✅ Factory para criação de objetos de infraestrutura
    
    BENEFÍCIOS:
    - Centraliza configuração de dependências
    - Facilita troca de implementações
    - Suporte a diferentes ambientes (dev, teste, produção)
    """
    
    @staticmethod
    def criar_repositorios_memoria() -> Dict[str, Any]:
        """Cria repositórios em memória para testes/demo"""
        return {
            'produtos': RepositorioProdutoMemoria(),
            'clientes': RepositorioClienteMemoria(),
            'pedidos': RepositorioPedidoMemoria()
        }
    
    @staticmethod
    def criar_gateways_simulados(taxa_sucesso_pagamento: float = 0.95) -> Dict[str, Any]:
        """Cria gateways simulados para testes/demo"""
        return {
            'pagamento': GatewayPagamentoSimulado(taxa_sucesso_pagamento),
            'notificacao': GatewayNotificacaoSimulado(),
            'frete': ServicoFreteSimulado()
        }
    
    @staticmethod
    def criar_infraestrutura_completa(taxa_sucesso_pagamento: float = 0.95) -> Dict[str, Any]:
        """Cria infraestrutura completa para demonstração"""
        infraestrutura = {}
        
        # Repositórios
        repositorios = FabricaInfraestrutura.criar_repositorios_memoria()
        infraestrutura.update(repositorios)
        
        # Gateways
        gateways = FabricaInfraestrutura.criar_gateways_simulados(taxa_sucesso_pagamento)
        infraestrutura.update(gateways)
        
        logging.info("Infraestrutura completa criada com implementações simuladas")
        return infraestrutura


# =============================================================================
# EXPORTAÇÕES
# =============================================================================

__all__ = [
    # Repositórios
    'RepositorioProdutoMemoria', 'RepositorioClienteMemoria', 'RepositorioPedidoMemoria',
    
    # Gateways
    'GatewayPagamentoSimulado', 'GatewayNotificacaoSimulado', 'ServicoFreteSimulado',
    
    # Factory
    'FabricaInfraestrutura'
]
