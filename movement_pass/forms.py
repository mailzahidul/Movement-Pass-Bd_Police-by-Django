from django import forms
from django.contrib.model import User

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=(forms.TextInput(attrs={'class':'form-control'})))
    password = forms.PasswordField(widget=(forms.PasswordInput(attrs={'class':'form-control'})))
