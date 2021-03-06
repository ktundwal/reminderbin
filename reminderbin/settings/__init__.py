import os
import django
import reminderbin

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(reminderbin.__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# http://bitkickers.blogspot.com/2012/04/djangoheroku-quickstart-for-existing.html
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')  # dev, staging, prod
exec('from %s import *' % ENVIRONMENT)