import csv
from io import StringIO
from pathlib import Path

from relatorio import generate_reports


def test_export_csv_retorna_200_e_attachment(client):
    response = client.get("/export")
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-type"]
    assert "vendas.csv" in response.headers["Content-Disposition"]


def test_export_csv_contem_cabecalho_e_registros(client):
    response = client.get("/export")
    content = response.get_data(as_text=True)
    reader = csv.reader(StringIO(content))
    rows = list(reader)
    assert rows[0] == ["ID", "Cliente", "Produto", "Valor", "Data"]
    assert len(rows) > 1
    assert "Alice Johnson" in rows[1] or "Alice Johnson" in [cell for row in rows for cell in row]


def test_generate_reports_cria_csv_e_graficos(tmp_path):
    rows = [
        {
            "id": 1,
            "client_name": "Alice Johnson",
            "product_name": "Wireless Mouse",
            "sale_value": 25.99,
            "sale_date": "2025-01-05",
        },
        {
            "id": 2,
            "client_name": "Bob Smith",
            "product_name": "Mechanical Keyboard",
            "sale_value": 89.50,
            "sale_date": "2025-01-12",
        },
    ]
    import pandas as pd

    df = pd.DataFrame(rows)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["sale_value"] = pd.to_numeric(df["sale_value"])

    csv_path = tmp_path / "saida.csv"
    graficos_dir = tmp_path / "graficos"
    result = generate_reports(df=df, csv_path=str(csv_path), graficos_dir=str(graficos_dir))

    assert Path(result["csv_path"]).exists()
    assert Path(result["grafico_produto"]).exists()
    assert Path(result["grafico_cliente"]).exists()
    exported = pd.read_csv(csv_path)
    assert len(exported) == 2
    assert round(result["total_por_produto"]["Wireless Mouse"], 2) == 25.99
