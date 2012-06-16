from django.conf.urls import patterns, include, url
from .api import PinResource, PatientResource

pin_resource = PinResource()
patient_resource = PatientResource()

urlpatterns = patterns('',
    url(r'', include(patient_resource.urls)),
)
