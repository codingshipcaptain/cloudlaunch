from django.conf.urls import url
from . import views
#(?P<INPUTNAME>\d+) for filling in a number in URL


urlpatterns = [
    url(r'^$', views.main), #This one for app urls.py
    url(r'^main$', views.main), #This one for app urls.py
    url(r'^vehicles/new$', views.new),
    url(r'^vehicles/create$', views.create),
    url(r'^vehicles/(?P<vic>\d+)$', views.show),
    url(r'^vehicles/(?P<vic>\d+)/edit$', views.edit),
    url(r'^vehicles/(?P<vic>\d+)/update$', views.update),
    url(r'^vehicles/(?P<vic>\d+)/fuel$', views.fuel),
    url(r'^vehicles/(?P<vic>\d+)/fuel/add$', views.add_fuel),
    url(r'^vehicles/(?P<vic>\d+)/fuel/create$', views.create_fuel),
    url(r'^vehicles/(?P<vic>\d+)/fuel/(?P<fid>\d+)/edit$', views.edit_fuel),
    url(r'^vehicles/(?P<vic>\d+)/fuel/(?P<fid>\d+)/update$', views.update_fuel),
    url(r'^vehicles/(?P<vic>\d+)/fuel/(?P<fid>\d+)/delete$', views.delete_fuel),
    url(r'^vehicles/(?P<vic>\d+)/maint$', views.maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/add$', views.add_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/create$', views.create_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/(?P<mid>\d+)/edit$', views.edit_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/(?P<mid>\d+)/update$', views.update_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/(?P<mid>\d+)/delete$', views.delete_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/search$', views.search_maint),
    url(r'^vehicles/(?P<vic>\d+)/maint/result/(?P<search>\w)$', views.search_result),
]
