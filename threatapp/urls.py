from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<periodtype>[012])$', views.index, name='index'),
        ]
