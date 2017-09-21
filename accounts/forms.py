from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserProfileModel

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class ExtraInfoForm(forms.Form):
    userTypeOptions = (('student', 'Student'),
                       ('businessmen', 'Businessmen'),
                       ('tourist', 'Tourist'))

    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=userTypeOptions)

    class Meta:
        model = UserProfileModel
        fields = (
            'username',
            'user_type',
            'phoneNumber'
        )

    def save(self, commit=True):
        user = super(ExtraInfoForm, self).save(commit=False)
        user.user_type = self.cleaned_data['user_type']

        if commit:
            user.save()

        return user

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class MapForm(forms.Form):
    ## This sections shows the GUI and selection process to the user
    ## based on the selections from these aspects, the solution should
    ## then use the "get_google_url" method (interactive_map/views) to
    ## generate the embeded link to the google map and refresh the map
    ## html insert with the new link!

    ## the lists below that have the city_locaitons and general_options
    ## should, in the final release, be connected to the db so that the
    ## admin can edit the selected cities/general options.

    ## in next strints, this GUI should be expanded so that users can
    ## pick from 'student', 'tourist', etc and get more options (this,
    ## as well, should be connected to the database!


    ## LOCATIONS
    city_locations = (('', 'Select City'),
                      ('brisbane', 'Brisbane'))

    ## GENERAL CITY INFORMATION USER STORY
    general_options = (
        ("park", "Parks"),
        ("zoo", "Zoos"),
        ("tourist attractions", "Tourist Attractions"),
        ("mall", "Malls"),
        ("museum", "Museums"),
        ("restaurant", "Restaurants")
        )

    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Brisbane',
                                 choices = city_locations,
                                 required = True)

    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = general_options)
##from django import forms
##from django.contrib.auth.models import User
##from django.contrib.auth.forms import UserCreationForm
##
##class UserLoginForm(forms.Form):
##    username = forms.CharField()
##    password = forms.CharField(widget=forms.PasswordInput)
##
##class RegistrationForm(UserCreationForm):
##    email = forms.EmailField(required=True)
##
##    class Meta:
##        model = User
##        fields = (
##        'username',
##        'first_name',
##        'last_name',
##        'email',
##        'password1',
##        'password2'
##        )
##
##    def save(self, commit=True):
##        user = super(RegistrationForm, self).save(commit=False)
##        user.first_name = self.cleaned_data['first_name']
##        user.last_name = self.cleaned_data['last_name']
##        user.email = self.cleaned_data['email']
##
##        if commit:
##            user.save()
##
##        return user
##
##class MapForm(forms.Form):
##    ## This sections shows the GUI and selection process to the user
##    ## based on the selections from these aspects, the solution should
##    ## then use the "get_google_url" method (interactive_map/views) to
##    ## generate the embeded link to the google map and refresh the map
##    ## html insert with the new link!
##
##    ## the lists below that have the city_locaitons and general_options
##    ## should, in the final release, be connected to the db so that the
##    ## admin can edit the selected cities/general options.
##
##    ## in next strints, this GUI should be expanded so that users can
##    ## pick from 'student', 'tourist', etc and get more options (this,
##    ## as well, should be connected to the database!
##
##
##    ## LOCATIONS
##    city_locations = (('', 'Select City'),
##                      ('brisbane', 'Brisbane'))
##
##    ## GENERAL CITY INFORMATION USER STORY
##    general_options = (
##        ("park", "Parks"),
##        ("zoo", "Zoos"),
##        ("tourist attractions", "Tourist Attractions"),
##        ("mall", "Malls"),
##        ("museum", "Museums"),
##        ("restaurant", "Restaurants")
##        )
##
##    location = forms.ChoiceField(label = "Choose location",
##                                 initial = 'Brisbane',
##                                 choices = city_locations,
##                                 required = True)
##
##    selected_options = forms.MultipleChoiceField(widget=
##                                                 forms.CheckboxSelectMultiple,
##                                                 choices = general_options)
