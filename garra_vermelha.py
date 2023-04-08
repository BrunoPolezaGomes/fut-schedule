from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import config

app = Flask(__name__)
app.secret_key = 'garra_vermelha'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'garra'
app.config['MYSQL_PASSWORD'] = 'garra'
app.config['MYSQL_DB'] = 'garra_vermelha'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM usuarios WHERE email = %s", (email,))
        if result > 0:
            data = cur.fetchone()
            senha_hash = data['senha']
            if sha256_crypt.verify(senha, senha_hash):
                session['logged_in'] = True
                session['email'] = email
                return redirect(url_for('index'))
            else:
                error = 'Senha incorreta.'
                return render_template('login.html', error=error)
        else:
            error = 'E-mail não cadastrado.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = sha256_crypt.encrypt(request.form['senha'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        return render_template('criar_conta.html')


if name == 'main':
    app.run(debug=True)
