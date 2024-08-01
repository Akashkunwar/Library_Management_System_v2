from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'B00KL1BRARYS4S7EM'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../library.db"
db = SQLAlchemy(app)

from app import routes