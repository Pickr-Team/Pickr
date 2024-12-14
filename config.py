import os


class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pickr_test"


class DevConfig:
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pickr"


class ProdConfig:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"
    APPLICATION_ROOT = '/studentprojectmanager'


class MemoryConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
