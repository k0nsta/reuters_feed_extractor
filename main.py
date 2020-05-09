import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from parser import ReutersRSSParser
from dbconnector import PGConnector
from dbconnector import MongoConnector


logging.basicConfig(level=logging.INFO)


def fetch_news():
    parser = ReutersRSSParser(Config.TARGET)
    records = parser.parse()

    pg_db = PGConnector(Config.PG_DBNAME, Config.PG_USER, Config.PG_HOST, Config.PG_PORT) 
    mongo_db = MongoConnector(Config.MONGO_HOST, Config.MONGO_PORT, Config.MONGO_DBNAME)

    for record in records:
        pg_db.execute(record)
        pg_db.conn.commit()
        mongo_db.execute({'url': record.url}, record._asdict())
    pg_db.conn.close()


if __name__ == "__main__":
    fetch_news()
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_news, 'interval', hours=1)
    scheduler.start()
