from django import forms
from django.contrib.auth.models import User
from uta_models.models import *
from django.contrib.auth.forms import UserChangeForm


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


class UserUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class StudentUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']

    class Meta:
        model = Student
        fields = ('matriculationNumber', 'department', 'lvlOfStudy')


class InstructorUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(InstructorUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']

    class Meta:
        model = Instructor
        fields = ()

