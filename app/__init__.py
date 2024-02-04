#---------Import from other files---------------------
from config import Config
#------------------------------------------------------

#---------Import library-------------------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_restful import Api
#--------------------------------------------------------

app = Flask(__name__) # Initialize Flask
app.config.from_object(Config)
db = SQLAlchemy(app) # Initialize SQLAlchemy
cache = Cache(app) # Initialize Flask-Caching
api = Api(app) # Initialize Api 

from app import routes