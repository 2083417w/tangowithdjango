from django.conf.urls import patterns,url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$',views.about, name='index'),
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
<<<<<<< HEAD
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^restricted/$', views.restricted, name='restricted'),
                       url(r'^logout/$', views.user_logout, name='logout'),)
=======
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)
>>>>>>> 00ce1efe6b75c907b9127012b28d62cf4445a70c
