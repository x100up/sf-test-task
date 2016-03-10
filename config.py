class Config(object):
    HOST = 'localhost'
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '5566889555'
    DATABASE_URI = 'sqlite://'
    STATIC_FILES_CACHE_TIMEOUT = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_PROVIDERS = ['simple', 'facebook', 'instagram']


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'postgresql://platform:platform@127.0.0.1/platform'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class MongoTestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'mongodb://localhost/auth'

