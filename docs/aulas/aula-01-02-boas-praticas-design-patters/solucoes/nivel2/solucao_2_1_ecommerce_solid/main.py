#!/usr/bin/env python3
"""
Sistema de E-commerce SOLID - Demonstração Completa

OBJETIVO PEDAGÓGICO: Demonstrar implementação prática de todos os
princípios SOLID em um sistema real de e-commerce.

ARQUITETURA:
- Domain: Entidades, Value Objects e regras de negócio
- Services: Casos de uso e coordenação de operações
- Infrastructure: Adaptadores e implementações concretas

PRINCÍPIOS SOLID DEMONSTRADOS:
✅ SRP: Cada classe tem responsabilidade única e bem definida
✅ OCP: Sistema extensível sem modificar código existente
✅ LSP: Subtipos respeitam contratos dos tipos base
✅ ISP: Interfaces segregadas por responsabilidade
✅ DIP: Dependências invertidas através de abstrações

PADRÕES DE DESIGN:
- Strategy: Descontos, frete, pagamento
- Factory: Criação de produtos e infraestrutura
- Observer: Eventos de domínio e notificações
- Adapter: Adaptação de APIs externas
- Repository: Persistência abstrata

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
VERSÃO: 1.0
"""

import logging
from decimal import Decimal
from typing import List
from uuid import UUID

# Configuração de logging para acompanhar execução
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Importações do sistema
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from domain.value_objects import (
    Dinheiro, Endereco, DimensoesProduto, InformacaoDigital, InformacaoServico,
    TipoProduto, StatusPedido, TipoNotificacao, FabricaValueObjects
)

from domain.entities import (
    ProdutoFisico, ProdutoDigital, ProdutoServico, Cliente, Pedido
)

from services import (
    ServicoGestãoProdutos, ServicoGestãoClientes, ServicoProcessamentoPedidos,
    ServicoNotificacoes
)

from infrastructure import FabricaInfraestrutura


def exibir_separador(titulo: str) -> None:
    """Exibe separador visual para organizar saída"""
    print("\n" + "="*80)
    print(f"  {titulo.upper()}")
    print("="*80)


def demonstrar_criacao_produtos() -> List:
    """
    Demonstra criação de diferentes tipos de produtos
    
    PRINCÍPIOS DEMONSTRADOS:
    - Factory Pattern: FabricaProdutos cria produtos baseados no tipo
    - SRP: Cada tipo de produto tem responsabilidades específicas
    - OCP: Novos tipos podem ser adicionados sem modificar existentes
    """
    exibir_separador("Demonstração 1: Criação de Produtos (Factory + SRP)")
    
    # Infraestrutura
    infra = FabricaInfraestrutura.criar_infraestrutura_completa()
    servico_produtos = ServicoGestãoProdutos(infra['produtos'])
    
    produtos_criados = []
    
    # 1. PRODUTO FÍSICO - Notebook
    print("\n📦 Criando Produto Físico: Notebook")
    produto_fisico_data = {
        'nome': 'Notebook Gamer ASUS ROG',
        'descricao': 'Notebook gamer com placa de vídeo dedicada RTX 4060, processador Intel i7, 16GB RAM, SSD 512GB',
        'preco': Dinheiro(Decimal('4500.00')),
        'categoria': 'Informática',
        'fabricante': 'ASUS',
        'dimensoes': {
            'altura': 2.5,
            'largura': 35.0,
            'profundidade': 25.0,
            'peso': 2.3
        },
        'estoque': 15
    }
    
    notebook = servico_produtos.criar_produto(TipoProduto.FISICO, produto_fisico_data)
    produtos_criados.append(notebook)
    
    print(f"✅ Produto criado: {notebook}")
    print(f"   Dimensões: {notebook.dimensoes}")
    print(f"   Estoque: {notebook.quantidade_estoque} unidades")
    
    # 2. PRODUTO DIGITAL - E-book
    print("\n💾 Criando Produto Digital: E-book")
    produto_digital_data = {
        'nome': 'E-book: Programação Python Avançada',
        'descricao': 'Guia completo de programação Python com foco em orientação a objetos, padrões de design e boas práticas',
        'preco': Dinheiro(Decimal('89.90')),
        'categoria': 'Educação',
        'fabricante': 'TechBooks Editora',
        'info_digital': {
            'tamanho_mb': 15.5,
            'formato': 'pdf',
            'url_download': 'https://downloads.techbooks.com/python-avancado.pdf',
            'chave_licenca': 'PYTH-ADV-2024'
        },
        'licencas': 1000
    }
    
    ebook = servico_produtos.criar_produto(TipoProduto.DIGITAL, produto_digital_data)
    produtos_criados.append(ebook)
    
    print(f"✅ Produto criado: {ebook}")
    print(f"   Arquivo: {ebook.info_digital}")
    print(f"   Licenças disponíveis: {ebook.licencas_disponiveis}")
    
    # 3. PRODUTO DE SERVIÇO - Consultoria
    print("\n🛠️ Criando Produto de Serviço: Consultoria")
    produto_servico_data = {
        'nome': 'Consultoria em Arquitetura de Software',
        'descricao': 'Consultoria especializada em design de sistemas, refatoração de código e implementação de padrões de arquitetura',
        'preco': Dinheiro(Decimal('350.00')),
        'categoria': 'consultoria',
        'fabricante': 'TechConsult Pro',
        'info_servico': {
            'duracao_horas': 8,
            'categoria': 'consultoria',
            'requer_presenca': False
        },
        'profissionais': 3
    }
    
    consultoria = servico_produtos.criar_produto(TipoProduto.SERVICO, produto_servico_data)
    produtos_criados.append(consultoria)
    
    print(f"✅ Produto criado: {consultoria}")
    print(f"   Serviço: {consultoria.info_servico}")
    print(f"   Preço por hora: {consultoria.obter_preco_por_hora()}")
    
    # Demonstrar polimorfismo (LSP)
    print("\n🔄 Demonstrando Polimorfismo (LSP):")
    for produto in produtos_criados:
        print(f"   {produto.nome}: {produto.obter_tipo_produto().value} - "
              f"Disponível: {'Sim' if produto.esta_disponivel() else 'Não'}")
    
    return produtos_criados


def demonstrar_gestao_clientes() -> Cliente:
    """
    Demonstra gestão de clientes com diferentes tipos de endereço
    
    PRINCÍPIOS DEMONSTRADOS:
    - SRP: Cliente responsável apenas por dados pessoais
    - Value Objects: Endereco como objeto imutável
    """
    exibir_separador("Demonstração 2: Gestão de Clientes (SRP + Value Objects)")
    
    # Infraestrutura
    infra = FabricaInfraestrutura.criar_infraestrutura_completa()
    servico_clientes = ServicoGestãoClientes(infra['clientes'])
    
    print("\n👤 Criando Cliente:")
    
    # Criar endereço usando Factory
    endereco_principal = FabricaValueObjects.criar_endereco_simples(
        cep="01310-100",
        numero="1000",
        complemento="Apto 501"
    )
    
    cliente = servico_clientes.criar_cliente(
        nome="Ana Carolina Silva",
        email="ana.silva@email.com",
        telefone="11987654321",
        endereco=endereco_principal
    )
    
    print(f"✅ Cliente criado: {cliente}")
    print(f"   Endereço principal:")
    print(f"   {cliente.endereco_principal}")
    
    # Adicionar endereço adicional
    print("\n📍 Adicionando endereço adicional:")
    endereco_trabalho = FabricaValueObjects.criar_endereco_simples(
        cep="20040-020",
        numero="200",
        complemento="Sala 1501"
    )
    
    cliente.adicionar_endereco(endereco_trabalho)
    
    print(f"   Endereço de trabalho adicionado")
    print(f"   Total de endereços: {len(cliente.obter_todos_enderecos())}")
    
    # Configurar preferências de notificação
    print("\n🔔 Configurando notificações:")
    preferencias = {TipoNotificacao.EMAIL, TipoNotificacao.SMS}
    cliente.configurar_notificacoes(preferencias)
    
    print(f"   Notificações configuradas: {[p.value for p in cliente.obter_preferencias_notificacao()]}")
    
    return cliente


def demonstrar_processamento_pedido(produtos: List, cliente: Cliente) -> Pedido:
    """
    Demonstra processamento completo de pedido
    
    PRINCÍPIOS DEMONSTRADOS:
    - DIP: Serviços dependem de abstrações
    - Strategy: Diferentes estratégias de desconto
    - Observer: Eventos de domínio para notificações
    """
    exibir_separador("Demonstração 3: Processamento de Pedido (DIP + Strategy + Observer)")
    
    # Infraestrutura
    infra = FabricaInfraestrutura.criar_infraestrutura_completa()
    
    servico_pedidos = ServicoProcessamentoPedidos(
        repositorio_pedido=infra['pedidos'],
        repositorio_produto=infra['produtos'],
        repositorio_cliente=infra['clientes'],
        gateway_pagamento=infra['pagamento'],
        servico_frete=infra['frete']
    )
    
    servico_notificacoes = ServicoNotificacoes(
        gateway_notificacao=infra['notificacao'],
        repositorio_cliente=infra['clientes']
    )
    
    # Salvar produtos e cliente nos repositórios
    for produto in produtos:
        infra['produtos'].salvar(produto)
    infra['clientes'].salvar(cliente)
    
    print("\n🛒 Criando pedido:")
    
    # Criar pedido
    endereco_entrega = cliente.endereco_principal
    pedido = servico_pedidos.criar_pedido(cliente.id, endereco_entrega)
    
    print(f"✅ Pedido criado: {pedido.id}")
    
    # Adicionar itens
    print("\n📦 Adicionando itens ao pedido:")
    
    # Notebook (produto físico)
    notebook = produtos[0]
    servico_pedidos.adicionar_item_pedido(pedido.id, notebook.id, 1)
    print(f"   + {notebook.nome} (Qtd: 1)")
    
    # E-book (produto digital)
    ebook = produtos[1]
    servico_pedidos.adicionar_item_pedido(pedido.id, ebook.id, 1)
    print(f"   + {ebook.nome} (Qtd: 1)")
    
    # Atualizar pedido
    pedido = infra['pedidos'].buscar_por_id(pedido.id)
    
    print(f"\n💰 Valores do pedido:")
    print(f"   Subtotal: {pedido.calcular_subtotal()}")
    
    # Calcular frete (Strategy Pattern)
    print(f"\n🚚 Calculando frete:")
    resultado_frete = servico_pedidos.calcular_frete(pedido.id)
    if resultado_frete:
        print(f"   {resultado_frete}")
    
    # Aplicar desconto (Strategy Pattern)
    print(f"\n🎁 Aplicando descontos:")
    desconto = servico_pedidos.aplicar_melhor_desconto(pedido.id)
    if not desconto.eh_zero():
        print(f"   Desconto aplicado: {desconto}")
    else:
        print(f"   Nenhum desconto aplicável")
    
    # Valores finais
    pedido = infra['pedidos'].buscar_por_id(pedido.id)
    print(f"\n💳 Valores finais:")
    print(f"   Subtotal: {pedido.calcular_subtotal()}")
    print(f"   Frete: {pedido.valor_frete}")
    print(f"   Total: {pedido.calcular_total()}")
    
    # Confirmar pedido
    print(f"\n✅ Confirmando pedido:")
    pedido.confirmar("Pedido confirmado pelo cliente")
    infra['pedidos'].salvar(pedido)
    
    # Processar eventos (Observer Pattern)
    eventos = pedido.limpar_eventos()
    for evento in eventos:
        servico_notificacoes.processar_evento(evento)
    
    print(f"   Status: {pedido.status.value}")
    print(f"   Eventos processados: {len(eventos)}")
    
    return pedido


def demonstrar_pagamento_e_entrega(pedido: Pedido, infra: dict) -> None:
    """
    Demonstra processamento de pagamento e entrega
    
    PRINCÍPIOS DEMONSTRADOS:
    - Adapter: Gateway de pagamento adaptado
    - State Pattern: Transições de estado do pedido
    """
    exibir_separador("Demonstração 4: Pagamento e Entrega (Adapter + State)")
    
    servico_pedidos = ServicoProcessamentoPedidos(
        repositorio_pedido=infra['pedidos'],
        repositorio_produto=infra['produtos'],
        repositorio_cliente=infra['clientes'],
        gateway_pagamento=infra['pagamento'],
        servico_frete=infra['frete']
    )
    
    # Processar pagamento
    print("\n💳 Processando pagamento:")
    
    from domain.value_objects import DadosPagamento
    dados_pagamento = DadosPagamento(
        numero_cartao="1234 5678 9012 3456",
        nome_titular="ANA CAROLINA SILVA",
        cvv="123",
        mes_vencimento=12,
        ano_vencimento=2027
    )
    
    print(f"   Cartão: {dados_pagamento.obter_numero_mascarado()}")
    
    sucesso_pagamento = servico_pedidos.processar_pagamento(pedido.id, dados_pagamento)
    
    if sucesso_pagamento:
        print("   ✅ Pagamento aprovado!")
        
        # Atualizar pedido
        pedido_atualizado = infra['pedidos'].buscar_por_id(pedido.id)
        print(f"   Status atualizado: {pedido_atualizado.status.value}")
        
        # Simular envio
        print("\n📦 Processando envio:")
        pedido_atualizado.enviar("BR123456789")
        infra['pedidos'].salvar(pedido_atualizado)
        print(f"   Código de rastreamento: {pedido_atualizado.numero_rastreamento}")
        print(f"   Status: {pedido_atualizado.status.value}")
        
        # Simular entrega
        print("\n🏠 Simulando entrega:")
        pedido_atualizado.entregar()
        infra['pedidos'].salvar(pedido_atualizado)
        print(f"   Status final: {pedido_atualizado.status.value}")
        
        # Atualizar histórico do cliente
        cliente = infra['clientes'].buscar_por_id(pedido_atualizado.cliente_id)
        print(f"\n📊 Histórico do cliente atualizado:")
        print(f"   Total de pedidos: {cliente.numero_pedidos}")
        print(f"   Valor total de compras: {cliente.valor_total_compras}")
        print(f"   Cliente VIP: {'Sim' if cliente.eh_cliente_vip() else 'Não'}")
        
    else:
        print("   ❌ Falha no pagamento!")


def demonstrar_relatorios(infra: dict) -> None:
    """
    Demonstra geração de relatórios e estatísticas
    
    PRINCÍPIOS DEMONSTRADOS:
    - SRP: Cada serviço gera relatórios específicos
    - ISP: Interfaces segregadas para diferentes tipos de consulta
    """
    exibir_separador("Demonstração 5: Relatórios e Estatísticas")
    
    # Estatísticas de produtos
    print("\n📊 Estatísticas de Produtos:")
    produtos = infra['produtos'].obter_todos()
    produtos_por_tipo = {}
    
    for produto in produtos:
        tipo = produto.obter_tipo_produto().value
        if tipo not in produtos_por_tipo:
            produtos_por_tipo[tipo] = 0
        produtos_por_tipo[tipo] += 1
    
    for tipo, quantidade in produtos_por_tipo.items():
        print(f"   {tipo.title()}: {quantidade} produtos")
    
    # Estatísticas de clientes
    print("\n👥 Estatísticas de Clientes:")
    servico_clientes = ServicoGestãoClientes(infra['clientes'])
    segmentacao = servico_clientes.calcular_segmentacao()
    
    for segmento, clientes in segmentacao.items():
        print(f"   {segmento.title()}: {len(clientes)} clientes")
    
    # Estatísticas de pedidos
    print("\n🛒 Estatísticas de Pedidos:")
    pedidos = infra['pedidos'].obter_todos()
    pedidos_por_status = {}
    
    for pedido in pedidos:
        status = pedido.status.value
        if status not in pedidos_por_status:
            pedidos_por_status[status] = 0
        pedidos_por_status[status] += 1
    
    for status, quantidade in pedidos_por_status.items():
        print(f"   {status.title()}: {quantidade} pedidos")
    
    # Estatísticas de notificações
    print("\n📧 Estatísticas de Notificações:")
    stats_notificacao = infra['notificacao'].obter_estatisticas()
    print(f"   Total enviadas: {stats_notificacao['total']}")
    print(f"   Sucessos: {stats_notificacao['sucesso']}")
    print(f"   Falhas: {stats_notificacao['falha']}")
    print(f"   Taxa de sucesso: {stats_notificacao['taxa_sucesso']}%")
    
    # Estatísticas de pagamentos
    print("\n💳 Estatísticas de Pagamentos:")
    historico_pagamentos = infra['pagamento'].obter_historico_transacoes()
    pagamentos_sucesso = sum(1 for t in historico_pagamentos if t.get('sucesso'))
    pagamentos_total = len(historico_pagamentos)
    
    if pagamentos_total > 0:
        taxa_aprovacao = (pagamentos_sucesso / pagamentos_total) * 100
        print(f"   Total de transações: {pagamentos_total}")
        print(f"   Aprovadas: {pagamentos_sucesso}")
        print(f"   Taxa de aprovação: {taxa_aprovacao:.1f}%")
    else:
        print("   Nenhuma transação processada")


def demonstrar_extensibilidade() -> None:
    """
    Demonstra como o sistema pode ser estendido
    
    PRINCÍPIOS DEMONSTRADOS:
    - OCP: Sistema aberto para extensão, fechado para modificação
    - Strategy: Novas estratégias podem ser adicionadas
    - Factory: Novos tipos podem ser criados
    """
    exibir_separador("Demonstração 6: Extensibilidade (OCP)")
    
    print("\n🔧 Demonstrando Extensibilidade do Sistema:")
    print("\n1. ✅ Novos tipos de produto podem ser criados:")
    print("   - Herdar de Produto")
    print("   - Implementar métodos abstratos")
    print("   - Adicionar à Factory")
    
    print("\n2. ✅ Novas estratégias de desconto podem ser adicionadas:")
    print("   - Implementar EstrategiaDesconto")
    print("   - Adicionar ao ServicoProcessamentoPedidos")
    print("   - Sem modificar código existente")
    
    print("\n3. ✅ Novos gateways podem ser implementados:")
    print("   - Implementar interfaces de Gateway")
    print("   - Substituir na FabricaInfraestrutura")
    print("   - Sistema funciona transparentemente")
    
    print("\n4. ✅ Novos repositórios podem ser criados:")
    print("   - Implementar interfaces de Repositorio")
    print("   - Banco de dados real, arquivos, APIs")
    print("   - Lógica de negócio permanece inalterada")
    
    print("\n🎯 SOLID PRINCIPLES APLICADOS COM SUCESSO!")
    print("   ✅ SRP: Cada classe tem responsabilidade única")
    print("   ✅ OCP: Sistema extensível sem modificações")
    print("   ✅ LSP: Subtipos substituem tipos base corretamente")
    print("   ✅ ISP: Interfaces pequenas e focadas")
    print("   ✅ DIP: Dependências invertidas via abstrações")


def main() -> None:
    """
    Função principal - executa demonstração completa
    """
    print("🚀 SISTEMA DE E-COMMERCE SOLID - DEMONSTRAÇÃO COMPLETA")
    print("=" * 80)
    print("Implementação educacional demonstrando todos os princípios SOLID")
    print("em um sistema real de e-commerce com múltiplos padrões de design.")
    print("=" * 80)
    
    try:
        # Criar infraestrutura
        infra = FabricaInfraestrutura.criar_infraestrutura_completa(taxa_sucesso_pagamento=0.95)
        
        # Executar demonstrações
        produtos = demonstrar_criacao_produtos()
        cliente = demonstrar_gestao_clientes()
        pedido = demonstrar_processamento_pedido(produtos, cliente)
        demonstrar_pagamento_e_entrega(pedido, infra)
        demonstrar_relatorios(infra)
        demonstrar_extensibilidade()
        
        # Conclusão
        exibir_separador("Demonstração Concluída com Sucesso!")
        print("\n🎓 OBJETIVOS PEDAGÓGICOS ALCANÇADOS:")
        print("   ✅ Demonstração prática de todos os princípios SOLID")
        print("   ✅ Implementação de múltiplos padrões de design")
        print("   ✅ Arquitetura em camadas com responsabilidades claras")
        print("   ✅ Sistema extensível e testável")
        print("   ✅ Separação de conceitos de domínio e infraestrutura")
        
        print("\n📚 CONCEITOS DEMONSTRADOS:")
        print("   • Domain-Driven Design (DDD)")
        print("   • Hexagonal Architecture")
        print("   • Inversion of Control (IoC)")
        print("   • Event-Driven Architecture")
        print("   • Value Objects e Entities")
        print("   • Repository Pattern")
        print("   • Strategy Pattern")
        print("   • Factory Pattern")
        print("   • Observer Pattern")
        print("   • Adapter Pattern")
        
        print("\n🔮 PRÓXIMOS PASSOS:")
        print("   • Implementar persistência real (PostgreSQL, MongoDB)")
        print("   • Adicionar API REST com FastAPI")
        print("   • Implementar testes unitários e de integração")
        print("   • Adicionar monitoramento e observabilidade")
        print("   • Implementar cache distribuído")
        print("   • Adicionar mensageria assíncrona")
        
    except Exception as e:
        logging.error(f"Erro durante a demonstração: {e}")
        raise


if __name__ == "__main__":
    main()
