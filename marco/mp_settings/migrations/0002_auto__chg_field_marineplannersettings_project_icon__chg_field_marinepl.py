# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MarinePlannerSettings.project_icon'
        db.alter_column('mp_settings_marineplannersettings', 'project_icon', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'MarinePlannerSettings.project_logo'
        db.alter_column('mp_settings_marineplannersettings', 'project_logo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'MarinePlannerSettings.project_icon'
        db.alter_column('mp_settings_marineplannersettings', 'project_icon', self.gf('django.db.models.fields.URLField')(max_length=255, null=True))

        # Changing field 'MarinePlannerSettings.project_logo'
        db.alter_column('mp_settings_marineplannersettings', 'project_logo', self.gf('django.db.models.fields.URLField')(max_length=255, null=True))

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
            'project_icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mp_settings']