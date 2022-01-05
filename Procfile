release: python manage.py migrate

web: gunicorn config.wsgi --log-file - --log-level debug

