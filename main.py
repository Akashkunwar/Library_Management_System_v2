from app import app

if __name__ == '__main__':
    app.run(debug=True)

# python3 main.py
# celery -A app.celery_config.celery worker --loglevel=info
# celery -A app.celery_config.celery beat --loglevel=info