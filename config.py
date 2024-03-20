class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:20020316@127.0.0.1:3306/testDB"

class DevConfig:
    Testing = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:20020316@127.0.0.1:3306/demo"

class ProdConfig:
    Testing = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:20020316@127.0.0.1:3306/demo"