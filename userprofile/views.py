from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm,ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("Account number or password is wrong!")
        else:
            return HttpResponse("Wrong form data!")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse("Please use post or get method.")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save()
            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("Form is wrong, please input again.")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("Please use GET or POST to get the data.")

@login_required(login_url='/userprofile/login/')
def user_delete(request,id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("No Authority!")
    else:
        return HttpResponse("Only accept POST request.")

@login_required(login_url='/userprofile/login/')
def profile_edit(request,id):
    user = User.objects.get(id=id)
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("You don't have authourity to edit the user information.")

        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect("userprofile:edit",id=id)
        else:
            return HttpResponse("Wrong Form!")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form':profile_form, 'profile':profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("Please use POST or GET method to get data.")
