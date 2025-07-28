"""
Soluções dos Exercícios - Nível 1 (Básico)
==========================================

Este módulo contém as soluções completas e comentadas para os exercícios
básicos da Aula 2 - Ambiente Profissional de Projetos Python.

Módulos Disponíveis:
-------------------
- calculadora_impostos_solucao: Sistema de cálculo de impostos brasileiros
- gerenciador_tarefas_solucao: Aplicação de gerenciamento de tarefas

Conceitos Demonstrados:
----------------------
- Configuração profissional de projeto com pyproject.toml
- Type hints e verificação com mypy
- Formatação automática com ruff
- Testes unitários com pytest
- Documentação com docstrings
- Precisão decimal para cálculos financeiros
- Persistência de dados em JSON
- Tratamento robusto de erros
- Interface de linha de comando intuitiva

Exemplos de Uso:
--------------
>>> from calculadora_impostos_solucao import total_impostos
>>> resultado = total_impostos(valor_venda=1000, valor_servico=500)
>>> print(f"Total de impostos: R$ {resultado['total']}")

>>> from gerenciador_tarefas_solucao import GerenciadorTarefas
>>> gerenciador = GerenciadorTarefas("tarefas_exemplo.json")
>>> tarefa = gerenciador.adicionar_tarefa("Estudar Python", "Focar em POO")
>>> print(f"Tarefa {tarefa.id} criada: {tarefa.titulo}")

Para Executar os Exemplos:
-------------------------
# Calculadora de impostos
python calculadora_impostos_solucao.py

# Gerenciador de tarefas
python gerenciador_tarefas_solucao.py

# Executar testes
pytest test_*.py -v --cov

# Verificar qualidade do código
make check  # ou ruff check . && mypy .

Autor: Jackson Antonio do Prado Lima
Disciplina: Programação Orientada a Objetos II
Instituição: [Nome da Instituição]
"""

__version__ = "1.0.0"
__author__ = "Jackson Antonio do Prado Lima"
__email__ = "jackson@exemplo.com"

# Importações principais para facilitar o uso
from .calculadora_impostos_solucao import (
    calcular_icms,
    calcular_iss,
    calcular_pis_cofins,
    total_impostos,
    formatar_valor_monetario,
)

from .gerenciador_tarefas_solucao import (
    Tarefa,
    GerenciadorTarefas,
    InterfaceUsuario,
)

__all__ = [
    # Calculadora de impostos
    "calcular_icms",
    "calcular_iss", 
    "calcular_pis_cofins",
    "total_impostos",
    "formatar_valor_monetario",
    # Gerenciador de tarefas
    "Tarefa",
    "GerenciadorTarefas", 
    "InterfaceUsuario",
]
