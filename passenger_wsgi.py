

# sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source('wsgi', 'passenger_wsgi.py')
from django_catalog import wsgi

application = wsgi.application
