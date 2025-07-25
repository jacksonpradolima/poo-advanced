#!/usr/bin/env bash
# solucao-3.2: rollback.sh
# Reverte para a última versão estável e registra logs.
# Uso:
#   ./rollback.sh --environment <dev|staging|prod> [--release <revision>]

set -euo pipefail

ENVIRONMENT=""
RELEASE=""
LOG_DIR="logs"

# Função de log com timestamp
ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() {
  echo "$(ts) [rollback] $1"
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --environment) ENVIRONMENT="$2"; shift 2 ;;    
    --release)     RELEASE="$2"; shift 2 ;;    
    *) echo "Parâmetro inválido: $1"; exit 1 ;;    
  esac
done

# Validação
[[ -z "$ENVIRONMENT" ]] && {
  echo "Uso: $0 --environment <ambiente> [--release <revision>]"
  exit 1
}

mkdir -p "$LOG_DIR"

log "Iniciando rollback em '$ENVIRONMENT'"

# Executar rollback
if [[ -n "$RELEASE" ]]; then
  log "Rollback para release $RELEASE"
  helm rollback myapp "$RELEASE" --namespace "$ENVIRONMENT"
else
  log "Rollback para última release"
  kubectl rollout undo deployment/myapp -n "$ENVIRONMENT"
fi

log "Rollback concluído com sucesso"
