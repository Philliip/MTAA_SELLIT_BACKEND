web: daphne my_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=sellit_api.settings.base -v2
