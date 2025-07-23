# 🟡 Exercícios Nível 2 - Intermediário

## Exercício 2.1: Sistema de Biblioteca Digital 📚

### Contexto
Desenvolva um sistema de gerenciamento para uma biblioteca digital que permite cadastrar livros, usuários e controlar empréstimos. O sistema deve ser robusto, bem estruturado e seguir princípios de design orientado a objetos.

### Objetivos Pedagógicos
- Integrar múltiplos conceitos de POO
- Implementar relacionamentos entre entidades
- Praticar validações complexas de negócio
- Estruturar projeto com múltiplos módulos

### Requisitos Funcionais

#### Gestão de Livros
1. **Cadastrar livro**: ISBN, título, autor, ano, categoria, exemplares
2. **Buscar livros**: Por título, autor, ISBN ou categoria
3. **Atualizar informações**: Dados do livro e quantidade de exemplares
4. **Listar livros**: Com filtros e ordenação

#### Gestão de Usuários
1. **Cadastrar usuário**: Nome, email, telefone, tipo (estudante/professor)
2. **Validar dados**: Email único, telefone válido
3. **Atualizar perfil**: Informações pessoais
4. **Listar usuários**: Com busca por nome ou email

#### Gestão de Empréstimos
1. **Realizar empréstimo**: Validar disponibilidade e limites
2. **Devolver livro**: Calcular multas por atraso
3. **Renovar empréstimo**: Se não há reservas pendentes
4. **Relatórios**: Empréstimos em aberto, histórico, estatísticas

### Requisitos Técnicos
- Modelos com validação robusta usando Pydantic
- Serviços de negócio para operações complexas
- Persistência simulada em memória com opção para JSON
- Tratamento completo de exceções
- Sistema de logs para auditoria
- Configuração via arquivo TOML

### Estrutura do Projeto
```
biblioteca-digital/
├── pyproject.toml
├── README.md
├── .gitignore
├── .pre-commit-config.yaml
├── config.toml
├── biblioteca/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── livro.py
│   │   ├── usuario.py
│   │   └── emprestimo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── livro_service.py
│   │   ├── usuario_service.py
│   │   └── emprestimo_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── memory_repository.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── formatters.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── livros.json
│   │   └── usuarios.json
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_validators.py
│   └── integration/
│       ├── test_emprestimos.py
│       └── test_sistema_completo.py
└── docs/
    ├── api/
    └── exemplos/
```

### Modelos de Domínio

#### Livro
```python
# biblioteca/models/livro.py
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class CategoriaLivro(str, Enum):
    """Categorias de livros na biblioteca."""
    FICCAO = "ficcao"
    NAO_FICCAO = "nao_ficcao"
    TECNICO = "tecnico"
    ACADEMICO = "academico"
    INFANTIL = "infantil"
    BIOGRAFIA = "biografia"
    HISTORIA = "historia"
    CIENCIA = "ciencia"


class StatusLivro(str, Enum):
    """Status de disponibilidade do livro."""
    DISPONIVEL = "disponivel"
    EMPRESTADO = "emprestado"
    RESERVADO = "reservado"
    MANUTENCAO = "manutencao"
    PERDIDO = "perdido"


class Livro(BaseModel):
    """
    Modelo de domínio para um livro na biblioteca.
    
    Representa um livro com todas as informações necessárias
    para gestão bibliotecária, incluindo controle de exemplares
    e metadados bibliográficos.
    """
    
    id: UUID = Field(default_factory=uuid4)
    isbn: str = Field(min_length=10, max_length=17)
    titulo: str = Field(min_length=1, max_length=500)
    autor: str = Field(min_length=1, max_length=200)
    editora: str = Field(min_length=1, max_length=100)
    ano_publicacao: int = Field(ge=1000, le=datetime.now().year)
    categoria: CategoriaLivro
    total_exemplares: int = Field(ge=1, le=100)
    exemplares_disponiveis: int = Field(ge=0)
    sinopse: Optional[str] = Field(default=None, max_length=2000)
    paginas: Optional[int] = Field(default=None, ge=1)
    idioma: str = Field(default="portugues", max_length=50)
    tags: List[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('isbn')
    @classmethod
    def validar_isbn(cls, v: str) -> str:
        """Valida formato do ISBN."""
        # IMPLEMENTAR: Validação de ISBN-10 ou ISBN-13
        pass
    
    @validator('exemplares_disponiveis')
    @classmethod
    def validar_disponibilidade(cls, v: int, values: dict) -> int:
        """Valida que exemplares disponíveis <= total."""
        # IMPLEMENTAR: Validação de consistência
        pass
    
    def emprestar_exemplar(self) -> bool:
        """
        Empresta um exemplar se disponível.
        
        Returns:
            True se empréstimo foi possível
        """
        # IMPLEMENTAR: Lógica de empréstimo
        pass
    
    def devolver_exemplar(self) -> None:
        """Devolve um exemplar emprestado."""
        # IMPLEMENTAR: Lógica de devolução
        pass
    
    @property
    def disponivel_para_emprestimo(self) -> bool:
        """Verifica se há exemplares disponíveis."""
        return self.exemplares_disponiveis > 0
    
    @property
    def taxa_utilizacao(self) -> float:
        """Calcula percentual de exemplares emprestados."""
        if self.total_exemplares == 0:
            return 0.0
        return (self.total_exemplares - self.exemplares_disponiveis) / self.total_exemplares * 100
```

#### Usuario
```python
# biblioteca/models/usuario.py
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr, validator


class TipoUsuario(str, Enum):
    """Tipos de usuário na biblioteca."""
    ESTUDANTE = "estudante"
    PROFESSOR = "professor"
    FUNCIONARIO = "funcionario"
    VISITANTE = "visitante"


class StatusUsuario(str, Enum):
    """Status do usuário no sistema."""
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    BLOQUEADO = "bloqueado"
    INATIVO = "inativo"


class Usuario(BaseModel):
    """
    Modelo de domínio para usuário da biblioteca.
    
    Representa um usuário com permissões e limites
    específicos baseados no tipo de usuário.
    """
    
    id: UUID = Field(default_factory=uuid4)
    nome: str = Field(min_length=2, max_length=200)
    email: EmailStr
    telefone: str = Field(min_length=10, max_length=20)
    tipo_usuario: TipoUsuario
    status: StatusUsuario = Field(default=StatusUsuario.ATIVO)
    
    # Dados pessoais opcionais
    data_nascimento: Optional[date] = None
    cpf: Optional[str] = Field(default=None, min_length=11, max_length=14)
    endereco: Optional[str] = Field(default=None, max_length=500)
    
    # Metadados do sistema
    data_cadastro: datetime = Field(default_factory=datetime.now)
    ultimo_acesso: Optional[datetime] = None
    
    # Controle de empréstimos
    emprestimos_ativos: int = Field(default=0, ge=0)
    total_emprestimos_realizados: int = Field(default=0, ge=0)
    multas_pendentes: float = Field(default=0.0, ge=0.0)
    
    @validator('telefone')
    @classmethod
    def validar_telefone(cls, v: str) -> str:
        """Valida formato do telefone brasileiro."""
        # IMPLEMENTAR: Validação de telefone
        pass
    
    @validator('cpf')
    @classmethod
    def validar_cpf(cls, v: Optional[str]) -> Optional[str]:
        """Valida CPF se fornecido."""
        if v is None:
            return v
        # IMPLEMENTAR: Validação de CPF
        pass
    
    @property
    def limite_emprestimos(self) -> int:
        """Retorna limite de empréstimos baseado no tipo de usuário."""
        limites = {
            TipoUsuario.ESTUDANTE: 3,
            TipoUsuario.PROFESSOR: 10,
            TipoUsuario.FUNCIONARIO: 5,
            TipoUsuario.VISITANTE: 1,
        }
        return limites[self.tipo_usuario]
    
    @property
    def pode_realizar_emprestimo(self) -> bool:
        """Verifica se usuário pode realizar novo empréstimo."""
        return (
            self.status == StatusUsuario.ATIVO
            and self.emprestimos_ativos < self.limite_emprestimos
            and self.multas_pendentes == 0
        )
    
    def aplicar_multa(self, valor: float) -> None:
        """Aplica multa ao usuário."""
        if valor > 0:
            self.multas_pendentes += valor
    
    def quitar_multa(self, valor: float) -> float:
        """
        Quita multa parcial ou total.
        
        Args:
            valor: Valor a ser quitado
            
        Returns:
            Valor restante da multa
        """
        # IMPLEMENTAR: Lógica de quitação
        pass
```

### Serviços de Negócio

#### Serviço de Empréstimos
```python
# biblioteca/services/emprestimo_service.py
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from ..models.emprestimo import Emprestimo, StatusEmprestimo
from ..models.livro import Livro
from ..models.usuario import Usuario
from ..core.exceptions import (
    EmprestimoError,
    LivroIndisponivelError,
    UsuarioSemPermissaoError,
    LimiteEmprestimosExcedidoError
)
from ..repositories.base import Repository


class EmprestimoService:
    """
    Serviço de negócio para gestão de empréstimos.
    
    Centraliza as regras de negócio relacionadas a empréstimos,
    devoluções, renovações e cálculo de multas.
    """
    
    def __init__(
        self,
        emprestimo_repo: Repository[Emprestimo],
        livro_repo: Repository[Livro],
        usuario_repo: Repository[Usuario],
        config: dict
    ):
        self._emprestimo_repo = emprestimo_repo
        self._livro_repo = livro_repo
        self._usuario_repo = usuario_repo
        self._config = config
    
    def realizar_emprestimo(
        self,
        usuario_id: UUID,
        livro_id: UUID,
        prazo_dias: Optional[int] = None
    ) -> Emprestimo:
        """
        Realiza empréstimo de livro para usuário.
        
        Aplica todas as validações de negócio:
        - Usuário ativo e sem restrições
        - Livro disponível
        - Limite de empréstimos respeitado
        
        Args:
            usuario_id: ID do usuário
            livro_id: ID do livro
            prazo_dias: Prazo em dias (usa padrão se None)
            
        Returns:
            Empréstimo criado
            
        Raises:
            UsuarioSemPermissaoError: Se usuário não pode emprestar
            LivroIndisponivelError: Se livro não está disponível
            LimiteEmprestimosExcedidoError: Se limite foi atingido
        """
        # IMPLEMENTAR: Lógica completa de empréstimo
        # 1. Buscar e validar usuário
        # 2. Buscar e validar livro
        # 3. Verificar regras de negócio
        # 4. Criar empréstimo
        # 5. Atualizar contadores
        pass
    
    def devolver_livro(
        self,
        emprestimo_id: UUID,
        data_devolucao: Optional[datetime] = None
    ) -> Emprestimo:
        """
        Processa devolução de livro.
        
        Calcula multas por atraso e atualiza status.
        
        Args:
            emprestimo_id: ID do empréstimo
            data_devolucao: Data da devolução (now se None)
            
        Returns:
            Empréstimo atualizado
        """
        # IMPLEMENTAR: Lógica de devolução com cálculo de multa
        pass
    
    def renovar_emprestimo(
        self,
        emprestimo_id: UUID,
        dias_adicionais: int = 7
    ) -> Emprestimo:
        """
        Renova empréstimo por período adicional.
        
        Só permite se não há reservas para o livro.
        
        Args:
            emprestimo_id: ID do empréstimo
            dias_adicionais: Dias a adicionar ao prazo
            
        Returns:
            Empréstimo renovado
        """
        # IMPLEMENTAR: Lógica de renovação
        pass
    
    def calcular_multa(self, emprestimo: Emprestimo) -> float:
        """
        Calcula multa por atraso na devolução.
        
        Args:
            emprestimo: Empréstimo a verificar
            
        Returns:
            Valor da multa em reais
        """
        if emprestimo.data_devolucao_prevista >= datetime.now():
            return 0.0
        
        dias_atraso = (datetime.now() - emprestimo.data_devolucao_prevista).days
        valor_multa_diaria = self._config.get('multa_diaria', 1.0)
        multa_maxima = self._config.get('multa_maxima', 50.0)
        
        multa_calculada = dias_atraso * valor_multa_diaria
        return min(multa_calculada, multa_maxima)
    
    def listar_emprestimos_em_aberto(
        self,
        usuario_id: Optional[UUID] = None
    ) -> List[Emprestimo]:
        """
        Lista empréstimos em aberto, opcionalmente filtrados por usuário.
        
        Args:
            usuario_id: ID do usuário (None para todos)
            
        Returns:
            Lista de empréstimos em aberto
        """
        # IMPLEMENTAR: Consulta com filtros
        pass
    
    def gerar_relatorio_atrasos(self) -> dict:
        """
        Gera relatório de empréstimos em atraso.
        
        Returns:
            Dicionário com estatísticas de atraso
        """
        # IMPLEMENTAR: Relatório de atrasos
        pass
```

### Casos de Teste Integrados

```python
# tests/integration/test_sistema_completo.py
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from biblioteca.models.livro import Livro, CategoriaLivro
from biblioteca.models.usuario import Usuario, TipoUsuario
from biblioteca.services.emprestimo_service import EmprestimoService
from biblioteca.repositories.memory_repository import MemoryRepository


class TestSistemaCompleto:
    """Testes de integração do sistema completo."""
    
    @pytest.fixture
    def sistema_biblioteca(self):
        """Configura sistema completo para testes."""
        # Repositórios
        livro_repo = MemoryRepository()
        usuario_repo = MemoryRepository()
        emprestimo_repo = MemoryRepository()
        
        # Configuração
        config = {
            'prazo_padrao_dias': 14,
            'multa_diaria': 2.0,
            'multa_maxima': 100.0
        }
        
        # Serviço
        emprestimo_service = EmprestimoService(
            emprestimo_repo, livro_repo, usuario_repo, config
        )
        
        return {
            'livro_repo': livro_repo,
            'usuario_repo': usuario_repo,
            'emprestimo_service': emprestimo_service
        }
    
    def test_fluxo_completo_emprestimo(self, sistema_biblioteca):
        """Testa fluxo completo: cadastro -> empréstimo -> devolução."""
        # Arrange
        sistema = sistema_biblioteca
        
        # Criar livro
        livro = Livro(
            isbn="978-3-16-148410-0",
            titulo="Python para Iniciantes",
            autor="João Silva",
            editora="TechBooks",
            ano_publicacao=2023,
            categoria=CategoriaLivro.TECNICO,
            total_exemplares=3
        )
        sistema['livro_repo'].save(livro)
        
        # Criar usuário
        usuario = Usuario(
            nome="Maria Santos",
            email="maria@example.com",
            telefone="11999999999",
            tipo_usuario=TipoUsuario.ESTUDANTE
        )
        sistema['usuario_repo'].save(usuario)
        
        # Act & Assert
        # 1. Realizar empréstimo
        emprestimo = sistema['emprestimo_service'].realizar_emprestimo(
            usuario.id, livro.id
        )
        assert emprestimo is not None
        assert emprestimo.usuario_id == usuario.id
        assert emprestimo.livro_id == livro.id
        
        # 2. Verificar atualização de contadores
        livro_atualizado = sistema['livro_repo'].get_by_id(livro.id)
        assert livro_atualizado.exemplares_disponiveis == 2
        
        usuario_atualizado = sistema['usuario_repo'].get_by_id(usuario.id)
        assert usuario_atualizado.emprestimos_ativos == 1
        
        # 3. Devolver livro
        emprestimo_devolvido = sistema['emprestimo_service'].devolver_livro(
            emprestimo.id
        )
        assert emprestimo_devolvido.data_devolucao_real is not None
        
        # 4. Verificar restauração de contadores
        livro_final = sistema['livro_repo'].get_by_id(livro.id)
        assert livro_final.exemplares_disponiveis == 3
        
        usuario_final = sistema['usuario_repo'].get_by_id(usuario.id)
        assert usuario_final.emprestimos_ativos == 0
    
    def test_validacao_limite_emprestimos(self, sistema_biblioteca):
        """Testa validação de limite de empréstimos por tipo de usuário."""
        # IMPLEMENTAR: Teste de limite de empréstimos
        pass
    
    def test_calculo_multa_atraso(self, sistema_biblioteca):
        """Testa cálculo correto de multa por atraso."""
        # IMPLEMENTAR: Teste de cálculo de multa
        pass
    
    def test_renovacao_emprestimo(self, sistema_biblioteca):
        """Testa renovação de empréstimo válida."""
        # IMPLEMENTAR: Teste de renovação
        pass
```

### Critérios de Avaliação
- [ ] Todos os modelos implementados com validações
- [ ] Serviços de negócio funcionais
- [ ] Relacionamentos entre entidades corretos
- [ ] Tratamento completo de exceções
- [ ] Cobertura de testes >= 85%
- [ ] Testes de integração passando
- [ ] Documentação API completa
- [ ] Configuração de ambiente profissional

### Dicas de Implementação
1. Comece pelos modelos e suas validações
2. Implemente repositórios simples em memória primeiro
3. Foque nas regras de negócio nos serviços
4. Use fixtures para dados de teste consistentes
5. Documente decisões de design no README

### Extensões Opcionais
- Interface CLI com typer
- Persistência em arquivo JSON
- Sistema de reservas de livros
- Relatórios estatísticos avançados
- Notificações por email (simuladas)

---

## Exercício 2.2: API de Clima com Cache 🌤️

### Contexto
Desenvolva uma API que consome dados meteorológicos de serviços externos, implementa cache inteligente para otimizar performance e oferece endpoints para consulta de previsões do tempo com agregações úteis.

### Objetivos Pedagógicos
- Integrar consumo de APIs externas
- Implementar sistemas de cache
- Trabalhar com dados temporais
- Praticar agregações e análises de dados

### Requisitos Funcionais
1. **Consumo de APIs**: OpenWeatherMap ou similar
2. **Cache inteligente**: TTL, invalidação, persistência
3. **Endpoints REST**: Clima atual, previsão, histórico
4. **Agregações**: Média, máxima, mínima, tendências
5. **Alertas**: Condições climáticas extremas

### Requisitos Técnicos
- Cliente HTTP assíncrono com retry/backoff
- Cache com Redis simulado ou em memória
- Validação de entrada e sanitização
- Rate limiting para APIs externas
- Logging estruturado
- Monitoramento de saúde da API

### Critérios de Avaliação
- [ ] Integração com API externa funcional
- [ ] Sistema de cache eficiente
- [ ] Endpoints REST bem documentados
- [ ] Tratamento robusto de erros
- [ ] Testes com mocks para APIs externas
- [ ] Performance adequada sob carga
- [ ] Monitoramento e logging

---

## Exercício 2.3: Sistema de Blog com Tags 📝

### Contexto
Crie um sistema de blog que permite criação de posts, sistema de tags para categorização, busca textual e comentários. O sistema deve ser escalável e ter boa performance para consultas.

### Objetivos Pedagógicos
- Modelar relacionamentos many-to-many
- Implementar busca textual
- Trabalhar com hierarquias (comentários)
- Otimizar consultas e performance

### Requisitos Funcionais
1. **Gestão de Posts**: CRUD completo, rascunhos, publicação
2. **Sistema de Tags**: Criação automática, contadores, busca
3. **Comentários**: Aninhados, moderação, aprovação
4. **Busca**: Por título, conteúdo, tags, autor
5. **Estatísticas**: Visualizações, posts populares, trending tags

### Requisitos Técnicos
- Modelos com relacionamentos complexos
- Índices para otimização de busca
- Paginação eficiente
- Sistema de slug para URLs amigáveis
- Sanitização de HTML
- Sistema de permissões básico

### Critérios de Avaliação
- [ ] Relacionamentos implementados corretamente
- [ ] Sistema de busca funcionando
- [ ] Performance adequada com volumes grandes
- [ ] Interface administrativa funcional
- [ ] Testes de carga básicos
- [ ] Segurança básica implementada
- [ ] API REST documentada
