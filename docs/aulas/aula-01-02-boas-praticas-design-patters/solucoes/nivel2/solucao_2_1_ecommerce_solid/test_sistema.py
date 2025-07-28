#!/usr/bin/env python3
"""
Testes Abrangentes - Sistema E-commerce SOLID

OBJETIVO: Demonstrar como a arquitetura SOLID facilita a criação de testes
unitários, de integração e de comportamento.

BENEFÍCIOS DA ARQUITETURA:
- Injeção de dependências facilita mocking
- Interfaces permitem substituição em testes
- Separação de responsabilidades isola comportamentos
- Value Objects são facilmente testáveis

TIPOS DE TESTE:
- Unitários: Testam classes isoladamente
- Integração: Testam interação entre componentes
- Comportamento: Testam cenários de uso completos

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

import unittest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from uuid import UUID, uuid4
import sys
import os

# Adicionar diretório atual ao path
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(current_dir)

from domain.value_objects import (
    Dinheiro, Endereco, DimensoesProduto, InformacaoDigital,
    InformacaoServico, TipoProduto, StatusPedido, FabricaValueObjects
)

from domain.entities import (
    ProdutoFisico, ProdutoDigital, ProdutoServico, Cliente, Pedido
)

from services import (
    ServicoGestãoProdutos, ServicoGestãoClientes, ServicoProcessamentoPedidos,
    DescontoClienteVIP, DescontoPrimeiraCompra
)

from infrastructure import (
    RepositorioProdutoMemoria, RepositorioClienteMemoria, RepositorioPedidoMemoria,
    GatewayPagamentoSimulado, FabricaInfraestrutura
)


class TestValueObjects(unittest.TestCase):
    """
    Testes para Value Objects
    
    FOCO: Imutabilidade, validações e comportamentos
    """
    
    def test_dinheiro_criacao_e_operacoes(self):
        """Testa criação e operações com dinheiro"""
        # Criação
        valor1 = Dinheiro(Decimal('100.50'))
        valor2 = Dinheiro(Decimal('50.25'))
        
        # Teste de imutabilidade
        self.assertEqual(valor1.valor, Decimal('100.50'))
        self.assertEqual(valor1.moeda, 'BRL')
        
        # Operações
        soma = valor1.somar(valor2)
        self.assertEqual(soma.valor, Decimal('150.75'))
        
        subtracao = valor1.subtrair(valor2)
        self.assertEqual(subtracao.valor, Decimal('50.25'))
        
        multiplicacao = valor1.multiplicar(Decimal('2'))
        self.assertEqual(multiplicacao.valor, Decimal('201.00'))
        
        # Comparações
        self.assertTrue(valor1.eh_maior_que(valor2))
        self.assertFalse(valor1.eh_menor_que(valor2))
    
    def test_dinheiro_validacoes(self):
        """Testa validações do value object Dinheiro"""
        # Valor negativo deve falhar
        with self.assertRaises(ValueError):
            Dinheiro(Decimal('-10.00'))
        
        # Moeda inválida deve falhar
        with self.assertRaises(ValueError):
            Dinheiro(Decimal('10.00'), 'INVALID')
        
        # Moedas incompatíveis em operações
        real = Dinheiro(Decimal('100.00'), 'BRL')
        dolar = Dinheiro(Decimal('50.00'), 'USD')
        
        with self.assertRaises(ValueError):
            real.somar(dolar)
    
    def test_endereco_validacoes(self):
        """Testa validações de endereço"""
        # CEP válido
        endereco = Endereco(
            cep="01310100",  # Será formatado automaticamente
            logradouro="Av. Paulista",
            numero="1000",
            complemento=None,
            bairro="Bela Vista",
            cidade="São Paulo",
            uf="sp"  # Será convertido para maiúsculo
        )
        
        self.assertEqual(endereco.cep, "01310-100")
        self.assertEqual(endereco.uf, "SP")
        
        # CEP inválido
        with self.assertRaises(ValueError):
            Endereco("123", "Rua A", "1", None, "Bairro", "Cidade", "SP")
        
        # UF inválida
        with self.assertRaises(ValueError):
            Endereco("12345678", "Rua A", "1", None, "Bairro", "Cidade", "XX")
    
    def test_fabrica_value_objects(self):
        """Testa Factory de Value Objects"""
        # Criar dinheiro a partir de string
        dinheiro = FabricaValueObjects.criar_dinheiro("R$ 1.500,75")
        self.assertEqual(dinheiro.valor, Decimal('1500.75'))
        
        # Criar endereço simples
        endereco = FabricaValueObjects.criar_endereco_simples("01310100", "1000")
        self.assertEqual(endereco.cep, "01310-100")
        self.assertEqual(endereco.numero, "1000")


class TestEntidades(unittest.TestCase):
    """
    Testes para entidades de domínio
    
    FOCO: Comportamentos de negócio e invariantes
    """
    
    def setUp(self):
        """Configuração comum para testes"""
        self.dimensoes = DimensoesProduto(
            altura=Decimal('10'),
            largura=Decimal('20'),
            profundidade=Decimal('5'),
            peso=Decimal('2')
        )
        
        self.endereco = Endereco(
            cep="01310-100",
            logradouro="Av. Paulista",
            numero="1000",
            complemento=None,
            bairro="Bela Vista",
            cidade="São Paulo",
            uf="SP"
        )
    
    def test_produto_fisico_criacao(self):
        """Testa criação de produto físico"""
        produto = ProdutoFisico(
            nome="Teste Produto",
            descricao="Descrição do produto de teste",
            preco=Dinheiro(Decimal('99.90')),
            categoria="Teste",
            fabricante="Teste Ltda",
            dimensoes=self.dimensoes,
            quantidade_estoque=10
        )
        
        self.assertEqual(produto.nome, "Teste Produto")
        self.assertEqual(produto.quantidade_estoque, 10)
        self.assertEqual(produto.obter_tipo_produto(), TipoProduto.FISICO)
        self.assertTrue(produto.esta_disponivel())
    
    def test_produto_fisico_estoque(self):
        """Testa gestão de estoque"""
        produto = ProdutoFisico(
            nome="Teste",
            descricao="Teste produto",
            preco=Dinheiro(Decimal('50.00')),
            categoria="Teste",
            fabricante="Teste",
            dimensoes=self.dimensoes,
            quantidade_estoque=5
        )
        
        # Adicionar estoque
        produto.adicionar_estoque(10)
        self.assertEqual(produto.quantidade_estoque, 15)
        
        # Remover estoque com sucesso
        sucesso = produto.remover_estoque(5)
        self.assertTrue(sucesso)
        self.assertEqual(produto.quantidade_estoque, 10)
        
        # Tentar remover mais que disponível
        sucesso = produto.remover_estoque(15)
        self.assertFalse(sucesso)
        self.assertEqual(produto.quantidade_estoque, 10)
    
    def test_cliente_criacao_e_validacoes(self):
        """Testa criação e validações de cliente"""
        cliente = Cliente(
            nome="João Silva",
            email="joao@email.com",
            telefone="11987654321",
            endereco_principal=self.endereco
        )
        
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.email, "joao@email.com")
        self.assertTrue(cliente.ativo)
        
        # Teste de email inválido
        with self.assertRaises(ValueError):
            Cliente("Nome", "email_invalido", "11999999999", self.endereco)
    
    def test_cliente_historico_compras(self):
        """Testa histórico de compras do cliente"""
        cliente = Cliente("Ana", "ana@email.com", "11999999999", self.endereco)
        
        # Cliente novo não é VIP
        self.assertFalse(cliente.eh_cliente_vip())
        self.assertEqual(cliente.numero_pedidos, 0)
        
        # Registrar compras
        cliente.registrar_compra(Dinheiro(Decimal('200.00')))
        cliente.registrar_compra(Dinheiro(Decimal('300.00')))
        cliente.registrar_compra(Dinheiro(Decimal('500.00')))
        
        self.assertEqual(cliente.numero_pedidos, 3)
        self.assertEqual(cliente.valor_total_compras.valor, Decimal('1000.00'))
        
        # Com múltiplas compras e valor alto, deve ser VIP
        cliente.registrar_compra(Dinheiro(Decimal('100.00')))
        cliente.registrar_compra(Dinheiro(Decimal('100.00')))
        self.assertTrue(cliente.eh_cliente_vip())  # 5+ pedidos e R$ 1000+
    
    def test_pedido_criacao_e_itens(self):
        """Testa criação de pedido e gestão de itens"""
        cliente_id = uuid4()
        pedido = Pedido(cliente_id, self.endereco)
        
        self.assertEqual(pedido.cliente_id, cliente_id)
        self.assertEqual(pedido.status, StatusPedido.CRIADO)
        self.assertEqual(len(pedido.itens), 0)
        
        # Criar produto para adicionar ao pedido
        produto = ProdutoFisico(
            nome="Produto Teste",
            descricao="Produto para teste de funcionalidade",
            preco=Dinheiro(Decimal('100.00')),
            categoria="Teste",
            fabricante="Teste",
            dimensoes=self.dimensoes,
            quantidade_estoque=10
        )
        produto._disponivel = True  # Forçar disponibilidade
        
        # Adicionar item
        pedido.adicionar_item(produto, 2)
        self.assertEqual(len(pedido.itens), 1)
        self.assertEqual(pedido.itens[0].quantidade, 2)
        
        # Calcular subtotal
        subtotal = pedido.calcular_subtotal()
        self.assertEqual(subtotal.valor, Decimal('200.00'))
    
    def test_pedido_fluxo_status(self):
        """Testa fluxo de status do pedido"""
        from domain.value_objects import DadosPagamento
        
        pedido = Pedido(uuid4(), self.endereco)
        
        # Adicionar item primeiro
        produto = ProdutoFisico(
            nome="Produto Teste Status",
            descricao="Produto para teste de fluxo de status",
            preco=Dinheiro("25.00"),
            categoria="Teste",
            fabricante="Fabricante Teste",
            dimensoes=self.dimensoes,
            quantidade_estoque=10
        )
        produto._disponivel = True
        pedido.adicionar_item(produto, 1)
        
        # Confirmar pedido
        pedido.confirmar()
        self.assertEqual(pedido.status, StatusPedido.CONFIRMADO)
        
        # Processar pagamento
        dados_pagamento = DadosPagamento(
            numero_cartao="1234567890123456",
            nome_titular="TESTE",
            cvv="123",
            mes_vencimento=12,
            ano_vencimento=2025
        )
        
        valor_pedido = pedido.calcular_subtotal()
        pedido.processar_pagamento(dados_pagamento, valor_pedido)
        self.assertEqual(pedido.status, StatusPedido.PAGO)
        
        # Enviar
        pedido.enviar("BR123456789")
        self.assertEqual(pedido.status, StatusPedido.ENVIADO)
        self.assertEqual(pedido.numero_rastreamento, "BR123456789")
        
        # Entregar
        pedido.entregar()
        self.assertEqual(pedido.status, StatusPedido.ENTREGUE)


class TestRepositorios(unittest.TestCase):
    """
    Testes para repositórios
    
    FOCO: Persistência e consultas
    """
    
    def setUp(self):
        self.repo_produto = RepositorioProdutoMemoria()
        self.repo_cliente = RepositorioClienteMemoria()
        self.repo_pedido = RepositorioPedidoMemoria()
    
    def test_repositorio_produto(self):
        """Testa repositório de produtos"""
        # Criar produto
        dimensoes = DimensoesProduto(
            altura=Decimal('10'),
            largura=Decimal('20'),
            profundidade=Decimal('5'),
            peso=Decimal('2')
        )
        
        produto = ProdutoFisico(
            nome="Produto Teste",
            descricao="Descrição do produto",
            preco=Dinheiro(Decimal('99.90')),
            categoria="Eletrônicos",
            fabricante="Teste Ltda",
            dimensoes=dimensoes
        )
        produto._disponivel = True  # Marcar como disponível
        
        # Salvar
        self.repo_produto.salvar(produto)
        
        # Buscar por ID
        produto_encontrado = self.repo_produto.buscar_por_id(produto.id)
        self.assertIsNotNone(produto_encontrado)
        self.assertEqual(produto_encontrado.nome, "Produto Teste")
        
        # Buscar por categoria
        produtos_categoria = self.repo_produto.buscar_por_categoria("Eletrônicos")
        self.assertEqual(len(produtos_categoria), 1)
        
        # Buscar disponíveis
        produtos_disponiveis = self.repo_produto.buscar_disponiveis()
        self.assertEqual(len(produtos_disponiveis), 1)
    
    def test_repositorio_cliente(self):
        """Testa repositório de clientes"""
        endereco = Endereco(
            cep="01310-100", logradouro="Av. Paulista", numero="1000",
            complemento=None, bairro="Bela Vista", cidade="São Paulo", uf="SP"
        )
        
        cliente = Cliente(
            nome="João Silva",
            email="joao@email.com",
            telefone="11999999999",
            endereco_principal=endereco
        )
        
        # Salvar
        self.repo_cliente.salvar(cliente)
        
        # Buscar por ID
        cliente_encontrado = self.repo_cliente.buscar_por_id(cliente.id)
        self.assertIsNotNone(cliente_encontrado)
        
        # Buscar por email
        cliente_email = self.repo_cliente.buscar_por_email("joao@email.com")
        self.assertIsNotNone(cliente_email)
        self.assertEqual(cliente_email.id, cliente.id)
        
        # Buscar ativos
        clientes_ativos = self.repo_cliente.buscar_ativos()
        self.assertEqual(len(clientes_ativos), 1)


class TestServicos(unittest.TestCase):
    """
    Testes para serviços de aplicação
    
    FOCO: Casos de uso e coordenação
    """
    
    def setUp(self):
        self.infra = FabricaInfraestrutura.criar_infraestrutura_completa()
        self.servico_produtos = ServicoGestãoProdutos(self.infra['produtos'])
        self.servico_clientes = ServicoGestãoClientes(self.infra['clientes'])
    
    def test_servico_criacao_produto(self):
        """Testa criação de produto via serviço"""
        dados_produto = {
            'nome': 'Notebook Teste',
            'descricao': 'Notebook para testes',
            'preco': Dinheiro(Decimal('2000.00')),
            'categoria': 'Informática',
            'fabricante': 'Teste Corp',
            'dimensoes': {
                'altura': 3.0,
                'largura': 35.0,
                'profundidade': 25.0,
                'peso': 2.5
            },
            'estoque': 10
        }
        
        produto = self.servico_produtos.criar_produto(TipoProduto.FISICO, dados_produto)
        
        self.assertIsNotNone(produto)
        self.assertEqual(produto.nome, 'Notebook Teste')
        self.assertEqual(produto.quantidade_estoque, 10)
        
        # Verificar se foi salvo no repositório
        produto_salvo = self.infra['produtos'].buscar_por_id(produto.id)
        self.assertIsNotNone(produto_salvo)
    
    def test_servico_gestao_cliente(self):
        """Testa gestão de clientes via serviço"""
        endereco = FabricaValueObjects.criar_endereco_simples("01310100", "1000")
        
        # Criar cliente
        cliente = self.servico_clientes.criar_cliente(
            nome="Maria Silva",
            email="maria@email.com",
            telefone="11888888888",
            endereco=endereco
        )
        
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.email, "maria@email.com")
        
        # Tentar criar cliente com mesmo email (deve falhar)
        with self.assertRaises(ValueError):
            self.servico_clientes.criar_cliente(
                nome="Outro Nome",
                email="maria@email.com",  # Email já existe
                telefone="11777777777",
                endereco=endereco
            )
    
    def test_estrategias_desconto(self):
        """Testa estratégias de desconto"""
        # Criar cliente VIP
        endereco = FabricaValueObjects.criar_endereco_simples("01310100", "1000")
        cliente_vip = Cliente("VIP Cliente", "vip@email.com", "11999999999", endereco)
        
        # Simular histórico VIP
        for _ in range(6):  # Mais de 5 pedidos
            cliente_vip.registrar_compra(Dinheiro(Decimal('200.00')))  # Total > R$ 1000
        
        # Criar pedido
        pedido = Pedido(cliente_vip.id, endereco)
        
        # Adicionar valor ao pedido
        from domain.entities import ProdutoFisico
        from domain.value_objects import DimensoesProduto
        dimensoes_especiais = DimensoesProduto(
            altura=Decimal('10'), largura=Decimal('20'),
            profundidade=Decimal('5'), peso=Decimal('2')
        )
        produto = ProdutoFisico(
            nome="Produto Desconto",
            descricao="Produto especial para teste de estratégias de desconto com descrição detalhada",
            preco=Dinheiro("1000.00"),
            categoria="Teste",
            fabricante="Fabricante Teste",
            dimensoes=dimensoes_especiais,
            quantidade_estoque=10
        )
        produto._disponivel = True
        pedido.adicionar_item(produto, 1)
        
        # Testar desconto VIP
        estrategia_vip = DescontoClienteVIP()
        self.assertTrue(estrategia_vip.eh_aplicavel(pedido, cliente_vip))
        
        desconto = estrategia_vip.calcular_desconto(pedido, cliente_vip)
        self.assertEqual(desconto.valor, Decimal('100.00'))  # 10% de R$ 1000
        
        # Testar desconto primeira compra (cliente novo)
        cliente_novo = Cliente("Novo Cliente", "novo@email.com", "11888888888", endereco)
        estrategia_primeira = DescontoPrimeiraCompra()
        
        self.assertTrue(estrategia_primeira.eh_aplicavel(pedido, cliente_novo))
        desconto_primeira = estrategia_primeira.calcular_desconto(pedido, cliente_novo)
        self.assertEqual(desconto_primeira.valor, Decimal('20.00'))  # Valor fixo


class TestIntegracao(unittest.TestCase):
    """
    Testes de integração
    
    FOCO: Interação entre componentes
    """
    
    def test_fluxo_completo_pedido(self):
        """Testa fluxo completo de processamento de pedido"""
        # Configurar infraestrutura
        infra = FabricaInfraestrutura.criar_infraestrutura_completa(
            taxa_sucesso_pagamento=1.0  # Garantir sucesso
        )
        
        # Criar serviços
        servico_produtos = ServicoGestãoProdutos(infra['produtos'])
        servico_clientes = ServicoGestãoClientes(infra['clientes'])
        servico_pedidos = ServicoProcessamentoPedidos(
            repositorio_pedido=infra['pedidos'],
            repositorio_produto=infra['produtos'],
            repositorio_cliente=infra['clientes'],
            gateway_pagamento=infra['pagamento'],
            servico_frete=infra['frete']
        )
        
        # 1. Criar produto
        dados_produto = {
            'nome': 'Produto Integração',
            'descricao': 'Produto para teste de integração',
            'preco': Dinheiro(Decimal('150.00')),
            'categoria': 'Teste',
            'fabricante': 'Teste Corp',
            'dimensoes': {
                'altura': 10.0, 'largura': 20.0,
                'profundidade': 5.0, 'peso': 1.0
            },
            'estoque': 5
        }
        produto = servico_produtos.criar_produto(TipoProduto.FISICO, dados_produto)
        
        # 2. Criar cliente
        endereco = FabricaValueObjects.criar_endereco_simples("01310100", "1000")
        cliente = servico_clientes.criar_cliente(
            nome="Cliente Integração",
            email="integracao@email.com",
            telefone="11999999999",
            endereco=endereco
        )
        
        # 3. Criar pedido
        pedido = servico_pedidos.criar_pedido(cliente.id, endereco)
        
        # 4. Adicionar item
        sucesso_item = servico_pedidos.adicionar_item_pedido(pedido.id, produto.id, 2)
        self.assertTrue(sucesso_item)
        
        # 5. Calcular frete
        resultado_frete = servico_pedidos.calcular_frete(pedido.id)
        self.assertIsNotNone(resultado_frete)
        
        # 6. Aplicar desconto
        desconto = servico_pedidos.aplicar_melhor_desconto(pedido.id)
        # Cliente novo deve receber desconto de primeira compra
        self.assertEqual(desconto.valor, Decimal('20.00'))
        
        # 7. Confirmar pedido
        pedido_atualizado = infra['pedidos'].buscar_por_id(pedido.id)
        pedido_atualizado.confirmar()
        infra['pedidos'].salvar(pedido_atualizado)
        
        # 8. Processar pagamento
        from domain.value_objects import DadosPagamento
        dados_pagamento = DadosPagamento(
            numero_cartao="1234567890123456",
            nome_titular="CLIENTE INTEGRACAO",
            cvv="123",
            mes_vencimento=12,
            ano_vencimento=2025
        )
        
        sucesso_pagamento = servico_pedidos.processar_pagamento(pedido.id, dados_pagamento)
        self.assertTrue(sucesso_pagamento)
        
        # 9. Verificar resultado final
        pedido_final = infra['pedidos'].buscar_por_id(pedido.id)
        self.assertEqual(pedido_final.status, StatusPedido.PAGO)
        
        # Verificar estoque foi reduzido
        produto_atualizado = infra['produtos'].buscar_por_id(produto.id)
        self.assertEqual(produto_atualizado.quantidade_estoque, 3)  # 5 - 2
        
        # Verificar histórico do cliente
        cliente_atualizado = infra['clientes'].buscar_por_id(cliente.id)
        self.assertEqual(cliente_atualizado.numero_pedidos, 1)


def executar_demonstracao_testes():
    """Executa demonstração educativa dos testes"""
    print("\n🧪 DEMONSTRAÇÃO DE TESTES - ARQUITETURA SOLID")
    print("=" * 60)
    print("Demonstrando como a arquitetura SOLID facilita testes:")
    print("• Isolamento de responsabilidades")
    print("• Injeção de dependências")
    print("• Interfaces permitem mocking")
    print("• Value Objects são naturalmente testáveis")
    print("=" * 60)
    
    # Executar suíte de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestValueObjects))
    suite.addTests(loader.loadTestsFromTestCase(TestEntidades))
    suite.addTests(loader.loadTestsFromTestCase(TestRepositorios))
    suite.addTests(loader.loadTestsFromTestCase(TestServicos))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracao))
    
    # Executar
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL DOS TESTES")
    print("=" * 40)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Sucessos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("A arquitetura SOLID permite testes:")
        print("• Unitários rápidos e isolados")
        print("• Integração confiáveis")
        print("• Fácil manutenção e extensão")
    else:
        print("\n❌ Alguns testes falharam")
        for failure in resultado.failures:
            print(f"FALHA: {failure[0]}")
        for error in resultado.errors:
            print(f"ERRO: {error[0]}")


if __name__ == "__main__":
    executar_demonstracao_testes()
