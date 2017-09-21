from django.conf.urls import url, include
from . import views
from interactive_map.views import MapView


urlpatterns = [
    url(r'^$', MapView.as_view(), name='index'),
]
