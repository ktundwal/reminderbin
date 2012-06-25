#!/usr/bin/env python

"""forms.py: store additional information related to users
also see:
    http://birdhouse.org/blog/2009/06/27/django-profiles/
    https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
"""

__author__      = 'ktundwal'
__copyright__   = "Copyright 2012, Indraworks"
__credits__     = ["Kapil Tundwal"]
__license__     = "Indraworks Confidential. All Rights Reserved."
__version__     = "0.5.0"
__maintainer__  = "Kapil Tundwal"
__email__       = "ktundwal@gmail.com"
__status__      = "Development"

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from .models import *
from .fields import *
from django.contrib.localflavor.us.forms import USPhoneNumberField

class PatientForm(forms.ModelForm):

    cell = USPhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['cell', 'name',]

    class Meta:
        model = Patient
        exclude = ['created_by', 'created_on', 'consent_status', 'status']

class MedicalProfessionalForm(forms.ModelForm):

    cell = USPhoneNumberField()

    class Meta:
        model = MedicalProfessional
        exclude = ['created_by']

class AppointmentForm(forms.ModelForm):

    date = forms.DateField(required=True, label='Appointment date',)
    date.widget.attrs = {'class':'datePicker', 'readonly':'true',}
    time = forms.TimeField(required=True, label='Appointment time',
        input_formats=['%I:%M %p'],
        help_text="Changing date and time will recalculate reminder date and time")
    time.widget.attrs = {'class':'timePicker'}

    #status = forms.ChoiceField(choices=Appointment.STATUS_CHOICES,
    #    help_text="Selecting 'Cancel' will delete all remaining reminders.")

    class Meta:
        model = Appointment
        exclude = ['created_by', 'patient', 'appointment_with', 'description', 'status']

class ReminderForm(forms.ModelForm):

    REMINDER_CHOICES = (
        (0, u'Now'),
        (2, u'2 hrs in advance'),
        (12, u'Night before'),
        (24, u'24 hrs in advance'),
    )

    reminder = forms.MultipleChoiceField(choices=REMINDER_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        help_text="'Night before' SMS are sent @ 7pm local time")

    class Meta:
        model = Reminder
        exclude = ['created_by', 'appointment', 'date', 'time', 'description', 'sms_status']

class AllInOneReminderForm(forms.Form):

    REMINDER_CHOICES = (
        (0, u'Now'),
        (2, u'2 hrs in advance'),
        (12, u'Night before'),
        (24, u'24 hrs in advance'),
    )

    patient_cell = USPhoneNumberField(required=True, help_text="Required")
    patient_name = forms.CharField(required=False, help_text='Optional')

    consent_status = forms.ChoiceField(choices=Patient.CONSENT_CHOICES,
        help_text="Select Pending to request consent via SMS now.")

    appointment_date = forms.DateField(required=True,
        help_text="Changing date and time will recalculate reminder date and time")
    appointment_date.widget.attrs = {'class':'datePicker', 'readonly':'true',}
    appointment_time = forms.TimeField(required=True, input_formats=['%I:%M %p'])
    appointment_time.widget.attrs = {'class':'timePicker'}

    appointment_status = forms.ChoiceField(choices=Appointment.STATUS_CHOICES,
        help_text="Selecting 'Cancel' will delete all remaining reminders.")

    reminder = forms.MultipleChoiceField(choices=REMINDER_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        help_text="'Night before' SMS are sent @ 7pm local time")

class Meta:
        model = Reminder
        exclude = ['created_by']
