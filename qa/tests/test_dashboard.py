def test_pagina_principal_retorna_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_pagina_principal_contem_titulo_e_tabela(client):
    html = client.get("/").get_data(as_text=True)
    assert "Dashboard de Vendas" in html
    assert "Lista de Vendas" in html
    assert 'data-testid="sales-table"' in html
    assert "Alice Johnson" in html
    assert "Wireless Mouse" in html


def test_pagina_principal_referencia_graficos(client):
    html = client.get("/").get_data(as_text=True)
    assert "total_vendas_por_produto.png" in html
    assert "total_vendas_por_cliente.png" in html
    assert 'data-testid="chart-product"' in html
    assert 'data-testid="chart-client"' in html


def test_formulario_adicionar_venda_get(client):
    response = client.get("/add")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Adicionar Nova Venda" in html
    assert 'name="client"' in html
    assert 'name="product"' in html
    assert 'name="value"' in html
    assert 'name="date"' in html


def test_adicionar_venda_valida_redireciona(client, sales_store):
    response = client.post(
        "/add",
        data={
            "client": "QA Tester",
            "product": "USB Hub",
            "value": "16.00",
            "date": "2025-06-09",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    assert any(row["client_name"] == "QA Tester" for row in sales_store["vendas"])


def test_adicionar_venda_valor_invalido(client):
    response = client.post(
        "/add",
        data={
            "client": "QA Tester",
            "product": "USB Hub",
            "value": "abc",
            "date": "2025-06-09",
        },
    )
    assert response.status_code == 200
    assert "valor inválido" in response.get_data(as_text=True).lower()


def test_adicionar_venda_campos_obrigatorios(client):
    response = client.post(
        "/add",
        data={"client": "", "product": "", "value": "", "date": ""},
    )
    assert response.status_code == 200
    assert "obrigatórios" in response.get_data(as_text=True).lower()
