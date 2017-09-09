##Import files
from django.conf.urls import url
from home import views

##Patterns
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'templates/personal/login.html$', views.login, name = 'login'),
    url(r'templates/personal/register.html$', views.register, name = 'register'),
    url(r'templates/personal/map.html$', views.map, name = 'map'),
    url(r'templates/personal/profile.html$', views.profile, name = 'profile'),
    url(r'templates/personal/admin.html$', views.admin, name = 'admin'),
    url(r'templates/personal/index.html$', views.index, name = 'home'),
    ]
