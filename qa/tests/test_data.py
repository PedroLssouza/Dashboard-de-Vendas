from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).resolve().parents[2] / "relatorio_vendas.csv"
REQUIRED_COLUMNS = {"client_name", "product_name", "sale_value", "sale_date"}


def _load_csv():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip().str.lower()
    return df


def test_csv_existe_e_pode_ser_carregado():
    assert CSV_PATH.exists()
    df = _load_csv()
    assert not df.empty


def test_csv_possui_colunas_obrigatorias():
    df = _load_csv()
    assert REQUIRED_COLUMNS.issubset(set(df.columns))


def test_valores_de_venda_sao_numericos():
    df = _load_csv()
    converted = pd.to_numeric(df["sale_value"], errors="coerce")
    assert converted.notna().all()
    assert (converted >= 0).all()


def test_datas_podem_ser_interpretadas():
    df = _load_csv()
    converted = pd.to_datetime(df["sale_date"], errors="coerce")
    assert converted.notna().all()


def test_csv_nao_tem_clientes_ou_produtos_vazios():
    df = _load_csv()
    assert df["client_name"].astype(str).str.strip().ne("").all()
    assert df["product_name"].astype(str).str.strip().ne("").all()


def test_totais_agregados_correspondem_a_soma_bruta():
    df = _load_csv()
    df["sale_value"] = pd.to_numeric(df["sale_value"])
    soma_geral = df["sale_value"].sum()
    soma_por_produto = df.groupby("product_name")["sale_value"].sum().sum()
    soma_por_cliente = df.groupby("client_name")["sale_value"].sum().sum()
    assert round(soma_geral, 2) == round(soma_por_produto, 2)
    assert round(soma_geral, 2) == round(soma_por_cliente, 2)
