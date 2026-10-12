import threading

import pytest
from werkzeug.serving import make_server

from app import app as flask_app
from qa.tests.fakes import FakeConnection

pytestmark = pytest.mark.ui


@pytest.fixture
def live_server(monkeypatch, sales_store):
    monkeypatch.setattr("app.get_connection", lambda: FakeConnection(sales_store))
    flask_app.config.update(TESTING=True, DEBUG=False)
    server = make_server("127.0.0.1", 0, flask_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)


def test_abrir_dashboard_no_navegador(page, live_server):
    page.goto(live_server)
    title = page.get_by_test_id("dashboard-title")
    title.wait_for()
    assert title.inner_text() == "Dashboard de Vendas"
    assert page.get_by_test_id("sales-table").is_visible()
    assert "Alice Johnson" in page.get_by_test_id("sales-table").inner_text()


def test_graficos_visiveis(page, live_server):
    page.goto(live_server)
    produto = page.get_by_test_id("chart-product")
    cliente = page.get_by_test_id("chart-client")
    produto.wait_for()
    assert produto.get_attribute("src")
    assert cliente.get_attribute("src")


def test_navegar_para_formulario_de_venda(page, live_server):
    page.goto(live_server)
    page.get_by_test_id("add-sale-link").click()
    page.get_by_test_id("add-sale-title").wait_for()
    assert page.get_by_test_id("add-sale-form").is_visible()


def test_exportacao_csv_pelo_navegador(page, live_server):
    page.goto(live_server)
    with page.expect_download() as download_info:
        page.get_by_test_id("export-csv").click()
    download = download_info.value
    assert download.suggested_filename.endswith(".csv")
