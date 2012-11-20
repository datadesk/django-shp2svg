# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Shape.poly'
        db.alter_column('shp2svg_shape', 'poly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')())

    def backwards(self, orm):

        # Changing field 'Shape.poly'
        db.alter_column('shp2svg_shape', 'poly', self.gf('django.contrib.gis.db.models.fields.PolygonField')())

    models = {
        'shp2svg.shape': {
            'Meta': {'object_name': 'Shape'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shp2svg.ShapeCollection']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {})
        },
        'shp2svg.shapecollection': {
            'Meta': {'object_name': 'ShapeCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['shp2svg']