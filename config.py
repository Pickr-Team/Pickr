import os

DB_USER = "root"
DB_PASSWORD = "Aw2685627193!"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "pickr"

class TestConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test"

class DevConfig:
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class ProdConfig:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://flask:2024flask@localhost/studentprojectmanager"
    APPLICATION_ROOT = '/studentprojectmanager'

class MemoryConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"