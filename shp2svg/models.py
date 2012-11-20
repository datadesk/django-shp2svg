import os
import math
from django.conf import settings
from django.contrib.gis.db import models


class ShapeCollection(models.Model):
    """
    A model for grouping multiple shapes. Allows
    you to group U.S. States, for example, then export them as
    a Dict of SVG paths with the same projection.
    """
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    def get_projected_shapes(self, srid):
        """
        Returns a projected geoqueryset of all of the Shape objects
        in the collection
        """
        return self.shape_set.all().transform(srid)


class Shape(models.Model):
    """
    An individual MultiPolygon
    """
    poly = models.MultiPolygonField()
    # Will store the attributes here as JSON
    attributes = models.TextField(blank=True, null=True)
    collection = models.ForeignKey("ShapeCollection", null=True, blank=True)
    objects = models.GeoManager()
    
    def get_extracted_coords(self):
        """
        Extracts the nested multigeometry coordinates into a nicer list
        """
        coords = self.poly.coords
        geom_list = []
        for i in coords:
            for coord in i:
                geom_list.append(list(coord))
        return geom_list