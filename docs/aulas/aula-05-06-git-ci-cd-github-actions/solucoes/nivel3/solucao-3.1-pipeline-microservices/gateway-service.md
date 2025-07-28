# Gateway Service - Solução Detalhada

## 1. API Gateway com Kong
### 1.1 Configuração do Kong (declarativo)
```yaml
_format_version: "1.1"
services:
  - name: gateway
    url: http://task-service:8002
    routes:
      - name: task-route
        paths:
          - /tasks
  - name: notification
    url: http://notification-service:8003
    routes:
      - name: notify-route
        paths:
          - /notify
plugins:
  - name: rate-limiting
    service: gateway
    config:
      minute: 1000
      policy: local
``` 

## 2. Dockerfile (services/gateway-service/Dockerfile)
```dockerfile
FROM kong:3.0
USER root
COPY kong.yml /usr/local/kong/declarative/kong.yml
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
EXPOSE 8000 8443 8001 8444
CMD ["kong", "docker-start"]
``` 

## 3. CI Workflow (services/gateway-service/.github/workflows/gateway-service-ci.yml)
```yaml
name: Gateway Service CI
on:
  push:
    paths:
      - 'services/gateway-service/**'
  pull_request:
    paths:
      - 'services/gateway-service/**'

jobs:
  test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint Kong config
        run: |
          kong config parse ./kong.yml
      - name: Build & push image
        if: github.event_name == 'push'
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ github.repository }}/gateway-service:${{ env.IMAGE_TAG }} services/gateway-service
          docker push ${{ env.REGISTRY }}/${{ github.repository }}/gateway-service:${{ env.IMAGE_TAG }}
```
