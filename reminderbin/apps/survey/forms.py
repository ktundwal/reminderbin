from django import forms
from .models import *
from reminderbin.apps.reminders.fields import *

class CreateSurvey(forms.Form):
    question_title = forms.CharField(widget = forms.TextInput(
        attrs = {'class':'required'}),
        help_text = 'Title for your question. This is required.')
    question_text = forms.CharField(
        widget = forms.Textarea,
        help_text = 'Some description. This is required.')

    start = forms.SplitDateTimeField(
        required=True,
        label='Start time',
        #input_date_formats=None,
        input_time_formats=['%I:%M %p'],
        widget=MySplitDateTimeWidget(
            attrs={'date_class' : 'datePicker', 'time_class' : 'timePicker'},
            date_format='%m/%d/%Y',
            time_format='%I:%M %p'))

    end = forms.SplitDateTimeField(
        required=True,
        label='End time',
        #input_date_formats=None,
        input_time_formats=['%I:%M %p'],
        widget=MySplitDateTimeWidget(
            attrs={'date_class' : 'datePicker', 'time_class' : 'timePicker'},
            date_format='%m/%d/%Y',
            time_format='%I:%M %p'))

    choice_1 = forms.CharField(widget = forms.TextInput(
        attrs = {'class':'required'}),
        help_text = 'Allowed choices for the question. At least two are required.')
    choice_2 = forms.CharField(widget = forms.TextInput(attrs = {'class':'required'}))
    choice_3 = forms.CharField(required = False)
    choice_4 = forms.CharField(required = False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(forms.Form, self).__init__(*args, **kwargs)

    def save(self):
        question = Question(title = self.cleaned_data['question_title'],
            text = self.cleaned_data['question_text'],
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'])
        question.save()
        for field in self.fields:
            if field in ['question_title','question_text', 'start', 'end']:
                continue
            if self.cleaned_data[field]:
                choice = Choice(question = question, text = self.cleaned_data[field])
                choice.save()
        return question