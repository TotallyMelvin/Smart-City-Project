from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView 
from django.contrib.auth.views import login, logout
from accounts.models import BusinessFeatureModel
from accounts.views import MapView, BusinessView, AddBusinessDataView, AdminPageView
#Import views as auth_views
from django.contrib.auth import views as auth_views

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
    url(r'^help/password_reset_form/$', views.password_reset, name='password_reset_form'),
    url(r'^addadmin/$', views.add_admin, name='add_admin'),
    url(r'^business_feature/$', BusinessView.as_view(), name='business'),
    url(r'^business_feature/(?P<pk>\d+)$', DetailView.as_view(model = BusinessFeatureModel,
                                                     template_name ='accounts/businessmanentry.html')),
    url(r'^admin/create_business_data/$', AddBusinessDataView.as_view(), name='adminCreateData'),
    url(r'^admin/admin_page/$', AdminPageView.as_view(), name='admin_page'),
    #Email Views
    url(r'^password_reset/$', auth_views.password_reset, name = 'password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name = 'password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)_(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html'}),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}),
    url(r'^', include('django.contrib.auth.urls')), #This adds all other ones that are reliant on others
     
]
