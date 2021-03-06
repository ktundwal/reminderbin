from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from reminderbin.settings.common import *
from django.utils.timezone import utc
import datetime

from models import *
import forms
#from googlechart import PieChart2D
from pygooglechart import PieChart2D

from django_twilio.decorators import twilio_view
from reminderbin.apps.core.utils import logger, log_exception
from .sms import *

def index(request):
    return render('survey/index.html', {}, request)

def active_surveys(request):
    # find all questions that are active
    active_questions = Question.objects.filter(start__lt=datetime.datetime.utcnow().replace(tzinfo=utc),
        end__gt=datetime.datetime.utcnow().replace(tzinfo=utc))
    active_questions_with_choices = [{'question':active_question,
                                      'choices':Choice.objects.filter(question = active_question),
                                      'chart': get_chart_url(active_question.slug)} for active_question in active_questions]
    payload = {'active_questions_with_choices':active_questions_with_choices,
               'sms_to':TWILIO_CALLER_ID,
               'feedback':Feedback.objects.all()[:5]}

    return render('survey/active.html', payload, request)


def get_chart_url(slug):
    try:
        question = Question.objects.get(slug = slug)
    except ObjectDoesNotExist, e:
        raise Http404

    try:
        total_votes = 0
        choice_name = []
        choice_val = []
        for choice in question.Choices.all():
            total_votes += choice.total_votes
            choice_name.append(choice.text)
            choice_val.append(choice.total_votes)
        chart = PieChart2D(400, 200)
        chart.add_data(choice_val)
        choice_name = [choice_obj.encode('utf8') for choice_obj in choice_name]
        chart.set_pie_labels(choice_name)
        url = chart.get_url()
        return url
    except Exception, e:
        log_exception('Error generating chart url')
        return None

def question(request, slug):
    try:
        question = Question.objects.get(slug = slug)
    except ObjectDoesNotExist, e:
        raise Http404
    if request.method == 'POST':
        try:
            last_choice_id = request.session[question.id]
            last_choice = Choice.objects.get(id = last_choice_id)
            last_choice.total_votes -= 1
            last_choice.save()
        except KeyError, e:
            pass
        choice_id = int(request.POST['choices'])
        choice = Choice.objects.get(id = choice_id)
        choice.total_votes += 1
        choice.save()
        request.session[question.id] = choice.id
        return HttpResponseRedirect(question.get_results_url())
    if request.method == 'GET':
        try:
            last_choice_id = request.session[question.id]
            last_choice = Choice.objects.get(id = last_choice_id)
        except KeyError, e:
            last_choice = 0
        choices = Choice.objects.filter(question = question)
        payload = {'question':question, 'choices':choices, 'last_choice':last_choice, 'sms_to':TWILIO_CALLER_ID}

        return render('survey/question.html', payload, request)

def results(request, slug):
    try:
        question = Question.objects.get(slug = slug)
    except ObjectDoesNotExist, e:
        raise Http404
    total_votes = 0
    choice_name = []
    choice_val = []
    for choice in question.Choices.all():
        total_votes += choice.total_votes
        choice_name.append(choice.text)
        choice_val.append(choice.total_votes)
    chart = PieChart2D(400, 200)
    chart.add_data(choice_val)
    choice_name = [choice_obj.encode('utf8') for choice_obj in choice_name]
    chart.set_pie_labels(choice_name)
    chart_url = chart.get_url()
    payload = {'question':question, 'total_votes':total_votes, 'chart_url':chart_url}
    return render('survey/results.html', payload, request)

def create(request):
    if request.method == 'POST':
        form = forms.CreateSurvey(request, request.POST)
        if form.is_valid():
            question = form.save()
            try:
                questions = request.session['questions']
            except KeyError, e:
                questions = []
            questions.append(question.id)
            request.session['questions'] = questions
            return HttpResponseRedirect(question.get_absolute_url())
    elif request.method == 'GET':
        form = forms.CreateSurvey(request)
    payload = {'form':form}
    return render('survey/create.html', payload, request)

def help(request):
    payload = {}
    return render('survey/help.html', payload, request)

#Helper methods.
def render(template_name, payload, request):
    recent_polls = Question.objects.all()[:8]
    try:
        questions = request.session['questions']
    except KeyError, e:
        questions = []
    your_polls = Question.objects.filter(id__in = questions)
    payload.update({'recent_polls':recent_polls, 'your_polls':your_polls})
    return render_to_response(template_name, payload, RequestContext(request))

#@twilio_view
def twilio_sms_handler(request, **kwargs):
    """
    Processes incoming SMS messages
    run this first localtunnel -k /Users/browsepad/.ssh/id_rsa.pub 8000
    """
    if request.method == 'POST':
        try:
            params = [(key, request.POST[key]) for key in request.POST.keys()]
            path = request.path
            cookies = [(key, request.COOKIES[key]) for key in request.COOKIES.keys()]
            meta = [(key, request.META[key]) for key in request.META.keys()]
            session = [(key, request.session[key]) for key in request.session.keys()]
            logger.debug('Request path = %s' % request.path)
            logger.debug('Request params = %s' % params)
            logger.debug('Request cookies = %s' % cookies)
            logger.debug('Request meta = %s' % meta)
            logger.debug('Request session obj = %s' % session)
        except:
            log_exception('Unable to log request details')

        cell = request.POST['From']
        body = request.POST['Body']

        response = sms_reply(process_sms(body, cell))
        #return response
        return HttpResponse(response, mimetype='application/xml')
    else:
        logger.debug('GET request received on twilio_sms_handler. Raising exception.')
        raise Exception('Only POST requests accepted at this endpoint')

@twilio_view
def twilio_sms_handler_exception(request, **kwargs):
    """
    Processes SMS Fallback
    Retrieve and execute the TwiML at this URL when the SMS Request URL above can't be reached or there is a runtime exception.
    """
    if request.method == 'POST':
        params = request.POST
        cell = params['From']
        body = params['Body']

        logger.error('ERROR: Unable to process cell = %s, body = %s' % (cell, body))
        return sms_reply(request, cell, 'An application error occurred. Please try again later. Sorry! -TXT4HLTH')
