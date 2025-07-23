#!/usr/bin/env python3
"""
SISTEMA DE MONITORAMENTO DISTRIBUÍDO - DEMONSTRAÇÃO PRINCIPAL
Padrões Arquiteturais Avançados

Este arquivo demonstra um sistema completo de monitoramento distribuído
implementando padrões avançados para sistemas de alta disponibilidade.

EXECUTAR: python main.py

AUTOR: Prof. Jackson Antonio do Prado Lima
"""

import sys
import os
import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(current_dir)

# Imports dos padrões
from patterns import (
    EventoSistema, TipoEvento, SeveridadeAlerta, StatusServico,
    Metrica, Alerta, Servico,
    EventStore, QueryModel,
    CircuitBreaker, CircuitBreakerAbertoException,
    RetryStrategy, RetryExecutor, RetryExhaustedException,
    EventBus,
    RecursoBulkhead, BulkheadTimeoutException,
    SimuladorServico
)


def demonstrar_sistema_monitoramento():
    """
    Demonstração completa do sistema de monitoramento distribuído
    """
    
    print("🏗️ SISTEMA DE MONITORAMENTO DISTRIBUÍDO")
    print("=" * 70)
    print("Demonstrando Padrões Arquiteturais Avançados para")
    print("Sistemas Distribuídos de Alta Disponibilidade")
    print()
    print("🎯 PADRÕES IMPLEMENTADOS:")
    print("• Event Sourcing & CQRS")
    print("• Circuit Breaker Pattern") 
    print("• Retry Pattern com Backoff Exponencial")
    print("• Publish-Subscribe Pattern")
    print("• Bulkhead Pattern")
    print("• Observer Pattern")
    print("=" * 70)
    
    # =================================================================
    # 1. CONFIGURAÇÃO DA INFRAESTRUTURA
    # =================================================================
    
    print("\n🔧 1. CONFIGURANDO INFRAESTRUTURA")
    print("-" * 50)
    
    # Event Store para Event Sourcing
    event_store = EventStore()
    print("✅ Event Store configurado")
    
    # Query Model para CQRS
    query_model = QueryModel(event_store)
    print("✅ Query Model (CQRS) configurado")
    
    # Event Bus para Pub/Sub
    event_bus = EventBus("MonitoramentoBus")
    print("✅ Event Bus configurado")
    
    # Circuit Breakers para serviços
    cb_api_pagamento = CircuitBreaker(
        threshold_falhas=3,
        timeout_segundos=30,
        nome="API_Pagamento"
    )
    cb_api_usuario = CircuitBreaker(
        threshold_falhas=5,
        timeout_segundos=60,
        nome="API_Usuario"
    )
    print("✅ Circuit Breakers configurados")
    
    # Retry Executors
    retry_strategy = RetryStrategy(
        max_tentativas=3,
        delay_inicial_ms=100,
        multiplicador=2.0,
        delay_maximo_ms=5000
    )
    retry_executor = RetryExecutor(retry_strategy, "MonitoramentoRetry")
    print("✅ Retry Strategy configurado")
    
    # Bulkheads para isolamento de recursos
    bulkhead_api = RecursoBulkhead("API_Pool", tamanho_pool=5)
    bulkhead_db = RecursoBulkhead("Database_Pool", tamanho_pool=3)
    bulkhead_cache = RecursoBulkhead("Cache_Pool", tamanho_pool=8)
    print("✅ Bulkheads configurados")
    
    # Simuladores de serviços
    servico_pagamento = SimuladorServico("PagamentoAPI", taxa_falha=0.15)
    servico_usuario = SimuladorServico("UsuarioAPI", taxa_falha=0.05)
    servico_notificacao = SimuladorServico("NotificacaoAPI", taxa_falha=0.2)
    print("✅ Simuladores de serviços configurados")
    
    # =================================================================
    # 2. CONFIGURAÇÃO DE HANDLERS DE EVENTOS
    # =================================================================
    
    print("\n📡 2. CONFIGURANDO EVENT HANDLERS")
    print("-" * 50)
    
    # Handler para métricas críticas
    def handler_metricas_criticas(evento: EventoSistema):
        if evento.tipo == TipoEvento.METRICA_COLETADA:
            dados = evento.dados
            valor = dados.get('valor', 0)
            nome = dados.get('nome', '')
            
            # Detectar métricas críticas
            if nome == 'cpu_usage' and isinstance(valor, (int, float)) and valor > 90:
                # Gerar alerta crítico
                alerta_evento = EventoSistema(
                    tipo=TipoEvento.ALERTA_GERADO,
                    origem=evento.origem,
                    dados={
                        'id': f'alert_{evento.id}',
                        'titulo': 'CPU Alta',
                        'descricao': f'CPU em {valor}% no serviço {evento.origem}',
                        'severidade': SeveridadeAlerta.CRITICAL.value,
                        'metadados': {'cpu_value': valor}
                    }
                )
                event_store.adicionar_evento(alerta_evento)
                event_bus.publicar(alerta_evento)
                print(f"🚨 ALERTA CRÍTICO: CPU {valor}% em {evento.origem}")
            
            elif nome == 'response_time_ms' and isinstance(valor, (int, float)) and valor > 5000:
                # Alerta de latência alta
                alerta_evento = EventoSistema(
                    tipo=TipoEvento.ALERTA_GERADO,
                    origem=evento.origem,
                    dados={
                        'id': f'alert_{evento.id}',
                        'titulo': 'Latência Alta',
                        'descricao': f'Tempo de resposta: {valor}ms',
                        'severidade': SeveridadeAlerta.WARNING.value,
                        'metadados': {'response_time': valor}
                    }
                )
                event_store.adicionar_evento(alerta_evento)
                event_bus.publicar(alerta_evento)
                print(f"⚠️ ALERTA: Latência alta {valor}ms em {evento.origem}")
    
    # Handler para indisponibilidade de sistema
    def handler_sistema_indisponivel(evento: EventoSistema):
        if evento.tipo == TipoEvento.SISTEMA_INDISPONIVEL:
            print(f"🔴 SISTEMA INDISPONÍVEL: {evento.origem}")
            
            # Gerar alerta crítico automaticamente
            alerta_evento = EventoSistema(
                tipo=TipoEvento.ALERTA_GERADO,
                origem=evento.origem,
                dados={
                    'id': f'outage_alert_{evento.id}',
                    'titulo': 'Sistema Indisponível',
                    'descricao': f'O serviço {evento.origem} está indisponível',
                    'severidade': SeveridadeAlerta.CRITICAL.value,
                    'metadados': evento.dados
                }
            )
            event_store.adicionar_evento(alerta_evento)
            event_bus.publicar(alerta_evento)
    
    # Handler para logging geral
    def handler_logging(evento: EventoSistema):
        timestamp = evento.timestamp.strftime("%H:%M:%S.%f")[:-3]
        origem = evento.origem[:15].ljust(15)
        tipo = evento.tipo.value[:20].ljust(20)
        print(f"📝 {timestamp} | {origem} | {tipo} | {evento.id[:8]}")
    
    # Registrar handlers
    event_bus.subscrever(TipoEvento.METRICA_COLETADA.value, handler_metricas_criticas)
    event_bus.subscrever(TipoEvento.SISTEMA_INDISPONIVEL.value, handler_sistema_indisponivel)
    event_bus.subscrever_global(handler_logging)
    print("✅ Event handlers registrados")
    
    # =================================================================
    # 3. SIMULAÇÃO DE INICIALIZAÇÃO DE SERVIÇOS
    # =================================================================
    
    print("\n🚀 3. INICIANDO SERVIÇOS")
    print("-" * 50)
    
    servicos_config = [
        ("pagamento-api", "http://api-pagamento.empresa.com", servico_pagamento),
        ("usuario-api", "http://api-usuario.empresa.com", servico_usuario),
        ("notificacao-api", "http://api-notificacao.empresa.com", servico_notificacao),
        ("web-frontend", "http://app.empresa.com", None),
        ("database-primary", "db://primary.empresa.com", None)
    ]
    
    for servico_id, url, simulador in servicos_config:
        # Criar evento de serviço iniciado
        evento_inicio = EventoSistema(
            tipo=TipoEvento.SERVICO_INICIADO,
            origem=servico_id,
            dados={
                'nome': servico_id.replace('-', ' ').title(),
                'url': url,
                'configuracao': {
                    'timeout_ms': 5000,
                    'max_connections': 100,
                    'health_check_interval': 30
                }
            }
        )
        
        # Adicionar ao Event Store
        event_store.adicionar_evento(evento_inicio)
        
        # Publicar no Event Bus
        event_bus.publicar(evento_inicio, assincrono=False)
        
        time.sleep(0.1)  # Simular tempo de inicialização
    
    print(f"✅ {len(servicos_config)} serviços iniciados")
    
    # =================================================================
    # 4. DEMONSTRAÇÃO DE COLETA DE MÉTRICAS COM EVENT SOURCING
    # =================================================================
    
    print("\n📊 4. COLETANDO MÉTRICAS (EVENT SOURCING)")
    print("-" * 50)
    
    def coletar_metricas_servico(servico_id: str, num_metricas: int = 5):
        """Simula coleta de métricas de um serviço"""
        metricas_tipos = [
            ('cpu_usage', lambda: random.uniform(30, 95), '%'),
            ('memory_usage', lambda: random.uniform(40, 85), '%'),
            ('response_time_ms', lambda: random.randint(50, 8000), 'ms'),
            ('requests_per_second', lambda: random.randint(10, 500), 'req/s'),
            ('error_rate', lambda: random.uniform(0, 15), '%')
        ]
        
        for _ in range(num_metricas):
            nome, gerador_valor, unidade = random.choice(metricas_tipos)
            valor = gerador_valor()
            
            evento_metrica = EventoSistema(
                tipo=TipoEvento.METRICA_COLETADA,
                origem=servico_id,
                dados={
                    'nome': nome,
                    'valor': valor,
                    'unidade': unidade,
                    'tags': {
                        'environment': 'production',
                        'region': 'us-east-1'
                    }
                }
            )
            
            event_store.adicionar_evento(evento_metrica)
            event_bus.publicar(evento_metrica, assincrono=False)
            
            time.sleep(0.05)  # Simular intervalo entre métricas
    
    # Coletar métricas para cada serviço
    for servico_id, _, _ in servicos_config:
        coletar_metricas_servico(servico_id, 3)
    
    print("✅ Métricas coletadas e eventos gerados")
    
    # =================================================================
    # 5. DEMONSTRAÇÃO DE CIRCUIT BREAKER
    # =================================================================
    
    print("\n⚡ 5. DEMONSTRANDO CIRCUIT BREAKER")
    print("-" * 50)
    
    @cb_api_pagamento
    def chamar_api_pagamento():
        """Simula chamada para API de pagamento"""
        with bulkhead_api.adquirir_recurso():
            return servico_pagamento.fazer_requisicao()
    
    @cb_api_usuario
    def chamar_api_usuario():
        """Simula chamada para API de usuário"""
        with bulkhead_api.adquirir_recurso():
            return servico_usuario.fazer_requisicao()
    
    print("🧪 Testando APIs com Circuit Breaker...")
    
    # Fazer algumas chamadas bem-sucedidas
    sucessos = 0
    falhas = 0
    
    for i in range(10):
        try:
            resultado = chamar_api_pagamento()
            sucessos += 1
            print(f"✅ Pagamento #{i+1}: {resultado['status']}")
        except CircuitBreakerAbertoException as e:
            print(f"🔴 Circuit Breaker: {e}")
            break
        except Exception as e:
            falhas += 1
            print(f"❌ Falha #{i+1}: {str(e)[:50]}")
        
        time.sleep(0.1)
    
    print(f"📊 Resultados: {sucessos} sucessos, {falhas} falhas")
    
    # Mostrar métricas do circuit breaker
    metricas_cb = cb_api_pagamento.obter_metricas()
    print(f"🔧 Circuit Breaker Estado: {metricas_cb['estado']}")
    print(f"🔧 Taxa de Sucesso: {metricas_cb['taxa_sucesso_pct']}%")
    
    # =================================================================
    # 6. DEMONSTRAÇÃO DE RETRY PATTERN
    # =================================================================
    
    print("\n🔄 6. DEMONSTRANDO RETRY PATTERN")
    print("-" * 50)
    
    def operacao_instavel():
        """Simula operação que falha ocasionalmente"""
        if random.random() < 0.7:  # 70% chance de falha
            raise Exception("Falha temporária na operação")
        return "Operação executada com sucesso"
    
    print("🧪 Testando operação instável com retry...")
    
    for i in range(3):
        try:
            resultado = retry_executor.executar(operacao_instavel)
            print(f"✅ Tentativa {i+1}: {resultado}")
        except RetryExhaustedException as e:
            print(f"❌ Tentativa {i+1}: Todas as tentativas falharam")
        except Exception as e:
            print(f"❌ Tentativa {i+1}: {e}")
        
        time.sleep(0.5)
    
    # Mostrar métricas do retry executor
    metricas_retry = retry_executor.obter_metricas()
    print(f"🔧 Taxa de Sucesso Retry: {metricas_retry['taxa_sucesso_pct']:.1f}%")
    print(f"🔧 Média de Tentativas: {metricas_retry['media_tentativas']:.1f}")
    
    # =================================================================
    # 7. DEMONSTRAÇÃO DE BULKHEAD PATTERN
    # =================================================================
    
    print("\n🏗️ 7. DEMONSTRANDO BULKHEAD PATTERN")
    print("-" * 50)
    
    def operacao_com_recursos(bulkhead: RecursoBulkhead, nome: str, duracao: float):
        """Simula operação que usa recursos do bulkhead"""
        try:
            with bulkhead.adquirir_recurso(timeout_segundos=2.0) as recurso:
                print(f"🔧 {nome}: Recurso adquirido, processando por {duracao:.1f}s")
                time.sleep(duracao)
                print(f"✅ {nome}: Operação concluída")
                return True
        except BulkheadTimeoutException as e:
            print(f"⏰ {nome}: Timeout - {e}")
            return False
    
    print("🧪 Testando isolamento de recursos...")
    
    # Simular múltiplas operações concorrentes
    threads = []
    
    # Pool de API - operações rápidas e lentas
    for i in range(8):  # Mais que o limite do pool (5)
        duracao = random.uniform(0.5, 2.0)
        thread = threading.Thread(
            target=operacao_com_recursos,
            args=(bulkhead_api, f"API-Op-{i+1}", duracao)
        )
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Espaçar início das operações
    
    # Aguardar conclusão
    for thread in threads:
        thread.join()
    
    # Mostrar métricas dos bulkheads
    print("\n📊 Métricas dos Bulkheads:")
    for bulkhead in [bulkhead_api, bulkhead_db, bulkhead_cache]:
        metricas = bulkhead.obter_metricas()
        print(f"🔧 {metricas['nome']}: {metricas['utilizacao_atual_pct']:.1f}% utilização")
        print(f"   Timeouts: {metricas['total_timeouts']} de {metricas['total_aquisicoes']}")
    
    # =================================================================
    # 8. SIMULAÇÃO DE FALHA DE SISTEMA
    # =================================================================
    
    print("\n💥 8. SIMULANDO FALHA DE SISTEMA")
    print("-" * 50)
    
    # Simular falha do serviço de pagamento
    print("🔴 Simulando falha no serviço de pagamento...")
    servico_pagamento.definir_ativo(False)
    
    # Gerar evento de sistema indisponível
    evento_falha = EventoSistema(
        tipo=TipoEvento.SISTEMA_INDISPONIVEL,
        origem="pagamento-api",
        dados={
            'motivo': 'Falha simulada para demonstração',
            'impacto': 'Alto - Processamento de pagamentos afetado',
            'estimativa_recuperacao': '15 minutos'
        }
    )
    
    event_store.adicionar_evento(evento_falha)
    event_bus.publicar(evento_falha, assincrono=False)
    
    time.sleep(1)
    
    # Simular recuperação
    print("🟢 Simulando recuperação do serviço...")
    servico_pagamento.definir_ativo(True)
    servico_pagamento.definir_taxa_falha(0.02)  # Reduzir taxa de falha
    
    evento_recuperacao = EventoSistema(
        tipo=TipoEvento.SISTEMA_RECUPERADO,
        origem="pagamento-api",
        dados={
            'tempo_indisponibilidade': '2 minutos',
            'acao_recuperacao': 'Restart automático do serviço',
            'status_pos_recuperacao': 'Estável'
        }
    )
    
    event_store.adicionar_evento(evento_recuperacao)
    event_bus.publicar(evento_recuperacao, assincrono=False)
    
    # Reset do circuit breaker após recuperação
    cb_api_pagamento.reset()
    print("🔧 Circuit Breaker resetado após recuperação")
    
    # =================================================================
    # 9. CONSULTAS CQRS
    # =================================================================
    
    print("\n🔍 9. CONSULTAS CQRS - QUERY MODEL")
    print("-" * 50)
    
    # Atualizar projeções
    query_model.atualizar_projecoes()
    
    # Consultar serviços
    servicos = query_model.obter_servicos()
    print(f"📊 Total de serviços monitorados: {len(servicos)}")
    
    for servico in servicos:
        print(f"🔧 {servico.nome}: {servico.status.value}")
        print(f"   Métricas coletadas: {len(servico.metricas)}")
        print(f"   Alertas ativos: {len(servico.alertas_ativos)}")
    
    # Consultar alertas ativos
    alertas_ativos = query_model.obter_alertas_ativos()
    print(f"\n🚨 Alertas ativos: {len(alertas_ativos)}")
    
    for alerta in alertas_ativos[-5:]:  # Mostrar últimos 5
        severidade_emoji = {
            SeveridadeAlerta.INFO: "ℹ️",
            SeveridadeAlerta.WARNING: "⚠️", 
            SeveridadeAlerta.ERROR: "❌",
            SeveridadeAlerta.CRITICAL: "🚨"
        }
        emoji = severidade_emoji.get(alerta.severidade, "📢")
        print(f"{emoji} {alerta.titulo}: {alerta.descricao}")
    
    # Consultar métricas agregadas
    print(f"\n📊 Métricas Agregadas:")
    for nome_metrica in ['cpu_usage', 'response_time_ms', 'memory_usage']:
        agregacao = query_model.obter_metricas_agregadas(nome_metrica)
        if agregacao:
            print(f"🔧 {nome_metrica}:")
            print(f"   Média: {agregacao.get('media', 0):.2f}")
            print(f"   Min/Max: {agregacao.get('min', 0):.2f} / {agregacao.get('max', 0):.2f}")
            print(f"   Amostras: {agregacao.get('count', 0)}")
    
    # =================================================================
    # 10. RELATÓRIO DE EVENTOS (EVENT SOURCING)
    # =================================================================
    
    print("\n📋 10. RELATÓRIO DE EVENTOS - EVENT SOURCING")
    print("-" * 50)
    
    # Consultar eventos por tipo
    tipos_evento = {}
    todos_eventos = event_store.obter_todos_eventos()
    
    for evento in todos_eventos:
        tipo = evento.tipo.value
        tipos_evento[tipo] = tipos_evento.get(tipo, 0) + 1
    
    print(f"📊 Total de eventos no sistema: {len(todos_eventos)}")
    print("📈 Distribuição por tipo:")
    for tipo, count in sorted(tipos_evento.items()):
        print(f"   {tipo}: {count} eventos")
    
    # Timeline dos últimos eventos
    print(f"\n⏰ Timeline dos últimos eventos:")
    ultimos_eventos = todos_eventos[-10:]
    for evento in ultimos_eventos:
        timestamp = evento.timestamp.strftime("%H:%M:%S")
        print(f"   {timestamp} | {evento.origem[:15].ljust(15)} | {evento.tipo.value}")
    
    # =================================================================
    # 11. MÉTRICAS DO SISTEMA
    # =================================================================
    
    print("\n📈 11. MÉTRICAS DO SISTEMA")
    print("-" * 50)
    
    # Métricas do Event Bus
    metricas_bus = event_bus.obter_metricas()
    print(f"📡 Event Bus:")
    print(f"   Eventos publicados: {metricas_bus['eventos_publicados']}")
    print(f"   Eventos processados: {metricas_bus['eventos_processados']}")
    print(f"   Subscribers ativos: {metricas_bus['total_subscribers']}")
    
    # Métricas dos Circuit Breakers
    print(f"\n⚡ Circuit Breakers:")
    for cb in [cb_api_pagamento, cb_api_usuario]:
        metricas = cb.obter_metricas()
        print(f"   {metricas['nome']}:")
        print(f"     Estado: {metricas['estado']}")
        print(f"     Taxa sucesso: {metricas['taxa_sucesso_pct']}%")
        print(f"     Total chamadas: {metricas['total_chamadas']}")
    
    # Métricas dos Bulkheads
    print(f"\n🏗️ Bulkheads:")
    for bulkhead in [bulkhead_api, bulkhead_db, bulkhead_cache]:
        metricas = bulkhead.obter_metricas()
        print(f"   {metricas['nome']}:")
        print(f"     Utilização máxima: {metricas['max_recursos_utilizados']}/{metricas['tamanho_pool']}")
        print(f"     Taxa timeout: {metricas['taxa_timeout_pct']:.1f}%")
    
    # =================================================================
    # 12. FINALIZAÇÃO
    # =================================================================
    
    print("\n🏁 12. RESUMO DA DEMONSTRAÇÃO")
    print("=" * 70)
    
    print("🎯 PADRÕES DEMONSTRADOS:")
    print()
    print("🔷 Event Sourcing:")
    print("   • Armazenamento imutável de eventos")
    print("   • Reconstrução de estado a partir de eventos")
    print("   • Auditoria completa de mudanças")
    
    print("\n🔷 CQRS (Command Query Responsibility Segregation):")
    print("   • Separação entre comandos e consultas")
    print("   • Query model otimizado para leitura")
    print("   • Projeções atualizadas automaticamente")
    
    print("\n🔷 Circuit Breaker Pattern:")
    print("   • Detecção automática de falhas")
    print("   • Falha rápida para evitar cascata")
    print("   • Recuperação automática")
    
    print("\n🔷 Retry Pattern:")
    print("   • Backoff exponencial com jitter")
    print("   • Configuração de tentativas máximas")
    print("   • Diferentes estratégias por tipo de erro")
    
    print("\n🔷 Publish-Subscribe Pattern:")
    print("   • Comunicação desacoplada via eventos")
    print("   • Múltiplos subscribers por evento")
    print("   • Processamento assíncrono")
    
    print("\n🔷 Bulkhead Pattern:")
    print("   • Isolamento de pools de recursos")
    print("   • Prevenção de efeito dominó")
    print("   • Monitoramento de utilização")
    
    print("\n🔷 Características do Sistema:")
    print("   • Alta disponibilidade")
    print("   • Resiliência a falhas")
    print("   • Escalabilidade horizontal")
    print("   • Observabilidade completa")
    print("   • Recuperação automática")
    
    # Cleanup
    print("\n🧹 Finalizando recursos...")
    event_bus.shutdown()
    
    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrar_sistema_monitoramento()
