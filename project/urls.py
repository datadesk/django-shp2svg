from shp2svg import views
from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_shape/', views.upload_shapefile),
    url(r'^setup/(?P<slug>[-\d\w]+)/$', views.shape_setup),
    
    # url(r'^(?P<slug>[-\d\w]+)/$', views.shape_collection),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
