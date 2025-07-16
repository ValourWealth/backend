# web: gunicorn VWBE.wsgi --log-file - 
# #or works good with external database
# web: python manage.py migrate && gunicorn VWBE.wsgi
#web: python manage.py migrate && gunicorn VWBE.wsgi:application --log-file -
web: python manage.py migrate && daphne -b 0.0.0.0 -p $PORT VWBE.asgi:application




