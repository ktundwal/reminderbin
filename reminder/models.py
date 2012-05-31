from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField

# Create your models here.

class Provider(models.Model):
    facility_name = models.CharField(max_length=200)
    admin = models.ForeignKey(User, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s at %s' % (self.admin.username, self.facility_name)

class Patient(models.Model):
    provider = models.ForeignKey(Provider)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name