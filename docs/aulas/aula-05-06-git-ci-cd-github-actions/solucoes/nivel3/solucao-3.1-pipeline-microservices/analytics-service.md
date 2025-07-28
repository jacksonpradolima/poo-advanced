# Analytics Service - Solução Detalhada

## 1. API FastAPI (services/analytics-service/src/main.py)
```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Analytics Service", version="1.0.0")

class MetricsQuery(BaseModel):
    service_name: str
    start_time: str
    end_time: str

@app.post("/metrics", response_model=dict)
def query_metrics(payload: MetricsQuery):
    # Simulação de consulta a datastore
    return {
        "service": payload.service_name,
        "count": 123,
        "average_latency": 0.34,
        "time_range": [payload.start_time, payload.end_time]
    }

@app.get("/health", response_model=dict)
def health_check():
    return {"status": "healthy"}

@app.get("/health/ready", response_model=dict)
def readiness_check():
    return {"status": "ready"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
```  

## 2. Dockerfile (services/analytics-service/Dockerfile)
```dockerfile
FROM python:3.12-slim as builder
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim as runtime
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8004
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8004/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8004"]
```  

## 3. CI Workflow (services/analytics-service/.github/workflows/analytics-service-ci.yml)
```yaml
name: Analytics Service CI
on:
  push:
    paths:
      - 'services/analytics-service/**'
  pull_request:
    paths:
      - 'services/analytics-service/**'

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies & test
        run: |
          cd services/analytics-service
          pip install -r requirements.txt
          pytest --maxfail=1 --disable-warnings -q
      - name: Build & push image
        if: github.event_name == 'push'
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ github.repository }}/analytics-service:${{ env.IMAGE_TAG }} services/analytics-service
          docker push ${{ env.REGISTRY }}/${{ github.repository }}/analytics-service:${{ env.IMAGE_TAG }}
```
