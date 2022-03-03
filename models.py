from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY']="thisissecret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite"

db = SQLAlchemy(app)


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True)
    password=db.Column(db.String(80))
    name=db.Column(db.String(50))
    email=db.Column(db.String(50), unique=True)

"""
#Run for the first time only
db.create_all()
db.session.add(User(username="manish", password="12345", name="Manish Yadav", email="manish@example.com"))
db.session.commit()
"""