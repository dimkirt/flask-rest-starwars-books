import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///../../wookie.sqlite.test'
    JWT_SECRET = os.environ.get('JWT_SECRET', 'default-super-secret')


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('DATABASE_URI',
                                  'sqlite:///../../wookie.sqlite.prod')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
