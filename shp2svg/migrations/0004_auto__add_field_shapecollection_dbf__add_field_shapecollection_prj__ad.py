# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ShapeCollection.dbf'
        db.add_column('shp2svg_shapecollection', 'dbf',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'ShapeCollection.prj'
        db.add_column('shp2svg_shapecollection', 'prj',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'ShapeCollection.shp'
        db.add_column('shp2svg_shapecollection', 'shp',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'ShapeCollection.shx'
        db.add_column('shp2svg_shapecollection', 'shx',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ShapeCollection.dbf'
        db.delete_column('shp2svg_shapecollection', 'dbf')

        # Deleting field 'ShapeCollection.prj'
        db.delete_column('shp2svg_shapecollection', 'prj')

        # Deleting field 'ShapeCollection.shp'
        db.delete_column('shp2svg_shapecollection', 'shp')

        # Deleting field 'ShapeCollection.shx'
        db.delete_column('shp2svg_shapecollection', 'shx')


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
            'dbf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'prj': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'shp': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'shx': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'})
        }
    }

    complete_apps = ['shp2svg']