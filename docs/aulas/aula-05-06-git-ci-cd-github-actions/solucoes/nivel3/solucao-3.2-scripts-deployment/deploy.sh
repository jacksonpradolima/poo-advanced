#!/usr/bin/env bash
# solucao-3.2: deploy.sh
# Automatiza o deployment no Kubernetes com rollback automático em caso de falha.
# Uso:
#   ./deploy.sh --environment <dev|staging|prod> --image-tag <tag> --strategy <canary|blue-green> --health-timeout <seconds>

set -euo pipefail

# Variáveis padrão
ENVIRONMENT=""
IMAGE_TAG=""
STRATEGY=""
HEALTH_TIMEOUT=60
LOG_DIR="logs"

# Função de log com timestamp
log() {
  local msg="$1"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [deploy] $msg"
}

# Parâmetros
while [[ $# -gt 0 ]]; do
  case "$1" in
    --environment) ENVIRONMENT="$2"; shift 2 ;;    
    --image-tag)   IMAGE_TAG="$2"; shift 2 ;;    
    --strategy)    STRATEGY="$2"; shift 2 ;;    
    --health-timeout) HEALTH_TIMEOUT="$2"; shift 2 ;;    
    *) echo "Parâmetro inválido: $1"; exit 1 ;;
  esac
done

# Validação de parâmetros
[[ -z "$ENVIRONMENT" || -z "$IMAGE_TAG" || -z "$STRATEGY" ]] && {
  echo "Uso: $0 --environment <ambiente> --image-tag <tag> --strategy <canary|blue-green> [--health-timeout <segundos>]"
  exit 1
}

# Criar diretório de logs
mkdir -p "$LOG_DIR"

# Função de rollback (invoca rollback.sh)
on_error() {
  log "Falha detectada. Iniciando rollback..."
  ./rollback.sh --environment "$ENVIRONMENT" | tee -a "$LOG_DIR/rollback-$(date '+%Y%m%d%H%M%S').log"
  exit 1
}
trap 'on_error' ERR INT

log "Iniciando deployment: env=$ENVIRONMENT, tag=$IMAGE_TAG, strategy=$STRATEGY"

# Aplicar manifests conforme estratégia
case "$STRATEGY" in
  canary)
    log "Executando canary deployment"
    kubectl set image deployment/myapp myapp=${IMAGE_TAG} -n "$ENVIRONMENT"
    ;;
  blue-green)
    log "Executando blue-green deployment"
    helm upgrade blue-green mychart/ --namespace "$ENVIRONMENT" --install --set image.tag="${IMAGE_TAG}"
    ;;
  *)
    echo "Estratégia inválida: $STRATEGY"; exit 1
    ;;
esac

# Health check
log "Aguardando ${HEALTH_TIMEOUT}s antes do health-check"
sleep "$HEALTH_TIMEOUT"
./health-check.sh --environment "$ENVIRONMENT" --timeout "$HEALTH_TIMEOUT"

log "Deployment concluído com sucesso"
