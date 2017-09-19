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

post_save.connect(create_profile, sender=UserProfileModel)
