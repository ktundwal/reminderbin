# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table('survey_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('survey', ['Survey'])

        # Adding model 'Question'
        db.create_table('survey_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 5, 0, 0))),
            ('allow_multiple', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('survey', ['Question'])

        # Adding model 'Choice'
        db.create_table('survey_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Choices', to=orm['survey.Question'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.IntegerField')(default=185, unique=True)),
            ('total_votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('survey', ['Choice'])

    def backwards(self, orm):
        # Deleting model 'Survey'
        db.delete_table('survey_survey')

        # Deleting model 'Question'
        db.delete_table('survey_question')

        # Deleting model 'Choice'
        db.delete_table('survey_choice')

    models = {
        'survey.choice': {
            'Meta': {'object_name': 'Choice'},
            'code': ('django.db.models.fields.IntegerField', [], {'default': '185', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Choices'", 'to': "orm['survey.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'survey.question': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Question'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 5, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
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