from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginFrom

# Create your views here.

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginFrom(data=request.POST)
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
        user_login_form = UserLoginFrom()
        context = {'form': user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse("Please use post or get method.")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")
