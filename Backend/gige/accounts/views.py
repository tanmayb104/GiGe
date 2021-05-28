from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile
from store.views import get
from django.contrib.auth.decorators import login_required

# Create your views here.

def welcome(request):
    return render(request, 'home.html')


def login(request):

    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('get')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')


    else:
        return render(request, 'login.html')

def register(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        _, file = request.FILES.popitem()
        file = file[0]
        location = request.POST['loc']

        if(password1==password2):
            if(User.objects.filter(username=username).exists()):
                messages.error(request, 'Username Taken')
                return redirect('register')
            elif(User.objects.filter(email=email).exists()):
                messages.error(request, 'Email Taken')
                return redirect('register')
            elif(Profile.objects.filter(phone_number=phone_number).exists()):
                messages.error(request, 'Phone Number Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.profile.phone_number = phone_number
                user.profile.profile_pic = file
                user.profile.location = location
                user.save()
                messages.success(request, 'Registered successfully')
                return redirect('login')
        else:
            messages.error(request, 'Password not matching')
            return redirect('register')

    else:
        return render(request, 'signup.html')


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully')
    return render(request, 'home.html')


@login_required
def profile(request):

    if (request.method == 'POST'):

        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        location = request.POST['loc']

        if(User.objects.filter(username=username).exists() and username!=request.user.username):
            messages.error(request, 'Username Taken')
            return redirect('profile')
        elif(User.objects.filter(email=email).exists() and email!=request.user.email):
            messages.error(request, 'Email Taken')
            return redirect('profile')
        else:
            
            user = User.objects.get(username = request.user.username)
            user.username = username
            user.email = email
            user.profile.phone_number = phone_number
            if(len(request.FILES)):
                _, file = request.FILES.popitem()
                file = file[0]
                user.profile.profile_pic = file
            user.profile.location = location
            user.save()
            messages.success(request, 'Profile edited successfully')
            return redirect('profile')


    else:
        user = User.objects.filter(username=request.user.username)
        profile={"user": user[0]}
        return render(request, 'profile.html', profile)

