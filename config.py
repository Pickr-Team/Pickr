import os

class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"


class DevConfig:
    Testing = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"


class ProdConfig:
    Testing = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"