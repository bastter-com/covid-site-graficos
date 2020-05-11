release: python manage.py migrate
web: gunicorn core.wsgi --log-file -
worker: celery worker --app=core -B 
beat: celery --app=core  
