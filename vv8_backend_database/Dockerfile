FROM postgres:14-alpine

COPY ./init/ /docker-entrypoint-initdb.d/
COPY postgresql.conf /var/lib/postgresql/data/postgresql.conf

# Expose postgres db port
EXPOSE 5432/tcp
