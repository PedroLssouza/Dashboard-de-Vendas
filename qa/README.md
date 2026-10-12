# QA — Dashboard de Vendas

Automação e artefatos de teste do dashboard Flask.

## Estrutura

```
qa/
├── tests/           # pytest
├── evidencias/      # screenshots de falha (não versionar PNG)
├── reports/         # relatório HTML do pytest
└── docs/            # plano, casos e defeitos
```

## Como executar

Na raiz do projeto, com o ambiente virtual ativado:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m playwright install chromium
pytest
```

Somente testes que não usam PostgreSQL:

```powershell
pytest -m "not db"
```

Somente interface:

```powershell
pytest -m ui
```

Relatório HTML gerado em `qa/reports/report.html`.

Os testes de dashboard, exportação e UI usam uma conexão falsa. Eles **não inserem nem apagam** registros do PostgreSQL real. Os testes marcados com `db` são somente leitura.
