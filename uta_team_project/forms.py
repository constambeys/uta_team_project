from django import forms
from uta_models.models import *


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'instructor', 'course', 'requirements', 'deadline')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'students')


class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('qualifications', 'min_group_size', 'max_group_size')



class CourseAssignmentForm(forms.Form):
    course_assignment = forms.ModelChoiceField(queryset=Assignment.objects.all().order_by('name'))

