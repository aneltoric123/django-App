import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from fitness.forms import ProfileForm
from fitness.models import UserProfile


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if not profile.is_complete():
                return redirect('complete_profile')
    return render(request,'login.html',{'message': 'Welcome to MFit!'})



@login_required
def complete_profile(request):
    profile,created = UserProfile.objects.get_or_create(user = request.user)
    if profile.is_complete():
        return redirect('home_page')
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = ProfileForm(instance=profile)

    return render(request,'complete_profile.html',{'form':form})
@login_required
def home_page(request):
    return render(request,  'home.html')

def profile_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'profile.html',{'user_profile':user_profile})

def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request,"Account successfully deleted!")
        return redirect('login')
    return render(request,'profile/delete_account.html')

def register_page(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            message = "Password don't match!"
        elif User.objects.filter(username=username).exists():
            message = "Username already in use by another user!"
        elif User.objects.filter(email = email).exists():
            message = "Email already registered!"
        else:
            User.objects.create_user(username=username,email=email,password=pass1)
            return redirect('login')

    return render(request,'register.html',{'message':message})


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')
def edit_profile(request):
    user_profile = UserProfile.objects.get(user = request.user)
    return render(request,'profile/update_account.html',{'user_profile':user_profile})
