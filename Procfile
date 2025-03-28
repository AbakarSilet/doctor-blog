release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput
web: gunicorn lekamyablog.wsgi --bind 0.0.0.0:$PORT --workers 4