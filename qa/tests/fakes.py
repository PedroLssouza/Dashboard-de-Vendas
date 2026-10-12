class FakeCursor:
    def __init__(self, store):
        self.store = store
        self._result = []

    def execute(self, query, params=None):
        normalized = " ".join(query.lower().split())
        if normalized.startswith("select"):
            self._result = list(self.store["vendas"])
        elif normalized.startswith("insert"):
            client, product, value, sale_date = params
            next_id = max((row["id"] for row in self.store["vendas"]), default=0) + 1
            self.store["vendas"].append(
                {
                    "id": next_id,
                    "client_name": client,
                    "product_name": product,
                    "sale_value": value,
                    "sale_date": sale_date,
                }
            )
            self._result = []
        return self

    def fetchall(self):
        return self._result

    def close(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, store):
        self.store = store

    def cursor(self):
        return FakeCursor(self.store)

    def commit(self):
        return None

    def close(self):
        return None
