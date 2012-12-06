# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShapefileContainer'
        db.create_table('shp2svg_shapefilecontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('dbf', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
            ('prj', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
            ('shp', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
            ('shx', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
        ))
        db.send_create_signal('shp2svg', ['ShapefileContainer'])

        # Adding model 'Shape'
        db.create_table('shp2svg_shape', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('attributes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shapefile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shp2svg.ShapefileContainer'], null=True, blank=True)),
        ))
        db.send_create_signal('shp2svg', ['Shape'])


    def backwards(self, orm):
        # Deleting model 'ShapefileContainer'
        db.delete_table('shp2svg_shapefilecontainer')

        # Deleting model 'Shape'
        db.delete_table('shp2svg_shape')


    models = {
        'shp2svg.shape': {
            'Meta': {'object_name': 'Shape'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'shapefile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shp2svg.ShapefileContainer']", 'null': 'True', 'blank': 'True'})
        },
        'shp2svg.shapefilecontainer': {
            'Meta': {'object_name': 'ShapefileContainer'},
            'dbf': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'prj': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'shp': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'shx': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        }
    }

    complete_apps = ['shp2svg']