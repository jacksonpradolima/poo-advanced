# Exercícios Nível 3 - Avançado 🔴

## Visão Geral

Os exercícios do Nível 3 representam o ápice da complexidade, simulando cenários reais de empresas de tecnologia de grande escala. Cada exercício deve ser completado em 2-4 horas e requer design arquitetural, tomada de decisões críticas e implementação de soluções production-ready.

---

## Exercício 3.1: Pipeline Completo com Microserviços 🔴

### Contexto
Sua startup se tornou uma scale-up e está migrando para arquitetura de microserviços. Como Senior DevOps Engineer, você foi designado para criar um pipeline de CI/CD completo que suporte múltiplos serviços, deployment independente, observabilidade e rollback automático.

### Objetivos Pedagógicos
- Arquitetar pipeline enterprise-grade para microserviços
- Implementar deployment strategies avançadas (blue-green, canary)
- Configurar observabilidade completa (logs, métricas, traces)
- Aplicar Infrastructure as Code (IaC) com Terraform
- Implementar security scanning e compliance

### Cenário
A arquitetura evoluiu para **5 microserviços independentes**:

1. **User Service** (Python/FastAPI) - Gestão de usuários e autenticação
2. **Task Service** (Python/FastAPI) - CRUD de tarefas e workflows
3. **Notification Service** (Node.js/Express) - Email, SMS, push notifications
4. **Analytics Service** (Python/FastAPI) - Métricas e relatórios
5. **Gateway Service** (Nginx/Kong) - API Gateway e rate limiting

Cada serviço possui:
- Pipeline independente de CI/CD
- Banco de dados dedicado (PostgreSQL, Redis, MongoDB)
- Deployment strategy configurável
- Monitoramento e alertas personalizados

### Requisitos Funcionais

1. **Arquitetura de Microserviços**
```
microservices-platform/
├── services/
│   ├── user-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── requirements.txt
│   │   └── .github/workflows/user-service-ci.yml
│   ├── task-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── .github/workflows/task-service-ci.yml
│   ├── notification-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── .github/workflows/notification-service-ci.yml
│   ├── analytics-service/
│   │   └── [similar structure]
│   └── gateway-service/
│       └── [nginx configs + CI/CD]
├── infrastructure/
│   ├── terraform/
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   ├── modules/
│   │   │   ├── kubernetes/
│   │   │   ├── monitoring/
│   │   │   └── networking/
│   │   └── shared/
│   ├── kubernetes/
│   │   ├── base/
│   │   ├── overlays/
│   │   └── monitoring/
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── jaeger/
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health-check.sh
└── .github/
    └── workflows/
        ├── infrastructure-ci.yml
        └── e2e-tests.yml
```

2. **Pipeline Features Avançadas**

**Multi-Service Detection**
- Detectar mudanças por serviço usando path filters
- Build e deploy apenas serviços modificados
- Dependency tracking entre serviços

**Deployment Strategies**
- **Blue-Green**: Zero-downtime deployments
- **Canary**: Gradual traffic shifting (10% → 50% → 100%)
- **A/B Testing**: Feature flag integration
- **Rolling Updates**: Kubernetes native deployments

**Security & Compliance**
- Container image scanning (Trivy, Snyk)
- Secret management (HashiCorp Vault)
- RBAC e service mesh (Istio)
- Compliance checks (SOC2, GDPR)

**Observabilidade**
- **Metrics**: Prometheus + Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger distributed tracing
- **Alerting**: PagerDuty integration

### Requisitos Técnicos

1. **Infrastructure as Code**
```hcl
# infrastructure/terraform/modules/kubernetes/main.tf
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.16"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.7"
    }
  }
}

resource "kubernetes_namespace" "microservices" {
  for_each = toset(var.namespaces)
  
  metadata {
    name = each.value
    labels = {
      environment = var.environment
      managed-by  = "terraform"
    }
  }
}

# Service mesh (Istio)
resource "helm_release" "istio_base" {
  name       = "istio-base"
  repository = "https://istio-release.storage.googleapis.com/charts"
  chart      = "base"
  namespace  = "istio-system"
  
  create_namespace = true
  
  values = [
    yamlencode({
      global = {
        meshID = var.environment
        network = var.environment
      }
    })
  ]
}

# Monitoring stack
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "monitoring"
  
  create_namespace = true
  
  values = [
    file("${path.module}/values/prometheus-values.yaml")
  ]
}
```

2. **Multi-Service CI/CD Workflow**
```yaml
# .github/workflows/microservices-ci.yml
name: Microservices CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_TAG: ${{ github.sha }}

jobs:
  # Detectar mudanças em serviços
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      user-service: ${{ steps.changes.outputs.user-service }}
      task-service: ${{ steps.changes.outputs.task-service }}
      notification-service: ${{ steps.changes.outputs.notification-service }}
      analytics-service: ${{ steps.changes.outputs.analytics-service }}
      gateway-service: ${{ steps.changes.outputs.gateway-service }}
      infrastructure: ${{ steps.changes.outputs.infrastructure }}
    
    steps:
    - uses: actions/checkout@v4
    - uses: dorny/paths-filter@v2
      id: changes
      with:
        filters: |
          user-service:
            - 'services/user-service/**'
          task-service:
            - 'services/task-service/**'
          notification-service:
            - 'services/notification-service/**'
          analytics-service:
            - 'services/analytics-service/**'
          gateway-service:
            - 'services/gateway-service/**'
          infrastructure:
            - 'infrastructure/**'

  # Matrix strategy para build de serviços
  build-services:
    needs: detect-changes
    if: |
      needs.detect-changes.outputs.user-service == 'true' ||
      needs.detect-changes.outputs.task-service == 'true' ||
      needs.detect-changes.outputs.notification-service == 'true' ||
      needs.detect-changes.outputs.analytics-service == 'true' ||
      needs.detect-changes.outputs.gateway-service == 'true'
    
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        service: 
        - name: user-service
          changed: ${{ needs.detect-changes.outputs.user-service }}
          language: python
          dockerfile: services/user-service/Dockerfile
        - name: task-service
          changed: ${{ needs.detect-changes.outputs.task-service }}
          language: python
          dockerfile: services/task-service/Dockerfile
        - name: notification-service
          changed: ${{ needs.detect-changes.outputs.notification-service }}
          language: node
          dockerfile: services/notification-service/Dockerfile
        - name: analytics-service
          changed: ${{ needs.detect-changes.outputs.analytics-service }}
          language: python
          dockerfile: services/analytics-service/Dockerfile
        - name: gateway-service
          changed: ${{ needs.detect-changes.outputs.gateway-service }}
          language: nginx
          dockerfile: services/gateway-service/Dockerfile
    
    steps:
    - name: Skip if service unchanged
      if: matrix.service.changed != 'true'
      run: echo "Skipping ${{ matrix.service.name }} - no changes detected"
    
    - uses: actions/checkout@v4
      if: matrix.service.changed == 'true'
    
    - name: Setup language environment
      if: matrix.service.changed == 'true'
      uses: ./.github/actions/setup-${{ matrix.service.language }}
    
    - name: Run tests
      if: matrix.service.changed == 'true'
      run: |
        cd services/${{ matrix.service.name }}
        make test
    
    - name: Security scan
      if: matrix.service.changed == 'true'
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: services/${{ matrix.service.name }}/security-scan.sarif
    
    - name: Build and push Docker image
      if: matrix.service.changed == 'true' && github.event_name == 'push'
      uses: docker/build-push-action@v4
      with:
        context: services/${{ matrix.service.name }}
        file: ${{ matrix.service.dockerfile }}
        push: true
        tags: |
          ${{ env.REGISTRY }}/${{ github.repository }}/${{ matrix.service.name }}:${{ env.IMAGE_TAG }}
          ${{ env.REGISTRY }}/${{ github.repository }}/${{ matrix.service.name }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Testes de integração entre serviços
  integration-tests:
    needs: [detect-changes, build-services]
    if: always() && (needs.build-services.result == 'success' || needs.build-services.result == 'skipped')
    
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup test environment
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30  # Wait for services to be ready
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --tb=short
        
    - name: Run E2E tests
      run: |
        pytest tests/e2e/ -v --tb=short --html=e2e-report.html
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: integration-test-results
        path: |
          e2e-report.html
          tests/reports/

  # Deploy para ambientes
  deploy:
    needs: [detect-changes, build-services, integration-tests]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    runs-on: ubuntu-latest
    environment: production
    
    strategy:
      matrix:
        environment: [staging, production]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Kubernetes
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.28.0'
    
    - name: Deploy infrastructure changes
      if: needs.detect-changes.outputs.infrastructure == 'true'
      run: |
        cd infrastructure/terraform/environments/${{ matrix.environment }}
        terraform init
        terraform plan -out=tfplan
        terraform apply tfplan
    
    - name: Deploy changed services
      run: |
        ./scripts/deploy.sh \
          --environment ${{ matrix.environment }} \
          --image-tag ${{ env.IMAGE_TAG }} \
          --strategy canary \
          --health-check-timeout 300
    
    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh ${{ matrix.environment }}
    
    - name: Promote canary deployment
      run: |
        ./scripts/promote-canary.sh ${{ matrix.environment }}
```

### Implementação Detalhada

#### Fase 1: Arquitetura de Microserviços (60 min)

**1.1 User Service Implementation**
```python
# services/user-service/src/main.py
"""
User Service - Microserviço de gestão de usuários.
Responsável por autenticação, autorização e CRUD de usuários.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from contextlib import asynccontextmanager

from .database import engine, get_db, create_tables
from .models import User, UserCreate, UserUpdate, UserResponse
from .services import UserService, AuthService
from .middleware import RequestLoggingMiddleware, MetricsMiddleware
from .config import Settings

# Configurações
settings = Settings()

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia lifecycle da aplicação."""
    # Startup
    create_tables()
    print("🚀 User Service started successfully")
    yield
    # Shutdown
    print("🔄 User Service shutting down")

# FastAPI app
app = FastAPI(
    title="User Service",
    description="Microserviço de gestão de usuários e autenticação",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Dependency injection
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Injeta instância do UserService."""
    return UserService(db)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Injeta instância do AuthService."""
    return AuthService(db)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Obtém usuário atual através do token JWT."""
    token = credentials.credentials
    user = await auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return user

# Health checks
@app.get("/health")
async def health_check():
    """Health check endpoint para load balancer."""
    return {
        "status": "healthy",
        "service": "user-service",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check para Kubernetes."""
    try:
        # Verificar conexão com banco
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

@app.get("/health/live")
async def liveness_check():
    """Liveness check para Kubernetes."""
    return {"status": "alive"}

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Registra novo usuário."""
    try:
        user = await user_service.create_user(user_data)
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/auth/login")
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Autentica usuário e retorna tokens."""
    try:
        tokens = await auth_service.authenticate(
            credentials.email, 
            credentials.password
        )
        return {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "token_type": "bearer",
            "expires_in": 3600
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@app.post("/auth/refresh")
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Renova access token usando refresh token."""
    try:
        new_token = await auth_service.refresh_access_token(
            refresh_data.refresh_token
        )
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": 3600
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@app.post("/auth/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Faz logout do usuário (invalida tokens)."""
    await auth_service.logout_user(current_user.id)
    return {"message": "Logout successful"}

# User management endpoints
@app.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Retorna perfil do usuário atual."""
    return UserResponse.from_orm(current_user)

@app.put("/users/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Atualiza perfil do usuário atual."""
    try:
        updated_user = await user_service.update_user(
            current_user.id, 
            user_data
        )
        return UserResponse.from_orm(updated_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Lista usuários (apenas para admins)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users = await user_service.list_users(skip=skip, limit=limit)
    return [UserResponse.from_orm(user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Obtém usuário por ID (apenas para admins ou próprio usuário)."""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)

# Metrics endpoint (Prometheus format)
@app.get("/metrics")
async def metrics():
    """Métricas no formato Prometheus."""
    from .metrics import generate_prometheus_metrics
    return generate_prometheus_metrics()

# Admin endpoints
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Deleta usuário (apenas para admins)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=settings.debug,
        log_level="info"
    )
```

**1.2 Dockerfile Multi-stage para User Service**
```dockerfile
# services/user-service/Dockerfile
# Multi-stage build para otimização
FROM python:3.12-slim as builder

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim as runtime

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar apenas dependências runtime necessárias
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar virtual environment do builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Criar diretório da aplicação
WORKDIR /app

# Copiar código da aplicação
COPY --chown=appuser:appuser . .

# Mudar para usuário não-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Expor porta
EXPOSE 8001

# Comando padrão
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

Preciso continuar com a implementação completa? Ainda temos muito conteúdo para gerar:

1. Task Service, Notification Service, Analytics Service, Gateway Service
2. Infrastructure as Code completa (Terraform + Kubernetes)
3. Observabilidade (Prometheus, Grafana, Jaeger)
4. Scripts de deployment e rollback
5. Exercícios 3.2 e 3.3
6. Todas as soluções dos exercícios

Conforme suas instruções: "Se você ficar sem tokens ou se a resposta atingir o limite de comprimento, então por favor, me espere dizer 'Go' para continuar gerando o conteúdo."

Aguardo seu "Go" para continuar com a implementação completa dos exercícios avançados e todas as soluções!

---

## Exercício 3.2: Scripts de Deployment e Rollback 🔴

### Contexto
Nesta etapa, você criará scripts robustos em Bash para automatizar o processo de deployment e rollback dos microserviços no cluster Kubernetes, garantindo operações seguras, idempotentes e com tratamento de erros.

### Objetivos Pedagógicos
- Desenvolver scripts Bash com parâmetros e validações.
- Implementar práticas de logging e tratamento de erros (set -euo pipefail).
- Automatizar health checks antes e após deployments.
- Garantir rollback automático em caso de falhas.

### Cenário
Utilizando a arquitetura definida no Exercício 3.1, crie três scripts na pasta `scripts/`:
1. `deploy.sh`  
2. `rollback.sh`  
3. `health-check.sh`

### Requisitos Funcionais
1. **deploy.sh** deve:
   - Aceitar argumentos: `--environment`, `--image-tag`, `--strategy`, `--health-timeout`.
   - Verificar a validade dos parâmetros.
   - Executar comandos `kubectl` ou `helm` para aplicar manifests com a imagem especificada.
   - Realizar health checks invocando `health-check.sh` após o deploy.
   - Em caso de falha, chamar automaticamente o `rollback.sh`.

2. **rollback.sh** deve:
   - Aceitar argumentos: `--environment` e opcional `--release`.
   - Reverter para a última versão estável usando `helm rollback` ou `kubectl rollout undo`.
   - Registrar logs de rollback em arquivo `logs/rollback-<timestamp>.log`.

3. **health-check.sh** deve:
   - Aceitar `--environment` e `--timeout`.
   - Iterar sobre cada serviço, chamando o endpoint `/health` e `/health/ready`.
   - Retornar código de saída não-zero se qualquer verificação falhar.

### Requisitos Técnicos
- Use Bash com `#!/usr/bin/env bash`, `set -euo pipefail`.
- Validate positional e flags com `getopts`.
- Utilize `trap` para captura de sinais e limpeza.
- Implemente logs detalhados com timestamps.

### Entregáveis
- Arquivos em `scripts/deploy.sh`, `scripts/rollback.sh`, `scripts/health-check.sh`.
- Documentação de uso no topo de cada script.

### Critérios de Avaliação
- Scripts idempotentes e com tratamento de erros.
- Parâmetros validados corretamente.
- Logs informativos e legíveis.
- Rollback acionado automaticamente em falhas.

### Dicas
- Utilize arrays para listar serviços e iterar.
- Use `kubectl rollout status` com timeout.
- Formate logs em `YYYY-MM-DD HH:MM:SS`.

### Extensões (Opcional)
- Implementar suporte a feature flags via ConfigMap.
- Enviar notificação ao Slack em eventos de deploy e rollback.

---

## Exercício 3.3: Observabilidade e Monitoramento 🔴

### Contexto
Você integrará um stack de observabilidade completo para coletar métricas, logs e traces dos microserviços, permitindo monitorar a saúde e o desempenho em produção.

### Objetivos Pedagógicos
- Configurar Prometheus, Grafana e Jaeger via IaC.
- Definir regras de alerta e dashboards personalizados.
- Instrumentar código para métricas e tracing.

### Cenário
A infraestrutura deve incluir:
- Prometheus para coleta de métricas.
- Grafana para dashboards.
- Jaeger para tracing distribuído.
- Alertmanager para notificações (ex: PagerDuty).

### Requisitos Funcionais
1. **Prometheus**:
   - Arquivo `monitoring/prometheus/alerts.yaml` com regras para:
     - Pod crash loop.
     - Latência de requisição acima de 500ms.
     - CPU ou memória acima de 80%.

2. **Grafana**:
   - Dashboards em JSON em `monitoring/grafana/` para:
     - Visão geral de serviços (health, latência).
     - Métricas de uso de recursos.

3. **Jaeger**:
   - Configuração de tracing em `monitoring/jaeger/` via Helm ou manifest.
   - Instrumentação básica nos serviços Python e Node.js (bibliotecas `prometheus_client`, `jaeger-client`).

4. **Alertmanager**:
   - Integração com PagerDuty (roteamento e receptores).

### Requisitos Técnicos
- Use Helm charts oficiais ou manifests YAML.
- Versionamento dos dashboards no repositório.
- Exemplos de código prontamente executáveis para instrumentação.

### Entregáveis
- Arquivos de configuração em `monitoring/`.
- Trechos de código de instrumentação em `services/.../src/instrumentation.py` (ou equivalente).
- README explicando como aplicar o stack e visualizar alerts.

### Critérios de Avaliação
- Regras de alerta corretas e eficazes.
- Dashboards informativos e organizados.
- Tracing funcionando e associado a requests reais.
- Documentação clara para replicação.

### Dicas
- Utilize `helm repo add` e `helm install --namespace`.
- Teste alertas ajustando thresholds.
- Gere spans em endpoints críticos (ex: autenticação, CRUD).

### Extensões (Opcional)
- Configurar Logstash e Kibana para centralizar logs.
- Implementar tracing avançado com baggage e contexto.
