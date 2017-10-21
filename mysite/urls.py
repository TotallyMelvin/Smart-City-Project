from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('accounts.urls')),
    ## code to redirect the user if the weblink is unknown, ensure this is the last page
    url('', home, name='home'),  
]
