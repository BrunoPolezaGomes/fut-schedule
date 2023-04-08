from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import config

app = Flask(__name__)

# Configurando o MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'garra'
app.config['MYSQL_PASSWORD'] = 'garra'
app.config['MYSQL_DB'] = 'garra_vermelha'
mysql = MySQL(app)

# Configurando a chave secreta
app.secret_key = 'garra_vermelha'

# Página de login


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cur.fetchone()
        cur.close()
        if usuario is None:
            return render_template('login.html', mensagem='E-mail não cadastrado')
        elif not check_password_hash(usuario[3], senha):
            return render_template('login.html', mensagem='Senha incorreta')
        else:
            session['id'] = usuario[0]
            session['nome'] = usuario[1]
            return redirect(url_for('home'))
    else:
        return render_template('login.html')

# Página de criação de conta

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cur.fetchone()
        if usuario is not None:
            return render_template('criar_conta.html', mensagem='E-mail já cadastrado')
        else:
            cur.execute(
                'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, senha))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
    else:
        return render_template('criar_conta.html')

# Tela inicial


@app.route('/home')
def home():
    if 'id' in session:
        return render_template('index.html', nome=session['nome'])
    else:
        return redirect(url_for('login'))

# Logout


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('nome', None)
    return redirect(url_for('login'))
