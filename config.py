# Config file


class Config(object):
    HOST_URL = "0.0.0.0"
    KONG_HOST_URL = 'localhost'
    HOST_PORT = 9010
    KONG_HOST_PORT = 8000
    KONG_SERVICE_ENDPOINT = '/inventoryservice'
    SERVICE_ENDPOINT = '/inventory/'
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
