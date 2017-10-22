from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from accounts.forms import *
from django.views.generic import TemplateView
#to translate the user input into useable links for google
from accounts.codesnippets import get_google_url
#contact
from accounts.forms import ContactForm
from accounts.forms import getPasswordReset
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

def home(request):
    form = UserLoginForm(request.POST)
    args = {'form': form}
    return render(request, 'accounts/home.html', args)

def login(request):
    return render(request, 'accounts/login.html')

def profile(request):
    return render(request, 'accounts/profile.html')

def edit_profile(request):
    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return redirect('/home/profile')

    else:
        edit_form = EditProfileForm(instance=request.user)
        # edit_form_optional = EditProfileFormOptional(instance=request.user)
        args = {'edit_form': edit_form}
        # args = {'edit_form': edit_form, 'edit_form_optional': edit_form_optional}
        return render(request, 'accounts/edit_profile.html', args)

def edit_profile2(request):
    # if request.method == 'POST':
    #     edit_form2 = EditProfileFormOptional(request.POST, instance=request.user.userprofile)
	#
    #     if edit_form2.is_valid():
    #         edit_form2.save()
    #         return redirect('/home/profile')
    # else:
    #     edit_form2 = EditProfileFormOptional(instance=request.user.userprofile)
    #     # edit_form_optional = EditProfileFormOptional(instance=request.user)
    #     args = {'edit_form2': edit_form2}
    #     # args = {'edit_form': edit_form, 'edit_form_optional': edit_form_optional}
    #     return render(request, 'accounts/edit_profile.html', args)
	return render(request, 'accounts/edit_profile2.html')

def feedback(request):

    #if data is posted (from user submission) perform this
	if request.method =='POST':
		feedback_form = FeedbackForm(request.POST)
		if feedback_form.is_valid():
			feedback_form.save()
			return redirect('/home/')
	else:
		feedback_form = FeedbackForm()
		args = {'feedback_form': feedback_form}
		return render(request, 'accounts/feedback.html', args)

def add_admin(request):
    if request.method =='POST':
        form = AdminCreationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                          username=form.cleaned_data['username'],
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'],
                          email=form.cleaned_data['email'],
                          #password=user_form.cleaned_data['password'],)
                          password=form.cleaned_data.get('password'),)
            user.is_staff = True
            user.save()
            return redirect('/home/addadminsuccess')
    else:
        form = AdminCreationForm()
        args = {'form': form}
        return render(request, 'accounts/add_admin.html', args)

def add_admin_success(request):
    return render(request, 'accounts/add_admin_success.html')

def register(request):

    registered = False
    #if data is posted (from user submission) perform this
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
                          username=user_form.cleaned_data['username'],
                          first_name=user_form.cleaned_data['first_name'],
                          last_name=user_form.cleaned_data['last_name'],
                          email=user_form.cleaned_data['email'],
                          #password=user_form.cleaned_data['password'],)
                          password=user_form.cleaned_data.get('password'),)
            # user = user_form.save()
            # user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print('error') # user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
        'accounts/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered':registered})

###############################
## Jamie Section Start
###############################

class MapView(TemplateView):
    ## Creator: Jamie Kostaschuk
    ## Description: This is the 'map' view for the webpage. it links to the different map forms fro mthe forms.py file,
    ## and depending on the user type of the active user, displays the accociated form for them

    ## the base map link that can be used. It will just display australia on the map. will be overwritten to show more
    #3 specifics based on the forms and user
    map_au_link = "https://www.google.com/maps/embed/v1/search?q=australia&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"

    template_name = 'accounts/main.html' ## linked template that is used.

    def get(self, request):
        ## create all of the possible map input forms to pass to the template - which can them decide their user type
        ## and display the correct form to the user

        base_form = GeneralMapForm()
        tourist_form = TouristMapForm()
        student_form = StudentMapForm()
        businessman_form = BusinessmanMapForm()
        args = {'base_form': base_form, 'tourist_form' : tourist_form, 'student_form': student_form,
                'businessman_form': businessman_form}

        return render(request, self.template_name, args)

    def post(self, request):
        user_type = request.POST.get('active_user_type') ## this is a hidden field in the template that can retrieved
        ## when the user sends a POST request, now the python file can use their user type to display different
        ## information, pick which form to use, etc.

        if user_type == 'tourist':
            tourist_form = TouristMapForm(request.POST)
            if tourist_form.is_valid():
                search_location = tourist_form.cleaned_data['location']
                search_data = tourist_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data, 0)

            self.map_au_link = search_link_string

            ## return to the UI with the map
            args = {'tourist_form': tourist_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

        elif user_type == 'student':
            student_form = StudentMapForm(request.POST)
            if student_form.is_valid():
                search_location = student_form.cleaned_data['location']
                search_data = student_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data, 0)

            self.map_au_link = search_link_string

            ## return to the UI with the map link
            args = {'student_form': student_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

        elif user_type == 'businessman':
            businessman_form = BusinessmanMapForm(request.POST)
            if businessman_form.is_valid():
                search_location = businessman_form.cleaned_data['location']
                search_data = businessman_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data, 0)

            self.map_au_link = search_link_string

            ## return to the UI with the map link
            args = {'businessman_form': businessman_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

        else: # In the case that a admin is viewing the page, or if a error has occured
            base_form = GeneralMapForm(request.POST)
            if base_form.is_valid(): ## use the base form
                search_location = base_form.cleaned_data['location']
                search_data = base_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data, 0)

            self.map_au_link = search_link_string

            ## return to the UI
            args = {'base_form': base_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

class BusinessView(TemplateView):
    ## Creator: Jamie Kostaschuk
    ## Description: This is the view that allows users to see the 'organisational data'
    ## The view makes use of a form which asks for the user to select a location,
    ## based on that it returns all organisational data entries about that city from
    ## the model

    main_template = "accounts/businessman.html" ## the template that will be used

    def get(self, request):
        location_form = LocationSelectForm() ## pass the form to be displayed to the user
        return render(request, self.main_template, {'location_form': location_form})

    def post(self, request):
        location_form = LocationSelectForm(request.POST)

        if location_form.is_valid():
            search_location = location_form.cleaned_data['location']  ## get the location that they
        ## selected

        ## get the entries that relate to the city
        all_entries = BusinessFeatureModel.objects.filter(associatedCity=search_location)

        args = {'location_form': location_form, 'all_entries': all_entries} ## Pass the
        ## entries to the tempalte to display to the user
        return render(request, self.main_template, args)

class AddBusinessDataView(TemplateView):
    ## Creator: Jamie Kostaschuk
    ## Description: This is a view that is designed to allow users (admins) to create data for
    ## the business organisational data model. This form is designed to allow for the admins
    ## to add data. however the important reason for this view is to autofill the map
    ## link field in the model

    main_template = "accounts/businessmandatacreation.html" ## the template that will be used


    def get(self, request):
        ## get and display the form
        business_data_creation_form = BusinessDataCreationForm()
        args = {'business_data_creation_form': business_data_creation_form}
        return render(request, self.main_template, args)

    def post(self, request):
        business_data_creation_form = BusinessDataCreationForm(request.POST)
        if business_data_creation_form.is_valid():

            ## Create Map link based in the city of the data and the map input the user wanted
            search_link_string = get_google_url(business_data_creation_form.cleaned_data['associatedCity'],
                                                business_data_creation_form.cleaned_data['optionalMapSearchInput'], 1)

            ## Create the entry in the model
            new_data = BusinessFeatureModel()

            ## fill out the new entry's data fields
            new_data.businessType = business_data_creation_form.cleaned_data['businessType']
            new_data.associatedCity = business_data_creation_form.cleaned_data['associatedCity']
            new_data.cityOrganisationalData = business_data_creation_form.cleaned_data['cityOrganisationalData']
            new_data.stateAnalysis = business_data_creation_form.cleaned_data['stateAnalysis']
            new_data.furtherReadings = business_data_creation_form.cleaned_data['furtherReadings']
            new_data.useMap = business_data_creation_form.cleaned_data['useMap']
            new_data.optionalMapSearchInput = search_link_string ## use the map link that was created not the
            ## user's input

            ## Save the data in the model
            new_data.save()

        ## return a empty form to the user so they can add more data in they want
        business_data_creation_form = BusinessDataCreationForm()
        args = {'business_data_creation_form': business_data_creation_form}
        return render(request, self.main_template, args)

class AdminPageView(TemplateView):
    ## Creator: Jamie Kostaschuk
    ## Description: This is a view that displays the admin page to the user
    main_template = "accounts/admin_link_page.html" ## the template that will be used
    def get(self, request):
        return render(request, self.main_template)

###############################
## Jamie Section End
###############################


def help(request):
    return render(request, 'accounts/help.html')

# add to your views
def contact(request):
    form_class = ContactForm

   # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'accounts/contact.html', {
        'form': form_class,
    })

#Password Recovery Views
def password_reset(request):
    form = getPasswordReset(request.POST)
    return render(request, 'accounts/password_reset_form.html')
