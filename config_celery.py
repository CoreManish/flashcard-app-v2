from celery import Celery
#You must have redis database installed
 # sudo apt install redis-server
BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
mycelery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)