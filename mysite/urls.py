from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^accounts/',include('allauth.urls')),
    url(r'^$', include('accounts.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('accounts.urls')),
]
