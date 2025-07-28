# Instrumentação - Exemplos de Código

## Python (FastAPI)
```python
from prometheus_client import Counter, Histogram, start_http_server
from jaeger_client import Config

# Métricas
REQUEST_COUNT = Counter('request_count', 'Total de requisições', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latência das requisições')

# Iniciar servidor de métricas
start_http_server(8002)

# Configuração Jaeger
config = Config(
    config={
        'sampler': {'type': 'const', 'param': 1},
        'logging': True,
    },
    service_name='user-service'
)
tracer = config.initialize_tracer()

# Exemplo de endpoint
@app.middleware('http')
async def metrics_middleware(request, call_next):
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    return response
``` 

## Node.js (Express)
```javascript
const client = require('prom-client');
const initTracer = require('jaeger-client').initTracer;

// Métricas
const requestCount = new client.Counter({ name: 'request_count', help: 'Total de requisições', labelNames: ['method', 'path'] });
const requestLatency = new client.Histogram({ name: 'request_latency_seconds', help: 'Latência das requisições' });

// Iniciar servidor de métricas
const express = require('express');
const app = express();
client.collectDefaultMetrics();
app.get('/metrics', (req, res) => res.send(client.register.metrics()));

// Configurar Jaeger
const tracer = initTracer({
  serviceName: 'notification-service',
  sampler: { type: 'const', param: 1 },
  reporter: { logSpans: true }
});

// Middleware de métricas
app.use((req, res, next) => {
  const end = requestLatency.startTimer();
  res.on('finish', () => {
    requestCount.labels(req.method, req.path).inc();
    end();
  });
  next();
});
```
