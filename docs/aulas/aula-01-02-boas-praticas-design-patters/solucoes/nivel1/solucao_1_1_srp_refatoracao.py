#!/usr/bin/env python3
"""
Solução do Exercício 1.1: Refatoração SRP - Sistema de Usuário

OBJETIVO: Demonstrar a aplicação do Single Responsibility Principle (SRP)
refatorando uma classe que viola este princípio.

CONCEITOS DEMONSTRADOS:
- Single Responsibility Principle (SRP)
- Dependency Injection
- Separation of Concerns
- Type Hints
- Protocol-based interfaces

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from typing import Protocol
from datetime import datetime
from abc import ABC, abstractmethod


# =============================================================================
# PROBLEMA ORIGINAL - CÓDIGO QUE VIOLA SRP
# =============================================================================

class Usuario_Problemático:
    """
    ❌ PROBLEMA: Esta classe viola o SRP ao ter múltiplas responsabilidades:
    1. Gerenciar dados do usuário
    2. Autenticar usuários  
    3. Enviar emails
    4. Fazer logging
    5. Validar emails
    6. Criptografar senhas
    
    Consequências:
    - Difícil de testar (muitas dependências)
    - Difícil de manter (mudanças em uma área afetam outras)
    - Violação do princípio de responsabilidade única
    - Alto acoplamento
    """
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.logado = False
    
    def fazer_login(self, email, senha):
        if self.email == email and self.senha == senha:
            self.logado = True
            self.enviar_email_boas_vindas()
            self.salvar_log_login()
            return True
        return False
    
    def enviar_email_boas_vindas(self):
        print(f"Enviando email de boas-vindas para {self.email}")
    
    def salvar_log_login(self):
        print(f"Salvando log: {self.nome} fez login em {self._obter_timestamp()}")
    
    def _obter_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validar_email(self, email):
        return "@" in email and "." in email.split("@")[1]
    
    def criptografar_senha(self, senha):
        return f"cripto_{senha}"


# =============================================================================
# SOLUÇÃO REFATORADA - APLICANDO SRP
# =============================================================================

# 1. INTERFACES (usando Protocol para maior flexibilidade)
# -----------------------------------------------------------------------------

class ValidadorEmail(Protocol):
    """Interface para validação de email (ISP)"""
    
    def validar(self, email: str) -> bool:
        """Valida formato do email"""
        ...


class ServicoEmail(Protocol):
    """Interface para serviços de email (ISP)"""
    
    def enviar_boas_vindas(self, destinatario: str, nome: str) -> bool:
        """Envia email de boas-vindas"""
        ...


class LoggerSistema(Protocol):
    """Interface para logging do sistema (ISP)"""
    
    def registrar_evento(self, evento: str, detalhes: str) -> None:
        """Registra evento no sistema"""
        ...


class CriptografadorSenha(Protocol):
    """Interface para criptografia de senhas (ISP)"""
    
    def criptografar(self, senha: str) -> str:
        """Criptografa senha"""
        ...
    
    def verificar(self, senha: str, hash_senha: str) -> bool:
        """Verifica se senha corresponde ao hash"""
        ...


# 2. IMPLEMENTAÇÕES CONCRETAS (Cada uma com responsabilidade única)
# -----------------------------------------------------------------------------

class ValidadorEmailImpl:
    """
    ✅ RESPONSABILIDADE ÚNICA: Validar formato de emails
    
    BENEFÍCIOS:
    - Fácil de testar
    - Pode ser reutilizada
    - Fácil de modificar regras de validação
    """
    
    def validar(self, email: str) -> bool:
        """
        Valida formato básico do email.
        
        Args:
            email: String com email a ser validado
            
        Returns:
            bool: True se email é válido, False caso contrário
            
        Examples:
            >>> validador = ValidadorEmailImpl()
            >>> validador.validar("teste@email.com")
            True
            >>> validador.validar("email_invalido")
            False
        """
        if not email or "@" not in email:
            return False
        
        partes = email.split("@")
        if len(partes) != 2:
            return False
            
        local, dominio = partes
        if not local or not dominio:
            return False
            
        return "." in dominio


class ServicoEmailImpl:
    """
    ✅ RESPONSABILIDADE ÚNICA: Enviar emails
    
    BENEFÍCIOS:
    - Pode ser substituída por implementação real (SendGrid, AWS SES)
    - Fácil de mockar em testes
    - Configuração centralizada
    """
    
    def __init__(self, servidor_smtp: str = "localhost"):
        self._servidor_smtp = servidor_smtp
    
    def enviar_boas_vindas(self, destinatario: str, nome: str) -> bool:
        """
        Envia email de boas-vindas para novo usuário.
        
        Args:
            destinatario: Email do destinatário
            nome: Nome do usuário
            
        Returns:
            bool: True se email foi enviado com sucesso
        """
        # Simulação de envio de email
        # Em ambiente real, aqui teria integração com provedor de email
        mensagem = f"Bem-vindo(a) {nome}! Seu cadastro foi realizado com sucesso."
        
        print(f"📧 [EMAIL] Para: {destinatario}")
        print(f"📧 [EMAIL] Assunto: Bem-vindo!")
        print(f"📧 [EMAIL] Corpo: {mensagem}")
        print(f"📧 [EMAIL] Servidor: {self._servidor_smtp}")
        
        # Simular sucesso
        return True


class LoggerSistemaImpl:
    """
    ✅ RESPONSABILIDADE ÚNICA: Registrar eventos do sistema
    
    BENEFÍCIOS:
    - Centraliza estratégia de logging
    - Pode ser configurado para diferentes níveis
    - Fácil de integrar com sistemas externos
    """
    
    def __init__(self, arquivo_log: str = "sistema.log"):
        self._arquivo_log = arquivo_log
    
    def registrar_evento(self, evento: str, detalhes: str) -> None:
        """
        Registra evento no sistema de log.
        
        Args:
            evento: Tipo do evento (ex: 'LOGIN', 'ERRO', 'INFO')
            detalhes: Detalhes específicos do evento
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_log = f"[{timestamp}] {evento}: {detalhes}"
        
        # Em ambiente real, escreveria no arquivo
        print(f"📋 [LOG] {entrada_log}")
        
        # Simular escrita no arquivo
        # with open(self._arquivo_log, 'a') as f:
        #     f.write(entrada_log + '\n')


class CriptografadorSenhaImpl:
    """
    ✅ RESPONSABILIDADE ÚNICA: Criptografar e verificar senhas
    
    BENEFÍCIOS:
    - Algoritmo de hash centralizado
    - Fácil de trocar algoritmo (bcrypt, argon2, etc.)
    - Validação de senhas segura
    """
    
    def __init__(self, algoritmo: str = "sha256"):
        self._algoritmo = algoritmo
    
    def criptografar(self, senha: str) -> str:
        """
        Criptografa senha usando algoritmo configurado.
        
        Args:
            senha: Senha em texto plano
            
        Returns:
            str: Hash da senha
        """
        # Simulação simples - em produção usaria bcrypt ou similar
        import hashlib
        
        # Adicionar salt para segurança
        salt = "sistema_seguro_2024"
        senha_com_salt = f"{senha}{salt}"
        
        hash_objeto = hashlib.sha256(senha_com_salt.encode())
        return hash_objeto.hexdigest()
    
    def verificar(self, senha: str, hash_senha: str) -> bool:
        """
        Verifica se senha corresponde ao hash armazenado.
        
        Args:
            senha: Senha em texto plano
            hash_senha: Hash armazenado
            
        Returns:
            bool: True se senha é válida
        """
        hash_calculado = self.criptografar(senha)
        return hash_calculado == hash_senha


# 3. CLASSE USUARIO REFATORADA (Apenas dados e identidade)
# -----------------------------------------------------------------------------

class Usuario:
    """
    ✅ RESPONSABILIDADE ÚNICA: Representar dados de um usuário
    
    BENEFÍCIOS:
    - Classe simples e focada
    - Fácil de testar
    - Sem dependências externas
    - Imutabilidade dos dados essenciais
    """
    
    def __init__(self, nome: str, email: str, senha_hash: str):
        """
        Inicializa usuário com dados validados.
        
        Args:
            nome: Nome completo do usuário
            email: Email do usuário (deve ser validado externamente)
            senha_hash: Hash da senha (deve ser criptografada externamente)
        """
        if not nome or not email or not senha_hash:
            raise ValueError("Nome, email e senha são obrigatórios")
        
        self._nome = nome
        self._email = email  
        self._senha_hash = senha_hash
        self._logado = False
        self._data_criacao = datetime.now()
    
    @property
    def nome(self) -> str:
        """Nome do usuário (read-only)"""
        return self._nome
    
    @property  
    def email(self) -> str:
        """Email do usuário (read-only)"""
        return self._email
    
    @property
    def senha_hash(self) -> str:
        """Hash da senha (read-only)"""
        return self._senha_hash
    
    @property
    def logado(self) -> bool:
        """Status de login atual"""
        return self._logado
    
    @property
    def data_criacao(self) -> datetime:
        """Data de criação do usuário"""
        return self._data_criacao
    
    def marcar_como_logado(self) -> None:
        """Marca usuário como logado (uso interno do autenticador)"""
        self._logado = True
    
    def marcar_como_deslogado(self) -> None:
        """Marca usuário como deslogado"""
        self._logado = False
    
    def __str__(self) -> str:
        """Representação string do usuário"""
        status = "Logado" if self._logado else "Deslogado"
        return f"Usuario(nome='{self._nome}', email='{self._email}', status='{status}')"
    
    def __repr__(self) -> str:
        """Representação técnica do usuário"""
        return (f"Usuario(nome='{self._nome}', email='{self._email}', "
                f"criado_em='{self._data_criacao.isoformat()}')")


# 4. AUTENTICADOR (Orquestra o processo de login)
# -----------------------------------------------------------------------------

class AutenticadorUsuario:
    """
    ✅ RESPONSABILIDADE ÚNICA: Orquestrar processo de autenticação
    
    BENEFÍCIOS:
    - Coordena diferentes serviços
    - Dependency Injection facilita testes
    - Lógica de autenticação centralizada
    - Fácil de estender com novos requisitos
    """
    
    def __init__(self, 
                 validador_email: ValidadorEmail,
                 servico_email: ServicoEmail,
                 logger: LoggerSistema,
                 criptografador: CriptografadorSenha):
        """
        Inicializa autenticador com dependências injetadas.
        
        Args:
            validador_email: Serviço para validação de emails
            servico_email: Serviço para envio de emails  
            logger: Serviço para logging de eventos
            criptografador: Serviço para verificação de senhas
        """
        self._validador_email = validador_email
        self._servico_email = servico_email
        self._logger = logger
        self._criptografador = criptografador
    
    def criar_usuario(self, nome: str, email: str, senha: str) -> Usuario:
        """
        Cria novo usuário com validações.
        
        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            Usuario: Instância do usuário criado
            
        Raises:
            ValueError: Se dados são inválidos
        """
        # Validar email
        if not self._validador_email.validar(email):
            raise ValueError(f"Email inválido: {email}")
        
        # Criptografar senha
        senha_hash = self._criptografador.criptografar(senha)
        
        # Criar usuário
        usuario = Usuario(nome, email, senha_hash)
        
        # Registrar criação
        self._logger.registrar_evento(
            "USUARIO_CRIADO", 
            f"Usuário criado: {nome} ({email})"
        )
        
        return usuario
    
    def fazer_login(self, usuario: Usuario, email: str, senha: str) -> bool:
        """
        Executa processo de login completo.
        
        Args:
            usuario: Instância do usuário
            email: Email fornecido para login
            senha: Senha em texto plano
            
        Returns:
            bool: True se login foi bem-sucedido
        """
        try:
            # Verificar se email corresponde
            if usuario.email != email:
                self._logger.registrar_evento(
                    "LOGIN_FALHOU", 
                    f"Email incorreto para usuário: {email}"
                )
                return False
            
            # Verificar senha
            if not self._criptografador.verificar(senha, usuario.senha_hash):
                self._logger.registrar_evento(
                    "LOGIN_FALHOU", 
                    f"Senha incorreta para usuário: {email}"
                )
                return False
            
            # Login bem-sucedido
            usuario.marcar_como_logado()
            
            # Enviar email de boas-vindas
            email_enviado = self._servico_email.enviar_boas_vindas(
                usuario.email, 
                usuario.nome
            )
            
            # Registrar login
            detalhes = f"Login bem-sucedido: {usuario.nome} ({usuario.email})"
            if email_enviado:
                detalhes += " - Email de boas-vindas enviado"
            
            self._logger.registrar_evento("LOGIN_SUCESSO", detalhes)
            
            return True
            
        except Exception as e:
            # Log de erro
            self._logger.registrar_evento(
                "LOGIN_ERRO", 
                f"Erro durante login de {email}: {str(e)}"
            )
            return False


# =============================================================================
# EXEMPLO DE USO - DEMONSTRAÇÃO DA SOLUÇÃO
# =============================================================================

def demonstrar_solucao():
    """
    Demonstra o uso da solução refatorada aplicando SRP.
    
    BENEFÍCIOS EVIDENCIADOS:
    1. Cada classe tem responsabilidade única
    2. Fácil de testar (dependências injetadas)
    3. Fácil de estender (novos validadores, serviços, etc.)
    4. Baixo acoplamento entre componentes
    """
    
    print("🔧 DEMONSTRAÇÃO: Sistema de Usuário Refatorado (SRP)")
    print("=" * 60)
    
    # 1. Configurar dependências (Dependency Injection)
    print("\n📦 1. Configurando dependências...")
    validador = ValidadorEmailImpl()
    servico_email = ServicoEmailImpl("smtp.empresa.com")
    logger = LoggerSistemaImpl("app.log")
    criptografador = CriptografadorSenhaImpl("sha256")
    
    # 2. Criar autenticador
    print("\n🔐 2. Criando autenticador...")
    autenticador = AutenticadorUsuario(
        validador_email=validador,
        servico_email=servico_email,
        logger=logger,
        criptografador=criptografador
    )
    
    # 3. Criar usuário
    print("\n👤 3. Criando usuário...")
    try:
        usuario = autenticador.criar_usuario(
            nome="João Silva",
            email="joao@email.com", 
            senha="minhasenha123"
        )
        print(f"✅ Usuário criado: {usuario}")
        
    except ValueError as e:
        print(f"❌ Erro na criação: {e}")
        return
    
    # 4. Fazer login com credenciais corretas
    print("\n🔑 4. Fazendo login com credenciais corretas...")
    sucesso = autenticador.fazer_login(
        usuario=usuario,
        email="joao@email.com",
        senha="minhasenha123"
    )
    
    if sucesso:
        print(f"✅ Login bem-sucedido! Status: {usuario}")
    else:
        print("❌ Login falhou!")
    
    # 5. Tentar login com credenciais incorretas
    print("\n🚫 5. Tentando login com senha incorreta...")
    usuario.marcar_como_deslogado()  # Reset para teste
    
    sucesso = autenticador.fazer_login(
        usuario=usuario,
        email="joao@email.com", 
        senha="senha_errada"
    )
    
    if sucesso:
        print("❌ ERRO: Login deveria ter falhado!")
    else:
        print("✅ Login falhou corretamente (senha incorreta)")
    
    print("\n📊 6. Análise da Refatoração:")
    print("   ✅ SRP: Cada classe tem responsabilidade única")
    print("   ✅ DIP: Dependências injetadas via interfaces")
    print("   ✅ ISP: Interfaces específicas e coesas")
    print("   ✅ Testabilidade: Fácil de mockar dependências")
    print("   ✅ Manutenibilidade: Mudanças isoladas por responsabilidade")


# =============================================================================
# TESTES AUTOMATIZADOS
# =============================================================================

def executar_testes():
    """
    Executa testes básicos para validar a implementação.
    
    NOTA: Em um projeto real, estes estariam em arquivos separados
    usando pytest ou unittest.
    """
    
    print("\n🧪 EXECUTANDO TESTES...")
    print("=" * 40)
    
    # Setup
    validador = ValidadorEmailImpl()
    servico_email = ServicoEmailImpl()
    logger = LoggerSistemaImpl()
    criptografador = CriptografadorSenhaImpl()
    
    autenticador = AutenticadorUsuario(
        validador, servico_email, logger, criptografador
    )
    
    # Teste 1: Validação de email
    print("\n🔍 Teste 1: Validação de email...")
    assert validador.validar("teste@email.com") == True
    assert validador.validar("email_invalido") == False
    assert validador.validar("") == False
    print("✅ Validação de email: PASSOU")
    
    # Teste 2: Criptografia de senha
    print("\n🔒 Teste 2: Criptografia de senha...")
    senha = "teste123"
    hash_senha = criptografador.criptografar(senha)
    assert criptografador.verificar(senha, hash_senha) == True
    assert criptografador.verificar("senha_errada", hash_senha) == False
    print("✅ Criptografia de senha: PASSOU")
    
    # Teste 3: Criação de usuário
    print("\n👤 Teste 3: Criação de usuário...")
    usuario = autenticador.criar_usuario("Test User", "test@email.com", "senha123")
    assert usuario.nome == "Test User"
    assert usuario.email == "test@email.com"
    assert not usuario.logado
    print("✅ Criação de usuário: PASSOU")
    
    # Teste 4: Login bem-sucedido
    print("\n🔑 Teste 4: Login bem-sucedido...")
    sucesso = autenticador.fazer_login(usuario, "test@email.com", "senha123")
    assert sucesso == True
    assert usuario.logado == True
    print("✅ Login bem-sucedido: PASSOU")
    
    # Teste 5: Login com credenciais incorretas
    print("\n🚫 Teste 5: Login com credenciais incorretas...")
    usuario.marcar_como_deslogado()
    sucesso = autenticador.fazer_login(usuario, "test@email.com", "senha_errada")
    assert sucesso == False
    assert usuario.logado == False
    print("✅ Login com credenciais incorretas: PASSOU")
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Demonstrar a solução
    demonstrar_solucao()
    
    # Executar testes
    executar_testes()
    
    print("\n" + "=" * 60)
    print("📚 ANÁLISE DA REFATORAÇÃO:")
    print()
    print("ANTES (Código Problemático):")
    print("❌ Uma classe com 6+ responsabilidades")
    print("❌ Alto acoplamento")
    print("❌ Difícil de testar")
    print("❌ Difícil de manter")
    print()
    print("DEPOIS (Código Refatorado):")
    print("✅ Cada classe com responsabilidade única (SRP)")
    print("✅ Dependências injetadas (DIP)")
    print("✅ Interfaces específicas (ISP)")
    print("✅ Fácil de testar e manter")
    print("✅ Baixo acoplamento")
    print("✅ Extensibilidade sem modificação (OCP)")
    print()
    print("🎯 RESULTADO: Código mais limpo, testável e manutenível!")
