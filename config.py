class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:20020316@127.0.0.1:3306/testDB"

class DevConfig:
    Testing = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:20020316@127.0.0.1:3306/demo"