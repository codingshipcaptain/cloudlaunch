from django.conf.urls import url
from . import views #for app urls.py
#(?P<INPUTNAME>\d+) for filling in a number in URL


urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^wishes/new$', views.new_wish),
    url(r'^wishes/create$', views.create_wish),
    url(r'^wishes/(?P<wid>\d+)$', views.show_wish),
    url(r'^wishes/(?P<wid>\d+)/edit$', views.edit_wish),
    url(r'^wishes/(?P<wid>\d+)/update$', views.update_wish),
    url(r'^wishes/(?P<wid>\d+)/delete$', views.delete_wish),
    url(r'^wishes/(?P<wid>\d+)/like$', views.like_wish),
    url(r'^wishes/(?P<wid>\d+)/granted$', views.granted),
    url(r'^wishes/stats$', views.stats_page),
    url(r'^logout$', views.logout),
]
