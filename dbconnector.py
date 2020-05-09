import os
import logging
import datetime as dt
from datetime import datetime

import psycopg2
from psycopg2 import OperationalError
from pymongo import MongoClient
from pymongo import errors

from config import Config


log = logging.getLogger(__name__)


class PGConnector:
    def __init__(self, db_name, db_user, db_host, db_port: str):
        try:
            connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                host=db_host,
                port=db_port,
            )
            self.conn = connection
            log.error("[PG]: Connection to PostgreSQL DB successful")
        except OperationalError as e:
            log.error("[PG]: The error %s' occurred", e, exc_info=1)

    def execute(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO reuters (url, title, description, content, datetime) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;', data)
            log.info("[PG]: Query executed successfully")
        except OperationalError as e:
            log.error("[PG]: The error %s' occurred", e)

    def get_by_date(self, date):
        cursor = self.conn.cursor()
        start = date.replace(hour=0, minute=0)
        end = start + dt.timedelta(days=1)
        query = f"SELECT * FROM reuters WHERE datetime between '{str(start)}' and '{str(end)}';"
        try:
            cursor.execute(query)
        except OperationalError as e:
            log.error("[PG]: The error %s' occurred", e)
        result = cursor.fetchall()
        self.conn.close()
        return result


class MongoConnector:

    def __init__(self,db_host, db_port, db_name: str):
        conn = MongoClient(db_host, int(db_port))
        self.db = conn[db_name]

    def execute(self, key, data: str):
        collection = self.db['reuters']
        try:
            res = collection.update_one(key, {'$set': data}, upsert=True)
            if res:
                log.info("[MONGO]: Query executed successfully")
        except errors.ServerSelectionTimeoutError as e:
                log.error("[MONGO]: The connection error %s' occurred", e)

    def get_by_date(self, date):
        start = date.replace(hour=0, minute=0)
        end = start + dt.timedelta(days=1)
        collection = self.db['reuters']
        res = collection.find({'datetime': {'$gte': start, '$lt': end, }})
        return list(res)
