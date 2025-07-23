#!/usr/bin/env python3
"""
Teste progressivo do sistema bancário
"""

import sys
import os
from decimal import Decimal
from datetime import datetime

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(current_dir)

def teste_progressivo():
    print("🧪 TESTE PROGRESSIVO DO SISTEMA BANCÁRIO")
    print("=" * 60)
    
    try:
        # Imports
        from domain import (
            CPF, Dinheiro, TipoConta, 
            ComandoCriarCliente, ComandoAbrirConta,
            CriarClienteUseCase, AbrirContaUseCase
        )
        from infrastructure import (
            RepositorioClienteMemoria, RepositorioContaMemoria,
            ConsultorCreditoSerasa
        )
        
        print("✅ Imports realizados com sucesso")
        
        # Criar repositórios
        repo_cliente = RepositorioClienteMemoria()
        repo_conta = RepositorioContaMemoria()
        consultor_credito = ConsultorCreditoSerasa()
        
        print("✅ Repositórios criados")
        
        # Criar casos de uso
        criar_cliente_uc = CriarClienteUseCase(repo_cliente, consultor_credito)
        abrir_conta_uc = AbrirContaUseCase(repo_cliente, repo_conta)
        
        print("✅ Casos de uso criados")
        
        # Teste 1: Criar cliente
        print("\n📝 Teste 1: Criando cliente...")
        comando_cliente = ComandoCriarCliente(
            nome="João Teste",
            cpf="11144477735",
            endereco_cep="01310-100",
            endereco_logradouro="Av. Paulista",
            endereco_numero="1000",
            endereco_complemento="Apto 101",
            endereco_bairro="Bela Vista",
            endereco_cidade="São Paulo",
            endereco_uf="SP",
            telefone="11999887766",
            email="joao@email.com",
            data_nascimento=datetime(1990, 5, 15)
        )
        
        resultado_cliente = criar_cliente_uc.executar(comando_cliente)
        if resultado_cliente.sucesso:
            print(f"✅ Cliente criado: {resultado_cliente.cliente_id}")
            cliente_id = resultado_cliente.cliente_id
        else:
            print(f"❌ Erro ao criar cliente: {resultado_cliente.mensagem}")
            return
        
        # Teste 2: Abrir conta
        print("\n🏦 Teste 2: Abrindo conta...")
        comando_conta = ComandoAbrirConta(
            cliente_id=cliente_id,
            tipo_conta=TipoConta.CORRENTE,
            agencia="0001",
            deposito_inicial=Dinheiro(Decimal("1000.00"))
        )
        
        resultado_conta = abrir_conta_uc.executar(comando_conta)
        if resultado_conta.sucesso:
            print(f"✅ Conta criada: {resultado_conta.agencia}-{resultado_conta.numero}")
        else:
            print(f"❌ Erro ao abrir conta: {resultado_conta.mensagem}")
            
        print("\n🎉 TESTE PROGRESSIVO CONCLUÍDO!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_progressivo()
