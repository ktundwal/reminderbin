# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table('survey_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('enrolled_in_beta', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('survey', ['Participant'])

        # Adding M2M table for field responses on 'Participant'
        db.create_table('survey_participant_responses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm['survey.participant'], null=False)),
            ('question', models.ForeignKey(orm['survey.question'], null=False))
        ))
        db.create_unique('survey_participant_responses', ['participant_id', 'question_id'])

    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table('survey_participant')

        # Removing M2M table for field responses on 'Participant'
        db.delete_table('survey_participant_responses')

    models = {
        'survey.choice': {
            'Meta': {'object_name': 'Choice'},
            'code': ('django.db.models.fields.IntegerField', [], {'default': '424', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Choices'", 'to': "orm['survey.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'survey.participant': {
            'Meta': {'object_name': 'Participant'},
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'enrolled_in_beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants'", 'symmetrical': 'False', 'to': "orm['survey.Question']"})
        },
        'survey.question': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Question'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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