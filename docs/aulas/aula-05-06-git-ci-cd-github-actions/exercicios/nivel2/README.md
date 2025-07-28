# Exercícios Nível 2 - Intermediário 🟡

## Visão Geral

Os exercícios do Nível 2 focam na integração de múltiplos conceitos e ferramentas, criando sistemas mais complexos que demonstram práticas empresariais de CI/CD. Cada exercício deve ser completado em 45-90 minutos e requer aplicação de conhecimentos dos exercícios básicos.


## Exercício 2.1: Sistema de Branching Empresarial 🟡

### Contexto
Sua startup cresceu e agora possui uma equipe de 5 desenvolvedores trabalhando simultaneamente. A empresa decidiu implementar um sistema de branching mais robusto que suporte desenvolvimento paralelo, releases programados e hotfixes de emergência, seguindo padrões de empresas de tecnologia consolidadas.

### Objetivos Pedagógicos
- Implementar Git Flow completo em ambiente colaborativo
- Gerenciar conflitos de merge complexos
- Aplicar políticas de branch protection
- Coordenar releases multi-feature

### Cenário
A equipe está desenvolvendo um **Sistema de Gestão de Tarefas** corporativo que precisa de três features principais sendo desenvolvidas em paralelo:
1. **Autenticação JWT** (Developer A)
2. **API de Notificações** (Developer B) 
3. **Dashboard Analytics** (Developer C)

Além disso, durante o desenvolvimento, um bug crítico de segurança foi descoberto em produção e precisa de hotfix imediato.

### Requisitos Funcionais

1. **Estrutura do Projeto Base**
```
task-manager/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_manager.py
│   │   └── user_service.py
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   └── push_service.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   └── metrics.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── task_model.py
│   │   └── database.py
│   └── main.py
├── tests/
├── docs/
├── requirements.txt
└── docker-compose.yml
```

2. **Features Paralelas a Desenvolver**

**Feature A: Autenticação JWT**
- Implementar login/logout com JWT tokens
- Middleware de autenticação para rotas protegidas
- Refresh token mechanism
- Password hashing com bcrypt

**Feature B: Sistema de Notificações**
- Email notifications para task updates
- Push notifications para mobile
- Notification preferences per user
- Template system para mensagens

**Feature C: Dashboard Analytics**
- Task completion metrics
- User productivity analytics
- Real-time charts e graphs
- Export reports (PDF/Excel)

3. **Cenário de Hotfix**
- Bug de segurança: SQL injection na busca de tarefas
- Deve ser corrigido em produção imediatamente
- Hotfix deve ser aplicado em todas as branches ativas

### Requisitos Técnicos

1. **Git Flow Completo**
```bash
# Estrutura de branches obrigatória
main                    # Produção estável
develop                 # Integração de desenvolvimento
feature/jwt-auth        # Feature A
feature/notifications   # Feature B  
feature/analytics       # Feature C
release/v2.0.0         # Release branch
hotfix/security-fix    # Hotfix crítico
```

2. **Branch Protection Rules**
- `main`: Require PR + 2 approvals + status checks
- `develop`: Require PR + 1 approval + status checks
- No direct pushes to protected branches
- Require branches to be up to date before merging

3. **Merge Strategy**
- Feature → Develop: Squash and merge
- Release → Main: Merge commit (preserve history)
- Hotfix → Main & Develop: Cherry-pick strategy

### Implementação Passo a Passo

#### Fase 1: Setup Inicial e Branch Protection (15 min)

**1.1 Criar Repositório Base**
```bash
# Criar repositório e structure inicial
git init task-manager
cd task-manager

# Criar estrutura de diretórios
mkdir -p src/{auth,notifications,analytics,core} tests docs

# Criar arquivos base
cat > src/main.py << 'EOF'
"""
Sistema de Gestão de Tarefas - Aplicação Principal
Coordena todos os módulos do sistema.
"""

from flask import Flask, jsonify, request
from src.core.database import Database
from src.auth.jwt_manager import JWTManager
from src.notifications.email_service import EmailService
from src.analytics.dashboard import Dashboard

class TaskManagerApp:
    """Aplicação principal do sistema de gestão de tarefas."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.db = Database()
        self.jwt_manager = JWTManager()
        self.email_service = EmailService()
        self.dashboard = Dashboard()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura rotas principais da aplicação."""
        
        @self.app.route('/health')
        def health_check():
            """Endpoint de health check."""
            return jsonify({
                'status': 'healthy',
                'version': '1.0.0',
                'services': {
                    'database': self.db.is_connected(),
                    'auth': True,  # TODO: Implementar check JWT
                    'notifications': True,  # TODO: Implementar check email
                    'analytics': True  # TODO: Implementar check dashboard
                }
            })
        
        @self.app.route('/api/tasks')
        def list_tasks():
            """Lista todas as tarefas do usuário."""
            # VULNERABILIDADE: SQL Injection aqui (para hotfix)
            user_id = request.args.get('user_id', '')
            # Query vulnerável: f"SELECT * FROM tasks WHERE user_id = '{user_id}'"
            # TODO: Implementar busca segura
            return jsonify({'tasks': [], 'count': 0})
    
    def run(self, debug=False):
        """Executa a aplicação."""
        self.app.run(debug=debug, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app = TaskManagerApp()
    app.run(debug=True)
EOF

# Commit inicial
git add .
git commit -m "feat: estrutura inicial do projeto task manager

- Setup básico da aplicação Flask
- Estrutura de diretórios organizados por módulos
- Health check endpoint implementado
- TODO: vulnerabilidade SQL injection para hotfix demo"

# Criar branch develop
git checkout -b develop
git push -u origin develop
git checkout main
git push -u origin main
```

## Exercício 2.2: Pipeline Multi-Ambiente 🟡

### Contexto
Com vários ambientes de desenvolvimento (dev, staging e prod), sua equipe precisa definir um pipeline que realize deploy automático e isolado para cada ambiente. O objetivo é garantir qualidade e consistência, minimizando riscos ao promover alterações.

### Objetivos Pedagógicos
- Configurar pipelines de deploy para múltiplos ambientes
- Utilizar GitHub Actions para gerenciar secrets e variáveis de ambiente
- Implementar gate de aprovação antes do deploy em staging e prod
- Automatizar rollback em caso de falha

### Cenário
Imagine que você tem o repositório `task-manager` e deseja criar workflows que:
1. Deploy automático em ambiente `dev` após merge em `develop`
2. Deploy em `staging` a partir de `release/*` com aprovação manual
3. Deploy em `production` a partir de tags `v*.*.*`, comprovando testes e segurança

### Requisitos Funcionais
1. **Dev Environment**
   - Trigger: push na branch `develop`
   - Deploy automático sem intervenção
2. **Staging Environment**
   - Trigger: pull request para `main` ou criação de branch `release/*`
   - Approval step obrigatório por 1 reviewer
3. **Production Environment**
   - Trigger: criação de tag sem prefixo (ex: `v2.1.0`)
   - Approval step por 2 reviewers + status checks passados
   - Rollback automático em caso de health check negativo

### Requisitos Técnicos
1. **Secrets e Variáveis**
   - `DEV_CREDENTIALS`, `STAGING_CREDENTIALS`, `PROD_CREDENTIALS`
   - `ENV=dev|staging|prod`
2. **Workflows**
   - `.github/workflows/deploy-dev.yml`
   - `.github/workflows/deploy-staging.yml`
   - `.github/workflows/deploy-prod.yml`
3. **Health Checks e Rollback**
   - Testar endpoint `/health` após deploy
   - Se falhar, executar `rollback.sh`

### Passo a Passo Sugerido
1. Criar arquivo `deploy-dev.yml`:
```yaml
name: Deploy Dev
on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Dev
      run: ./scripts/deploy.sh --env dev --image-tag ${{ github.sha }}
```
2. Criar `deploy-staging.yml` com `workflow_dispatch` e `approval`:
```yaml
name: Deploy Staging
on:
  workflow_dispatch:
    inputs:
      release_branch:
        description: 'Release branch'
        required: true

jobs:
  approval:
    runs-on: ubuntu-latest
    steps:
    - name: Wait for approval
      uses: hmarr/auto-approve-action@v2
      with:
        reviewers: 'team-lead'

  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Staging
      run: ./scripts/deploy.sh --env staging --branch ${{ github.event.inputs.release_branch }}
```
3. Criar `deploy-prod.yml` para tags e rollback:
```yaml
name: Deploy Prod
on:
  push:
    tags: ['v*.*.*']

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run Tests
      run: pytest
  approval:
    needs: checks
    uses: peter-evans/slash-command-dispatch@v2
    with:
      required_approvals: 2
  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Production
      run: |
        ./scripts/deploy.sh --env prod --image-tag ${{ github.ref_name }}
        ./scripts/health-check.sh prod || ./scripts/rollback.sh prod
```

## Exercício 2.3: Workflow com Matrix Strategy 🟡

### Contexto
Você precisa garantir compatibilidade multiplataforma (Linux, Windows, macOS) e múltiplas versões de dependências (Python 3.10, 3.11, 3.12). Um matrix build em GitHub Actions é a solução ideal.

### Objetivos Pedagógicos
- Implementar matrix strategy para test matrix
- Otimizar tempo de execução com paralelização
- Configurar separação de jobs por sistema operacional e versão de runtime
- Analisar resultados agregados

### Cenário
O projeto Python `task-manager` deve garantir que todas as dependências e o código funcionem em:
- Python 3.10, 3.11, 3.12
- Ubuntu, Windows, macOS

### Requisitos Funcionais
1. Matrix de OS e Python versions
2. Cache de dependências para cada ambiente
3. Execução de testes e lint em paralelo
4. Upload de artifacts separados por combinação

### Exemplo de Workflow Matrix
```yaml
name: Matrix Build Tests
on: [ push, pull_request ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run lint
      run: flake8 src/
    - name: Run tests
      run: pytest --junitxml=report-${{ matrix.os }}-${{ matrix.python-version }}.xml
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: report-${{ matrix.os }}-${{ matrix.python-version }}
        path: report-${{ matrix.os }}-${{ matrix.python-version }}.xml
```

### Observações
- Analise os resultados agregados na aba "Actions" do GitHub
- Ajuste o matrix conforme novas versões ou sistemas operacionais
- Combine caching e paralelização para otimizar performance

---
**Parabéns!** Você concluiu todos os exercícios do Nível 2. Agora, prossiga para o Nível 3 para desafios avançados! 🚀
