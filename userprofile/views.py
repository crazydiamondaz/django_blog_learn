from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm

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
