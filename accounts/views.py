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
        edit_form_optional = EditProfileFormOptional(request.POST, instance=request.user)

        if edit_form.is_valid() and edit_form_optional.is_valid():
            edit_form.save()
            edit_form_optional.save()
            return redirect('/home/profile')

    else:
        edit_form = EditProfileForm(instance=request.user)
        edit_form_optional = EditProfileFormOptional(request.POST, instance=request.user)
        args = {'edit_form': edit_form, 'edit_form_optional': edit_form_optional}
        return render(request, 'accounts/edit_profile.html', args)

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

class MapView(TemplateView): ## the maps page of the website

    map_au_link = "https://www.google.com/maps/embed/v1/search?q=australia&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"
    template_name = 'accounts/main.html'

    def get(self, request):
        base_form = GeneralMapForm()
        tourist_form = TouristMapForm()
        student_form = StudentMapForm()
        businessman_form = BusinessmanMapForm()
        args = {'base_form': base_form, 'tourist_form' : tourist_form, 'student_form': student_form,
                'businessman_form': businessman_form}
        return render(request, self.template_name, args)

    def post(self, request):
        user_type = request.POST.get('active_user_type')
        
        if user_type == 'tourist':
            print('is tourist')
            tourist_form = TouristMapForm(request.POST)
            if tourist_form.is_valid():
                search_location = tourist_form.cleaned_data['location']
                search_data = tourist_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data)

            self.map_au_link = search_link_string

            ## return to the UI
            args = {'tourist_form': tourist_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

        elif user_type == 'student':
            print('is student')
            student_form = StudentMapForm(request.POST)
            if student_form.is_valid():
                search_location = student_form.cleaned_data['location']
                search_data = student_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data)

            self.map_au_link = search_link_string

            ## return to the UI
            args = {'student_form': student_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

        elif user_type == 'businessman':
            print('is businessman')
            businessman_form = BusinessmanMapForm(request.POST)
            if businessman_form.is_valid():
                search_location = businessman_form.cleaned_data['location']
                search_data = businessman_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data)

            self.map_au_link = search_link_string

            ## return to the UI
            args = {'businessman_form': businessman_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)


        else:
            base_form = GeneralMapForm(request.POST)
            if base_form.is_valid():
                search_location = base_form.cleaned_data['location']
                search_data = base_form.cleaned_data['selected_options']

            ## update the google link
            search_link_string = get_google_url(search_location, search_data)

            self.map_au_link = search_link_string

            ## return to the UI
            args = {'base_form': base_form, 'map_link': self.map_au_link}
            return render(request, self.template_name, args)

class BusinessView(TemplateView):## Jamie 

    main_template = "accounts/businessman.html"
    def get(self, request):
        location_form = LocationSelectForm()
        return render(request, self.main_template, {'location_form': location_form})

    def post(self, request):
        print(""" ------------------
                there has been a post request
                -------------------------""")
        location_form = LocationSelectForm(request.POST)
        if location_form.is_valid(): 
            search_location = location_form.cleaned_data['location']
        print(search_location)
        ## get the entries that relate to the city 
        all_entries = BusinessFeatureModel.objects.filter(associatedCity=search_location)
        print(all_entries)
       
        
        return render(request, self.main_template, {'location_form': location_form, 'all_entries': all_entries})

    


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
                ['ifb299g16.techteam@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'accounts/contact.html', {
        'form': form_class,
    })

## Jamie - add admin
def add_admin(request):
    form = AdminCreationForm(request.POST)
    args = {'form': form}
    return render(request, 'accounts/add_admin.html', args)

