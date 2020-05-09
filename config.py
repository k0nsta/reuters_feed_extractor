import os


class Config:
    TARGET = os.environ.get('TARGET_URL')
    PG_HOST = os.environ.get('PG_HOST', 'postgres')
    PG_PORT = os.environ.get('PG_PORT', '5432')
    PG_DBNAME = os.environ.get('PG_DBNAME', 'news')
    PG_USER = os.environ.get('PG_USER', 'postgres')
    MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'news')
    MONGO_PORT = os.environ.get('MONGO_PORT', '27017')