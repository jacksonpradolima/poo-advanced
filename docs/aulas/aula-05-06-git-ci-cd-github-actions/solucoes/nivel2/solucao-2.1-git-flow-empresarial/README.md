# Solução 2.1: Sistema de Branching Empresarial

## 1. Configuração de Git Flow

### 1.1 Inicialização e branches principais
```bash
# Iniciar repositório
cd task-manager
git init

# Criar e configurar branches principais
git checkout -b main
git checkout -b develop
```

### 1.2 Criação de feature branches
```bash
# Feature A: Autenticação JWT
git checkout develop
git checkout -b feature/jwt-auth
# Implementar login/logout com JWT, bcrypt, refresh tokens
# ...código JWT no src/auth/jwt_manager.py...
## Commit das alterações
 git add src/auth/jwt_manager.py src/auth/user_service.py
git commit -m "feat(jwt): implementação de autenticação JWT"
```

### 1.3 Feature B: Sistema de Notificações
```bash
git checkout develop
git checkout -b feature/notifications
# Criar email_service.py e push_service.py no módulo notifications
# ...implementação de envio de notificações...
 git add src/notifications/
git commit -m "feat(notifications): sistema de notificações por email e push"
```

### 1.4 Feature C: Dashboard Analytics
```bash
git checkout develop
git checkout -b feature/analytics
# Criar dashboard.py e metrics.py no módulo analytics
# ...implementação de coleta e exibição de métricas...
 git add src/analytics/
git commit -m "feat(analytics): dashboard de métricas e relatórios"
```

### 1.5 Branch Release e Merge em Main
```bash
# Preparar release v2.0.0
git checkout develop
git checkout -b release/v2.0.0
# Atualizar changelog e bump de versão
# ...altere arquivo setup.py ou version...
 git add CHANGES.md setup.py
git commit -m "chore(release): v2.0.0"

# Merge release em main (preserva histórico)
git checkout main
git merge --no-ff release/v2.0.0 -m "feat: release v2.0.0"

# Tag para produção
git tag -a v2.0.0 -m "Release v2.0.0"

# Merge release em develop
git checkout develop
git merge --no-ff release/v2.0.0
```

### 1.6 Hotfix de Segurança
```bash
# Criar hotfix a partir da main
git checkout main
git checkout -b hotfix/security-fix
# Corrigir SQL injection na src/core/database.py ou em main.py
# Exemplo: usar query parametrizada em vez de f-string
# ...ajuste no código...
 git add src/core/database.py src/main.py
git commit -m "fix(security): SQL injection patched"

# Publicar hotfix
git checkout main
git merge --no-ff hotfix/security-fix -m "fix: security-fix"
git tag -a v2.0.1 -m "Hotfix v2.0.1"

# Propagar em develop
git checkout develop
git merge --no-ff hotfix/security-fix
```

### 1.7 Exemplos de Merge Strategies
| Merge Type        | Comando                           | Uso                                 |
|-------------------|-----------------------------------|-------------------------------------|
| Squash and Merge  | `git merge --squash URL`          | Features em develop, mantém linha única de commit |
| Merge Commit      | `git merge --no-ff release/...`   | Release em main, preserva histórico |
| Cherry-pick       | `git cherry-pick <commit>`        | Propaga hotfix em develop sem merge de branch inteira |

---
Parabéns! O Git Flow empresarial foi implementado com sucesso.
