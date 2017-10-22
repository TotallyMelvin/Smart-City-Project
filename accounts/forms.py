from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *

class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = FeedbackModel
        fields = ('feedback',)

    def save(self, commit=True):
        user = super(FeedbackForm, self).save(commit=False)
        user.feedback = self.cleaned_data['feedback']
        if commit:
            user.save()
        return user

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

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

##Password Reset
class getPasswordReset(forms.Form):
    Email = forms.EmailField(required = True)

class AdminCreationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password')

###############################
## Jamie Section Start
###############################

def return_locations():
    ## Creator: Jamie Kostaschuk
    ## Description: this returns a 'drop down ready' list of the added locations from
    ## the models.

    all_loc_list = [['', 'Select Location']]
    all_loc_data = FeatureLocationModel.objects.all().values() ## get data from the models
    for loc_entry in all_loc_data: ## for all the different locations
        pass_list = [[loc_entry.get('locationId'), loc_entry.get(
            'locationName')]] ##gathering the name to search for google and the name to display to UI
        all_loc_list = all_loc_list + pass_list ## pass into list
        ## for the form
    return all_loc_list


def get_user_type_features(user_type):
    ## Creator: Jamie Kostaschuk
    ## Description: this returns the type of locations each user type is allowed to search for
    ## in the map page as a list. the user tpye that is searched is based in the user_type input

    all_feature_list = [] ##base black items for the UI

    all_features = userTypeAccessModel.objects.filter(
        userType=user_type).values() ## get
    print(all_features)
    for feature_set in all_features: ## access the data in the list
        all_features = feature_set.get('accessableFeatures') #the strin containing all features separated by a ','
        split_ver = all_features.split(',')## split into individual (list format)
        for feature in split_ver: ## make form readable for UI
            entry = [[feature, feature]]

            all_feature_list = all_feature_list + entry ## add all to the UI
    return all_feature_list


class GeneralMapForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description:
    ## This is a TEMPLATE/BASE Class that is made without 'user types'
    ##      new classes for each user type should is made

    ## This sections shows the GUI and selection process to the user
    ## based on the selections from these aspects, the solution should
    ## then use the "get_google_url" method (interactive_map/views) to
    ## generate the embeded link to the google map and refresh the map
    ## page with the new link to display the mapo to the user

    ## LOCATIONS - database read
    locations = return_locations()
    print(locations)

    ## Get the features. "cityInfo" is the base usertype that all
    ## users have access to.
    general_features = get_user_type_features('cityInfo')
    print(general_features)

    ## make the GUI elements
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)

    selected_options = forms.MultipleChoiceField(widget=
                                                 forms.CheckboxSelectMultiple,
                                                 choices = general_features)


class TouristMapForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description: Same as the GeneralMapForm but with aditional user type
    ## features in the all_features list


    locations = return_locations()
    print(locations)

    ## extra user type specific list
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

class BusinessmanMapForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description: Same as the GeneralMapForm but with aditional user type
    ## features in the all_features list


    locations = return_locations()
    print(locations)

    ## extra user type specific list
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

class StudentMapForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description: Same as the GeneralMapForm but with aditional user type
    ## features in the all_features list
    locations = return_locations()
    print(locations)

    ## extra user type specific list
    general_features = get_user_type_features('cityInfo')
    user_specific_features = get_user_type_features('student')

    all_features = general_features + user_specific_features
    print(all_features)

    ## GENERAL CITY INFORMATION USER STORY
    location = forms.ChoiceField(label = "Choose location", initial = 'Choose location',
                                 choices = locations, required = True)

    selected_options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 choices = all_features)
class LocationSelectForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description:
    ## this is to select locations
    ## there will be a drop down with the different locations

    locations = return_locations()

    ## locations
    location = forms.ChoiceField(label = "Choose location",
                                 initial = 'Choose location',
                                 choices = locations,
                                 required = True)

class BusinessDataCreationForm(forms.Form):
    ## Creator: Jamie Kostaschuk
    ## Description:
    ## This will be a form that is used by admins to add data to the
    ## model "BusinessFeatureModel". Ideally, these form inputs should be generated
    ## based on the model's fields. but for now will be created using coded form aspects.
    ## if time permits, this should be updated to be based on the model rather than hard coded.

    ## get the locations
    possible_locations = return_locations()

    ##----  entries ---- ## # every option should be required besides the map
    ## businessType: character entry, should hopfully be one word describing the org
    businessType = forms.CharField(required=True)

    ## associatedCity: Cities that can be related, should be taken from the "feature
    ## Location Model" to force the user to add only from the approved cities and
    ## stops human error
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

    ## boolian checkbox ## to know whether or not to display a map to the users when
    ## they view the data
    useMap = forms.BooleanField(
        label='useMap',
        required=False,
        initial=False
     )

    ## should be a character input for the user, which is
    ## then combined with the selected location to create the embed link, which can
    ## be saved directly into the database
    optionalMapSearchInput = forms.CharField(required=False)
