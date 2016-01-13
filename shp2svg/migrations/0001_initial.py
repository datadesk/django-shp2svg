# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 23:28
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import shp2svg.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('attributes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShapefileContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('source', models.CharField(blank=True, max_length=500)),
                ('slug', models.CharField(max_length=500, unique=True)),
                ('dbf', models.FileField(max_length=500, upload_to=shp2svg.models.get_dbf_path)),
                ('prj', models.FileField(max_length=500, upload_to=shp2svg.models.get_prj_path)),
                ('shp', models.FileField(max_length=500, upload_to=shp2svg.models.get_shp_path)),
                ('shx', models.FileField(max_length=500, upload_to=shp2svg.models.get_shx_path)),
            ],
        ),
        migrations.AddField(
            model_name='shape',
            name='shapefile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shp2svg.ShapefileContainer'),
        ),
    ]
