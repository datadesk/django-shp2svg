import math
import json
from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
from shp2svg.models import Shape, ShapeCollection

#
# Some utility functions for processing the SVG paths
#

def get_projected_extent(geoqueryset):
    """
    Returns the min and max x and y coordinates for the collection
    """
    x_coords = []
    y_coords = []
    for i in geoqueryset:
        coords = i.poly.extent
        x_coords.append(coords[0])
        x_coords.append(coords[2])
        y_coords.append(coords[1])
        y_coords.append(coords[3])
    return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))

def get_scale_factor(extent, max_size):
    """
    Provides a scaling constant to convert our translated coordinates to
    screen pixels.
    """
    max_translated_x = abs(extent[2] - extent[0])
    max_translated_y = abs(extent[3] - extent[1])
    
    if max_translated_x > max_translated_y:
        scaling_factor = max_size / max_translated_x
    
    elif max_translated_y > max_translated_x:
        scaling_factor = max_size / max_translated_y
    
    return scaling_factor

def get_scaled_max_coords(extent, scale):
    """
    Returns the scaled max x and y coordinates of the state,
    good for image height and width.
    """
    extent = list(extent)
    y_translated_max = abs(extent[3] - extent[1])
    x_translated_max = abs(extent[2] - extent[0])
    return [int(math.ceil(x_translated_max * scale)), int(math.ceil(y_translated_max * scale))]

def translate_coords(coord_list, extent):
    """
    takes a list of coordinates, then translates them to [0, 0]
    """
    x_min = extent[0]
    y_min = extent[1]
    y_translated_max = abs(extent[3] - extent[1])
    translated_coords = []
    for i in coord_list:
        new_coords = (i[0] - x_min, y_translated_max - (i[1] - y_min))
        translated_coords.append(new_coords)
    return translated_coords

def coords_2_path(coord_list):
    """
    Takes a list of coordinates and returns an SVG path element
    """
    path = 'M%s,%s' % (coord_list[0][0], coord_list[0][1])
    for i in coord_list[1:]:
        path += 'L%s,%s' % (i[0], i[1])
    path += 'Z'
    return path.replace('-0.0', '0').replace('0.0', '0').replace('.0', '')

def get_scaled_paths(queryset, scale, extent, key, translate=[0,0]):
    """
    Returns a dict with each item in the queryset and a list of scaled coordinates.
    """
    scaled_coord_set = {}
    for i in queryset:
        # load in the attribute dict
        attrs = json.loads(i.attributes)
        k = attrs.get(key)
        # First grab the coordinates to play with
        coords = i.get_extracted_coords()
        # Loop through each set and translate them
        translated_coords = []
        for c in coords:
            translated_coords.append(translate_coords(c, extent))
        
        # Then loop through our translated coords and scale them
        scaled_coords = []
        for t in translated_coords:
            scaled_list = []
            for coord_set in t:
                scaled_set = (format(( coord_set[0] * scale) + translate[0], '.1f'), format(( coord_set[1] * scale)  + translate[1], '.1f'))
                scaled_list.append(scaled_set)
            scaled_coords.append(scaled_list)
        
        # Now to grab a translated/scaled centroid for each shape
        centroid = i.poly.centroid.coords
        translated_centroid = translate_coords([centroid], extent)
        translated_centroid = translated_centroid[0]
        scaled_centroid = [int(translated_centroid[0] * scale), int(translated_centroid[1] * scale)]

        path = ''
        for i in scaled_coords:
            path += coords_2_path(i)

        scaled_coord_set[k] = {
            'path': path,
            'centroid': scaled_centroid,
        }
    
    return scaled_coord_set

#
# The actual Views
#

def index(request):
    context = {
        'collections': ShapeCollection.objects.all()
    }
    
    return render(request, 'index.html', context)



def shape_collection(request, slug):
    """

    """
    try:
        collection = ShapeCollection.objects.get(slug=slug)
    except ShapeCollection.DoesNotExist:
        raise Http404

    # must work in a way to feed in options through the request
    # in the meantime...
    translate = [0, 0]
    max_size = 700
    srid = 900913
    key = "postal"

    projected_shapes = collection.get_projected_shapes(srid)
    extent = get_projected_extent(projected_shapes)
    scale_factor = get_scale_factor(extent, max_size)
    max_coords = get_scaled_max_coords(extent, scale_factor)
    paths = get_scaled_paths(projected_shapes, scale_factor, extent, key, translate=translate)

    context = {
        'collection': collection,
        'paths': json.dumps(paths),
        'max_coords': max_coords
    }

    return render(request, 'collection.html', context)



# def generate_svg(self):
#     """
#     Generates an SVG file from the state
#     """
#     county_paths = self.get_county_paths()
#     cities = self.get_top_city_coords()
#     size = self.get_scaled_max_coords()
#     template = get_template('svg.html')
#     svg_string = template.render(Context({
#         'size': size,
#         'county_paths': county_paths,
#         'cities': cities,
#     }))
#     # Write the SVG to system
#     outfile = open(os.path.join(settings.SVG_EXPORT_PATH, '%s.svg' % self.name), "w")
#     outfile.write(svg_string)
#     outfile.close()