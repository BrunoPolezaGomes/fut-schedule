# Importações necessárias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Configurações do aplicativo
app = Flask(__name__)
app.secret_key = 'seu_secreto_aqui'

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'sua_senha_mysql'
app.config['MYSQL_DB'] = 'garra_vermelha'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicialização do objeto MySQL
mysql = MySQL(app)

# Rota para a página principal


@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de cadastro de usuário


@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        posicao = request.form['posicao']
        camisa = request.form['camisa']
        chuteira = request.form['chuteira']
        destro_canhoto = request.form['destro_canhoto']
        foto = request.files['foto']

        # Validação do formulário
        if not nome:
            flash('Informe o nome', 'error')
        elif not email:
            flash('Informe o email', 'error')
        elif not senha:
            flash('Informe a senha', 'error')
        elif not confirmar_senha:
            flash('Confirme a senha', 'error')
        elif senha != confirmar_senha:
            flash('As senhas informadas não coincidem', 'error')
        elif not posicao:
            flash('Informe a posição que joga', 'error')
        elif not camisa:
            flash('Informe o número da camisa', 'error')
        elif not chuteira:
            flash('Informe o número da chuteira', 'error')
        elif not destro_canhoto:
            flash('Informe se é destro ou canhoto', 'error')
        elif not foto:
            flash('Informe a foto de perfil', 'error')
        else:
            # Salvar usuário no banco de dados
            try:
                # Salvar foto no diretório uploads
                foto_filename = secure_filename(foto.filename)
                foto.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], foto_filename))

                # Gerar hash da senha
                senha_hash = generate_password_hash(senha)

                # Inserir usuário no banco de dados
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO usuarios (nome, email, senha, posicao, camisa, chuteira, destro_canhoto, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (nome, email, senha_hash, posicao, camisa, chuteira, destro_canhoto, foto_filename))
                mysql.connection.commit()
                cur.close()

                flash('Usuário cadastrado com sucesso', 'success')
            except Exception as e:
                flash(f'Erro ao cadastrar usuário: {e}', 'error')

    return render_template('cadastro.html')

# Rota para a página de login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# definir @login_required para que o usuário tenha que estar logado para acessar a página

@app.route('/user/<username>')
def user(username):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
def follow(username):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
def edit_profile_admin(id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.about_me = form.about_me.data
        db.session.commit()
        flash('Alterações salvas com sucesso.')
        return redirect(url_for('user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@app.route('/explore')
def explore():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
