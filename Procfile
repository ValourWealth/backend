# web: gunicorn VWBE.wsgi --log-file - 
# #or works good with external database
# #or works good with external database
# web: python manage.py migrate && gunicorn VWBE.wsgi
web: python manage.py migrate && gunicorn VWBE.wsgi:application --log-file -

