# Notification Service - Solução Detalhada

## 1. API Express (services/notification-service/src/index.js)
```javascript
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = process.env.PORT || 8003;

app.use(bodyParser.json());

// Envio de notificação simulada
app.post('/notify', (req, res) => {
  const { to, type, message } = req.body;
  if (!to || !type || !message) {
    return res.status(400).json({ error: 'Parâmetros inválidos' });
  }
  // Lógica de envio (SMS/Email/Push)
  console.log(`[notification] Enviando ${type} para ${to}: ${message}`);
  res.status(200).json({ status: 'sent' });
});

// Health check
app.get('/health', (req, res) => res.json({ status: 'healthy' }));
app.get('/health/ready', (req, res) => res.json({ status: 'ready' }));

app.listen(port, () => console.log(`Notification Service rodando na porta ${port}`));
``` 

## 2. Dockerfile (services/notification-service/Dockerfile)
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production

FROM node:18-alpine as runtime
RUN addgroup -S appuser && adduser -S appuser -G appuser
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8003
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -qO- http://localhost:8003/health || exit 1
CMD ["node", "src/index.js"]
``` 

## 3. CI Workflow (services/notification-service/.github/workflows/notification-service-ci.yml)
```yaml
name: Notification Service CI
on:
  push:
    paths:
      - 'services/notification-service/**'
  pull_request:
    paths:
      - 'services/notification-service/**'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd services/notification-service
          npm ci
      - name: Run lint
        run: |
          cd services/notification-service
          npm run lint
      - name: Run tests
        run: |
          cd services/notification-service
          npm test
      - name: Build & push Docker image
        if: github.event_name == 'push'
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ github.repository }}/notification-service:${{ env.IMAGE_TAG }} services/notification-service
          docker push ${{ env.REGISTRY }}/${{ github.repository }}/notification-service:${{ env.IMAGE_TAG }}
```
