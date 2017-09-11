from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#this creates a model for a user profile (if this is modified,
#makemigrations and migrate need to be run to update the model)
class UserProfile(models.Model):
    userID = models.OneToOneField(User)
    #userType needs to be a drop down box
    userType = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.IntegerField(default=0)

#this code associates the user that is being created with the user profile
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(userID=kwargs['instance'])

post_save.connect(create_profile, sender=User)
