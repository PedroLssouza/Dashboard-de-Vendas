import os

import pandas as pd
import matplotlib.pyplot as plt

from db import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAFICOS_DIR = os.path.join(BASE_DIR, "static", "graficos")


def load_sales_dataframe(rows=None):
    if rows is None:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM relatorio_vendas")
                rows = cursor.fetchall()
        finally:
            conn.close()

    df = pd.DataFrame(rows)
    df.columns = df.columns.str.lower()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["sale_value"] = pd.to_numeric(df["sale_value"])
    return df


def generate_reports(df=None, csv_path=None, graficos_dir=None):
    if df is None:
        df = load_sales_dataframe()

    csv_path = csv_path or os.path.join(BASE_DIR, "relatorio_vendas.csv")
    graficos_dir = graficos_dir or GRAFICOS_DIR
    os.makedirs(graficos_dir, exist_ok=True)

    total_por_produto = df.groupby("product_name")["sale_value"].sum().sort_values()
    total_por_cliente = (
        df.groupby("client_name")["sale_value"].sum().sort_values(ascending=False)
    )

    df.to_csv(csv_path, index=False)

    plt.figure(figsize=(10, 6))
    total_por_produto.plot(kind="barh")
    plt.title("Total de Vendas por Produto")
    plt.tight_layout()
    produto_path = os.path.join(graficos_dir, "total_vendas_por_produto.png")
    plt.savefig(produto_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    total_por_cliente.plot(kind="bar")
    plt.title("Total de Vendas por Cliente")
    plt.tight_layout()
    cliente_path = os.path.join(graficos_dir, "total_vendas_por_cliente.png")
    plt.savefig(cliente_path)
    plt.close()

    return {
        "csv_path": csv_path,
        "grafico_produto": produto_path,
        "grafico_cliente": cliente_path,
        "total_por_produto": total_por_produto,
        "total_por_cliente": total_por_cliente,
    }


if __name__ == "__main__":
    resultado = generate_reports()
    print("Gráficos salvos em:", os.path.dirname(resultado["grafico_produto"]))
