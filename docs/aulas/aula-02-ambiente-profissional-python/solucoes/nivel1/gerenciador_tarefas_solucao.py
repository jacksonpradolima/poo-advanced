"""
Gerenciador de Tarefas - Aplicação de Linha de Comando

Demonstra aplicação prática dos conceitos do ambiente profissional:
- Configuração de projeto com pyproject.toml
- Uso de type hints e validação com mypy
- Formatação automática com ruff
- Documentação com docstrings
- Testes unitários com pytest

Funcionalidades:
- Adicionar, listar, marcar como concluída e remover tarefas
- Persistência em arquivo JSON
- Interface de linha de comando intuitiva
- Tratamento robusto de erros

Execução: python gerenciador_tarefas_solucao.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Tarefa:
    """
    Representa uma tarefa no sistema de gerenciamento.
    
    Attributes:
        id: Identificador único da tarefa
        titulo: Título descritivo da tarefa
        descricao: Descrição detalhada (opcional)
        concluida: Status de conclusão
        data_criacao: Timestamp de criação
        data_conclusao: Timestamp de conclusão (None se não concluída)
    """
    id: int
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False
    data_criacao: str = ""
    data_conclusao: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa data_criacao se não fornecida."""
        if not self.data_criacao:
            self.data_criacao = datetime.now().isoformat()


class GerenciadorTarefas:
    """
    Sistema de gerenciamento de tarefas com persistência em arquivo.
    
    Responsável por manter uma lista de tarefas, permitindo operações
    CRUD (Create, Read, Update, Delete) e persistindo os dados em JSON.
    """
    
    def __init__(self, arquivo_dados: str = "tarefas.json") -> None:
        """
        Inicializa o gerenciador com arquivo de persistência.
        
        Args:
            arquivo_dados: Caminho para arquivo JSON de armazenamento
        """
        self.arquivo_dados = Path(arquivo_dados)
        self.tarefas: List[Tarefa] = []
        self._proximo_id = 1
        self._carregar_tarefas()
    
    def _carregar_tarefas(self) -> None:
        """
        Carrega tarefas do arquivo JSON.
        
        Cria arquivo vazio se não existir. Trata erros de formato
        e corrupção de dados de forma elegante.
        """
        try:
            if self.arquivo_dados.exists():
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    
                # Converte dicionários de volta para objetos Tarefa
                self.tarefas = [
                    Tarefa(**tarefa_dict) 
                    for tarefa_dict in dados.get('tarefas', [])
                ]
                
                # Atualiza contador de ID
                if self.tarefas:
                    self._proximo_id = max(t.id for t in self.tarefas) + 1
                else:
                    self._proximo_id = 1
                    
                print(f"✅ Carregadas {len(self.tarefas)} tarefas de {self.arquivo_dados}")
            else:
                print(f"📁 Arquivo {self.arquivo_dados} não existe. Criando novo...")
                self._salvar_tarefas()
                
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"⚠️  Erro ao carregar tarefas: {e}")
            print("Criando arquivo de backup e iniciando com lista vazia...")
            
            # Backup do arquivo corrompido
            if self.arquivo_dados.exists():
                backup_path = self.arquivo_dados.with_suffix('.backup')
                self.arquivo_dados.rename(backup_path)
                print(f"Backup salvo em: {backup_path}")
            
            self.tarefas = []
            self._proximo_id = 1
    
    def _salvar_tarefas(self) -> None:
        """
        Salva tarefas no arquivo JSON.
        
        Raises:
            OSError: Se não conseguir escrever no arquivo
        """
        try:
            dados = {
                'tarefas': [asdict(tarefa) for tarefa in self.tarefas],
                'metadata': {
                    'total_tarefas': len(self.tarefas),
                    'ultima_atualizacao': datetime.now().isoformat(),
                    'versao': '1.0'
                }
            }
            
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
                
        except OSError as e:
            print(f"❌ Erro ao salvar tarefas: {e}")
            raise
    
    def adicionar_tarefa(self, titulo: str, descricao: Optional[str] = None) -> Tarefa:
        """
        Adiciona nova tarefa ao sistema.
        
        Args:
            titulo: Título da tarefa (obrigatório)
            descricao: Descrição opcional da tarefa
            
        Returns:
            Tarefa criada
            
        Raises:
            ValueError: Se título estiver vazio
        """
        if not titulo or not titulo.strip():
            raise ValueError("Título da tarefa não pode estar vazio")
        
        tarefa = Tarefa(
            id=self._proximo_id,
            titulo=titulo.strip(),
            descricao=descricao.strip() if descricao else None
        )
        
        self.tarefas.append(tarefa)
        self._proximo_id += 1
        self._salvar_tarefas()
        
        print(f"✅ Tarefa '{tarefa.titulo}' adicionada com ID {tarefa.id}")
        return tarefa
    
    def listar_tarefas(self, apenas_pendentes: bool = False) -> List[Tarefa]:
        """
        Lista tarefas do sistema.
        
        Args:
            apenas_pendentes: Se True, mostra apenas tarefas não concluídas
            
        Returns:
            Lista de tarefas filtradas
        """
        if apenas_pendentes:
            tarefas_filtradas = [t for t in self.tarefas if not t.concluida]
        else:
            tarefas_filtradas = self.tarefas.copy()
        
        return tarefas_filtradas
    
    def buscar_tarefa(self, id_tarefa: int) -> Optional[Tarefa]:
        """
        Busca tarefa pelo ID.
        
        Args:
            id_tarefa: ID da tarefa a buscar
            
        Returns:
            Tarefa encontrada ou None
        """
        for tarefa in self.tarefas:
            if tarefa.id == id_tarefa:
                return tarefa
        return None
    
    def marcar_concluida(self, id_tarefa: int) -> bool:
        """
        Marca tarefa como concluída.
        
        Args:
            id_tarefa: ID da tarefa a marcar
            
        Returns:
            True se tarefa foi marcada, False se não encontrada
        """
        tarefa = self.buscar_tarefa(id_tarefa)
        if not tarefa:
            print(f"❌ Tarefa com ID {id_tarefa} não encontrada")
            return False
        
        if tarefa.concluida:
            print(f"ℹ️  Tarefa '{tarefa.titulo}' já estava concluída")
            return True
        
        tarefa.concluida = True
        tarefa.data_conclusao = datetime.now().isoformat()
        self._salvar_tarefas()
        
        print(f"✅ Tarefa '{tarefa.titulo}' marcada como concluída")
        return True
    
    def remover_tarefa(self, id_tarefa: int) -> bool:
        """
        Remove tarefa do sistema.
        
        Args:
            id_tarefa: ID da tarefa a remover
            
        Returns:
            True se tarefa foi removida, False se não encontrada
        """
        tarefa = self.buscar_tarefa(id_tarefa)
        if not tarefa:
            print(f"❌ Tarefa com ID {id_tarefa} não encontrada")
            return False
        
        self.tarefas.remove(tarefa)
        self._salvar_tarefas()
        
        print(f"🗑️  Tarefa '{tarefa.titulo}' removida")
        return True
    
    def estatisticas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do sistema.
        
        Returns:
            Dicionário com estatísticas das tarefas
        """
        total = len(self.tarefas)
        concluidas = sum(1 for t in self.tarefas if t.concluida)
        pendentes = total - concluidas
        
        return {
            'total': total,
            'concluidas': concluidas,
            'pendentes': pendentes,
            'percentual_conclusao': (concluidas / total * 100) if total > 0 else 0
        }


class InterfaceUsuario:
    """Interface de linha de comando para o gerenciador de tarefas."""
    
    def __init__(self) -> None:
        """Inicializa interface com gerenciador de tarefas."""
        self.gerenciador = GerenciadorTarefas()
    
    def mostrar_menu(self) -> None:
        """Exibe menu principal de opções."""
        print("\n" + "="*50)
        print("🚀 GERENCIADOR DE TAREFAS")
        print("="*50)
        print("1. ➕ Adicionar tarefa")
        print("2. 📋 Listar todas as tarefas")
        print("3. ⏳ Listar tarefas pendentes")
        print("4. ✅ Marcar tarefa como concluída")
        print("5. 🗑️  Remover tarefa")
        print("6. 📊 Estatísticas")
        print("0. 🚪 Sair")
        print("="*50)
    
    def imprimir_tarefa(self, tarefa: Tarefa) -> None:
        """
        Imprime tarefa formatada.
        
        Args:
            tarefa: Tarefa a ser impressa
        """
        status = "✅" if tarefa.concluida else "⏳"
        print(f"\n{status} [{tarefa.id:03d}] {tarefa.titulo}")
        
        if tarefa.descricao:
            print(f"    📝 {tarefa.descricao}")
        
        # Formatação de datas
        data_criacao = datetime.fromisoformat(tarefa.data_criacao)
        print(f"    📅 Criada: {data_criacao.strftime('%d/%m/%Y %H:%M')}")
        
        if tarefa.concluida and tarefa.data_conclusao:
            data_conclusao = datetime.fromisoformat(tarefa.data_conclusao)
            print(f"    🏁 Concluída: {data_conclusao.strftime('%d/%m/%Y %H:%M')}")
    
    def executar_adicionar_tarefa(self) -> None:
        """Executa fluxo de adição de tarefa."""
        print("\n➕ ADICIONAR NOVA TAREFA")
        print("-" * 30)
        
        titulo = input("Título: ").strip()
        if not titulo:
            print("❌ Título não pode estar vazio!")
            return
        
        descricao = input("Descrição (opcional): ").strip()
        descricao = descricao if descricao else None
        
        try:
            self.gerenciador.adicionar_tarefa(titulo, descricao)
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def executar_listar_tarefas(self, apenas_pendentes: bool = False) -> None:
        """
        Executa fluxo de listagem de tarefas.
        
        Args:
            apenas_pendentes: Se True, lista apenas tarefas pendentes
        """
        titulo = "📋 TODAS AS TAREFAS" if not apenas_pendentes else "⏳ TAREFAS PENDENTES"
        print(f"\n{titulo}")
        print("-" * 30)
        
        tarefas = self.gerenciador.listar_tarefas(apenas_pendentes)
        
        if not tarefas:
            msg = "Nenhuma tarefa pendente!" if apenas_pendentes else "Nenhuma tarefa cadastrada!"
            print(f"ℹ️  {msg}")
            return
        
        for tarefa in tarefas:
            self.imprimir_tarefa(tarefa)
    
    def executar_marcar_concluida(self) -> None:
        """Executa fluxo de marcação de tarefa como concluída."""
        print("\n✅ MARCAR TAREFA COMO CONCLUÍDA")
        print("-" * 35)
        
        try:
            id_tarefa = int(input("ID da tarefa: "))
            self.gerenciador.marcar_concluida(id_tarefa)
        except ValueError:
            print("❌ ID deve ser um número!")
    
    def executar_remover_tarefa(self) -> None:
        """Executa fluxo de remoção de tarefa."""
        print("\n🗑️  REMOVER TAREFA")
        print("-" * 20)
        
        try:
            id_tarefa = int(input("ID da tarefa: "))
            
            # Confirmação de segurança
            tarefa = self.gerenciador.buscar_tarefa(id_tarefa)
            if tarefa:
                print(f"\nTarefa a ser removida: '{tarefa.titulo}'")
                confirmacao = input("Confirma remoção? (s/N): ").lower().strip()
                
                if confirmacao in ['s', 'sim', 'y', 'yes']:
                    self.gerenciador.remover_tarefa(id_tarefa)
                else:
                    print("❌ Remoção cancelada")
            
        except ValueError:
            print("❌ ID deve ser um número!")
    
    def executar_estatisticas(self) -> None:
        """Exibe estatísticas do sistema."""
        print("\n📊 ESTATÍSTICAS")
        print("-" * 20)
        
        stats = self.gerenciador.estatisticas()
        
        print(f"📈 Total de tarefas: {stats['total']}")
        print(f"✅ Concluídas: {stats['concluidas']}")
        print(f"⏳ Pendentes: {stats['pendentes']}")
        print(f"📊 Taxa de conclusão: {stats['percentual_conclusao']:.1f}%")
        
        if stats['total'] > 0:
            # Barra de progresso visual
            concluidas = stats['concluidas']
            total = stats['total']
            progresso = int((concluidas / total) * 20)  # 20 caracteres de largura
            
            barra = "█" * progresso + "░" * (20 - progresso)
            print(f"📊 Progresso: [{barra}] {concluidas}/{total}")
    
    def executar(self) -> None:
        """Loop principal da aplicação."""
        print("🚀 Bem-vindo ao Gerenciador de Tarefas!")
        
        while True:
            try:
                self.mostrar_menu()
                opcao = input("\n👉 Escolha uma opção: ").strip()
                
                if opcao == "0":
                    print("\n👋 Até logo!")
                    break
                elif opcao == "1":
                    self.executar_adicionar_tarefa()
                elif opcao == "2":
                    self.executar_listar_tarefas()
                elif opcao == "3":
                    self.executar_listar_tarefas(apenas_pendentes=True)
                elif opcao == "4":
                    self.executar_marcar_concluida()
                elif opcao == "5":
                    self.executar_remover_tarefa()
                elif opcao == "6":
                    self.executar_estatisticas()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                # Pausa para o usuário ver o resultado
                input("\n⏸️  Pressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                print("🔄 Tentando continuar...")


def main() -> None:
    """
    Função principal da aplicação.
    
    Verifica argumentos de linha de comando e inicia interface apropriada.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Gerenciador de Tarefas")
        print("=====================")
        print("Uso: python gerenciador_tarefas_solucao.py")
        print("\nFuncionalidades:")
        print("- Adicionar, listar e gerenciar tarefas")
        print("- Persistência automática em arquivo JSON")
        print("- Interface interativa de linha de comando")
        print("- Estatísticas e relatórios")
        return
    
    # Verificar se arquivo de dados está acessível
    try:
        interface = InterfaceUsuario()
        interface.executar()
    except PermissionError:
        print("❌ Erro: Sem permissão para acessar arquivo de dados")
        print("Verifique as permissões do diretório atual")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        print("Entre em contato com o suporte técnico")


if __name__ == "__main__":
    main()
