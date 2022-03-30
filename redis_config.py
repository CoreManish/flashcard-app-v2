from flask_caching import Cache
# These are configuration to connect flask server to redis-server
config = {"CACHE_TYPE": "RedisCache",
          "CACHE_REDIS_HOST": "localhost",
          "CACHE_REDIS_PORT": 6379,
          "CACHE_REDIS_URL": "redis://localhost:6379",
          "CACHE_DEFAULT_TIMEOUT": 1000}


# To use redis database for caching the response, we should have redis-server installed and running
# Install
# sudo apt install redis-server
# Run (BY default redis-server run when installed)
# redis-server
