from django.contrib import admin
from accounts.models import UserProfileModel
# Register your models here.

admin.site.register(UserProfileModel)
admin.site.register(FeatureLocationModel)
admin.site.register(userTypeAccessModel)
