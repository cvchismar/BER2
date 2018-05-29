#APP LEVEL URLS

from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^display$', views.display, name="display"),
    url(r'^login$', views.login),
    url(r'^add_session$', views.add_session),
    url(r'^create$', views.create),
    url(r'^join/(?P<lecture_id>\d+)', views.join, name="join"),
    url(r'^info/(?P<lecture_id>\d+)', views.info, name="info"),
    url(r'^billing$',views.billing),
    url(r'^logout$', views.logout, name="logout"),
]