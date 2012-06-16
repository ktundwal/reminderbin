from tastypie.resources import ModelResource
from tastypie import fields

from reminderbin.apps.pins.models import Pin
from reminderbin.apps.reminders.models import Patient

class PinResource(ModelResource):  # pylint: disable-msg=R0904
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False

    def dehydrate_thumbnail(self, bundle):
        pin = Pin.objects.only('image').get(pk=bundle.data['id'])
        return pin.image.url_200x1000

class PatientResource(ModelResource):  # pylint: disable-msg=R0904

    class Meta:
        queryset = Patient.objects.all()
        resource_name = 'patient'
        include_resource_uri = False