import os
import django
import reminderbin

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(reminderbin.__file__))

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')  # dev, prod, test, etc
exec('from %s import *' % ENVIRONMENT)