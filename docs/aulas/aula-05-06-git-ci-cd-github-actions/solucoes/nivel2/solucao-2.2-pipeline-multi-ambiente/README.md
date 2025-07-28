# Solução 2.2: Pipeline Multi-Ambiente

## 1. Deploy Dev (.github/workflows/deploy-dev.yml)
```yaml
name: Deploy Dev
on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Dev
        run: ./scripts/deploy.sh --environment dev --image-tag ${{ github.sha }}
```

## 2. Deploy Staging (.github/workflows/deploy-staging.yml)
```yaml
name: Deploy Staging
on:
  workflow_dispatch:
    inputs:
      release_branch:
        description: 'Release branch'
        required: true

jobs:
  approval:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for approval
        uses: hmarr/auto-approve-action@v2
        with:
          reviewers: 'team-lead'

  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: ./scripts/deploy.sh --environment staging --image-tag ${{ github.event.inputs.release_branch }}
```

## 3. Deploy Prod (.github/workflows/deploy-prod.yml)
```yaml
name: Deploy Prod
on:
  push:
    tags: ['v*.*.*']

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: pytest --maxfail=1 --disable-warnings -q

  approval:
    needs: checks
    runs-on: ubuntu-latest
    steps:
      - name: Wait for 2 approvals
        uses: peter-evans/slash-command-dispatch@v2
        with:
          required_approvals: 2

  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          ./scripts/deploy.sh --environment prod --image-tag ${{ github.ref_name }}
          ./scripts/health-check.sh --environment prod --timeout 60 || ./scripts/rollback.sh --environment prod
```

Parabéns! Pipeline multi-ambiente configurado com sucesso.
