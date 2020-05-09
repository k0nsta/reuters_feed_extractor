FROM postgres:10.12-alpine

ENV POSTGRES_DB news
COPY sql/init.sql /docker-entrypoint-initdb.d/
