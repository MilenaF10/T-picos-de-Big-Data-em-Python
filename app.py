from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# Nome do arquivo CSV onde os dados serão armazenados
csv_file = 'stock_data.csv'

# Função para carregar os dados do estoque
def load_stock_data():
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Produto', 'Quantidade'])
        df.to_csv(csv_file, index=False)
    return df

# Função para salvar os dados do estoque
def save_stock_data(df):
    df.to_csv(csv_file, index=False)

@app.route('/')
def index():
    df = load_stock_data()
    return render_template('index.html', table=df.to_html(index=False))

@app.route('/update_stock', methods=['POST'])
def update_stock():
    product = request.form['product']
    quantity = int(request.form['quantity'])
    operation = request.form['operation']

    df = load_stock_data()

    if product in df['Produto'].values:
        if operation == 'entrada':
            df.loc[df['Produto'] == product, 'Quantidade'] += quantity
        elif operation == 'saida':
            df.loc[df['Produto'] == product, 'Quantidade'] -= quantity
    else:
        new_row = {'Produto': product, 'Quantidade': quantity if operation == 'entrada' else -quantity}
        df = df.append(new_row, ignore_index=True)

    save_stock_data(df)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
