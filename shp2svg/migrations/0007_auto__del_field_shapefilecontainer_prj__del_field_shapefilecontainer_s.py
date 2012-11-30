# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ShapefileContainer.prj'
        db.delete_column('shp2svg_shapefilecontainer', 'prj')

        # Deleting field 'ShapefileContainer.shx'
        db.delete_column('shp2svg_shapefilecontainer', 'shx')

        # Deleting field 'ShapefileContainer.dbf'
        db.delete_column('shp2svg_shapefilecontainer', 'dbf')


    def backwards(self, orm):
        # Adding field 'ShapefileContainer.prj'
        db.add_column('shp2svg_shapefilecontainer', 'prj',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'ShapefileContainer.shx'
        db.add_column('shp2svg_shapefilecontainer', 'shx',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'ShapefileContainer.dbf'
        db.add_column('shp2svg_shapefilecontainer', 'dbf',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'shp': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        }
    }

    complete_apps = ['shp2svg']