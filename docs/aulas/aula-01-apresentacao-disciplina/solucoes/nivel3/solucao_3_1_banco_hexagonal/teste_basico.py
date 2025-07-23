#!/usr/bin/env python3
"""
Teste mínimo do sistema bancário
"""

import sys
import os
from decimal import Decimal

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(current_dir)

def teste_basico():
    print("🧪 TESTE BÁSICO DO SISTEMA BANCÁRIO")
    print("=" * 50)
    
    try:
        print("📦 Importando módulo domain...")
        from domain import CPF, Dinheiro, TipoConta
        print("✅ Domain importado com sucesso")
        
        print("📦 Testando criação de Value Objects...")
        cpf = CPF("11144477735")  # CPF válido
        dinheiro = Dinheiro(Decimal("100.50"))
        print(f"✅ CPF: {cpf.formatado}")
        print(f"✅ Dinheiro: {dinheiro.formatado}")
        
        print("📦 Importando módulo infrastructure...")
        from infrastructure import RepositorioClienteMemoria
        print("✅ Infrastructure importado com sucesso")
        
        print("📦 Testando repositório...")
        repo = RepositorioClienteMemoria()
        print("✅ Repositório criado com sucesso")
        
        print("\n🎉 TESTE BÁSICO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_basico()
