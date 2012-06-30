#!/usr/bin/env python

"""models.py"""

__author__      = 'ktundwal'
__copyright__   = "Copyright 2012, Indraworks"
__credits__     = ["Kapil Tundwal"]
__license__     = "Indraworks Confidential. All Rights Reserved."
__version__     = "0.5.0"
__maintainer__  = "Kapil Tundwal"
__email__       = "ktundwal@gmail.com"
__status__      = "Development"

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('reminderbin.apps.reminders.views',

    url(r'^patient-search/$', 'patient_search', name='patient-search'),
    #url(r'^patient-detail/$', 'patient_detail', name='patient-detail'),

    url(r'^recent-reminders/$', 'reminders_index', name='recent-reminders'),
    url(r'^new-reminder/$', 'new_reminder', name='new-reminder'),
    url(r'^edit/(?P<reminder_id>\d+)', 'new_reminder', name='edit-reminder'),

    url(r'^$', 'patients_index', name='recent-patients'),
    url(r'^new-patient/$', 'new_patient', name='new-patient'),
    url(r'^edit/(?P<patient_id>\d+)', 'new_patient', name='edit-patient'),

    url(r'^recent-medicalprofessionals$', 'medicalprofessionals_index', name='recent-medicalprofessionals'),
    url(r'^new-medicalprofessional/$', 'new_medicalprofessional', name='new-medicalprofessional'),
    url(r'^edit/(?P<medicalprofessional_id>\d+)', 'new_medicalprofessional', name='edit-medicalprofessional'),

    url(r'^recent-appointments$', 'appointments_index', name='recent-appointments'),
    url(r'^new-appointment/$', 'new_appointment', name='new-appointment'),
    url(r'^edit/(?P<appointment_id>\d+)', 'new_appointment', name='edit-appointment'),
)
