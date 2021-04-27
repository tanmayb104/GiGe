from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile

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
            print("authenticated")
            return render(request, 'welcome.html')
        else:
            print("Invalid Credentials")
            messages.info(request, 'Invalid Credentials')
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
        profile_pic = request.POST['profile_pic']

        if(password1==password2):
            if(User.objects.filter(username=username).exists()):
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif(Profile.objects.filter(phone_number=phone_number).exists()):
                messages.info(request, 'Phone Number Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.profile.phone_number = phone_number
                user.profile.profile_pic = profile_pic
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    else:
        return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):

    if request.user.is_authenticated:

        if (request.method == 'POST'):

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            profile_pic = request.POST['profile_pic']

            if(password1==password2):
                if(User.objects.filter(username=username).exists() and username!=request.user.username):
                    messages.info(request, 'Username Taken')
                    return redirect('profile')
                elif(User.objects.filter(email=email).exists() and email!=request.user.email):
                    messages.info(request, 'Email Taken')
                    return redirect('profile')
                elif(User.objects.filter(phone_number=phone_number).exists()):
                    messages.info(request, 'Phone Number Taken')
                    return redirect('profile')
                else:
                    user = User.objects.get(username = request.user.username)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.email = email
                    user.profile.phone_number = phone_number
                    user.profile.profile_pic = profile_pic
                    user.set_password(password1)
                    user.save()
                    print('user profile changed')
                    return redirect('profile')
            else:
                messages.info(request, 'Password not matching')
                return redirect('profile')


        else:
            user = User.objects.filter(username=request.user.username)
            profile={"user": user[0]}
            return render(request, 'profile.html', profile)
    else:
        return render(request, 'login.html')

