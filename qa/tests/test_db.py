import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.db

ENV_EXAMPLE = Path(__file__).resolve().parents[2] / ".env.example"


def _can_connect():
    try:
        from db import get_connection

        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False


skip_sem_postgres = pytest.mark.skipif(
    not _can_connect(),
    reason="PostgreSQL indisponível ou não configurado neste ambiente",
)


@skip_sem_postgres
def test_conexao_postgresql():
    from db import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            row = cursor.fetchone()
        assert row["ok"] == 1
    finally:
        conn.close()


@skip_sem_postgres
def test_esquema_tabela_relatorio_vendas():
    from db import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'relatorio_vendas'
                ORDER BY ordinal_position
                """
            )
            columns = {row["column_name"]: row for row in cursor.fetchall()}
        assert set(columns) >= {
            "id",
            "client_name",
            "product_name",
            "sale_value",
            "sale_date",
        }
        assert columns["client_name"]["is_nullable"] == "NO"
        assert columns["product_name"]["is_nullable"] == "NO"
        assert columns["sale_value"]["is_nullable"] == "NO"
        assert columns["sale_date"]["is_nullable"] == "NO"
    finally:
        conn.close()


@skip_sem_postgres
def test_quantidade_e_integridade_somente_leitura():
    from db import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM relatorio_vendas")
            total = cursor.fetchone()["total"]
            cursor.execute(
                """
                SELECT COUNT(*) AS invalidos
                FROM relatorio_vendas
                WHERE sale_value < 0
                   OR client_name IS NULL
                   OR product_name IS NULL
                   OR sale_date IS NULL
                """
            )
            invalidos = cursor.fetchone()["invalidos"]
        assert total >= 1
        assert invalidos == 0
    finally:
        conn.close()


def test_variaveis_de_ambiente_documentadas():
    content = ENV_EXAMPLE.read_text(encoding="utf-8")
    for key in ("PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"):
        assert key in content
    assert os.getenv("PGDATABASE", "dashboard_vendas")
