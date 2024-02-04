import os
class Config:
    SECRET_KEY = 'your_secret_key' # better to store secret key in os environment var, os.environ.get('SECRET_KEY', 'default_secret_key')
    
    # database location
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "database", "project.db")
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/database/project.db'
    
    # Configuration for Flask-Caching, store cache in memory
    CACHE_TYPE = "simple" # Use a simple, in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

    # Configuration for Flask-Caching, store cache in redis database
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_URL = "redis://localhost:6379"

