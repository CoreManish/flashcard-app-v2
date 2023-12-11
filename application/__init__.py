import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_caching import Cache
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__,template_folder='../templates/',static_folder='../static/')

app.config['SECRET_KEY'] = "thisissecret"
# better to store secret key in os environment var
#app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(
  os.getcwd()) + '/database/project.sqlite'

# Configuration for Flask-Caching
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # Cache timeout in seconds

# Use a simple in-memory cache
app.config["CACHE_TYPE"] = "simple"  

# These are configuration to connect flask server to redis-server
# app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_HOST"] = "localhost"
# app.config["CACHE_REDIS_PORT"] = "6379"
# app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"

# To use redis database for caching the response, we should have redis installed and running
# Install
# sudo apt install redis
# Run (BY default redis-server run when computer boot up) - open terminal and type
# redis-server



# Initialize Flask-Caching
cache = Cache(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Api 
api = Api(app)

#jwt
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure, random value in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # Set the expiration time
jwt = JWTManager(app)


# from application.models import *
# with app.app_context():
#     db.create_all()

from application.apis import *

# Add Resources to API route
api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(DeckResource, '/deck')
api.add_resource(CardResource, '/card/<int:deck_id>')
api.add_resource(OneCardResource, "/onecard/<int:deck_id>")
api.add_resource(IEDeckResource, "/iedeck")
api.add_resource(IECardResource, "/iecard")