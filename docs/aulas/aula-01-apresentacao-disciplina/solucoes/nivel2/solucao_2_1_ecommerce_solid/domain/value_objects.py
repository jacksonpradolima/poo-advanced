#!/usr/bin/env python3
"""
Value Objects do Sistema de E-commerce

RESPONSABILIDADE: Objetos imutáveis que representam conceitos importantes
do domínio sem identidade própria.

PRINCÍPIOS SOLID APLICADOS:
- SRP: Cada value object tem responsabilidade específica
- OCP: Novos value objects podem ser adicionados sem modificar existentes
- LSP: Todos implementam corretamente igualdade e imutabilidade
- ISP: Interfaces focadas e específicas
- DIP: Não dependem de implementações concretas

AUTOR: Prof. Jackson Antonio do Prado Lima
DATA: 2024-12-19
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple
from enum import Enum
import re


# =============================================================================
# ENUMS PARA TYPE SAFETY
# =============================================================================

class TipoProduto(Enum):
    """Enum para tipos de produtos (Type Safety)"""
    FISICO = "fisico"
    DIGITAL = "digital"
    SERVICO = "servico"


class StatusPedido(Enum):
    """Estados válidos de um pedido"""
    CRIADO = "criado"
    CONFIRMADO = "confirmado"
    PAGO = "pago"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class TipoNotificacao(Enum):
    """Tipos de notificação disponíveis"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


# =============================================================================
# VALUE OBJECTS PRINCIPAIS
# =============================================================================

@dataclass(frozen=True)
class Dinheiro:
    """
    ✅ Value Object para valores monetários
    
    PRINCÍPIOS APLICADOS:
    - SRP: Responsável apenas por representar e calcular valores monetários
    - Imutabilidade: Operações retornam novos objetos
    - Precisão: Usa Decimal para evitar problemas de ponto flutuante
    """
    valor: Decimal
    moeda: str = "BRL"
    
    def __post_init__(self):
        """Validações na inicialização"""
        if not isinstance(self.valor, Decimal):
            object.__setattr__(self, 'valor', Decimal(str(self.valor)))
        
        if self.valor < Decimal('0'):
            raise ValueError(f"Valor monetário não pode ser negativo: {self.valor}")
        
        if not self.moeda or len(self.moeda) != 3:
            raise ValueError(f"Código de moeda inválido: {self.moeda}")
        
        # Garantir 2 casas decimais
        valor_formatado = self.valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        object.__setattr__(self, 'valor', valor_formatado)
    
    def somar(self, outro: 'Dinheiro') -> 'Dinheiro':
        """Soma dois valores monetários"""
        self._validar_moeda_compativel(outro)
        return Dinheiro(self.valor + outro.valor, self.moeda)
    
    def subtrair(self, outro: 'Dinheiro') -> 'Dinheiro':
        """Subtrai dois valores monetários"""
        self._validar_moeda_compativel(outro)
        resultado = self.valor - outro.valor
        return Dinheiro(resultado, self.moeda)
    
    def multiplicar(self, fator: Decimal) -> 'Dinheiro':
        """Multiplica valor por um fator"""
        if not isinstance(fator, Decimal):
            fator = Decimal(str(fator))
        
        if fator < Decimal('0'):
            raise ValueError("Fator de multiplicação não pode ser negativo")
        
        return Dinheiro(self.valor * fator, self.moeda)
    
    def aplicar_percentual(self, percentual: Decimal) -> 'Dinheiro':
        """Aplica percentual ao valor (ex: 10% = Decimal('10'))"""
        if not isinstance(percentual, Decimal):
            percentual = Decimal(str(percentual))
        
        fator = percentual / Decimal('100')
        return self.multiplicar(fator)
    
    def eh_zero(self) -> bool:
        """Verifica se valor é zero"""
        return self.valor == Decimal('0')
    
    def eh_maior_que(self, outro: 'Dinheiro') -> bool:
        """Compara se é maior que outro valor"""
        self._validar_moeda_compativel(outro)
        return self.valor > outro.valor
    
    def eh_menor_que(self, outro: 'Dinheiro') -> bool:
        """Compara se é menor que outro valor"""
        self._validar_moeda_compativel(outro)
        return self.valor < outro.valor
    
    def _validar_moeda_compativel(self, outro: 'Dinheiro') -> None:
        """Valida se moedas são compatíveis para operação"""
        if self.moeda != outro.moeda:
            raise ValueError(f"Moedas incompatíveis: {self.moeda} vs {outro.moeda}")
    
    def __str__(self) -> str:
        """Representação string formatada"""
        simbolos_moeda = {"BRL": "R$", "USD": "$", "EUR": "€"}
        simbolo = simbolos_moeda.get(self.moeda, self.moeda)
        return f"{simbolo} {self.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def __repr__(self) -> str:
        """Representação técnica"""
        return f"Dinheiro(valor={self.valor}, moeda='{self.moeda}')"


@dataclass(frozen=True)
class DimensoesProduto:
    """
    ✅ Value Object para dimensões físicas de produtos
    
    PRINCÍPIOS APLICADOS:
    - SRP: Responsável apenas por representar dimensões
    - Validação: Garante valores positivos e realistas
    - Cálculos: Métodos para volume e peso volumétrico
    """
    altura: Decimal  # em centímetros
    largura: Decimal  # em centímetros
    profundidade: Decimal  # em centímetros
    peso: Decimal  # em quilogramas
    
    def __post_init__(self):
        """Validações das dimensões"""
        dimensoes = [self.altura, self.largura, self.profundidade, self.peso]
        
        for i, (nome, valor) in enumerate([
            ("altura", self.altura),
            ("largura", self.largura), 
            ("profundidade", self.profundidade),
            ("peso", self.peso)
        ]):
            if not isinstance(valor, Decimal):
                object.__setattr__(self, list(self.__dataclass_fields__.keys())[i], 
                                 Decimal(str(valor)))
            
            if valor <= Decimal('0'):
                raise ValueError(f"{nome} deve ser positiva: {valor}")
        
        # Validações de realismo (evitar erros de digitação)
        if self.altura > Decimal('500'):  # 5 metros
            raise ValueError(f"Altura muito grande: {self.altura}cm")
        
        if self.peso > Decimal('1000'):  # 1 tonelada
            raise ValueError(f"Peso muito grande: {self.peso}kg")
    
    def calcular_volume(self) -> Decimal:
        """Calcula volume em centímetros cúbicos"""
        return self.altura * self.largura * self.profundidade
    
    def calcular_peso_volumetrico(self, fator_divisao: Decimal = Decimal('5000')) -> Decimal:
        """
        Calcula peso volumétrico para frete.
        
        Args:
            fator_divisao: Fator padrão dos Correios (5000)
            
        Returns:
            Peso volumétrico em kg
        """
        volume_cm3 = self.calcular_volume()
        return volume_cm3 / fator_divisao
    
    def obter_maior_dimensao(self) -> Decimal:
        """Retorna a maior dimensão (para validações de transportadora)"""
        return max(self.altura, self.largura, self.profundidade)
    
    def __str__(self) -> str:
        """Representação amigável"""
        return f"{self.altura}x{self.largura}x{self.profundidade}cm, {self.peso}kg"


@dataclass(frozen=True)
class Endereco:
    """
    ✅ Value Object para endereços de entrega
    
    PRINCÍPIOS APLICADOS:
    - SRP: Responsável apenas por representar endereços
    - Validação: CEP, campos obrigatórios
    - Formatação: Representação padronizada
    """
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    uf: str
    pais: str = "Brasil"
    
    def __post_init__(self):
        """Validações do endereço"""
        # Validar CEP brasileiro
        cep_limpo = re.sub(r'[^0-9]', '', self.cep)
        if len(cep_limpo) != 8:
            raise ValueError(f"CEP inválido: {self.cep}")
        object.__setattr__(self, 'cep', f"{cep_limpo[:5]}-{cep_limpo[5:]}")
        
        # Validar campos obrigatórios
        campos_obrigatorios = {
            'logradouro': self.logradouro,
            'numero': self.numero,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'uf': self.uf
        }
        
        for campo, valor in campos_obrigatorios.items():
            if not valor or not valor.strip():
                raise ValueError(f"Campo {campo} é obrigatório")
        
        # Validar UF
        ufs_validas = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        if self.uf.upper() not in ufs_validas:
            raise ValueError(f"UF inválida: {self.uf}")
        
        object.__setattr__(self, 'uf', self.uf.upper())
    
    def eh_capital(self) -> bool:
        """Verifica se endereço é de uma capital (simplificado)"""
        capitais = {
            'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Belo Horizonte',
            'RS': 'Porto Alegre', 'PR': 'Curitiba', 'SC': 'Florianópolis',
            'DF': 'Brasília', 'GO': 'Goiânia', 'BA': 'Salvador'
        }
        capital_uf = capitais.get(self.uf)
        return capital_uf and capital_uf.lower() in self.cidade.lower()
    
    def obter_regiao(self) -> str:
        """Retorna região do Brasil baseada na UF"""
        regioes = {
            'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
            'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
            'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
            'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
            'Sul': ['PR', 'RS', 'SC']
        }
        
        for regiao, ufs in regioes.items():
            if self.uf in ufs:
                return regiao
        return "Desconhecida"
    
    def calcular_distancia_aproximada(self, outro: 'Endereco') -> int:
        """
        Calcula distância aproximada entre CEPs (simplificado).
        
        Em sistema real, usaria API de geocodificação.
        """
        if self.uf == outro.uf:
            if self.cidade.lower() == outro.cidade.lower():
                return 10  # Mesma cidade
            return 100  # Mesmo estado
        
        if self.obter_regiao() == outro.obter_regiao():
            return 300  # Mesma região
        
        return 800  # Regiões diferentes
    
    def __str__(self) -> str:
        """Formatação completa do endereço"""
        complemento_str = f", {self.complemento}" if self.complemento else ""
        return (f"{self.logradouro}, {self.numero}{complemento_str}\n"
                f"{self.bairro}, {self.cidade} - {self.uf}\n"
                f"CEP: {self.cep}")


@dataclass(frozen=True)
class InformacaoDigital:
    """
    ✅ Value Object para informações de produtos digitais
    
    PRINCÍPIOS APLICADOS:
    - SRP: Específico para produtos digitais
    - Validação: Tamanho de arquivo e formato
    """
    tamanho_arquivo_mb: Decimal
    formato: str
    url_download: str
    chave_licenca: Optional[str] = None
    
    def __post_init__(self):
        """Validações para produtos digitais"""
        if self.tamanho_arquivo_mb <= Decimal('0'):
            raise ValueError("Tamanho do arquivo deve ser positivo")
        
        if self.tamanho_arquivo_mb > Decimal('10000'):  # 10GB
            raise ValueError("Arquivo muito grande")
        
        formatos_validos = ['pdf', 'mp4', 'zip', 'exe', 'dmg', 'apk', 'ebook']
        if self.formato.lower() not in formatos_validos:
            raise ValueError(f"Formato não suportado: {self.formato}")
        
        if not self.url_download or not self.url_download.startswith(('http://', 'https://')):
            raise ValueError("URL de download inválida")
    
    def eh_arquivo_grande(self) -> bool:
        """Verifica se é arquivo grande (> 1GB)"""
        return self.tamanho_arquivo_mb > Decimal('1024')
    
    def tempo_download_estimado(self, velocidade_mbps: Decimal = Decimal('10')) -> int:
        """
        Estima tempo de download em segundos.
        
        Args:
            velocidade_mbps: Velocidade da conexão em Mbps
            
        Returns:
            Tempo estimado em segundos
        """
        if velocidade_mbps <= Decimal('0'):
            raise ValueError("Velocidade deve ser positiva")
        
        # Conversão: MB para Mb e depois para segundos
        tamanho_mb = self.tamanho_arquivo_mb * Decimal('8')  # MB para Mb
        tempo_segundos = tamanho_mb / velocidade_mbps
        return int(tempo_segundos)
    
    def __str__(self) -> str:
        return f"{self.formato.upper()} - {self.tamanho_arquivo_mb}MB"


@dataclass(frozen=True)
class InformacaoServico:
    """
    ✅ Value Object para informações de serviços
    
    PRINCÍPIOS APLICADOS:
    - SRP: Específico para serviços
    - Validação: Duração e categoria
    """
    duracao_horas: Decimal
    categoria: str
    requer_presenca: bool = False
    
    def __post_init__(self):
        """Validações para serviços"""
        if self.duracao_horas <= Decimal('0'):
            raise ValueError("Duração deve ser positiva")
        
        if self.duracao_horas > Decimal('8760'):  # 1 ano
            raise ValueError("Duração muito longa")
        
        categorias_validas = [
            'consultoria', 'manutencao', 'instalacao', 'treinamento',
            'suporte', 'desenvolvimento', 'design'
        ]
        if self.categoria.lower() not in categorias_validas:
            raise ValueError(f"Categoria inválida: {self.categoria}")
    
    def eh_servico_longo(self) -> bool:
        """Verifica se é serviço de longa duração (> 40h)"""
        return self.duracao_horas > Decimal('40')
    
    def calcular_dias_trabalho(self, horas_por_dia: Decimal = Decimal('8')) -> Decimal:
        """Calcula quantos dias de trabalho são necessários"""
        if horas_por_dia <= Decimal('0') or horas_por_dia > Decimal('24'):
            raise ValueError("Horas por dia deve estar entre 0 e 24")
        
        return (self.duracao_horas / horas_por_dia).quantize(
            Decimal('0.1'), rounding=ROUND_HALF_UP
        )
    
    def __str__(self) -> str:
        presenca = "Presencial" if self.requer_presenca else "Remoto"
        return f"{self.categoria.title()} - {self.duracao_horas}h ({presenca})"


# =============================================================================
# VALUE OBJECTS AUXILIARES
# =============================================================================

@dataclass(frozen=True)
class ResultadoCalculoFrete:
    """Value Object para resultado do cálculo de frete"""
    valor: Dinheiro
    prazo_dias: int
    transportadora: str
    servico: str
    detalhes: str = ""
    
    def __post_init__(self):
        if self.prazo_dias < 0:
            raise ValueError("Prazo não pode ser negativo")
        
        if self.prazo_dias > 365:
            raise ValueError("Prazo muito longo")
    
    def __str__(self) -> str:
        return f"{self.transportadora} - {self.servico}: {self.valor} em {self.prazo_dias} dias"


@dataclass(frozen=True)
class DadosPagamento:
    """Value Object para dados de pagamento"""
    numero_cartao: str
    nome_titular: str
    cvv: str
    mes_vencimento: int
    ano_vencimento: int
    
    def __post_init__(self):
        # Validações básicas (em produção seria mais robusta)
        if len(self.numero_cartao.replace(' ', '')) != 16:
            raise ValueError("Número do cartão inválido")
        
        if len(self.cvv) not in [3, 4]:
            raise ValueError("CVV inválido")
        
        if not (1 <= self.mes_vencimento <= 12):
            raise ValueError("Mês de vencimento inválido")
        
        if self.ano_vencimento < 2024:
            raise ValueError("Cartão vencido")
    
    def obter_numero_mascarado(self) -> str:
        """Retorna número do cartão mascarado"""
        numero_limpo = self.numero_cartao.replace(' ', '')
        return f"****-****-****-{numero_limpo[-4:]}"
    
    def __str__(self) -> str:
        return f"Cartão {self.obter_numero_mascarado()} - {self.nome_titular}"


# =============================================================================
# FACTORY PARA VALUE OBJECTS (Bonus)
# =============================================================================

class FabricaValueObjects:
    """
    ✅ Factory para criação de Value Objects
    
    BENEFÍCIOS:
    - Centraliza validações complexas
    - Facilita criação a partir de dados externos
    - Permite diferentes formatos de entrada
    """
    
    @staticmethod
    def criar_dinheiro(valor, moeda: str = "BRL") -> Dinheiro:
        """Cria objeto Dinheiro com conversão automática"""
        if isinstance(valor, str):
            # Remove formatação brasileira
            valor_limpo = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return Dinheiro(Decimal(valor_limpo), moeda)
        
        return Dinheiro(Decimal(str(valor)), moeda)
    
    @staticmethod
    def criar_endereco_simples(cep: str, numero: str, complemento: str = None) -> Endereco:
        """
        Cria endereço básico (em produção consultaria API dos Correios)
        """
        # Simulação de consulta de CEP
        mock_dados_cep = {
            "01310-100": ("Av. Paulista", "Bela Vista", "São Paulo", "SP"),
            "20040-020": ("Rua da Assembleia", "Centro", "Rio de Janeiro", "RJ"),
            "30112-000": ("Av. Afonso Pena", "Centro", "Belo Horizonte", "MG")
        }
        
        cep_limpo = re.sub(r'[^0-9]', '', cep)
        cep_formatado = f"{cep_limpo[:5]}-{cep_limpo[5:]}"
        
        if cep_formatado in mock_dados_cep:
            logradouro, bairro, cidade, uf = mock_dados_cep[cep_formatado]
        else:
            # Dados genéricos para demonstração
            logradouro = "Rua Exemplo"
            bairro = "Bairro Exemplo"
            cidade = "Cidade Exemplo"
            uf = "SP"
        
        return Endereco(
            cep=cep_formatado,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            uf=uf
        )
    
    @staticmethod
    def criar_dimensoes_produto(altura_cm: float, largura_cm: float, 
                               profundidade_cm: float, peso_kg: float) -> DimensoesProduto:
        """Cria dimensões com conversão automática"""
        return DimensoesProduto(
            altura=Decimal(str(altura_cm)),
            largura=Decimal(str(largura_cm)),
            profundidade=Decimal(str(profundidade_cm)),
            peso=Decimal(str(peso_kg))
        )


# =============================================================================
# EXPORTAÇÕES
# =============================================================================

__all__ = [
    # Enums
    'TipoProduto', 'StatusPedido', 'TipoNotificacao',
    
    # Value Objects principais
    'Dinheiro', 'DimensoesProduto', 'Endereco',
    'InformacaoDigital', 'InformacaoServico',
    
    # Value Objects auxiliares
    'ResultadoCalculoFrete', 'DadosPagamento',
    
    # Factory
    'FabricaValueObjects'
]
