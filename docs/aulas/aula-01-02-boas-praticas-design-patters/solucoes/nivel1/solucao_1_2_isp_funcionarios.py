#!/usr/bin/env python3
"""
Solução do Exercício 1.2: Implementação de Interface Segregation Principle (ISP)

OBJETIVO: Demonstrar a aplicação do Interface Segregation Principle (ISP)
criando interfaces segregadas para diferentes tipos de funcionários.

CONCEITOS DEMONSTRADOS:
- Interface Segregation Principle (ISP)
- Protocol-based interfaces
- Multiple interface inheritance
- Polymorphism
- Type Hints

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from typing import Protocol, List, Union
from abc import abstractmethod


# =============================================================================
# PROBLEMA: Interface Monolítica (Violação do ISP)
# =============================================================================

class FuncionarioCompleto_Problemático(Protocol):
    """
    ❌ PROBLEMA: Esta interface viola o ISP ao forçar implementação
    de métodos desnecessários para alguns tipos de funcionário.
    
    Consequências:
    - Desenvolvedor forçado a implementar métodos de design
    - Designer forçado a implementar métodos de programação
    - Gerente forçado a implementar métodos técnicos
    - Classes com métodos vazios ou que lançam NotImplementedError
    """
    
    def escrever_codigo(self, linguagem: str) -> str: ...
    def revisar_codigo(self, codigo: str) -> bool: ...
    def criar_design(self, tipo: str) -> str: ...
    def usar_ferramenta_design(self, ferramenta: str) -> bool: ...
    def gerenciar_equipe(self, tarefa: str) -> bool: ...
    def aprovar_projeto(self, projeto: str) -> bool: ...


# =============================================================================
# SOLUÇÃO: INTERFACES SEGREGADAS (Aplicando ISP)
# =============================================================================

# 1. INTERFACES ESPECÍFICAS E COESAS
# -----------------------------------------------------------------------------

class PodeProgramar(Protocol):
    """
    ✅ Interface específica para capacidades de programação
    
    BENEFÍCIOS:
    - Coesa: apenas métodos relacionados à programação
    - Específica: foca em uma responsabilidade clara
    - Reutilizável: pode ser implementada por qualquer classe que programa
    """
    
    @abstractmethod
    def escrever_codigo(self, linguagem: str) -> str:
        """
        Escreve código na linguagem especificada.
        
        Args:
            linguagem: Linguagem de programação (Python, Java, etc.)
            
        Returns:
            str: Código escrito
        """
        ...
    
    @abstractmethod
    def revisar_codigo(self, codigo: str) -> bool:
        """
        Revisa código fornecido.
        
        Args:
            codigo: Código fonte para revisar
            
        Returns:
            bool: True se código foi aprovado na revisão
        """
        ...


class PodeDesignar(Protocol):
    """
    ✅ Interface específica para capacidades de design
    
    BENEFÍCIOS:
    - Independente de programação
    - Focada em criação visual
    - Pode evoluir sem afetar outras interfaces
    """
    
    @abstractmethod
    def criar_design(self, tipo: str) -> str:
        """
        Cria design do tipo especificado.
        
        Args:
            tipo: Tipo de design (logo, banner, interface, etc.)
            
        Returns:
            str: Descrição ou caminho do design criado
        """
        ...
    
    @abstractmethod
    def usar_ferramenta_design(self, ferramenta: str) -> bool:
        """
        Utiliza ferramenta de design.
        
        Args:
            ferramenta: Nome da ferramenta (Figma, Photoshop, etc.)
            
        Returns:
            bool: True se conseguiu usar a ferramenta
        """
        ...


class PodeGerenciar(Protocol):
    """
    ✅ Interface específica para capacidades de gerenciamento
    
    BENEFÍCIOS:
    - Separada de habilidades técnicas
    - Focada em liderança e processos
    - Permite diferentes estilos de gerenciamento
    """
    
    @abstractmethod
    def gerenciar_equipe(self, tarefa: str) -> bool:
        """
        Gerencia equipe para executar tarefa.
        
        Args:
            tarefa: Descrição da tarefa a ser gerenciada
            
        Returns:
            bool: True se tarefa foi delegada com sucesso
        """
        ...
    
    @abstractmethod
    def aprovar_projeto(self, projeto: str) -> bool:
        """
        Aprova ou rejeita projeto.
        
        Args:
            projeto: Descrição do projeto para aprovação
            
        Returns:
            bool: True se projeto foi aprovado
        """
        ...


class PodeTreinar(Protocol):
    """
    ✅ Interface específica para capacidades de treinamento
    
    BENEFÍCIOS:
    - Reutilizável por diferentes tipos de funcionário
    - Focada em transferência de conhecimento
    - Independente das outras habilidades
    """
    
    @abstractmethod
    def criar_treinamento(self, topico: str) -> str:
        """
        Cria material de treinamento sobre tópico.
        
        Args:
            topico: Assunto do treinamento
            
        Returns:
            str: Descrição do material criado
        """
        ...
    
    @abstractmethod
    def ministrar_aula(self, participantes: List[str], conteudo: str) -> bool:
        """
        Ministra aula para participantes.
        
        Args:
            participantes: Lista de nomes dos participantes
            conteudo: Conteúdo a ser ensinado
            
        Returns:
            bool: True se aula foi ministrada com sucesso
        """
        ...


# =============================================================================
# IMPLEMENTAÇÕES CONCRETAS DOS FUNCIONÁRIOS
# =============================================================================

class Desenvolvedor:
    """
    ✅ Implementa apenas interface relevante (PodeProgramar)
    
    BENEFÍCIOS:
    - Não é forçado a implementar métodos irrelevantes
    - Interface coesa com suas responsabilidades
    - Pode focar na qualidade da implementação de programação
    """
    
    def __init__(self, nome: str, linguagens: List[str]):
        self.nome = nome
        self.linguagens = linguagens
        self.projetos_desenvolvidos: List[str] = []
        self.codigo_revisado: List[str] = []
    
    def escrever_codigo(self, linguagem: str) -> str:
        """
        Escreve código na linguagem especificada.
        
        Implementação específica para desenvolvedor que verifica
        se ele conhece a linguagem solicitada.
        """
        if linguagem not in self.linguagens:
            return f"❌ {self.nome} não conhece {linguagem}"
        
        codigo = f"""
        # Código {linguagem} desenvolvido por {self.nome}
        def funcao_exemplo():
            print("Hello from {linguagem}!")
            return "Código de qualidade desenvolvido"
        """
        
        self.projetos_desenvolvidos.append(f"Projeto em {linguagem}")
        print(f"👨‍💻 {self.nome} escreveu código em {linguagem}")
        return codigo.strip()
    
    def revisar_codigo(self, codigo: str) -> bool:
        """
        Revisa código aplicando boas práticas.
        
        Implementação que simula análise de qualidade de código.
        """
        # Simulação de critérios de revisão
        criterios_aprovacao = [
            len(codigo) > 10,  # Não pode ser muito simples
            "def " in codigo or "class " in codigo,  # Deve ter estrutura
            "#" in codigo or '"""' in codigo  # Deve ter comentários
        ]
        
        aprovado = all(criterios_aprovacao)
        self.codigo_revisado.append(codigo[:50] + "...")
        
        status = "✅ aprovado" if aprovado else "❌ rejeitado"
        print(f"🔍 {self.nome} revisou código: {status}")
        return aprovado
    
    def listar_linguagens(self) -> List[str]:
        """Método específico do desenvolvedor"""
        return self.linguagens.copy()
    
    def __str__(self) -> str:
        return f"Desenvolvedor({self.nome}, linguagens={self.linguagens})"


class Designer:
    """
    ✅ Implementa apenas interface relevante (PodeDesignar)
    
    BENEFÍCIOS:
    - Focado em suas competências de design
    - Não precisa implementar métodos de programação
    - Interface limpa e específica
    """
    
    def __init__(self, nome: str, ferramentas: List[str]):
        self.nome = nome
        self.ferramentas = ferramentas
        self.designs_criados: List[str] = []
    
    def criar_design(self, tipo: str) -> str:
        """
        Cria design baseado no tipo solicitado.
        
        Implementação específica que considera especialização do designer.
        """
        tipos_suportados = ["logo", "banner", "interface", "icone", "poster"]
        
        if tipo.lower() not in tipos_suportados:
            return f"❌ {self.nome} não cria designs do tipo '{tipo}'"
        
        design_path = f"designs/{tipo}_{self.nome.lower()}_{len(self.designs_criados)+1}.svg"
        self.designs_criados.append(design_path)
        
        print(f"🎨 {self.nome} criou {tipo}: {design_path}")
        return design_path
    
    def usar_ferramenta_design(self, ferramenta: str) -> bool:
        """
        Utiliza ferramenta de design se disponível.
        
        Verifica se o designer tem experiência com a ferramenta.
        """
        if ferramenta in self.ferramentas:
            print(f"🛠️ {self.nome} está usando {ferramenta}")
            return True
        else:
            print(f"❌ {self.nome} não sabe usar {ferramenta}")
            return False
    
    def listar_ferramentas(self) -> List[str]:
        """Método específico do designer"""
        return self.ferramentas.copy()
    
    def __str__(self) -> str:
        return f"Designer({self.nome}, ferramentas={self.ferramentas})"


class Gerente:
    """
    ✅ Implementa apenas interface relevante (PodeGerenciar)
    
    BENEFÍCIOS:
    - Focado em responsabilidades de gestão
    - Não é obrigado a implementar habilidades técnicas
    - Interface alinhada com seu papel na empresa
    """
    
    def __init__(self, nome: str, equipe: List[str]):
        self.nome = nome
        self.equipe = equipe
        self.tarefas_delegadas: List[str] = []
        self.projetos_aprovados: List[str] = []
    
    def gerenciar_equipe(self, tarefa: str) -> bool:
        """
        Delega tarefa para equipe gerenciada.
        
        Implementação que verifica disponibilidade da equipe.
        """
        if not self.equipe:
            print(f"❌ {self.nome} não tem equipe para delegar '{tarefa}'")
            return False
        
        # Simular delegação para membro da equipe
        responsavel = self.equipe[len(self.tarefas_delegadas) % len(self.equipe)]
        self.tarefas_delegadas.append(f"{tarefa} -> {responsavel}")
        
        print(f"👥 {self.nome} delegou '{tarefa}' para {responsavel}")
        return True
    
    def aprovar_projeto(self, projeto: str) -> bool:
        """
        Analisa e aprova/rejeita projeto.
        
        Implementação que simula critérios de aprovação gerencial.
        """
        # Simulação de critérios de aprovação
        criterios_aprovacao = [
            len(projeto) > 20,  # Projeto deve ter descrição adequada
            any(palavra in projeto.lower() for palavra in 
                ["beneficio", "custo", "prazo", "recurso"]),  # Deve abordar aspectos gerenciais
            "cronograma" in projeto.lower() or "deadline" in projeto.lower()  # Deve ter timeline
        ]
        
        aprovado = sum(criterios_aprovacao) >= 2  # Pelo menos 2 critérios
        
        if aprovado:
            self.projetos_aprovados.append(projeto)
            print(f"✅ {self.nome} aprovou projeto: {projeto[:30]}...")
        else:
            print(f"❌ {self.nome} rejeitou projeto: critérios insuficientes")
        
        return aprovado
    
    def listar_equipe(self) -> List[str]:
        """Método específico do gerente"""
        return self.equipe.copy()
    
    def __str__(self) -> str:
        return f"Gerente({self.nome}, equipe={len(self.equipe)} pessoas)"


class FullStack:
    """
    ✅ Implementa múltiplas interfaces (PodeProgramar + PodeDesignar)
    
    BENEFÍCIOS:
    - Demonstra herança múltipla de interfaces
    - Cada interface mantém sua coesão
    - Flexibilidade para funcionários multidisciplinares
    - Sem violação do ISP: implementa apenas o que usa
    """
    
    def __init__(self, nome: str, linguagens: List[str], ferramentas_design: List[str]):
        self.nome = nome
        self.linguagens = linguagens
        self.ferramentas_design = ferramentas_design
        self.projetos_completos: List[str] = []
    
    # Implementação da interface PodeProgramar
    def escrever_codigo(self, linguagem: str) -> str:
        """Implementa método de programação"""
        if linguagem not in self.linguagens:
            return f"❌ {self.nome} não programa em {linguagem}"
        
        codigo = f"""
        // Código Full Stack em {linguagem} por {self.nome}
        class AplicacaoCompleta {{
            frontend() {{ return "Interface responsiva"; }}
            backend() {{ return "API robusta"; }}
            database() {{ return "Dados estruturados"; }}
        }}
        """
        
        print(f"💻 {self.nome} (FullStack) desenvolveu em {linguagem}")
        return codigo.strip()
    
    def revisar_codigo(self, codigo: str) -> bool:
        """Implementa revisão com visão full stack"""
        # Critérios mais rigorosos para full stack
        criterios = [
            len(codigo) > 15,
            any(palavra in codigo.lower() for palavra in 
                ["frontend", "backend", "api", "database", "interface"]),
            "{" in codigo or "def " in codigo or "class " in codigo
        ]
        
        aprovado = all(criterios)
        status = "✅ aprovado (visão full stack)" if aprovado else "❌ rejeitado"
        print(f"🔍 {self.nome} (FullStack) revisou: {status}")
        return aprovado
    
    # Implementação da interface PodeDesignar
    def criar_design(self, tipo: str) -> str:
        """Implementa criação de design"""
        design_path = f"designs/fullstack_{tipo}_{self.nome.lower()}.fig"
        print(f"🎨 {self.nome} (FullStack) criou design {tipo}: {design_path}")
        return design_path
    
    def usar_ferramenta_design(self, ferramenta: str) -> bool:
        """Implementa uso de ferramentas de design"""
        if ferramenta in self.ferramentas_design:
            print(f"🛠️ {self.nome} (FullStack) usando {ferramenta}")
            return True
        else:
            print(f"❌ {self.nome} (FullStack) não usa {ferramenta}")
            return False
    
    def desenvolver_projeto_completo(self, nome_projeto: str) -> str:
        """Método específico do full stack: projeto end-to-end"""
        projeto = {
            "nome": nome_projeto,
            "frontend": self.criar_design("interface"),
            "backend": self.escrever_codigo("Python"),
            "responsivo": True
        }
        
        self.projetos_completos.append(nome_projeto)
        print(f"🚀 {self.nome} entregou projeto completo: {nome_projeto}")
        return f"Projeto {nome_projeto} desenvolvido end-to-end"
    
    def __str__(self) -> str:
        return f"FullStack({self.nome}, {len(self.linguagens)} linguagens, {len(self.ferramentas_design)} ferramentas design)"


class TechLead:
    """
    ✅ Implementa múltiplas interfaces (PodeProgramar + PodeGerenciar + PodeTreinar)
    
    BENEFÍCIOS:
    - Combinação natural de habilidades para o cargo
    - Cada interface mantém sua responsabilidade específica
    - Flexibilidade para diferentes modelos de liderança técnica
    """
    
    def __init__(self, nome: str, linguagens: List[str], equipe: List[str]):
        self.nome = nome
        self.linguagens = linguagens
        self.equipe = equipe
        self.mentorias_realizadas: List[str] = []
    
    # Implementação PodeProgramar
    def escrever_codigo(self, linguagem: str) -> str:
        """Tech Lead programa soluções arquiteturais"""
        if linguagem not in self.linguagens:
            return f"❌ {self.nome} não arquiteta em {linguagem}"
        
        codigo = f"""
        # Arquitetura {linguagem} por Tech Lead {self.nome}
        class ArquiteturaSistema:
            def definir_padroes(self):
                return "SOLID + Design Patterns"
            
            def revisar_arquitetura(self):
                return "Escalabilidade + Manutenibilidade"
        """
        
        print(f"🏗️ {self.nome} (TechLead) definiu arquitetura em {linguagem}")
        return codigo.strip()
    
    def revisar_codigo(self, codigo: str) -> bool:
        """Revisão focada em arquitetura e padrões"""
        criterios_arquiteturais = [
            len(codigo) > 20,
            any(palavra in codigo.lower() for palavra in 
                ["class", "interface", "pattern", "solid", "architecture"]),
            "def " in codigo or "function" in codigo
        ]
        
        aprovado = sum(criterios_arquiteturais) >= 2
        foco = "arquitetura e padrões" if aprovado else "precisa melhorar estrutura"
        print(f"🔍 {self.nome} (TechLead) revisou: {foco}")
        return aprovado
    
    # Implementação PodeGerenciar
    def gerenciar_equipe(self, tarefa: str) -> bool:
        """Gerenciamento técnico de equipe"""
        if not self.equipe:
            return False
        
        # Tech Lead considera complexidade técnica
        if "arquitetura" in tarefa.lower() or "design" in tarefa.lower():
            responsavel = self.nome  # Tech Lead assume tarefas arquiteturais
            print(f"🏗️ {self.nome} (TechLead) assumiu tarefa arquitetural: {tarefa}")
        else:
            responsavel = self.equipe[0]  # Delega implementação
            print(f"👥 {self.nome} (TechLead) delegou para {responsavel}: {tarefa}")
        
        return True
    
    def aprovar_projeto(self, projeto: str) -> bool:
        """Aprovação com foco em viabilidade técnica"""
        criterios_tecnicos = [
            "tecnologia" in projeto.lower() or "arquitetura" in projeto.lower(),
            "escalabilidade" in projeto.lower() or "performance" in projeto.lower(),
            len(projeto) > 30
        ]
        
        aprovado = sum(criterios_tecnicos) >= 2
        aspecto = "viabilidade técnica" if aprovado else "precisa detalhamento técnico"
        print(f"⚙️ {self.nome} (TechLead) analisou {aspecto}")
        return aprovado
    
    # Implementação PodeTreinar  
    def criar_treinamento(self, topico: str) -> str:
        """Cria treinamento técnico para equipe"""
        material = f"""
        Treinamento: {topico}
        Instrutor: {self.nome} (Tech Lead)
        
        Módulos:
        1. Fundamentos teóricos
        2. Boas práticas
        3. Exemplos práticos
        4. Exercícios hands-on
        
        Duração: 4 horas
        Pré-requisitos: Conhecimento básico de programação
        """
        
        print(f"📚 {self.nome} (TechLead) criou treinamento: {topico}")
        return material.strip()
    
    def ministrar_aula(self, participantes: List[str], conteudo: str) -> bool:
        """Ministra aula técnica"""
        if not participantes:
            return False
        
        self.mentorias_realizadas.append(f"{conteudo} para {len(participantes)} pessoas")
        print(f"🎓 {self.nome} (TechLead) treinou {len(participantes)} pessoas em: {conteudo}")
        return True
    
    def __str__(self) -> str:
        return f"TechLead({self.nome}, {len(self.equipe)} devs, {len(self.mentorias_realizadas)} treinamentos)"


# =============================================================================
# FUNÇÕES POLIMÓRFICAS (Demonstram benefícios do ISP)
# =============================================================================

def processar_funcionario_programador(funcionario: PodeProgramar) -> None:
    """
    Função polimórfica que trabalha com qualquer funcionário que pode programar.
    
    BENEFÍCIO DO ISP:
    - Aceita apenas o que precisa (interface específica)
    - Não se importa com outras capacidades do funcionário
    - Fácil de testar (pode receber mock de PodeProgramar)
    """
    print(f"\n🔧 Processando capacidades de programação...")
    codigo = funcionario.escrever_codigo("Python")
    aprovado = funcionario.revisar_codigo("def exemplo(): return 'teste'")
    print(f"📝 Código produzido: {len(codigo)} caracteres")
    print(f"✅ Revisão: {'Aprovada' if aprovado else 'Rejeitada'}")


def processar_funcionario_designer(funcionario: PodeDesignar) -> None:
    """
    Função polimórfica para funcionários com capacidades de design.
    
    BENEFÍCIO DO ISP:
    - Interface coesa e específica
    - Sem dependência de métodos irrelevantes
    - Fácil manutenção e extensão
    """
    print(f"\n🎨 Processando capacidades de design...")
    design = funcionario.criar_design("logo")
    ferramenta_ok = funcionario.usar_ferramenta_design("Figma")
    print(f"🖼️ Design criado: {design}")
    print(f"🛠️ Ferramenta: {'Disponível' if ferramenta_ok else 'Indisponível'}")


def processar_funcionario_gerente(funcionario: PodeGerenciar) -> None:
    """
    Função polimórfica para funcionários com capacidades gerenciais.
    
    BENEFÍCIO DO ISP:
    - Foca apenas em responsabilidades de gestão
    - Independente de habilidades técnicas
    - Permite diferentes estilos de liderança
    """
    print(f"\n👥 Processando capacidades gerenciais...")
    tarefa_ok = funcionario.gerenciar_equipe("Desenvolver nova funcionalidade")
    projeto_ok = funcionario.aprovar_projeto("Sistema de vendas com cronograma de 3 meses e benefício de redução de custos em 20%")
    print(f"📋 Delegação: {'Sucesso' if tarefa_ok else 'Falha'}")
    print(f"✅ Aprovação: {'Autorizada' if projeto_ok else 'Rejeitada'}")


def processar_funcionario_multifuncional(funcionario: Union[PodeProgramar, PodeDesignar]) -> None:
    """
    Função que demonstra como trabalhar com funcionários multifuncionais.
    
    BENEFÍCIO DO ISP:
    - Type hints específicos para cada capacidade
    - Verificação em tempo de execução
    - Flexibilidade sem violação de princípios
    """
    print(f"\n🔄 Verificando capacidades múltiplas...")
    
    # Verifica se pode programar
    if isinstance(funcionario, PodeProgramar):
        print("💻 Capacidade de programação detectada")
        codigo = funcionario.escrever_codigo("JavaScript")
    
    # Verifica se pode fazer design (usando hasattr para Protocol)
    if hasattr(funcionario, 'criar_design') and hasattr(funcionario, 'usar_ferramenta_design'):
        print("🎨 Capacidade de design detectada")
        design = funcionario.criar_design("interface")


# =============================================================================
# DEMONSTRAÇÃO E TESTES
# =============================================================================

def demonstrar_isp():
    """
    Demonstra os benefícios do Interface Segregation Principle.
    
    DEMONSTRAÇÃO:
    1. Criação de funcionários com interfaces específicas
    2. Uso polimórfico das interfaces
    3. Benefícios de manutenibilidade e testabilidade
    """
    
    print("🔧 DEMONSTRAÇÃO: Interface Segregation Principle (ISP)")
    print("=" * 65)
    
    print("\n📦 1. Criando funcionários com interfaces específicas...")
    
    # Criar diferentes tipos de funcionário
    dev = Desenvolvedor("Alice", ["Python", "JavaScript", "Go"])
    designer = Designer("Bob", ["Figma", "Photoshop", "Sketch"])
    gerente = Gerente("Carol", ["Alice", "Bob", "David", "Eva"])
    fullstack = FullStack("Diana", ["Python", "React"], ["Figma", "Adobe XD"])
    tech_lead = TechLead("Eduardo", ["Python", "Java", "Architecture"], ["Alice", "Bob"])
    
    print(f"✅ {dev}")
    print(f"✅ {designer}")
    print(f"✅ {gerente}")
    print(f"✅ {fullstack}")
    print(f"✅ {tech_lead}")
    
    print("\n🔄 2. Demonstrando polimorfismo com interfaces específicas...")
    
    # Demonstrar polimorfismo - cada função recebe apenas a interface necessária
    funcionarios_programadores: List[PodeProgramar] = [dev, fullstack, tech_lead]
    funcionarios_designers: List[PodeDesignar] = [designer, fullstack]
    funcionarios_gerentes: List[PodeGerenciar] = [gerente, tech_lead]
    
    # Processar programadores
    for programador in funcionarios_programadores:
        processar_funcionario_programador(programador)
    
    # Processar designers  
    for design_worker in funcionarios_designers:
        processar_funcionario_designer(design_worker)
    
    # Processar gerentes
    for manager in funcionarios_gerentes:
        processar_funcionario_gerente(manager)
    
    print("\n🎯 3. Demonstrando funcionários multifuncionais...")
    
    # FullStack pode ser usado como programador OU designer
    print("\n🔄 FullStack como programador:")
    processar_funcionario_programador(fullstack)
    
    print("\n🔄 FullStack como designer:")
    processar_funcionario_designer(fullstack)
    
    # TechLead pode ser programador, gerente E treinador
    print("\n🔄 TechLead exercendo múltiplos papéis:")
    processar_funcionario_programador(tech_lead)
    processar_funcionario_gerente(tech_lead)
    
    # Demonstrar capacidade única de treinamento
    treinamento = tech_lead.criar_treinamento("Design Patterns em Python")
    tech_lead.ministrar_aula(["Alice", "Bob", "Diana"], "SOLID Principles")
    
    print("\n📊 4. Análise dos Benefícios do ISP:")
    print("   ✅ Interfaces coesas e específicas")
    print("   ✅ Nenhuma classe implementa métodos desnecessários")
    print("   ✅ Polimorfismo preciso e type-safe")
    print("   ✅ Fácil adição de novos tipos de funcionário")
    print("   ✅ Testabilidade melhorada (interfaces menores)")
    print("   ✅ Manutenibilidade: mudanças isoladas por interface")


def executar_testes_isp():
    """
    Executa testes para validar implementação do ISP.
    
    TESTES:
    - Verificação de interfaces específicas
    - Polimorfismo correto
    - Não violação do ISP
    """
    
    print("\n🧪 EXECUTANDO TESTES ISP...")
    print("=" * 40)
    
    # Setup
    dev = Desenvolvedor("TestDev", ["Python"])
    designer = Designer("TestDesigner", ["Figma"])
    gerente = Gerente("TestManager", ["Dev1", "Dev2"])
    fullstack = FullStack("TestFull", ["Python"], ["Figma"])
    
    # Teste 1: Interfaces específicas
    print("\n🔍 Teste 1: Verificação de interfaces específicas...")
    
    # Desenvolvedor implementa PodeProgramar
    assert hasattr(dev, 'escrever_codigo')
    assert hasattr(dev, 'revisar_codigo')
    # Desenvolvedor NÃO implementa outras interfaces
    assert not hasattr(dev, 'criar_design')
    assert not hasattr(dev, 'gerenciar_equipe')
    
    print("✅ Desenvolvedor: implementa apenas PodeProgramar")
    
    # Designer implementa PodeDesignar
    assert hasattr(designer, 'criar_design')
    assert hasattr(designer, 'usar_ferramenta_design')
    # Designer NÃO implementa outras interfaces
    assert not hasattr(designer, 'escrever_codigo')
    assert not hasattr(designer, 'gerenciar_equipe')
    
    print("✅ Designer: implementa apenas PodeDesignar")
    
    # Gerente implementa PodeGerenciar
    assert hasattr(gerente, 'gerenciar_equipe')
    assert hasattr(gerente, 'aprovar_projeto')
    # Gerente NÃO implementa outras interfaces
    assert not hasattr(gerente, 'escrever_codigo')
    assert not hasattr(gerente, 'criar_design')
    
    print("✅ Gerente: implementa apenas PodeGerenciar")
    
    # Teste 2: FullStack implementa múltiplas interfaces
    print("\n🔍 Teste 2: FullStack com múltiplas interfaces...")
    
    assert hasattr(fullstack, 'escrever_codigo')  # PodeProgramar
    assert hasattr(fullstack, 'revisar_codigo')   # PodeProgramar
    assert hasattr(fullstack, 'criar_design')     # PodeDesignar
    assert hasattr(fullstack, 'usar_ferramenta_design')  # PodeDesignar
    
    print("✅ FullStack: implementa PodeProgramar E PodeDesignar")
    
    # Teste 3: Polimorfismo funciona
    print("\n🔍 Teste 3: Polimorfismo com type hints...")
    
    def teste_polimorfismo_programador(p: PodeProgramar) -> bool:
        codigo = p.escrever_codigo("Python")
        return len(codigo) > 0
    
    def teste_polimorfismo_designer(d: PodeDesignar) -> bool:
        design = d.criar_design("teste")
        return len(design) > 0
    
    # Testar polimorfismo
    assert teste_polimorfismo_programador(dev) == True
    assert teste_polimorfismo_programador(fullstack) == True
    assert teste_polimorfismo_designer(designer) == True
    assert teste_polimorfismo_designer(fullstack) == True
    
    print("✅ Polimorfismo: funciona corretamente")
    
    # Teste 4: Funcionalidade específica
    print("\n🔍 Teste 4: Funcionalidade específica por tipo...")
    
    # Desenvolvedor consegue programar
    codigo = dev.escrever_codigo("Python")
    assert "Python" in codigo
    assert dev.revisar_codigo("def test(): pass") == True
    
    # Designer consegue criar design
    design = designer.criar_design("logo")
    assert "logo" in design
    assert designer.usar_ferramenta_design("Figma") == True
    
    # Gerente consegue gerenciar
    assert gerente.gerenciar_equipe("tarefa teste") == True
    assert gerente.aprovar_projeto("projeto com cronograma e beneficio de redução") == True
    
    print("✅ Funcionalidades específicas: todas funcionam")
    
    print("\n🎉 TODOS OS TESTES ISP PASSARAM!")
    print("\n📋 Resumo dos benefícios demonstrados:")
    print("   🎯 Interfaces coesas e focadas")
    print("   🔒 Nenhuma implementação desnecessária")
    print("   🔄 Polimorfismo type-safe")
    print("   🧩 Composição flexível de interfaces")
    print("   🧪 Facilidade de testes (interfaces menores)")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Demonstrar ISP
    demonstrar_isp()
    
    # Executar testes
    executar_testes_isp()
    
    print("\n" + "=" * 65)
    print("📚 ANÁLISE FINAL DO ISP:")
    print()
    print("PROBLEMA ORIGINAL:")
    print("❌ Interface monolítica força implementações desnecessárias")
    print("❌ Classes com métodos vazios ou NotImplementedError")
    print("❌ Acoplamento alto entre responsabilidades diferentes")
    print("❌ Dificulta testes e manutenção")
    print()
    print("SOLUÇÃO COM ISP:")
    print("✅ Interfaces específicas e coesas")
    print("✅ Cada classe implementa apenas o que usa")
    print("✅ Polimorfismo preciso e type-safe")
    print("✅ Facilita composição e extensibilidade")
    print("✅ Testes mais simples (interfaces menores)")
    print("✅ Manutenção isolada por responsabilidade")
    print()
    print("🎯 RESULTADO: Interfaces segregadas melhoram flexibilidade e manutenibilidade!")
