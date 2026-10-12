# Dashboard de Vendas

Sistema simples de gerenciamento e visualização de vendas em **Python (Flask)** com persistência em **PostgreSQL**. Permite listar vendas, cadastrar novos registros, exportar CSV e gerar gráficos com Pandas/Matplotlib.

O projeto também inclui uma suíte de **QA Automation** (pytest + Playwright) pensada para portfólio de QA Júnior.

## Tecnologias

- Python 3
- Flask + Jinja2
- PostgreSQL (`psycopg2`)
- Pandas e Matplotlib
- pytest e Playwright (desenvolvimento/QA)

## Funcionalidades

- Cadastro de vendas (cliente, produto, valor e data)
- Listagem em tabela
- Exportação CSV em `/export`
- Gráficos estáticos gerados por `relatorio.py`
- Sem filtros na interface atual

## Como iniciar (Windows / PowerShell)

Não use o Live Server / Go Live. A aplicação precisa do Flask.

```powershell
cd caminho\para\Dashboard-de-Vendas-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edite o `.env` local com os dados do seu PostgreSQL. O arquivo `.env` não deve ser versionado.

```powershell
python app.py
```

Abra **http://127.0.0.1:5000** no navegador.

Para atualizar CSV e gráficos a partir do banco:

```powershell
python relatorio.py
```

## PostgreSQL

Banco esperado: `dashboard_vendas`. Tabela: `relatorio_vendas`.

```sql
CREATE DATABASE dashboard_vendas;
```

Depois, no banco criado:

```bash
psql -U postgres -d dashboard_vendas -f schema.sql
```

`schema.sql` cria a tabela se ela ainda não existir. Ele **não** apaga dados e **não** reinsere o CSV. Se os 50 registros do CSV já foram importados, não rode o script de INSERT novamente para evitar duplicatas.

Variáveis (veja `.env.example`):

- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

## Testes

```powershell
pip install -r requirements-dev.txt
python -m playwright install chromium
pytest
```

Sem PostgreSQL (adequado para CI):

```powershell
pytest -m "not db"
```

Relatório HTML: `qa/reports/report.html`. Detalhes em `qa/README.md`.

## Estrutura

```
Dashboard-de-Vendas-main
├── app.py
├── db.py
├── relatorio.py
├── schema.sql
├── relatorio_vendas.csv
├── templates/
├── static/graficos/
├── qa/
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Limitações conhecidas

- A listagem não tem filtros, paginação nem autenticação.
- Os gráficos não são gerados a cada request; é preciso executar `relatorio.py`.
- A conexão real com o banco é obrigatória para usar a aplicação no navegador; os testes de integração/UI usam uma conexão falsa e não alteram dados de produção.

## Autor

Pedro Luís dos Santos Souza
