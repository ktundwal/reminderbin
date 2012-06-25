from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext
from django.shortcuts import render_to_response

from reminderbin.apps.reminders.forms import *
from reminderbin.apps.reminders.models import *

register = Library()

@register.simple_tag()
def new_reminder():

    patient_form = PatientForm(instance=Patient(), prefix = "patient")
    appointment_form = AppointmentForm(instance=Appointment(), prefix = "appointment")
    reminder_form = ReminderForm(instance=Reminder(), prefix = "reminder")

    context = {'patient_form': patient_form,
               'appointment_form': appointment_form,
               'reminder_form': reminder_form,}
    return render_to_string("reminders/templatetags/new_reminder.html", context)