from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

message = """
Hello, Reminderbin users! This is just a dummy response from twilio library.
"""

urlpatterns = patterns('',
    url(r'', include('reminderbin.apps.core.urls', namespace='core')),
    url(r'^reminders/', include('reminderbin.apps.reminders.urls', namespace='reminders')),
    url(r'^pins/', include('reminderbin.apps.pins.urls', namespace='pins')),
    url(r'^api/', include('reminderbin.apps.api.urls', namespace='api')),

    url(r'^say/$', 'django_twilio.views.say', {'text': message}),
    url(r'^conf/$', 'django_twilio.views.conference', {
        'name': 'conf1',
        'wait_url': 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.rock',
        'wait_method': 'GET',
    }),
    # url(r'^sentry/', include('sentry.urls')),
    # Examples:
    # url(r'^$', 'reminderbin.views.home', name='home'),
    # url(r'^reminderbin/', include('reminderbin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),

    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
