import os

# Configurações gerais
DEBUG = True
SECRET_KEY = 'sua-chave-secreta-aqui'

# Configurações do MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'garra'
MYSQL_PASSWORD = 'garra'
MYSQL_DB = 'garra_vermelha'
MYSQL_CURSORCLASS = 'DictCursor'

# Configurações de upload de arquivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Configurações de e-mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'seu_email_aqui'
MAIL_PASSWORD = 'sua_senha_aqui'
MAIL_DEFAULT_SENDER = 'seu_email_aqui'
