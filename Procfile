web: gunicorn tag.wsgi --log-file -
worker: celery -A tag worker -B -l info 
