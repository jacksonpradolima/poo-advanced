"""
Solução do Exercício 1.2: Replace Conditional with Polymorphism - Sistema de Desconto

Esta solução demonstra como eliminar switch statements complexos
usando Strategy Pattern e polimorfismo, resultando em código
mais extensível e aderente ao Open/Closed Principle.

REFATORAÇÕES APLICADAS:
1. Strategy Pattern para diferentes tipos de cliente
2. Eliminação de switch statement complexo
3. Polimorfismo em vez de condicionais
4. Factory Method para criação de estratégias
5. Facilita extensão sem modificação
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from enum import Enum


class TipoCliente(Enum):
    """Enum para tipos de cliente - elimina strings mágicas."""
    BRONZE = "bronze"
    SILVER = "silver" 
    GOLD = "gold"
    PLATINUM = "platinum"
    REGULAR = "regular"


class CalculadoraDesconto(ABC):
    """
    Interface abstrata para estratégias de desconto.
    
    BENEFÍCIOS DO STRATEGY PATTERN:
    - Elimina switch statements complexos
    - Facilita adição de novos tipos
    - Cada estratégia é testável isoladamente
    - Adere ao Open/Closed Principle
    """
    
    @abstractmethod
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        """
        Calcula desconto baseado nas regras específicas do tipo de cliente.
        
        Returns:
            Dict com desconto_percentual, desconto_fixo
        """
        pass
    
    def _aplicar_desconto_primeiro_pedido(self, desconto_percentual: float, 
                                         desconto_fixo: float) -> Dict[str, float]:
        """
        Método auxiliar para aplicar lógica comum de primeiro pedido.
        Pode ser sobrescrito pelas subclasses se necessário.
        """
        return {
            "desconto_percentual": desconto_percentual,
            "desconto_fixo": desconto_fixo
        }


class DescontoBronze(CalculadoraDesconto):
    """
    Estratégia de desconto para clientes Bronze.
    
    REGRAS BRONZE:
    - Primeiro pedido: 5% desconto
    - Pedidos normais: 2% se valor > R$ 100, senão 0%
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        if primeiro_pedido:
            return self._aplicar_desconto_primeiro_pedido(5.0, 0.0)
        
        # Lógica para pedidos normais
        if valor_compra > 100:
            return {"desconto_percentual": 2.0, "desconto_fixo": 0.0}
        
        return {"desconto_percentual": 0.0, "desconto_fixo": 0.0}


class DescontoSilver(CalculadoraDesconto):
    """
    Estratégia de desconto para clientes Silver.
    
    REGRAS SILVER:
    - Primeiro pedido: 10% + R$ 5 fixo
    - Valor > R$ 200: 5% desconto
    - Valor > R$ 100: 3% desconto
    - Senão: 0% desconto
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        if primeiro_pedido:
            return self._aplicar_desconto_primeiro_pedido(10.0, 5.0)
        
        # Lógica para pedidos normais
        if valor_compra > 200:
            return {"desconto_percentual": 5.0, "desconto_fixo": 0.0}
        elif valor_compra > 100:
            return {"desconto_percentual": 3.0, "desconto_fixo": 0.0}
        
        return {"desconto_percentual": 0.0, "desconto_fixo": 0.0}


class DescontoGold(CalculadoraDesconto):
    """
    Estratégia de desconto para clientes Gold.
    
    REGRAS GOLD:
    - Primeiro pedido: 15% + R$ 10 fixo
    - Quantidade > 10 itens: 12% + R$ 5 fixo
    - Valor > R$ 300: 8% desconto
    - Senão: 5% desconto (mínimo garantido)
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        if primeiro_pedido:
            return self._aplicar_desconto_primeiro_pedido(15.0, 10.0)
        
        # Lógica para pedidos normais com múltiplos critérios
        if quantidade_itens > 10:
            return {"desconto_percentual": 12.0, "desconto_fixo": 5.0}
        elif valor_compra > 300:
            return {"desconto_percentual": 8.0, "desconto_fixo": 0.0}
        else:
            # Gold sempre tem desconto mínimo
            return {"desconto_percentual": 5.0, "desconto_fixo": 0.0}


class DescontoPlatinum(CalculadoraDesconto):
    """
    Estratégia de desconto para clientes Platinum.
    
    REGRAS PLATINUM:
    - Primeiro pedido: 20% + R$ 20 fixo
    - Valor > R$ 500: 18% + R$ 15 fixo
    - Valor > R$ 300: 15% + R$ 10 fixo
    - Senão: 12% + R$ 5 fixo (mínimo garantido)
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        if primeiro_pedido:
            return self._aplicar_desconto_primeiro_pedido(20.0, 20.0)
        
        # Lógica escalonada para Platinum
        if valor_compra > 500:
            return {"desconto_percentual": 18.0, "desconto_fixo": 15.0}
        elif valor_compra > 300:
            return {"desconto_percentual": 15.0, "desconto_fixo": 10.0}
        else:
            # Platinum sempre tem desconto mínimo generoso
            return {"desconto_percentual": 12.0, "desconto_fixo": 5.0}


class DescontoRegular(CalculadoraDesconto):
    """
    Estratégia de desconto para clientes regulares (sem classificação).
    
    REGRAS REGULAR:
    - Nenhum desconto aplicado
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        return {"desconto_percentual": 0.0, "desconto_fixo": 0.0}


class FabricaEstrategias:
    """
    Factory Method para criação de estratégias de desconto.
    
    BENEFÍCIOS:
    - Centraliza criação de objetos
    - Facilita adição de novos tipos
    - Isola lógica de criação
    - Permite reutilização de instâncias
    """
    
    def __init__(self):
        # Cache de estratégias para reutilização (Flyweight pattern)
        self._estrategias = {
            TipoCliente.BRONZE: DescontoBronze(),
            TipoCliente.SILVER: DescontoSilver(),
            TipoCliente.GOLD: DescontoGold(),
            TipoCliente.PLATINUM: DescontoPlatinum(),
            TipoCliente.REGULAR: DescontoRegular()
        }
    
    def criar_estrategia(self, tipo_cliente: str) -> CalculadoraDesconto:
        """
        Cria/retorna estratégia apropriada para o tipo de cliente.
        
        Args:
            tipo_cliente: String representando o tipo do cliente
            
        Returns:
            Instância da estratégia apropriada
            
        Raises:
            ValueError: Se o tipo não for reconhecido
        """
        try:
            tipo_enum = TipoCliente(tipo_cliente.lower())
            return self._estrategias[tipo_enum]
        except ValueError:
            # Retorna estratégia padrão para tipos desconhecidos
            return self._estrategias[TipoCliente.REGULAR]


class SistemaDescontoRefatorado:
    """
    Sistema de desconto refatorado usando Strategy Pattern.
    
    MELHORIAS IMPLEMENTADAS:
    - Switch statement eliminado
    - Strategy Pattern aplicado
    - Factory Method para criação
    - Código extensível e testável
    - Adere ao Open/Closed Principle
    """
    
    def __init__(self):
        self.fabrica = FabricaEstrategias()
    
    def calcular_desconto(self, tipo_cliente: str, valor_compra: float, 
                         quantidade_itens: int, primeiro_pedido: bool) -> dict:
        """
        Método principal refatorado - agora com delegação simples.
        
        ANTES: Switch statement complexo com 30+ linhas
        DEPOIS: 10 linhas focadas apenas em coordenar cálculo
        
        Complexidade ciclomática: 1 (era 6+)
        """
        # 1. Obter estratégia apropriada
        estrategia = self.fabrica.criar_estrategia(tipo_cliente)
        
        # 2. Delegar cálculo para a estratégia
        resultado_desconto = estrategia.calcular_desconto(
            valor_compra, quantidade_itens, primeiro_pedido
        )
        
        # 3. Aplicar descontos e calcular valores finais
        desconto_percentual = resultado_desconto["desconto_percentual"]
        desconto_fixo = resultado_desconto["desconto_fixo"]
        
        valor_desconto_percentual = valor_compra * (desconto_percentual / 100)
        valor_desconto_total = valor_desconto_percentual + desconto_fixo
        valor_final = max(valor_compra - valor_desconto_total, 0)
        
        return {
            "tipo_cliente": tipo_cliente,
            "valor_original": valor_compra,
            "desconto_percentual": desconto_percentual,
            "desconto_fixo": desconto_fixo,
            "valor_desconto_total": valor_desconto_total,
            "valor_final": valor_final
        }
    
    def adicionar_nova_estrategia(self, tipo: TipoCliente, estrategia: CalculadoraDesconto):
        """
        Permite adicionar novas estratégias dinamicamente.
        Demonstra a extensibilidade do sistema.
        """
        self.fabrica._estrategias[tipo] = estrategia


# =============================================================================
# EXEMPLO DE EXTENSIBILIDADE: NOVO TIPO DE CLIENTE
# =============================================================================

class DescontoDiamond(CalculadoraDesconto):
    """
    Nova estratégia Diamond - demonstra facilidade de extensão.
    
    REGRAS DIAMOND (VIP):
    - Primeiro pedido: 25% + R$ 50 fixo
    - Sempre 20% + R$ 25 fixo (mínimo)
    """
    
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> Dict[str, float]:
        if primeiro_pedido:
            return {"desconto_percentual": 25.0, "desconto_fixo": 50.0}
        
        return {"desconto_percentual": 20.0, "desconto_fixo": 25.0}


# =============================================================================
# DEMONSTRAÇÃO DE USO E COMPARAÇÃO
# =============================================================================

def demonstrar_refatoracao():
    """
    Demonstra o uso do sistema refatorado e facilidade de extensão.
    """
    print("=== DEMONSTRAÇÃO: Sistema de Desconto Refatorado ===\n")
    
    sistema = SistemaDescontoRefatorado()
    
    # Cenários de teste
    cenarios = [
        {"tipo": "bronze", "valor": 150.00, "itens": 3, "primeiro": False},
        {"tipo": "silver", "valor": 250.00, "itens": 5, "primeiro": True},
        {"tipo": "gold", "valor": 350.00, "itens": 12, "primeiro": False},
        {"tipo": "platinum", "valor": 600.00, "itens": 8, "primeiro": False},
        {"tipo": "desconhecido", "valor": 100.00, "itens": 2, "primeiro": False}
    ]
    
    for cenario in cenarios:
        print(f"🛍️ Cliente {cenario['tipo'].title()}")
        print(f"   Valor: R$ {cenario['valor']:.2f}, Itens: {cenario['itens']}, Primeiro pedido: {cenario['primeiro']}")
        
        resultado = sistema.calcular_desconto(
            cenario['tipo'],
            cenario['valor'],
            cenario['itens'],
            cenario['primeiro']
        )
        
        print(f"   Desconto: {resultado['desconto_percentual']:.1f}% + R$ {resultado['desconto_fixo']:.2f}")
        print(f"   Valor final: R$ {resultado['valor_final']:.2f}")
        print(f"   Economia: R$ {resultado['valor_desconto_total']:.2f}")
        print()
    
    # Demonstrar extensibilidade
    print("💎 EXTENSIBILIDADE: Adicionando novo tipo Diamond")
    
    # Adicionar nova estratégia (não precisa modificar código existente!)
    TipoCliente.DIAMOND = "diamond"  # Simular adição ao enum
    sistema.fabrica._estrategias[TipoCliente.DIAMOND] = DescontoDiamond()
    
    resultado_diamond = sistema.calcular_desconto("diamond", 1000.00, 5, True)
    print(f"   Cliente Diamond - Primeiro pedido")
    print(f"   Valor: R$ 1000.00")
    print(f"   Desconto: {resultado_diamond['desconto_percentual']:.1f}% + R$ {resultado_diamond['desconto_fixo']:.2f}")
    print(f"   Valor final: R$ {resultado_diamond['valor_final']:.2f}")
    print(f"   Economia: R$ {resultado_diamond['valor_desconto_total']:.2f}")


def testar_estrategias_individuais():
    """
    Demonstra como estratégias individuais são testáveis.
    """
    print("\n=== TESTES UNITÁRIOS DAS ESTRATÉGIAS ===\n")
    
    # Teste estratégia Gold
    print("🧪 Teste Estratégia Gold:")
    estrategia_gold = DescontoGold()
    
    cenarios_gold = [
        (200.00, 5, False, "Valor baixo"),
        (400.00, 8, False, "Valor alto"),
        (300.00, 15, False, "Muitos itens"),
        (500.00, 3, True, "Primeiro pedido")
    ]
    
    for valor, itens, primeiro, descricao in cenarios_gold:
        resultado = estrategia_gold.calcular_desconto(valor, itens, primeiro)
        print(f"   ✓ {descricao}: {resultado['desconto_percentual']:.1f}% + R$ {resultado['desconto_fixo']:.2f}")
    
    # Teste estratégia Platinum
    print("\n🧪 Teste Estratégia Platinum:")
    estrategia_platinum = DescontoPlatinum()
    
    cenarios_platinum = [
        (200.00, 3, False, "Valor baixo"),
        (400.00, 5, False, "Valor médio"),
        (600.00, 8, False, "Valor alto"),
        (800.00, 10, True, "Primeiro pedido")
    ]
    
    for valor, itens, primeiro, descricao in cenarios_platinum:
        resultado = estrategia_platinum.calcular_desconto(valor, itens, primeiro)
        print(f"   ✓ {descricao}: {resultado['desconto_percentual']:.1f}% + R$ {resultado['desconto_fixo']:.2f}")


if __name__ == "__main__":
    demonstrar_refatoracao()
    testar_estrategias_individuais()
    
    print("\n🎯 BENEFÍCIOS DA REFATORAÇÃO:")
    print("✅ Switch statement eliminado completamente")
    print("✅ Cada tipo de cliente é uma classe testável independente")
    print("✅ Facilidade para adicionar novos tipos (Open/Closed)")
    print("✅ Código mais legível e organizacionalmente coeso")
    print("✅ Factory Method centraliza criação de estratégias")
    print("✅ Polimorfismo substitui condicionais complexas")
