__author__ = 'ktundwal'

from reminder.models import Provider, Patient
from django.contrib import admin

admin.site.register(Provider)
admin.site.register(Patient)