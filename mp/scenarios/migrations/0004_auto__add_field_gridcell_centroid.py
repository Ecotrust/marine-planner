# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GridCell.centroid'
        db.add_column(u'scenarios_gridcell', 'centroid',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GridCell.centroid'
        db.delete_column(u'scenarios_gridcell', 'centroid')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scenarios.gridcell': {
            'Meta': {'object_name': 'GridCell'},
            'acropora_pa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fish_abundance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'habitat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inlet_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modifier': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prev_impact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'scenarios.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'acropora_pa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'scenarios_scenario_related'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'coral_density': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_density_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_size': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_size_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_size_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fish_abundance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fish_abundance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_abundance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fish_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_dissolved': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'geometry_final_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'grid_cells': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'habitat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inlet_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inlet_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modifier': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prev_impact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sharing_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'scenarios_scenario_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            'shore_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shore_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'type_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'scenarios_scenario_related'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['scenarios']