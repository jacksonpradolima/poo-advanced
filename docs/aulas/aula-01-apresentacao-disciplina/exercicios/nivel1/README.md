# 🔵 Exercícios Nível 1 - Básico

## Exercício 1.1: Refatoração SRP - Sistema de Usuário (15 min)

### 📋 Descrição
Você recebeu uma classe `Usuario` que claramente viola o **Single Responsibility Principle (SRP)**. Sua tarefa é refatorá-la aplicando SRP e outras boas práticas.

### 💻 Código Base Problemático

```python
class Usuario:
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
        # Simulação de envio de email
    
    def salvar_log_login(self):
        print(f"Salvando log: {self.nome} fez login em {self._obter_timestamp()}")
        # Simulação de salvamento no banco
    
    def _obter_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validar_email(self, email):
        return "@" in email and "." in email.split("@")[1]
    
    def criptografar_senha(self, senha):
        # Simulação de criptografia
        return f"cripto_{senha}"
```

### 🎯 Objetivos
1. **Identificar violações de SRP** na classe original
2. **Extrair responsabilidades** em classes separadas
3. **Aplicar dependency injection** quando apropriado
4. **Manter funcionalidade** sem quebrar contratos

### ✅ Requisitos da Solução

#### **Requisitos Funcionais:**
- O sistema deve permitir login de usuários
- Envio de email deve ocorrer após login bem-sucedido
- Logs de login devem ser registrados
- Validação de email deve ser mantida

#### **Requisitos Técnicos:**
- Cada classe deve ter **uma única responsabilidade**
- Use **type hints** em todos os métodos
- Implemente **injeção de dependência** para serviços externos
- Mantenha **interfaces consistentes**

#### **Restrições:**
- Apenas bibliotecas padrão do Python
- Não altere a interface pública do login
- Preserve funcionalidade de validação

### 🔧 Estrutura Sugerida

Considere extrair as seguintes responsabilidades:
- `Usuario`: Dados e identidade do usuário
- `ValidadorEmail`: Validação de formato de email
- `ServicoEmail`: Envio de notificações
- `LoggerSistema`: Registro de eventos
- `AutenticadorUsuario`: Lógica de autenticação

### 💡 Dicas de Implementação

1. **Comece identificando responsabilidades:** Liste todas as funções que a classe atual executa
2. **Crie interfaces abstratas:** Use `Protocol` ou `ABC` para definir contratos
3. **Implemente injeção de dependência:** Passe serviços pelo construtor
4. **Teste incrementalmente:** Valide cada extração de responsabilidade

### 📝 Exemplo de Uso Esperado

```python
# Configuração das dependências
validador = ValidadorEmail()
servico_email = ServicoEmail()
logger = LoggerSistema()
autenticador = AutenticadorUsuario(validador, servico_email, logger)

# Criação do usuário
usuario = Usuario("João Silva", "joao@email.com", "senha123")

# Login (deve manter a mesma interface)
sucesso = autenticador.fazer_login(usuario, "joao@email.com", "senha123")
print(f"Login {'bem-sucedido' if sucesso else 'falhou'}")
```

### 🧪 Casos de Teste

Sua solução deve passar nos seguintes cenários:

```python
def test_login_com_credenciais_validas():
    # Deve retornar True e executar ações secundárias
    pass

def test_login_com_credenciais_invalidas():
    # Deve retornar False sem executar ações secundárias
    pass

def test_validacao_email_formato_invalido():
    # Deve rejeitar emails malformados
    pass

def test_cada_classe_tem_responsabilidade_unica():
    # Verificar se classes não violam SRP
    pass
```

---

## Exercício 1.2: Implementação de Interface Segregation (20 min)

### 📋 Descrição
Implemente o **Interface Segregation Principle (ISP)** criando um sistema de diferentes tipos de funcionários com interfaces específicas.

### 🎯 Objetivo
Criar interfaces segregadas para diferentes papéis de funcionários em uma empresa, evitando que implementações sejam forçadas a depender de métodos desnecessários.

### 📋 Requisitos

#### **Tipos de Funcionários:**
1. **Desenvolvedor**: Pode programar e revisar código
2. **Designer**: Pode criar designs e usar ferramentas de design
3. **Gerente**: Pode gerenciar equipe e aprovar projetos
4. **Full Stack**: Pode programar, revisar código E criar designs

#### **Requisitos Funcionais:**
- Cada funcionário deve implementar apenas interfaces relevantes ao seu papel
- Deve ser possível adicionar novos tipos sem modificar interfaces existentes
- Sistema deve permitir que um funcionário tenha múltiplos papéis

#### **Requisitos Técnicos:**
- Use `Protocol` para definir interfaces
- Implemente todas as classes de funcionários
- Demonstre uso polimórfico das interfaces

### 💻 Esqueleto de Código

```python
from typing import Protocol

# TODO: Definir interfaces segregadas
class PodeProgramar(Protocol):
    def escrever_codigo(self, linguagem: str) -> str: ...
    def revisar_codigo(self, codigo: str) -> bool: ...

# TODO: Implementar outras interfaces necessárias

# TODO: Implementar classes de funcionários

# Exemplo de uso esperado:
def processar_funcionario_programador(funcionario: PodeProgramar):
    codigo = funcionario.escrever_codigo("Python")
    funcionario.revisar_codigo(codigo)

def processar_funcionario_designer(funcionario: "PodeDesignar"):
    design = funcionario.criar_design("Logo")
    funcionario.usar_ferramenta_design("Figma")
```

### ✅ Critérios de Sucesso
- [ ] Interfaces são específicas e coesas
- [ ] Nenhuma classe implementa métodos desnecessários
- [ ] FullStack demonstra herança múltipla de interfaces
- [ ] Código demonstra uso polimórfico

---

## Exercício 1.3: Aplicação Básica do Strategy Pattern (25 min)

### 📋 Descrição
Implemente o **Strategy Pattern** para um sistema de cálculo de desconto em uma loja online.

### 🎯 Cenário
Uma loja online precisa aplicar diferentes estratégias de desconto baseadas no tipo de cliente:
- **Cliente Regular**: 5% de desconto
- **Cliente VIP**: 15% de desconto
- **Cliente Funcionário**: 20% de desconto
- **Sem Desconto**: 0% de desconto

### 📋 Requisitos

#### **Requisitos Funcionais:**
- Calcular preço final aplicando estratégia de desconto
- Permitir mudança de estratégia em tempo de execução
- Adicionar novas estratégias sem modificar código existente

#### **Requisitos Técnicos:**
- Implemente interface `EstrategiaDesconto`
- Crie pelo menos 4 estratégias concretas
- Use `Decimal` para cálculos monetários precisos
- Demonstre mudança de estratégia em runtime

### 💻 Código Base

```python
from decimal import Decimal
from typing import Protocol

class EstrategiaDesconto(Protocol):
    def calcular_desconto(self, valor_original: Decimal) -> Decimal:
        """Retorna o valor do desconto a ser aplicado"""
        ...

# TODO: Implementar estratégias concretas

class CalculadoraPreco:
    def __init__(self, estrategia: EstrategiaDesconto):
        self._estrategia = estrategia
    
    def definir_estrategia(self, estrategia: EstrategiaDesconto) -> None:
        """Permite trocar estratégia em tempo de execução"""
        self._estrategia = estrategia
    
    def calcular_preco_final(self, valor_original: Decimal) -> Decimal:
        """Calcula preço final aplicando desconto da estratégia atual"""
        # TODO: Implementar cálculo usando estratégia
        pass

# Exemplo de uso esperado:
def exemplo_uso():
    produto_valor = Decimal("100.00")
    
    # Cliente regular
    calculadora = CalculadoraPreco(DescontoClienteRegular())
    preco_regular = calculadora.calcular_preco_final(produto_valor)
    
    # Mudança para cliente VIP
    calculadora.definir_estrategia(DescontoClienteVIP())
    preco_vip = calculadora.calcular_preco_final(produto_valor)
    
    print(f"Preço regular: R$ {preco_regular}")
    print(f"Preço VIP: R$ {preco_vip}")
```

### 🧪 Casos de Teste Obrigatórios

```python
def test_desconto_cliente_regular():
    # Deve aplicar 5% de desconto
    assert desconto == Decimal("5.00")

def test_desconto_cliente_vip():
    # Deve aplicar 15% de desconto
    assert desconto == Decimal("15.00")

def test_mudanca_estrategia_runtime():
    # Deve alterar comportamento sem quebrar
    pass

def test_sem_desconto():
    # Deve retornar valor original
    pass
```

### 💡 Dicas de Implementação
1. Use `Decimal` para evitar problemas de ponto flutuante
2. Valide valores negativos e casos extremos
3. Considere usar `Enum` para tipos de cliente
4. Implemente `__str__` nas estratégias para debugging

---

## 📊 Resumo do Nível 1

Ao completar estes exercícios, você terá praticado:

✅ **Single Responsibility Principle (SRP)**
✅ **Interface Segregation Principle (ISP)**  
✅ **Strategy Pattern**
✅ **Dependency Injection**
✅ **Type Hints e Protocols**

### 🎯 Próximos Passos
Após dominar estes conceitos, avance para o **[Nível 2](../nivel2/README.md)** onde você integrará múltiplos padrões em sistemas mais complexos.

---

**⏱️ Tempo estimado total: 60 minutos**
**🎖️ Nível de dificuldade: Básico**
**📚 Conceitos cobertos: SRP, ISP, Strategy, Dependency Injection**
