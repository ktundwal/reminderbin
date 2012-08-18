__author__ = 'browsepad'

from .models import *
from django.contrib import admin

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Participant)
admin.site.register(Feedback)