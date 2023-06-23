import os

celery_broker = os.environ['VV8_CELERY_BROKER']
celery_broker_port = os.environ['VV8_CELERY_BROKER_PORT']
celery_id = os.environ['VV8_CELERY_ID']
celery_broker_uri = f'redis://{celery_broker}:{celery_broker_port}/0'
celery_backend_uri = f'redis://{celery_broker}:{celery_broker_port}/1'
