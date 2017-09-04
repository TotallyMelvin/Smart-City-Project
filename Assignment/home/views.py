from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'personal/index.html')

def login(request):
    return render(request, 'personal/login.html')

def register(request):
    return render(request, 'personal/register.html')

def map(request):
    return render(request, 'personal/map.html')

def profile(request):
    return render(request, 'personal/profile.html')

def admin(request):
    return render(request, 'personal/admin.html')
