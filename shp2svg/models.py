import os
import math
from django.conf import settings
from django.contrib.gis.db import models
from django.template.loader import get_template, Context
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType


class ShapeCollection(models.Model):
    """
    A model for grouping multiple shapes. Allows
    you to group U.S. States, for example, then export them as
    a Dict of SVG paths with the same projection.
    """
    name = models.CharField(max_length=500)
    # srid = models.IntegerField(max_length=100, default=900913)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name


class Shape(models.Model):
    """
    An individual MultiPolygon
    """
    poly = models.MultiPolygonField()
    # Will store the attributes here as JSON
    attributes = models.TextField(blank=True, null=True)
    collection = models.ForeignKey("ShapeCollection", null=True, blank=True)
