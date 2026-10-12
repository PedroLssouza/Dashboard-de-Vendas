# Plano de testes — Dashboard de Vendas

## Objetivo

Validar as funcionalidades atuais do dashboard Flask (listagem, cadastro, exportação CSV e geração de gráficos) e a qualidade dos dados de origem, com cobertura automatizada adequada a um portfólio de QA Júnior / QA Automation Júnior.

## Escopo

Incluído:

- Página inicial (`/`)
- Formulário de nova venda (`/add`)
- Exportação CSV (`/export`)
- Arquivo `relatorio_vendas.csv`
- Geração de gráficos em `relatorio.py`
- Esquema e integridade da tabela `relatorio_vendas` no PostgreSQL (quando o banco estiver disponível)
- Fluxos de interface no Chromium via Playwright

Fora de escopo nesta etapa:

- Autenticação e autorização (não existem na aplicação)
- Filtros de tela (não implementados)
- Deploy em produção
- Testes de carga ou segurança ofensiva

## Ambiente

- Sistema: Windows 10, PowerShell
- Python 3.15.0
- Flask em `http://127.0.0.1:5000`
- PostgreSQL local, banco `dashboard_vendas`, tabela `relatorio_vendas`
- Configuração de conexão via arquivo `.env` (não versionado)
- Cliente de testes do Flask para integração
- Playwright/Chromium para UI

## Pré-condições

- Dependências de `requirements.txt` e `requirements-dev.txt` instaladas
- Templates em `templates/` e gráficos em `static/graficos/`
- Para testes marcados com `db`: PostgreSQL acessível com as variáveis `PG*`
- Os testes de dashboard/UI usam dados isolados (conexão falsa) e não alteram o banco real

## Funcionalidades testadas

| ID | Funcionalidade | Tipo |
|----|----------------|------|
| F01 | Listar vendas | Integração / UI |
| F02 | Cadastrar venda | Integração / UI |
| F03 | Validar campos do cadastro | Integração |
| F04 | Exportar CSV | Integração / UI |
| F05 | Qualidade do CSV de origem | Dados |
| F06 | Gerar gráficos e CSV analítico | Relatório |
| F07 | Esquema e dados no PostgreSQL | Banco (condicional) |

## Riscos e limitações

- A aplicação depende do PostgreSQL em execução real; os testes de CI não tentam conectar a um banco local.
- Não há filtros na interface; casos de filtro não se aplicam.
- `relatorio.py` sobrescreve `relatorio_vendas.csv` quando executado na raiz do projeto.
- DEF-01 aberto: o CSS de `h2` na home usa cor branca sobre fundo branco — visualmente invisível ao usuário. Veja `relatorio_de_defeitos.md`.
- DEF-02 corrigido: a rota `/export` produzia `TypeError` devido ao uso incorreto de `csv.writer`. O bug foi corrigido em `app.py`.

## Resultado da execução — 2026-10-12

| Suíte | Total | Passou | Falhou | Ignorado |
|-------|-------|--------|--------|----------|
| `test_dashboard` | 7 | 7 | 0 | 0 |
| `test_data` | 6 | 6 | 0 | 0 |
| `test_db` | 4 | 4 | 0 | 0 |
| `test_reports` | 3 | 3 | 0 | 0 |
| `test_ui` (Playwright) | 4 | 4 | 0 | 0 |
| **Total** | **24** | **24** | **0** | **0** |
