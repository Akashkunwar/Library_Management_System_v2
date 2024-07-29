from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'B00KL1BRARYS4S7EM'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../library.db"
db = SQLAlchemy(app)

from app import routes
import os
from .celery_config import celery

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    )

    celery.conf.update(app.config)

    return app

app = create_app()
