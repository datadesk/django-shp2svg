from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.template.defaultfilters import slugify
from shp2svg.models import ShapeCollection, Shape
from django.contrib.gis.gdal import *
import json


class Command(BaseCommand):
    help = "Loads in Shapes from a shp file"
    
    def handle(self, *args, **kwds):
        # Kill the old shit
        ShapeCollection.objects.all().delete()
        Shape.objects.all().delete()

        # Make this an option, obvs
        shp_path = 'shp2svg/data/us_states/ne_110m_admin_1_states_provinces_lakes_shp.shp'
        ds = DataSource(shp_path)
        # make the layer index an option too
        # or maybe it can autodetect, and only ask for more than one layer
        layer = ds[0]
        attribute_fields = layer.fields
        # make the name an option, obvs
        collection = ShapeCollection.objects.create(
            name = "U.S. States",
            slug = slugify("U.S. States"),
        )
        print collection
        for feature in layer:
            if feature.geom.geom_type in ['Polygon', 'MultiPolygon']:
                # Grab a dict of all the attributes
                attribute_dict = dict( (attr, feature[attr].value) for attr in attribute_fields )
                # convert to multipolygon if necessary
                if feature.geom.geom_type == 'Polygon':
                    mp = MultiPolygon(feature.geom.geos)
                else:
                    mp = feature.geom.geos
                # load in the shape
                shape = Shape.objects.create(
                    poly = mp,
                    attributes = json.dumps(attribute_dict),
                    collection = collection,
                )
                print shape
            else:
                print 'skipped %s' % feature.geom.geom_type
                continue