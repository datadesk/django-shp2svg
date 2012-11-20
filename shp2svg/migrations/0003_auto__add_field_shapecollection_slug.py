# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ShapeCollection.slug'
        db.add_column('shp2svg_shapecollection', 'slug',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=500),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ShapeCollection.slug'
        db.delete_column('shp2svg_shapecollection', 'slug')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'})
        }
    }

    complete_apps = ['shp2svg']