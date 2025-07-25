#!/usr/bin/env bash
# solucao-3.2: health-check.sh
# Valida endpoints /health e /health/ready de cada microserviço.
# Uso:
#   ./health-check.sh --environment <dev|staging|prod> --timeout <seconds>

set -euo pipefail

ENVIRONMENT=""
TIMEOUT=60
SERVICES=(user-service task-service notification-service analytics-service gateway-service)

# Função de log com timestamp
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [health-check] $1"
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --environment) ENVIRONMENT="$2"; shift 2 ;;    
    --timeout)     TIMEOUT="$2"; shift 2 ;;    
    *) echo "Parâmetro inválido: $1"; exit 1 ;;    
  esac
done

# Validação
debug="false"
[[ -z "$ENVIRONMENT" ]] && { echo "Uso: $0 --environment <ambiente> --timeout <segundos>"; exit 1; }

log "Iniciando health-check para ambiente '$ENVIRONMENT' com timeout de $TIMEOUT segundos"

for svc in "${SERVICES[@]}"; do
  for endpoint in "/health" "/health/ready"; do
    url="http://${svc}.${ENVIRONMENT}.svc.cluster.local:8001${endpoint}"
    log "Verificando $svc$endpoint"
    if ! timeout "$TIMEOUT" curl -sf "$url"; then
      log "Falha no health-check de $svc$endpoint"
      exit 1
    fi
  done
done

log "Todos os serviços respondem corretamente"
