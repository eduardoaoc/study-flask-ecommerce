from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_msearch import Search

basedir= os.path.abspath(os.path.dirname(__file__))

app= Flask(__name__)

app.config['SECRET_KEY']='dsadsadsa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['UPLOADED_PHOTOS_DEST']= os.path.join(basedir,'static/images')

photos= UploadSet('photos',IMAGES)
configure_uploads(app, photos)

db= SQLAlchemy(app)
#criptografia de senhas
bcrypt= Bcrypt(app)
#pesquisa/busca
search= Search()
search.init_app(app)

from shop.admin import routes 
from shop.products import routes
from shop.carts import carts
