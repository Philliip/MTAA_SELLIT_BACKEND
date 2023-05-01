web: daphne sellit_api.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker default --settings=sellit_api.settings.development -v2
