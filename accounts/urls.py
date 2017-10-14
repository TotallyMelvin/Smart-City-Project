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
    url(r'^map/$', MapView.as_view(), name='map'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^help/$', views.help, name='help'),
    url(r'^help/contact/$', views.contact, name='contact'),
    url(r'^help/password_recovery/$', views.password_recovery, name='password_recovery'),
    url(r'^addadmin/$', views.add_admin, name='add_admin'),
]
