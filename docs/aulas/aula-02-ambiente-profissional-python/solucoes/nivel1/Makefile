# Makefile para Ambiente Profissional Python
# ==========================================
#
# Este Makefile demonstra como criar comandos úteis para desenvolvimento,
# testing, qualidade de código e deployment. É uma excelente prática para
# padronizar operações comuns em projetos Python profissionais.
#
# Uso: make <comando>
# Exemplo: make test, make lint, make setup

# ================================
# CONFIGURAÇÕES GLOBAIS
# ================================

# Definir shell padrão (importante para compatibilidade)
SHELL := /bin/bash

# Variáveis do projeto
PROJECT_NAME := aula-02-ambiente-profissional
PYTHON_VERSION := 3.12
VENV_NAME := .venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip
PYTEST := $(VENV_NAME)/bin/pytest
MYPY := $(VENV_NAME)/bin/mypy
RUFF := $(VENV_NAME)/bin/ruff

# Cores para output (tornar comandos mais legíveis)
RESET := \033[0m
BOLD := \033[1m
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
MAGENTA := \033[35m
CYAN := \033[36m

# ================================
# COMANDOS PRINCIPAIS
# ================================

.PHONY: help
help: ## 📚 Mostrar ajuda com todos os comandos disponíveis
	@echo "$(BOLD)$(BLUE)🚀 $(PROJECT_NAME) - Comandos Disponíveis$(RESET)"
	@echo "$(YELLOW)═══════════════════════════════════════════════════$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)Exemplos de uso:$(RESET)"
	@echo "  $(GREEN)make setup$(RESET)     - Configura ambiente completo"
	@echo "  $(GREEN)make test$(RESET)      - Executa todos os testes"
	@echo "  $(GREEN)make check$(RESET)     - Verifica qualidade do código"
	@echo "  $(GREEN)make clean$(RESET)     - Limpa arquivos temporários"

# ================================
# SETUP E CONFIGURAÇÃO
# ================================

.PHONY: setup
setup: ## 🔧 Configurar ambiente completo de desenvolvimento
	@echo "$(BOLD)$(BLUE)🔧 Configurando ambiente de desenvolvimento...$(RESET)"
	@$(MAKE) venv
	@$(MAKE) install-deps
	@$(MAKE) install-hooks
	@echo "$(BOLD)$(GREEN)✅ Ambiente configurado com sucesso!$(RESET)"
	@echo ""
	@echo "$(YELLOW)Próximos passos:$(RESET)"
	@echo "  1. Ative o ambiente virtual: $(CYAN)source $(VENV_NAME)/bin/activate$(RESET)"
	@echo "  2. Execute os testes: $(CYAN)make test$(RESET)"
	@echo "  3. Verifique a qualidade: $(CYAN)make check$(RESET)"

.PHONY: venv
venv: ## 🐍 Criar ambiente virtual
	@echo "$(BOLD)$(BLUE)🐍 Criando ambiente virtual...$(RESET)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		python$(PYTHON_VERSION) -m venv $(VENV_NAME); \
		echo "$(GREEN)✅ Ambiente virtual criado em $(VENV_NAME)$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Ambiente virtual já existe$(RESET)"; \
	fi

.PHONY: install-deps
install-deps: venv ## 📦 Instalar dependências do projeto
	@echo "$(BOLD)$(BLUE)📦 Instalando dependências...$(RESET)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -e ".[dev,docs,quality,testing]"
	@echo "$(GREEN)✅ Dependências instaladas$(RESET)"

.PHONY: install-hooks
install-hooks: venv ## 🎣 Instalar pre-commit hooks
	@echo "$(BOLD)$(BLUE)🎣 Instalando pre-commit hooks...$(RESET)"
	@$(VENV_NAME)/bin/pre-commit install
	@$(VENV_NAME)/bin/pre-commit install --hook-type commit-msg
	@echo "$(GREEN)✅ Pre-commit hooks instalados$(RESET)"

# ================================
# TESTES E QUALIDADE
# ================================

.PHONY: test
test: ## 🧪 Executar todos os testes
	@echo "$(BOLD)$(BLUE)🧪 Executando testes...$(RESET)"
	@$(PYTEST) -v --cov=solucoes --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Testes concluídos$(RESET)"

.PHONY: test-fast
test-fast: ## ⚡ Executar testes rápidos (apenas falhas anteriores)
	@echo "$(BOLD)$(BLUE)⚡ Executando testes rápidos...$(RESET)"
	@$(PYTEST) -x --lf -q

.PHONY: test-unit
test-unit: ## 🔬 Executar apenas testes unitários
	@echo "$(BOLD)$(BLUE)🔬 Executando testes unitários...$(RESET)"
	@$(PYTEST) -m "not integration" -v

.PHONY: test-integration
test-integration: ## 🔗 Executar apenas testes de integração
	@echo "$(BOLD)$(BLUE)🔗 Executando testes de integração...$(RESET)"
	@$(PYTEST) -m "integration" -v

.PHONY: benchmark
benchmark: ## 📊 Executar testes de performance
	@echo "$(BOLD)$(BLUE)📊 Executando benchmarks...$(RESET)"
	@$(PYTEST) --benchmark-only --benchmark-sort=mean

.PHONY: coverage
coverage: ## 📈 Gerar relatório de cobertura detalhado
	@echo "$(BOLD)$(BLUE)📈 Gerando relatório de cobertura...$(RESET)"
	@$(PYTEST) --cov=solucoes --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✅ Relatório gerado em htmlcov/index.html$(RESET)"

# ================================
# QUALIDADE DE CÓDIGO
# ================================

.PHONY: lint
lint: ## 🔍 Verificar qualidade do código com ruff
	@echo "$(BOLD)$(BLUE)🔍 Verificando qualidade do código...$(RESET)"
	@$(RUFF) check .

.PHONY: format
format: ## 🎨 Formatar código automaticamente
	@echo "$(BOLD)$(BLUE)🎨 Formatando código...$(RESET)"
	@$(RUFF) format .
	@echo "$(GREEN)✅ Código formatado$(RESET)"

.PHONY: format-check
format-check: ## ✅ Verificar se código está formatado
	@echo "$(BOLD)$(BLUE)✅ Verificando formatação...$(RESET)"
	@$(RUFF) format --check .

.PHONY: typecheck
typecheck: ## 🔍 Verificar tipos com mypy
	@echo "$(BOLD)$(BLUE)🔍 Verificando tipos...$(RESET)"
	@$(MYPY) solucoes

.PHONY: security
security: ## 🔐 Verificar problemas de segurança
	@echo "$(BOLD)$(BLUE)🔐 Verificando segurança...$(RESET)"
	@$(VENV_NAME)/bin/bandit -r solucoes -f json | jq -r '.results[] | "⚠️  \(.filename):\(.line_number) - \(.issue_text)"' || echo "$(GREEN)✅ Nenhum problema de segurança encontrado$(RESET)"

.PHONY: deps-check
deps-check: ## 🛡️ Verificar vulnerabilidades em dependências
	@echo "$(BOLD)$(BLUE)🛡️ Verificando dependências...$(RESET)"
	@$(VENV_NAME)/bin/safety check

.PHONY: check
check: lint format-check typecheck security test ## 🚀 Executar verificação completa
	@echo "$(BOLD)$(GREEN)🚀 Verificação completa concluída com sucesso!$(RESET)"

# ================================
# DOCUMENTAÇÃO
# ================================

.PHONY: docs
docs: ## 📚 Gerar documentação
	@echo "$(BOLD)$(BLUE)📚 Gerando documentação...$(RESET)"
	@$(VENV_NAME)/bin/pdoc --html --output-dir docs/ solucoes
	@echo "$(GREEN)✅ Documentação gerada em docs/$(RESET)"

.PHONY: docs-serve
docs-serve: ## 🌐 Servir documentação localmente
	@echo "$(BOLD)$(BLUE)🌐 Servindo documentação em http://localhost:8080$(RESET)"
	@$(VENV_NAME)/bin/pdoc --http localhost:8080 solucoes

# ================================
# EXECUÇÃO DE APLICAÇÕES
# ================================

.PHONY: run-calc
run-calc: ## 🧮 Executar calculadora de impostos
	@echo "$(BOLD)$(BLUE)🧮 Executando calculadora de impostos...$(RESET)"
	@$(PYTHON) solucoes/nivel1/calculadora_impostos_solucao.py

.PHONY: run-tasks
run-tasks: ## 📋 Executar gerenciador de tarefas
	@echo "$(BOLD)$(BLUE)📋 Executando gerenciador de tarefas...$(RESET)"
	@$(PYTHON) solucoes/nivel1/gerenciador_tarefas_solucao.py

.PHONY: demo
demo: ## 🎭 Executar demonstração de todas as funcionalidades
	@echo "$(BOLD)$(BLUE)🎭 Demonstração das aplicações$(RESET)"
	@echo ""
	@echo "$(YELLOW)1. Calculadora de Impostos:$(RESET)"
	@echo "   $(CYAN)make run-calc$(RESET)"
	@echo ""
	@echo "$(YELLOW)2. Gerenciador de Tarefas:$(RESET)"
	@echo "   $(CYAN)make run-tasks$(RESET)"
	@echo ""
	@echo "$(YELLOW)3. Testes Automatizados:$(RESET)"
	@echo "   $(CYAN)make test$(RESET)"

# ================================
# LIMPEZA E MANUTENÇÃO
# ================================

.PHONY: clean
clean: ## 🧹 Limpar arquivos temporários
	@echo "$(BOLD)$(BLUE)🧹 Limpando arquivos temporários...$(RESET)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache htmlcov .coverage dist build
	@echo "$(GREEN)✅ Limpeza concluída$(RESET)"

.PHONY: clean-venv
clean-venv: ## 🗑️ Remover ambiente virtual
	@echo "$(BOLD)$(BLUE)🗑️ Removendo ambiente virtual...$(RESET)"
	@rm -rf $(VENV_NAME)
	@echo "$(GREEN)✅ Ambiente virtual removido$(RESET)"

.PHONY: reset
reset: clean clean-venv ## 🔄 Reset completo do projeto
	@echo "$(BOLD)$(BLUE)🔄 Reset completo do projeto...$(RESET)"
	@echo "$(GREEN)✅ Projeto resetado$(RESET)"
	@echo "$(YELLOW)Execute 'make setup' para reconfigurar$(RESET)"

# ================================
# DESENVOLVIMENTO E DEBUGGING
# ================================

.PHONY: shell
shell: ## 🐚 Abrir shell Python interativo
	@echo "$(BOLD)$(BLUE)🐚 Abrindo shell Python...$(RESET)"
	@$(PYTHON) -i -c "
import sys
print('🐍 Python', sys.version)
print('📁 Projeto: $(PROJECT_NAME)')
print('💡 Dica: Import suas classes e teste interativamente!')
print()

# Imports úteis
from solucoes.nivel1.calculadora_impostos_solucao import *
from solucoes.nivel1.gerenciador_tarefas_solucao import *
"

.PHONY: notebook
notebook: ## 📓 Abrir Jupyter Lab
	@echo "$(BOLD)$(BLUE)📓 Abrindo Jupyter Lab...$(RESET)"
	@$(VENV_NAME)/bin/jupyter lab

.PHONY: debug
debug: ## 🐛 Executar testes em modo debug
	@echo "$(BOLD)$(BLUE)🐛 Executando testes em modo debug...$(RESET)"
	@$(PYTEST) -v -s --pdb --pdbcls=IPython.terminal.debugger:Pdb

# ================================
# CI/CD E DEPLOYMENT
# ================================

.PHONY: ci-check
ci-check: ## 🤖 Verificação completa para CI/CD
	@echo "$(BOLD)$(BLUE)🤖 Executando verificação CI/CD...$(RESET)"
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) typecheck
	@$(MAKE) security
	@$(MAKE) deps-check
	@$(MAKE) test
	@echo "$(BOLD)$(GREEN)✅ Verificação CI/CD passou!$(RESET)"

.PHONY: build
build: ## 📦 Construir pacote para distribuição
	@echo "$(BOLD)$(BLUE)📦 Construindo pacote...$(RESET)"
	@$(PYTHON) -m build
	@echo "$(GREEN)✅ Pacote construído em dist/$(RESET)"

.PHONY: release-check
release-check: ## 🚀 Verificar se está pronto para release
	@echo "$(BOLD)$(BLUE)🚀 Verificando preparação para release...$(RESET)"
	@$(MAKE) ci-check
	@$(MAKE) build
	@echo "$(BOLD)$(GREEN)✅ Pronto para release!$(RESET)"

# ================================
# INFORMAÇÕES E STATUS
# ================================

.PHONY: status
status: ## 📊 Mostrar status do projeto
	@echo "$(BOLD)$(BLUE)📊 Status do Projeto$(RESET)"
	@echo "$(YELLOW)═══════════════════════════════════════$(RESET)"
	@echo "$(CYAN)Projeto:$(RESET) $(PROJECT_NAME)"
	@echo "$(CYAN)Python:$(RESET) $(PYTHON_VERSION)"
	@echo "$(CYAN)Ambiente Virtual:$(RESET) $(if $(wildcard $(VENV_NAME)),$(GREEN)✅ Ativo$(RESET),$(RED)❌ Não encontrado$(RESET))"
	@echo ""
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "$(CYAN)Dependências instaladas:$(RESET)"; \
		$(PIP) list --format=columns | head -10; \
		echo "..."; \
		echo ""; \
		echo "$(CYAN)Última execução de testes:$(RESET)"; \
		if [ -f ".coverage" ]; then \
			echo "$(GREEN)✅ Cobertura disponível$(RESET)"; \
		else \
			echo "$(YELLOW)⚠️  Execute 'make test' para gerar cobertura$(RESET)"; \
		fi; \
	fi

.PHONY: info
info: ## ℹ️ Informações detalhadas do ambiente
	@echo "$(BOLD)$(BLUE)ℹ️  Informações do Ambiente$(RESET)"
	@echo "$(YELLOW)═══════════════════════════════════════$(RESET)"
	@echo "$(CYAN)Sistema Operacional:$(RESET) $$(uname -s) $$(uname -r)"
	@echo "$(CYAN)Arquitetura:$(RESET) $$(uname -m)"
	@echo "$(CYAN)Python do sistema:$(RESET) $$(python3 --version)"
	@echo "$(CYAN)Pip do sistema:$(RESET) $$(pip3 --version)"
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "$(CYAN)Python do venv:$(RESET) $$($$(PYTHON) --version)"; \
		echo "$(CYAN)Pip do venv:$(RESET) $$($$(PIP) --version)"; \
	fi
	@echo "$(CYAN)Diretório atual:$(RESET) $$(pwd)"
	@echo "$(CYAN)Tamanho do projeto:$(RESET) $$(du -sh . | cut -f1)"

# ================================
# COMANDOS ESPECIAIS
# ================================

.PHONY: install-uv
install-uv: ## ⚡ Instalar UV (gerenciador de pacotes rápido)
	@echo "$(BOLD)$(BLUE)⚡ Instalando UV...$(RESET)"
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "$(GREEN)✅ UV instalado$(RESET)"
	@echo "$(YELLOW)Dica: Use 'uv venv' e 'uv pip install' para velocidade máxima$(RESET)"

.PHONY: profile
profile: ## 📊 Analisar performance do código
	@echo "$(BOLD)$(BLUE)📊 Analisando performance...$(RESET)"
	@$(PYTHON) -m cProfile -o profile.stats solucoes/nivel1/calculadora_impostos_solucao.py
	@$(PYTHON) -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(10)
"
	@echo "$(GREEN)✅ Profile salvo em profile.stats$(RESET)"

# ================================
# HOOKS PRE-COMMIT MANUAIS
# ================================

.PHONY: pre-commit
pre-commit: ## 🎣 Executar todos os hooks do pre-commit manualmente
	@echo "$(BOLD)$(BLUE)🎣 Executando hooks do pre-commit...$(RESET)"
	@$(VENV_NAME)/bin/pre-commit run --all-files

.PHONY: update-hooks
update-hooks: ## 🔄 Atualizar hooks do pre-commit
	@echo "$(BOLD)$(BLUE)🔄 Atualizando hooks...$(RESET)"
	@$(VENV_NAME)/bin/pre-commit autoupdate
	@echo "$(GREEN)✅ Hooks atualizados$(RESET)"

# ================================
# COMANDO PADRÃO
# ================================

# Comando executado quando apenas 'make' é digitado
.DEFAULT_GOAL := help

# Prevenir tratamento de nomes como arquivos
.SUFFIXES:
