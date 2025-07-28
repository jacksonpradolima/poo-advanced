"""
Solução do Exercício 1.1: Extract Method - Calculadora de Impostos

Esta solução demonstra como refatorar um método longo aplicando
a técnica Extract Method para melhorar a legibilidade, 
testabilidade e manutenibilidade do código.

REFATORAÇÕES APLICADAS:
1. Extract Method para cálculos específicos
2. Eliminação de Magic Numbers
3. Redução de complexidade ciclomática
4. Melhoria da testabilidade
"""

from typing import Tuple


class CalculadoraImpostosRefatorada:
    """
    Versão refatorada da calculadora de impostos.
    
    MELHORIAS IMPLEMENTADAS:
    - Métodos específicos para cada tipo de cálculo
    - Constantes nomeadas para valores fixos
    - Complexidade ciclomática reduzida
    - Cada método testável isoladamente
    """
    
    # CONSTANTES EXTRAÍDAS (elimina Magic Numbers)
    
    # Faixas e alíquotas do INSS (2024)
    INSS_FAIXAS = [
        (1100.00, 0.075),
        (2203.48, 0.09),
        (3305.22, 0.12),
        (6433.57, 0.14)
    ]
    INSS_TETO = 6433.57
    INSS_ALIQUOTA_MAXIMA = 0.14
    
    # Faixas e alíquotas do IRRF (2024)
    IRRF_FAIXAS = [
        (1903.98, 0.0, 0.0),        # (limite, alíquota, dedução)
        (2826.65, 0.075, 142.80),
        (3751.05, 0.15, 354.80),
        (4664.68, 0.225, 636.13),
        (float('inf'), 0.275, 869.36)
    ]
    
    # Deduções fixas
    DEDUCAO_POR_DEPENDENTE = 189.59
    NUMERO_DEPENDENTES_ASSUMIDO = 2
    
    # Planos de saúde
    PLANOS_SAUDE = {
        "basic": 150.00,
        "premium": 300.00
    }
    
    def calcular_impostos_totais(self, salario_bruto: float, tem_dependentes: bool, 
                                plano_saude: str, contribuicao_previdencia: float) -> dict:
        """
        Método principal refatorado - agora com apenas coordenação.
        
        ANTES: 50+ linhas com múltiplas responsabilidades
        DEPOIS: 10 linhas focadas apenas em coordenar cálculos
        
        Complexidade ciclomática: 1 (era 8+)
        """
        # 1. Calcular INSS
        inss = self._calcular_inss(salario_bruto)
        
        # 2. Calcular deduções permitidas
        total_deducoes = self._calcular_deducoes(tem_dependentes, plano_saude)
        
        # 3. Calcular base para IRRF
        base_irrf = salario_bruto - inss - contribuicao_previdencia - total_deducoes
        
        # 4. Calcular IRRF
        irrf, aliquota_irrf = self._calcular_irrf(base_irrf)
        
        # 5. Calcular salário líquido
        salario_liquido = salario_bruto - inss - irrf
        
        return {
            "salario_bruto": salario_bruto,
            "inss": inss,
            "irrf": irrf,
            "deducao_dependentes": self.DEDUCAO_POR_DEPENDENTE * self.NUMERO_DEPENDENTES_ASSUMIDO if tem_dependentes else 0,
            "deducao_saude": self.PLANOS_SAUDE.get(plano_saude, 0),
            "base_irrf": base_irrf,
            "aliquota_irrf": aliquota_irrf,
            "salario_liquido": salario_liquido
        }
    
    def _calcular_inss(self, salario_bruto: float) -> float:
        """
        Calcula o INSS baseado nas faixas progressivas.
        
        BENEFÍCIOS DA EXTRAÇÃO:
        - Lógica isolada e testável
        - Reutilizável em outros contextos
        - Fácil manutenção das tabelas
        - Complexidade ciclomática: 2
        """
        if salario_bruto > self.INSS_TETO:
            return self.INSS_TETO * self.INSS_ALIQUOTA_MAXIMA
        
        for limite, aliquota in self.INSS_FAIXAS:
            if salario_bruto <= limite:
                return salario_bruto * aliquota
        
        # Fallback (não deveria acontecer com dados válidos)
        return 0.0
    
    def _calcular_deducoes(self, tem_dependentes: bool, plano_saude: str) -> float:
        """
        Calcula o total de deduções permitidas.
        
        BENEFÍCIOS DA EXTRAÇÃO:
        - Centraliza lógica de deduções
        - Facilita adição de novos tipos de dedução
        - Testável isoladamente
        - Complexidade ciclomática: 1
        """
        deducao_dependentes = 0
        if tem_dependentes:
            deducao_dependentes = self.DEDUCAO_POR_DEPENDENTE * self.NUMERO_DEPENDENTES_ASSUMIDO
        
        deducao_saude = self.PLANOS_SAUDE.get(plano_saude, 0)
        
        return deducao_dependentes + deducao_saude
    
    def _calcular_irrf(self, base_calculo: float) -> Tuple[float, float]:
        """
        Calcula o IRRF baseado nas faixas progressivas.
        
        BENEFÍCIOS DA EXTRAÇÃO:
        - Lógica complexa isolada
        - Retorna valor e alíquota juntos
        - Fácil manutenção das tabelas
        - Testável com diferentes cenários
        
        Returns:
            Tuple[float, float]: (valor_irrf, aliquota_aplicada)
        """
        if base_calculo <= 0:
            return 0.0, 0.0
        
        for limite, aliquota, deducao in self.IRRF_FAIXAS:
            if base_calculo <= limite:
                if aliquota == 0:
                    return 0.0, 0.0
                else:
                    irrf = base_calculo * aliquota - deducao
                    return max(0.0, irrf), aliquota
        
        # Fallback (não deveria acontecer)
        return 0.0, 0.0


# =============================================================================
# EXEMPLO DE USO E DEMONSTRAÇÃO
# =============================================================================

def demonstrar_refatoracao():
    """
    Demonstra o uso da versão refatorada e compara com cenários comuns.
    """
    print("=== DEMONSTRAÇÃO: Calculadora de Impostos Refatorada ===\n")
    
    calc = CalculadoraImpostosRefatorada()
    
    # Cenários de teste
    cenarios = [
        {
            "nome": "Analista Júnior",
            "salario": 3500.00,
            "dependentes": False,
            "plano": "basic",
            "previdencia": 200.00
        },
        {
            "nome": "Gerente Senior",
            "salario": 8000.00,
            "dependentes": True,
            "plano": "premium",
            "previdencia": 500.00
        },
        {
            "nome": "Estagiário",
            "salario": 1200.00,
            "dependentes": False,
            "plano": "",
            "previdencia": 0.00
        }
    ]
    
    for cenario in cenarios:
        print(f"📊 Cenário: {cenario['nome']}")
        print(f"   Salário Bruto: R$ {cenario['salario']:.2f}")
        
        resultado = calc.calcular_impostos_totais(
            cenario['salario'],
            cenario['dependentes'], 
            cenario['plano'],
            cenario['previdencia']
        )
        
        print(f"   INSS: R$ {resultado['inss']:.2f}")
        print(f"   IRRF: R$ {resultado['irrf']:.2f} (alíquota: {resultado['aliquota_irrf']*100:.1f}%)")
        print(f"   Salário Líquido: R$ {resultado['salario_liquido']:.2f}")
        print(f"   Desconto Total: R$ {(resultado['salario_bruto'] - resultado['salario_liquido']):.2f}")
        print()


# =============================================================================
# TESTES UNITÁRIOS PARA DEMONSTRAR TESTABILIDADE
# =============================================================================

def testar_metodos_extraidos():
    """
    Demonstra como os métodos extraídos são facilmente testáveis.
    """
    print("=== TESTES UNITÁRIOS DOS MÉTODOS EXTRAÍDOS ===\n")
    
    calc = CalculadoraImpostosRefatorada()
    
    # Teste 1: INSS
    print("🧪 Teste INSS:")
    teste_inss = [
        (1000.00, 75.00),   # 7.5%
        (2000.00, 180.00),  # 9%
        (3000.00, 360.00),  # 12%
        (5000.00, 700.00),  # 14%
        (8000.00, 900.11),  # Teto
    ]
    
    for salario, esperado in teste_inss:
        resultado = calc._calcular_inss(salario)
        status = "✅" if abs(resultado - esperado) < 0.1 else "❌"
        print(f"   {status} Salário R$ {salario:.2f} → INSS R$ {resultado:.2f} (esperado: R$ {esperado:.2f})")
    
    # Teste 2: Deduções
    print("\n🧪 Teste Deduções:")
    teste_deducoes = [
        (False, "", 0.00),
        (True, "", 379.18),  # 2 dependentes
        (False, "basic", 150.00),
        (True, "premium", 679.18),  # dependentes + premium
    ]
    
    for dependentes, plano, esperado in teste_deducoes:
        resultado = calc._calcular_deducoes(dependentes, plano)
        status = "✅" if abs(resultado - esperado) < 0.1 else "❌"
        print(f"   {status} Dependentes: {dependentes}, Plano: '{plano}' → R$ {resultado:.2f} (esperado: R$ {esperado:.2f})")
    
    # Teste 3: IRRF
    print("\n🧪 Teste IRRF:")
    teste_irrf = [
        (1500.00, 0.00, 0.0),      # Isento
        (2500.00, 45.20, 0.075),   # 7.5%
        (3500.00, 170.20, 0.15),   # 15%
        (4500.00, 373.87, 0.225),  # 22.5%
        (6000.00, 781.64, 0.275),  # 27.5%
    ]
    
    for base, esperado_valor, esperado_aliquota in teste_irrf:
        valor, aliquota = calc._calcular_irrf(base)
        status_valor = "✅" if abs(valor - esperado_valor) < 0.1 else "❌"
        status_aliquota = "✅" if abs(aliquota - esperado_aliquota) < 0.001 else "❌"
        print(f"   {status_valor}{status_aliquota} Base R$ {base:.2f} → IRRF R$ {valor:.2f} ({aliquota*100:.1f}%)")


if __name__ == "__main__":
    demonstrar_refatoracao()
    print("\n" + "="*60 + "\n")
    testar_metodos_extraidos()
    
    print("\n🎯 BENEFÍCIOS DA REFATORAÇÃO:")
    print("✅ Complexidade ciclomática reduzida de 8+ para 1-2 por método")
    print("✅ Cada cálculo pode ser testado isoladamente")  
    print("✅ Magic numbers eliminados com constantes nomeadas")
    print("✅ Método principal focado apenas em coordenação")
    print("✅ Facilita manutenção de tabelas de impostos")
    print("✅ Código mais legível e autodocumentado")
