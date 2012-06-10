# Load defaults in order to then add/override with production-only settings
import os
from reminderbin.settings import *
from common import *

DEBUG = False

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

# ... etc.