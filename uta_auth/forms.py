from django import forms
from django.contrib.auth.models import User
from uta_auth.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name' , 'email', 'password')

class Student(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('name',)

class Instructor(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = ('department',)