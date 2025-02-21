import os
from datetime import timedelta

database_config = {
    "user": os.environ.get("USER_DB"),
    "password": os.environ.get("USER_PWS"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "data_base": os.environ.get("DB_NAME"),
}

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://%(user)s:%(password)s@%(host)s:%(port)s/%(data_base)s' % database_config

class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://%(user)s:%(password)s@%(host)s:%(port)s/%(data_base)s' % database_config

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://%(user)s:%(password)s@%(host)s:%(port)s/%(data_base)s' % database_config
