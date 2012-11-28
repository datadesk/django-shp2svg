from shp2svg import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_shape/', views.upload_shapefile),
    url(r'^setup/', views.generate_svg),
    url(r'^(?P<slug>[-\d\w]+)/$', views.shape_collection),
)
