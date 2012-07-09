# Load defaults in order to then add/override with production-only settings
import os
from reminderbin.settings import *
from common import *

DEBUG = True

#import dj_database_url
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

if ENVIRONMENT == 'staging':
    from postgresify import postgresify
    DATABASES = postgresify()

    # ... etc.