from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    userTypeOptions = (('student', 'Student'),
                       ('businessmen', 'Businessmen'),
                       ('tourist', 'Tourist'))
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=userTypeOptions)
    phone_number = forms.CharField(max_length=30, required=False)
    street_number = forms.IntegerField(required=False)
    street_name = forms.CharField(max_length=30, required=False)
    suburb = forms.CharField(max_length=30, required=False)
    postcode = forms.IntegerField(required=False)
    class Meta:
        model = UserProfile
        fields = ('user_type', 'phone_number', 'street_number', 'street_name', 'suburb', 'postcode')

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class EditProfileFormOptional(UserChangeForm):
    # phone_number = forms.CharField(max_length=30, required=False)
    # street_number = forms.IntegerField(required=False)
    # street_name = forms.CharField(max_length=30, required=False)
    # suburb = forms.CharField(max_length=30, required=False)
    # postcode = forms.IntegerField(required=False)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'street_number', 'street_name', 'suburb', 'postcode')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    userTypeOptions = (('student', 'Student'),
                       ('businessmen', 'Businessmen'),
                       ('tourist', 'Tourist'))

    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=userTypeOptions)

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        'user_type'
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


## Jamie



def return_locations():
    all_loc_list = [['', 'Select Location']] 
    all_loc_data = FeatureLocationModel.objects.all().values() ## get
    ## data from the models
    for loc_entry in all_loc_data: ## for all the different locations
        pass_list = [[loc_entry.get('locationId'), loc_entry.get(
            'locationName')]] ##gathering the name to search for
        ## google and the name to display to UI
        all_loc_list = all_loc_list + pass_list ## pass into list
        ## for the form
    return all_loc_list
    

def get_user_type_features(user_type):
    all_feature_list = [] ##base black items for the UI

    all_features = userTypeAccessModel.objects.filter(
        userType=user_type).values() ## get
    print(all_features)
    for feature_set in all_features: ## there should only be one
        
        ## just doing this to access it
        all_features = feature_set.get('accessableFeatures') #the string
        ## containing all features separated by a ,
        split_ver = all_features.split(',')## split into individual (list format)
        for feature in split_ver: ## make form readable for UI
            entry = [[feature, feature]]

            all_feature_list = all_feature_list + entry ## add all to the UI
    return all_feature_list


class GeneralMapForm(forms.Form): ## Jamie
    ## This is a TEMPLATE Class that is made without 'user types'
    ##      new classes for each user type should be made!
    
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
    locations = return_locations()
    print(locations)
    
    general_features = get_user_type_features('cityInfo')
    print(general_features)
    
    ## GENERAL CITY INFORMATION USER STORY
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)
    
    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = general_features)

class TouristMapForm(forms.Form): ## Jamie

    locations = return_locations()
    print(locations)
    
    general_features = get_user_type_features('cityInfo')
    user_specific_features = get_user_type_features('tourist')

    all_features = general_features + user_specific_features
    print(all_features)
    
    ## GENERAL CITY INFORMATION USER STORY
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)
    
    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = all_features)

class BusinessmanMapForm(forms.Form): ## Jamie

    locations = return_locations()
    print(locations)
    
    general_features = get_user_type_features('cityInfo')
    user_specific_features = get_user_type_features('businessman')

    all_features = general_features + user_specific_features
    print(all_features)
    
    ## GENERAL CITY INFORMATION USER STORY
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)
    
    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = all_features)
    
class StudentMapForm(forms.Form): ## Jamie

    locations = return_locations()
    print(locations)
    
    general_features = get_user_type_features('cityInfo')
    user_specific_features = get_user_type_features('student')

    all_features = general_features + user_specific_features
    print(all_features)
    
    ## GENERAL CITY INFORMATION USER STORY
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)
    
    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = all_features)


class LocationSelectForm(forms.Form): ## Jamie
    ## this is the businessman specific features
    ## there will be a drop down with the different locations, and
    ## a serch button (button will be on the template side)
    ## once the button is pressed, it returns the different
    ## organisation types to the user,. which they have then click
    ## to view the specifics of each
    
    locations = return_locations()

    
    ## locations
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)

class BusinessDataCreationForm(forms.Form):
    ## This will be a form that is used by admins to add data to the
    ## model "BusinessFeatureModel". Ideally, these form inputs should be generated
    ## based on the model's fields. but for now will be created using form aspects.
    ## if time permits, this should be updated.

    ## get the locations
    possible_locations = return_locations()
    
    ##----  entries ---- ## # every option should be required besides the map
    ## businessType: character entry, should hopfully be one word describing the org
    businessType = forms.CharField(required=True)

    ## associatedCity: Cities that can be related, should be taken from the "feature
    ## Location Model" for consistancy standards 
    associatedCity = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = possible_locations,
                                 required = True)

     ## cityOrganisationalData: text input for the data
    cityOrganisationalData = forms.CharField(required=True, widget=forms.Textarea)

    ##stateAnalysis: professional analysis 
    stateAnalysis = forms.CharField(required=True, widget=forms.Textarea)

    ## further references
    furtherReadings = forms.CharField(required=True, widget=forms.Textarea)

    ## boolian checkbox
    
    useMap = forms.BooleanField(
        label='myLabel', 
        required=False,
        initial=False
     )


    ## should be a character input for the user, which is
    ## then combined with the selected location to create the embed link, which can
    ## be saved directly into the database
    optionalMapSearchInput = forms.CharField(required=False)

## jamie end
    
class AdminCreationForm(forms.ModelForm): ## Jamie  ## draft form for the add admin page

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password')
		



