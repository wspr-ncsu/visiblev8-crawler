FROM python:3

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./vv8web ./vv8web

EXPOSE 80/tcp

CMD uvicorn vv8web.server:app --host 0.0.0.0 --port 80
