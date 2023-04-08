class Config:


SECRET_KEY = 'sua_chave_secreta_aqui'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'garra'
MYSQL_PASSWORD = 'garra'
MYSQL_DB = 'garra'


class DevelopmentConfig(Config):


DEBUG = True
OPENAI_KEY = 'sua_chave_api_openai_aqui'
