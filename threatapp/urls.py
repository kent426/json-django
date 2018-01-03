from django.conf.urls import url

from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^(?P<periodtype>[012])$', views.index, name='index'),
        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
