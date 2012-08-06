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

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('reminderbin.apps.survey.views',
    url(r'^$', 'index', name='survey_index'),
    url(r'^active/$', 'active_surveys', name='active_surveys_view'),
    url(r'^question/(?P<slug>[^\.^/]+)/$', 'question', name='survey_question'),
    url(r'^create/$', 'create', name='survey_create'),
    url(r'^help/$', 'help', name='survey_help'),
    url(r'^results/(?P<slug>[^\.^/]+)/$', 'results', name='survey_results'),
)
