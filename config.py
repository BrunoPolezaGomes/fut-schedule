class Config:
    pass

SECRET_KEY = "QetsdFgHjKlMnOpQrStUvWxYz"
MYSQL_HOST = 'localhost'
MYSQL_USER = 'garra'
MYSQL_PASSWORD = 'garra'
MYSQL_DB = 'garra'


class DevelopmentConfig(Config):
    pass

DEBUG = True
OPENAI_KEY = 'sua_chave_api_openai_aqui'
