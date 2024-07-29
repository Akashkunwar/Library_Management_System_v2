from app import app
from app.celery import celery

if __name__ == '__main__':
    app.run(debug=True)