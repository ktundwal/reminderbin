from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

message = """
Hello, Los Angeles django users! I hope you are having a good time so far at
the meetup! Goodbye.
"""

urlpatterns = patterns('',
    url(r'^$', 'django_twilio.views.say', {'text': message}),
    url(r'^$', 'django_twilio.views.conference', {
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
)
