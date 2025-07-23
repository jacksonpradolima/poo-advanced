#!/usr/bin/env python3
"""
Demonstração Completa do Ambiente Profissional Python
======================================================

Este script demonstra o uso integrado de todas as ferramentas e conceitos
apresentados na Aula 2, incluindo:

- Configuração de projeto com pyproject.toml
- Type hints e validação com mypy
- Formatação automática com ruff
- Testes unitários com pytest
- Documentação com docstrings
- Precisão decimal para cálculos financeiros
- Tratamento robusto de erros
- Logging profissional

Execute: python demo_completa.py
"""

import logging
import sys
from decimal import Decimal
from pathlib import Path
from typing import Dict, Any

# Configuração de logging profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('demo.log')
    ]
)

logger = logging.getLogger(__name__)

# Importações dos módulos desenvolvidos
from calculadora_impostos_solucao import total_impostos, formatar_valor_monetario
from gerenciador_tarefas_solucao import GerenciadorTarefas, Tarefa


def demonstrar_calculadora() -> None:
    """
    Demonstra o uso da calculadora de impostos com diferentes cenários.
    
    Mostra:
    - Cálculos com diferentes tipos de valores
    - Tratamento de erros
    - Formatação de resultado
    - Logging das operações
    """
    logger.info("🧮 Iniciando demonstração da calculadora de impostos")
    
    # Cenários de teste
    cenarios = [
        {
            "nome": "Empresa de Tecnologia", 
            "vendas": Decimal("50000.00"),
            "servicos": Decimal("30000.00"), 
            "receita": Decimal("80000.00")
        },
        {
            "nome": "Consultoria",
            "vendas": Decimal("0.00"),
            "servicos": Decimal("15000.00"),
            "receita": Decimal("15000.00")
        },
        {
            "nome": "Comércio Eletrônico",
            "vendas": Decimal("120000.00"),
            "servicos": Decimal("5000.00"),
            "receita": Decimal("125000.00")
        }
    ]
    
    print("\n" + "="*60)
    print("🧮 DEMONSTRAÇÃO: CALCULADORA DE IMPOSTOS")
    print("="*60)
    
    for cenario in cenarios:
        logger.info(f"Calculando impostos para: {cenario['nome']}")
        
        try:
            resultado = total_impostos(
                valor_venda=cenario["vendas"],
                valor_servico=cenario["servicos"], 
                valor_receita=cenario["receita"]
            )
            
            print(f"\n📊 {cenario['nome']}")
            print("-" * 40)
            print(f"💰 Vendas: {formatar_valor_monetario(cenario['vendas'])}")
            print(f"🛠️  Serviços: {formatar_valor_monetario(cenario['servicos'])}")
            print(f"💵 Receita Total: {formatar_valor_monetario(cenario['receita'])}")
            print()
            print(f"🏛️  ICMS (18%): {formatar_valor_monetario(resultado['icms'])}")
            print(f"🏢 ISS (5%): {formatar_valor_monetario(resultado['iss'])}")
            print(f"📋 PIS/COFINS (9.25%): {formatar_valor_monetario(resultado['pis_cofins'])}")
            print(f"💸 TOTAL IMPOSTOS: {formatar_valor_monetario(resultado['total'])}")
            
            # Cálculo da carga tributária
            if cenario["receita"] > 0:
                carga = (resultado['total'] / cenario["receita"]) * 100
                print(f"📊 Carga Tributária: {carga:.2f}%")
            
            logger.info(f"Impostos calculados: {resultado['total']}")
            
        except Exception as e:
            logger.error(f"Erro ao calcular impostos: {e}")
            print(f"❌ Erro: {e}")


def demonstrar_gerenciador_tarefas() -> None:
    """
    Demonstra o uso do gerenciador de tarefas com operações completas.
    
    Mostra:
    - Criação e manipulação de tarefas
    - Persistência em arquivo
    - Estatísticas e relatórios
    - Tratamento de erros
    """
    logger.info("📋 Iniciando demonstração do gerenciador de tarefas")
    
    print("\n" + "="*60)
    print("📋 DEMONSTRAÇÃO: GERENCIADOR DE TAREFAS")
    print("="*60)
    
    # Criar gerenciador com arquivo temporário
    arquivo_demo = "tarefas_demo.json"
    gerenciador = GerenciadorTarefas(arquivo_demo)
    
    try:
        # 1. Adicionar tarefas de exemplo
        print("\n1️⃣ Adicionando tarefas de exemplo...")
        
        tarefas_exemplo = [
            ("Configurar ambiente Python", "Instalar UV, configurar pyproject.toml"),
            ("Implementar calculadora", "Criar funções de cálculo de impostos"), 
            ("Escrever testes", "Cobertura de 100% com pytest"),
            ("Configurar pre-commit", "Hooks de qualidade automáticos"),
            ("Documentar projeto", "README e docstrings completos")
        ]
        
        tarefas_criadas = []
        for titulo, descricao in tarefas_exemplo:
            tarefa = gerenciador.adicionar_tarefa(titulo, descricao)
            tarefas_criadas.append(tarefa)
            logger.info(f"Tarefa criada: {tarefa.titulo}")
        
        # 2. Marcar algumas como concluídas
        print("\n2️⃣ Marcando tarefas como concluídas...")
        for i in [0, 2, 4]:  # Primeira, terceira e quinta tarefas
            if i < len(tarefas_criadas):
                gerenciador.marcar_concluida(tarefas_criadas[i].id)
        
        # 3. Exibir estatísticas
        print("\n3️⃣ Estatísticas do projeto:")
        stats = gerenciador.estatisticas()
        
        print(f"📈 Total de tarefas: {stats['total']}")
        print(f"✅ Concluídas: {stats['concluidas']}")
        print(f"⏳ Pendentes: {stats['pendentes']}")
        print(f"📊 Taxa de conclusão: {stats['percentual_conclusao']:.1f}%")
        
        # Barra de progresso visual
        if stats['total'] > 0:
            progresso = int((stats['concluidas'] / stats['total']) * 20)
            barra = "█" * progresso + "░" * (20 - progresso)
            print(f"📊 Progresso: [{barra}] {stats['concluidas']}/{stats['total']}")
        
        # 4. Listar tarefas pendentes
        print("\n4️⃣ Tarefas pendentes:")
        pendentes = gerenciador.listar_tarefas(apenas_pendentes=True)
        
        for tarefa in pendentes:
            print(f"⏳ [{tarefa.id:03d}] {tarefa.titulo}")
            if tarefa.descricao:
                print(f"    📝 {tarefa.descricao}")
        
        # 5. Demonstrar busca
        print("\n5️⃣ Testando busca de tarefa:")
        if tarefas_criadas:
            tarefa_encontrada = gerenciador.buscar_tarefa(tarefas_criadas[0].id)
            if tarefa_encontrada:
                status = "✅ Concluída" if tarefa_encontrada.concluida else "⏳ Pendente"
                print(f"🔍 Tarefa {tarefa_encontrada.id}: {tarefa_encontrada.titulo} - {status}")
        
        logger.info(f"Demonstração concluída. Arquivo salvo em: {arquivo_demo}")
        
    except Exception as e:
        logger.error(f"Erro no gerenciador de tarefas: {e}")
        print(f"❌ Erro: {e}")
    
    finally:
        # Limpeza opcional - remover arquivo de demonstração
        try:
            Path(arquivo_demo).unlink(missing_ok=True)
            logger.info("Arquivo de demonstração removido")
        except Exception:
            pass


def demonstrar_qualidade_codigo() -> None:
    """
    Demonstra as práticas de qualidade de código implementadas.
    
    Mostra:
    - Type hints e validação
    - Tratamento de erros
    - Logging estruturado
    - Documentação
    """
    logger.info("🔍 Demonstrando práticas de qualidade de código")
    
    print("\n" + "="*60)
    print("🔍 DEMONSTRAÇÃO: QUALIDADE DE CÓDIGO")
    print("="*60)
    
    print("\n✅ Práticas implementadas neste projeto:")
    
    qualidades = [
        ("🐍 Type Hints", "Todas as funções têm anotações de tipo"),
        ("📝 Docstrings", "Documentação completa no formato Google/Sphinx"), 
        ("🧪 Testes", "Cobertura de 90%+ com pytest"),
        ("🎨 Formatação", "Código formatado automaticamente com ruff"),
        ("🔍 Linting", "Verificações de qualidade com ruff"),
        ("🔐 Segurança", "Análise de vulnerabilidades com bandit"),
        ("⚡ Performance", "Benchmarks com pytest-benchmark"),
        ("📦 Configuração", "pyproject.toml centralizado"),
        ("🎣 Pre-commit", "Hooks automáticos de qualidade"),
        ("🐳 Containers", "Ambiente reproduzível"),
        ("📊 Cobertura", "Relatórios detalhados de testes"),
        ("🤖 CI/CD", "Integração contínua configurada")
    ]
    
    for emoji_titulo, descricao in qualidades:
        print(f"{emoji_titulo}: {descricao}")
    
    print("\n🚀 Comandos úteis para verificar qualidade:")
    comandos = [
        ("make check", "Verificação completa de qualidade"),
        ("make test", "Executar todos os testes"),
        ("make lint", "Verificar estilo de código"),
        ("make format", "Formatar código automaticamente"),
        ("make typecheck", "Verificar tipos com mypy"),
        ("make security", "Análise de segurança"),
        ("make docs", "Gerar documentação")
    ]
    
    for comando, descricao in comandos:
        print(f"  📝 {comando:<15} - {descricao}")


def demonstrar_ambiente_completo() -> None:
    """
    Executa demonstração completa de todo o ambiente profissional.
    
    Combina todas as demonstrações em um fluxo coeso que mostra
    como os diferentes componentes trabalham juntos.
    """
    logger.info("🚀 Iniciando demonstração completa do ambiente profissional")
    
    print("🚀 AMBIENTE PROFISSIONAL PYTHON - DEMONSTRAÇÃO COMPLETA")
    print("="*70)
    print("📚 Aula 2: Ambiente Profissional de Projetos Python")
    print("👨‍🏫 Professor: Jackson Antonio do Prado Lima")
    print("🎯 Objetivo: Demonstrar ferramentas e práticas profissionais")
    
    try:
        # Executar todas as demonstrações
        demonstrar_calculadora()
        demonstrar_gerenciador_tarefas() 
        demonstrar_qualidade_codigo()
        
        print("\n" + "="*70)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        
        print("\n📋 Próximos passos para o estudante:")
        proximos_passos = [
            "1. Execute os testes: pytest -v --cov",
            "2. Verifique a qualidade: make check",
            "3. Experimente modificar o código",
            "4. Observe como os testes falham/passam",
            "5. Use as ferramentas no seu próprio projeto"
        ]
        
        for passo in proximos_passos:
            print(f"   {passo}")
        
        print("\n💡 Lembre-se: Qualidade de código é uma prática, não um evento!")
        
        logger.info("Demonstração completa finalizada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro na demonstração completa: {e}")
        print(f"\n❌ Erro durante demonstração: {e}")
        print("🔍 Verifique os logs em demo.log para mais detalhes")
        raise


def main() -> None:
    """
    Função principal que executa a demonstração completa.
    
    Trata argumentos de linha de comando e executa demonstrações
    específicas ou completa baseado na entrada do usuário.
    """
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
        
        if demo_type == "calc":
            demonstrar_calculadora()
        elif demo_type == "tasks":
            demonstrar_gerenciador_tarefas()
        elif demo_type == "quality":
            demonstrar_qualidade_codigo()
        elif demo_type == "help":
            print("Uso: python demo_completa.py [calc|tasks|quality|help]")
            print()
            print("Opções:")
            print("  calc    - Demonstrar apenas calculadora de impostos")
            print("  tasks   - Demonstrar apenas gerenciador de tarefas") 
            print("  quality - Demonstrar apenas práticas de qualidade")
            print("  help    - Mostrar esta ajuda")
            print("  (vazio) - Demonstração completa")
        else:
            print(f"❌ Opção inválida: {demo_type}")
            print("Use 'python demo_completa.py help' para ver opções")
            sys.exit(1)
    else:
        # Demonstração completa
        demonstrar_ambiente_completo()


if __name__ == "__main__":
    main()
