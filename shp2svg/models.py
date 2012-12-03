import os
import math
import shutil
from django.conf import settings
from django.contrib.gis.db import models


def get_dbf_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.dbf')

def get_prj_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.prj')

def get_shp_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.shp')

def get_shx_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.shx')


class ShapefileContainer(models.Model):
    """
    A model for grouping multiple shapes. Allows
    you to group U.S. States, for example, then export them as
    a Dict of SVG paths with the same projection.
    """
    name = models.CharField(max_length=500)
    source = models.CharField(max_length=500, blank=True)
    is_permanent = models.BooleanField(default=False)
    slug = models.CharField(max_length=500, unique=True)
    dbf = models.FileField(upload_to=get_dbf_path, max_length=500)
    prj = models.FileField(upload_to=get_prj_path, max_length=500)
    shp = models.FileField(upload_to=get_shp_path, max_length=500)
    shx = models.FileField(upload_to=get_shx_path, max_length=500)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    def get_shapefile_folder(self):
        """
        returns the path to the folder containing the shapefile
        """
        return os.path.join('media', 'shapes', self.slug)

    def get_projected_shapes(self, srid):
        """
        Returns a projected geoqueryset of all of the Shape objects
        in the collection
        """
        return self.shape_set.all().transform(srid)

    def get_absolute_url(self):
        return '/%s/' % self.slug

    # def delete(self):
    #     """
    #     A custom delete method that also kills the associated files
    #     """
    #     shutil.rmtree(self.get_shapefile_folder())
    #     self.shape_set.all().delete()
    #     self.delete()


class Shape(models.Model):
    """
    An individual MultiPolygon
    """
    poly = models.MultiPolygonField()
    # Will store the attributes here as JSON
    attributes = models.TextField(blank=True, null=True)
    shapefile = models.ForeignKey("ShapefileContainer", null=True, blank=True)
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