# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Scenario.sand_area_max'
        db.delete_column(u'scenarios_scenario', 'sand_area_max')

        # Deleting field 'Scenario.habitat'
        db.delete_column(u'scenarios_scenario', 'habitat')

        # Deleting field 'Scenario.art_area_min'
        db.delete_column(u'scenarios_scenario', 'art_area_min')

        # Deleting field 'Scenario.acerv_area_min'
        db.delete_column(u'scenarios_scenario', 'acerv_area_min')

        # Deleting field 'Scenario.type_1'
        db.delete_column(u'scenarios_scenario', 'type_1')

        # Deleting field 'Scenario.sand_area_min'
        db.delete_column(u'scenarios_scenario', 'sand_area_min')

        # Deleting field 'Scenario.sg_area'
        db.delete_column(u'scenarios_scenario', 'sg_area')

        # Deleting field 'Scenario.art_area_max'
        db.delete_column(u'scenarios_scenario', 'art_area_max')

        # Deleting field 'Scenario.reef_area'
        db.delete_column(u'scenarios_scenario', 'reef_area')

        # Deleting field 'Scenario.acerv_area'
        db.delete_column(u'scenarios_scenario', 'acerv_area')

        # Deleting field 'Scenario.art_area'
        db.delete_column(u'scenarios_scenario', 'art_area')

        # Deleting field 'Scenario.sg_area_max'
        db.delete_column(u'scenarios_scenario', 'sg_area_max')

        # Deleting field 'Scenario.sand_area'
        db.delete_column(u'scenarios_scenario', 'sand_area')

        # Deleting field 'Scenario.reef_area_min'
        db.delete_column(u'scenarios_scenario', 'reef_area_min')

        # Deleting field 'Scenario.reef_area_max'
        db.delete_column(u'scenarios_scenario', 'reef_area_max')

        # Deleting field 'Scenario.type_2'
        db.delete_column(u'scenarios_scenario', 'type_2')

        # Deleting field 'Scenario.sg_area_min'
        db.delete_column(u'scenarios_scenario', 'sg_area_min')

        # Deleting field 'Scenario.county'
        db.delete_column(u'scenarios_scenario', 'county')

        # Deleting field 'Scenario.region'
        db.delete_column(u'scenarios_scenario', 'region')

        # Deleting field 'Scenario.prev_impact'
        db.delete_column(u'scenarios_scenario', 'prev_impact')

        # Deleting field 'Scenario.modifier'
        db.delete_column(u'scenarios_scenario', 'modifier')

        # Deleting field 'Scenario.acerv_area_max'
        db.delete_column(u'scenarios_scenario', 'acerv_area_max')

        # Adding field 'Scenario.pillar_presence'
        db.add_column(u'scenarios_scenario', 'pillar_presence',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.pillar_presence_input'
        db.add_column(u'scenarios_scenario', 'pillar_presence_input',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.anchorage'
        db.add_column(u'scenarios_scenario', 'anchorage',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.anchorage_input'
        db.add_column(u'scenarios_scenario', 'anchorage_input',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.mooring_buoy'
        db.add_column(u'scenarios_scenario', 'mooring_buoy',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.mooring_buoy_input'
        db.add_column(u'scenarios_scenario', 'mooring_buoy_input',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.impacted'
        db.add_column(u'scenarios_scenario', 'impacted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.impacted_input'
        db.add_column(u'scenarios_scenario', 'impacted_input',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sg'
        db.add_column(u'scenarios_scenario', 'prcnt_sg',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sg_min'
        db.add_column(u'scenarios_scenario', 'prcnt_sg_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sg_max'
        db.add_column(u'scenarios_scenario', 'prcnt_sg_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_reef'
        db.add_column(u'scenarios_scenario', 'prcnt_reef',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_reef_min'
        db.add_column(u'scenarios_scenario', 'prcnt_reef_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_reef_max'
        db.add_column(u'scenarios_scenario', 'prcnt_reef_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sand'
        db.add_column(u'scenarios_scenario', 'prcnt_sand',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sand_min'
        db.add_column(u'scenarios_scenario', 'prcnt_sand_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_sand_max'
        db.add_column(u'scenarios_scenario', 'prcnt_sand_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_art'
        db.add_column(u'scenarios_scenario', 'prcnt_art',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_art_min'
        db.add_column(u'scenarios_scenario', 'prcnt_art_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prcnt_art_max'
        db.add_column(u'scenarios_scenario', 'prcnt_art_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Scenario.sand_area_max'
        db.add_column(u'scenarios_scenario', 'sand_area_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.habitat'
        db.add_column(u'scenarios_scenario', 'habitat',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.art_area_min'
        db.add_column(u'scenarios_scenario', 'art_area_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.acerv_area_min'
        db.add_column(u'scenarios_scenario', 'acerv_area_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.type_1'
        db.add_column(u'scenarios_scenario', 'type_1',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.sand_area_min'
        db.add_column(u'scenarios_scenario', 'sand_area_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.sg_area'
        db.add_column(u'scenarios_scenario', 'sg_area',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.art_area_max'
        db.add_column(u'scenarios_scenario', 'art_area_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_area'
        db.add_column(u'scenarios_scenario', 'reef_area',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.acerv_area'
        db.add_column(u'scenarios_scenario', 'acerv_area',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.art_area'
        db.add_column(u'scenarios_scenario', 'art_area',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.sg_area_max'
        db.add_column(u'scenarios_scenario', 'sg_area_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.sand_area'
        db.add_column(u'scenarios_scenario', 'sand_area',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.reef_area_min'
        db.add_column(u'scenarios_scenario', 'reef_area_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_area_max'
        db.add_column(u'scenarios_scenario', 'reef_area_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.type_2'
        db.add_column(u'scenarios_scenario', 'type_2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.sg_area_min'
        db.add_column(u'scenarios_scenario', 'sg_area_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.county'
        db.add_column(u'scenarios_scenario', 'county',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.region'
        db.add_column(u'scenarios_scenario', 'region',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.prev_impact'
        db.add_column(u'scenarios_scenario', 'prev_impact',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.modifier'
        db.add_column(u'scenarios_scenario', 'modifier',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.acerv_area_max'
        db.add_column(u'scenarios_scenario', 'acerv_area_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Scenario.pillar_presence'
        db.delete_column(u'scenarios_scenario', 'pillar_presence')

        # Deleting field 'Scenario.pillar_presence_input'
        db.delete_column(u'scenarios_scenario', 'pillar_presence_input')

        # Deleting field 'Scenario.anchorage'
        db.delete_column(u'scenarios_scenario', 'anchorage')

        # Deleting field 'Scenario.anchorage_input'
        db.delete_column(u'scenarios_scenario', 'anchorage_input')

        # Deleting field 'Scenario.mooring_buoy'
        db.delete_column(u'scenarios_scenario', 'mooring_buoy')

        # Deleting field 'Scenario.mooring_buoy_input'
        db.delete_column(u'scenarios_scenario', 'mooring_buoy_input')

        # Deleting field 'Scenario.impacted'
        db.delete_column(u'scenarios_scenario', 'impacted')

        # Deleting field 'Scenario.impacted_input'
        db.delete_column(u'scenarios_scenario', 'impacted_input')

        # Deleting field 'Scenario.prcnt_sg'
        db.delete_column(u'scenarios_scenario', 'prcnt_sg')

        # Deleting field 'Scenario.prcnt_sg_min'
        db.delete_column(u'scenarios_scenario', 'prcnt_sg_min')

        # Deleting field 'Scenario.prcnt_sg_max'
        db.delete_column(u'scenarios_scenario', 'prcnt_sg_max')

        # Deleting field 'Scenario.prcnt_reef'
        db.delete_column(u'scenarios_scenario', 'prcnt_reef')

        # Deleting field 'Scenario.prcnt_reef_min'
        db.delete_column(u'scenarios_scenario', 'prcnt_reef_min')

        # Deleting field 'Scenario.prcnt_reef_max'
        db.delete_column(u'scenarios_scenario', 'prcnt_reef_max')

        # Deleting field 'Scenario.prcnt_sand'
        db.delete_column(u'scenarios_scenario', 'prcnt_sand')

        # Deleting field 'Scenario.prcnt_sand_min'
        db.delete_column(u'scenarios_scenario', 'prcnt_sand_min')

        # Deleting field 'Scenario.prcnt_sand_max'
        db.delete_column(u'scenarios_scenario', 'prcnt_sand_max')

        # Deleting field 'Scenario.prcnt_art'
        db.delete_column(u'scenarios_scenario', 'prcnt_art')

        # Deleting field 'Scenario.prcnt_art_min'
        db.delete_column(u'scenarios_scenario', 'prcnt_art_min')

        # Deleting field 'Scenario.prcnt_art_max'
        db.delete_column(u'scenarios_scenario', 'prcnt_art_max')


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
            'acerv_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'acropora_pa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'anchorage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'art_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'boat_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'coral_bleach': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'depth_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dive_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'esa_spp': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fish_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_div': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impacted': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'injury_site': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'large_live_coral': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lionfish': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'major_habitat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_buoy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pillar_presence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rec_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reef_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sand_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sg_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unique_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'scenarios.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'acropora_pa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'acropora_pa_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anchorage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anchorage_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'depth_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fish_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_dissolved': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'geometry_final_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'grid_cells': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'impacted_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'injury_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'injury_site_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inlet_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'large_live_coral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large_live_coral_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_buoy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mooring_buoy_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'outfall_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pier_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pillar_presence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pillar_presence_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_art_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_reef_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_sand_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_sg_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sharing_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'scenarios_scenario_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            'shore_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shore_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'scenarios_scenario_related'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['scenarios']