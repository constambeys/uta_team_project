from django import forms
from django.contrib.auth.models import User
from uta_models.models import *

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ('name', 'instructor', 'course', 'requirements')

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'students')