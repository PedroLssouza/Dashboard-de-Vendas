from flask import Flask, render_template, request, redirect, make_response
import csv
import io

from db import get_connection

app = Flask(__name__)


@app.route('/')
def index():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM relatorio_vendas ORDER BY sale_date DESC")
            vendas = cursor.fetchall()
    finally:
        conn.close()

    return render_template("index.html", vendas=vendas)


@app.route('/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        client = request.form.get('client')
        product = request.form.get('product')
        value = request.form.get('value')
        date = request.form.get('date')

        if client and product and value and date:
            try:
                value = float(value)
                query = (
                    "INSERT INTO relatorio_vendas (client_name, product_name, sale_value, sale_date) "
                    "VALUES (%s, %s, %s, %s)"
                )
                conn = get_connection()
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(query, (client, product, value, date))
                    conn.commit()
                finally:
                    conn.close()
                return redirect('/')
            except ValueError:
                return "Erro: valor inválido"
        else:
            return "Erro: todos os campos são obrigatórios"

    return render_template("add_sale.html")


@app.route('/export')
def export_csv():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM relatorio_vendas ORDER BY sale_date DESC")
            vendas = cursor.fetchall()
    finally:
        conn.close()

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Cliente', 'Produto', 'Valor', 'Data'])

    for v in vendas:
        writer.writerow([
            v.get('id', ''),
            v.get('client_name', ''),
            v.get('product_name', ''),
            v.get('sale_value', ''),
            v.get('sale_date', ''),
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=vendas.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    app.run(debug=True)
