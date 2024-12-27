from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(UserCreationForm):
    # password = forms.CharField()
    # password2 = forms.CharField()
    email = forms.EmailField(label = "Email")
    class Meta:
        model = User
        fields = ('username', 'email',)

    # def clean_password2(self):
    #     data = self.cleaned_data
    #     if data.get('password') == data.get('password2'):
    #         return data.get('password')
    #     else:
    #         raise forms.ValidationError("Password input is inconsistent, please retry.")