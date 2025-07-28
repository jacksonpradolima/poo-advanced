# 🟡 Nível 2 - Exercícios Intermediários

## Exercício 2.1: Sistema de Biblioteca - Refatoração Completa

### Contexto e Motivação

Você foi contratado para modernizar o sistema de gerenciamento de uma biblioteca universitária. O código atual funciona, mas apresenta múltiplos code smells que dificultam manutenção e adição de novas funcionalidades. A biblioteca planeja implementar recursos como reservas online, multas automáticas e integração com sistemas acadêmicos.

### Código Inicial

```python
# sistema_biblioteca.py
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class SistemaBiblioteca:
    """
    Sistema de biblioteca com múltiplos code smells.
    
    PROBLEMAS IDENTIFICADOS:
    - God Class (150+ linhas, múltiplas responsabilidades)
    - Long Methods (alguns com 30+ linhas)
    - Data Clumps (dados de livro, usuário sempre juntos)
    - Primitive Obsession (strings/dicts em vez de objetos)
    - Duplicated Code (validações repetidas)
    - Feature Envy (métodos que deveriam estar em outras classes)
    """
    
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []
        self.reservas = []
        self.configuracoes = {
            "dias_emprestimo": 14,
            "multa_dia": 2.00,
            "max_emprestimos": 3,
            "max_reservas": 2
        }
    
    def cadastrar_livro(self, titulo: str, autor: str, isbn: str, categoria: str, 
                       quantidade: int, ano_publicacao: int) -> bool:
        """
        DATA CLUMPS: Sempre passamos os mesmos dados de livro juntos.
        LONG PARAMETER LIST: 6 parâmetros são muitos.
        """
        # Validações repetitivas
        if not titulo or len(titulo.strip()) < 2:
            return False
        if not autor or len(autor.strip()) < 2:
            return False
        if not isbn or len(isbn) not in [10, 13]:
            return False
        if quantidade < 0:
            return False
        if ano_publicacao < 1500 or ano_publicacao > datetime.now().year:
            return False
        
        # Verificar se ISBN já existe
        for livro in self.livros:
            if livro["isbn"] == isbn:
                return False
        
        livro_id = len(self.livros) + 1
        livro = {
            "id": livro_id,
            "titulo": titulo.strip(),
            "autor": autor.strip(),
            "isbn": isbn,
            "categoria": categoria,
            "quantidade_total": quantidade,
            "quantidade_disponivel": quantidade,
            "ano_publicacao": ano_publicacao,
            "data_cadastro": datetime.now().isoformat()
        }
        self.livros.append(livro)
        return True
    
    def cadastrar_usuario(self, nome: str, email: str, telefone: str, 
                         tipo_usuario: str, curso: str = "") -> bool:
        """
        DATA CLUMPS: Dados de usuário sempre passados juntos.
        SWITCH STATEMENT: Lógica baseada em tipo_usuario.
        """
        # Validações repetitivas (duplicadas de outros métodos)
        if not nome or len(nome.strip()) < 2:
            return False
        if not email or "@" not in email:
            return False
        if not telefone or len(telefone) < 10:
            return False
        
        # Verificar se email já existe
        for usuario in self.usuarios:
            if usuario["email"] == email:
                return False
        
        # Lógica baseada em tipo (Switch Statement smell)
        if tipo_usuario == "estudante":
            max_emprestimos = 3
            dias_emprestimo = 14
            if not curso:
                return False
        elif tipo_usuario == "professor":
            max_emprestimos = 10
            dias_emprestimo = 30
        elif tipo_usuario == "funcionario":
            max_emprestimos = 5
            dias_emprestimo = 21
        else:
            max_emprestimos = 2
            dias_emprestimo = 7
        
        usuario_id = len(self.usuarios) + 1
        usuario = {
            "id": usuario_id,
            "nome": nome.strip(),
            "email": email.strip(),
            "telefone": telefone,
            "tipo": tipo_usuario,
            "curso": curso,
            "max_emprestimos": max_emprestimos,
            "dias_emprestimo": dias_emprestimo,
            "data_cadastro": datetime.now().isoformat(),
            "ativo": True
        }
        self.usuarios.append(usuario)
        return True
    
    def processar_emprestimo(self, usuario_id: int, livro_id: int) -> dict:
        """
        LONG METHOD: Método com múltiplas responsabilidades.
        FEATURE ENVY: Usa muitos dados de usuário e livro.
        """
        # Buscar usuário (código duplicado)
        usuario = None
        for u in self.usuarios:
            if u["id"] == usuario_id:
                usuario = u
                break
        
        if not usuario or not usuario["ativo"]:
            return {"sucesso": False, "erro": "Usuário não encontrado ou inativo"}
        
        # Buscar livro (código duplicado)
        livro = None
        for l in self.livros:
            if l["id"] == livro_id:
                livro = l
                break
        
        if not livro:
            return {"sucesso": False, "erro": "Livro não encontrado"}
        
        if livro["quantidade_disponivel"] <= 0:
            return {"sucesso": False, "erro": "Livro indisponível"}
        
        # Verificar limite de empréstimos do usuário
        emprestimos_ativos = 0
        for emp in self.emprestimos:
            if emp["usuario_id"] == usuario_id and emp["status"] == "ativo":
                emprestimos_ativos += 1
        
        if emprestimos_ativos >= usuario["max_emprestimos"]:
            return {"sucesso": False, "erro": "Limite de empréstimos atingido"}
        
        # Verificar se usuário já tem este livro emprestado
        for emp in self.emprestimos:
            if (emp["usuario_id"] == usuario_id and 
                emp["livro_id"] == livro_id and 
                emp["status"] == "ativo"):
                return {"sucesso": False, "erro": "Usuário já possui este livro"}
        
        # Verificar se existe reserva do usuário para este livro
        reserva_usuario = None
        for res in self.reservas:
            if (res["usuario_id"] == usuario_id and 
                res["livro_id"] == livro_id and 
                res["status"] == "ativa"):
                reserva_usuario = res
                break
        
        # Calcular data de devolução
        data_emprestimo = datetime.now()
        data_devolucao = data_emprestimo + timedelta(days=usuario["dias_emprestimo"])
        
        # Criar empréstimo
        emprestimo_id = len(self.emprestimos) + 1
        emprestimo = {
            "id": emprestimo_id,
            "usuario_id": usuario_id,
            "livro_id": livro_id,
            "data_emprestimo": data_emprestimo.isoformat(),
            "data_devolucao_prevista": data_devolucao.isoformat(),
            "data_devolucao_real": None,
            "status": "ativo",
            "multa": 0.0
        }
        self.emprestimos.append(emprestimo)
        
        # Atualizar quantidade disponível
        livro["quantidade_disponivel"] -= 1
        
        # Cancelar reserva se existir
        if reserva_usuario:
            reserva_usuario["status"] = "atendida"
        
        return {
            "sucesso": True,
            "emprestimo_id": emprestimo_id,
            "data_devolucao": data_devolucao.strftime("%d/%m/%Y"),
            "dias_emprestimo": usuario["dias_emprestimo"]
        }
    
    def processar_devolucao(self, emprestimo_id: int) -> dict:
        """
        LONG METHOD: Lógica complexa de cálculo de multa.
        DUPLICATED CODE: Busca por empréstimo repetida.
        """
        # Buscar empréstimo
        emprestimo = None
        for emp in self.emprestimos:
            if emp["id"] == emprestimo_id:
                emprestimo = emp
                break
        
        if not emprestimo or emprestimo["status"] != "ativo":
            return {"sucesso": False, "erro": "Empréstimo não encontrado ou já devolvido"}
        
        # Buscar livro para atualizar quantidade
        livro = None
        for l in self.livros:
            if l["id"] == emprestimo["livro_id"]:
                livro = l
                break
        
        data_devolucao_real = datetime.now()
        data_devolucao_prevista = datetime.fromisoformat(emprestimo["data_devolucao_prevista"])
        
        # Calcular multa se atrasado
        multa = 0.0
        dias_atraso = 0
        if data_devolucao_real > data_devolucao_prevista:
            dias_atraso = (data_devolucao_real - data_devolucao_prevista).days
            multa = dias_atraso * self.configuracoes["multa_dia"]
        
        # Atualizar empréstimo
        emprestimo["data_devolucao_real"] = data_devolucao_real.isoformat()
        emprestimo["status"] = "devolvido"
        emprestimo["multa"] = multa
        
        # Atualizar quantidade disponível do livro
        livro["quantidade_disponivel"] += 1
        
        # Verificar se há reservas pendentes para este livro
        for reserva in self.reservas:
            if (reserva["livro_id"] == emprestimo["livro_id"] and 
                reserva["status"] == "ativa"):
                # Notificar primeiro da fila (simulado)
                print(f"Notificando usuário {reserva['usuario_id']} - livro disponível!")
                break
        
        return {
            "sucesso": True,
            "dias_atraso": dias_atraso,
            "multa": multa,
            "data_devolucao": data_devolucao_real.strftime("%d/%m/%Y %H:%M")
        }
    
    def criar_reserva(self, usuario_id: int, livro_id: int) -> dict:
        """
        DUPLICATED CODE: Validações repetidas de usuário e livro.
        """
        # Buscar usuário (código duplicado)
        usuario = None
        for u in self.usuarios:
            if u["id"] == usuario_id:
                usuario = u
                break
        
        if not usuario or not usuario["ativo"]:
            return {"sucesso": False, "erro": "Usuário não encontrado ou inativo"}
        
        # Buscar livro (código duplicado)
        livro = None
        for l in self.livros:
            if l["id"] == livro_id:
                livro = l
                break
        
        if not livro:
            return {"sucesso": False, "erro": "Livro não encontrado"}
        
        # Verificar se livro está disponível
        if livro["quantidade_disponivel"] > 0:
            return {"sucesso": False, "erro": "Livro disponível - faça empréstimo direto"}
        
        # Verificar limite de reservas
        reservas_ativas = 0
        for res in self.reservas:
            if res["usuario_id"] == usuario_id and res["status"] == "ativa":
                reservas_ativas += 1
        
        if reservas_ativas >= self.configuracoes["max_reservas"]:
            return {"sucesso": False, "erro": "Limite de reservas atingido"}
        
        # Verificar se já tem reserva para este livro
        for res in self.reservas:
            if (res["usuario_id"] == usuario_id and 
                res["livro_id"] == livro_id and 
                res["status"] == "ativa"):
                return {"sucesso": False, "erro": "Já possui reserva para este livro"}
        
        reserva_id = len(self.reservas) + 1
        reserva = {
            "id": reserva_id,
            "usuario_id": usuario_id,
            "livro_id": livro_id,
            "data_reserva": datetime.now().isoformat(),
            "status": "ativa"
        }
        self.reservas.append(reserva)
        
        return {"sucesso": True, "reserva_id": reserva_id}

# Exemplo de uso
if __name__ == "__main__":
    biblioteca = SistemaBiblioteca()
    
    # Cadastrar livro
    biblioteca.cadastrar_livro(
        "Clean Code", "Robert Martin", "9780132350884", 
        "Programação", 3, 2008
    )
    
    # Cadastrar usuário
    biblioteca.cadastrar_usuario(
        "João Silva", "joao@email.com", "11999999999", 
        "estudante", "Ciência da Computação"
    )
    
    # Fazer empréstimo
    resultado = biblioteca.processar_emprestimo(1, 1)
    print(f"Empréstimo: {resultado}")
```

### Requisitos

#### Refatorações Obrigatórias

1. **Extract Class:** Criar classes `Livro`, `Usuario`, `Emprestimo`, `Reserva`
2. **Move Method:** Mover validações para as classes apropriadas
3. **Replace Conditional with Polymorphism:** Diferentes tipos de usuário
4. **Extract Method:** Decompor métodos longos em métodos menores
5. **Remove Duplicated Code:** Centralizar buscas e validações
6. **Introduce Parameter Object:** Agrupar parâmetros relacionados

#### Melhorias de Qualidade

1. **Reduzir complexidade ciclomática** de 8+ para 3- nos métodos principais
2. **Eliminar magic numbers** usando constantes ou configurações
3. **Implementar Repository pattern** para persistência
4. **Adicionar tratamento robusto de erros**
5. **Melhorar testabilidade** (cada classe testável isoladamente)

### Restrições Técnicas

- Manter compatibilidade com interface pública atual
- Não usar bibliotecas externas (apenas Python stdlib)
- Preservar toda a funcionalidade existente
- Implementar pelo menos 15 testes unitários
- Cobertura de código mínima de 80%

### Dicas de Implementação

#### Fase 1: Extract Classes (40 minutos)
1. **Comece com classe `Livro`** - mais simples, sem lógica complexa
2. **Implemente classe `Usuario`** com Strategy para tipos
3. **Crie classes `Emprestimo` e `Reserva`**
4. **Mantenha API atual funcionando** durante transição

#### Fase 2: Move Methods (30 minutos)
1. **Mova validações** para classes apropriadas
2. **Extraia métodos de busca** para repositórios
3. **Centralize lógica de negócio** nas entidades

#### Fase 3: Repository Pattern (15 minutos)
1. **Crie interfaces abstratas** para repositórios
2. **Implemente repositórios em memória**
3. **Injete dependências** na classe principal

### Resultado Esperado

```python
# Estrutura de classes esperada após refatoração

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class TipoUsuario(Enum):
    ESTUDANTE = "estudante"
    PROFESSOR = "professor"
    FUNCIONARIO = "funcionario"
    VISITANTE = "visitante"

@dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    isbn: str
    categoria: str
    quantidade_total: int
    quantidade_disponivel: int
    ano_publicacao: int
    data_cadastro: datetime
    
    def esta_disponivel(self) -> bool:
        return self.quantidade_disponivel > 0
    
    def emprestar(self) -> bool:
        if self.esta_disponivel():
            self.quantidade_disponivel -= 1
            return True
        return False
    
    def devolver(self) -> None:
        self.quantidade_disponivel += 1

class ConfiguracaoUsuario(ABC):
    @abstractmethod
    def max_emprestimos(self) -> int:
        pass
    
    @abstractmethod
    def dias_emprestimo(self) -> int:
        pass

class ConfiguracaoEstudante(ConfiguracaoUsuario):
    def max_emprestimos(self) -> int:
        return 3
    
    def dias_emprestimo(self) -> int:
        return 14

# ... outras configurações

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    telefone: str
    tipo: TipoUsuario
    curso: str
    data_cadastro: datetime
    ativo: bool
    _configuracao: ConfiguracaoUsuario
    
    def pode_emprestar(self, emprestimos_ativos: int) -> bool:
        return emprestimos_ativos < self._configuracao.max_emprestimos()
    
    def dias_emprestimo(self) -> int:
        return self._configuracao.dias_emprestimo()

class RepositorioLivros(ABC):
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Livro]:
        pass
    
    @abstractmethod
    def salvar(self, livro: Livro) -> None:
        pass

class RepositorioUsuarios(ABC):
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        pass

class SistemaBibliotecaRefatorado:
    def __init__(self, repo_livros: RepositorioLivros, 
                 repo_usuarios: RepositorioUsuarios):
        self.repo_livros = repo_livros
        self.repo_usuarios = repo_usuarios
        # Métodos principais simplificados com delegação
    
    def processar_emprestimo(self, usuario_id: int, livro_id: int) -> dict:
        # Método principal com ~10 linhas, delegando para services
        pass
```

### Extensões Avançadas (Opcionais)

1. **Implementar padrão Observer** para notificações de reserva
2. **Adicionar sistema de multas** com diferentes estratégias de cálculo
3. **Criar relatórios** de empréstimos e reservas
4. **Implementar cache** para buscas frequentes
5. **Adicionar auditoria** de operações

---

## Exercício 2.2: Sistema de Vendas Online - Refatoração com TDD

### Contexto e Motivação

Um sistema de vendas online cresceu organicamente e agora apresenta sérios problemas de manutenibilidade. Você foi contratado para refatorar o sistema usando TDD, garantindo que nenhuma funcionalidade seja perdida durante o processo.

### Código Inicial

```python
# sistema_vendas.py
from datetime import datetime
from typing import List, Dict, Any
import json

class SistemaVendasOnline:
    """
    Sistema de vendas com múltiplos code smells críticos.
    
    PROBLEMAS CRÍTICOS:
    - God Class (200+ linhas)
    - Long Methods (50+ linhas alguns)
    - No Exception Handling
    - Tight Coupling
    - No Input Validation
    - Business Logic in UI Layer
    """
    
    def __init__(self):
        self.produtos = []
        self.clientes = []
        self.pedidos = []
        self.estoque = {}
        self.promocoes = []
        self.configuracoes = {
            "frete_gratis_acima": 99.0,
            "taxa_cartao": 0.035,
            "desconto_pix": 0.05,
            "limite_parcelamento": 12
        }
    
    def processar_venda_completa(self, dados_venda: dict) -> dict:
        """
        LONG METHOD CRÍTICO: 60+ linhas com múltiplas responsabilidades.
        
        Responsabilidades identificadas:
        1. Validação de dados
        2. Verificação de estoque
        3. Cálculo de preços
        4. Aplicação de promoções
        5. Cálculo de frete
        6. Processamento de pagamento
        7. Atualização de estoque
        8. Geração de nota fiscal
        9. Envio de confirmação
        """
        
        # Validação básica (sem tratamento de erro adequado)
        cliente_id = dados_venda.get("cliente_id")
        itens = dados_venda.get("itens", [])
        forma_pagamento = dados_venda.get("forma_pagamento")
        endereco_entrega = dados_venda.get("endereco_entrega")
        cupom_desconto = dados_venda.get("cupom_desconto", "")
        
        if not cliente_id or not itens or not forma_pagamento:
            return {"erro": "Dados incompletos"}
        
        # Buscar cliente (sem validação adequada)
        cliente = None
        for c in self.clientes:
            if c["id"] == cliente_id:
                cliente = c
                break
        
        if not cliente:
            return {"erro": "Cliente não encontrado"}
        
        # Validar e calcular itens
        total_produtos = 0
        itens_processados = []
        
        for item in itens:
            produto_id = item.get("produto_id")
            quantidade = item.get("quantidade", 1)
            
            # Buscar produto
            produto = None
            for p in self.produtos:
                if p["id"] == produto_id:
                    produto = p
                    break
            
            if not produto:
                return {"erro": f"Produto {produto_id} não encontrado"}
            
            # Verificar estoque
            estoque_disponivel = self.estoque.get(produto_id, 0)
            if estoque_disponivel < quantidade:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            
            # Calcular preço com promoções
            preco_unitario = produto["preco"]
            
            # Aplicar promoções por quantidade
            if quantidade >= 5:
                preco_unitario *= 0.9  # 10% desconto
            elif quantidade >= 3:
                preco_unitario *= 0.95  # 5% desconto
            
            # Verificar promoções ativas
            for promocao in self.promocoes:
                if (promocao["produto_id"] == produto_id and 
                    promocao["ativa"] and
                    datetime.now() >= datetime.fromisoformat(promocao["inicio"]) and
                    datetime.now() <= datetime.fromisoformat(promocao["fim"])):
                    preco_unitario *= (1 - promocao["desconto"])
            
            subtotal = preco_unitario * quantidade
            total_produtos += subtotal
            
            itens_processados.append({
                "produto_id": produto_id,
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal
            })
        
        # Aplicar cupom de desconto
        desconto_cupom = 0
        if cupom_desconto:
            # Lógica complexa de cupons (deveria estar em classe separada)
            if cupom_desconto == "PRIMEIRA_COMPRA":
                if len([p for p in self.pedidos if p["cliente_id"] == cliente_id]) == 0:
                    desconto_cupom = min(total_produtos * 0.1, 50.0)
            elif cupom_desconto == "VOLTA_SEMPRE":
                if len([p for p in self.pedidos if p["cliente_id"] == cliente_id]) >= 5:
                    desconto_cupom = total_produtos * 0.15
            elif cupom_desconto.startswith("DESC"):
                # Cupons fixos (simulado)
                valor_desc = int(cupom_desconto.replace("DESC", ""))
                desconto_cupom = min(valor_desc, total_produtos * 0.3)
        
        total_com_desconto = total_produtos - desconto_cupom
        
        # Calcular frete
        if total_com_desconto >= self.configuracoes["frete_gratis_acima"]:
            frete = 0
        else:
            # Cálculo de frete simplificado por região
            estado = endereco_entrega.get("estado", "")
            if estado == "SP":
                frete = 15.0
            elif estado in ["RJ", "MG", "ES"]:
                frete = 25.0
            else:
                frete = 35.0
        
        total_final = total_com_desconto + frete
        
        # Processar pagamento baseado na forma
        taxa_pagamento = 0
        parcelamento = dados_venda.get("parcelamento", 1)
        
        if forma_pagamento == "cartao_credito":
            taxa_pagamento = total_final * self.configuracoes["taxa_cartao"]
            if parcelamento > self.configuracoes["limite_parcelamento"]:
                return {"erro": "Parcelamento excede limite"}
        elif forma_pagamento == "pix":
            # Desconto PIX
            desconto_pix = total_final * self.configuracoes["desconto_pix"]
            total_final -= desconto_pix
        elif forma_pagamento == "boleto":
            # Sem taxa adicional
            pass
        else:
            return {"erro": "Forma de pagamento inválida"}
        
        total_final += taxa_pagamento
        
        # Atualizar estoque
        for item in itens_processados:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]
            self.estoque[produto_id] -= quantidade
        
        # Gerar pedido
        pedido_id = len(self.pedidos) + 1
        pedido = {
            "id": pedido_id,
            "cliente_id": cliente_id,
            "itens": itens_processados,
            "total_produtos": total_produtos,
            "desconto_cupom": desconto_cupom,
            "frete": frete,
            "taxa_pagamento": taxa_pagamento,
            "total_final": total_final,
            "forma_pagamento": forma_pagamento,
            "parcelamento": parcelamento,
            "endereco_entrega": endereco_entrega,
            "data_pedido": datetime.now().isoformat(),
            "status": "confirmado"
        }
        self.pedidos.append(pedido)
        
        # Simular envio de email
        print(f"Email enviado para {cliente['email']}")
        
        return {
            "sucesso": True,
            "pedido_id": pedido_id,
            "total_final": total_final,
            "prazo_entrega": "3-5 dias úteis"
        }
    
    def adicionar_produto(self, nome: str, preco: float, categoria: str, 
                         descricao: str, peso: float, estoque_inicial: int) -> int:
        """DATA CLUMPS: Parâmetros sempre passados juntos."""
        produto_id = len(self.produtos) + 1
        produto = {
            "id": produto_id,
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
            "descricao": descricao,
            "peso": peso,
            "ativo": True
        }
        self.produtos.append(produto)
        self.estoque[produto_id] = estoque_inicial
        return produto_id
    
    def adicionar_cliente(self, nome: str, email: str, cpf: str, telefone: str) -> int:
        """PRIMITIVE OBSESSION: Strings em vez de objetos."""
        cliente_id = len(self.clientes) + 1
        cliente = {
            "id": cliente_id,
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "telefone": telefone,
            "data_cadastro": datetime.now().isoformat()
        }
        self.clientes.append(cliente)
        return cliente_id

# Dados de exemplo para teste
if __name__ == "__main__":
    sistema = SistemaVendasOnline()
    
    # Adicionar produtos
    produto1 = sistema.adicionar_produto(
        "Smartphone XYZ", 899.99, "Eletrônicos", 
        "Smartphone com 128GB", 0.2, 50
    )
    produto2 = sistema.adicionar_produto(
        "Fone Bluetooth", 199.99, "Acessórios",
        "Fone sem fio", 0.1, 100
    )
    
    # Adicionar cliente
    cliente1 = sistema.adicionar_cliente(
        "João Silva", "joao@email.com", "12345678900", "11999999999"
    )
    
    # Processar venda
    dados_venda = {
        "cliente_id": 1,
        "itens": [
            {"produto_id": 1, "quantidade": 1},
            {"produto_id": 2, "quantidade": 2}
        ],
        "forma_pagamento": "pix",
        "endereco_entrega": {
            "rua": "Rua das Flores, 123",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01234-567"
        },
        "cupom_desconto": "PRIMEIRA_COMPRA"
    }
    
    resultado = sistema.processar_venda_completa(dados_venda)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

### Requisitos

#### Fase 1: Characterization Tests (25 minutos)
1. **Criar testes que capturam comportamento atual** do sistema
2. **Cobertura mínima de 80%** dos caminhos críticos
3. **Documentar edge cases** descobertos durante teste
4. **Validar cenários de erro** existentes

#### Fase 2: Refatoração com TDD (50 minutos)
1. **Extract Classes:** `Produto`, `Cliente`, `Pedido`, `Carrinho`
2. **Extract Services:** `CalculadoraPreco`, `ProcessadorPagamento`, `GerenciadorEstoque`
3. **Strategy Pattern:** Diferentes formas de pagamento
4. **Command Pattern:** Operações de venda
5. **Repository Pattern:** Persistência de dados

#### Fase 3: Integração e Validação (15 minutos)
1. **Validar que todos os testes passam** após refatoração
2. **Comparar métricas** antes/depois
3. **Documentar melhorias** alcançadas

### Estrutura de Testes Requerida

```python
# test_sistema_vendas.py - Estrutura esperada

class TestSistemaVendasCharacterization:
    """Testes que capturam comportamento atual."""
    
    def test_venda_simples_com_pix(self):
        """Testa cenário básico com PIX."""
        pass
    
    def test_venda_com_cupom_primeira_compra(self):
        """Testa aplicação de cupom para primeiro cliente."""
        pass
    
    def test_calculo_frete_por_regiao(self):
        """Testa diferentes cálculos de frete."""
        pass
    
    def test_aplicacao_promocoes_quantidade(self):
        """Testa descontos por quantidade."""
        pass
    
    def test_erro_estoque_insuficiente(self):
        """Testa tratamento de estoque insuficiente."""
        pass

class TestSistemaVendasRefatorado:
    """Testes para sistema refatorado."""
    
    def test_calculadora_preco_isolada(self):
        """Testa calculadora de preço isoladamente."""
        pass
    
    def test_processador_pagamento_pix(self):
        """Testa processador PIX isoladamente."""
        pass
    
    def test_gerenciador_estoque_operacoes(self):
        """Testa operações de estoque."""
        pass
```

### Dicas de Implementação

#### TDD Cycle para cada Refatoração:
1. **RED:** Escreva teste que falha para nova estrutura
2. **GREEN:** Implemente código mínimo para passar
3. **REFACTOR:** Melhore código mantendo testes passando

#### Estratégia de Refatoração:
1. **Mantenha sistema original funcionando** durante transição
2. **Refatore uma responsabilidade por vez**
3. **Use Adapter Pattern** temporariamente se necessário
4. **Valide comportamento a cada mudança**

### Critérios de Avaliação

#### Qualidade dos Testes (40%)
- ✅ Characterization tests capturam comportamento atual
- ✅ Cobertura ≥ 80% do código crítico
- ✅ Testes unitários para classes extraídas
- ✅ Testes de integração para workflows completos

#### Qualidade da Refatoração (60%)
- ✅ Code smells eliminados adequadamente
- ✅ Arquitetura modular e testável
- ✅ Separação de responsabilidades clara
- ✅ Padrões de design aplicados corretamente
- ✅ Comportamento preservado (todos os testes passam)

---

## Exercício 2.3: Sistema de RH - Folha de Pagamento

### Contexto e Motivação

Uma empresa de médio porte está modernizando seu sistema de RH. O sistema atual de cálculo de folha de pagamento foi desenvolvido há 5 anos e possui vários problemas de manutenibilidade. Recentemente, a empresa precisa adaptar-se a novas leis trabalhistas e integrar com sistemas de ponto eletrônico.

### Código Inicial

```python
# sistema_folha_pagamento.py
from datetime import datetime, timedelta
from typing import Dict, List, Any
import calendar

class SistemaFolhaPagamento:
    """
    Sistema de folha de pagamento com sérios problemas arquiteturais.
    
    PROBLEMS CRÍTICOS:
    - God Class (250+ linhas)
    - Calculation Logic Scattered
    - Hard-coded Business Rules
    - No Extensibility for New Rules
    - Complex Conditional Logic
    """
    
    def __init__(self):
        self.funcionarios = []
        self.pontos = []
        self.folhas_pagamento = []
        self.configuracoes = {
            "salario_minimo": 1320.00,
            "valor_hora_extra": 1.5,
            "desconto_vale_transporte": 0.06,
            "desconto_vale_refeicao": 0.20,
            "limite_horas_mes": 220
        }
    
    def calcular_folha_completa(self, funcionario_id: int, mes: int, ano: int) -> dict:
        """
        LONG METHOD EXTREMO: 80+ linhas com cálculos complexos.
        
        Cálculos inclusos:
        1. Salário base proporcional
        2. Horas extras
        3. Adicional noturno  
        4. Comissões
        5. Gratificações
        6. Descontos obrigatórios (INSS, IRRF)
        7. Descontos opcionais (VT, VR, plano saúde)
        8. Benefícios
        9. 13º salário proporcional
        10. Férias proporcionais
        """
        
        # Buscar funcionário (sem validação adequada)
        funcionario = None
        for f in self.funcionarios:
            if f["id"] == funcionario_id:
                funcionario = f
                break
        
        if not funcionario:
            return {"erro": "Funcionário não encontrado"}
        
        # Buscar pontos do mês
        pontos_mes = []
        for ponto in self.pontos:
            if (ponto["funcionario_id"] == funcionario_id and 
                ponto["mes"] == mes and ponto["ano"] == ano):
                pontos_mes.append(ponto)
        
        # Calcular dias trabalhados
        dias_mes = calendar.monthrange(ano, mes)[1]
        dias_trabalhados = len([p for p in pontos_mes if p["presente"]])
        
        # Salário base proporcional
        salario_base = funcionario["salario_base"]
        salario_proporcional = (salario_base / dias_mes) * dias_trabalhados
        
        # Calcular horas extras
        total_horas_trabalhadas = sum(p["horas_trabalhadas"] for p in pontos_mes)
        horas_normais = dias_trabalhados * 8  # 8 horas por dia
        horas_extras = max(0, total_horas_trabalhadas - horas_normais)
        
        valor_hora_normal = salario_base / self.configuracoes["limite_horas_mes"]
        valor_horas_extras = horas_extras * valor_hora_normal * self.configuracoes["valor_hora_extra"]
        
        # Adicional noturno (22h às 5h)
        adicional_noturno = 0
        for ponto in pontos_mes:
            if ponto["turno"] == "noturno":
                adicional_noturno += ponto["horas_trabalhadas"] * valor_hora_normal * 0.2
        
        # Comissões (apenas para vendedores)
        comissoes = 0
        if funcionario["cargo"] == "vendedor":
            vendas_mes = funcionario.get("vendas_mes", 0)
            if vendas_mes > 10000:
                comissoes = vendas_mes * 0.05
            elif vendas_mes > 5000:
                comissoes = vendas_mes * 0.03
            else:
                comissoes = vendas_mes * 0.01
        
        # Gratificações especiais
        gratificacoes = 0
        if funcionario.get("meta_atingida", False):
            gratificacoes += 500
        if funcionario.get("anos_empresa", 0) >= 5:
            gratificacoes += 200
        
        # Total de proventos
        total_proventos = (salario_proporcional + valor_horas_extras + 
                          adicional_noturno + comissoes + gratificacoes)
        
        # Cálculo do INSS
        if total_proventos <= 1320.00:
            inss = total_proventos * 0.075
        elif total_proventos <= 2571.29:
            inss = total_proventos * 0.09
        elif total_proventos <= 3856.94:
            inss = total_proventos * 0.12
        elif total_proventos <= 7507.49:
            inss = total_proventos * 0.14
        else:
            inss = 7507.49 * 0.14  # Teto do INSS
        
        # Base de cálculo para IRRF
        base_irrf = total_proventos - inss
        
        # Dedução por dependentes
        num_dependentes = funcionario.get("dependentes", 0)
        deducao_dependentes = num_dependentes * 189.59
        base_irrf -= deducao_dependentes
        
        # Cálculo do IRRF
        if base_irrf <= 1903.98:
            irrf = 0
        elif base_irrf <= 2826.65:
            irrf = base_irrf * 0.075 - 142.80
        elif base_irrf <= 3751.05:
            irrf = base_irrf * 0.15 - 354.80
        elif base_irrf <= 4664.68:
            irrf = base_irrf * 0.225 - 636.13
        else:
            irrf = base_irrf * 0.275 - 869.36
        
        irrf = max(0, irrf)
        
        # Descontos opcionais
        desconto_vt = 0
        if funcionario.get("usa_vale_transporte", False):
            desconto_vt = min(total_proventos * self.configuracoes["desconto_vale_transporte"],
                             funcionario.get("custo_transporte_mensal", 0))
        
        desconto_vr = 0
        if funcionario.get("usa_vale_refeicao", False):
            valor_vr = funcionario.get("valor_vale_refeicao", 500)
            desconto_vr = valor_vr * self.configuracoes["desconto_vale_refeicao"]
        
        desconto_plano_saude = funcionario.get("valor_plano_saude", 0)
        
        # Outros descontos
        outros_descontos = funcionario.get("outros_descontos", 0)
        
        # Total de descontos
        total_descontos = (inss + irrf + desconto_vt + desconto_vr + 
                          desconto_plano_saude + outros_descontos)
        
        # Salário líquido
        salario_liquido = total_proventos - total_descontos
        
        # 13º salário proporcional (se dezembro ou rescisão)
        decimo_terceiro = 0
        if mes == 12 or funcionario.get("rescisao", False):
            meses_trabalhados = min(12, funcionario.get("meses_trabalhados_ano", 12))
            decimo_terceiro = (salario_base / 12) * meses_trabalhados
        
        # Férias proporcionais
        ferias_proporcionais = 0
        if funcionario.get("rescisao", False):
            meses_ferias = funcionario.get("meses_para_ferias", 0)
            ferias_proporcionais = (salario_base / 12) * meses_ferias
        
        # Criar registro da folha
        folha_id = len(self.folhas_pagamento) + 1
        folha = {
            "id": folha_id,
            "funcionario_id": funcionario_id,
            "mes": mes,
            "ano": ano,
            "dias_trabalhados": dias_trabalhados,
            "horas_extras": horas_extras,
            "salario_base": salario_base,
            "salario_proporcional": salario_proporcional,
            "valor_horas_extras": valor_horas_extras,
            "adicional_noturno": adicional_noturno,
            "comissoes": comissoes,
            "gratificacoes": gratificacoes,
            "total_proventos": total_proventos,
            "inss": inss,
            "irrf": irrf,
            "desconto_vt": desconto_vt,
            "desconto_vr": desconto_vr,
            "desconto_plano_saude": desconto_plano_saude,
            "outros_descontos": outros_descontos,
            "total_descontos": total_descontos,
            "salario_liquido": salario_liquido,
            "decimo_terceiro": decimo_terceiro,
            "ferias_proporcionais": ferias_proporcionais,
            "data_calculo": datetime.now().isoformat()
        }
        
        self.folhas_pagamento.append(folha)
        
        return folha
    
    def adicionar_funcionario(self, nome: str, cpf: str, cargo: str, 
                             salario_base: float, data_admissao: str) -> int:
        """DATA CLUMPS: Dados de funcionário sempre passados juntos."""
        funcionario_id = len(self.funcionarios) + 1
        funcionario = {
            "id": funcionario_id,
            "nome": nome,
            "cpf": cpf,
            "cargo": cargo,
            "salario_base": salario_base,
            "data_admissao": data_admissao,
            "ativo": True,
            "dependentes": 0,
            "usa_vale_transporte": False,
            "usa_vale_refeicao": False,
            "valor_plano_saude": 0,
            "outros_descontos": 0
        }
        self.funcionarios.append(funcionario)
        return funcionario_id

# Exemplo de uso
if __name__ == "__main__":
    sistema = SistemaFolhaPagamento()
    
    # Adicionar funcionário
    func_id = sistema.adicionar_funcionario(
        "João Silva", "12345678900", "analista", 5000.00, "2023-01-15"
    )
    
    # Simular pontos (dados simplificados)
    for dia in range(1, 23):  # 22 dias trabalhados
        sistema.pontos.append({
            "funcionario_id": func_id,
            "dia": dia,
            "mes": 7,
            "ano": 2024,
            "presente": True,
            "horas_trabalhadas": 8,
            "turno": "diurno"
        })
    
    # Calcular folha
    folha = sistema.calcular_folha_completa(func_id, 7, 2024)
    print(f"Salário líquido: R$ {folha['salario_liquido']:.2f}")
```

### Requisitos

#### Refatorações Obrigatórias

1. **Extract Classes:**
   - `Funcionario` com diferentes tipos (CLT, PJ, Estagiário)
   - `CalculadoraSalario` com strategies por tipo
   - `CalculadoraImpostos` (INSS, IRRF)
   - `GerenciadorBeneficios` (VT, VR, Plano Saúde)

2. **Strategy Pattern:**
   - Diferentes cálculos por tipo de funcionário
   - Diferentes regras de INSS/IRRF por ano
   - Diferentes políticas de benefícios

3. **Command Pattern:**
   - Operações de cálculo de folha
   - Permite auditoria e desfazer operações

4. **Builder Pattern:**
   - Construção complexa de folha de pagamento
   - Permite diferentes configurações

#### Melhorias Específicas

1. **Eliminar Magic Numbers:** Todas as alíquotas em configurações
2. **Tratamento de Exceções:** Validações robustas
3. **Separation of Concerns:** Cálculo vs. Persistência vs. Apresentação
4. **Extensibilidade:** Fácil adição de novos tipos de cálculo

### Restrições e Requisitos Técnicos

- Manter precisão de cálculos (2 casas decimais)
- Suportar diferentes regras por ano (2023, 2024, 2025)
- Interface compatível com sistema atual
- Cobertura de testes ≥ 85%
- Documentação das regras de negócio

### Resultado Esperado

```python
# Estrutura esperada após refatoração

from abc import ABC, abstractmethod
from typing import List, Dict
from decimal import Decimal
from dataclasses import dataclass
from enum import Enum

class TipoFuncionario(Enum):
    CLT = "clt"
    PJ = "pj" 
    ESTAGIARIO = "estagiario"
    TERCEIRIZADO = "terceirizado"

@dataclass
class Funcionario:
    id: int
    nome: str
    cpf: str
    cargo: str
    tipo: TipoFuncionario
    salario_base: Decimal
    data_admissao: datetime
    
    def calcular_dias_trabalhados(self, pontos: List) -> int:
        # Lógica específica do funcionário
        pass

class CalculadoraSalario(ABC):
    @abstractmethod
    def calcular_proventos(self, funcionario: Funcionario, pontos: List) -> Dict:
        pass

class CalculadoraSalarioCLT(CalculadoraSalario):
    def calcular_proventos(self, funcionario: Funcionario, pontos: List) -> Dict:
        # Implementação específica para CLT
        pass

class CalculadoraImpostos:
    def __init__(self, ano: int):
        self.tabelas = self._carregar_tabelas(ano)
    
    def calcular_inss(self, salario: Decimal) -> Decimal:
        # Usa tabela do ano específico
        pass
    
    def calcular_irrf(self, base_calculo: Decimal, dependentes: int) -> Decimal:
        # Usa tabela do ano específico
        pass

class FolhaPagamentoBuilder:
    def __init__(self):
        self.folha = {}
    
    def com_funcionario(self, funcionario: Funcionario):
        return self
    
    def com_periodo(self, mes: int, ano: int):
        return self
    
    def com_pontos(self, pontos: List):
        return self
    
    def build(self) -> Dict:
        # Constrói folha completa
        pass

class SistemaFolhaPagamentoRefatorado:
    def __init__(self):
        self.calculadoras = {
            TipoFuncionario.CLT: CalculadoraSalarioCLT(),
            TipoFuncionario.PJ: CalculadoraSalarioPJ(),
            # ...
        }
    
    def calcular_folha_completa(self, funcionario_id: int, mes: int, ano: int) -> Dict:
        # Método principal simplificado usando Builder e Strategies
        pass
```

### Extensões Avançadas

1. **Implementar auditoria** de cálculos com Command Pattern
2. **Criar relatórios** personalizáveis de folha
3. **Integração com ponto eletrônico** via API
4. **Cálculo automático de férias** e 13º salário
5. **Simulação de cenários** (aumento salarial, mudança de benefícios)

---

## Critérios de Avaliação - Nível 2

### Exercício 2.1 - Sistema de Biblioteca
- ✅ **Extract Classes (25%):** Pelo menos 4 classes bem definidas
- ✅ **Repository Pattern (20%):** Interfaces e implementações
- ✅ **Strategy Pattern (20%):** Tipos de usuário polimórficos  
- ✅ **Complexity Reduction (15%):** Métodos com complexidade ≤ 3
- ✅ **Testing (20%):** Cobertura ≥ 80%, testes unitários

### Exercício 2.2 - Sistema de Vendas com TDD
- ✅ **Characterization Tests (30%):** Comportamento atual capturado
- ✅ **TDD Process (25%):** Red-Green-Refactor aplicado
- ✅ **Architectural Patterns (25%):** Strategy, Command, Repository
- ✅ **Code Quality (20%):** Code smells eliminados

### Exercício 2.3 - Sistema de RH
- ✅ **Business Logic Separation (30%):** Cálculos isolados e testáveis
- ✅ **Extensibility (25%):** Fácil adição de novos tipos/regras
- ✅ **Precision (20%):** Cálculos financeiros corretos
- ✅ **Documentation (25%):** Regras de negócio documentadas

### Pontuação Geral
- **Excepcional (90-100%):** Todos os critérios + extensões + inovações
- **Proficiente (75-89%):** Todos os critérios obrigatórios bem executados
- **Em Desenvolvimento (60-74%):** Maioria dos critérios com algumas lacunas
- **Insuficiente (<60%):** Critérios essenciais não demonstrados adequadamente
