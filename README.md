# Reuters News Feed Parser Example

## Description

This is a test app which allows fetching Reuters feed every 1 hour and store data into `PostgreSQL` and `MongoDB`.

## Installing and Usage

This app is fully automatic, you just need to clone this repository and run `docker-compose`, that is all.

```bash
git clone https://gist.github.com/k0nsta/reuters_feed_parser
cd reuters_feed_parser/
docker-compose -f compose.yml up -d
```

### Extract data from DB

The app allows extracting data from PostgreSQL or MongoDB for a specific date by invoking extractor script. Extracted data will store in a project folder `/output`

The script accepts two mandatory parameters - `date` and `database`.

The `date` param must be present in a format such as: `MM/DD/YYYY`.

The `databse` param must be type of data base: `postgres` or `mongo`.


```bash
docker-compose -f compose.yml run parser python output.py 05/09/2020 postgres
docker-compose -f compose.yml run parser python output.py 05/09/2020 mongo
```

## Configurations

The app configure via enviroment variables, which can set into `compose.yml` file.

Avaliable variables:

`TARGET_URL` - feed url

`PG_HOST` - postgres host

`PG_PORT` - postgres port

`PG_DBNAME` - postgres database name

`PG_USER` - posgtres username

`MONGO_HOST` - mongoDB host

`MONGO_DBNAME` - mongoDB database name

`MONGO_PORT` - mongoDB port


## Limitations

Due to time boundaries:

1. Postgres: Insert by one row, instead of batch insertion.

2. Single thread app, although we can insert into dbs concurrently at least. 
