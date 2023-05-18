FROM postgres:14-alpine3.17

COPY ./init/ /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql.conf

# Expose postgres db port
EXPOSE 5432/tcp
