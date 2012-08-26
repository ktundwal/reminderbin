__author__ = 'browsepad'

from .models import *
from django.contrib import admin

admin.site.register(Survey)
admin.site.register(Participant)
admin.site.register(Feedback)

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

    def save_model(self, request, obj, form, change):
        update_question_before_save(obj)
        obj.save()

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('simple_code',)

    def save_model(self, request, obj, form, change):
        update_choice_before_save(obj)
        obj.save()

admin.site.register(Choice, ChoiceAdmin)