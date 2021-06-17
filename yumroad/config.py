import os
import yumroad

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'rand0102323') #resion need this bc 

    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    # MAIL_POST = os.getenv('MAIL_SERVER_POST', 2525)
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

    # SECRET_KEY = os.getenv('SECRET_KEY', '0e778f7378864bc590a26057872dbcc7')

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    TESTING = True

class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')


configuration = {
'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
