from os import environ

class Config(object):
    """Base configuration"""
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"

    # Configurar la extensión Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("MAIL_USER")
    MAIL_PASSWORD = environ.get("MAIL_PASS")
    MAIL_DEFAULT_SENDER = environ.get("MAIL_USER")

    #Configurar todo lo necesario para el uso de JWT
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY") #DECIRLES QUIE ACTUALICEN EL ENV
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie" #esto no se si lo necesito
    #x-csrf-token????

    
class ProductionConfig(Config):
    """Production configuration"""
    
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_NOTIFICATIONS = True
    SQLALCHEMY_DATABASE_URI= f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

    JWT_COOKIE_SECURE = True #EXPLICACION GRABADA PARA QUE SOLO SE MANDE POR HTTP Y SE INACCESIBLE SI SE QUIERE USAR JS??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

class DevelopmentConfig(Config):
    """Development configuration"""
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    DB_NAME = "grupo18"
    SQLALCHEMY_TRACK_NOTIFICATIONS = True
    SQLALCHEMY_DATABASE_URI= f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {"production": ProductionConfig,"development": DevelopmentConfig,"testing": TestingConfig}
#This is a dictionary used to properly return the configuration selected when the app was created