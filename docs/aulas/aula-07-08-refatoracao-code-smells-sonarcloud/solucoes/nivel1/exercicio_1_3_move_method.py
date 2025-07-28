"""
Solução do Exercício 1.3: Move Method - Sistema de Validação

Esta solução demonstra como aplicar Move Method para resolver
Feature Envy, movendo métodos para as classes onde eles
realmente pertencem, melhorando coesão e encapsulamento.

REFATORAÇÕES APLICADAS:
1. Move Method para eliminar Feature Envy
2. Criação da classe Usuario com validações próprias
3. Melhoria do encapsulamento
4. Separação clara de responsabilidades
5. Preservação da interface pública
"""

import re
from typing import List, Optional, Dict


class Usuario:
    """
    Classe Usuario com validações próprias.
    
    ANTES: Validações espalhadas no GerenciadorUsuarios (Feature Envy)
    DEPOIS: Validações encapsuladas na própria classe Usuario
    
    BENEFÍCIOS:
    - Coesão melhorada (dados e métodos juntos)
    - Reutilização das validações
    - Testabilidade individual
    - Encapsulamento adequado
    """
    
    def __init__(self, nome: str, email: str, senha: str, idade: int):
        """
        Inicializa usuário com validação automática opcional.
        
        Args:
            nome: Nome completo do usuário
            email: Email válido
            senha: Senha com critérios de segurança
            idade: Idade em anos
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idade = idade
    
    def validar_email(self) -> bool:
        """
        Valida o formato do email do usuário.
        
        MOVIMENTO: GerenciadorUsuarios.validar_email() → Usuario.validar_email()
        MOTIVO: Método usa apenas dados do usuário (self.email)
        
        Returns:
            bool: True se email é válido, False caso contrário
        """
        if not self.email:
            return False
        
        # Regex mais robusta para validação de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, self.email))
    
    def validar_senha(self) -> bool:
        """
        Valida se a senha atende aos critérios de segurança.
        
        MOVIMENTO: GerenciadorUsuarios.validar_senha() → Usuario.validar_senha()
        MOTIVO: Método usa apenas dados do usuário (self.senha)
        
        Critérios:
        - Mínimo 8 caracteres
        - Pelo menos uma letra maiúscula
        - Pelo menos um número
        - Pelo menos um caractere especial
        
        Returns:
            bool: True se senha é válida, False caso contrário
        """
        if len(self.senha) < 8:
            return False
        
        # Verificar se tem pelo menos uma letra maiúscula
        if not any(c.isupper() for c in self.senha):
            return False
        
        # Verificar se tem pelo menos um número
        if not any(c.isdigit() for c in self.senha):
            return False
        
        # Verificar se tem pelo menos um caractere especial
        especiais = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in especiais for c in self.senha):
            return False
        
        return True
    
    def validar_idade(self) -> bool:
        """
        Valida se a idade está dentro dos limites aceitáveis.
        
        MOVIMENTO: GerenciadorUsuarios.validar_idade() → Usuario.validar_idade()
        MOTIVO: Método usa apenas dados do usuário (self.idade)
        
        Returns:
            bool: True se idade é válida (18-120), False caso contrário
        """
        return 18 <= self.idade <= 120
    
    def validar_nome(self) -> bool:
        """
        Valida se o nome possui formato adequado.
        
        MOVIMENTO: GerenciadorUsuarios.validar_nome() → Usuario.validar_nome()
        MOTIVO: Método usa apenas dados do usuário (self.nome)
        
        Critérios:
        - Mínimo 2 caracteres
        - Apenas letras e espaços
        
        Returns:
            bool: True se nome é válido, False caso contrário
        """
        nome_limpo = self.nome.strip()
        if len(nome_limpo) < 2:
            return False
        
        # Verificar se contém apenas letras e espaços
        return all(c.isalpha() or c.isspace() for c in nome_limpo)
    
    def validar_completo(self) -> Dict[str, any]:
        """
        Executa todas as validações e retorna resultado consolidado.
        
        NOVO MÉTODO: Coordena validações internas da classe
        BENEFÍCIO: Interface simples para validação completa
        
        Returns:
            Dict com resultado das validações e lista de erros
        """
        erros = []
        
        if not self.validar_email():
            erros.append("Email inválido")
        
        if not self.validar_senha():
            erros.append("Senha deve ter 8+ caracteres, maiúscula, número e símbolo")
        
        if not self.validar_idade():
            erros.append("Idade deve estar entre 18 e 120 anos")
        
        if not self.validar_nome():
            erros.append("Nome deve ter 2+ caracteres e apenas letras")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros
        }
    
    def obter_detalhes_validacao(self) -> Dict[str, bool]:
        """
        Método adicional para obter status individual de cada validação.
        
        BENEFÍCIO: Útil para UIs que mostram status campo por campo
        
        Returns:
            Dict com status de cada validação
        """
        return {
            "email_valido": self.validar_email(),
            "senha_valida": self.validar_senha(), 
            "idade_valida": self.validar_idade(),
            "nome_valido": self.validar_nome()
        }
    
    def to_dict(self) -> Dict[str, any]:
        """
        Converte usuário para dicionário (para compatibilidade).
        
        Returns:
            Dict com dados do usuário
        """
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "idade": self.idade
        }
    
    @classmethod
    def from_dict(cls, dados: Dict[str, any]) -> 'Usuario':
        """
        Cria instância de Usuario a partir de dicionário.
        
        Args:
            dados: Dicionário com dados do usuário
            
        Returns:
            Nova instância de Usuario
        """
        return cls(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
            idade=dados.get("idade", 0)
        )
    
    def __str__(self) -> str:
        """String representation do usuário."""
        return f"Usuario(nome='{self.nome}', email='{self.email}', idade={self.idade})"
    
    def __repr__(self) -> str:
        """Representation detalhada do usuário."""
        return f"Usuario(nome='{self.nome}', email='{self.email}', idade={self.idade})"


class GerenciadorUsuariosRefatorado:
    """
    Gerenciador refatorado após aplicação de Move Method.
    
    RESPONSABILIDADES RESTANTES:
    - Persistência/armazenamento
    - Coordenação do processo de cadastro
    - Gerenciamento da coleção de usuários
    
    RESPONSABILIDADES REMOVIDAS:
    - Validações específicas (movidas para Usuario)
    - Lógica de negócio sobre dados do usuário
    """
    
    def __init__(self):
        """Inicializa com lista de usuários vazia."""
        self.usuarios: List[Usuario] = []
    
    def cadastrar_usuario(self, dados_usuario: Dict[str, any]) -> bool:
        """
        Método principal para cadastro - mantém interface pública.
        
        ALTERAÇÕES APÓS MOVE METHOD:
        - Cria instância de Usuario
        - Delega validações para a classe Usuario
        - Foca apenas na coordenação e persistência
        
        Args:
            dados_usuario: Dicionário com dados do usuário
            
        Returns:
            bool: True se cadastro foi bem-sucedido, False caso contrário
        """
        # Criar instância de Usuario a partir dos dados
        usuario = Usuario.from_dict(dados_usuario)
        
        # Delegar validação para a classe Usuario
        validacao = usuario.validar_completo()
        
        if not validacao["valido"]:
            print(f"Erros de validação: {validacao['erros']}")
            return False
        
        # Verificar se email já existe (responsabilidade do gerenciador)
        if self._email_ja_existe(usuario.email):
            print(f"Erro: Email {usuario.email} já está cadastrado")
            return False
        
        # Persistir usuário (responsabilidade do gerenciador)
        self.usuarios.append(usuario)
        print(f"Usuário {usuario.nome} cadastrado com sucesso!")
        return True
    
    def _email_ja_existe(self, email: str) -> bool:
        """
        Verifica se email já está cadastrado.
        
        RESPONSABILIDADE CORRETA: Gerenciador conhece todos os usuários
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se email já existe, False caso contrário
        """
        return any(usuario.email.lower() == email.lower() for usuario in self.usuarios)
    
    def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Usuario encontrado ou None
        """
        for usuario in self.usuarios:
            if usuario.email.lower() == email.lower():
                return usuario
        return None
    
    def listar_usuarios(self) -> List[Usuario]:
        """
        Retorna lista de todos os usuários cadastrados.
        
        Returns:
            Lista de usuários
        """
        return self.usuarios.copy()
    
    def obter_estatisticas_validacao(self) -> Dict[str, int]:
        """
        Método adicional que demonstra como trabalhar com as validações.
        
        Returns:
            Estatísticas sobre validações dos usuários cadastrados
        """
        if not self.usuarios:
            return {"total": 0}
        
        estatisticas = {
            "total": len(self.usuarios),
            "emails_validos": 0,
            "senhas_validas": 0,
            "idades_validas": 0,
            "nomes_validos": 0
        }
        
        for usuario in self.usuarios:
            detalhes = usuario.obter_detalhes_validacao()
            if detalhes["email_valido"]:
                estatisticas["emails_validos"] += 1
            if detalhes["senha_valida"]:
                estatisticas["senhas_validas"] += 1
            if detalhes["idade_valida"]:
                estatisticas["idades_validas"] += 1
            if detalhes["nome_valido"]:
                estatisticas["nomes_validos"] += 1
        
        return estatisticas


# =============================================================================
# DEMONSTRAÇÃO DE USO E COMPARAÇÃO
# =============================================================================

def demonstrar_refatoracao():
    """
    Demonstra o uso do sistema refatorado e melhoria na organização.
    """
    print("=== DEMONSTRAÇÃO: Sistema de Validação Refatorado ===\n")
    
    gerenciador = GerenciadorUsuariosRefatorado()
    
    # Cenários de teste
    usuarios_teste = [
        {
            "nome": "João Silva",
            "email": "joao@email.com",
            "senha": "MinhaSenh@123",
            "idade": 30
        },
        {
            "nome": "A",  # Nome muito curto
            "email": "maria@email.com",
            "senha": "123",  # Senha fraca
            "idade": 16  # Menor de idade
        },
        {
            "nome": "Pedro Santos",
            "email": "pedro@empresa.com.br",
            "senha": "P3dr0#2024!",
            "idade": 28
        },
        {
            "nome": "Ana Costa",
            "email": "ana@email",  # Email inválido
            "senha": "SenhaForte@99",
            "idade": 25
        }
    ]
    
    print("📝 Processando cadastros:")
    for i, dados in enumerate(usuarios_teste, 1):
        print(f"\n{i}. Tentativa de cadastro:")
        print(f"   Nome: {dados['nome']}")
        print(f"   Email: {dados['email']}")
        print(f"   Idade: {dados['idade']}")
        
        sucesso = gerenciador.cadastrar_usuario(dados)
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        print(f"   Status: {status}")
    
    # Mostrar usuários cadastrados
    print(f"\n👥 Usuários cadastrados: {len(gerenciador.usuarios)}")
    for usuario in gerenciador.usuarios:
        print(f"   • {usuario}")
    
    # Mostrar estatísticas
    print(f"\n📊 Estatísticas de Validação:")
    stats = gerenciador.obter_estatisticas_validacao()
    for campo, valor in stats.items():
        print(f"   {campo}: {valor}")


def testar_validacoes_individuais():
    """
    Demonstra testabilidade individual das validações.
    """
    print("\n=== TESTES UNITÁRIOS DAS VALIDAÇÕES ===\n")
    
    # Teste de email
    print("🧪 Teste Validação de Email:")
    emails_teste = [
        ("joao@email.com", True),
        ("maria.silva@empresa.com.br", True),
        ("teste@dominio", False),
        ("@dominio.com", False),
        ("", False),
        ("email.sem.arroba.com", False)
    ]
    
    for email, esperado in emails_teste:
        usuario = Usuario("Test", email, "TempPass@123", 25)
        resultado = usuario.validar_email()
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} '{email}' → {resultado} (esperado: {esperado})")
    
    # Teste de senha
    print("\n🧪 Teste Validação de Senha:")
    senhas_teste = [
        ("MinhaSenh@123", True),
        ("Teste#99", True),
        ("senhafraca", False),  # Sem maiúscula, número e símbolo
        ("SENHAFORTE", False),  # Sem minúscula, número e símbolo
        ("Senha123", False),    # Sem símbolo
        ("12345678", False),    # Sem letra
        ("Ab@1", False),        # Muito curta
    ]
    
    for senha, esperado in senhas_teste:
        usuario = Usuario("Test", "test@email.com", senha, 25)
        resultado = usuario.validar_senha()
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} '{senha}' → {resultado} (esperado: {esperado})")
    
    # Teste de idade
    print("\n🧪 Teste Validação de Idade:")
    idades_teste = [
        (18, True),   # Limite mínimo
        (25, True),   # Idade normal
        (120, True),  # Limite máximo
        (17, False),  # Menor de idade
        (121, False), # Muito idoso
        (0, False),   # Inválida
    ]
    
    for idade, esperado in idades_teste:
        usuario = Usuario("Test", "test@email.com", "TempPass@123", idade)
        resultado = usuario.validar_idade()
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} {idade} anos → {resultado} (esperado: {esperado})")


def demonstrar_encapsulamento():
    """
    Demonstra como o encapsulamento melhorou após Move Method.
    """
    print("\n=== DEMONSTRAÇÃO: Melhoria do Encapsulamento ===\n")
    
    print("📦 Criando usuário diretamente:")
    usuario = Usuario("Maria Santos", "maria@empresa.com", "Maria#2024!", 32)
    
    print(f"   Usuário: {usuario}")
    print(f"   Email válido: {usuario.validar_email()}")
    print(f"   Senha válida: {usuario.validar_senha()}")
    
    print("\n🔍 Detalhes completos de validação:")
    detalhes = usuario.obter_detalhes_validacao()
    for campo, valido in detalhes.items():
        status = "✅" if valido else "❌"
        print(f"   {status} {campo}: {valido}")
    
    print("\n🎯 Validação completa:")
    resultado = usuario.validar_completo()
    print(f"   Válido: {resultado['valido']}")
    if resultado['erros']:
        print(f"   Erros: {resultado['erros']}")
    else:
        print("   ✅ Todos os dados são válidos!")


if __name__ == "__main__":
    demonstrar_refatoracao()
    testar_validacoes_individuais()
    demonstrar_encapsulamento()
    
    print("\n🎯 BENEFÍCIOS DA REFATORAÇÃO (Move Method):")
    print("✅ Feature Envy eliminado - métodos movidos para classe correta")
    print("✅ Coesão melhorada - dados e validações juntos na classe Usuario")
    print("✅ Testabilidade individual - cada validação testável isoladamente")
    print("✅ Reutilização - validações podem ser usadas fora do gerenciador")
    print("✅ Encapsulamento adequado - responsabilidades bem definidas")
    print("✅ Interface pública preservada - compatibilidade mantida")
