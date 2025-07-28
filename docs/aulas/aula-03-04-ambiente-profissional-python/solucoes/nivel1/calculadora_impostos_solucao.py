"""
Solução do Exercício 1.1: Calculadora de Impostos

Esta implementação demonstra boas práticas para cálculos financeiros
em Python, incluindo uso de Decimal para precisão, validações robustas
e documentação completa.

Autor: Professor - Disciplina POO II
Data: 2025-01-23
"""

from decimal import Decimal, InvalidOperation
from typing import Union

# Type alias para melhor legibilidade
Numero = Union[int, float, Decimal]


def calcular_icms(valor_venda: Numero) -> Decimal:
    """
    Calcula o ICMS (18%) sobre o valor da venda.
    
    O ICMS (Imposto sobre Circulação de Mercadorias e Serviços) é um
    imposto estadual brasileiro calculado sobre o valor da operação.
    
    Args:
        valor_venda: Valor base para cálculo do ICMS. Deve ser >= 0.
        
    Returns:
        Valor do ICMS calculado com precisão de 2 casas decimais.
        
    Raises:
        ValueError: Se valor_venda for negativo.
        TypeError: Se valor_venda não for um número válido.
        
    Example:
        >>> calcular_icms(100)
        Decimal('18.00')
        >>> calcular_icms(Decimal('1000.50'))
        Decimal('180.09')
    """
    # Validação de tipo - converte para Decimal para precisão
    try:
        valor = Decimal(str(valor_venda))
    except (InvalidOperation, TypeError) as e:
        raise TypeError(f"Valor deve ser um número válido, recebido: {valor_venda}") from e
    
    # Validação de valor negativo
    if valor < 0:
        raise ValueError(f"Valor da venda não pode ser negativo: {valor}")
    
    # Cálculo do ICMS (18%)
    # Usamos quantize para garantir 2 casas decimais
    icms = valor * Decimal('0.18')
    return icms.quantize(Decimal('0.01'))


def calcular_iss(valor_servico: Numero) -> Decimal:
    """
    Calcula o ISS (5%) sobre o valor do serviço.
    
    O ISS (Imposto sobre Serviços) é um imposto municipal brasileiro
    calculado sobre o valor dos serviços prestados.
    
    Args:
        valor_servico: Valor base para cálculo do ISS. Deve ser >= 0.
        
    Returns:
        Valor do ISS calculado com precisão de 2 casas decimais.
        
    Raises:
        ValueError: Se valor_servico for negativo.
        TypeError: Se valor_servico não for um número válido.
        
    Example:
        >>> calcular_iss(1000)
        Decimal('50.00')
        >>> calcular_iss(Decimal('2500.75'))
        Decimal('125.04')
    """
    try:
        valor = Decimal(str(valor_servico))
    except (InvalidOperation, TypeError) as e:
        raise TypeError(f"Valor deve ser um número válido, recebido: {valor_servico}") from e
    
    if valor < 0:
        raise ValueError(f"Valor do serviço não pode ser negativo: {valor}")
    
    # Cálculo do ISS (5%)
    iss = valor * Decimal('0.05')
    return iss.quantize(Decimal('0.01'))


def calcular_pis_cofins(valor_receita: Numero) -> Decimal:
    """
    Calcula PIS (1.65%) + COFINS (7.6%) sobre o valor da receita.
    
    PIS e COFINS são contribuições federais calculadas sobre a receita
    bruta das empresas. As alíquotas padrão são:
    - PIS: 1.65%
    - COFINS: 7.6%
    
    Args:
        valor_receita: Valor base para cálculo. Deve ser >= 0.
        
    Returns:
        Valor total de PIS + COFINS com precisão de 2 casas decimais.
        
    Raises:
        ValueError: Se valor_receita for negativo.
        TypeError: Se valor_receita não for um número válido.
        
    Example:
        >>> calcular_pis_cofins(1000)
        Decimal('92.50')
        >>> calcular_pis_cofins(Decimal('5000.25'))
        Decimal('462.52')
    """
    try:
        valor = Decimal(str(valor_receita))
    except (InvalidOperation, TypeError) as e:
        raise TypeError(f"Valor deve ser um número válido, recebido: {valor_receita}") from e
    
    if valor < 0:
        raise ValueError(f"Valor da receita não pode ser negativo: {valor}")
    
    # Cálculo separado para maior clareza
    pis = valor * Decimal('0.0165')      # 1.65%
    cofins = valor * Decimal('0.076')    # 7.6%
    
    total = pis + cofins
    return total.quantize(Decimal('0.01'))


def total_impostos(
    valor_venda: Numero = 0,
    valor_servico: Numero = 0,
    valor_receita: Numero = 0
) -> dict[str, Decimal]:
    """
    Calcula todos os impostos de uma operação comercial.
    
    Esta função unifica o cálculo de todos os impostos, permitindo
    calcular ICMS (vendas), ISS (serviços) e PIS/COFINS (receita total)
    de forma integrada.
    
    Args:
        valor_venda: Valor das vendas para cálculo do ICMS (padrão: 0).
        valor_servico: Valor dos serviços para cálculo do ISS (padrão: 0).
        valor_receita: Valor da receita para PIS/COFINS (padrão: 0).
        
    Returns:
        Dicionário com os impostos calculados:
        - 'icms': Valor do ICMS
        - 'iss': Valor do ISS  
        - 'pis_cofins': Valor do PIS + COFINS
        - 'total': Soma de todos os impostos
        
    Raises:
        ValueError: Se algum valor for negativo.
        TypeError: Se algum valor não for um número válido.
        
    Example:
        >>> resultado = total_impostos(valor_venda=1000, valor_servico=500, valor_receita=1500)
        >>> resultado['total']
        Decimal('343.75')
        >>> resultado['icms']
        Decimal('180.00')
    """
    # Calcular cada imposto individualmente
    # Permite que cada função faça suas próprias validações
    icms = calcular_icms(valor_venda)
    iss = calcular_iss(valor_servico)
    pis_cofins = calcular_pis_cofins(valor_receita)
    
    # Calcular total
    total = icms + iss + pis_cofins
    
    return {
        'icms': icms,
        'iss': iss,
        'pis_cofins': pis_cofins,
        'total': total.quantize(Decimal('0.01'))
    }


def formatar_valor_monetario(valor: Decimal) -> str:
    """
    Formata valor decimal como moeda brasileira.
    
    Função utilitária para apresentação de valores monetários
    no formato brasileiro (R$ XXX.XXX,XX).
    
    Args:
        valor: Valor decimal a ser formatado.
        
    Returns:
        String formatada como moeda brasileira.
        
    Example:
        >>> formatar_valor_monetario(Decimal('1234.56'))
        'R$ 1.234,56'
        >>> formatar_valor_monetario(Decimal('0.05'))
        'R$ 0,05'
    """
    # Converte para string com formato brasileiro
    valor_str = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"R$ {valor_str}"


# Exemplo de uso interativo
if __name__ == "__main__":
    """
    Demonstração interativa da calculadora de impostos.
    
    Execute este arquivo diretamente para ver exemplos práticos
    dos cálculos implementados.
    """
    print("=== Calculadora de Impostos Brasileiros ===\n")
    
    # Exemplo 1: Empresa de comércio
    print("Exemplo 1: Empresa de Comércio")
    vendas = Decimal('10000.00')
    resultado = total_impostos(valor_venda=vendas, valor_receita=vendas)
    
    print(f"Vendas: {formatar_valor_monetario(vendas)}")
    print(f"ICMS (18%): {formatar_valor_monetario(resultado['icms'])}")
    print(f"PIS/COFINS (9.25%): {formatar_valor_monetario(resultado['pis_cofins'])}")
    print(f"Total de impostos: {formatar_valor_monetario(resultado['total'])}")
    print()
    
    # Exemplo 2: Empresa de serviços
    print("Exemplo 2: Empresa de Serviços")
    servicos = Decimal('5000.00')
    resultado = total_impostos(valor_servico=servicos, valor_receita=servicos)
    
    print(f"Serviços: {formatar_valor_monetario(servicos)}")
    print(f"ISS (5%): {formatar_valor_monetario(resultado['iss'])}")
    print(f"PIS/COFINS (9.25%): {formatar_valor_monetario(resultado['pis_cofins'])}")
    print(f"Total de impostos: {formatar_valor_monetario(resultado['total'])}")
    print()
    
    # Exemplo 3: Empresa mista
    print("Exemplo 3: Empresa Mista (Comércio + Serviços)")
    vendas = Decimal('8000.00')
    servicos = Decimal('3000.00')
    receita_total = vendas + servicos
    
    resultado = total_impostos(
        valor_venda=vendas,
        valor_servico=servicos,
        valor_receita=receita_total
    )
    
    print(f"Vendas: {formatar_valor_monetario(vendas)}")
    print(f"Serviços: {formatar_valor_monetario(servicos)}")
    print(f"Receita Total: {formatar_valor_monetario(receita_total)}")
    print(f"ICMS: {formatar_valor_monetario(resultado['icms'])}")
    print(f"ISS: {formatar_valor_monetario(resultado['iss'])}")
    print(f"PIS/COFINS: {formatar_valor_monetario(resultado['pis_cofins'])}")
    print(f"Total de impostos: {formatar_valor_monetario(resultado['total'])}")
    
    # Calcular carga tributária
    carga_tributaria = (resultado['total'] / receita_total) * 100
    print(f"Carga tributária: {carga_tributaria:.2f}%")
