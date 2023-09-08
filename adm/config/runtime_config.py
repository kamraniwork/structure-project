import os


class Config:
    # project root directory
    BASE_DIR = os.path.join(os.pardir, os.path.dirname(__file__))

    SECRET_KEY = "8A(P6+)Ml-?(>vjirxH6q}IKU8QnQuFl|jzfIhgXg-/Xd5jI<:!i%UIWQMKig:"

    # Flask Configuration
    JSON_SORT_KEYS = False

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = True

    # RATE_LIMITER_OPTS = ['200 per day', '50 per hour']

    # Session API config
    # SESSION_PERMANENT = False
    # SESSION_TYPE = "filesystem"

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    # sqlalchemy database main
    MYSQL_HOST = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DATABASE = None
    MYSQL_PORT = None
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'


class TestingRuntimeConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAX_SELECT_DATETIME = 7776012


class ProductionRuntimeConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = True

    # sqlalchemy database main
    MYSQL_HOST = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DATABASE = None
    MYSQL_PORT = None
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'


class StructureRuntimeConfig(DevelopmentConfig):
    pass


settings = {
    'base': Config,
    'development': DevelopmentConfig,
    'testing': TestingRuntimeConfig,
    'production': ProductionRuntimeConfig,
    'default': StructureRuntimeConfig,
}
