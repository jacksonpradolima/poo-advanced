# 🔴 Nível 3 - Exercícios Avançados

## Exercício 3.1: Sistema de E-commerce - Refatoração Arquitetural Completa

### Contexto e Motivação

Você foi contratado como Arquiteto de Software para modernizar o sistema de e-commerce de uma grande empresa. O sistema atual possui mais de 100.000 linhas de código, múltiplos code smells críticos e dificuldades sérias de manutenibilidade. A empresa quer migrar para microserviços e implementar integração completa com SonarCloud para monitoramento contínuo de qualidade.

### Escopo do Sistema

O sistema atual inclui:
- **Gestão de Produtos** (catálogo, estoque, preços)
- **Gestão de Usuários** (cadastro, autenticação, perfis)
- **Carrinho e Checkout** (cálculos, pagamentos, impostos)
- **Pedidos e Entrega** (tracking, logística, notificações)
- **Relatórios e Analytics** (vendas, performance, dashboards)

### Código Inicial (Representativo)

```python
# ecommerce_monolith.py - Representação do sistema monolítico atual
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import hashlib
import uuid
from decimal import Decimal
from enum import Enum

class SistemaEcommerceMonolitico:
    """
    Sistema monolítico de e-commerce com múltiplos code smells críticos.
    
    PROBLEMAS ARQUITETURAIS IDENTIFICADOS:
    - God Class (1000+ linhas)
    - Tight Coupling entre módulos
    - No Separation of Concerns
    - Business Logic misturada com Data Access
    - No Dependency Injection
    - Hard-coded dependencies
    - No Event-driven architecture
    - Primitive Obsession massiva
    - Shotgun Surgery patterns
    - Inappropriate Intimacy entre classes
    """
    
    def __init__(self):
        # PROBLEMA: Tudo misturado em uma única classe
        self.produtos = []
        self.usuarios = []
        self.carrinhos = {}
        self.pedidos = []
        self.pagamentos = []
        self.estoque = {}
        self.promocoes = []
        self.configuracoes = self._carregar_configuracoes()
        self.cache = {}
        self.logs = []
        
    def processar_checkout_completo(self, usuario_id: str, dados_checkout: dict) -> dict:
        """
        MÉTODO CRÍTICO: 200+ linhas com múltiplas responsabilidades.
        
        Responsabilidades misturadas:
        1. Validação de dados
        2. Cálculo de preços  
        3. Aplicação de promoções
        4. Verificação de estoque
        5. Cálculo de impostos
        6. Processamento de pagamento
        7. Atualização de estoque
        8. Criação de pedido
        9. Envio de notificações
        10. Geração de relatórios
        11. Log de auditoria
        12. Integração com APIs externas
        """
        
        # Validação inicial (sem tratamento adequado de erro)
        if not usuario_id or not dados_checkout:
            return {"erro": "Dados incompletos"}
        
        # Buscar usuário (N+1 queries problem)
        usuario = None
        for u in self.usuarios:
            if u["id"] == usuario_id:
                usuario = u
                break
        
        if not usuario:
            return {"erro": "Usuário não encontrado"}
        
        # Buscar carrinho (code duplication)
        carrinho = self.carrinhos.get(usuario_id)
        if not carrinho or not carrinho["itens"]:
            return {"erro": "Carrinho vazio"}
        
        # Validar e calcular itens (Long Method)
        total_produtos = Decimal('0.00')
        itens_processados = []
        
        for item in carrinho["itens"]:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]
            
            # Buscar produto (N+1 problem)
            produto = None
            for p in self.produtos:
                if p["id"] == produto_id:
                    produto = p
                    break
            
            if not produto or not produto["ativo"]:
                return {"erro": f"Produto {produto_id} indisponível"}
            
            # Verificar estoque (Primitive Obsession)
            estoque_disponivel = self.estoque.get(produto_id, 0)
            if estoque_disponivel < quantidade:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            
            # Calcular preço com promoções (Feature Envy + Switch Statement)
            preco_unitario = Decimal(str(produto["preco"]))
            
            # Aplicar promoções por categoria (Switch Statement smell)
            if produto["categoria"] == "eletronicos":
                if quantidade >= 2:
                    preco_unitario *= Decimal('0.95')  # 5% desconto
            elif produto["categoria"] == "roupas":
                if quantidade >= 3:
                    preco_unitario *= Decimal('0.90')  # 10% desconto
            elif produto["categoria"] == "livros":
                if quantidade >= 5:
                    preco_unitario *= Decimal('0.85')  # 15% desconto
            
            # Verificar promoções ativas (Data Class smell)
            for promocao in self.promocoes:
                if (promocao["produto_id"] == produto_id and 
                    promocao["ativa"] and
                    datetime.now() >= datetime.fromisoformat(promocao["inicio"]) and
                    datetime.now() <= datetime.fromisoformat(promocao["fim"])):
                    
                    if promocao["tipo"] == "percentual":
                        preco_unitario *= (Decimal('1') - Decimal(str(promocao["valor"])))
                    elif promocao["tipo"] == "fixo":
                        preco_unitario -= Decimal(str(promocao["valor"]))
            
            # Calcular subtotal
            subtotal = preco_unitario * quantidade
            total_produtos += subtotal
            
            itens_processados.append({
                "produto_id": produto_id,
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preco_unitario": float(preco_unitario),
                "subtotal": float(subtotal)
            })
        
        # Calcular impostos (Hard-coded business rules)
        imposto_estadual = total_produtos * Decimal('0.18')  # 18% ICMS
        imposto_federal = total_produtos * Decimal('0.065')  # 6.5% PIS/COFINS
        total_impostos = imposto_estadual + imposto_federal
        
        # Aplicar cupons de desconto (Inappropriate Intimacy)
        cupom = dados_checkout.get("cupom_desconto")
        desconto_cupom = Decimal('0.00')
        
        if cupom:
            # Lógica complexa de cupons (deveria estar em service separado)
            if cupom == "PRIMEIRA_COMPRA":
                if len([p for p in self.pedidos if p["usuario_id"] == usuario_id]) == 0:
                    desconto_cupom = min(total_produtos * Decimal('0.1'), Decimal('100.0'))
            elif cupom == "FIDELIDADE":
                total_compras = sum(Decimal(str(p["total"])) for p in self.pedidos if p["usuario_id"] == usuario_id)
                if total_compras >= Decimal('1000.0'):
                    desconto_cupom = total_produtos * Decimal('0.15')
            elif cupom.startswith("DESC"):
                try:
                    valor_desc = Decimal(cupom.replace("DESC", ""))
                    desconto_cupom = min(valor_desc, total_produtos * Decimal('0.3'))
                except:
                    pass
        
        # Calcular frete (God Method continues...)
        endereco = dados_checkout.get("endereco_entrega", {})
        estado = endereco.get("estado", "")
        peso_total = sum(p["peso"] * item["quantidade"] for item in carrinho["itens"] 
                        for p in self.produtos if p["id"] == item["produto_id"])
        
        # Cálculo de frete baseado em região e peso (Magic Numbers)
        if estado in ["SP", "RJ"]:
            frete_base = Decimal('15.0')
        elif estado in ["MG", "ES", "SC", "PR", "RS"]:
            frete_base = Decimal('25.0')
        else:
            frete_base = Decimal('35.0')
        
        frete_peso = peso_total * Decimal('2.5')  # R$ 2.50 por kg
        frete_total = frete_base + frete_peso
        
        # Frete grátis acima de valor (Hard-coded rule)
        if total_produtos >= Decimal('99.0'):
            frete_total = Decimal('0.00')
        
        # Calcular total final
        total_final = total_produtos + total_impostos + frete_total - desconto_cupom
        
        # Processar pagamento (Tight Coupling)
        forma_pagamento = dados_checkout.get("forma_pagamento")
        dados_pagamento = dados_checkout.get("dados_pagamento", {})
        
        if forma_pagamento == "cartao_credito":
            # Simulação de integração com gateway (Hard-coded)
            numero_cartao = dados_pagamento.get("numero", "")
            if len(numero_cartao) != 16 or not numero_cartao.isdigit():
                return {"erro": "Cartão inválido"}
            
            # Taxa do cartão (Magic Number)
            taxa_cartao = total_final * Decimal('0.035')
            total_final += taxa_cartao
            
        elif forma_pagamento == "pix":
            # Desconto PIX (Hard-coded)
            desconto_pix = total_final * Decimal('0.05')
            total_final -= desconto_pix
            
        elif forma_pagamento == "boleto":
            # Sem taxa adicional, mas vencimento em 3 dias
            pass
        else:
            return {"erro": "Forma de pagamento inválida"}
        
        # Atualizar estoque (Data corruption risk)
        for item in itens_processados:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]
            self.estoque[produto_id] -= quantidade
        
        # Criar pedido (Primitive Obsession)
        pedido_id = str(uuid.uuid4())
        pedido = {
            "id": pedido_id,
            "usuario_id": usuario_id,
            "itens": itens_processados,
            "total_produtos": float(total_produtos),
            "total_impostos": float(total_impostos),
            "frete": float(frete_total),
            "desconto_cupom": float(desconto_cupom),
            "total_final": float(total_final),
            "forma_pagamento": forma_pagamento,
            "endereco_entrega": endereco,
            "status": "confirmado",
            "data_pedido": datetime.now().isoformat(),
            "estimativa_entrega": (datetime.now() + timedelta(days=5)).isoformat()
        }
        self.pedidos.append(pedido)
        
        # Limpar carrinho
        self.carrinhos[usuario_id] = {"itens": []}
        
        # Enviar notificações (Tight Coupling)
        self._enviar_email_confirmacao(usuario["email"], pedido)
        self._enviar_sms_confirmacao(usuario["telefone"], pedido_id)
        
        # Log de auditoria (Mixed responsibilities)
        self.logs.append({
            "acao": "checkout",
            "usuario_id": usuario_id,
            "pedido_id": pedido_id,
            "valor": float(total_final),
            "timestamp": datetime.now().isoformat()
        })
        
        # Atualizar analytics (God Class symptom)
        self._atualizar_analytics_vendas(pedido)
        
        return {
            "sucesso": True,
            "pedido_id": pedido_id,
            "total_final": float(total_final),
            "estimativa_entrega": "5 dias úteis"
        }
    
    def _carregar_configuracoes(self) -> dict:
        """Hard-coded configurations (should be external)."""
        return {
            "taxa_cartao": 0.035,
            "desconto_pix": 0.05,
            "frete_gratis_acima": 99.0,
            "imposto_estadual": 0.18,
            "imposto_federal": 0.065
        }
    
    def _enviar_email_confirmacao(self, email: str, pedido: dict) -> None:
        """Simulação de envio de email (Tight Coupling)."""
        print(f"Email enviado para {email} - Pedido {pedido['id']}")
    
    def _enviar_sms_confirmacao(self, telefone: str, pedido_id: str) -> None:
        """Simulação de envio de SMS (Tight Coupling)."""
        print(f"SMS enviado para {telefone} - Pedido {pedido_id}")
    
    def _atualizar_analytics_vendas(self, pedido: dict) -> None:
        """Analytics misturado com business logic (Violation of SRP)."""
        # Simulação de atualização de métricas
        pass
    
    # Mais 50+ métodos com problemas similares...
    # (adicionar_produto, buscar_produtos, gerenciar_estoque, 
    #  processar_devolucao, gerar_relatorios, etc.)

# Exemplo de uso demonstrando a complexidade
if __name__ == "__main__":
    sistema = SistemaEcommerceMonolitico()
    
    # Setup inicial complexo e propenso a erros
    # ... (código de inicialização)
    
    # Checkout que pode falhar de múltiplas formas
    resultado = sistema.processar_checkout_completo("user123", {
        "cupom_desconto": "PRIMEIRA_COMPRA",
        "forma_pagamento": "cartao_credito",
        "dados_pagamento": {"numero": "1234567812345678"},
        "endereco_entrega": {"estado": "SP", "cidade": "São Paulo"}
    })
    
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

### Requisitos de Refatoração

#### Fase 1: Análise e Planejamento (40 minutos)

1. **Code Smell Analysis:**
   - Identificar e catalogar todos os code smells presentes
   - Priorizar por impacto e dificuldade de correção
   - Documentar dependências e acoplamentos

2. **Architectural Assessment:**
   - Definir bounded contexts para microserviços
   - Identificar agregados e entidades de domínio
   - Mapear fluxos de dados críticos

3. **Refactoring Strategy:**
   - Sequência de refatorações (Strangler Fig Pattern)
   - Pontos de quebra para validação
   - Estratégia de testes para preservar comportamento

#### Fase 2: Domain Modeling e Clean Architecture (60 minutos)

1. **Domain-Driven Design:**
   - Modelar agregados: Produto, Usuario, Pedido, Pagamento
   - Definir Value Objects: Dinheiro, Endereco, Email
   - Implementar Domain Services e Repositories

2. **Clean Architecture Layers:**
   - **Domain Layer:** Entidades, Value Objects, Domain Services
   - **Application Layer:** Use Cases, DTOs, Interfaces
   - **Infrastructure Layer:** Repositories, External Services
   - **Presentation Layer:** Controllers, Mappers

3. **Design Patterns Application:**
   - **Strategy:** Diferentes formas de pagamento e frete
   - **Factory:** Criação de entidades complexas
   - **Observer:** Eventos de domínio
   - **Command:** Operações transacionais
   - **Repository:** Acesso a dados

#### Fase 3: Microservices Architecture (45 minutos)

1. **Service Decomposition:**
   - **Product Service:** Catálogo, estoque, preços
   - **User Service:** Autenticação, perfis, preferências
   - **Order Service:** Carrinho, checkout, pedidos
   - **Payment Service:** Processamento, validação, reconciliação
   - **Notification Service:** Email, SMS, push notifications

2. **Inter-service Communication:**
   - **Synchronous:** REST APIs para consultas
   - **Asynchronous:** Event-driven para comandos
   - **Data Consistency:** Saga Pattern para transações distribuídas

3. **Infrastructure Patterns:**
   - **API Gateway:** Roteamento e autenticação
   - **Service Registry:** Descoberta de serviços
   - **Circuit Breaker:** Resiliência e tolerância a falhas

#### Fase 4: SonarCloud Integration (25 minutos)

1. **Quality Gates Configuration:**
   - Métricas de cobertura mínima (85%)
   - Complexidade ciclomática máxima (10)
   - Duplicação de código máxima (3%)
   - Debt ratio máximo (5%)

2. **CI/CD Pipeline:**
   - Análise automática em cada commit
   - Bloqueio de merge com quality gates
   - Relatórios de tendência de qualidade

3. **Custom Rules:**
   - Regras específicas para padrões da empresa
   - Detecção de anti-patterns arquiteturais
   - Validação de convenções de naming

### Arquitetura Final Esperada

```python
# Estrutura esperada após refatoração completa

# Domain Layer
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Dinheiro:
    """Value Object para valores monetários."""
    valor: Decimal
    moeda: str = "BRL"
    
    def somar(self, outro: 'Dinheiro') -> 'Dinheiro':
        if self.moeda != outro.moeda:
            raise ValueError("Moedas diferentes")
        return Dinheiro(self.valor + outro.valor, self.moeda)

class Produto:
    """Entidade do domínio Produto."""
    def __init__(self, id: UUID, nome: str, preco: Dinheiro):
        self._id = id
        self._nome = nome
        self._preco = preco
    
    def aplicar_desconto(self, percentual: Decimal) -> Dinheiro:
        """Aplica desconto e retorna novo preço."""
        novo_valor = self._preco.valor * (1 - percentual)
        return Dinheiro(novo_valor, self._preco.moeda)

class CalculadoraPreco(ABC):
    """Strategy para cálculo de preços."""
    @abstractmethod
    def calcular(self, itens: List['ItemCarrinho']) -> Dinheiro:
        pass

class CalculadoraPrecoComPromocao(CalculadoraPreco):
    """Implementação com aplicação de promoções."""
    def calcular(self, itens: List['ItemCarrinho']) -> Dinheiro:
        # Implementação específica
        pass

# Application Layer
class CheckoutUseCase:
    """Use Case para processo de checkout."""
    def __init__(self, 
                 repo_pedidos: 'RepositorioPedidos',
                 calculadora_preco: CalculadoraPreco,
                 processador_pagamento: 'ProcessadorPagamento'):
        self._repo_pedidos = repo_pedidos
        self._calculadora_preco = calculadora_preco
        self._processador_pagamento = processador_pagamento
    
    def executar(self, comando: 'ComandoCheckout') -> 'ResultadoCheckout':
        # Lógica do use case isolada e testável
        pass

# Infrastructure Layer
class RepositorioPedidosSQL:
    """Implementação concreta do repositório."""
    def salvar(self, pedido: 'Pedido') -> None:
        # Implementação de persistência
        pass

# Microservices
class ProductService:
    """Microserviço de produtos."""
    def __init__(self):
        self.repository = RepositorioProdutos()
    
    async def buscar_produto(self, id: UUID) -> Optional[Produto]:
        return await self.repository.buscar_por_id(id)

class OrderService:
    """Microserviço de pedidos."""
    def __init__(self):
        self.checkout_use_case = CheckoutUseCase(
            # Dependency injection
        )
    
    async def processar_checkout(self, comando: ComandoCheckout) -> ResultadoCheckout:
        return await self.checkout_use_case.executar(comando)
```

### Critérios de Avaliação

#### Qualidade Arquitetural (40%)
- ✅ **Clean Architecture** implementada corretamente
- ✅ **Domain-Driven Design** aplicado adequadamente
- ✅ **Microservices** bem decompostos
- ✅ **Separation of Concerns** clara entre camadas
- ✅ **Dependency Inversion** aplicada consistentemente

#### Code Quality (30%)
- ✅ **Code Smells eliminados** (mínimo 90%)
- ✅ **Design Patterns** aplicados apropriadamente
- ✅ **SOLID Principles** respeitados
- ✅ **Testabilidade** alta (> 85% cobertura)
- ✅ **Complexidade** reduzida (< 10 por método)

#### SonarCloud Integration (20%)
- ✅ **Quality Gates** configurados e funcionando
- ✅ **CI/CD Pipeline** implementado
- ✅ **Métricas** tracking adequado
- ✅ **Custom Rules** para padrões específicos

#### Documentation & Process (10%)
- ✅ **Documentação** arquitetural completa
- ✅ **ADRs** (Architecture Decision Records)
- ✅ **Migration Strategy** detalhada
- ✅ **Team Guidelines** estabelecidas

### Entregáveis Esperados

1. **Código Refatorado:**
   - Estrutura completa de microserviços
   - Testes unitários e integração
   - Configuração de CI/CD

2. **Documentação:**
   - Architecture Decision Records (ADRs)
   - API Documentation (OpenAPI)
   - Deployment Guide

3. **Configurações:**
   - SonarCloud project setup
   - Quality gates configuration
   - Pipeline definitions (.github/workflows)

4. **Métricas Demonstradas:**
   - Before/After code quality comparison
   - Performance benchmarks
   - Maintenance effort reduction estimates

---

## Exercício 3.2: Sistema Bancário - Event Sourcing e CQRS

### Contexto e Motivação

Um banco digital em crescimento precisa modernizar seu sistema core banking para suportar milhões de transações diárias, auditoria completa e compliance regulatório. O sistema atual não consegue rastrear adequadamente o histórico de mudanças e possui problemas de performance em consultas complexas.

### Escopo do Sistema

**Core Banking Features:**
- Gestão de contas correntes e poupança
- Transferências entre contas (TED, PIX, DOC)
- Cartões de crédito e débito
- Empréstimos e financiamentos
- Investimentos básicos (CDB, LCI, LCA)
- Compliance e auditoria

### Código Inicial

```python
# core_banking_legacy.py
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid

class TipoTransacao(Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque" 
    TRANSFERENCIA = "transferencia"
    PIX = "pix"
    PAGAMENTO = "pagamento"

class SistemaCoreBankingLegacy:
    """
    Sistema legacy com problemas críticos de auditoria e performance.
    
    PROBLEMAS IDENTIFICADOS:
    - No Event Sourcing (perda de histórico)
    - No CQRS (queries lentas)
    - State mutations diretas (auditoria impossível)
    - No Domain Events (integração frágil)
    - Concurrent access issues
    - No temporal queries
    - Compliance gaps
    """
    
    def __init__(self):
        self.contas = {}
        self.transacoes = []
        self.cartoes = {}
        self.emprestimos = {}
        
    def transferir_entre_contas(self, conta_origem: str, conta_destino: str, 
                               valor: Decimal, descricao: str) -> dict:
        """
        PROBLEMA CRÍTICO: Mutação de estado sem Event Sourcing.
        
        Problemas:
        1. Sem histórico de estados intermediários
        2. Impossível reconstituir estado em ponto temporal
        3. Auditoria limitada
        4. Race conditions possíveis
        5. Rollback complexo
        """
        
        # Validações básicas
        if valor <= 0:
            return {"erro": "Valor deve ser positivo"}
        
        if conta_origem == conta_destino:
            return {"erro": "Conta origem igual a destino"}
        
        # Buscar contas (State access direto)
        conta_orig = self.contas.get(conta_origem)
        conta_dest = self.contas.get(conta_destino)
        
        if not conta_orig or not conta_dest:
            return {"erro": "Conta não encontrada"}
        
        # Verificar saldo (State check)
        if conta_orig["saldo"] < valor:
            return {"erro": "Saldo insuficiente"}
        
        # MUTATION SEM EVENTO - PROBLEMA CRÍTICO
        conta_orig["saldo"] -= valor
        conta_dest["saldo"] += valor
        
        # Log simples (insuficiente para auditoria)
        transacao_id = str(uuid.uuid4())
        transacao = {
            "id": transacao_id,
            "tipo": TipoTransacao.TRANSFERENCIA.value,
            "conta_origem": conta_origem,
            "conta_destino": conta_destino,
            "valor": float(valor),
            "descricao": descricao,
            "timestamp": datetime.now().isoformat()
        }
        self.transacoes.append(transacao)
        
        return {"sucesso": True, "transacao_id": transacao_id}
    
    def consultar_extrato(self, conta: str, data_inicio: datetime, 
                         data_fim: datetime) -> List[dict]:
        """
        PROBLEMA: Query lenta sem CQRS.
        
        Issues:
        1. Scan completo da lista de transações
        2. Sem índices otimizados
        3. Sem cache para queries frequentes
        4. Sem views materializadas
        """
        extrato = []
        for transacao in self.transacoes:
            # Scan linear - O(n) complexity
            if (transacao["conta_origem"] == conta or 
                transacao["conta_destino"] == conta):
                
                trans_time = datetime.fromisoformat(transacao["timestamp"])
                if data_inicio <= trans_time <= data_fim:
                    extrato.append(transacao)
        
        return extrato
```

### Requisitos

#### Event Sourcing Implementation
1. **Event Store Design:**
   - Streams por agregado
   - Snapshot strategy
   - Event versioning
   - Idempotency guarantees

2. **Domain Events:**
   - ContaCriada, DepositoRealizado, TransferenciaIniciada
   - Event enrichment
   - Causation/correlation tracking

3. **Event Replay:**
   - Estado reconstruction
   - Temporal queries
   - Point-in-time recovery

#### CQRS Implementation
1. **Command Side:**
   - Command handlers
   - Aggregate rebuilding
   - Business rule enforcement

2. **Query Side:**
   - Read models otimizados
   - Eventual consistency
   - Multiple projections

3. **Integration:**
   - Event-driven projections
   - Saga coordination
   - External system integration

### Resultado Esperado

```python
# Event Sourcing + CQRS Implementation

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any
import asyncio

# Domain Events
@dataclass
class EventoDominio(ABC):
    """Base para todos os eventos de domínio."""
    aggregate_id: str
    version: int
    timestamp: datetime
    correlation_id: str
    causation_id: Optional[str] = None

@dataclass
class ContaCriada(EventoDominio):
    numero_conta: str
    titular: str
    tipo_conta: str

@dataclass
class DepositoRealizado(EventoDominio):
    valor: Decimal
    descricao: str

# Aggregate Root
class ContaBancaria:
    """Aggregate com Event Sourcing."""
    
    def __init__(self, eventos: List[EventoDominio] = None):
        self._eventos_nao_commitados: List[EventoDominio] = []
        self._version = 0
        
        if eventos:
            self._aplicar_eventos(eventos)
    
    def depositar(self, valor: Decimal, descricao: str) -> None:
        """Command que gera evento."""
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        
        evento = DepositoRealizado(
            aggregate_id=self.id,
            version=self._version + 1,
            timestamp=datetime.now(),
            correlation_id=str(uuid.uuid4()),
            valor=valor,
            descricao=descricao
        )
        
        self._aplicar_evento(evento)
        self._eventos_nao_commitados.append(evento)

# Event Store
class EventStore(ABC):
    @abstractmethod
    async def salvar_eventos(self, stream_id: str, 
                           eventos: List[EventoDominio], 
                           versao_esperada: int) -> None:
        pass
    
    @abstractmethod
    async def carregar_eventos(self, stream_id: str) -> List[EventoDominio]:
        pass

# Read Model
class ReadModelExtrato:
    """Read model otimizado para consultas de extrato."""
    
    def __init__(self):
        self._transacoes_por_conta = {}
        self._saldos_por_conta = {}
    
    async def handle_deposito_realizado(self, evento: DepositoRealizado) -> None:
        """Event handler para atualizar read model."""
        conta = evento.aggregate_id
        
        if conta not in self._transacoes_por_conta:
            self._transacoes_por_conta[conta] = []
        
        self._transacoes_por_conta[conta].append({
            "tipo": "deposito",
            "valor": evento.valor,
            "descricao": evento.descricao,
            "timestamp": evento.timestamp
        })
        
        self._saldos_por_conta[conta] = (
            self._saldos_por_conta.get(conta, Decimal('0')) + evento.valor
        )

# Command Handler
class DepositarCommandHandler:
    """Handler para comando de depósito."""
    
    def __init__(self, repository: 'RepositorioContaBancaria', 
                 event_bus: 'EventBus'):
        self._repository = repository
        self._event_bus = event_bus
    
    async def handle(self, comando: 'ComandoDepositar') -> None:
        conta = await self._repository.carregar(comando.conta_id)
        conta.depositar(comando.valor, comando.descricao)
        await self._repository.salvar(conta)
        
        # Publish events
        for evento in conta.eventos_nao_commitados:
            await self._event_bus.publish(evento)
```

---

## Exercício 3.3: Sistema de IoT Industrial - Real-time Processing

### Contexto e Motivação

Uma empresa de manufatura precisa modernizar seu sistema de monitoramento industrial para processar dados de milhares de sensores IoT em tempo real, detectar anomalias automaticamente e implementar manutenção preditiva usando machine learning.

### Escopo Técnico

**Volumes de Dados:**
- 10.000+ sensores simultâneos
- 100.000+ mensagens/segundo
- Latência < 100ms para alertas críticos
- 99.9% uptime requirement

### Código Inicial

```python
# iot_industrial_legacy.py
import time
import threading
from queue import Queue
from typing import Dict, List, Any
import json

class SistemaIoTLegacy:
    """
    Sistema legacy com problemas críticos de performance e escalabilidade.
    
    PROBLEMAS CRÍTICOS:
    - No real-time processing (batch only)
    - No stream processing
    - Thread-based concurrency (GIL issues)
    - No backpressure handling
    - Memory leaks com high throughput
    - No fault tolerance
    - No horizontal scaling
    """
    
    def __init__(self):
        self.sensores = {}
        self.dados_buffer = Queue(maxsize=1000)  # Buffer limitado
        self.alertas = []
        self.is_running = False
        
    def processar_dados_sensor(self, dados_sensor: dict) -> None:
        """
        PROBLEMA: Processing síncrono bloqueante.
        
        Issues:
        1. Blocking I/O operations
        2. No concurrent processing
        3. Single point of failure
        4. No error recovery
        5. Memory accumulation
        """
        
        sensor_id = dados_sensor["sensor_id"]
        timestamp = dados_sensor["timestamp"]
        valor = dados_sensor["valor"]
        
        # Processing síncrono (BLOQUEANTE)
        if self._detectar_anomalia(sensor_id, valor):
            alerta = {
                "sensor_id": sensor_id,
                "valor": valor,
                "timestamp": timestamp,
                "tipo": "anomalia_detectada"
            }
            self.alertas.append(alerta)  # Memory leak potential
            
        # Salvar dados (I/O bloqueante)
        self._salvar_dados_banco(dados_sensor)  # Synchronous DB write
        
        # Update sensor status (Race condition possible)
        self.sensores[sensor_id] = {
            "ultimo_valor": valor,
            "timestamp": timestamp
        }
    
    def _detectar_anomalia(self, sensor_id: str, valor: float) -> bool:
        """Detecção simplista sem ML."""
        # Hardcoded thresholds (não inteligente)
        if sensor_id.startswith("temp"):
            return valor > 80 or valor < -10
        elif sensor_id.startswith("pressure"):
            return valor > 100 or valor < 0
        return False
```

### Requisitos

#### Real-time Stream Processing
1. **Async Event Processing:**
   - AsyncIO-based architecture
   - Event streaming with Kafka/Redis
   - Backpressure handling
   - Circuit breaker patterns

2. **ML-based Anomaly Detection:**
   - Online learning algorithms
   - Sliding window statistics
   - Pattern recognition
   - Threshold adaptation

3. **Horizontal Scaling:**
   - Microservices architecture
   - Container orchestration
   - Load balancing
   - Auto-scaling policies

### Resultado Esperado

```python
# Real-time IoT Processing System

import asyncio
import aioredis
from typing import AsyncIterator, Protocol
from dataclasses import dataclass
import numpy as np
from collections import deque

@dataclass
class DadosSensor:
    sensor_id: str
    valor: float
    timestamp: datetime
    metadados: Dict[str, Any]

class ProcessadorStream(Protocol):
    async def processar(self, dados: DadosSensor) -> None:
        ...

class DetectorAnomaliaML:
    """Detector de anomalias usando ML online."""
    
    def __init__(self, window_size: int = 100):
        self._window_size = window_size
        self._historico: Dict[str, deque] = {}
        
    async def detectar_anomalia(self, dados: DadosSensor) -> bool:
        """Detecção usando estatística adaptativa."""
        sensor_id = dados.sensor_id
        
        if sensor_id not in self._historico:
            self._historico[sensor_id] = deque(maxlen=self._window_size)
        
        historico = self._historico[sensor_id]
        historico.append(dados.valor)
        
        if len(historico) < 10:  # Dados insuficientes
            return False
        
        # Z-score adaptativo
        media = np.mean(historico)
        std = np.std(historico)
        z_score = abs((dados.valor - media) / std) if std > 0 else 0
        
        return z_score > 3.0  # Threshold adaptativo

class ProcessadorEventosIoT:
    """Processador principal assíncrono."""
    
    def __init__(self):
        self._detector_anomalia = DetectorAnomaliaML()
        self._redis = None
        
    async def inicializar(self):
        self._redis = await aioredis.create_redis_pool('redis://localhost')
    
    async def processar_stream(self, stream: AsyncIterator[DadosSensor]) -> None:
        """Processa stream de dados de forma assíncrona."""
        async for dados in stream:
            # Processing paralelo sem bloqueio
            await asyncio.gather(
                self._processar_dados(dados),
                self._verificar_anomalias(dados),
                self._atualizar_metricas(dados)
            )
    
    async def _processar_dados(self, dados: DadosSensor) -> None:
        """Processamento principal dos dados."""
        # Async database write
        await self._salvar_dados_async(dados)
        
    async def _verificar_anomalias(self, dados: DadosSensor) -> None:
        """Verificação de anomalias em tempo real."""
        if await self._detector_anomalia.detectar_anomalia(dados):
            await self._emitir_alerta(dados)
    
    async def _emitir_alerta(self, dados: DadosSensor) -> None:
        """Emissão de alerta para downstream systems."""
        alerta = {
            "sensor_id": dados.sensor_id,
            "valor": dados.valor,
            "timestamp": dados.timestamp.isoformat(),
            "severity": "high"
        }
        
        # Publish to multiple channels
        await asyncio.gather(
            self._redis.publish("alertas:anomalias", json.dumps(alerta)),
            self._notificar_ops_team(alerta),
            self._acionar_sistema_emergencia(alerta)
        )
```

---

## Critérios de Avaliação - Nível 3

### Exercício 3.1 - E-commerce Arquitetural
- ✅ **Architectural Quality (40%):** Clean Architecture + DDD + Microservices
- ✅ **Code Quality (30%):** Eliminação completa de code smells + SOLID
- ✅ **SonarCloud Integration (20%):** Quality gates + CI/CD + métricas
- ✅ **Documentation (10%):** ADRs + API docs + migration strategy

### Exercício 3.2 - Event Sourcing Banking
- ✅ **Event Sourcing (35%):** Proper event design + replay capability
- ✅ **CQRS Implementation (35%):** Optimized read models + command handling
- ✅ **Domain Design (20%):** Aggregates + events + business rules
- ✅ **Integration (10%):** External systems + eventual consistency

### Exercício 3.3 - Real-time IoT
- ✅ **Stream Processing (40%):** AsyncIO + real-time + backpressure
- ✅ **ML Integration (30%):** Online learning + anomaly detection
- ✅ **Scalability (20%):** Horizontal scaling + performance
- ✅ **Reliability (10%):** Fault tolerance + monitoring

### Pontuação Geral
- **Excepcional (95-100%):** Arquitetura enterprise-grade + inovações
- **Avançado (85-94%):** Todos critérios + extensões significativas  
- **Proficiente (75-84%):** Critérios core bem executados
- **Em Desenvolvimento (60-74%):** Maioria dos critérios com lacunas
- **Insuficiente (<60%):** Critérios fundamentais não demonstrados

## Tempo Estimado Total: 8-12 horas

Este nível representa o ápice dos exercícios, simulando desafios reais de sistemas enterprise com milhões de usuários, requisitos de compliance e alta disponibilidade.
