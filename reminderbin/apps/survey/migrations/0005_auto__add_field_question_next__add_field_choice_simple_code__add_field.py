# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.next'
        db.add_column('survey_question', 'next',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='previous', null=True, to=orm['survey.Question']),
                      keep_default=False)

        # Adding field 'Choice.simple_code'
        db.add_column('survey_choice', 'simple_code',
                      self.gf('django.db.models.fields.CharField')(default='a', max_length=1),
                      keep_default=False)

        # Adding field 'Participant.awaiting_response_on'
        db.add_column('survey_participant', 'awaiting_response_on',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awaiting_responses_from', null=True, to=orm['survey.Question']),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Question.next'
        db.delete_column('survey_question', 'next_id')

        # Deleting field 'Choice.simple_code'
        db.delete_column('survey_choice', 'simple_code')

        # Deleting field 'Participant.awaiting_response_on'
        db.delete_column('survey_participant', 'awaiting_response_on_id')

    models = {
        'survey.choice': {
            'Meta': {'object_name': 'Choice'},
            'code': ('django.db.models.fields.IntegerField', [], {'default': '137', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Choices'", 'to': "orm['survey.Question']"}),
            'simple_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'survey.feedback': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Feedback'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 25, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'provided_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Feedbacks'", 'to': "orm['survey.Participant']"})
        },
        'survey.participant': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Participant'},
            'awaiting_response_on': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awaiting_responses_from'", 'null': 'True', 'to': "orm['survey.Question']"}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 25, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'enrolled_in_beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants'", 'symmetrical': 'False', 'to': "orm['survey.Question']"})
        },
        'survey.question': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Question'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 25, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous'", 'null': 'True', 'to': "orm['survey.Question']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'survey.survey': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Survey'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['survey']