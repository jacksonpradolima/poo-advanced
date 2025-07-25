# Task Service - Solução Detalhada

## 1. API FastAPI (services/task-service/src/main.py)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Task Service", version="1.0.0")

# Modelo de dados
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Armazenamento em memória (exemplo simplificado)
_tasks: List[Task] = []
_next_id = 1

# Endpoints CRUD
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    global _next_id
    task.id = _next_id
    _next_id += 1
    _tasks.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return _tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for t in _tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: Task):
    for idx, t in enumerate(_tasks):
        if t.id == task_id:
            updated = payload.copy()
            updated.id = task_id
            _tasks[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global _tasks
    _tasks = [t for t in _tasks if t.id != task_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
``` 

## 2. Dockerfile (services/task-service/Dockerfile)
```dockerfile
FROM python:3.12-slim as builder
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim as runtime
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8002
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8002/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
``` 

## 3. CI Workflow (services/task-service/.github/workflows/task-service-ci.yml)
```yaml
name: Task Service CI
on:
  push:
    paths:
      - 'services/task-service/**'
  pull_request:
    paths:
      - 'services/task-service/**'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd services/task-service
          pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd services/task-service
          pytest --maxfail=1 --disable-warnings -q
      - name: Build & push Docker image
        if: github.event_name == 'push'
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ github.repository }}/task-service:${{ env.IMAGE_TAG }} services/task-service
          docker push ${{ env.REGISTRY }}/${{ github.repository }}/task-service:${{ env.IMAGE_TAG }}
```
