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

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404


from django.template import RequestContext

from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def patients_index(request):
    return render_to_response('reminders/patient_index.html',
            {'patient_list': Patient.objects.filter(created_by=request.user),
             'consent_choices' : dict(Patient.CONSENT_CHOICES),
             'status_choices' : dict(Patient.STATUS_CHOICES)},
        context_instance=RequestContext(request))

@login_required
def new_patient(request, patient_id = None):
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(data=request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False) # returns unsaved instance
            patient.created_by = request.user
            patient.save() # real save to DB.
            messages.success(request, 'New patient successfully added.')
            return HttpResponseRedirect(reverse('reminders:recent-patients'))
        else:
            messages.error(request, 'Patient form did not pass validation!')
    else:
        form = PatientForm(instance=patient)
    context = {'form': form,}
    #return TemplateResponse(request, 'reminders/new_patient.html', context)
    return render_to_response("reminders/new_patient.html",
        context, context_instance=RequestContext(request))

@login_required
def medicalprofessionals_index(request):
    return render_to_response('reminders/medicalprofessional_index.html',
            {'medicalprofessional_list': MedicalProfessional.objects.filter(created_by=request.user),
             'status_choices' : dict(MedicalProfessional.STATUS_CHOICES),
             'type_choices' : dict(MedicalProfessional.TYPE_CHOICES)},
        context_instance=RequestContext(request))

@login_required
def new_medicalprofessional(request, medicalprofessional_id = None):
    medicalprofessional = None
    if medicalprofessional_id:
        medicalprofessional = get_object_or_404(MedicalProfessional, id=medicalprofessional_id)

    if request.method == 'POST':
        form = MedicalProfessionalForm(data=request.POST, instance=medicalprofessional)
        if form.is_valid():
            medicalprofessional = form.save(commit=False) # returns unsaved instance
            medicalprofessional.created_by = request.user
            medicalprofessional.save() # real save to DB.
            messages.success(request, 'New medical professional successfully added.')
            return HttpResponseRedirect(reverse('reminders:recent-medicalprofessionals'))
        else:
            messages.error(request, 'Medical Professional form did not pass validation!')
    else:
        form = MedicalProfessionalForm(instance=medicalprofessional)
    context = {'form': form,}
    #return TemplateResponse(request, 'reminders/new_reminder.html', context)
    return render_to_response("reminders/new_medicalprofessional.html",
        context, context_instance=RequestContext(request))

@login_required
def appointments_index(request):
    return render_to_response('reminders/appointment_index.html',
            {'appointment_list': Appointment.objects.filter(created_by=request.user),
             'status_choices' : dict(Appointment.STATUS_CHOICES),},
        context_instance=RequestContext(request))

@login_required
def new_appointment(request, appointment_id = None):
    appointment = None
    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(data=request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False) # returns unsaved instance
            appointment.created_by = request.user
            appointment.save() # real save to DB.
            messages.success(request, 'New appointment successfully added.')
            return HttpResponseRedirect(reverse('reminders:recent-appointments'))
        else:
            messages.error(request, 'Appointment form did not pass validation!')
    else:
        form = AppointmentForm(instance=appointment)
    context = {'form': form,}
    #return TemplateResponse(request, 'reminders/new_reminder.html', context)
    return render_to_response("reminders/new_appointment.html",
        context, context_instance=RequestContext(request))

@login_required
def recent_reminders(request):
    #return TemplateResponse(request, 'reminders/recent_reminders.html', {'reminders': Reminder.objects.all()})
    return render_to_response("reminders/recent_reminders.html",
        {'reminders': Reminder.objects.all(),},
        RequestContext(request))

@login_required
def reminders_index(request):
    x = dict(REMINDER_CHOICES)
    return render_to_response('reminders/reminder_index.html',
            {'reminder_list': Reminder.objects.filter(created_by=request.user),
             'status_choices' : dict(Reminder.STATUS_CHOICES)},
            context_instance=RequestContext(request))

@login_required
def new_reminder(request, reminder_id = None):
    reminder = None
    if reminder_id:
        reminder = get_object_or_404(Reminder, id=reminder_id)

    if request.method == 'POST':
        form = ReminderForm(data=request.POST, instance=reminder)
        if form.is_valid():
            reminder = form.save(commit=False) # returns unsaved instance
            reminder.created_by = request.user
            reminder.save() # real save to DB.
            messages.success(request, 'New reminder successfully added.')
            return HttpResponseRedirect(reverse('reminders:recent-reminders'))
        else:
            messages.error(request, 'Reminder did not pass validation!')
    else:
        form = ReminderForm(instance=reminder)
    context = {'form': form,}
    #return TemplateResponse(request, 'reminders/new_reminder.html', context)
    return render_to_response("reminders/new_reminder.html",
        context, context_instance=RequestContext(request))
