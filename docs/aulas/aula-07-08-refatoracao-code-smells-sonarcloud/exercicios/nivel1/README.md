# 🔵 Nível 1 - Exercícios Básicos

## Exercício 1.1: Extract Method - Calculadora de Impostos

### Contexto e Motivação

Você herdou o código de uma calculadora de impostos que funciona corretamente, mas é difícil de manter e testar. O método principal está muito longo e contém múltiplas responsabilidades.

### Código Inicial

```python
# calculadora_impostos.py
class CalculadoraImpostos:
    """Calculadora de impostos com code smells intencionais."""
    
    def calcular_impostos_totais(self, salario_bruto: float, tem_dependentes: bool, 
                                plano_saude: str, contribuicao_previdencia: float) -> dict:
        """
        PROBLEMAS IDENTIFICADOS:
        - Long Method (35+ linhas)
        - Multiple Responsibilities (cálculo IRRF, INSS, dedução)
        - Long Parameter List (4+ parâmetros)
        - Magic Numbers espalhados pelo código
        - Dificuldade para testar componentes isoladamente
        """
        
        # Cálculo do INSS (8 linhas)
        if salario_bruto <= 1100:
            inss = salario_bruto * 0.075
        elif salario_bruto <= 2203.48:
            inss = salario_bruto * 0.09
        elif salario_bruto <= 3305.22:
            inss = salario_bruto * 0.12
        elif salario_bruto <= 6433.57:
            inss = salario_bruto * 0.14
        else:
            inss = 6433.57 * 0.14  # Teto do INSS
            
        # Base de cálculo para IRRF (10 linhas)
        base_irrf = salario_bruto - inss - contribuicao_previdencia
        
        # Dedução por dependentes
        if tem_dependentes:
            deducao_dependentes = 189.59 * 2  # Assumindo 2 dependentes
        else:
            deducao_dependentes = 0
            
        # Dedução plano de saúde
        if plano_saude == "basic":
            deducao_saude = 150.00
        elif plano_saude == "premium":
            deducao_saude = 300.00
        else:
            deducao_saude = 0
            
        base_irrf = base_irrf - deducao_dependentes - deducao_saude
        
        # Cálculo do IRRF (12 linhas)
        if base_irrf <= 1903.98:
            irrf = 0
            aliquota_irrf = 0
        elif base_irrf <= 2826.65:
            irrf = base_irrf * 0.075 - 142.80
            aliquota_irrf = 0.075
        elif base_irrf <= 3751.05:
            irrf = base_irrf * 0.15 - 354.80
            aliquota_irrf = 0.15
        elif base_irrf <= 4664.68:
            irrf = base_irrf * 0.225 - 636.13
            aliquota_irrf = 0.225
        else:
            irrf = base_irrf * 0.275 - 869.36
            aliquota_irrf = 0.275
            
        # Cálculo do salário líquido
        salario_liquido = salario_bruto - inss - irrf
        
        return {
            "salario_bruto": salario_bruto,
            "inss": inss,
            "irrf": irrf,
            "deducao_dependentes": deducao_dependentes,
            "deducao_saude": deducao_saude,
            "base_irrf": base_irrf,
            "aliquota_irrf": aliquota_irrf,
            "salario_liquido": salario_liquido
        }

# Exemplo de uso
if __name__ == "__main__":
    calc = CalculadoraImpostos()
    resultado = calc.calcular_impostos_totais(5000.00, True, "premium", 200.00)
    print(f"Salário líquido: R$ {resultado['salario_liquido']:.2f}")
```

### Requisitos

1. **Aplicar Extract Method** para decompor o método principal
2. **Eliminar Magic Numbers** criando constantes nomeadas
3. **Reduzir complexidade ciclomática** de ~8 para ~2 no método principal
4. **Manter comportamento idêntico** (mesmos resultados para mesmas entradas)
5. **Melhorar testabilidade** (cada cálculo testável isoladamente)

### Restrições Técnicas

- Manter a interface pública inalterada
- Não usar bibliotecas externas
- Preservar precisão dos cálculos (até 2 casas decimais)
- Cada método extraído deve ter no máximo 10 linhas

### Dicas

1. **Identifique responsabilidades claras:** INSS, IRRF, deduções, salário líquido
2. **Comece pelos cálculos mais simples:** INSS é mais direto que IRRF
3. **Use constantes para faixas:** Facilita manutenção e legibilidade
4. **Teste cada método extraído** antes de partir para o próximo

### Resultado Esperado

```python
# Estrutura esperada após refatoração
class CalculadoraImpostosRefatorada:
    
    def calcular_impostos_totais(self, salario_bruto: float, tem_dependentes: bool, 
                                plano_saude: str, contribuicao_previdencia: float) -> dict:
        # Método principal com ~5 linhas, apenas coordenando cálculos
        pass
    
    def _calcular_inss(self, salario_bruto: float) -> float:
        # Lógica específica do INSS
        pass
    
    def _calcular_deducoes(self, tem_dependentes: bool, plano_saude: str) -> float:
        # Lógica de deduções
        pass
    
    def _calcular_irrf(self, base_calculo: float) -> tuple[float, float]:
        # Lógica específica do IRRF, retorna (valor, alíquota)
        pass
```

### Extensões (Opcionais)

1. **Criar enum para tipos de plano de saúde**
2. **Adicionar validação de entrada** (salários negativos, etc.)
3. **Implementar diferentes regras por ano** (2023, 2024, etc.)
4. **Adicionar cálculo de outras deduções** (educação, previdência privada)

---

## Exercício 1.2: Replace Conditional with Polymorphism - Sistema de Desconto

### Contexto e Motivação

Um e-commerce possui um sistema de descontos que usa múltiplas condicionais para diferentes tipos de cliente. O código funciona, mas é difícil adicionar novos tipos de desconto e as regras estão espalhadas.

### Código Inicial

```python
# sistema_desconto.py
class SistemaDesconto:
    """Sistema de desconto com Switch Statement smell."""
    
    def calcular_desconto(self, tipo_cliente: str, valor_compra: float, 
                         quantidade_itens: int, primeiro_pedido: bool) -> dict:
        """
        PROBLEMAS IDENTIFICADOS:
        - Switch Statement complexo
        - Violação do Open/Closed Principle
        - Magic Numbers sem contexto
        - Lógica de negócio misturada com estruturas de controle
        - Dificuldade para adicionar novos tipos
        """
        
        if tipo_cliente == "bronze":
            if primeiro_pedido:
                desconto_percentual = 5.0
                desconto_fixo = 0.0
            else:
                if valor_compra > 100:
                    desconto_percentual = 2.0
                    desconto_fixo = 0.0
                else:
                    desconto_percentual = 0.0
                    desconto_fixo = 0.0
                    
        elif tipo_cliente == "silver":
            if primeiro_pedido:
                desconto_percentual = 10.0
                desconto_fixo = 5.0
            else:
                if valor_compra > 200:
                    desconto_percentual = 5.0
                    desconto_fixo = 0.0
                elif valor_compra > 100:
                    desconto_percentual = 3.0
                    desconto_fixo = 0.0
                else:
                    desconto_percentual = 0.0
                    desconto_fixo = 0.0
                    
        elif tipo_cliente == "gold":
            if primeiro_pedido:
                desconto_percentual = 15.0
                desconto_fixo = 10.0
            else:
                if quantidade_itens > 10:
                    desconto_percentual = 12.0
                    desconto_fixo = 5.0
                elif valor_compra > 300:
                    desconto_percentual = 8.0
                    desconto_fixo = 0.0
                else:
                    desconto_percentual = 5.0
                    desconto_fixo = 0.0
                    
        elif tipo_cliente == "platinum":
            if primeiro_pedido:
                desconto_percentual = 20.0
                desconto_fixo = 20.0
            else:
                if valor_compra > 500:
                    desconto_percentual = 18.0
                    desconto_fixo = 15.0
                elif valor_compra > 300:
                    desconto_percentual = 15.0
                    desconto_fixo = 10.0
                else:
                    desconto_percentual = 12.0
                    desconto_fixo = 5.0
        else:
            # Cliente regular
            desconto_percentual = 0.0
            desconto_fixo = 0.0
            
        # Aplicar descontos
        valor_desconto_percentual = valor_compra * (desconto_percentual / 100)
        valor_desconto_total = valor_desconto_percentual + desconto_fixo
        valor_final = valor_compra - valor_desconto_total
        
        return {
            "tipo_cliente": tipo_cliente,
            "valor_original": valor_compra,
            "desconto_percentual": desconto_percentual,
            "desconto_fixo": desconto_fixo,
            "valor_desconto_total": valor_desconto_total,
            "valor_final": max(valor_final, 0)  # Não pode ser negativo
        }

# Exemplo de uso
if __name__ == "__main__":
    sistema = SistemaDesconto()
    resultado = sistema.calcular_desconto("gold", 250.00, 8, False)
    print(f"Desconto aplicado: R$ {resultado['valor_desconto_total']:.2f}")
```

### Requisitos

1. **Implementar Strategy Pattern** para eliminar switch statement
2. **Criar hierarquia de classes** para diferentes tipos de cliente
3. **Usar polimorfismo** em vez de condicionais
4. **Facilitar adição de novos tipos** sem modificar código existente
5. **Manter interface pública** compatível

### Restrições Técnicas

- Usar ABC (Abstract Base Classes) do Python
- Preservar exatamente os mesmos valores de desconto
- Manter a estrutura do dict retornado
- Não usar bibliotecas externas

### Dicas

1. **Comece definindo a interface abstrata** (CalculadoraDesconto)
2. **Implemente uma estratégia por vez** (Bronze → Silver → Gold → Platinum)
3. **Use factory method** para criar instâncias das estratégias
4. **Teste cada estratégia isoladamente** antes de integrar

### Resultado Esperado

```python
# Estrutura esperada após refatoração
from abc import ABC, abstractmethod

class CalculadoraDesconto(ABC):
    @abstractmethod
    def calcular_desconto(self, valor_compra: float, quantidade_itens: int, 
                         primeiro_pedido: bool) -> dict:
        pass

class DescontoBronze(CalculadoraDesconto):
    # Implementação específica para Bronze
    pass

class DescontoSilver(CalculadoraDesconto):
    # Implementação específica para Silver
    pass

# ... outras estratégias

class SistemaDescontoRefatorado:
    def __init__(self):
        self.estrategias = {
            "bronze": DescontoBronze(),
            "silver": DescontoSilver(),
            # ...
        }
    
    def calcular_desconto(self, tipo_cliente: str, valor_compra: float, 
                         quantidade_itens: int, primeiro_pedido: bool) -> dict:
        # Método principal simplificado com delegação
        pass
```

### Extensões (Opcionais)

1. **Adicionar novo tipo "diamond"** sem modificar código existente
2. **Implementar descontos sazonais** (Black Friday, Natal)
3. **Criar configuração externa** para as regras de desconto
4. **Adicionar histórico de descontos** aplicados

---

## Exercício 1.3: Move Method - Sistema de Validação

### Contexto e Motivação

Um sistema de cadastro possui validações espalhadas em uma classe que também gerencia persistência. As validações estão no lugar errado, violando o princípio de responsabilidade única.

### Código Inicial

```python
# sistema_cadastro.py
import re
from typing import List, Optional

class GerenciadorUsuarios:
    """Classe com Feature Envy - métodos que deveriam estar em User."""
    
    def __init__(self):
        self.usuarios: List[dict] = []
    
    def validar_email(self, usuario: dict) -> bool:
        """
        FEATURE ENVY: Este método usa apenas dados do usuário,
        deveria estar na classe Usuario.
        """
        email = usuario.get("email", "")
        if not email:
            return False
        
        # Regex básico para validação de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validar_senha(self, usuario: dict) -> bool:
        """
        FEATURE ENVY: Validação deveria estar na classe Usuario.
        """
        senha = usuario.get("senha", "")
        if len(senha) < 8:
            return False
        
        # Verificar se tem pelo menos uma letra maiúscula
        if not any(c.isupper() for c in senha):
            return False
        
        # Verificar se tem pelo menos um número
        if not any(c.isdigit() for c in senha):
            return False
        
        # Verificar se tem pelo menos um caractere especial
        especiais = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in especiais for c in senha):
            return False
        
        return True
    
    def validar_idade(self, usuario: dict) -> bool:
        """
        FEATURE ENVY: Validação deveria estar na classe Usuario.
        """
        idade = usuario.get("idade", 0)
        return 18 <= idade <= 120
    
    def validar_nome(self, usuario: dict) -> bool:
        """
        FEATURE ENVY: Validação deveria estar na classe Usuario.
        """
        nome = usuario.get("nome", "").strip()
        if len(nome) < 2:
            return False
        
        # Verificar se contém apenas letras e espaços
        return all(c.isalpha() or c.isspace() for c in nome)
    
    def validar_usuario_completo(self, usuario: dict) -> dict:
        """
        Método que coordena todas as validações.
        PROBLEMA: Usa métodos que deveriam estar em outra classe.
        """
        erros = []
        
        if not self.validar_email(usuario):
            erros.append("Email inválido")
        
        if not self.validar_senha(usuario):
            erros.append("Senha deve ter 8+ caracteres, maiúscula, número e símbolo")
        
        if not self.validar_idade(usuario):
            erros.append("Idade deve estar entre 18 e 120 anos")
        
        if not self.validar_nome(usuario):
            erros.append("Nome deve ter 2+ caracteres e apenas letras")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros
        }
    
    def cadastrar_usuario(self, dados_usuario: dict) -> bool:
        """Método principal para cadastro."""
        validacao = self.validar_usuario_completo(dados_usuario)
        
        if not validacao["valido"]:
            print(f"Erros de validação: {validacao['erros']}")
            return False
        
        # Simular persistência
        self.usuarios.append(dados_usuario.copy())
        print(f"Usuário {dados_usuario['nome']} cadastrado com sucesso!")
        return True

# Exemplo de uso
if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios()
    
    usuario_teste = {
        "nome": "João Silva",
        "email": "joao@email.com", 
        "senha": "MinhaSenh@123",
        "idade": 30
    }
    
    gerenciador.cadastrar_usuario(usuario_teste)
```

### Requisitos

1. **Criar classe Usuario** para encapsular dados e validações
2. **Mover métodos de validação** para a classe Usuario
3. **Aplicar Move Method** sistematicamente
4. **Manter interface pública** do GerenciadorUsuarios
5. **Preservar funcionalidade** de cadastro

### Restrições Técnicas

- Não usar bibliotecas de validação externas
- Manter exatamente as mesmas regras de validação
- Preservar mensagens de erro idênticas
- Não alterar a interface do método cadastrar_usuario

### Dicas

1. **Identifique todos os métodos com Feature Envy** primeiro
2. **Crie a classe Usuario** com os dados como atributos
3. **Mova um método de validação por vez**
4. **Ajuste chamadas** no GerenciadorUsuarios após cada movimento

### Resultado Esperado

```python
# Estrutura esperada após refatoração
class Usuario:
    def __init__(self, nome: str, email: str, senha: str, idade: int):
        self.nome = nome
        self.email = email  
        self.senha = senha
        self.idade = idade
    
    def validar_email(self) -> bool:
        # Lógica movida do GerenciadorUsuarios
        pass
    
    def validar_senha(self) -> bool:
        # Lógica movida do GerenciadorUsuarios
        pass
    
    def validar_idade(self) -> bool:
        # Lógica movida do GerenciadorUsuarios
        pass
    
    def validar_nome(self) -> bool:
        # Lógica movida do GerenciadorUsuarios
        pass
    
    def validar_completo(self) -> dict:
        # Coordena todas as validações
        pass

class GerenciadorUsuariosRefatorado:
    def __init__(self):
        self.usuarios: List[Usuario] = []
    
    def cadastrar_usuario(self, dados_usuario: dict) -> bool:
        # Cria instância de Usuario e delega validação
        pass
```

### Extensões (Opcionais)

1. **Adicionar validação de CPF** na classe Usuario
2. **Implementar diferentes níveis de validação** (básica, avançada)
3. **Criar decorator para validações** automáticas
4. **Adicionar serialização/deserialização** da classe Usuario

---

## Critérios de Avaliação - Nível 1

### Exercício 1.1 - Extract Method
- ✅ Método principal reduzido para < 10 linhas
- ✅ Pelo menos 4 métodos extraídos (INSS, IRRF, deduções, líquido)
- ✅ Complexidade ciclomática do método principal ≤ 3
- ✅ Constantes nomeadas para magic numbers
- ✅ Comportamento preservado (testes passam)

### Exercício 1.2 - Replace Conditional
- ✅ Switch statement eliminado
- ✅ Strategy pattern implementado com ABC
- ✅ Pelo menos 4 estratégias criadas (Bronze, Silver, Gold, Platinum)
- ✅ Factory method para criar estratégias
- ✅ Facilidade para adicionar novos tipos

### Exercício 1.3 - Move Method
- ✅ Classe Usuario criada com validações próprias
- ✅ Pelo menos 4 métodos movidos
- ✅ Feature Envy eliminado
- ✅ Encapsulamento adequado
- ✅ Interface pública preservada

### Pontuação
- **Excepcional (90-100%):** Todos os critérios + extensões implementadas
- **Satisfatório (70-89%):** Todos os critérios obrigatórios atendidos
- **Parcial (50-69%):** Maioria dos critérios com pequenas falhas
- **Insuficiente (<50%):** Critérios essenciais não atendidos
