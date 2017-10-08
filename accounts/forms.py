from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *


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

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    

## --- jamie --- 

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


    ## LOCATIONS - database read
    all_loc_list = [['', 'Select City']] ##base items for the UI
    all_loc_data = FeatureLocationModel.objects.all().values() ## get
    ## data from the models
    for loc_entry in all_loc_data: ## for all the different locations
        pass_list = [[loc_entry.get('locationId'), loc_entry.get(
            'locationName')]] ##gathering the name to search for
        ## google and the name to display to UI
        all_loc_list = all_loc_list + pass_list ## pass into list
        ## for the form
        
    print(all_loc_list)        

    ## GENERAL - database read
    ##      get general options for all users (in model: cityInfo

            ## example of hard-coded:
                    #general_options = (
                        #("park", "Parks"),
                        #("zoo", "Zoos"),
                        #("tourist attractions", "Tourist Attractions"),
                        #("mall", "Malls"),
                        #("museum", "Museums"),
                        #("restaurant", "Restaurants")
                        #)
            ##
   
    all_feature_list = [] ##base black items for the UI
    
    all_general_features = userTypeAccessModel.objects.filter(
        userType='cityInfo').values() ## get
    print(all_general_features)
    
    for feature_set in all_general_features: ## there should only be one
        ## just doing this to access it
        all_general = feature_set.get('accessableFeatures') #the string
        ## containing all features separated by a ,
        print(all_general) ## test 
        split_ver = all_general.split(',')## split into individual (list format)
        for feature in split_ver: ## make form readable for UI
            entry = [[feature, feature]]
            
            all_feature_list = all_feature_list + entry ## add all to the UI
    print(all_feature_list) ## test
        
    ## GENERAL CITY INFORMATION USER STORY

    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = all_loc_list,
                                 required = True)

    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = all_feature_list)
##    ## USER SPECIFIC
##    #test_name = [['test', 'test']]
##    
##    test_name = [[User.username, User.username]]
##        
##
##    test_read_data = forms.MultipleChoiceField(widget=
##                                                 forms.CheckboxSelectMultiple,
##                                                 choices = test_name)
##    
##    


## xxx jamie xxx


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
