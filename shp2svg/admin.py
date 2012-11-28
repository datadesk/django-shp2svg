from django.contrib.gis import admin
from shp2svg.models import Shape, ShapefileContainer

admin.site.register(Shape, admin.GeoModelAdmin)
admin.site.register(ShapefileContainer, admin.GeoModelAdmin)