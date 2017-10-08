from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

#this creates a model for a user profile (if this is modified,
#makemigrations and migrate need to be run to update the model)

# class View(models.Model):
#     user_type = models.CharField(max_length=30, default='')
#
# class SiteUser(AbstractUser):
#     userType = models.ForeignKey(View, null=True, on_delete=models.SET_NULL)
#     def create_profile(sender, **kwargs):
#         if kwargs['created']:
#             user_profile = User.objects.create(userID=kwargs['instance'])
#
#     post_save.connect(create_profile, sender=User)

class UserProfileModel(models.Model):
    username = models.OneToOneField(User)
    userType = models.CharField(max_length=30, default='')
    phoneNumber = models.IntegerField(default=0)
    #USERNAME_FIELD = 'username'

# def __str__(self):
#     return self.username
def __unicode__(self):
        return self.username

    #this code associates the user that is being created with the user profile
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfileModel.objects.create(userID=kwargs['instance'])


## --- Jamie Added Stuff for Maps ---

class FeatureLocationModel(models.Model):
    ## This Model will hold all the locations that the admin users want the
    ## service to work for, such as 'brisbane', 'melbourne'
    
    locationId = models.CharField(max_length=50, default='') #what will search in google
    # because it's meant to be a small ID
    locationName = models.CharField(max_length=50, default='') #what will dispaly UI

    def __unicode__(self):
        return self.locationName ## added as placeholder because i dont know what
                                 ## it does

    
class userTypeAccessModel(models.Model):
    ## This Model will hold all the type of locations
    
    userType = models.CharField(max_length=10, default='') 
    accessableFeatures = models.CharField(max_length=100000, default='') ## a list
    ## with all the type of locations that the user can access

    def __unicode__(self):
        return self.userType ## added as placeholder because i dont know what
                                 ## it does
    





## xxx Jamie Added Stuff for Maps xxx
post_save.connect(create_profile, sender=UserProfileModel)
