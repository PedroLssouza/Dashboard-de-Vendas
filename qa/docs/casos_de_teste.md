# Casos de teste — Dashboard de Vendas

Última execução: **2026-10-12** · Python 3.15.0 · pytest 9.1.1 · **24 passed / 0 failed / 0 skipped**

| ID | Título | Pré-condições | Passos | Dados | Resultado esperado | Resultado obtido | Status |
|----|--------|---------------|--------|-------|--------------------|------------------|--------|
| CT-01 | Home responde 200 | App Flask carregável | GET `/` | — | HTTP 200 | HTTP 200 ✅ | **PASSOU** |
| CT-02 | Home exibe título e tabela | GET `/` com dados fake | Abrir home | Alice Johnson / Wireless Mouse | HTML contém título, tabela e venda | HTML correto, dados visíveis ✅ | **PASSOU** |
| CT-03 | Home referencia gráficos | GET `/` | Inspecionar HTML | PNGs em `static/graficos` | `total_vendas_por_produto.png` e `..._cliente.png` no HTML | Referências e `data-testid` presentes ✅ | **PASSOU** |
| CT-04 | Formulário de cadastro abre | GET `/add` | Abrir `/add` | — | HTTP 200 e campos client, product, value, date | HTTP 200, campos presentes ✅ | **PASSOU** |
| CT-05 | Cadastro válido redireciona | POST `/add` com dados completos | Enviar formulário | QA Tester, USB Hub, 16.00, 2025-06-09 | HTTP 302 para `/` e registro na store isolada | 302 para `/`, venda inserida na store fake ✅ | **PASSOU** |
| CT-06 | Valor não numérico | POST `/add` | Enviar `value=abc` | valor="abc" | Mensagem de valor inválido | "Erro: valor inválido" retornado ✅ | **PASSOU** |
| CT-07 | Campos obrigatórios vazios | POST `/add` | Enviar formulário vazio | strings vazias | Mensagem de campos obrigatórios | "Erro: todos os campos são obrigatórios" retornado ✅ | **PASSOU** |
| CT-08 | Export CSV HTTP | GET `/export` | Chamar endpoint | — | 200, `text/csv`, filename `vendas.csv` | 200, Content-type text/csv, attachment vendas.csv ✅ | **PASSOU** (após correção DEF-02) |
| CT-09 | Export CSV colunas | GET `/export` | Ler corpo CSV | cabeçalho ID, Cliente, Produto, Valor, Data | Cabeçalho e ao menos 1 linha de dados | Cabeçalho correto, Alice Johnson na linha 1 ✅ | **PASSOU** (após correção DEF-02) |
| CT-10 | CSV de origem carrega | Arquivo `relatorio_vendas.csv` | `pandas.read_csv` | arquivo na raiz | DataFrame não vazio | DataFrame com 50 linhas ✅ | **PASSOU** |
| CT-11 | Colunas obrigatórias do CSV | CSV carregado | Normalizar nomes | client_name, product_name, sale_value, sale_date | Colunas presentes | Todas as 4 colunas presentes ✅ | **PASSOU** |
| CT-12 | Valores de venda numéricos e >= 0 | CSV carregado | `to_numeric` | coluna sale_value | Sem nulos; valores >= 0 | 50/50 numéricos, todos >= 0 ✅ | **PASSOU** |
| CT-13 | Datas interpretáveis | CSV carregado | `to_datetime` | coluna sale_date | Sem datas inválidas | 50/50 datas válidas no formato YYYY-MM-DD ✅ | **PASSOU** |
| CT-14 | Somas por produto/cliente batem com total | CSV carregado | groupby sum | sale_value | Totais iguais com 2 casas | Soma geral == soma por produto == soma por cliente ✅ | **PASSOU** |
| CT-15 | Relatório gera arquivos | Diretório temporário | `generate_reports` | 2 vendas de exemplo | CSV e 2 PNGs criados | `saida.csv`, `total_vendas_por_produto.png`, `total_vendas_por_cliente.png` criados ✅ | **PASSOU** |
| CT-16 | Variáveis de ambiente documentadas | `.env.example` | Ler arquivo | PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE | Chaves presentes | Todas as 5 chaves presentes em `.env.example` ✅ | **PASSOU** |
| CT-17 | Conexão PostgreSQL | Banco local | `SELECT 1` | `.env` válido | Conexão ok, retorno `{'ok': 1}` | Conexão estabelecida, `row["ok"] == 1` ✅ | **PASSOU** |
| CT-18 | Esquema da tabela | Banco local | information_schema | tabela `relatorio_vendas` | Colunas e NOT NULL | 5 colunas com NOT NULL corretos ✅ | **PASSOU** |
| CT-19 | Integridade somente leitura | Banco local | COUNT e CHECK lógico | sale_value >= 0 | Sem inválidos, total >= 1 | 50 registros, 0 inválidos ✅ | **PASSOU** |
| CT-20 | UI abre dashboard | Playwright + servidor isolado | Abrir home | Alice Johnson | Título e tabela visíveis | "Dashboard de Vendas" visível, tabela com dados ✅ | **PASSOU** |
| CT-21 | UI mostra gráficos | Playwright | Inspecionar imgs | chart-product / chart-client | Atributo src presente | `src` presente em ambos os elementos `img` ✅ | **PASSOU** |
| CT-22 | UI navega para cadastro | Playwright | Clicar Adicionar Venda | — | Formulário visível | Formulário `/add` carregado após clique ✅ | **PASSOU** |
| CT-23 | UI dispara download CSV | Playwright | Clicar exportar | — | Download `.csv` | Arquivo `.csv` baixado via `expect_download` ✅ | **PASSOU** |
| CT-24 | Filtros na listagem | Home carregada | Procurar campos de filtro | — | Não aplicável: filtros não existem | N/A — confirmado na auditoria | **Fora de escopo** |
| CT-25 | Live Server VS Code | HTML estático | Go Live | — | Não substitui o Flask | Validado; README explica o comando correto | **Informativo** |

> Relatório HTML completo gerado em `qa/reports/report.html` a cada execução de `pytest`.
