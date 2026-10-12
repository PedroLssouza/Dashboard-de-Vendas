# 📊 Dashboard de Vendas & QA Automation

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg)
![Pytest](https://img.shields.io/badge/tests-Pytest%20%7C%2024%20passed-brightgreen.svg)
![Playwright](https://img.shields.io/badge/E2E-Playwright-45ba4b.svg)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)

Aplicação web em **Python (Flask)** com persistência em **PostgreSQL** para gestão e acompanhamento de vendas, integrada a um projeto completo de **Engenharia de Qualidade e QA Automation** (testes automatizados de API, integridade de dados, banco e interface E2E).

---

## 🎯 O Que Foi Feito no Projeto

### 1. Auditoria e Correções na Aplicação (Bug Fixes)
- **DEF-01 (Visual / Acessibilidade):** Correção de herança de CSS em `templates/index.html`. Os títulos `<h2>` herdavam a cor branca global, tornando-os invisíveis sobre o fundo claro. Foi criada uma regra de contraste específica (`main h2 { color: #333; }`).
- **DEF-02 (Funcional / Crítico):** Correção na rota `/export` em `app.py`. A função passava um objeto `flask.Response` diretamente ao `csv.writer`, gerando `TypeError`. O fluxo foi refatorado utilizando buffer em memória `io.StringIO`, normalizando o download do CSV.
- **Estruturação de Seletores:** Inclusão de atributos semânticos `data-testid` nos templates HTML para suporte a testes E2E robustos e desacoplados de estilo.

### 2. Engenharia de Testes e Automação (24 Testes — 100% Aprovados)
Implementação de suíte de testes com **Pytest** e **Playwright**, cobrindo todas as camadas da aplicação sem risco a dados reais (utilizando injeção de dependências e banco simulado com `fakes.py`):

| Categoria | Arquivo | Cobertura | Status |
| :--- | :--- | :--- | :---: |
| **Rotas & Validações** | `qa/tests/test_dashboard.py` | Status HTTP, renderização de tabelas, regras de campos obrigatórios e valores inválidos | **7/7 ✅** |
| **Integridade de Dados** | `qa/tests/test_data.py` | Leitura do CSV base, tipos numéricos, datas, valores negativos e consistência de agrupamentos | **6/6 ✅** |
| **Banco de Dados** | `qa/tests/test_db.py` | Conectividade PostgreSQL, conformidade de schema/tipos e integridade de registros | **4/4 ✅** |
| **Exportações & Relatórios**| `qa/tests/test_reports.py` | Download do CSV (`/export`), cabeçalhos HTTP e geração de gráficos com Pandas/Matplotlib | **3/3 ✅** |
| **End-to-End (UI)** | `qa/tests/test_ui.py` | Navegação real com navegador headless (Playwright/Chromium), verificação de gráficos e fluxo de exportação | **4/4 ✅** |
| **Total** | | **Suíte completa executada em ~4s** | **24/24 ✅** |

### 3. Documentação Formal de QA
Na pasta [`qa/docs/`](qa/docs/):
- **`plano_de_testes.md`:** Escopo, estratégia de testes, pirâmide de automação, critérios de aceite e ambientes.
- **`casos_de_teste.md`:** Matriz rastreável com 25 casos de teste documentados com passos, massa e resultados obtidos.
- **`relatorio_de_defeitos.md`:** Documentação detalhada dos defeitos encontrados (DEF-01 e DEF-02) com causa-raiz e evidências de resolução.

### 4. Integração Contínua (CI/CD)
- Configuração de pipeline no GitHub Actions ([`.github/workflows/qa.yml`](.github/workflows/qa.yml)) que executa automaticamente a suíte de testes (com isolamento de banco via `pytest -m "not db"`) e gera artefatos de relatório a cada `push` e `pull request`.

---

## 🛠️ Tecnologias Utilizadas

- **Back-end:** Python 3, Flask, Jinja2
- **Banco de Dados:** PostgreSQL, `psycopg2-binary`
- **Análise e Gráficos:** Pandas, Matplotlib
- **Testes & Automação:** Pytest, pytest-playwright (Chromium), pytest-html
- **Configuração:** `python-dotenv`

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.10+ instalado
- PostgreSQL rodando localmente (opcional para rodar apenas os testes)

### 1. Clonar e preparar o ambiente
```powershell
git clone https://github.com/PedroLssouza/Dashboard-de-Vendas.git
cd Dashboard-de-Vendas

# Criar e ativar o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências da aplicação
pip install -r requirements.txt
```

### 2. Configuração de Variáveis de Ambiente
Copie o modelo de exemplo para criar seu arquivo local:
```powershell
copy .env.example .env
```
Preencha o `.env` com os dados do seu banco PostgreSQL local:
```env
PGHOST=localhost
PGPORT=5432
PGUSER=seu_usuario
PGPASSWORD=sua_senha
PGDATABASE=dashboard_vendas
```
*(Nota de segurança: O arquivo `.env` está no `.gitignore` e nunca é enviado ao repositório).*

### 3. Banco de Dados e Execução
Execute o script DDL no PostgreSQL para criar a tabela necessária:
```powershell
psql -U postgres -d dashboard_vendas -f schema.sql
```

Inicie o servidor Flask:
```powershell
python app.py
```
Acesse no navegador: **http://127.0.0.1:5000**

Para gerar os gráficos a partir dos dados do banco:
```powershell
python relatorio.py
```

---

## 🧪 Como Executar a Suíte de Testes

Instale as dependências de desenvolvimento e os navegadores do Playwright:
```powershell
pip install -r requirements-dev.txt
python -m playwright install chromium
```

### Execuções disponíveis:

```powershell
# Executar todos os 24 testes
pytest -v

# Executar sem necessidade de banco de dados ativo (modo CI)
pytest -m "not db"

# Executar somente testes de interface gráfica (Playwright E2E)
pytest -m "ui"

# Executar somente testes de banco de dados
pytest -m "db"
```

O relatório visual em HTML é gerado automaticamente em `qa/reports/report.html`.

---

## 📁 Estrutura do Projeto

```text
Dashboard-de-Vendas/
├── .github/workflows/       # Pipeline de CI/CD (GitHub Actions)
├── qa/
│   ├── docs/                # Documentação formal (Plano, Casos e Defeitos)
│   ├── reports/             # Relatórios de execução HTML
│   └── tests/               # Testes automatizados (API, DB, Data, UI)
├── static/graficos/         # Gráficos gerados pelo Matplotlib
├── templates/               # Páginas HTML (Jinja2) com seletores de teste
├── app.py                   # Rotas e regras de negócio da aplicação Flask
├── db.py                    # Camada de conexão com PostgreSQL
├── relatorio.py             # Script de análise e geração gráfica com Pandas
├── relatorio_vendas.csv     # Conjunto de dados base (massa de teste)
├── schema.sql               # Definição segura da tabela relatorio_vendas
├── pytest.ini               # Configuração e marcadores do Pytest
├── requirements.txt         # Dependências de produção
└── requirements-dev.txt     # Dependências de teste e QA
```

---

## 👤 Autor

**Pedro Luís dos Santos Souza**  
Projeto voltado para portfólio prático em **Desenvolvimento Web & QA Automation**.
