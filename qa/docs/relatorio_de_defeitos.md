# Registro de defeitos — Dashboard de Vendas

Modelo:

| Campo | Conteúdo |
|-------|----------|
| ID | DEF-XX |
| Título | |
| Descrição | |
| Passos para reproduzir | |
| Resultado esperado | |
| Resultado obtido | |
| Severidade | baixa / média / alta / crítica |
| Prioridade | baixa / média / alta |
| Evidências | caminho do screenshot/log |
| Status | aberto / confirmado / corrigido / não é defeito |

## Defeitos encontrados

### DEF-01 — Títulos `h2` da home com cor branca

- **Descrição:** Em `templates/index.html`, a regra `h1, h2 { color: #ffffff; }` também se aplica aos títulos dentro de `main` (fundo branco), tornando "Lista de Vendas" e os títulos dos gráficos invisíveis ao olho humano.
- **Passos:** Abrir `/` no navegador; observar "Lista de Vendas" e os títulos dos gráficos.
- **Resultado esperado:** Títulos legíveis sobre o fundo branco do `<main>`.
- **Resultado obtido:** Confirmado visualmente — texto `#ffffff` sobre fundo `#ffffff`. Os elementos existem no DOM (Playwright passa), mas são invisíveis para o usuário.
- **Severidade:** média (não quebra funcionalidade, mas impacta UX)
- **Prioridade:** média
- **Evidências:** inspeção de `templates/index.html`, linhas 29–31
- **Status:** aberto (auditoria estática confirmada; correção de CSS pendente de aprovação do autor)

---

### DEF-02 — Rota `/export` lança `TypeError` ao tentar exportar CSV  ✅ CORRIGIDO

- **Descrição:** `app.py`, rota `export_csv()`: `csv.writer(output)` recebia um objeto `flask.Response` em vez de um objeto com método `.write()`. O módulo `csv` do Python exige um file-like object (duck typing com `.write()`).
- **Passos para reproduzir:**
  1. Iniciar a aplicação com PostgreSQL configurado: `python app.py`
  2. Acessar `http://127.0.0.1:5000/export`
  3. Observar traceback `TypeError: argument 1 must have a "write" method`
- **Resultado esperado:** Download de arquivo `vendas.csv` com as vendas listadas.
- **Resultado obtido (antes da correção):** `Internal Server Error 500` — `TypeError: argument 1 must have a "write" method`
- **Severidade:** alta (funcionalidade principal completamente quebrada)
- **Prioridade:** alta
- **Evidências:** saída de `pytest` — `FAILED qa/tests/test_reports.py::test_export_csv_retorna_200_e_attachment` e `test_export_csv_contem_cabecalho_e_registros`
- **Correção aplicada:** introduzido `io.StringIO` como buffer intermediário; `csv.writer(si)` escreve para o buffer e `make_response(si.getvalue())` constrói a resposta HTTP. Arquivo alterado: `app.py` (adicionado `import io`; função `export_csv` refatorada).
- **Status:** ✅ corrigido — testes CT-08 e CT-09 passam após a correção (24/24 em verde)

---

### Observações que não são defeitos

- A aplicação não possui filtros. Casos de filtro estão fora de escopo.
- Credenciais não devem ir para o Git; a senha ficou restrita ao `.env` local.
- Testes de banco são pulados quando o PostgreSQL não está acessível, por desenho.
- O arquivo `fakes.py` contém as mesmas classes de `conftest.py`. A redundância é intencional: `fakes.py` permite importação explícita (usado em `test_ui.py`), enquanto `conftest.py` é injetado automaticamente pelo pytest (não deve ser importado diretamente por módulos de teste).
