from django import forms
from django.contrib.auth.models import User
from uta_models.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('matriculationNumber', 'department', 'lvlOfStudy')


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ()
