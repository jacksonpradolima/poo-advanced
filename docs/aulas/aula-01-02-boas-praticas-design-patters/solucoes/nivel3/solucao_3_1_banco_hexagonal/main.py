#!/usr/bin/env python3
"""
SISTEMA BANCÁRIO - ARQUITETURA HEXAGONAL
Demonstração Completa

Este arquivo demonstra um sistema bancário completo implementado com
Arquitetura Hexagonal (Ports & Adapters), Domain-Driven Design e 
todos os princípios SOLID.

EXECUTAR: python main.py

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

import sys
import os
import time
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(current_dir)

# Imports do domínio
from domain import (
    CPF, Dinheiro, Endereco, TipoConta, 
    ComandoCriarCliente, ComandoAbrirConta, ComandoRealizarTransferencia,
    CriarClienteUseCase, AbrirContaUseCase, RealizarTransferenciaUseCase,
    EventoContaCriada, EventoTransacaoRealizada
)

# Imports da infraestrutura
from infrastructure import (
    RepositorioClienteMemoria, RepositorioContaMemoria, RepositorioTransacaoMemoria,
    ConsultorCreditoSerasa, ValidadorFraudeInteligente, NotificadorEmailSMTP,
    ProcessadorEventosAssincrono, ColetorMetricasBanco, AuditoriaTransacoes
)


def demonstrar_sistema_bancario():
    """
    Demonstração completa do sistema bancário com Arquitetura Hexagonal
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
    
    # =================================================================
    # 1. CONFIGURAÇÃO DA INFRAESTRUTURA (ADAPTERS)
    # =================================================================
    
    print("\n🔧 1. CONFIGURANDO INFRAESTRUTURA (ADAPTERS)")
    print("-" * 50)
    
    # Repositórios (Adapters de Persistência)
    repo_cliente = RepositorioClienteMemoria()
    repo_conta = RepositorioContaMemoria()
    repo_transacao = RepositorioTransacaoMemoria()
    print("✅ Repositórios em memória configurados")
    
    # Serviços externos (Adapters)
    consultor_credito = ConsultorCreditoSerasa()
    validador_fraude = ValidadorFraudeInteligente()
    notificador = NotificadorEmailSMTP()
    print("✅ Serviços externos configurados")
    
    # Infraestrutura de eventos e métricas
    processador_eventos = ProcessadorEventosAssincrono()
    coletor_metricas = ColetorMetricasBanco()
    auditoria = AuditoriaTransacoes()
    print("✅ Eventos, métricas e auditoria configurados")
    
    # Configurar handlers de eventos
    def handler_conta_criada(evento):
        print(f"📊 EVENTO: Conta {evento.agencia}-{evento.numero} criada para cliente {evento.cliente_id}")
        auditoria.registrar_evento(evento, {"origem": "sistema_bancario"})
    
    def handler_transacao_realizada(evento):
        print(f"💰 EVENTO: Transação {evento.tipo.value} de {evento.valor.formatado} realizada")
        auditoria.registrar_evento(evento, {"origem": "sistema_bancario"})
        coletor_metricas.registrar_transacao(evento.tipo, evento.valor)
    
    processador_eventos.registrar_handler("EventoContaCriada", handler_conta_criada)
    processador_eventos.registrar_handler("EventoTransacaoRealizada", handler_transacao_realizada)
    
    # =================================================================
    # 2. CONFIGURAÇÃO DOS CASOS DE USO (APPLICATION LAYER)
    # =================================================================
    
    print("\n📋 2. CONFIGURANDO CASOS DE USO (APPLICATION LAYER)")
    print("-" * 50)
    
    # Criar casos de uso injetando dependências (DIP)
    criar_cliente_uc = CriarClienteUseCase(repo_cliente, consultor_credito)
    abrir_conta_uc = AbrirContaUseCase(repo_cliente, repo_conta)
    transferencia_uc = RealizarTransferenciaUseCase(
        repo_conta, repo_transacao, validador_fraude, notificador
    )
    print("✅ Casos de uso configurados com injeção de dependências")
    
    # =================================================================
    # 3. DEMONSTRAÇÃO: CRIAÇÃO DE CLIENTES
    # =================================================================
    
    print("\n👥 3. DEMONSTRANDO CRIAÇÃO DE CLIENTES")
    print("-" * 50)
    
    # Cliente 1: João Silva
    print("\n📝 Criando Cliente 1: João Silva")
    comando_joao = ComandoCriarCliente(
        nome="João Silva",
        cpf="11144477735",  # CPF válido
        endereco_cep="01310-100",
        endereco_logradouro="Av. Paulista",
        endereco_numero="1000",
        endereco_complemento="Apto 101",
        endereco_bairro="Bela Vista",
        endereco_cidade="São Paulo",
        endereco_uf="SP",
        telefone="11999887766",
        email="joao.silva@email.com",
        data_nascimento=datetime(1990, 5, 15)
    )
    
    inicio = time.time()
    resultado_joao = criar_cliente_uc.executar(comando_joao)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_joao.sucesso:
        print(f"✅ {resultado_joao.mensagem}")
        print(f"   ID: {resultado_joao.cliente_id}")
        cliente_joao_id = resultado_joao.cliente_id
        
        # Processar eventos
        for evento in criar_cliente_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_joao.mensagem}")
        return
    
    coletor_metricas.registrar_operacao("criar_cliente", tempo_ms, resultado_joao.sucesso)
    
    # Cliente 2: Maria Santos
    print("\n📝 Criando Cliente 2: Maria Santos")
    comando_maria = ComandoCriarCliente(
        nome="Maria Santos",
        cpf="52998224725",  # CPF válido
        endereco_cep="22070-900",
        endereco_logradouro="Av. Atlântica",
        endereco_numero="2000",
        endereco_complemento=None,
        endereco_bairro="Copacabana",
        endereco_cidade="Rio de Janeiro",
        endereco_uf="RJ",
        telefone="21888776655",
        email="maria.santos@email.com",
        data_nascimento=datetime(1985, 10, 22)
    )
    
    inicio = time.time()
    resultado_maria = criar_cliente_uc.executar(comando_maria)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_maria.sucesso:
        print(f"✅ {resultado_maria.mensagem}")
        print(f"   ID: {resultado_maria.cliente_id}")
        cliente_maria_id = resultado_maria.cliente_id
        
        # Processar eventos
        for evento in criar_cliente_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_maria.mensagem}")
        return
    
    coletor_metricas.registrar_operacao("criar_cliente", tempo_ms, resultado_maria.sucesso)
    
    # Configurar emails para notificações
    notificador.definir_email_cliente(cliente_joao_id, "joao.silva@email.com")
    notificador.definir_email_cliente(cliente_maria_id, "maria.santos@email.com")
    
    # =================================================================
    # 4. DEMONSTRAÇÃO: ABERTURA DE CONTAS
    # =================================================================
    
    print("\n🏦 4. DEMONSTRANDO ABERTURA DE CONTAS")
    print("-" * 50)
    
    # Conta Corrente para João
    print("\n💳 Abrindo conta corrente para João")
    comando_conta_joao = ComandoAbrirConta(
        cliente_id=cliente_joao_id,
        tipo_conta=TipoConta.CORRENTE,
        agencia="0001",
        deposito_inicial=Dinheiro(Decimal("1500.00"))
    )
    
    inicio = time.time()
    resultado_conta_joao = abrir_conta_uc.executar(comando_conta_joao)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_conta_joao.sucesso:
        print(f"✅ {resultado_conta_joao.mensagem}")
        print(f"   Agência: {resultado_conta_joao.agencia}")
        print(f"   Conta: {resultado_conta_joao.numero}")
        conta_joao_id = resultado_conta_joao.conta_id
        
        # Processar eventos
        for evento in abrir_conta_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_conta_joao.mensagem}")
        return
    
    coletor_metricas.registrar_operacao("abrir_conta", tempo_ms, resultado_conta_joao.sucesso)
    
    # Conta Poupança para Maria
    print("\n💰 Abrindo conta poupança para Maria")
    comando_conta_maria = ComandoAbrirConta(
        cliente_id=cliente_maria_id,
        tipo_conta=TipoConta.POUPANCA,
        agencia="0001",
        deposito_inicial=Dinheiro(Decimal("800.00"))
    )
    
    inicio = time.time()
    resultado_conta_maria = abrir_conta_uc.executar(comando_conta_maria)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_conta_maria.sucesso:
        print(f"✅ {resultado_conta_maria.mensagem}")
        print(f"   Agência: {resultado_conta_maria.agencia}")
        print(f"   Conta: {resultado_conta_maria.numero}")
        conta_maria_id = resultado_conta_maria.conta_id
        
        # Processar eventos
        for evento in abrir_conta_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_conta_maria.mensagem}")
        return
    
    coletor_metricas.registrar_operacao("abrir_conta", tempo_ms, resultado_conta_maria.sucesso)
    
    # =================================================================
    # 5. DEMONSTRAÇÃO: CONSULTA DE SALDOS
    # =================================================================
    
    print("\n💰 5. CONSULTANDO SALDOS INICIAIS")
    print("-" * 50)
    
    conta_joao = repo_conta.buscar_por_id(conta_joao_id)
    conta_maria = repo_conta.buscar_por_id(conta_maria_id)
    
    print(f"💳 João Silva - Conta Corrente:")
    print(f"   Saldo: {conta_joao.saldo.formatado}")
    print(f"   Limite diário disponível: {conta_joao.limite_diario_disponivel.formatado}")
    
    print(f"💰 Maria Santos - Conta Poupança:")
    print(f"   Saldo: {conta_maria.saldo.formatado}")
    print(f"   Limite diário disponível: {conta_maria.limite_diario_disponivel.formatado}")
    
    # =================================================================
    # 6. DEMONSTRAÇÃO: TRANSFERÊNCIAS
    # =================================================================
    
    print("\n💸 6. DEMONSTRANDO TRANSFERÊNCIAS")
    print("-" * 50)
    
    # Transferência 1: João → Maria (R$ 300)
    print("\n🔄 Transferência 1: João → Maria (R$ 300,00)")
    comando_transf1 = ComandoRealizarTransferencia(
        conta_origem_id=conta_joao_id,
        conta_destino_id=conta_maria_id,
        valor=Dinheiro(Decimal("300.00")),
        descricao="Transferência de aniversário"
    )
    
    inicio = time.time()
    resultado_transf1 = transferencia_uc.executar(comando_transf1)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_transf1.sucesso:
        print(f"✅ {resultado_transf1.mensagem}")
        print(f"   ID Transação: {resultado_transf1.transacao_id}")
        
        # Processar eventos
        for evento in transferencia_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_transf1.mensagem}")
    
    coletor_metricas.registrar_operacao("transferencia", tempo_ms, resultado_transf1.sucesso)
    
    # Aguardar processamento assíncrono
    time.sleep(0.5)
    
    # Transferência 2: Maria → João (R$ 150)
    print("\n🔄 Transferência 2: Maria → João (R$ 150,00)")
    comando_transf2 = ComandoRealizarTransferencia(
        conta_origem_id=conta_maria_id,
        conta_destino_id=conta_joao_id,
        valor=Dinheiro(Decimal("150.00")),
        descricao="Reembolso de jantar"
    )
    
    inicio = time.time()
    resultado_transf2 = transferencia_uc.executar(comando_transf2)
    tempo_ms = (time.time() - inicio) * 1000
    
    if resultado_transf2.sucesso:
        print(f"✅ {resultado_transf2.mensagem}")
        print(f"   ID Transação: {resultado_transf2.transacao_id}")
        
        # Processar eventos
        for evento in transferencia_uc.obter_eventos():
            processador_eventos.processar(evento)
    else:
        print(f"❌ {resultado_transf2.mensagem}")
    
    coletor_metricas.registrar_operacao("transferencia", tempo_ms, resultado_transf2.sucesso)
    
    # Aguardar processamento assíncrono
    time.sleep(0.5)
    
    # =================================================================
    # 7. DEMONSTRAÇÃO: SALDOS APÓS TRANSFERÊNCIAS
    # =================================================================
    
    print("\n💰 7. SALDOS APÓS TRANSFERÊNCIAS")
    print("-" * 50)
    
    # Recarregar contas do repositório
    conta_joao = repo_conta.buscar_por_id(conta_joao_id)
    conta_maria = repo_conta.buscar_por_id(conta_maria_id)
    
    print(f"💳 João Silva - Conta Corrente:")
    print(f"   Saldo: {conta_joao.saldo.formatado}")
    print(f"   Limite usado hoje: {conta_joao._limite_usado_hoje.formatado}")
    
    print(f"💰 Maria Santos - Conta Poupança:")
    print(f"   Saldo: {conta_maria.saldo.formatado}")
    print(f"   Limite usado hoje: {conta_maria._limite_usado_hoje.formatado}")
    
    # =================================================================
    # 8. DEMONSTRAÇÃO: VALIDAÇÃO DE FRAUDE
    # =================================================================
    
    print("\n🔐 8. DEMONSTRANDO VALIDAÇÃO DE FRAUDE")
    print("-" * 50)
    
    # Tentar transferência suspeita (valor alto)
    print("\n⚠️ Tentativa de transferência suspeita: R$ 10.000,00")
    comando_suspeito = ComandoRealizarTransferencia(
        conta_origem_id=conta_joao_id,
        conta_destino_id=conta_maria_id,
        valor=Dinheiro(Decimal("10000.00")),
        descricao="Transferência de valor alto"
    )
    
    resultado_suspeito = transferencia_uc.executar(comando_suspeito)
    if resultado_suspeito.sucesso:
        print(f"✅ Transferência aprovada: {resultado_suspeito.mensagem}")
    else:
        print(f"🚫 Transferência bloqueada: {resultado_suspeito.mensagem}")
    
    # =================================================================
    # 9. DEMONSTRAÇÃO: HISTÓRICO DE TRANSAÇÕES
    # =================================================================
    
    print("\n📊 9. HISTÓRICO DE TRANSAÇÕES")
    print("-" * 50)
    
    # Transações da conta do João
    transacoes_joao = repo_transacao.listar_por_conta(conta_joao_id)
    print(f"\n💳 Transações de João Silva ({len(transacoes_joao)} transações):")
    for i, transacao in enumerate(transacoes_joao, 1):
        print(f"   {i}. {transacao.tipo.value} - {transacao.valor.formatado}")
        print(f"      {transacao.descricao}")
        print(f"      {transacao.data_criacao.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.status.value}")
    
    # Transações da conta da Maria
    transacoes_maria = repo_transacao.listar_por_conta(conta_maria_id)
    print(f"\n💰 Transações de Maria Santos ({len(transacoes_maria)} transações):")
    for i, transacao in enumerate(transacoes_maria, 1):
        print(f"   {i}. {transacao.tipo.value} - {transacao.valor.formatado}")
        print(f"      {transacao.descricao}")
        print(f"      {transacao.data_criacao.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.status.value}")
    
    # =================================================================
    # 10. DEMONSTRAÇÃO: CONSULTA EXTERNA DE CRÉDITO
    # =================================================================
    
    print("\n🔍 10. DEMONSTRANDO CONSULTA EXTERNA DE CRÉDITO")
    print("-" * 50)
    
    # Consultar score do João
    cpf_joao = CPF("11144477735")  # CPF válido
    score_joao = consultor_credito.consultar_score(cpf_joao)
    restricoes_joao = consultor_credito.consultar_restricoes(cpf_joao)
    
    print(f"📊 João Silva (CPF: {cpf_joao.formatado}):")
    print(f"   Score: {score_joao}")
    print(f"   Restrições: {restricoes_joao if restricoes_joao else 'Nenhuma'}")
    
    # Consultar score da Maria
    cpf_maria = CPF("52998224725")  # CPF válido
    score_maria = consultor_credito.consultar_score(cpf_maria)
    restricoes_maria = consultor_credito.consultar_restricoes(cpf_maria)
    
    print(f"📊 Maria Santos (CPF: {cpf_maria.formatado}):")
    print(f"   Score: {score_maria}")
    print(f"   Restrições: {restricoes_maria if restricoes_maria else 'Nenhuma'}")
    
    # =================================================================
    # 11. DEMONSTRAÇÃO: MÉTRICAS DO SISTEMA
    # =================================================================
    
    print("\n📈 11. MÉTRICAS DO SISTEMA")
    print("-" * 50)
    
    relatorio_metricas = coletor_metricas.obter_relatorio()
    
    print("📊 Operações realizadas:")
    for operacao, valor in relatorio_metricas["metricas_gerais"].items():
        if "_total" in operacao:
            print(f"   {operacao}: {valor}")
    
    print("\n⏱️ Performance das operações:")
    for operacao, stats in relatorio_metricas["tempos_operacao"].items():
        print(f"   {operacao}:")
        print(f"     Tempo médio: {stats['media_ms']:.2f}ms")
        print(f"     Min/Max: {stats['min_ms']:.2f}ms / {stats['max_ms']:.2f}ms")
    
    # =================================================================
    # 12. DEMONSTRAÇÃO: RELATÓRIO DE AUDITORIA
    # =================================================================
    
    print("\n📋 12. RELATÓRIO DE AUDITORIA")
    print("-" * 50)
    
    # Aguardar processamento de eventos
    time.sleep(1)
    
    # Gerar relatório de compliance
    data_inicio = datetime.now() - timedelta(hours=1)
    data_fim = datetime.now()
    
    relatorio_compliance = auditoria.gerar_relatorio_compliance(data_inicio, data_fim)
    
    print(f"📊 Eventos auditados: {relatorio_compliance['total_eventos']}")
    print("📈 Tipos de evento:")
    for tipo, count in relatorio_compliance["tipos_evento"].items():
        print(f"   {tipo}: {count}")
    
    if relatorio_compliance["transacoes_suspeitas"]:
        print("⚠️ Transações suspeitas detectadas:")
        for ts in relatorio_compliance["transacoes_suspeitas"]:
            print(f"   Valor: R$ {ts['valor']:.2f} - ID: {ts['transacao_id']}")
    else:
        print("✅ Nenhuma transação suspeita detectada")
    
    print("💰 Valores movimentados por tipo:")
    for tipo, valor in relatorio_compliance["valores_movimentados"].items():
        if valor > 0:
            print(f"   {tipo}: R$ {valor:.2f}")
    
    # =================================================================
    # 13. DEMONSTRAÇÃO: EXTENSIBILIDADE (NOVOS ADAPTERS)
    # =================================================================
    
    print("\n🔌 13. DEMONSTRANDO EXTENSIBILIDADE")
    print("-" * 50)
    
    print("🏗️ Criando novo adapter para notificação via SMS...")
    
    class NotificadorSMS:
        """Novo adapter para notificações via SMS"""
        
        def notificar_transacao_realizada(self, transacao, conta_origem, conta_destino):
            if conta_origem:
                print(f"📱 SMS para conta origem: Transação {transacao.tipo.value} "
                      f"de {transacao.valor.formatado} realizada")
            if conta_destino:
                print(f"📱 SMS para conta destino: Depósito de {transacao.valor.formatado} recebido")
    
    # Adicionar novo notificador
    notificador_sms = NotificadorSMS()
    
    # Criar novo caso de uso com múltiplos notificadores
    class TransferenciaComMultiplosNotificadores(RealizarTransferenciaUseCase):
        def __init__(self, repo_conta, repo_transacao, validador_fraude, 
                     notificador_email, notificador_sms):
            super().__init__(repo_conta, repo_transacao, validador_fraude, notificador_email)
            self._notificador_sms = notificador_sms
        
        def executar(self, comando):
            resultado = super().executar(comando)
            
            # Notificar via SMS também (se sucesso)
            if resultado.sucesso:
                conta_origem = self._repo_conta.buscar_por_id(comando.conta_origem_id)
                conta_destino = self._repo_conta.buscar_por_id(comando.conta_destino_id)
                transacao = self._repo_transacao.buscar_por_id(resultado.transacao_id)
                
                self._notificador_sms.notificar_transacao_realizada(
                    transacao, conta_origem, conta_destino
                )
            
            return resultado
    
    # Usar novo caso de uso
    transferencia_multi_uc = TransferenciaComMultiplosNotificadores(
        repo_conta, repo_transacao, validador_fraude, notificador, notificador_sms
    )
    
    print("✅ Novo adapter SMS adicionado sem modificar código existente!")
    
    # Testar nova funcionalidade
    print("\n🧪 Testando transferência com múltiplas notificações:")
    comando_teste = ComandoRealizarTransferencia(
        conta_origem_id=conta_maria_id,
        conta_destino_id=conta_joao_id,
        valor=Dinheiro(Decimal("50.00")),
        descricao="Teste de múltiplos notificadores"
    )
    
    resultado_teste = transferencia_multi_uc.executar(comando_teste)
    if resultado_teste.sucesso:
        print(f"✅ {resultado_teste.mensagem}")
    
    # =================================================================
    # 14. FINALIZAÇÃO E RESUMO
    # =================================================================
    
    print("\n🏁 14. RESUMO DA DEMONSTRAÇÃO")
    print("=" * 70)
    
    print("🎯 PADRÕES E PRINCÍPIOS DEMONSTRADOS:")
    print()
    print("🔷 Arquitetura Hexagonal (Ports & Adapters):")
    print("   • Domínio isolado de infraestrutura")
    print("   • Ports (interfaces) definem contratos")
    print("   • Adapters implementam integrações")
    print("   • Testabilidade e flexibilidade máximas")
    
    print("\n🔷 Domain-Driven Design (DDD):")
    print("   • Value Objects (CPF, Dinheiro, Endereco)")
    print("   • Entities (Cliente, Conta, Transacao)")
    print("   • Domain Events para comunicação")
    print("   • Rich domain model com comportamentos")
    
    print("\n🔷 Princípios SOLID:")
    print("   • SRP: Cada classe tem responsabilidade única")
    print("   • OCP: Extensível sem modificar código existente")
    print("   • LSP: Adapters substituíveis transparentemente")
    print("   • ISP: Interfaces específicas e focadas")
    print("   • DIP: Dependências invertidas via interfaces")
    
    print("\n🔷 Design Patterns:")
    print("   • Repository Pattern: Abstração de persistência")
    print("   • Command Pattern: Encapsulamento de operações")
    print("   • Observer Pattern: Processamento de eventos")
    print("   • Strategy Pattern: Algoritmos intercambiáveis")
    print("   • Factory Pattern: Criação de objetos")
    print("   • Adapter Pattern: Integração com sistemas externos")
    
    print("\n🔷 Características Arquiteturais:")
    print("   • Separação clara de responsabilidades")
    print("   • Testabilidade em todas as camadas")
    print("   • Extensibilidade e manutenibilidade")
    print("   • Performance e escalabilidade")
    print("   • Auditoria e compliance")
    print("   • Segurança e validação de fraude")
    
    # Finalizar processador de eventos
    processador_eventos.parar()
    
    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrar_sistema_bancario()
