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
import string
import datetime

CODE_START = 100
CODE_END = 999

def valid_choice_codes():
    return list(string.ascii_lowercase)

def find_question(id_to_look):
    try:
        return Question.objects.get(pk=id_to_look)
    except:
        return None

def update_choice_before_save(choice):
    if not choice.simple_code:
        choices = choice.question.Choices.all()
        if len(choices) > 25:
            raise Exception('You have reached maximum number of choices allowed for a question')
        choice.simple_code = string.ascii_lowercase[len(choices)]

def update_question_before_save(self):
    title = self.title.replace('?', '')
    title = title.replace('.', '')
    slug = '-'.join(title.split())
    count = Question.objects.filter(slug__icontains=slug).count()
    print count
    if count:
        slug = slug + str(count + 1)
    self.slug = slug

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

    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True, max_length = 200)
    text = models.TextField()

    start = models.DateTimeField(default=datetime.datetime.now, blank=False)
    end = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(hours=1))

    allow_multiple = models.BooleanField(default = False)

    next = models.ForeignKey('self', related_name='previous', null=True, blank=True)

    def save(self, *args, **kwargs):
        update_question_before_save(self)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.pk, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('survey:survey_question', [self.slug])

    @models.permalink
    def get_results_url(self):
        return ('survey:survey_results', [self.slug])

    def __unicode__(self):
        return self.slug

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['-created_on']

class Choice(models.Model):
    """This represents an answer to the Question, and has a foreignkey to it"""

    question = models.ForeignKey(Question, related_name='Choices')
    text = models.TextField()

    simple_code = models.CharField(max_length = 1)

    total_votes = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        update_choice_before_save(self)
        super(Choice, self).save(*args, **kwargs)

    def __str__(self):
        return '%s%s(%s) %s(%s)' % (self.question.pk, self.simple_code, self.question.title, self.pk, self.text)

class Participant(models.Model):
    cell = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    enrolled_in_beta = models.BooleanField(default=False)

    responses = models.ManyToManyField(Question, related_name='participants')

    awaiting_response_on = models.ForeignKey(Question, related_name='awaiting_responses_from', null=True, blank=True)

    def __unicode__(self):
        return self.cell

    class Meta:
        ordering = ['-created_on']

class Feedback(models.Model):
    message = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())

    provided_by = models.ForeignKey(Participant, related_name='Feedbacks')

    def __unicode__(self):
        return '%s: %s' % (self.provided_by.cell, self.message)

    class Meta:
        verbose_name_plural = "Feedback"
        ordering = ['-created_on']