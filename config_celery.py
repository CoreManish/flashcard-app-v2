from celery import Celery

# to use redis database to store message queue, provide redis information
BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
mycelery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

#You must have redis database installed and running
 # sudo apt install redis
 # In ubuntu redis will run automatically why computer boot up. If not -
 # redis-server
