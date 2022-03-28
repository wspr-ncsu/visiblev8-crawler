FROM postgres:14-alpine

ENV POSTGRES_PASSWORD vv8
ENV POSTGRES_USER vv8
ENV POSTGRES_DB vv8_logs
ENV PGDATA /var/lib/postgresql/data

COPY ./vv8_logs_init.sql /docker-entrypoint-initdb.d/vv8_logs_init.sql

# Expose postgres db port
EXPOSE 5432/tcp
