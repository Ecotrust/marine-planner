# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MarinePlannerSettings'
        db.create_table('mp_settings_marineplannersettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('zoom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_zoom', self.gf('django.db.models.fields.IntegerField')(default=5, null=True, blank=True)),
            ('max_zoom', self.gf('django.db.models.fields.IntegerField')(default=12, null=True, blank=True)),
            ('project_logo', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('project_icon', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('project_home_page', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('bitly_registered_domain', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('bitly_username', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('bitly_api_key', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('mp_settings', ['MarinePlannerSettings'])


    def backwards(self, orm):
        # Deleting model 'MarinePlannerSettings'
        db.delete_table('mp_settings_marineplannersettings')


    models = {
        'mp_settings.marineplannersettings': {
            'Meta': {'object_name': 'MarinePlannerSettings'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bitly_api_key': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'bitly_registered_domain': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bitly_username': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'max_zoom': ('django.db.models.fields.IntegerField', [], {'default': '12', 'null': 'True', 'blank': 'True'}),
            'min_zoom': ('django.db.models.fields.IntegerField', [], {'default': '5', 'null': 'True', 'blank': 'True'}),
            'project_home_page': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_icon': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_logo': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mp_settings']