from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile

# Create your views here.

def mode(request):
    return render(request, 'mode.html')

def give(request):
    pass

def get(request):
    pass