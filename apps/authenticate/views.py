from django.shortcuts import render, redirect
from .forms import UserForm,UserProfileInfoForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        nextPage = request.POST.get('next')
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user.is_active:
                login(request,user)
                request.session['myUserName'] = user.username
                request.session['myProfilePicture'] = user.userprofileinfo.profile_image.url
                if nextPage:
                    return redirect(nextPage)
                else:
                    return redirect("authenticate:index")
            else:
                return HttpResponse("Your account was inactive.")
    else:
        form = LoginForm
    return render(request, 'login.html', {'form':form})

@login_required
def validate_auth(request):
    return render(request, 'validate.html', {'message':"Solo los verdaderos profetas autenticados veran este mensaje !"})

@login_required
def export_pdf(request):
    pass

@login_required
def user_logout(request):
    logout(request)
    return redirect("authenticate:index")

    