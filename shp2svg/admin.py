from django.contrib.gis import admin
from shp2svg.models import Shape, ShapeCollection

admin.site.register(Shape, admin.GeoModelAdmin)
admin.site.register(ShapeCollection, admin.GeoModelAdmin)