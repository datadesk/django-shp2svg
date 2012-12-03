# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ShapefileContainer.shp'
        db.alter_column('shp2svg_shapefilecontainer', 'shp', self.gf('django.db.models.fields.files.FileField')(max_length=500))

        # Changing field 'ShapefileContainer.shx'
        db.alter_column('shp2svg_shapefilecontainer', 'shx', self.gf('django.db.models.fields.files.FileField')(max_length=500))

        # Changing field 'ShapefileContainer.dbf'
        db.alter_column('shp2svg_shapefilecontainer', 'dbf', self.gf('django.db.models.fields.files.FileField')(max_length=500))

        # Changing field 'ShapefileContainer.prj'
        db.alter_column('shp2svg_shapefilecontainer', 'prj', self.gf('django.db.models.fields.files.FileField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'ShapefileContainer.shp'
        db.alter_column('shp2svg_shapefilecontainer', 'shp', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'ShapefileContainer.shx'
        db.alter_column('shp2svg_shapefilecontainer', 'shx', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'ShapefileContainer.dbf'
        db.alter_column('shp2svg_shapefilecontainer', 'dbf', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'ShapefileContainer.prj'
        db.alter_column('shp2svg_shapefilecontainer', 'prj', self.gf('django.db.models.fields.files.FileField')(max_length=100))

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
            'is_permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'prj': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'shp': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'shx': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        }
    }

    complete_apps = ['shp2svg']