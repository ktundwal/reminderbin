__author__ = 'ktundwal'

from .models import *
from django.contrib import admin

admin.site.register(Patient)
admin.site.register(MedicalProfessional)
admin.site.register(Appointment)
admin.site.register(Reminder)