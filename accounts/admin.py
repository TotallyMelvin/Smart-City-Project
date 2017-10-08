from django.contrib import admin
from accounts.models import UserProfile, userTypeAccessModel, FeatureLocationModel
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(FeatureLocationModel)
admin.site.register(userTypeAccessModel)
