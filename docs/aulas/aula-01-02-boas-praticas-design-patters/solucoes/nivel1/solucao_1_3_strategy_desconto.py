#!/usr/bin/env python3
"""
Solução do Exercício 1.3: Aplicação Básica do Strategy Pattern

OBJETIVO: Demonstrar a aplicação do Strategy Pattern para um sistema de
cálculo de desconto em uma loja online.

CONCEITOS DEMONSTRADOS:
- Strategy Pattern
- Open/Closed Principle (OCP)
- Dependency Injection
- Polimorfismo
- Decimal para cálculos monetários
- Enum para types seguros

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol, Optional, Dict, List
from enum import Enum
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime, date


# =============================================================================
# PROBLEMA: Código sem Strategy Pattern (Violação OCP)
# =============================================================================

class CalculadoraPreco_Problemática:
    """
    ❌ PROBLEMA: Esta implementação viola o Open/Closed Principle (OCP)
    
    Problemas:
    1. Para adicionar novo tipo de desconto, precisa modificar a classe
    2. Lógica de desconto misturada com lógica de cálculo
    3. Difícil de testar cada estratégia isoladamente
    4. Alto acoplamento entre tipos de cliente e cálculos
    """
    
    def calcular_preco_final(self, valor_original: float, tipo_cliente: str) -> float:
        """Método que viola OCP - precisa ser modificado para novos tipos"""
        
        if tipo_cliente == "regular":
            desconto = valor_original * 0.05
        elif tipo_cliente == "vip":
            desconto = valor_original * 0.15
        elif tipo_cliente == "funcionario":
            desconto = valor_original * 0.20
        elif tipo_cliente == "sem_desconto":
            desconto = 0.0
        else:
            # ❌ Problema: precisa adicionar novos casos aqui
            raise ValueError(f"Tipo de cliente desconhecido: {tipo_cliente}")
        
        return valor_original - desconto


# =============================================================================
# SOLUÇÃO: STRATEGY PATTERN
# =============================================================================

# 1. ENUMS E VALUE OBJECTS PARA TYPE SAFETY
# -----------------------------------------------------------------------------

class TipoCliente(Enum):
    """Enum para tipos de cliente (Type Safety)"""
    REGULAR = "regular"
    VIP = "vip"
    FUNCIONARIO = "funcionario"
    PREMIUM = "premium"
    ESTUDANTE = "estudante"


@dataclass(frozen=True)
class Produto:
    """Value Object para representar um produto"""
    codigo: str
    nome: str
    preco: Decimal
    categoria: str
    
    def __post_init__(self):
        if self.preco < Decimal('0'):
            raise ValueError("Preço não pode ser negativo")


@dataclass(frozen=True)
class ResultadoDesconto:
    """Value Object para o resultado do cálculo de desconto"""
    valor_original: Decimal
    percentual_desconto: Decimal
    valor_desconto: Decimal
    valor_final: Decimal
    estrategia_aplicada: str
    detalhes: str
    
    def __str__(self) -> str:
        return (f"Desconto: {self.percentual_desconto}% | "
                f"Original: R$ {self.valor_original} | "
                f"Final: R$ {self.valor_final}")


# 2. INTERFACE STRATEGY (Protocol)
# -----------------------------------------------------------------------------

class EstrategiaDesconto(Protocol):
    """
    ✅ Interface Strategy usando Protocol
    
    BENEFÍCIOS:
    - Type hints claros
    - Fácil de implementar
    - Flexibilidade sem herança obrigatória
    - Compatível com duck typing do Python
    """
    
    @abstractmethod
    def calcular_desconto(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """
        Calcula desconto baseado na estratégia específica.
        
        Args:
            valor_original: Valor base do produto/carrinho
            **kwargs: Parâmetros específicos da estratégia
            
        Returns:
            ResultadoDesconto: Objeto com detalhes do desconto aplicado
        """
        ...
    
    @abstractmethod
    def get_nome_estrategia(self) -> str:
        """Retorna nome descritivo da estratégia"""
        ...
    
    @abstractmethod
    def is_aplicavel(self, **kwargs) -> bool:
        """Verifica se estratégia pode ser aplicada nas condições dadas"""
        ...


# 3. ESTRATÉGIAS CONCRETAS
# -----------------------------------------------------------------------------

class DescontoSemDesconto:
    """
    ✅ Estratégia: Sem desconto (Null Object Pattern)
    
    BENEFÍCIOS:
    - Evita casos especiais no código cliente
    - Comportamento consistente
    - Fácil de testar
    """
    
    def calcular_desconto(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """Implementa ausência de desconto"""
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=Decimal('0'),
            valor_desconto=Decimal('0'),
            valor_final=valor_original,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes="Nenhum desconto aplicado"
        )
    
    def get_nome_estrategia(self) -> str:
        return "Sem Desconto"
    
    def is_aplicavel(self, **kwargs) -> bool:
        return True  # Sempre aplicável como fallback


class DescontoClienteRegular:
    """
    ✅ Estratégia: Cliente Regular (5% de desconto)
    
    CARACTERÍSTICAS:
    - Desconto fixo de 5%
    - Aplicável a qualquer valor
    - Estratégia básica de fidelização
    """
    
    def __init__(self, percentual: Decimal = Decimal('5')):
        if percentual < Decimal('0') or percentual > Decimal('100'):
            raise ValueError("Percentual deve estar entre 0 e 100")
        self._percentual = percentual
    
    def calcular_desconto(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """Calcula desconto de cliente regular"""
        percentual_decimal = self._percentual / Decimal('100')
        valor_desconto = (valor_original * percentual_decimal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        valor_final = valor_original - valor_desconto
        
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=self._percentual,
            valor_desconto=valor_desconto,
            valor_final=valor_final,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes=f"Desconto de {self._percentual}% para cliente regular"
        )
    
    def get_nome_estrategia(self) -> str:
        return f"Cliente Regular ({self._percentual}%)"
    
    def is_aplicavel(self, **kwargs) -> bool:
        return True  # Sempre aplicável


class DescontoClienteVIP:
    """
    ✅ Estratégia: Cliente VIP (15% de desconto)
    
    CARACTERÍSTICAS:
    - Desconto maior para clientes especiais
    - Pode ter valor mínimo de compra
    - Estratégia de retenção premium
    """
    
    def __init__(self, percentual: Decimal = Decimal('15'), valor_minimo: Decimal = Decimal('0')):
        if percentual < Decimal('0') or percentual > Decimal('100'):
            raise ValueError("Percentual deve estar entre 0 e 100")
        if valor_minimo < Decimal('0'):
            raise ValueError("Valor mínimo deve ser positivo")
        
        self._percentual = percentual
        self._valor_minimo = valor_minimo
    
    def calcular_desconto(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """Calcula desconto VIP com verificação de valor mínimo"""
        if not self.is_aplicavel(valor_original=valor_original, **kwargs):
            return DescontoSemDesconto().calcular_desconto(valor_original, **kwargs)
        
        percentual_decimal = self._percentual / Decimal('100')
        valor_desconto = (valor_original * percentual_decimal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        valor_final = valor_original - valor_desconto
        
        detalhes = f"Desconto VIP de {self._percentual}%"
        if self._valor_minimo > Decimal('0'):
            detalhes += f" (valor mínimo: R$ {self._valor_minimo})"
        
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=self._percentual,
            valor_desconto=valor_desconto,
            valor_final=valor_final,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes=detalhes
        )
    
    def get_nome_estrategia(self) -> str:
        return f"Cliente VIP ({self._percentual}%)"
    
    def is_aplicavel(self, valor_original: Decimal = None, **kwargs) -> bool:
        if valor_original is None:
            return False
        return valor_original >= self._valor_minimo


class DescontoClienteFuncionario:
    """
    ✅ Estratégia: Funcionário (20% de desconto)
    
    CARACTERÍSTICAS:
    - Maior desconto para funcionários
    - Pode ter limite por mês
    - Estratégia de benefício corporativo
    """
    
    def __init__(self, percentual: Decimal = Decimal('20'), limite_mensal: Optional[Decimal] = None):
        if percentual < Decimal('0') or percentual > Decimal('100'):
            raise ValueError("Percentual deve estar entre 0 e 100")
        
        self._percentual = percentual
        self._limite_mensal = limite_mensal
        self._uso_mensal: Dict[str, Decimal] = {}  # Simula controle por funcionário
    
    def calcular_desconto(self, valor_original: Decimal, 
                         funcionario_id: Optional[str] = None, **kwargs) -> ResultadoDesconto:
        """Calcula desconto de funcionário com controle de limite"""
        
        # Verificar limite mensal se especificado
        if self._limite_mensal and funcionario_id:
            mes_atual = datetime.now().strftime("%Y-%m")
            chave_controle = f"{funcionario_id}_{mes_atual}"
            uso_atual = self._uso_mensal.get(chave_controle, Decimal('0'))
            
            if uso_atual + valor_original > self._limite_mensal:
                detalhes = f"Limite mensal de R$ {self._limite_mensal} excedido"
                return ResultadoDesconto(
                    valor_original=valor_original,
                    percentual_desconto=Decimal('0'),
                    valor_desconto=Decimal('0'),
                    valor_final=valor_original,
                    estrategia_aplicada="Funcionário (Limite Excedido)",
                    detalhes=detalhes
                )
        
        percentual_decimal = self._percentual / Decimal('100')
        valor_desconto = (valor_original * percentual_decimal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        valor_final = valor_original - valor_desconto
        
        # Atualizar controle de uso
        if self._limite_mensal and funcionario_id:
            mes_atual = datetime.now().strftime("%Y-%m")
            chave_controle = f"{funcionario_id}_{mes_atual}"
            self._uso_mensal[chave_controle] = self._uso_mensal.get(chave_controle, Decimal('0')) + valor_original
        
        detalhes = f"Desconto funcionário de {self._percentual}%"
        if self._limite_mensal:
            detalhes += f" (limite mensal: R$ {self._limite_mensal})"
        
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=self._percentual,
            valor_desconto=valor_desconto,
            valor_final=valor_final,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes=detalhes
        )
    
    def get_nome_estrategia(self) -> str:
        return f"Funcionário ({self._percentual}%)"
    
    def is_aplicavel(self, funcionario_id: Optional[str] = None, **kwargs) -> bool:
        return funcionario_id is not None


class DescontoClientePremium:
    """
    ✅ Estratégia: Cliente Premium (Desconto progressivo)
    
    CARACTERÍSTICAS:
    - Desconto varia conforme valor da compra
    - Incentiva compras maiores
    - Estratégia de upselling
    """
    
    def __init__(self):
        # Faixas de desconto progressivo
        self._faixas = [
            (Decimal('1000'), Decimal('25')),  # Acima de R$ 1000: 25%
            (Decimal('500'), Decimal('20')),   # Acima de R$ 500: 20%
            (Decimal('200'), Decimal('15')),   # Acima de R$ 200: 15%
            (Decimal('100'), Decimal('10')),   # Acima de R$ 100: 10%
            (Decimal('0'), Decimal('5'))       # Qualquer valor: 5%
        ]
    
    def calcular_desconto(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """Calcula desconto progressivo baseado no valor"""
        
        # Encontrar faixa de desconto aplicável
        percentual_desconto = Decimal('0')
        faixa_aplicada = "Nenhuma"
        
        for valor_minimo, percentual in self._faixas:
            if valor_original >= valor_minimo:
                percentual_desconto = percentual
                faixa_aplicada = f"R$ {valor_minimo}+"
                break
        
        percentual_decimal = percentual_desconto / Decimal('100')
        valor_desconto = (valor_original * percentual_decimal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        valor_final = valor_original - valor_desconto
        
        detalhes = f"Desconto Premium progressivo: {percentual_desconto}% (faixa {faixa_aplicada})"
        
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=percentual_desconto,
            valor_desconto=valor_desconto,
            valor_final=valor_final,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes=detalhes
        )
    
    def get_nome_estrategia(self) -> str:
        return "Cliente Premium (Progressivo)"
    
    def is_aplicavel(self, **kwargs) -> bool:
        return True


class DescontoEstudante:
    """
    ✅ Estratégia: Estudante (10% com validação)
    
    CARACTERÍSTICAS:
    - Desconto específico para estudantes
    - Requer validação de matrícula
    - Pode ter restrições por categoria de produto
    """
    
    def __init__(self, percentual: Decimal = Decimal('10'), categorias_permitidas: Optional[List[str]] = None):
        if percentual < Decimal('0') or percentual > Decimal('100'):
            raise ValueError("Percentual deve estar entre 0 e 100")
        
        self._percentual = percentual
        self._categorias_permitidas = categorias_permitidas or ["livros", "tecnologia", "educacao"]
    
    def calcular_desconto(self, valor_original: Decimal, 
                         categoria_produto: Optional[str] = None,
                         matricula_valida: bool = False, **kwargs) -> ResultadoDesconto:
        """Calcula desconto estudante com validações"""
        
        if not matricula_valida:
            return ResultadoDesconto(
                valor_original=valor_original,
                percentual_desconto=Decimal('0'),
                valor_desconto=Decimal('0'),
                valor_final=valor_original,
                estrategia_aplicada="Estudante (Matrícula Inválida)",
                detalhes="Matrícula estudantil não validada"
            )
        
        if categoria_produto and categoria_produto.lower() not in self._categorias_permitidas:
            return ResultadoDesconto(
                valor_original=valor_original,
                percentual_desconto=Decimal('0'),
                valor_desconto=Decimal('0'),
                valor_final=valor_original,
                estrategia_aplicada="Estudante (Categoria Restrita)",
                detalhes=f"Categoria '{categoria_produto}' não elegível para desconto estudantil"
            )
        
        percentual_decimal = self._percentual / Decimal('100')
        valor_desconto = (valor_original * percentual_decimal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        valor_final = valor_original - valor_desconto
        
        detalhes = f"Desconto estudante de {self._percentual}%"
        if categoria_produto:
            detalhes += f" (categoria: {categoria_produto})"
        
        return ResultadoDesconto(
            valor_original=valor_original,
            percentual_desconto=self._percentual,
            valor_desconto=valor_desconto,
            valor_final=valor_final,
            estrategia_aplicada=self.get_nome_estrategia(),
            detalhes=detalhes
        )
    
    def get_nome_estrategia(self) -> str:
        return f"Estudante ({self._percentual}%)"
    
    def is_aplicavel(self, matricula_valida: bool = False, **kwargs) -> bool:
        return matricula_valida


# 4. CONTEXT CLASS (Calculadora de Preço)
# -----------------------------------------------------------------------------

class CalculadoraPreco:
    """
    ✅ Context class que usa Strategy Pattern
    
    BENEFÍCIOS:
    - Permite mudança de estratégia em runtime
    - Delega responsabilidade para estratégias
    - Fácil de testar (injeção de dependência)
    - Extensível sem modificação (OCP)
    """
    
    def __init__(self, estrategia: EstrategiaDesconto):
        """
        Inicializa calculadora com estratégia de desconto.
        
        Args:
            estrategia: Estratégia de desconto a ser aplicada
        """
        self._estrategia = estrategia
        self._historico: List[ResultadoDesconto] = []
    
    def definir_estrategia(self, estrategia: EstrategiaDesconto) -> None:
        """
        Permite trocar estratégia em tempo de execução.
        
        Args:
            estrategia: Nova estratégia de desconto
        """
        self._estrategia = estrategia
    
    def calcular_preco_final(self, valor_original: Decimal, **kwargs) -> ResultadoDesconto:
        """
        Calcula preço final aplicando desconto da estratégia atual.
        
        Args:
            valor_original: Valor base para cálculo
            **kwargs: Parâmetros específicos da estratégia
            
        Returns:
            ResultadoDesconto: Resultado completo do cálculo
        """
        if valor_original < Decimal('0'):
            raise ValueError("Valor original não pode ser negativo")
        
        resultado = self._estrategia.calcular_desconto(valor_original, **kwargs)
        self._historico.append(resultado)
        
        return resultado
    
    def calcular_preco_produto(self, produto: Produto, **kwargs) -> ResultadoDesconto:
        """
        Conveniência: calcula desconto para um produto específico.
        
        Args:
            produto: Produto para aplicar desconto
            **kwargs: Parâmetros da estratégia
            
        Returns:
            ResultadoDesconto: Resultado do cálculo
        """
        kwargs.setdefault('categoria_produto', produto.categoria)
        return self.calcular_preco_final(produto.preco, **kwargs)
    
    def obter_estrategia_atual(self) -> str:
        """Retorna nome da estratégia atual"""
        return self._estrategia.get_nome_estrategia()
    
    def obter_historico(self) -> List[ResultadoDesconto]:
        """Retorna histórico de cálculos realizados"""
        return self._historico.copy()
    
    def limpar_historico(self) -> None:
        """Limpa histórico de cálculos"""
        self._historico.clear()


# 5. FACTORY PARA ESTRATÉGIAS (Bonus)
# -----------------------------------------------------------------------------

class FabricaEstrategias:
    """
    ✅ Factory para criação de estratégias (Bonus: Factory Pattern)
    
    BENEFÍCIOS:
    - Centraliza criação de estratégias
    - Facilita configuração
    - Permite estratégias pré-configuradas
    """
    
    @staticmethod
    def criar_estrategia(tipo_cliente: TipoCliente, **configuracoes) -> EstrategiaDesconto:
        """
        Cria estratégia baseada no tipo de cliente.
        
        Args:
            tipo_cliente: Tipo do cliente
            **configuracoes: Configurações específicas da estratégia
            
        Returns:
            EstrategiaDesconto: Estratégia configurada
        """
        
        estrategias = {
            TipoCliente.REGULAR: lambda: DescontoClienteRegular(
                configuracoes.get('percentual', Decimal('5'))
            ),
            TipoCliente.VIP: lambda: DescontoClienteVIP(
                configuracoes.get('percentual', Decimal('15')),
                configuracoes.get('valor_minimo', Decimal('50'))
            ),
            TipoCliente.FUNCIONARIO: lambda: DescontoClienteFuncionario(
                configuracoes.get('percentual', Decimal('20')),
                configuracoes.get('limite_mensal', Decimal('500'))
            ),
            TipoCliente.PREMIUM: lambda: DescontoClientePremium(),
            TipoCliente.ESTUDANTE: lambda: DescontoEstudante(
                configuracoes.get('percentual', Decimal('10')),
                configuracoes.get('categorias_permitidas', ["livros", "tecnologia"])
            )
        }
        
        factory_func = estrategias.get(tipo_cliente)
        if not factory_func:
            raise ValueError(f"Tipo de cliente não suportado: {tipo_cliente}")
        
        return factory_func()
    
    @staticmethod
    def criar_sem_desconto() -> EstrategiaDesconto:
        """Cria estratégia sem desconto"""
        return DescontoSemDesconto()


# =============================================================================
# DEMONSTRAÇÃO E CASOS DE USO
# =============================================================================

def demonstrar_strategy_pattern():
    """
    Demonstra o uso do Strategy Pattern com exemplos práticos.
    
    DEMONSTRAÇÃO:
    1. Criação de produtos e estratégias
    2. Uso da calculadora com diferentes estratégias
    3. Mudança de estratégia em runtime
    4. Comparação de resultados
    """
    
    print("🔧 DEMONSTRAÇÃO: Strategy Pattern para Descontos")
    print("=" * 55)
    
    # Criar produtos de exemplo
    print("\n📦 1. Criando produtos de exemplo...")
    produtos = [
        Produto("BOOK001", "Livro Python Avançado", Decimal("89.90"), "livros"),
        Produto("TECH001", "Mouse Gamer", Decimal("299.90"), "tecnologia"), 
        Produto("CLOTH001", "Camiseta", Decimal("49.90"), "roupas"),
        Produto("LAPTOP001", "Notebook", Decimal("2499.90"), "tecnologia")
    ]
    
    for produto in produtos:
        print(f"✅ {produto.nome}: R$ {produto.preco}")
    
    # Criar estratégias usando factory
    print("\n🏭 2. Criando estratégias usando Factory...")
    factory = FabricaEstrategias()
    
    estrategias = {
        "Regular": factory.criar_estrategia(TipoCliente.REGULAR),
        "VIP": factory.criar_estrategia(TipoCliente.VIP, valor_minimo=Decimal('100')),
        "Funcionário": factory.criar_estrategia(TipoCliente.FUNCIONARIO, limite_mensal=Decimal('1000')),
        "Premium": factory.criar_estrategia(TipoCliente.PREMIUM),
        "Estudante": factory.criar_estrategia(TipoCliente.ESTUDANTE),
        "Sem Desconto": factory.criar_sem_desconto()
    }
    
    for nome, estrategia in estrategias.items():
        print(f"✅ Estratégia criada: {nome} ({estrategia.get_nome_estrategia()})")
    
    # Demonstrar uso com produto específico
    print("\n💰 3. Aplicando diferentes estratégias ao Notebook (R$ 2.499,90)...")
    produto_teste = produtos[3]  # Notebook
    calculadora = CalculadoraPreco(estrategias["Regular"])
    
    resultados = {}
    for nome, estrategia in estrategias.items():
        calculadora.definir_estrategia(estrategia)
        
        # Parâmetros específicos para cada estratégia
        kwargs = {}
        if nome == "Funcionário":
            kwargs["funcionario_id"] = "FUNC001"
        elif nome == "Estudante":
            kwargs["matricula_valida"] = True
        
        resultado = calculadora.calcular_preco_produto(produto_teste, **kwargs)
        resultados[nome] = resultado
        
        print(f"📊 {nome:12}: {resultado}")
    
    # Demonstrar mudança de estratégia em runtime
    print("\n🔄 4. Demonstrando mudança de estratégia em runtime...")
    
    carrinho_valor = Decimal("150.00")
    print(f"💳 Valor do carrinho: R$ {carrinho_valor}")
    
    # Simular fluxo de cliente que muda de categoria
    fluxo_estrategias = ["Regular", "VIP", "Premium"]
    
    for estrategia_nome in fluxo_estrategias:
        calculadora.definir_estrategia(estrategias[estrategia_nome])
        resultado = calculadora.calcular_preco_final(carrinho_valor)
        print(f"🔄 {estrategia_nome}: R$ {resultado.valor_final} (economizou R$ {resultado.valor_desconto})")
    
    # Demonstrar vantagens do Strategy Pattern
    print("\n📈 5. Comparando economias por estratégia...")
    
    valores_teste = [Decimal("50"), Decimal("150"), Decimal("300"), Decimal("600"), Decimal("1200")]
    
    print(f"{'Valor':>8} | {'Regular':>10} | {'VIP':>10} | {'Premium':>10} | {'Funcionário':>12}")
    print("-" * 70)
    
    for valor in valores_teste:
        linha_resultado = f"R${valor:>6}"
        
        for estrategia_nome in ["Regular", "VIP", "Premium", "Funcionário"]:
            calculadora.definir_estrategia(estrategias[estrategia_nome])
            kwargs = {"funcionario_id": "FUNC001"} if estrategia_nome == "Funcionário" else {}
            resultado = calculadora.calcular_preco_final(valor, **kwargs)
            economia = resultado.valor_desconto
            linha_resultado += f" | R${economia:>8}"
        
        print(linha_resultado)
    
    print("\n🎯 6. Benefícios do Strategy Pattern demonstrados:")
    print("   ✅ Fácil adição de novas estratégias (OCP)")
    print("   ✅ Mudança de comportamento em runtime")  
    print("   ✅ Cada estratégia tem lógica isolada")
    print("   ✅ Fácil de testar cada estratégia separadamente")
    print("   ✅ Cliente não conhece detalhes das estratégias")


def demonstrar_casos_especiais():
    """
    Demonstra casos especiais e validações das estratégias.
    
    CASOS ESPECIAIS:
    - Limites e restrições
    - Validações específicas
    - Tratamento de erros
    """
    
    print("\n🔍 CASOS ESPECIAIS E VALIDAÇÕES")
    print("=" * 40)
    
    factory = FabricaEstrategias()
    calculadora = CalculadoraPreco(factory.criar_sem_desconto())
    
    # Caso 1: Funcionário com limite mensal
    print("\n💼 1. Testando limite mensal do funcionário...")
    
    estrategia_func = factory.criar_estrategia(
        TipoCliente.FUNCIONARIO, 
        limite_mensal=Decimal('500')
    )
    calculadora.definir_estrategia(estrategia_func)
    
    # Primeira compra (dentro do limite)
    resultado1 = calculadora.calcular_preco_final(
        Decimal('300'), 
        funcionario_id="FUNC123"
    )
    print(f"🟢 Primeira compra: {resultado1}")
    
    # Segunda compra (excede o limite)
    resultado2 = calculadora.calcular_preco_final(
        Decimal('300'), 
        funcionario_id="FUNC123"
    )
    print(f"🔴 Segunda compra: {resultado2}")
    
    # Caso 2: Estudante com categoria restrita
    print("\n🎓 2. Testando restrições de categoria para estudante...")
    
    estrategia_estudante = factory.criar_estrategia(
        TipoCliente.ESTUDANTE,
        categorias_permitidas=["livros", "tecnologia"]
    )
    calculadora.definir_estrategia(estrategia_estudante)
    
    # Categoria permitida
    resultado3 = calculadora.calcular_preco_final(
        Decimal('100'),
        categoria_produto="livros",
        matricula_valida=True
    )
    print(f"🟢 Livro (permitido): {resultado3}")
    
    # Categoria não permitida
    resultado4 = calculadora.calcular_preco_final(
        Decimal('100'),
        categoria_produto="roupas",
        matricula_valida=True
    )
    print(f"🔴 Roupa (restrita): {resultado4}")
    
    # Matrícula inválida
    resultado5 = calculadora.calcular_preco_final(
        Decimal('100'),
        categoria_produto="livros",
        matricula_valida=False
    )
    print(f"❌ Matrícula inválida: {resultado5}")
    
    # Caso 3: VIP com valor mínimo
    print("\n⭐ 3. Testando valor mínimo para VIP...")
    
    estrategia_vip = factory.criar_estrategia(
        TipoCliente.VIP,
        valor_minimo=Decimal('100')
    )
    calculadora.definir_estrategia(estrategia_vip)
    
    # Valor acima do mínimo
    resultado6 = calculadora.calcular_preco_final(Decimal('150'))
    print(f"🟢 Acima do mínimo: {resultado6}")
    
    # Valor abaixo do mínimo
    resultado7 = calculadora.calcular_preco_final(Decimal('50'))
    print(f"🔴 Abaixo do mínimo: {resultado7}")


# =============================================================================
# TESTES AUTOMATIZADOS
# =============================================================================

def executar_testes_strategy():
    """
    Executa testes automatizados para validar Strategy Pattern.
    
    TESTES:
    - Cálculos corretos por estratégia
    - Mudança de estratégia em runtime
    - Validações e restrições
    - Factory pattern
    """
    
    print("\n🧪 EXECUTANDO TESTES STRATEGY PATTERN...")
    print("=" * 50)
    
    factory = FabricaEstrategias()
    
    # Teste 1: Cálculos básicos
    print("\n🔍 Teste 1: Cálculos básicos por estratégia...")
    
    valor_teste = Decimal('100.00')
    
    # Cliente Regular: 5%
    estrategia_regular = factory.criar_estrategia(TipoCliente.REGULAR)
    calculadora = CalculadoraPreco(estrategia_regular)
    resultado = calculadora.calcular_preco_final(valor_teste)
    
    assert resultado.valor_original == Decimal('100.00')
    assert resultado.percentual_desconto == Decimal('5')
    assert resultado.valor_desconto == Decimal('5.00')
    assert resultado.valor_final == Decimal('95.00')
    print("✅ Cliente Regular: cálculo correto")
    
    # Cliente VIP: 15%
    estrategia_vip = factory.criar_estrategia(TipoCliente.VIP)
    calculadora.definir_estrategia(estrategia_vip)
    resultado = calculadora.calcular_preco_final(valor_teste)
    
    assert resultado.percentual_desconto == Decimal('15')
    assert resultado.valor_desconto == Decimal('15.00')
    assert resultado.valor_final == Decimal('85.00')
    print("✅ Cliente VIP: cálculo correto")
    
    # Funcionário: 20%
    estrategia_func = factory.criar_estrategia(TipoCliente.FUNCIONARIO)
    calculadora.definir_estrategia(estrategia_func)
    resultado = calculadora.calcular_preco_final(valor_teste, funcionario_id="TEST001")
    
    assert resultado.percentual_desconto == Decimal('20')
    assert resultado.valor_desconto == Decimal('20.00')
    assert resultado.valor_final == Decimal('80.00')
    print("✅ Funcionário: cálculo correto")
    
    # Teste 2: Mudança de estratégia em runtime
    print("\n🔍 Teste 2: Mudança de estratégia em runtime...")
    
    calculadora = CalculadoraPreco(factory.criar_sem_desconto())
    valor_teste = Decimal('200.00')
    
    # Sem desconto
    resultado1 = calculadora.calcular_preco_final(valor_teste)
    assert resultado1.valor_final == valor_teste
    
    # Mudar para VIP
    calculadora.definir_estrategia(factory.criar_estrategia(TipoCliente.VIP))
    resultado2 = calculadora.calcular_preco_final(valor_teste)
    assert resultado2.valor_final == Decimal('170.00')  # 15% desconto
    
    # Mudar para Premium (faixa de R$ 200: 15%)
    calculadora.definir_estrategia(factory.criar_estrategia(TipoCliente.PREMIUM))
    resultado3 = calculadora.calcular_preco_final(valor_teste)
    assert resultado3.percentual_desconto == Decimal('15')  # Faixa R$ 200+
    
    print("✅ Mudança de estratégia: funcionando corretamente")
    
    # Teste 3: Validações e restrições
    print("\n🔍 Teste 3: Validações e restrições...")
    
    # Estudante sem matrícula válida
    estrategia_estudante = factory.criar_estrategia(TipoCliente.ESTUDANTE)
    calculadora.definir_estrategia(estrategia_estudante)
    resultado = calculadora.calcular_preco_final(
        Decimal('100'), 
        matricula_valida=False
    )
    assert resultado.valor_desconto == Decimal('0')
    print("✅ Estudante sem matrícula: desconto negado")
    
    # VIP com valor mínimo
    estrategia_vip_min = factory.criar_estrategia(
        TipoCliente.VIP, 
        valor_minimo=Decimal('150')
    )
    calculadora.definir_estrategia(estrategia_vip_min)
    resultado = calculadora.calcular_preco_final(Decimal('100'))  # Abaixo do mínimo
    assert resultado.valor_desconto == Decimal('0')
    print("✅ VIP abaixo do mínimo: desconto negado")
    
    # Teste 4: Precisão decimal
    print("\n🔍 Teste 4: Precisão decimal com Decimal...")
    
    # Teste com valor que gera dízima periódica
    valor_complexo = Decimal('33.33')
    calculadora.definir_estrategia(factory.criar_estrategia(TipoCliente.VIP))
    resultado = calculadora.calcular_preco_final(valor_complexo)
    
    # Verificar se resultado tem 2 casas decimais
    assert str(resultado.valor_desconto).count('.') <= 1
    decimal_part = str(resultado.valor_desconto).split('.')[-1]
    assert len(decimal_part) <= 2
    print("✅ Precisão decimal: arredondamento correto")
    
    # Teste 5: Factory pattern
    print("\n🔍 Teste 5: Factory pattern...")
    
    # Testar criação de todas as estratégias
    for tipo_cliente in TipoCliente:
        try:
            estrategia = factory.criar_estrategia(tipo_cliente)
            assert estrategia is not None
            assert hasattr(estrategia, 'calcular_desconto')
            assert hasattr(estrategia, 'get_nome_estrategia')
        except ValueError:
            pass  # Alguns tipos podem não estar implementados
    
    print("✅ Factory: criação de estratégias funcionando")
    
    print("\n🎉 TODOS OS TESTES STRATEGY PASSARAM!")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Demonstrar Strategy Pattern
    demonstrar_strategy_pattern()
    
    # Demonstrar casos especiais
    demonstrar_casos_especiais()
    
    # Executar testes
    executar_testes_strategy()
    
    print("\n" + "=" * 65)
    print("📚 ANÁLISE FINAL DO STRATEGY PATTERN:")
    print()
    print("PROBLEMA ORIGINAL:")
    print("❌ Código com múltiplos if/elif para diferentes tipos")
    print("❌ Violação do Open/Closed Principle")
    print("❌ Difícil adicionar novos tipos de desconto")
    print("❌ Lógica de negócio misturada com estrutura de controle")
    print("❌ Difícil de testar cada tipo individualmente")
    print()
    print("SOLUÇÃO COM STRATEGY PATTERN:")
    print("✅ Cada estratégia encapsula seu algoritmo")
    print("✅ Fácil adição de novas estratégias (OCP)")
    print("✅ Mudança de comportamento em runtime")
    print("✅ Testabilidade melhorada (estratégias isoladas)")
    print("✅ Código cliente limpo e focado")
    print("✅ Reutilização de estratégias em diferentes contextos")
    print()
    print("BENEFÍCIOS EXTRAS DEMONSTRADOS:")
    print("🏭 Factory Pattern para criação de estratégias")
    print("💰 Uso de Decimal para precisão monetária")
    print("🔒 Type safety com Enums e Protocols")
    print("📊 Value Objects para resultados estruturados")
    print("⚡ Configurabilidade e parametrização")
    print()
    print("🎯 RESULTADO: Código extensível, testável e maintível!")
