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
import random
import datetime

CODE_START = 100
CODE_END = 999

class Survey(models.Model):

    name = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Surveys"
        ordering = ['-start']

class Question(models.Model):
    """This class represents a question. It can have 2 or more options."""
    created_on = models.DateTimeField(auto_now_add=True)

    title = models.SlugField(max_length = 200)
    slug = models.SlugField(unique = True, max_length = 200)
    text = models.TextField()

    start = models.DateTimeField(default=datetime.datetime.now, blank=False)
    end = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(hours=1))

    allow_multiple = models.BooleanField(default = False)

    def save(self):
        title = self.title.replace('?', '')
        title = title.replace('.', '')
        slug = '-'.join(title.split())
        count = Question.objects.filter(slug__icontains = slug).count()
        print count
        if count:
            slug = slug + str(count+1)
        self.slug = slug
        super(Question, self).save()

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('survey:survey_question', [self.slug])

    @models.permalink
    def get_results_url(self):
        return ('survey:survey_results', [self.slug])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['-created_on']

class Choice(models.Model):
    """This represents an answer to the Question, and has a foreignkey to it"""
    question = models.ForeignKey(Question, related_name='Choices')
    text = models.TextField()

    code = models.IntegerField(default = random.randint(CODE_START, CODE_END), unique = True, blank=False)

    total_votes = models.IntegerField(default = 0)

    def __str__(self):
        return '%s - %s' % (self.question.title, self.text)