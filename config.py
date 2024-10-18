import os

class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pickr_demo"


class DevConfig:
    Testing = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pickr_demo"


class ProdConfig:
    Testing = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"
    APPLICATION_ROOT = '/studentprojectmanager'