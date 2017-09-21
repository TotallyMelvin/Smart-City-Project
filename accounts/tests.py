from django.test import TestCase
from django.contrib import *
from django.test import *
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.auth.base_user import *

# Create your tests here.

class loginTest(TestCase):

    def loginAnon(self):
        #Determine if self (client) is not logged in
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

    def loginTrue(self):
        #Determine is user is logged in
        user = User.objects.create_user('ASDF', email=None, password='Password.1')
        c = Client()
        self.assertTrue(c.login(username = user.username, password = 'Password.1'))

    def loginFalse(self):
        #Determine is user is logged in incorrectly
        user = User.objects.create_user('ASDF', email=None, password='Password.1')
        c = Client()
        self.assertFalse(c.login(username = user.username, password = 'Passwrd.1'))

class registerTest(TestCase):

    def register(self):
        #Create user object
        user = User.objects.create_user('ASDF', email = None, password = 'Password.1')
        c = Client()
        #If logs in successful, that means register is successful
        self.assertTrue(c.login(username = user.username, password = 'Password.1'))
