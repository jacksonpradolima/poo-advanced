"""
Testes para Calculadora de Impostos

Conjunto completo de testes que demonstra boas práticas:
- Testes parametrizados para múltiplos casos
- Fixtures para dados reutilizáveis
- Testes de casos limites e exceções
- Verificação de precisão decimal
- Documentação clara dos cenários

Execução: pytest test_calculadora_impostos_solucao.py -v --cov
"""

import pytest
from decimal import Decimal, InvalidOperation
from calculadora_impostos_solucao import (
    calcular_icms,
    calcular_iss,
    calcular_pis_cofins,
    total_impostos,
    formatar_valor_monetario
)


class TestCalcularICMS:
    """Testes para função calcular_icms."""
    
    def test_calcular_icms_valor_inteiro(self):
        """Testa cálculo de ICMS com valor inteiro."""
        resultado = calcular_icms(100)
        esperado = Decimal('18.00')
        assert resultado == esperado
    
    def test_calcular_icms_valor_decimal(self):
        """Testa cálculo de ICMS com valor decimal."""
        resultado = calcular_icms(Decimal('1000.50'))
        esperado = Decimal('180.09')
        assert resultado == esperado
    
    def test_calcular_icms_valor_zero(self):
        """Testa cálculo de ICMS com valor zero."""
        resultado = calcular_icms(0)
        esperado = Decimal('0.00')
        assert resultado == esperado
    
    def test_calcular_icms_valor_float(self):
        """Testa cálculo de ICMS com valor float."""
        resultado = calcular_icms(250.75)
        esperado = Decimal('45.14')  # 250.75 * 0.18 = 45.135 -> 45.14
        assert resultado == esperado
    
    def test_calcular_icms_valor_negativo_levanta_excecao(self):
        """Testa se ValueError é lançada para valor negativo."""
        with pytest.raises(ValueError, match="não pode ser negativo"):
            calcular_icms(-100)
    
    def test_calcular_icms_valor_string_invalida_levanta_excecao(self):
        """Testa se TypeError é lançada para string inválida."""
        with pytest.raises(TypeError, match="número válido"):
            calcular_icms("não é número")
    
    @pytest.mark.parametrize("valor_entrada,esperado", [
        (100, Decimal('18.00')),
        (500, Decimal('90.00')),
        (1000, Decimal('180.00')),
        (1234.56, Decimal('222.22')),
        (0.01, Decimal('0.00')),  # Arredondamento para baixo
    ])
    def test_calcular_icms_casos_parametrizados(self, valor_entrada, esperado):
        """Testa múltiplos casos usando parametrização."""
        resultado = calcular_icms(valor_entrada)
        assert resultado == esperado


class TestCalcularISS:
    """Testes para função calcular_iss."""
    
    def test_calcular_iss_valor_padrao(self):
        """Testa cálculo de ISS com valor padrão."""
        resultado = calcular_iss(1000)
        esperado = Decimal('50.00')
        assert resultado == esperado
    
    def test_calcular_iss_valor_decimal_precision(self):
        """Testa precisão decimal no cálculo de ISS."""
        resultado = calcular_iss(Decimal('2500.75'))
        esperado = Decimal('125.04')  # 2500.75 * 0.05 = 125.0375 -> 125.04
        assert resultado == esperado
    
    def test_calcular_iss_valor_zero(self):
        """Testa ISS para valor zero."""
        resultado = calcular_iss(0)
        esperado = Decimal('0.00')
        assert resultado == esperado
    
    def test_calcular_iss_valor_negativo_levanta_excecao(self):
        """Testa se ValueError é lançada para valor negativo."""
        with pytest.raises(ValueError, match="não pode ser negativo"):
            calcular_iss(-500)
    
    def test_calcular_iss_none_levanta_excecao(self):
        """Testa se TypeError é lançada para None."""
        with pytest.raises(TypeError, match="número válido"):
            calcular_iss(None)


class TestCalcularPISCOFINS:
    """Testes para função calcular_pis_cofins."""
    
    def test_calcular_pis_cofins_valor_padrao(self):
        """Testa cálculo de PIS/COFINS com valor padrão."""
        resultado = calcular_pis_cofins(1000)
        esperado = Decimal('92.50')  # (1.65% + 7.6%) = 9.25%
        assert resultado == esperado
    
    def test_calcular_pis_cofins_valor_decimal(self):
        """Testa cálculo com valor decimal específico."""
        resultado = calcular_pis_cofins(Decimal('5000.25'))
        # PIS: 5000.25 * 0.0165 = 82.50
        # COFINS: 5000.25 * 0.076 = 380.019
        # Total: 462.519 -> 462.52
        esperado = Decimal('462.52')
        assert resultado == esperado
    
    def test_calcular_pis_cofins_zero(self):
        """Testa PIS/COFINS para valor zero."""
        resultado = calcular_pis_cofins(0)
        esperado = Decimal('0.00')
        assert resultado == esperado
    
    def test_calcular_pis_cofins_valor_negativo_levanta_excecao(self):
        """Testa se ValueError é lançada para valor negativo."""
        with pytest.raises(ValueError, match="não pode ser negativo"):
            calcular_pis_cofins(-1000)


class TestTotalImpostos:
    """Testes para função total_impostos."""
    
    def test_total_impostos_apenas_vendas(self):
        """Testa cálculo apenas com vendas (ICMS)."""
        resultado = total_impostos(valor_venda=1000)
        
        assert resultado['icms'] == Decimal('180.00')
        assert resultado['iss'] == Decimal('0.00')
        assert resultado['pis_cofins'] == Decimal('0.00')
        assert resultado['total'] == Decimal('180.00')
    
    def test_total_impostos_apenas_servicos(self):
        """Testa cálculo apenas com serviços (ISS)."""
        resultado = total_impostos(valor_servico=2000)
        
        assert resultado['icms'] == Decimal('0.00')
        assert resultado['iss'] == Decimal('100.00')
        assert resultado['pis_cofins'] == Decimal('0.00')
        assert resultado['total'] == Decimal('100.00')
    
    def test_total_impostos_apenas_receita(self):
        """Testa cálculo apenas com receita (PIS/COFINS)."""
        resultado = total_impostos(valor_receita=1000)
        
        assert resultado['icms'] == Decimal('0.00')
        assert resultado['iss'] == Decimal('0.00')
        assert resultado['pis_cofins'] == Decimal('92.50')
        assert resultado['total'] == Decimal('92.50')
    
    def test_total_impostos_todos_valores(self):
        """Testa cálculo com todos os tipos de valor."""
        resultado = total_impostos(
            valor_venda=1000,
            valor_servico=500,
            valor_receita=1500
        )
        
        # ICMS: 1000 * 0.18 = 180.00
        # ISS: 500 * 0.05 = 25.00
        # PIS/COFINS: 1500 * 0.0925 = 138.75
        # Total: 343.75
        
        assert resultado['icms'] == Decimal('180.00')
        assert resultado['iss'] == Decimal('25.00')
        assert resultado['pis_cofins'] == Decimal('138.75')
        assert resultado['total'] == Decimal('343.75')
    
    def test_total_impostos_valores_padrao(self):
        """Testa comportamento com valores padrão (todos zero)."""
        resultado = total_impostos()
        
        assert resultado['icms'] == Decimal('0.00')
        assert resultado['iss'] == Decimal('0.00')
        assert resultado['pis_cofins'] == Decimal('0.00')
        assert resultado['total'] == Decimal('0.00')
    
    def test_total_impostos_propaga_excecoes(self):
        """Testa se exceções das funções individuais são propagadas."""
        with pytest.raises(ValueError):
            total_impostos(valor_venda=-100)
        
        with pytest.raises(ValueError):
            total_impostos(valor_servico=-500)
        
        with pytest.raises(ValueError):
            total_impostos(valor_receita=-1000)


class TestFormatarValorMonetario:
    """Testes para função formatar_valor_monetario."""
    
    def test_formatar_valor_simples(self):
        """Testa formatação de valor simples."""
        resultado = formatar_valor_monetario(Decimal('123.45'))
        assert resultado == "R$ 123,45"
    
    def test_formatar_valor_com_milhares(self):
        """Testa formatação com separador de milhares."""
        resultado = formatar_valor_monetario(Decimal('1234.56'))
        assert resultado == "R$ 1.234,56"
    
    def test_formatar_valor_zero(self):
        """Testa formatação de valor zero."""
        resultado = formatar_valor_monetario(Decimal('0.00'))
        assert resultado == "R$ 0,00"
    
    def test_formatar_valor_centavos(self):
        """Testa formatação de valor apenas em centavos."""
        resultado = formatar_valor_monetario(Decimal('0.05'))
        assert resultado == "R$ 0,05"
    
    def test_formatar_valor_grande(self):
        """Testa formatação de valor grande."""
        resultado = formatar_valor_monetario(Decimal('1234567.89'))
        assert resultado == "R$ 1.234.567,89"


class TestCasosLimites:
    """Testes para casos limites e edge cases."""
    
    def test_valores_muito_pequenos(self):
        """Testa comportamento com valores muito pequenos."""
        # Valor que resulta em imposto < 0.01
        resultado_icms = calcular_icms(Decimal('0.001'))
        assert resultado_icms == Decimal('0.00')
        
        resultado_iss = calcular_iss(Decimal('0.001'))
        assert resultado_iss == Decimal('0.00')
    
    def test_valores_muito_grandes(self):
        """Testa comportamento com valores muito grandes."""
        valor_grande = Decimal('999999999.99')
        
        # Deve funcionar sem overflow
        resultado_icms = calcular_icms(valor_grande)
        assert resultado_icms == Decimal('179999999.80')
        
        resultado_iss = calcular_iss(valor_grande)
        assert resultado_iss == Decimal('50000000.00')
    
    def test_precisao_decimal_preservada(self):
        """Testa se a precisão decimal é preservada em cálculos encadeados."""
        valor = Decimal('123.456')
        
        resultado = total_impostos(
            valor_venda=valor,
            valor_servico=valor,
            valor_receita=valor
        )
        
        # Verifica que todos os valores têm exatamente 2 casas decimais
        for key, value in resultado.items():
            if key != 'total':  # total é calculado separadamente
                assert len(str(value).split('.')[-1]) <= 2


# Fixtures para testes mais complexos
@pytest.fixture
def dados_empresa_exemplo():
    """Fixture com dados de exemplo para uma empresa."""
    return {
        'vendas_mes': Decimal('50000.00'),
        'servicos_mes': Decimal('20000.00'),
        'receita_total': Decimal('70000.00')
    }


def test_cenario_empresa_real(dados_empresa_exemplo):
    """Testa cenário com dados realistas de uma empresa."""
    dados = dados_empresa_exemplo
    
    resultado = total_impostos(
        valor_venda=dados['vendas_mes'],
        valor_servico=dados['servicos_mes'],
        valor_receita=dados['receita_total']
    )
    
    # Verificações de negócio
    assert resultado['icms'] == Decimal('9000.00')  # 50k * 18%
    assert resultado['iss'] == Decimal('1000.00')   # 20k * 5%
    assert resultado['pis_cofins'] == Decimal('6475.00')  # 70k * 9.25%
    assert resultado['total'] == Decimal('16475.00')
    
    # Carga tributária total: ~23.5%
    carga_tributaria = resultado['total'] / dados['receita_total'] * 100
    assert 23 <= carga_tributaria <= 24


# Testes de performance (opcional)
@pytest.mark.benchmark
def test_performance_calculo_impostos(benchmark):
    """Testa performance do cálculo de impostos."""
    def calculo_complexo():
        return total_impostos(
            valor_venda=Decimal('10000.50'),
            valor_servico=Decimal('5000.25'),
            valor_receita=Decimal('15000.75')
        )
    
    resultado = benchmark(calculo_complexo)
    assert resultado['total'] > 0
