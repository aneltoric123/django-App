import json
from datetime import date, timedelta

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from fitness.forms import ProfileForm, UserForm, PasswordChangeForm, WeightEntryForm
from fitness.models import UserProfile, WeightEntry


# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
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
        user_profile = UserProfile.objects.get(user=request.user)
        form = WeightEntryForm
        if request.method == 'POST':
            form = WeightEntryForm(request.POST)
            weight = request.POST.get('weight')
            if weight:
                user_profile.current_weight = weight
                user_profile.save()
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
            return redirect('home_page')
        weight_entries = WeightEntry.objects.filter(user=request.user).order_by('-date')[:30]
        return render(request,  'home.html',
                      {'user_profile':user_profile,
                       'form':form,
                       'weight_entries':weight_entries
                       })
@login_required
def profile_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'profile.html',{'user_profile':user_profile})
@login_required
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
    request.session.flush()
    return redirect('login')
@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.userprofile
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=user)
        profile_form = ProfileForm(request.POST, instance=user_profile)
        password_form = PasswordChangeForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            new_password = password_form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
                user.save()
            return redirect('profile')
    else:
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=user_profile)
            password_form = PasswordChangeForm()
    return render(request,'profile/update_account.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'password_form':password_form
    })

@login_required
def delete_weight_record(request,record_id):
    record = get_object_or_404(WeightEntry,id=record_id,user=request.user)
    record.delete()
    return redirect('home_page')


