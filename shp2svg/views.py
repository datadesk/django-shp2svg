import math
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.gis.gdal import *
from django.views.generic.base import View
from django.utils import simplejson as json
from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from shp2svg.models import Shape, ShapefileContainer
from django.contrib.gis.geos import MultiPolygon, Polygon


def index(request):
    context = {
        'shapefiles': ShapefileContainer.objects.all()
    }
    return render(request, 'index.html', context)

def shapefile(request, slug):
    try:
        shapefile = ShapefileContainer.objects.get(slug=slug)
    except ShapefileContainer.DoesNotExist:
        raise Http404

    ds = DataSource(shapefile.shp.path)
    layer = ds[0]
    context = {
        'name': shapefile.name,
        'slug': shapefile.slug,
        'fields': layer.fields,
    }
    return render(request, 'shapefile.html', context)

def upload_shapefile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # Check to see if we already have an object with that name
        try:
            ShapefileContainer.objects.get(slug=slugify(name))
            invalid_name_response = HttpResponse("The name you chose is already taken.")
            invalid_name_response.status_code = 500
            return invalid_name_response
        except ShapefileContainer.DoesNotExist:
            pass
        # Make the new shape container
        new_shapefile = ShapefileContainer.objects.create(
            name=name,
            slug=slugify(name),
            dbf=request.FILES.get('dbf'),
            prj=request.FILES.get('prj'),
            shp=request.FILES.get('shp'),
            shx=request.FILES.get('shx'),
        )
        # See if we can import the shapefile. 
        try:
            ds = DataSource(new_shapefile.shp.path)
        except:
            new_shapefile.delete()
            response = HttpResponse("There was a problem processing your shapefile.")
            response.status_code = 500
            return response

        layer = ds[0]
        attribute_fields = layer.fields
        for feature in layer:
            if feature.geom.geom_type in ['Polygon', 'MultiPolygon']:
                # Grab a dict of all the attributes
                attribute_dict = dict( (attr, str(feature[attr].value).decode('latin-1')) for attr in attribute_fields )
                # convert to multipolygon if necessary
                if feature.geom.geom_type == 'Polygon':
                    mp = MultiPolygon(feature.geom.geos)
                else:
                    mp = feature.geom.geos
                # load in the shape
                try:
                    shape = Shape.objects.create(
                        poly = mp,
                        attributes = json.dumps(attribute_dict),
                        shapefile = new_shapefile,
                    )
                except:
                    response = HttpResponse("There was a problem processing your shapefile.")
                    response.status_code = 500
                    return response
            else:
                continue

        data = {
            'name': new_shapefile.name,
            'slug': new_shapefile.slug,
            'fields': attribute_fields,
        }
        return HttpResponse(json.dumps(data), content_type='text/html')


class SVGResponseMixin(object):
    """
    A mixin that can be used to render an SVG response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a CSV file response, transforming 'context' to make the payload.
        """
        template = get_template('svg.html')
        response = HttpResponse(template.render(context), mimetype='image/svg+xml')
        response['Content-Disposition'] = 'attachment; filename=shp2svg.svg'
        return response


class JSONResponseMixin(object):
    """
    A mixin for rendering a JSON as an AJAX response. Where the 'JSON' is actually
    sent as a text/html mimetype to avoid an awkward bug in IE.
    """
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context), content_type='text/html')


class GenerateSVG(SVGResponseMixin, JSONResponseMixin, View):
    
    def translate_coords(self, coord_list, extent):
        """
        Takes a list of coordinates and translates them to [0, 0]
        """
        x_min = extent[0]
        y_min = extent[1]
        y_translated_max = abs(extent[3] - extent[1])
        translated_coords = []
        for i in coord_list:
            new_coords = (i[0] - x_min, y_translated_max - (i[1] - y_min))
            translated_coords.append(new_coords)
        return translated_coords

    def coords_2_path(self, coord_list):
        """
        Takes a list of coordinates and returns an SVG path
        """
        if len(coord_list) == 1:
            path = 'M%s,%sZ' % (coord_list[0][0], coord_list[0][1])
        else:
            path = 'M%s,%s' % (coord_list[0][0], coord_list[0][1])
            for i in coord_list[1:]:
                path += 'L%s,%s' % (i[0], i[1])
            path += 'Z'
        return path.replace('-0.0', '0').replace('0.0', '0').replace('.0', '')

    def get(self, request, *args, **kwargs):
        self.format = self.request.GET.get('format', 'json')
        slug = self.request.GET.get('slug')
        try:
            shapefile = ShapefileContainer.objects.get(slug=slug)
        except ShapefileContainer.DoesNotExist:
            raise Http404

        translate = [0, 0]
        # some validation on the user input
        invalid_int_response = HttpResponse("Please enter a valid integer.")
        invalid_int_response.status_code = 500

        if self.request.GET.get('translate_x'):
            try:
                translate[0] = int(self.request.GET.get('translate_x'))
            except ValueError:
                return invalid_int_response

        if self.request.GET.get('translate_y'):
            try:
                translate[1] = int(self.request.GET.get('translate_y'))
            except ValueError:
                return invalid_int_response
        
        try:
            max_size = int(self.request.GET.get('max_size'))
            srid = int(self.request.GET.get('srid'))
        except ValueError:
            return invalid_int_response
        
        key = self.request.GET.get('key')
        centroid = self.request.GET.get('centroid', False)
        if centroid == 'on':
            centroid = True
        
        # get a projected geoqueryset
        projected_shapes = shapefile.get_projected_shapes(srid)
        
        # get the projected extent of the geoqueryset
        x_coords = []
        y_coords = []
        # Wrap this in a try/except to return any errors we hit with the projection
        try:
            for i in projected_shapes:
                coords = i.poly.extent
                x_coords.append(coords[0])
                x_coords.append(coords[2])
                y_coords.append(coords[1])
                y_coords.append(coords[3])
        except:
            response = HttpResponse("There was a problem projecting your shapefile. Please try a different SRID.")
            response.status_code = 500
            return response
        extent = (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
        
        # get a constant to scale the coords to the provided max_size
        max_translated_x = abs(extent[2] - extent[0])
        max_translated_y = abs(extent[3] - extent[1])
        if max_translated_x > max_translated_y:
            scale_factor = max_size / max_translated_x
        elif max_translated_y > max_translated_x:
            scale_factor = max_size / max_translated_y
        
        # Determine our new max X and Y values
        extent = list(extent)
        y_translated_max = abs(extent[3] - extent[1])
        x_translated_max = abs(extent[2] - extent[0])
        max_coords = [int(math.ceil(x_translated_max * scale_factor)), int(math.ceil(y_translated_max * scale_factor))]
        
        # generate all the paths
        paths = {}
        for i in projected_shapes:
            # load in the attribute dict
            attrs = json.loads(i.attributes)
            k = attrs.get(key)
            # First grab the coordinates to play with
            coords = i.get_extracted_coords()
            # Loop through each set and translate them
            translated_coords = []
            for c in coords:
                translated_coords.append(self.translate_coords(c, extent))
            
            # Then loop through our translated coords and scale them
            scaled_coords = []
            for t in translated_coords:
                scaled_list = []
                for coord_set in t:
                    scaled_set = (format(( coord_set[0] * scale_factor) + translate[0], '.1f'), format(( coord_set[1] * scale_factor)  + translate[1], '.1f'))
                    scaled_list.append(scaled_set)
                scaled_coords.append(scaled_list)
            
            # Now to grab a translated/scaled centroid for each shape
            if centroid:
                centroid = i.poly.centroid.coords
                translated_centroid = self.translate_coords([centroid], extent)
                translated_centroid = translated_centroid[0]
                scaled_centroid = [int(translated_centroid[0] * scale_factor) + translate[0], int(translated_centroid[1] * scale_factor) + translate[1]]
                
                path = ''
                for i in scaled_coords:
                    path += self.coords_2_path(i)

                paths[k] = {
                    'path': path,
                    'centroid': scaled_centroid,
                }
            else:
                path = ''
                for i in scaled_coords:
                    path += self.coords_2_path(i)

                paths[k] = path
        
        context = {
            'paths': paths,
            'centroid': centroid,
            'max_coords': [max_coords[0] + translate[0], max_coords[1] + translate[1]],
        }
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """
        Figures out what type of response is necessary and pulls the trigger.
        """
        if self.format == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        elif self.format == 'svg':
            return SVGResponseMixin.render_to_response(self, context)
        else:
            return Http404

