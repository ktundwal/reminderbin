from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext
from django.shortcuts import render_to_response

from reminderbin.apps.reminders.forms import PatientForm

register = Library()

@register.simple_tag()
def new_patient():
    return render_to_string('reminders/templatetags/new_patient.html', {'form': PatientForm()})
    #context = {'form': ReminderForm()}
    #return render_to_response("reminders/templatetags/new_reminder.html",
    #    context, context_instance=RequestContext(request))