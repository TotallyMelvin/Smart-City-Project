from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout
from accounts.views import MapView

urlpatterns = [
    url(r'^$', views.home),
    url(r'^accounts/home/$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^map/$', MapView.as_view(), name='map')
    #url(r'^maps/$', MapView.as_view(), name='map')
]
