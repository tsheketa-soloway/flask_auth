from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
app.config['SECRET_KEY'] = 'super-secret-key'  # this should be hidden and secure in a real application
db = SQLAlchemy(app)
ma = Marshmallow(app)

from services import *
from controllers import *

if __name__ == '__main__':
    app.run(debug=True)
