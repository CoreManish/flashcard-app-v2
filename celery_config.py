from celery import Celery
BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
mycelery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)