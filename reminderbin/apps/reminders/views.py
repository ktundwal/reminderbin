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

from datetime import datetime, timedelta

from django.utils import timezone
from django.template import RequestContext

from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import *
from .models import *

@login_required
def patient_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Patient.objects.filter(cell__icontains=query)
    return render_to_response('reminders/patient_search.html',
            { 'query': query,
              'results': results })

@login_required
def patients_index(request):

    patient_form = PatientForm(instance=Patient(), prefix = "patient")
    appointment_form = AppointmentForm(instance=Appointment(), prefix = "appointment")
    reminder_form = ReminderForm(instance=Reminder(), prefix = "reminder")

    return render_to_response('reminders/patient_index.html',
            {'patient_list': Patient.objects.filter(created_by=request.user),
             'consent_choices' : dict(Patient.CONSENT_CHOICES),
             'patient_status_choices' : dict(Patient.STATUS_CHOICES),
             'appointment_list': Appointment.objects.filter(created_by=request.user),
             'appointment_status_choices' : dict(Appointment.STATUS_CHOICES),
             'patient_form': patient_form,
             'appointment_form': appointment_form,
             'reminder_form': reminder_form,},
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
    return render_to_response('reminders/reminder_index.html',
            {'reminder_list': Reminder.objects.filter(created_by=request.user),
             'status_choices' : dict(Reminder.STATUS_CHOICES)},
            context_instance=RequestContext(request))


def create_or_get_patient(user, patient_obj_from_form):
    patient = None
    try:
        patient_from_db = Patient.objects.get(cell=patient_obj_from_form.cell)
        patient = patient_from_db
    except ObjectDoesNotExist:    # this is the first time. create patient
        patient_obj_from_form.created_by = user
        patient_obj_from_form.save() # real save to DB.
        patient = patient_obj_from_form
    except MultipleObjectsReturned: # we found more than 1,  return first one
        patients_from_db = Patient.objects.filter(cell=patient_obj_from_form.cell)
        if patients_from_db.count() > 0:
            patient = patients_from_db[0]

    return patient


@login_required
def new_reminder(request, reminder_id = None):
    reminder = None
    if reminder_id:
        reminder = get_object_or_404(Reminder, id=reminder_id)

    if request.method == 'POST': #if the form has been submitted
        patient_form = PatientForm(request.POST, prefix = "patient")
        appointment_form = AppointmentForm(request.POST,  prefix = "appointment")

        if patient_form.is_valid() and appointment_form.is_valid(): # All validation rules pass
            print "all validation passed"

            patient = create_or_get_patient(request.user, patient_form.save(commit=False))



            appointment_form.cleaned_data["patient"] = patient
            appointment = appointment_form.save(commit=False)
            appointment.patient = patient
            appointment.save() # real save to DB.

            # FIXME: create reminder objects based on reminder_form.cleaned_data["reminder"]
            # It returns list [u'0', u'2', u'12', u'24']

            current_tz = timezone.get_current_timezone_name()

            appointment_datetime = appointment_form.cleaned_data["when"]

            for hours_before in appointment_form.cleaned_data["reminders"]:
                if u'12' == hours_before:
                    # special case, this means 7pm yesterday
                    day_before_appointment = appointment_datetime - timedelta(1)
                    reminder_time = day_before_appointment.replace(hour=17, minute=0, second=0, microsecond=0)
                else:
                    reminder_time = appointment_datetime - timedelta(hours=int(hours_before))

                reminder = Reminder()
                reminder.appointment = appointment
                reminder.when = reminder_time
                reminder_choice_dict = dict(AppointmentForm.REMINDER_CHOICES)
                reminder.description = reminder_choice_dict[int(hours_before)]
                reminder.save() # real save to DB.

            messages.success(request, 'Saved.')
            return HttpResponseRedirect(reverse('reminders:new-reminder'))
        else:
            messages.error(request, 'Reminder did not pass validation!')
    else:
        patient_form = PatientForm(prefix = "patient")
        appointment_form = AppointmentForm(prefix = "appointment")
    context = {
        'patient_form': patient_form,
        'appointment_form': appointment_form,
        #'reminder_list': Reminder.objects.filter(created_by=request.user),
        'patient_list': Patient.objects.filter(created_by=request.user),
        }
    #return TemplateResponse(request, 'reminders/new_reminder.html', context)
    return render_to_response("reminders/new_reminder.html",
        context, context_instance=RequestContext(request))
