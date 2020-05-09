import logging
import argparse

import csv
from datetime import datetime
from dbconnector import MongoConnector
from dbconnector import PGConnector
from datetime import datetime
from config import Config


log = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
                        description='Mongo csv exporter')
    parser.add_argument('date',
                        help="provide date by format: M/D/YYYY")
    parser.add_argument('db_type',
                        help="mongo or postgres")
    return parser.parse_args()


def extract_data_mongo(date):
    log.info("Start extrating data from mongo db")
    db = MongoConnector(Config.MONGO_HOST, Config.MONGO_PORT, Config.MONGO_DBNAME)
    result = db.get_by_date(date)
    with open('output/output_mongo.csv', 'w') as outfile:
        fields =  ('_id', 'url', 'title', 'description', 'content', 'datetime')
        write = csv.DictWriter(outfile, fieldnames=fields)
        write.writeheader()
        for record in result:
            write.writerow(record)
    

def extract_data_pg(date):
    log.info("Start extrating data from postgres db")
    db = PGConnector(Config.PG_DBNAME, Config.PG_USER, Config.PG_HOST, Config.PG_PORT)
    result = db.get_by_date(date)
    with open('output/output_postgres.csv', 'w') as outfile:
        fields =  ('id', 'url', 'title', 'description', 'content', 'datetime')
        write = csv.writer(outfile)
        write.writerow(fields)
        for record in result:
            write.writerow(record)
    

if __name__ == "__main__":
    param = get_parser()
    udate = datetime.strptime(param.date, '%m/%d/%Y')
    typedb = param.db_type

    if typedb == 'mongo':
        extract_data_mongo(udate)
        log.info('Data has been extracted')
    elif typedb == 'postgres':
        extract_data_pg(udate)
        log.info('Data has been extracted')
