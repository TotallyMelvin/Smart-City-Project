from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import RegistrationForm, ExtraInfoForm, EditProfileForm
from accounts.forms import MapForm, UserLoginForm
from django.views.generic import TemplateView
#to translate the user input into useable links for google
from accounts.codesnippets import get_google_url
from django.contrib.auth.forms import UserChangeForm

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
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/home/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def register(request):
    #if data is posted (from user submission) perform this
    if request.method =='POST':
        #form reads user input
        form = RegistrationForm(request.POST)
        #if the form contains valid data perform this
        if form.is_valid():
            #save information and redirect to specified location
            form.save()
            return redirect('/home/extraInfo')
    #if request method is 'get' generate empty form
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/register.html', args)

def extraInfo(request):
    #if data is posted (from user submission) perform this
    if request.method =='POST':
        #form reads user input
        form = ExtraInfoForm(request.POST)
        #if the form contains valid data perform this
        if form.is_valid():
            #save information and redirect to specified location
            form.save()
            return redirect('home/')
    #if request method is 'get' generate empty form
    else:
        form = ExtraInfoForm()
        args = {'form': form}
        return render(request, 'accounts/extrainfo.html', args)

class MapView(TemplateView): ## the maps page of the website

    map_au_link = "https://www.google.com/maps/embed/v1/search?q=australia&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"
    template_name = 'accounts/main.html'

    def get(self, request):
        form = MapForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = MapForm(request.POST)
        if form.is_valid():
            search_location = form.cleaned_data['location']
            search_data = form.cleaned_data['selected_options']

        ## update the google link
        search_link_string = get_google_url(search_location, search_data)

        self.map_au_link = search_link_string

        ## return to the UI
        args = {'form': form, 'map_link': self.map_au_link}
        return render(request, self.template_name, args)
