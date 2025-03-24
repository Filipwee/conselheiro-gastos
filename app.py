from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Dados e treinamento do modelo
dados = {
    'Valor': [120.50, 350.00, 45.75, 200.00, 80.00, 15.30, 90.00, 500.00, 60.00, 250.00,
              30.00, 180.00, 400.00, 75.00, 300.00, 50.00, 150.00, 220.00, 25.00, 600.00,
              95.00, 450.00, 35.00, 280.00, 70.00, 130.00, 320.00, 20.00, 550.00, 85.00,
              110.00, 380.00, 40.00, 230.00, 65.00, 140.00, 290.00, 15.00, 620.00, 90.00],
    'Categoria': ['Alimentação', 'Lazer', 'Transporte', 'Moradia', 'Lazer', 'Transporte', 
                  'Alimentação', 'Moradia', 'Educação', 'Lazer', 'Transporte', 'Alimentação', 
                  'Moradia', 'Educação', 'Lazer', 'Alimentação', 'Moradia', 'Lazer', 
                  'Transporte', 'Moradia', 'Alimentação', 'Lazer', 'Transporte', 'Moradia', 
                  'Educação', 'Alimentação', 'Lazer', 'Transporte', 'Moradia', 'Educação',
                  'Alimentação', 'Lazer', 'Transporte', 'Moradia', 'Educação', 'Alimentação', 
                  'Lazer', 'Transporte', 'Moradia', 'Educação'],
    'Conselho': ['Manter', 'Gastar menos', 'Manter', 'Manter', 'Manter', 'Manter', 
                 'Manter', 'Gastar menos', 'Manter', 'Gastar menos', 'Manter', 'Manter', 
                 'Gastar menos', 'Manter', 'Gastar menos', 'Manter', 'Manter', 
                 'Gastar menos', 'Manter', 'Gastar menos', 'Manter', 'Gastar menos', 
                 'Manter', 'Gastar menos', 'Manter', 'Manter', 'Gastar menos', 'Manter', 
                 'Gastar menos', 'Manter', 'Manter', 'Gastar menos', 'Manter', 'Gastar menos', 
                 'Manter', 'Manter', 'Gastar menos', 'Manter', 'Gastar menos', 'Manter']
}

for i in range(len(dados['Valor'])):
    valor = dados['Valor'][i]
    categoria = dados['Categoria'][i]
    if valor > 200 and categoria in ['Lazer', 'Moradia']:
        dados['Conselho'][i] = 'Gastar menos'
    elif valor <= 200 or categoria in ['Alimentação', 'Transporte', 'Educação']:
        dados['Conselho'][i] = 'Manter'

df = pd.DataFrame(dados)
df['Categoria'] = df['Categoria'].astype('category').cat.codes
X = df[['Valor', 'Categoria']]
y = df['Conselho']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = RandomForestClassifier(n_estimators=200, random_state=42)
modelo.fit(X_train, y_train)

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    conselho = ""
    erro = ""
    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            categoria_nome = request.form['categoria']
            categorias = {'Alimentação': 0, 'Lazer': 2, 'Transporte': 4, 'Moradia': 3, 'Educação': 1}
            categoria = categorias[categoria_nome]
            novo_gasto = [[valor, categoria]]
            conselho = modelo.predict(novo_gasto)[0]
        except ValueError:
            erro = "Por favor, insira um valor numérico válido!"
        except KeyError:
            erro = "Selecione uma categoria válida!"
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Conselheiro de Gastos</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .erro { color: red; }
        </style>
    </head>
    <body>
        <h1>Conselheiro de Gastos</h1>
        <form method="post">
            Valor (R$): <input type="number" step="0.01" name="valor" required><br><br>
            Categoria: <select name="categoria">
                <option value="Alimentação">Alimentação</option>
                <option value="Lazer">Lazer</option>
                <option value="Transporte">Transporte</option>
                <option value="Moradia">Moradia</option>
                <option value="Educação">Educação</option>
            </select><br><br>
            <input type="submit" value="Obter Conselho">
        </form>
        {% if conselho %}
            <p>Conselho: {{ conselho }}</p>
        {% endif %}
        {% if erro %}
            <p class="erro">{{ erro }}</p>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html, conselho=conselho, erro=erro)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)