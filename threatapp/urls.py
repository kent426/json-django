from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/(?P<periodtype>[012])$', views.getmeta, name="getmeta"),
        ]
