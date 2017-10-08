from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

#this creates a model for a user profile (if this is modified,
#makemigrations and migrate need to be run to update the model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, blank=True, default='')
    street_number = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=30, blank=True, default='')
    suburb = models.CharField(max_length=30, blank=True, default='')
    postcode = models.IntegerField(blank=True, null=True)

def __unicode__(self):
        return self.username

class FeatureLocationModel(models.Model): ## Jamie
    ## This Model will hold all the locations that the admin users want the
    ## service to work for, such as 'brisbane', 'melbourne'
    locationId = models.CharField(max_length=50, default='') #what will search in google
    # because it's meant to be a small ID
    locationName = models.CharField(max_length=50, default='') #what will dispaly UI
    def __unicode__(self):
        return self.locationName ## added as placeholder because i dont know what
                                 ## it does
class userTypeAccessModel(models.Model): ## Jamie
    ## This Model will hold all the type of locations
    userType = models.CharField(max_length=10, default='')
    accessableFeatures = models.CharField(max_length=100000, default='') ## a list
    ## with all the type of locations that the user can access
    def __unicode__(self):
        return self.userType ## added as placeholder because i dont know what
                                 ## it does
