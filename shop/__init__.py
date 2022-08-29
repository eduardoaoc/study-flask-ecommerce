from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt


app= Flask(__name__)

app.config['SECRET_KEY']='dsadsadsa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)
bcrypt= Bcrypt(app)

from shop.admin import routes 
from shop.products import routes