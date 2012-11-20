# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShapeCollection'
        db.create_table('shp2svg_shapecollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('shp2svg', ['ShapeCollection'])

        # Adding model 'Shape'
        db.create_table('shp2svg_shape', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poly', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('attributes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shp2svg.ShapeCollection'], null=True, blank=True)),
        ))
        db.send_create_signal('shp2svg', ['Shape'])


    def backwards(self, orm):
        # Deleting model 'ShapeCollection'
        db.delete_table('shp2svg_shapecollection')

        # Deleting model 'Shape'
        db.delete_table('shp2svg_shape')


    models = {
        'shp2svg.shape': {
            'Meta': {'object_name': 'Shape'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shp2svg.ShapeCollection']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poly': ('django.contrib.gis.db.models.fields.PolygonField', [], {})
        },
        'shp2svg.shapecollection': {
            'Meta': {'object_name': 'ShapeCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['shp2svg']