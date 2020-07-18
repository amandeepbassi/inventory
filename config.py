# Config file


class Config(object):
    HOST_URL = "0.0.0.0"
    HOST_PORT = 8001
    ACCESS_LOG = False
    DATABASE_HOST = 'localhost'
    DATBASE_NAME = 'db_inventory'
    DATABASE_USER = 'test'
    DATABASE_PASSWORD = 'test'
    SERVER_IMAGE_STORAGE = 'Images'
    TESTING = False


class ProductionConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    TESTING = True


class TestingConfig(Config):
    TESTING = True
