# 🔴 Exercícios Nível 3 - Avançado

## Exercício 3.1: Sistema de E-commerce Completo 🛒

### Contexto
Desenvolva um sistema de e-commerce completo com carrinho de compras, processamento de pedidos, gestão de estoque, sistema de pagamentos (simulado) e dashboard administrativo. O sistema deve ser enterprise-grade com todas as práticas de desenvolvimento profissional.

### Objetivos Pedagógicos
- Arquitetura de software complexa
- Padrões de design avançados
- Integração de múltiplos domínios
- Performance e escalabilidade
- Monitoramento e observabilidade

### Requisitos Funcionais

#### Gestão de Produtos
1. **Catálogo**: Produtos, categorias, variações (tamanho, cor)
2. **Estoque**: Controle por variação, alertas de baixo estoque
3. **Pricing**: Preços dinâmicos, promoções, cupons de desconto
4. **Imagens**: Upload, redimensionamento, otimização
5. **SEO**: URLs amigáveis, metadados, sitemap

#### Sistema de Usuários
1. **Autenticação**: Registro, login, recuperação de senha
2. **Perfis**: Dados pessoais, endereços múltiplos, preferências
3. **Permissões**: Cliente, admin, vendedor, suporte
4. **Histórico**: Pedidos, visualizações, wishlist

#### Carrinho e Checkout
1. **Carrinho**: Persistente, cálculo automático, validações
2. **Checkout**: Multi-step, validação de endereço, fretes
3. **Pagamentos**: Múltiplas formas, parcelamento, validações
4. **Confirmação**: Email, SMS, PDF do pedido

#### Gestão de Pedidos
1. **Workflow**: Pendente → Pago → Preparando → Enviado → Entregue
2. **Tracking**: Códigos de rastreamento, atualizações automáticas
3. **Devoluções**: Processo automatizado, reembolsos
4. **Relatórios**: Vendas, produtos mais vendidos, análises

### Arquitetura do Sistema

```
ecommerce-platform/
├── pyproject.toml
├── README.md
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── config/
│   ├── settings.py
│   ├── database.py
│   └── redis.py
├── ecommerce/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   ├── decorators.py
│   │   └── utils.py
│   ├── domains/
│   │   ├── __init__.py
│   │   ├── produtos/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   └── schemas.py
│   │   ├── usuarios/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── auth.py
│   │   │   └── schemas.py
│   │   ├── carrinho/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── schemas.py
│   │   ├── pedidos/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── workflow.py
│   │   │   └── schemas.py
│   │   ├── pagamentos/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── gateways.py
│   │   │   └── schemas.py
│   │   └── estoque/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── services.py
│   │       └── schemas.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── produtos.py
│   │       ├── usuarios.py
│   │       ├── carrinho.py
│   │       ├── pedidos.py
│   │       └── admin.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── redis_client.py
│   │   │   └── decorators.py
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── local.py
│   │   │   └── s3.py
│   │   └── messaging/
│   │       ├── __init__.py
│   │       ├── email.py
│   │       └── sms.py
│   └── web/
│       ├── __init__.py
│       ├── static/
│       ├── templates/
│       └── admin/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   ├── unit/
│   │   ├── test_models/
│   │   ├── test_services/
│   │   └── test_utils/
│   ├── integration/
│   │   ├── test_api/
│   │   └── test_workflows/
│   └── e2e/
│       ├── test_user_journey.py
│       └── test_admin_flows.py
├── scripts/
│   ├── seed_data.py
│   ├── backup.py
│   └── deploy.py
├── monitoring/
│   ├── prometheus.yml
│   ├── grafana/
│   └── alerts/
└── docs/
    ├── api/
    ├── architecture/
    ├── deployment/
    └── user_guide/
```

### Modelos de Domínio Complexos

#### Produto com Variações
```python
# ecommerce/domains/produtos/models.py
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from ...infrastructure.database.base import Base


class StatusProduto(str, Enum):
    """Status de um produto no catálogo."""
    ATIVO = "ativo"
    INATIVO = "inativo"
    ESGOTADO = "esgotado"
    DESCONTINUADO = "descontinuado"


class TipoVariacao(str, Enum):
    """Tipos de variação de produto."""
    COR = "cor"
    TAMANHO = "tamanho"
    MATERIAL = "material"
    VOLTAGEM = "voltagem"
    MEMORIA = "memoria"


class Categoria(Base):
    """Categoria de produto com hierarquia."""
    __tablename__ = "categorias"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    nome = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(500))
    categoria_pai_id = Column(PG_UUID(as_uuid=True), nullable=True)
    ativo = Column(Boolean, default=True)
    ordem = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    """Produto principal com informações base."""
    __tablename__ = "produtos"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    nome = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    descricao_curta = Column(String(300))
    descricao_completa = Column(String(5000))
    sku_base = Column(String(50), unique=True, nullable=False)
    
    # Preço base (variações podem ter preços diferentes)
    preco_base = Column(Numeric(10, 2), nullable=False)
    preco_custo = Column(Numeric(10, 2))
    
    # Metadados
    peso = Column(Numeric(8, 3))  # em kg
    dimensoes = Column(JSON)  # {"altura": 10, "largura": 20, "profundidade": 5}
    marca = Column(String(100))
    
    # Status e controle
    status = Column(String(20), default=StatusProduto.ATIVO)
    destaque = Column(Boolean, default=False)
    
    # SEO
    meta_title = Column(String(60))
    meta_description = Column(String(160))
    meta_keywords = Column(String(255))
    
    # Relacionamentos
    categoria_id = Column(PG_UUID(as_uuid=True), nullable=False)
    categoria = relationship("Categoria", back_populates="produtos")
    variacoes = relationship("VariacaoProduto", back_populates="produto")
    imagens = relationship("ImagemProduto", back_populates="produto")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VariacaoProduto(Base):
    """Variação específica de um produto (ex: Camiseta Azul M)."""
    __tablename__ = "variacoes_produto"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    produto_id = Column(PG_UUID(as_uuid=True), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    
    # Atributos da variação
    atributos = Column(JSON)  # {"cor": "azul", "tamanho": "M"}
    
    # Preço específico (pode sobrescrever o base)
    preco = Column(Numeric(10, 2))
    preco_promocional = Column(Numeric(10, 2))
    
    # Estoque e disponibilidade
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    estoque_maximo = Column(Integer, default=1000)
    
    # Status específico
    ativo = Column(Boolean, default=True)
    peso_especifico = Column(Numeric(8, 3))
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="variacoes")
    itens_estoque = relationship("MovimentacaoEstoque", back_populates="variacao")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProdutoSchema(BaseModel):
    """Schema Pydantic para validação e serialização."""
    
    id: Optional[UUID] = None
    nome: str = Field(min_length=5, max_length=200)
    descricao_curta: str = Field(max_length=300)
    descricao_completa: Optional[str] = Field(max_length=5000)
    preco_base: Decimal = Field(gt=0, decimal_places=2)
    categoria_id: UUID
    status: StatusProduto = StatusProduto.ATIVO
    
    # Metadados opcionais
    peso: Optional[Decimal] = Field(ge=0, decimal_places=3)
    dimensoes: Optional[Dict[str, float]] = None
    marca: Optional[str] = Field(max_length=100)
    
    # SEO
    meta_title: Optional[str] = Field(max_length=60)
    meta_description: Optional[str] = Field(max_length=160)
    
    @validator('dimensoes')
    @classmethod
    def validar_dimensoes(cls, v: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
        """Valida estrutura das dimensões."""
        if v is None:
            return v
        
        campos_obrigatorios = {'altura', 'largura', 'profundidade'}
        if not campos_obrigatorios.issubset(v.keys()):
            raise ValueError(f"Dimensões devem conter: {campos_obrigatorios}")
        
        for campo, valor in v.items():
            if valor <= 0:
                raise ValueError(f"Dimensão {campo} deve ser positiva")
        
        return v
    
    @validator('preco_base')
    @classmethod
    def validar_preco(cls, v: Decimal) -> Decimal:
        """Valida formato do preço."""
        if v.as_tuple().exponent < -2:
            raise ValueError("Preço não pode ter mais de 2 casas decimais")
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            UUID: lambda v: str(v)
        }


class VariacaoSchema(BaseModel):
    """Schema para variação de produto."""
    
    id: Optional[UUID] = None
    produto_id: UUID
    sku: str = Field(min_length=3, max_length=50)
    atributos: Dict[str, str] = Field(min_items=1)
    preco: Optional[Decimal] = Field(gt=0, decimal_places=2)
    estoque_atual: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0, default=5)
    ativo: bool = True
    
    @validator('atributos')
    @classmethod
    def validar_atributos(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Valida atributos da variação."""
        if not v:
            raise ValueError("Variação deve ter pelo menos um atributo")
        
        # Validar que valores não estão vazios
        for chave, valor in v.items():
            if not valor.strip():
                raise ValueError(f"Valor do atributo '{chave}' não pode estar vazio")
        
        return v
    
    @validator('sku')
    @classmethod
    def validar_sku(cls, v: str) -> str:
        """Valida formato do SKU."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError("SKU deve conter apenas letras, números, hífens e underscores")
        return v.upper()
    
    class Config:
        from_attributes = True
```

#### Sistema de Carrinho Avançado
```python
# ecommerce/domains/carrinho/models.py
from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from ...infrastructure.database.base import Base


class StatusCarrinho(str, Enum):
    """Status do carrinho de compras."""
    ATIVO = "ativo"
    ABANDONADO = "abandonado"
    CONVERTIDO = "convertido"
    EXPIRADO = "expirado"


class Carrinho(Base):
    """Carrinho de compras do usuário."""
    __tablename__ = "carrinhos"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    usuario_id = Column(PG_UUID(as_uuid=True), nullable=True)  # Pode ser anônimo
    session_id = Column(String(100), nullable=True)  # Para usuários não logados
    
    # Valores calculados
    subtotal = Column(Numeric(10, 2), default=0)
    desconto = Column(Numeric(10, 2), default=0)
    frete = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    
    # Cupons e promoções aplicados
    cupom_codigo = Column(String(50))
    cupom_desconto = Column(Numeric(10, 2), default=0)
    
    # Status e controle
    status = Column(String(20), default=StatusCarrinho.ATIVO)
    
    # Dados de entrega
    cep_destino = Column(String(10))
    dados_frete = Column(JSON)  # Resultado do cálculo de frete
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    # Relacionamentos
    itens = relationship("ItemCarrinho", back_populates="carrinho", cascade="all, delete-orphan")


class ItemCarrinho(Base):
    """Item específico dentro do carrinho."""
    __tablename__ = "itens_carrinho"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    carrinho_id = Column(PG_UUID(as_uuid=True), nullable=False)
    variacao_id = Column(PG_UUID(as_uuid=True), nullable=False)
    
    # Dados do produto no momento da adição
    produto_nome = Column(String(200), nullable=False)
    produto_sku = Column(String(50), nullable=False)
    atributos_variacao = Column(JSON)  # Snapshot dos atributos
    
    # Preços e quantidades
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    preco_original = Column(Numeric(10, 2))  # Para mostrar desconto
    quantidade = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relacionamentos
    carrinho = relationship("Carrinho", back_populates="itens")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CarrinhoService:
    """Serviço de negócio para gestão de carrinho."""
    
    def __init__(self, carrinho_repo, produto_repo, estoque_service, cupom_service):
        self._carrinho_repo = carrinho_repo
        self._produto_repo = produto_repo
        self._estoque_service = estoque_service
        self._cupom_service = cupom_service
    
    async def adicionar_item(
        self,
        carrinho_id: UUID,
        variacao_id: UUID,
        quantidade: int
    ) -> ItemCarrinho:
        """
        Adiciona item ao carrinho com validações completas.
        
        Validações aplicadas:
        - Produto existe e está ativo
        - Variação disponível
        - Estoque suficiente
        - Quantidade válida
        - Limites por item
        
        Args:
            carrinho_id: ID do carrinho
            variacao_id: ID da variação do produto
            quantidade: Quantidade desejada
            
        Returns:
            Item adicionado ao carrinho
            
        Raises:
            EstoqueInsuficienteError: Se não há estoque
            ProdutoInativoError: Se produto não está disponível
            QuantidadeInvalidaError: Se quantidade é inválida
        """
        # IMPLEMENTAR: Lógica completa de adição
        # 1. Validar carrinho existe e está ativo
        # 2. Buscar e validar variação do produto
        # 3. Verificar disponibilidade em estoque
        # 4. Verificar se item já existe (atualizar quantidade)
        # 5. Aplicar limites de quantidade
        # 6. Calcular preços e descontos
        # 7. Atualizar totais do carrinho
        pass
    
    async def atualizar_quantidade(
        self,
        item_id: UUID,
        nova_quantidade: int
    ) -> ItemCarrinho:
        """
        Atualiza quantidade de um item no carrinho.
        
        Args:
            item_id: ID do item
            nova_quantidade: Nova quantidade (0 remove o item)
            
        Returns:
            Item atualizado ou None se removido
        """
        # IMPLEMENTAR: Lógica de atualização com validações
        pass
    
    async def aplicar_cupom(
        self,
        carrinho_id: UUID,
        codigo_cupom: str
    ) -> Carrinho:
        """
        Aplica cupom de desconto ao carrinho.
        
        Args:
            carrinho_id: ID do carrinho
            codigo_cupom: Código do cupom
            
        Returns:
            Carrinho com cupom aplicado
            
        Raises:
            CupomInvalidoError: Se cupom não é válido
            CupomExpiradoError: Se cupom expirou
            CupomJaUtilizadoError: Se cupom já foi usado
        """
        # IMPLEMENTAR: Validação e aplicação de cupom
        pass
    
    async def calcular_frete(
        self,
        carrinho_id: UUID,
        cep_destino: str,
        tipo_entrega: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calcula opções de frete para o carrinho.
        
        Args:
            carrinho_id: ID do carrinho
            cep_destino: CEP de destino
            tipo_entrega: Tipo preferido de entrega
            
        Returns:
            Dicionário com opções de frete
        """
        # IMPLEMENTAR: Integração com APIs de frete
        pass
    
    async def finalizar_carrinho(self, carrinho_id: UUID) -> Dict[str, Any]:
        """
        Prepara carrinho para checkout final.
        
        Validações finais:
        - Estoque ainda disponível
        - Preços não alterados
        - Cupons ainda válidos
        - Dados de entrega válidos
        
        Args:
            carrinho_id: ID do carrinho
            
        Returns:
            Resumo final do carrinho
        """
        # IMPLEMENTAR: Validações finais e preparação para checkout
        pass


# Schema para validação e serialização
class CarrinhoSchema(BaseModel):
    """Schema do carrinho para API."""
    
    id: UUID
    usuario_id: Optional[UUID]
    subtotal: Decimal
    desconto: Decimal
    frete: Decimal
    total: Decimal
    cupom_codigo: Optional[str]
    status: StatusCarrinho
    itens: List['ItemCarrinhoSchema']
    
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True


class ItemCarrinhoSchema(BaseModel):
    """Schema do item do carrinho."""
    
    id: UUID
    produto_nome: str
    produto_sku: str
    atributos_variacao: Dict[str, str]
    preco_unitario: Decimal
    preco_original: Optional[Decimal]
    quantidade: int
    subtotal: Decimal
    
    # Indica se há desconto
    @property
    def tem_desconto(self) -> bool:
        return (
            self.preco_original is not None 
            and self.preco_original > self.preco_unitario
        )
    
    # Percentual de desconto
    @property
    def percentual_desconto(self) -> Optional[float]:
        if not self.tem_desconto:
            return None
        return float((self.preco_original - self.preco_unitario) / self.preco_original * 100)
    
    class Config:
        from_attributes = True


# Atualizar referência forward
CarrinhoSchema.model_rebuild()
```

### Sistema de Pagamentos com Strategy Pattern

```python
# ecommerce/domains/pagamentos/services.py
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel


class StatusPagamento(str, Enum):
    """Status de um pagamento."""
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"


class TipoPagamento(str, Enum):
    """Tipos de pagamento suportados."""
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    PAYPAL = "paypal"


class ResultadoPagamento(BaseModel):
    """Resultado de uma operação de pagamento."""
    sucesso: bool
    transaction_id: Optional[str]
    gateway_response: Dict[str, Any]
    mensagem: Optional[str]
    codigo_erro: Optional[str]


class GatewayPagamento(ABC):
    """Interface abstrata para gateways de pagamento."""
    
    @abstractmethod
    async def processar_pagamento(
        self,
        valor: Decimal,
        dados_pagamento: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ResultadoPagamento:
        """Processa um pagamento."""
        pass
    
    @abstractmethod
    async def estornar_pagamento(
        self,
        transaction_id: str,
        valor: Optional[Decimal] = None
    ) -> ResultadoPagamento:
        """Estorna um pagamento."""
        pass
    
    @abstractmethod
    async def consultar_status(self, transaction_id: str) -> StatusPagamento:
        """Consulta status de uma transação."""
        pass


class StripeGateway(GatewayPagamento):
    """Implementação para Stripe."""
    
    def __init__(self, api_key: str, webhook_secret: str):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        # Em implementação real: inicializar cliente Stripe
    
    async def processar_pagamento(
        self,
        valor: Decimal,
        dados_pagamento: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ResultadoPagamento:
        """Processa pagamento via Stripe."""
        try:
            # Simulação de integração com Stripe
            # Em implementação real:
            # import stripe
            # stripe.api_key = self.api_key
            # charge = stripe.Charge.create(...)
            
            # Para demonstração, simula sucesso
            return ResultadoPagamento(
                sucesso=True,
                transaction_id=f"stripe_{uuid4().hex[:16]}",
                gateway_response={
                    "id": f"ch_{uuid4().hex[:24]}",
                    "amount": int(valor * 100),  # Stripe usa centavos
                    "currency": "brl",
                    "status": "succeeded"
                },
                mensagem="Pagamento processado com sucesso"
            )
        
        except Exception as e:
            return ResultadoPagamento(
                sucesso=False,
                transaction_id=None,
                gateway_response={"error": str(e)},
                mensagem="Erro ao processar pagamento",
                codigo_erro="STRIPE_ERROR"
            )
    
    async def estornar_pagamento(
        self,
        transaction_id: str,
        valor: Optional[Decimal] = None
    ) -> ResultadoPagamento:
        """Estorna pagamento no Stripe."""
        # IMPLEMENTAR: Lógica de estorno
        pass
    
    async def consultar_status(self, transaction_id: str) -> StatusPagamento:
        """Consulta status no Stripe."""
        # IMPLEMENTAR: Consulta de status
        pass


class PayPalGateway(GatewayPagamento):
    """Implementação para PayPal."""
    
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
    
    async def processar_pagamento(
        self,
        valor: Decimal,
        dados_pagamento: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ResultadoPagamento:
        """Processa pagamento via PayPal."""
        # IMPLEMENTAR: Integração com PayPal
        pass


class PagamentoService:
    """Serviço central de pagamentos usando Strategy Pattern."""
    
    def __init__(self):
        self._gateways: Dict[TipoPagamento, GatewayPagamento] = {}
        self._gateway_padrao = None
    
    def registrar_gateway(
        self,
        tipo: TipoPagamento,
        gateway: GatewayPagamento,
        padrao: bool = False
    ) -> None:
        """Registra um gateway de pagamento."""
        self._gateways[tipo] = gateway
        if padrao:
            self._gateway_padrao = tipo
    
    async def processar_pagamento(
        self,
        pedido_id: UUID,
        valor: Decimal,
        tipo_pagamento: TipoPagamento,
        dados_pagamento: Dict[str, Any],
        parcelas: int = 1
    ) -> ResultadoPagamento:
        """
        Processa pagamento usando gateway apropriado.
        
        Args:
            pedido_id: ID do pedido
            valor: Valor a ser cobrado
            tipo_pagamento: Tipo de pagamento
            dados_pagamento: Dados específicos do pagamento
            parcelas: Número de parcelas
            
        Returns:
            Resultado do processamento
        """
        # Validações iniciais
        if valor <= 0:
            return ResultadoPagamento(
                sucesso=False,
                transaction_id=None,
                gateway_response={},
                mensagem="Valor inválido",
                codigo_erro="INVALID_AMOUNT"
            )
        
        # Selecionar gateway
        gateway = self._gateways.get(tipo_pagamento)
        if not gateway:
            return ResultadoPagamento(
                sucesso=False,
                transaction_id=None,
                gateway_response={},
                mensagem=f"Gateway não configurado para {tipo_pagamento}",
                codigo_erro="GATEWAY_NOT_FOUND"
            )
        
        # Preparar metadata
        metadata = {
            "pedido_id": str(pedido_id),
            "parcelas": parcelas,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Processar pagamento
        resultado = await gateway.processar_pagamento(
            valor, dados_pagamento, metadata
        )
        
        # Registrar transação no banco de dados
        await self._registrar_transacao(
            pedido_id, valor, tipo_pagamento, resultado
        )
        
        return resultado
    
    async def _registrar_transacao(
        self,
        pedido_id: UUID,
        valor: Decimal,
        tipo_pagamento: TipoPagamento,
        resultado: ResultadoPagamento
    ) -> None:
        """Registra transação no banco de dados."""
        # IMPLEMENTAR: Persistência da transação
        pass


# Factory para configuração dos gateways
class PagamentoFactory:
    """Factory para criar e configurar serviço de pagamentos."""
    
    @staticmethod
    def criar_servico_producao() -> PagamentoService:
        """Cria serviço configurado para produção."""
        servico = PagamentoService()
        
        # Configurar Stripe
        stripe_gateway = StripeGateway(
            api_key="sk_live_...",  # Chave real em produção
            webhook_secret="whsec_..."
        )
        servico.registrar_gateway(TipoPagamento.CARTAO_CREDITO, stripe_gateway, padrao=True)
        
        # Configurar PayPal
        paypal_gateway = PayPalGateway(
            client_id="client_id_real",
            client_secret="client_secret_real",
            sandbox=False
        )
        servico.registrar_gateway(TipoPagamento.PAYPAL, paypal_gateway)
        
        return servico
    
    @staticmethod
    def criar_servico_teste() -> PagamentoService:
        """Cria serviço configurado para testes."""
        servico = PagamentoService()
        
        # Usar mocks ou gateways de teste
        # IMPLEMENTAR: Configuração para testes
        
        return servico
```

### Testes End-to-End Complexos

```python
# tests/e2e/test_user_journey.py
import pytest
from decimal import Decimal
from uuid import uuid4

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ecommerce.domains.usuarios.models import Usuario, TipoUsuario
from ecommerce.domains.produtos.models import Produto, VariacaoProduto
from ecommerce.domains.carrinho.models import Carrinho


class TestJornadaCompletalUsuario:
    """Testes end-to-end da jornada completa do usuário."""
    
    @pytest.mark.asyncio
    async def test_jornada_compra_completa(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        usuario_teste: Usuario,
        produto_teste: Produto
    ):
        """
        Testa jornada completa: registro → busca → carrinho → checkout → pagamento.
        
        Este teste simula uma jornada real de usuário desde o registro
        até a finalização da compra, validando cada etapa do processo.
        """
        
        # Etapa 1: Registro de usuário
        dados_registro = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "SenhaSegura123!",
            "telefone": "11999999999"
        }
        
        response = await async_client.post("/api/usuarios/registro", json=dados_registro)
        assert response.status_code == 201
        usuario_data = response.json()
        usuario_id = usuario_data["id"]
        
        # Etapa 2: Login
        dados_login = {
            "email": "joao@example.com",
            "senha": "SenhaSegura123!"
        }
        
        response = await async_client.post("/api/auth/login", json=dados_login)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Etapa 3: Buscar produtos
        response = await async_client.get(
            "/api/produtos/buscar",
            params={"q": "camiseta", "categoria": "roupas"},
            headers=headers
        )
        assert response.status_code == 200
        produtos = response.json()["items"]
        assert len(produtos) > 0
        
        produto_id = produtos[0]["id"]
        variacao_id = produtos[0]["variacoes"][0]["id"]
        
        # Etapa 4: Adicionar ao carrinho
        dados_item = {
            "variacao_id": variacao_id,
            "quantidade": 2
        }
        
        response = await async_client.post(
            "/api/carrinho/adicionar",
            json=dados_item,
            headers=headers
        )
        assert response.status_code == 200
        
        # Etapa 5: Visualizar carrinho
        response = await async_client.get("/api/carrinho", headers=headers)
        assert response.status_code == 200
        carrinho = response.json()
        assert len(carrinho["itens"]) == 1
        assert carrinho["itens"][0]["quantidade"] == 2
        
        carrinho_id = carrinho["id"]
        
        # Etapa 6: Aplicar cupom de desconto
        dados_cupom = {"codigo": "DESCONTO10"}
        response = await async_client.post(
            f"/api/carrinho/{carrinho_id}/cupom",
            json=dados_cupom,
            headers=headers
        )
        assert response.status_code == 200
        
        # Etapa 7: Calcular frete
        dados_frete = {"cep": "01310-100"}
        response = await async_client.post(
            f"/api/carrinho/{carrinho_id}/frete",
            json=dados_frete,
            headers=headers
        )
        assert response.status_code == 200
        opcoes_frete = response.json()
        assert len(opcoes_frete["opcoes"]) > 0
        
        # Selecionar opção de frete
        frete_selecionado = opcoes_frete["opcoes"][0]
        response = await async_client.put(
            f"/api/carrinho/{carrinho_id}/frete",
            json={"opcao_id": frete_selecionado["id"]},
            headers=headers
        )
        assert response.status_code == 200
        
        # Etapa 8: Iniciar checkout
        endereco_entrega = {
            "cep": "01310-100",
            "logradouro": "Rua Augusta, 123",
            "bairro": "Consolação",
            "cidade": "São Paulo",
            "estado": "SP",
            "complemento": "Apto 45"
        }
        
        dados_checkout = {
            "endereco_entrega": endereco_entrega,
            "endereco_cobranca": endereco_entrega  # Mesmo endereço
        }
        
        response = await async_client.post(
            f"/api/carrinho/{carrinho_id}/checkout",
            json=dados_checkout,
            headers=headers
        )
        assert response.status_code == 200
        checkout_data = response.json()
        pedido_id = checkout_data["pedido_id"]
        
        # Etapa 9: Processar pagamento
        dados_pagamento = {
            "tipo": "cartao_credito",
            "cartao": {
                "numero": "4111111111111111",  # Número de teste Visa
                "nome": "JOAO SILVA",
                "mes": "12",
                "ano": "2025",
                "cvv": "123"
            },
            "parcelas": 1
        }
        
        response = await async_client.post(
            f"/api/pedidos/{pedido_id}/pagamento",
            json=dados_pagamento,
            headers=headers
        )
        assert response.status_code == 200
        pagamento_data = response.json()
        assert pagamento_data["status"] == "aprovado"
        
        # Etapa 10: Confirmar pedido final
        response = await async_client.get(f"/api/pedidos/{pedido_id}", headers=headers)
        assert response.status_code == 200
        pedido_final = response.json()
        
        # Validações finais
        assert pedido_final["status"] == "confirmado"
        assert pedido_final["total"] > 0
        assert len(pedido_final["itens"]) == 1
        assert pedido_final["endereco_entrega"]["cep"] == "01310-100"
        assert pedido_final["pagamento"]["status"] == "aprovado"
        
        # Verificar que carrinho foi limpo
        response = await async_client.get("/api/carrinho", headers=headers)
        carrinho_pos_compra = response.json()
        assert len(carrinho_pos_compra["itens"]) == 0
    
    @pytest.mark.asyncio
    async def test_jornada_abandono_carrinho(
        self,
        async_client: AsyncClient,
        usuario_teste: Usuario
    ):
        """Testa cenário de abandono de carrinho e recuperação."""
        # IMPLEMENTAR: Teste de abandono e recuperação de carrinho
        pass
    
    @pytest.mark.asyncio
    async def test_jornada_pagamento_rejeitado(
        self,
        async_client: AsyncClient,
        usuario_teste: Usuario
    ):
        """Testa cenário onde pagamento é rejeitado."""
        # IMPLEMENTAR: Teste de pagamento rejeitado
        pass


class TestJornadaAdmin:
    """Testes da jornada do administrador."""
    
    @pytest.mark.asyncio
    async def test_gestao_completa_produto(
        self,
        async_client: AsyncClient,
        admin_user: Usuario
    ):
        """Testa gestão completa de produto: criar → editar → ativar/desativar."""
        # IMPLEMENTAR: Teste de gestão de produtos
        pass
    
    @pytest.mark.asyncio
    async def test_processamento_pedidos(
        self,
        async_client: AsyncClient,
        admin_user: Usuario
    ):
        """Testa processamento de pedidos pelo admin."""
        # IMPLEMENTAR: Teste de processamento de pedidos
        pass


class TestPerformance:
    """Testes de performance e carga."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_carga_multiplos_usuarios(
        self,
        async_client: AsyncClient
    ):
        """Simula múltiplos usuários fazendo compras simultaneamente."""
        import asyncio
        
        async def simular_compra(user_id: int):
            """Simula uma compra completa para um usuário."""
            # IMPLEMENTAR: Simulação de compra com dados únicos
            pass
        
        # Executar 50 compras simultâneas
        tasks = [simular_compra(i) for i in range(50)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verificar que pelo menos 90% tiveram sucesso
        sucessos = sum(1 for r in results if not isinstance(r, Exception))
        assert sucessos >= 45  # 90% de sucesso
    
    @pytest.mark.asyncio
    async def test_performance_busca_produtos(
        self,
        async_client: AsyncClient,
        produtos_massa: List[Produto]  # Fixture com 1000+ produtos
    ):
        """Testa performance da busca com grande volume de produtos."""
        import time
        
        start_time = time.time()
        
        response = await async_client.get(
            "/api/produtos/buscar",
            params={"q": "teste", "limit": 20}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.5  # Menos de 500ms
        
        results = response.json()
        assert len(results["items"]) <= 20
```

### Critérios de Avaliação Detalhados

#### Arquitetura e Design (25%)
- [ ] **Domain-Driven Design**: Domínios bem separados e coesos
- [ ] **Patterns Aplicados**: Strategy, Factory, Repository, etc.
- [ ] **Separação de Responsabilidades**: API, Domínio, Infraestrutura
- [ ] **Extensibilidade**: Facilidade para adicionar novos recursos
- [ ] **Configurabilidade**: Ambiente, gateways, features toggles

#### Qualidade de Código (25%)
- [ ] **Type Safety**: Tipagem completa e consistente
- [ ] **Validações**: Entrada, negócio, integridade
- [ ] **Error Handling**: Tratamento robusto de exceções
- [ ] **Code Quality**: Ruff, mypy, complexidade ciclomática
- [ ] **Documentação**: Docstrings, README, API docs

#### Funcionalidades (25%)
- [ ] **Features Completas**: Todos os requisitos implementados
- [ ] **Regras de Negócio**: Validações corretas e completas
- [ ] **Integrações**: APIs externas, gateways de pagamento
- [ ] **Performance**: Tempo de resposta adequado
- [ ] **Usabilidade**: Interface intuitiva e responsiva

#### Testes e DevOps (25%)
- [ ] **Cobertura**: >= 90% para domínios críticos
- [ ] **Tipos de Teste**: Unit, integration, e2e
- [ ] **Qualidade dos Testes**: Cenários reais, edge cases
- [ ] **CI/CD**: Pipeline completo funcionando
- [ ] **Monitoramento**: Logs, métricas, health checks

### Extensões Avançadas

#### Observabilidade
- Integração com Prometheus/Grafana
- Distributed tracing com OpenTelemetry
- Alertas automáticos para métricas críticas
- Dashboard de negócio em tempo real

#### Escalabilidade
- Cache distribuído com Redis Cluster
- Message broker para processamento assíncrono
- Read replicas para consultas
- CDN para assets estáticos

#### Segurança
- Autenticação JWT com refresh tokens
- Rate limiting por usuário/IP
- Validação de entrada rigorosa
- Auditoria de ações críticas
- HTTPS only com certificados válidos

### Tempo Estimado e Entregas

**Fase 1 (Semana 1-2)**: Arquitetura e Modelos
- Setup do projeto e estrutura
- Modelos de domínio principais
- Repositórios e serviços básicos
- Testes unitários dos modelos

**Fase 2 (Semana 3-4)**: API e Integrações
- Endpoints REST completos
- Integração com gateways de pagamento
- Sistema de carrinho e checkout
- Testes de integração

**Fase 3 (Semana 5-6)**: Interface e DevOps
- Frontend/admin interface
- Pipeline CI/CD completo
- Monitoramento e logs
- Testes end-to-end

**Entrega Final**: Demonstração completa com:
- Aplicação rodando em produção
- Pipeline CI/CD funcional
- Documentação completa
- Métricas de performance
- Apresentação técnica (30 min)

Este exercício representa o nível máximo de complexidade esperado, integrando todos os conceitos abordados na disciplina em um projeto real e pronto para produção.
