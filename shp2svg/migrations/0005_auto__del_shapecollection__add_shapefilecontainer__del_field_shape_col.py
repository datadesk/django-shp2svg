# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ShapeCollection'
        db.delete_table('shp2svg_shapecollection')

        # Adding model 'ShapefileContainer'
        db.create_table('shp2svg_shapefilecontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('dbf', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('prj', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('shp', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('shx', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('shp2svg', ['ShapefileContainer'])

        # Deleting field 'Shape.collection'
        db.delete_column('shp2svg_shape', 'collection_id')

        # Adding field 'Shape.shapefile'
        db.add_column('shp2svg_shape', 'shapefile',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shp2svg.ShapefileContainer'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ShapeCollection'
        db.create_table('shp2svg_shapecollection', (
            ('shp', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=500, unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('shx', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('prj', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbf', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('shp2svg', ['ShapeCollection'])

        # Deleting model 'ShapefileContainer'
        db.delete_table('shp2svg_shapefilecontainer')

        # Adding field 'Shape.collection'
        db.add_column('shp2svg_shape', 'collection',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shp2svg.ShapeCollection'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Shape.shapefile'
        db.delete_column('shp2svg_shape', 'shapefile_id')


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