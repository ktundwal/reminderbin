from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext
from django.shortcuts import render_to_response

from reminderbin.apps.reminders.forms import MedicalProfessionalForm

register = Library()

@register.simple_tag()
def new_medicalprofessional():
    return render_to_string('reminders/templatetags/new_medicalprofessional.html', {'form': MedicalProfessionalForm()})
    #context = {'form': ReminderForm()}
    #return render_to_response("reminders/templatetags/new_reminder.html",
    #    context, context_instance=RequestContext(request))