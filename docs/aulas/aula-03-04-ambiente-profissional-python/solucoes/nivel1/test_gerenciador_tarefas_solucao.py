"""
Testes para o Gerenciador de Tarefas

Demonstra práticas avançadas de teste:
- Uso de fixtures para setup e teardown
- Mocking para isolamento de dependências
- Testes parametrizados para múltiplos cenários
- Testes de integração com arquivo real
- Validação de comportamento em casos extremos

Execução: pytest test_gerenciador_tarefas_solucao.py -v
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, mock_open
from gerenciador_tarefas_solucao import (
    Tarefa, 
    GerenciadorTarefas,
    InterfaceUsuario
)


class TestTarefa:
    """Testes para a classe Tarefa."""
    
    def test_criar_tarefa_basica(self):
        """Testa criação de tarefa com dados mínimos."""
        tarefa = Tarefa(id=1, titulo="Estudar Python")
        
        assert tarefa.id == 1
        assert tarefa.titulo == "Estudar Python"
        assert tarefa.descricao is None
        assert tarefa.concluida is False
        assert tarefa.data_conclusao is None
        assert tarefa.data_criacao  # Deve ser preenchida automaticamente
    
    def test_criar_tarefa_completa(self):
        """Testa criação de tarefa com todos os dados."""
        data_criacao = "2024-01-15T10:30:00"
        tarefa = Tarefa(
            id=1,
            titulo="Estudar Python",
            descricao="Focar em POO e testes",
            concluida=True,
            data_criacao=data_criacao,
            data_conclusao="2024-01-15T15:30:00"
        )
        
        assert tarefa.id == 1
        assert tarefa.titulo == "Estudar Python"
        assert tarefa.descricao == "Focar em POO e testes"
        assert tarefa.concluida is True
        assert tarefa.data_criacao == data_criacao
        assert tarefa.data_conclusao == "2024-01-15T15:30:00"
    
    def test_data_criacao_automatica(self):
        """Testa se data_criacao é preenchida automaticamente."""
        tarefa = Tarefa(id=1, titulo="Teste")
        
        # Verifica se é uma data ISO válida
        datetime.fromisoformat(tarefa.data_criacao)
        assert tarefa.data_criacao


class TestGerenciadorTarefas:
    """Testes para a classe GerenciadorTarefas."""
    
    @pytest.fixture
    def arquivo_temp(self, tmp_path):
        """Fixture que cria arquivo temporário para testes."""
        return tmp_path / "test_tarefas.json"
    
    @pytest.fixture
    def gerenciador(self, arquivo_temp):
        """Fixture que cria gerenciador com arquivo temporário."""
        return GerenciadorTarefas(str(arquivo_temp))
    
    def test_inicializacao_arquivo_inexistente(self, arquivo_temp):
        """Testa inicialização quando arquivo não existe."""
        gerenciador = GerenciadorTarefas(str(arquivo_temp))
        
        assert len(gerenciador.tarefas) == 0
        assert gerenciador._proximo_id == 1
        assert arquivo_temp.exists()  # Arquivo deve ser criado
    
    def test_adicionar_tarefa_basica(self, gerenciador):
        """Testa adição de tarefa básica."""
        tarefa = gerenciador.adicionar_tarefa("Estudar Python")
        
        assert tarefa.id == 1
        assert tarefa.titulo == "Estudar Python"
        assert tarefa.descricao is None
        assert len(gerenciador.tarefas) == 1
    
    def test_adicionar_tarefa_com_descricao(self, gerenciador):
        """Testa adição de tarefa com descrição."""
        tarefa = gerenciador.adicionar_tarefa(
            "Estudar Python",
            "Focar em conceitos de POO"
        )
        
        assert tarefa.titulo == "Estudar Python"
        assert tarefa.descricao == "Focar em conceitos de POO"
    
    def test_adicionar_tarefa_titulo_vazio_levanta_excecao(self, gerenciador):
        """Testa se ValueError é lançada para título vazio."""
        with pytest.raises(ValueError, match="não pode estar vazio"):
            gerenciador.adicionar_tarefa("")
        
        with pytest.raises(ValueError, match="não pode estar vazio"):
            gerenciador.adicionar_tarefa("   ")  # Apenas espaços
    
    def test_ids_sequenciais(self, gerenciador):
        """Testa se IDs são gerados sequencialmente."""
        tarefa1 = gerenciador.adicionar_tarefa("Tarefa 1")
        tarefa2 = gerenciador.adicionar_tarefa("Tarefa 2")
        tarefa3 = gerenciador.adicionar_tarefa("Tarefa 3")
        
        assert tarefa1.id == 1
        assert tarefa2.id == 2
        assert tarefa3.id == 3
    
    def test_listar_tarefas_vazio(self, gerenciador):
        """Testa listagem quando não há tarefas."""
        tarefas = gerenciador.listar_tarefas()
        assert len(tarefas) == 0
    
    def test_listar_todas_tarefas(self, gerenciador):
        """Testa listagem de todas as tarefas."""
        gerenciador.adicionar_tarefa("Tarefa 1")
        gerenciador.adicionar_tarefa("Tarefa 2")
        
        tarefas = gerenciador.listar_tarefas()
        assert len(tarefas) == 2
    
    def test_listar_apenas_pendentes(self, gerenciador):
        """Testa filtro de tarefas pendentes."""
        t1 = gerenciador.adicionar_tarefa("Tarefa 1")
        t2 = gerenciador.adicionar_tarefa("Tarefa 2")
        
        # Marca uma como concluída
        gerenciador.marcar_concluida(t1.id)
        
        pendentes = gerenciador.listar_tarefas(apenas_pendentes=True)
        assert len(pendentes) == 1
        assert pendentes[0].id == t2.id
    
    def test_buscar_tarefa_existente(self, gerenciador):
        """Testa busca de tarefa existente."""
        tarefa_criada = gerenciador.adicionar_tarefa("Teste")
        tarefa_encontrada = gerenciador.buscar_tarefa(tarefa_criada.id)
        
        assert tarefa_encontrada is not None
        assert tarefa_encontrada.id == tarefa_criada.id
        assert tarefa_encontrada.titulo == "Teste"
    
    def test_buscar_tarefa_inexistente(self, gerenciador):
        """Testa busca de tarefa inexistente."""
        tarefa = gerenciador.buscar_tarefa(999)
        assert tarefa is None
    
    def test_marcar_concluida_sucesso(self, gerenciador):
        """Testa marcação de tarefa como concluída."""
        tarefa = gerenciador.adicionar_tarefa("Teste")
        resultado = gerenciador.marcar_concluida(tarefa.id)
        
        assert resultado is True
        assert tarefa.concluida is True
        assert tarefa.data_conclusao is not None
        
        # Verifica se data de conclusão é válida
        datetime.fromisoformat(tarefa.data_conclusao)
    
    def test_marcar_concluida_tarefa_inexistente(self, gerenciador):
        """Testa marcação de tarefa inexistente."""
        resultado = gerenciador.marcar_concluida(999)
        assert resultado is False
    
    def test_marcar_concluida_tarefa_ja_concluida(self, gerenciador):
        """Testa marcação de tarefa já concluída."""
        tarefa = gerenciador.adicionar_tarefa("Teste")
        gerenciador.marcar_concluida(tarefa.id)  # Primeira marcação
        
        resultado = gerenciador.marcar_concluida(tarefa.id)  # Segunda marcação
        assert resultado is True  # Deve retornar True mesmo já estando concluída
    
    def test_remover_tarefa_sucesso(self, gerenciador):
        """Testa remoção de tarefa existente."""
        tarefa = gerenciador.adicionar_tarefa("Teste")
        resultado = gerenciador.remover_tarefa(tarefa.id)
        
        assert resultado is True
        assert len(gerenciador.tarefas) == 0
        assert gerenciador.buscar_tarefa(tarefa.id) is None
    
    def test_remover_tarefa_inexistente(self, gerenciador):
        """Testa remoção de tarefa inexistente."""
        resultado = gerenciador.remover_tarefa(999)
        assert resultado is False
    
    def test_estatisticas_lista_vazia(self, gerenciador):
        """Testa estatísticas com lista vazia."""
        stats = gerenciador.estatisticas()
        
        assert stats['total'] == 0
        assert stats['concluidas'] == 0
        assert stats['pendentes'] == 0
        assert stats['percentual_conclusao'] == 0
    
    def test_estatisticas_com_tarefas(self, gerenciador):
        """Testa estatísticas com tarefas variadas."""
        t1 = gerenciador.adicionar_tarefa("Tarefa 1")
        t2 = gerenciador.adicionar_tarefa("Tarefa 2")
        t3 = gerenciador.adicionar_tarefa("Tarefa 3")
        t4 = gerenciador.adicionar_tarefa("Tarefa 4")
        
        # Marca duas como concluídas
        gerenciador.marcar_concluida(t1.id)
        gerenciador.marcar_concluida(t3.id)
        
        stats = gerenciador.estatisticas()
        
        assert stats['total'] == 4
        assert stats['concluidas'] == 2
        assert stats['pendentes'] == 2
        assert stats['percentual_conclusao'] == 50.0


class TestPersistencia:
    """Testes para funcionalidades de persistência."""
    
    @pytest.fixture
    def arquivo_temp(self, tmp_path):
        """Fixture que cria arquivo temporário para testes."""
        return tmp_path / "test_persistencia.json"
    
    def test_salvar_e_carregar_tarefas(self, arquivo_temp):
        """Testa ciclo completo de salvar e carregar."""
        # Cria gerenciador e adiciona tarefas
        gerenciador1 = GerenciadorTarefas(str(arquivo_temp))
        t1 = gerenciador1.adicionar_tarefa("Tarefa 1", "Descrição 1")
        t2 = gerenciador1.adicionar_tarefa("Tarefa 2")
        gerenciador1.marcar_concluida(t1.id)
        
        # Cria novo gerenciador (simula reinício do programa)
        gerenciador2 = GerenciadorTarefas(str(arquivo_temp))
        
        # Verifica se dados foram carregados corretamente
        assert len(gerenciador2.tarefas) == 2
        assert gerenciador2._proximo_id == 3  # Próximo ID após os existentes
        
        tarefa_carregada = gerenciador2.buscar_tarefa(t1.id)
        assert tarefa_carregada.titulo == "Tarefa 1"
        assert tarefa_carregada.descricao == "Descrição 1"
        assert tarefa_carregada.concluida is True
    
    def test_arquivo_json_corrompido(self, arquivo_temp):
        """Testa comportamento com arquivo JSON corrompido."""
        # Cria arquivo com JSON inválido
        arquivo_temp.write_text("{ json inválido }")
        
        # Deve lidar com erro graciosamente
        gerenciador = GerenciadorTarefas(str(arquivo_temp))
        assert len(gerenciador.tarefas) == 0
        assert gerenciador._proximo_id == 1
        
        # Verifica se backup foi criado
        backup_path = arquivo_temp.with_suffix('.backup')
        assert backup_path.exists()
    
    def test_arquivo_com_estrutura_incorreta(self, arquivo_temp):
        """Testa arquivo com estrutura JSON incorreta."""
        # JSON válido mas estrutura incorreta
        dados_incorretos = {"dados": "incorretos"}
        arquivo_temp.write_text(json.dumps(dados_incorretos))
        
        gerenciador = GerenciadorTarefas(str(arquivo_temp))
        assert len(gerenciador.tarefas) == 0
    
    @patch("builtins.open", side_effect=OSError("Erro de permissão"))
    def test_erro_ao_salvar(self, mock_open, arquivo_temp):
        """Testa comportamento quando não consegue salvar."""
        gerenciador = GerenciadorTarefas(str(arquivo_temp))
        
        with pytest.raises(OSError):
            gerenciador.adicionar_tarefa("Teste")


class TestInterfaceUsuario:
    """Testes para a interface de usuário."""
    
    @pytest.fixture
    def interface(self, tmp_path):
        """Fixture que cria interface com gerenciador temporário."""
        arquivo_temp = tmp_path / "test_interface.json"
        interface = InterfaceUsuario()
        interface.gerenciador = GerenciadorTarefas(str(arquivo_temp))
        return interface
    
    def test_imprimir_tarefa_basica(self, interface, capsys):
        """Testa impressão de tarefa básica."""
        tarefa = Tarefa(
            id=1,
            titulo="Estudar Python",
            data_criacao="2024-01-15T10:30:00"
        )
        
        interface.imprimir_tarefa(tarefa)
        captured = capsys.readouterr()
        
        assert "⏳ [001] Estudar Python" in captured.out
        assert "15/01/2024 10:30" in captured.out
    
    def test_imprimir_tarefa_concluida(self, interface, capsys):
        """Testa impressão de tarefa concluída."""
        tarefa = Tarefa(
            id=2,
            titulo="Tarefa Concluída",
            descricao="Descrição da tarefa",
            concluida=True,
            data_criacao="2024-01-15T10:30:00",
            data_conclusao="2024-01-15T15:30:00"
        )
        
        interface.imprimir_tarefa(tarefa)
        captured = capsys.readouterr()
        
        assert "✅ [002] Tarefa Concluída" in captured.out
        assert "📝 Descrição da tarefa" in captured.out
        assert "🏁 Concluída: 15/01/2024 15:30" in captured.out


class TestCenarioCompleto:
    """Testes de cenário completo e integração."""
    
    def test_fluxo_completo_usuario(self, tmp_path):
        """Testa fluxo completo de uso da aplicação."""
        arquivo_temp = tmp_path / "test_completo.json"
        gerenciador = GerenciadorTarefas(str(arquivo_temp))
        
        # 1. Adiciona várias tarefas
        t1 = gerenciador.adicionar_tarefa("Estudar Python", "Focar em POO")
        t2 = gerenciador.adicionar_tarefa("Fazer exercícios")
        t3 = gerenciador.adicionar_tarefa("Ler documentação")
        
        # 2. Verifica estado inicial
        stats = gerenciador.estatisticas()
        assert stats['total'] == 3
        assert stats['pendentes'] == 3
        
        # 3. Marca algumas como concluídas
        gerenciador.marcar_concluida(t1.id)
        gerenciador.marcar_concluida(t3.id)
        
        # 4. Verifica progresso
        stats = gerenciador.estatisticas()
        assert stats['concluidas'] == 2
        assert stats['pendentes'] == 1
        assert abs(stats['percentual_conclusao'] - 66.67) < 0.01
        
        # 5. Lista apenas pendentes
        pendentes = gerenciador.listar_tarefas(apenas_pendentes=True)
        assert len(pendentes) == 1
        assert pendentes[0].id == t2.id
        
        # 6. Remove uma tarefa
        gerenciador.remover_tarefa(t2.id)
        
        # 7. Verifica estado final
        stats = gerenciador.estatisticas()
        assert stats['total'] == 2
        assert stats['concluidas'] == 2
        assert stats['pendentes'] == 0
        assert stats['percentual_conclusao'] == 100.0
    
    def test_persistencia_entre_sessoes(self, tmp_path):
        """Testa persistência de dados entre diferentes sessões."""
        arquivo_temp = tmp_path / "test_sessoes.json"
        
        # Sessão 1: Cria dados
        gerenciador1 = GerenciadorTarefas(str(arquivo_temp))
        t1 = gerenciador1.adicionar_tarefa("Tarefa Persistente")
        gerenciador1.marcar_concluida(t1.id)
        original_id = t1.id
        
        # Sessão 2: Carrega dados e adiciona mais
        gerenciador2 = GerenciadorTarefas(str(arquivo_temp))
        t2 = gerenciador2.adicionar_tarefa("Nova Tarefa")
        
        # Verificações
        assert len(gerenciador2.tarefas) == 2
        assert gerenciador2.buscar_tarefa(original_id).concluida is True
        assert t2.id == original_id + 1  # ID sequencial mantido
        
        # Sessão 3: Verifica tudo ainda está lá
        gerenciador3 = GerenciadorTarefas(str(arquivo_temp))
        assert len(gerenciador3.tarefas) == 2
        
        stats = gerenciador3.estatisticas()
        assert stats['total'] == 2
        assert stats['concluidas'] == 1
        assert stats['pendentes'] == 1
