from shp2svg import views
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
admin.autodiscover()

sitemaps = {
    'home': views.Sitemap(['index',]),
    'shapefiles': views.ShapefileContainerSitemap,
}

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_shape/', views.upload_shapefile),
    url(r'^setup/', views.GenerateSVG.as_view()),
    # url(r'^robots\.txt$', direct_to_template, {
        # 'template': 'robots.txt', 'mimetype': 'text/plain'}),
    # url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        # 'sitemaps': sitemaps}),
    url(r'^(?P<slug>[-\d\w]+)/$', views.shapefile_detail, name="shapefile detail"),
)