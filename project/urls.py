from shp2svg import views
from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView
admin.autodiscover()


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_shape/', views.upload_shapefile),
    url(r'^setup/', views.GenerateSVG.as_view()),
    url(r'^(?P<slug>[-\d\w]+)/$', views.shapefile_detail, name="shapefile detail"),
]