from celery import Celery

app = Celery(
    'vv8web',
    broker='redis://localhost:6379/0'
    #backend='db+postgresql://vv8@vv8db:5432/celery'
)

if __name__ == '__main__':
    app.start()
