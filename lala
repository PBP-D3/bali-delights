release: python3 manage.py migrate --noinput && python3 manage.py initdatabase
web: gunicorn mental_health_tracker.wsgi