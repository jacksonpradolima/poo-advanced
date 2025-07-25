# Solução 2.3: Workflow com Matrix Strategy

## Arquivo: .github/workflows/matrix-build-tests.yml
```yaml
name: Matrix Build Tests
on: [ push, pull_request ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run Linter
      run: flake8 src/
    - name: Run Tests
      run: pytest --junitxml=report-${{ matrix.os }}-${{ matrix.python-version }}.xml
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: report-${{ matrix.os }}-${{ matrix.python-version }}
        path: report-${{ matrix.os }}-${{ matrix.python-version }}.xml
```

## Otimizações
- Configure cache de dependências para `pip` e `npm` caso aplique múltiplas stacks.
- Aplique `continue-on-error` para builds não críticos enquanto monitora métricas da matriz.
- Use `fail-fast: false` para obter cobertura total de matrix.

---
Parabéns! Todos os exercícios do Nível 2 foram solucionados com sucesso. Prosseguindo para o Nível 3 de implementações complexas.
