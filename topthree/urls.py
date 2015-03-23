from django.conf.urls import patterns, url

from topthree import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'^listings/(?P<category1>\d+)/(?P<category2>\d+)/(?P<category3>\d+)/(?P<page>\d+)/$', views.listings, name='listings'),
)

