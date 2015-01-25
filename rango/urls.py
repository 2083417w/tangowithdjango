from django.conf.urls import patterns,url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'about/',views.about, name='index'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)
