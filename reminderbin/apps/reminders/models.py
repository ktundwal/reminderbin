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

from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)

    PENDING_CONSENT = 1
    GIVEN_CONSENT = 2
    DENIED_CONSENT = 3
    CONSENT_NOT_REQUIRED = 4

    CONSENT_CHOICES = (
        (PENDING_CONSENT, 'Pending'),
        (GIVEN_CONSENT, 'Given'),
        (DENIED_CONSENT, 'Denied'),
        (CONSENT_NOT_REQUIRED, "Not required"),
    )
    consent_status = models.IntegerField(choices=CONSENT_CHOICES, default=PENDING_CONSENT)

    ACTIVE_STATUS = 1
    INACTIVE_STATUS = 2

    STATUS_CHOICES = (
        (ACTIVE_STATUS, 'Active'),
        (INACTIVE_STATUS, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE_STATUS)

    name = models.CharField(max_length=200)
    cell = models.CharField(max_length=200)

    notes = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.cell, self.name)

class MedicalProfessional(models.Model):
    created_by = models.ForeignKey(User)

    ACTIVE_STATUS = 1
    INACTIVE_STATUS = 2

    STATUS_CHOICES = (
        (ACTIVE_STATUS, 'Active'),
        (INACTIVE_STATUS, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE_STATUS)

    DOCTOR_TYPE = 1
    NURSE_TYPE = 2
    TECHNICIAN_TYPE = 3

    TYPE_CHOICES = (
        (DOCTOR_TYPE, 'Doctor'),
        (NURSE_TYPE, 'Nurse'),
        (TECHNICIAN_TYPE, 'Lab Technician'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=DOCTOR_TYPE)

    name = models.CharField(max_length=200)
    cell = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s (%s), %s' % (self.name, self.cell, self.TYPE_CHOICES[self.type][1])

class Appointment(models.Model):

    patient = models.ForeignKey(Patient, related_name='appointments')

    when = models.DateTimeField(blank=False)   # UTC
    description = models.CharField(max_length=200, blank=True)  # ex: Blood work

    SCHEDULED_STATUS = 1
    CANCELLED_STATUS = 2
    POSTPONED_STATUS = 2

    STATUS_CHOICES = (
        (SCHEDULED_STATUS, 'Scheduled'),
        (CANCELLED_STATUS, 'Cancelled'),
        (POSTPONED_STATUS, 'Postponed'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=SCHEDULED_STATUS)

    def __unicode__(self):
        return '%s (%s) at %s' % (self.patient.cell, self.patient.name, self.when)

class Reminder(models.Model):

    appointment = models.ForeignKey(Appointment, related_name='reminders')
    time_delta = models.IntegerField(blank=False)

    PENDING_STATUS = 1
    DELIVERED_STATUS = 2
    FAILED_STATUS = 3

    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (DELIVERED_STATUS, 'Delivered'),
        (FAILED_STATUS, 'Unable to deliver'),
    )

    #reminders = models.IntegerField(choices=REMINDER_CHOICES)
    #reminders = MultiSelectField(max_length=250, blank=False, choices=REMINDER_CHOICES)

    when = models.DateTimeField(blank=False)   # UTC

    description = models.CharField(max_length=200, blank=True)  # ex: 2 hrs in advance | Now

    sms_status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING_STATUS)

    def __unicode__(self):
        return '%s %s' % (self.appointment.patient.cell, self.when)

    class Meta:
        ordering = ['-when']
