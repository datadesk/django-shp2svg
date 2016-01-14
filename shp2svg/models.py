import os
import json
import math
import subprocess
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon



def get_dbf_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.dbf')

def get_prj_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.prj')

def get_shp_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.shp')

def get_shx_path(instance, filename):
    return os.path.join('shapes', instance.slug, instance.slug + '.shx')


class Shape(models.Model):
    """
    An individual MultiPolygon
    """
    poly = models.MultiPolygonField(dim=3)
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


class ShapefileContainer(models.Model):
    """
    A model for grouping multiple shapes. Allows
    you to group U.S. States, for example, then export them as
    a Dict of SVG paths with the same projection.
    """
    name = models.CharField(max_length=500)
    source = models.CharField(max_length=500, blank=True)
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
        return os.path.join(settings.ROOT_PATH, 'media', 'shapes', self.slug)

    def get_projected_shapes(self, srid):
        """
        Returns a projected geoqueryset of all of the Shape objects
        in the collection
        """
        res = self.shape_set.all().transform(srid)
        print res
        return res
    
    def get_absolute_url(self):
        return '/%s/' % self.slug

    def delete(self, *args, **kwargs):
        """
        A custom delete method that also kills the associated files
        """
        # kill off the files individually
        self.dbf.delete()
        self.prj.delete()
        self.shp.delete()
        self.shx.delete()
        # get rid of the directory
        path = self.get_shapefile_folder()
        subprocess.call(['rm', '-rf', path])
        # and kill off the object
        super(ShapefileContainer, self).delete(*args, **kwargs)

    def create_shapes(self):
        ds = DataSource(self.shp.path)
        layer = ds[0]
        attribute_fields = layer.fields
        for feature in layer:
            if 'polygon' in str(feature.geom.geom_type).lower():
                # Grab a dict of all the attributes
                attribute_dict = dict( (attr, str(feature[attr].value).decode('latin-1')) for attr in attribute_fields )
                # convert to multipolygon if necessary
                if 'multipolygon' not in str(feature.geom.geom_type).lower():
                    mp = MultiPolygon(feature.geom.geos)
                else:
                    mp = feature.geom.geos
                # load in the shape
                print mp
                shape = Shape.objects.create(
                    poly=mp,
                    attributes=json.dumps(attribute_dict),
                    shapefile=self,
                )
                print "created", shape
