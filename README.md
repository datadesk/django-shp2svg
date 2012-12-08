<pre>

         dP                d8888b.                            
         88                    `88                            
.d8888b. 88d888b. 88d888b. .aaadP' .d8888b. dP   .dP .d8888b. 
Y8ooooo. 88'  `88 88'  `88 88'     Y8ooooo. 88   d8' 88'  `88 
      88 88    88 88.  .88 88.           88 88 .88'  88.  .88 
`88888P' dP    dP 88Y888P' Y88888P `88888P' 8888P'   `8888P88 
                  88                                      .88 
                  dP                                  d8888P  

</pre>

django-shp2svg
==============

*This project is still in progress, so don't take too seriously yet*

Convert a shapefile into an SVG you can use with JavaScript drawing libraries.

Features
--------

* Convert GIS shapefiles to SVG paths at any size
* Get the SVG as JSON or an SVG file editable in Adobe Illustrator
* Use any PostGIS supported projection
* Calculate the centroids for each shape, useable in a proportional symbol map

Setup
-----

Make sure to have your computer [configured for GeoDjango](https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/). We also suggest using PostgreSQL with a [spatial database template](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/#spatialdb-template).

If you go that route, you can set up a database using:

    $ createdb -T template_postgis shp2svg

Then, create a virtualenv to store the codebase:

    $ virtualenv --no-site-packages shp2svg

Clone down the repo:

    $ cd shp2svg
    $ git clone git@github.com:datadesk/django-shp2svg.git project

And install the requirements:

    $ . bin/activate
    $ cd project
    $ pip install -r requirements.txt

Sync up the database (we're using South, though you're welcome to drop it locally) and create the cache table:

    $ python manage.py syncdb
    $ python manage.py migrate shp2svg
    $ python manage.py createcachetable my_cache_table

Finally, update your settings.py file with your database name and local settings. Start the local server:

    $ fab rs

You're good to go! Check out [http://localhost:8000](http://localhost:8000).